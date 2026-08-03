"""Fetch L1 (native) speaker counts from Wikidata and build data/processed/l1_speakers.csv.

Source choice
-------------
Wikidata property P1098 ("number of speakers, writers, or signers") on items that
carry an ISO 639-3 code (P220). Wikidata's figures are overwhelmingly imported from
Ethnologue (the 2019 = Ethnologue 22 import is the largest batch), so provenance is
effectively "Ethnologue via Wikidata", but the data is CC0, machine-readable via
SPARQL, and covers ~1,900 ISO 639-3 codes - far more than Wikipedia's
"List of languages by number of native speakers" tables (~top 100).

Selection policy (documented in notes/phoneme-prevalence.md):
1. Drop deprecated-rank statements.
2. If a statement is qualified with P518 (applies to part) = Q36870 "first language",
   it is an explicit L1 figure. Every major lingua franca (eng, cmn, spa, hin, fra,
   arb, ...) has one, which is where L1-vs-total confusion would actually distort
   population weighting. Among these: prefer PreferredRank, then latest point-in-time
   (P585), then the larger value (deterministic tie-break).
3. Otherwise fall back to statements with NO P518 qualifier (unqualified Ethnologue
   imports for smaller languages are L1/"all users" figures; for languages outside
   the top ~30 the L1~=total approximation is a project convention). Same tie-break.
   Statements qualified as "second language" (Q125421), "whole"/totals, or with
   territorial qualifiers (e.g. "applies to part: Russia") are never used.
4. Languages with only L2/total/territorial figures are excluded.

Output columns: iso639_3, glottocode, name, l1_speakers, year, source_note.

Also downloads the SIL ISO 639-3 code table (iso-639-3.tab), which provides the
ISO 639-1 (two-letter) <-> 639-3 mapping needed to join CLDR BCP-47 codes.

Usage: uv run python scripts/fetch_l1_speakers.py [--offline]
  --offline: skip downloads, rebuild the CSV from cached raw files.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd
import requests

ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = ROOT / "data" / "raw" / "wikidata_l1"
ISO_DIR = ROOT / "data" / "raw" / "iso639"
OUT_CSV = ROOT / "data" / "processed" / "l1_speakers.csv"
GLOTTOLOG_LANGS = ROOT / "data" / "raw" / "glottolog-cldf" / "cldf" / "languages.csv"

SPARQL_ENDPOINT = "https://query.wikidata.org/sparql"
USER_AGENT = "interlang-research/0.1 (https://github.com/pthill; kevin.patrick.thill@gmail.com)"
ISO_TAB_URL = "https://iso639-3.sil.org/sites/iso639-3/files/downloads/iso-639-3.tab"

Q_FIRST_LANGUAGE = "Q36870"

# Per-language corrections applied after the generic selection policy.
# arb: Wikidata/Ethnologue attach the macro-Arabic total (335M) to "Standard
# Arabic", but MSA has essentially no native speakers - everyone's L1 is a
# regional variety (arz, arq, apd, ary, apc, ... which are listed separately,
# so keeping arb would double-count ~335M and attach them to PHOIBLE's
# 3-vowel MSA inventory). MSA keeps its CLDR *total*-speaker weight (ease
# term) - the L1 zero applies to the representation term only.
# See notes/contrast-study.md "Addendum".
L1_OVERRIDES = {
    "arb": (0, "override: MSA has ~no L1 speakers; macro-Arabic total lives on the varieties"),
}

QUERY = """
SELECT ?item ?iso ?speakers ?applies ?time ?rank WHERE {
  ?item wdt:P220 ?iso .
  ?item p:P1098 ?st .
  ?st ps:P1098 ?speakers .
  ?st wikibase:rank ?rank .
  OPTIONAL { ?st pq:P518 ?applies }
  OPTIONAL { ?st pq:P585 ?time }
}
"""


def fetch_raw() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    ISO_DIR.mkdir(parents=True, exist_ok=True)

    print("Querying Wikidata SPARQL (P1098 statements on items with ISO 639-3)...")
    r = requests.get(
        SPARQL_ENDPOINT,
        params={"query": QUERY, "format": "json"},
        headers={"User-Agent": USER_AGENT},
        timeout=300,
    )
    r.raise_for_status()
    (RAW_DIR / "p1098_raw.json").write_text(r.text)
    print(f"  wrote {RAW_DIR / 'p1098_raw.json'} ({len(r.text):,} bytes)")

    print("Downloading SIL ISO 639-3 code table...")
    r = requests.get(ISO_TAB_URL, headers={"User-Agent": USER_AGENT}, timeout=120)
    r.raise_for_status()
    (ISO_DIR / "iso-639-3.tab").write_text(r.text)
    print(f"  wrote {ISO_DIR / 'iso-639-3.tab'} ({len(r.text):,} bytes)")


def build_csv() -> None:
    raw = json.loads((RAW_DIR / "p1098_raw.json").read_text())
    rows = []
    for b in raw["results"]["bindings"]:
        try:
            float(b["speakers"]["value"])
        except ValueError:
            continue  # "unknown value" statements come back as genid URIs
        rows.append(
            {
                "qid": b["item"]["value"].rsplit("/", 1)[-1],
                "iso639_3": b["iso"]["value"],
                "speakers": float(b["speakers"]["value"]),
                "applies": b.get("applies", {}).get("value", "").rsplit("/", 1)[-1],
                "time": b.get("time", {}).get("value", ""),
                "rank": b["rank"]["value"].rsplit("#", 1)[-1],
            }
        )
    df = pd.DataFrame(rows)
    df = df[df["rank"] != "DeprecatedRank"].copy()
    df["rank_order"] = df["rank"].map({"PreferredRank": 0, "NormalRank": 1}).fillna(2)
    df["year"] = df["time"].str.slice(0, 4)
    df["year"] = pd.to_numeric(df["year"], errors="coerce")
    # some ISO codes appear only in uppercase/whitespace-damaged form; normalize
    df["iso639_3"] = df["iso639_3"].str.strip().str.lower()
    df = df[df["iso639_3"].str.fullmatch(r"[a-z]{3}")]

    # Drop ISO 639-3 *macrolanguage* codes (zho, ara, msa, ...): their individual
    # member languages (cmn, wuu, arb, apc, ...) are counted separately, so keeping
    # both would double-count populations. PHOIBLE inventories are attached to
    # individual languages anyway.
    iso_tab = pd.read_csv(ISO_DIR / "iso-639-3.tab", sep="\t", dtype=str)
    macro = set(iso_tab.loc[iso_tab["Scope"] == "M", "Id"])
    n_macro = df["iso639_3"].isin(macro).sum()
    df = df[~df["iso639_3"].isin(macro)]
    print(f"Dropped {n_macro} statements on macrolanguage codes (double-counting risk)")

    def pick(group: pd.DataFrame) -> pd.Series | None:
        for subset, note in (
            (group[group["applies"] == Q_FIRST_LANGUAGE], "wikidata P1098 (first-language qualified)"),
            (group[group["applies"] == ""], "wikidata P1098 (unqualified, assumed L1)"),
        ):
            if len(subset):
                best = subset.sort_values(
                    by=["rank_order", "year", "speakers"],
                    ascending=[True, False, False],
                    na_position="last",
                ).iloc[0]
                return pd.Series(
                    {
                        "l1_speakers": int(best["speakers"]),
                        "year": int(best["year"]) if pd.notna(best["year"]) else "",
                        "source_note": note,
                    }
                )
        return None  # only L2/total/territorial figures -> exclude

    picked = (
        df.groupby("iso639_3")[df.columns]
        .apply(pick)
        .dropna(how="all")
        .reset_index()
    )

    # Attach names and glottocodes from Glottolog.
    gl = pd.read_csv(GLOTTOLOG_LANGS, usecols=["Name", "Glottocode", "ISO639P3code"])
    gl = gl.dropna(subset=["ISO639P3code"]).drop_duplicates("ISO639P3code")
    picked = picked.merge(
        gl.rename(
            columns={"ISO639P3code": "iso639_3", "Glottocode": "glottocode", "Name": "name"}
        ),
        on="iso639_3",
        how="left",
    )
    picked["l1_speakers"] = picked["l1_speakers"].astype(int)
    for iso, (n, note) in L1_OVERRIDES.items():
        hit = picked["iso639_3"] == iso
        picked.loc[hit, "l1_speakers"] = n
        picked.loc[hit, "source_note"] = note
    picked = picked[["iso639_3", "glottocode", "name", "l1_speakers", "year", "source_note"]]
    picked = picked.sort_values("l1_speakers", ascending=False)
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    picked.to_csv(OUT_CSV, index=False)
    print(f"Wrote {OUT_CSV}: {len(picked):,} languages")
    print(picked.head(15).to_string(index=False))


if __name__ == "__main__":
    if "--offline" not in sys.argv:
        fetch_raw()
    build_csv()
