"""Phoneme prevalence study: which sounds do the world's speakers have?

For every phoneme (segment) in PHOIBLE, computes three prevalence measures over
the universe of 2,177 PHOIBLE languages:

  pct_languages      unweighted: share of languages whose inventory has the segment
  pct_l1_weighted    share of L1 (native) speakers whose native language has it
                     (L1 counts from data/processed/l1_speakers.csv, Wikidata/Ethnologue)
  pct_total_weighted share of speaker-language pairs weighted by TOTAL speakers
                     (CLDR territory data), approximating "share of people who have
                     the sound in ANY language they speak". Overcounts multilinguals:
                     a person counts once per language they speak.

Two symbol-granularity levels are produced:

  strict  PHOIBLE Value symbols as-is (/t̪/ and /t/ are different segments)
  lumped  diacritic-level variation judged perceptually negligible is collapsed
          (see LUMP_* below for the exact rules)

Key policies (documented in notes/phoneme-prevalence.md, "Judgment calls"):
  - Multi-inventory languages: majority vote - a segment counts as present in a
    language if it appears in >= 50% of that language's PHOIBLE inventories.
  - Marginal segments: would be excluded, but this CLDF export contains no
    Marginal=True rows, so the filter is a no-op.
  - Languages missing from the L1 source get a default of 10,000 L1 speakers
    (keeps them in the denominator; total effect < 0.1% of world population).
  - Languages missing from CLDR get total := L1 (project convention, principles §3.8).
  - Tone "segments" are excluded from the ranking output.

Inputs (all local; run scripts/fetch_l1_speakers.py first):
  data/raw/phoible/cldf/{values,languages,parameters}.csv
  data/processed/l1_speakers.csv
  data/raw/cldr_supplementalData.xml
  data/raw/iso639/iso-639-3.tab

Output: data/processed/phoneme_prevalence.csv  (full ranked table, both levels)

Usage: uv run python scripts/phoneme_prevalence.py
"""

from __future__ import annotations

import unicodedata
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
PHOIBLE = ROOT / "data" / "raw" / "phoible" / "cldf"
L1_CSV = ROOT / "data" / "processed" / "l1_speakers.csv"
CLDR_XML = ROOT / "data" / "raw" / "cldr_supplementalData.xml"
ISO_TAB = ROOT / "data" / "raw" / "iso639" / "iso-639-3.tab"
OUT_CSV = ROOT / "data" / "processed" / "phoneme_prevalence.csv"

L1_DEFAULT = 10_000  # L1 speakers assumed for PHOIBLE languages absent from the L1 source

# ---------------------------------------------------------------------------
# Lumping rules (the "lumped" symbol level)
# ---------------------------------------------------------------------------
# Diacritics stripped because the variation they encode is judged perceptually
# negligible for a learner recognizing a sound category (sub-place, fine height,
# length, syllabicity, release detail). Phonation (voicing, aspiration, breathy,
# creaky), nasalization, ejective, palatalization/labialization/velarization,
# and retroflexion are deliberately KEPT - those are salient category differences.
LUMP_STRIP = set(
    "ː"  # ː long
    "ˑ"  # ˑ half-long
    "̆"  # ̆ extra-short
    "̪"  # ̪ dental
    "̺"  # ̺ apical
    "̻"  # ̻ laminal
    "̟"  # ̟ advanced
    "̠"  # ̠ retracted
    "̈"  # ̈ centralized (ä -> a)
    "̽"  # ̽ mid-centralized
    "̝"  # ̝ raised
    "̞"  # ̞ lowered (e̞ -> e)
    "̩"  # ̩ syllabic
    "̯"  # ̯ non-syllabic
    "̚"  # ̚ unreleased
    "͡"  # ͡ tie bar above
    "͜"  # ͜ tie bar below
    "ʰ"  # ʰ aspirated - for PRESENCE counting only: languages analyzed with /kʰ tʰ pʰ/
    "ʱ"  # ʱ breathy release   as their sole voiceless-stop series (6 of 9 English
         #   inventories, Standard Arabic, ...) do have k-like/t-like sounds. The
         #   aspiration CONTRAST is a separate question (principles §3.3) and is
         #   preserved at the strict level.
)
# Whole-symbol merges applied after diacritic stripping.
LUMP_MAP = {
    "ɡ": "ɡ",  # ɡ stays ɡ (identity, listed for clarity)
    "g": "ɡ",       # ASCII g -> IPA ɡ (lookalike safety; PHOIBLE itself is clean)
    # Coronal rhotics -> one r-category (principles §3.4: "any rhotic counts as
    # /r/"). Uvular ʀ ʁ are NOT lumped: ʁ doubles as a plain fricative (Arabic
    # ghayn) and merging it would miscount non-rhotic uses.
    "ɾ": "r",       # ɾ tap
    "ɹ": "r",       # ɹ approximant (English r)
    "ɻ": "r",       # ɻ retroflex approximant
    "ɽ": "r",       # ɽ retroflex flap
    "ɑ": "a",       # ɑ (back low) -> a: low-vowel quality variants as one /a/
    "ɐ": "a",       # ɐ (near-low central) -> a
}


def lump(symbol: str) -> str:
    s = unicodedata.normalize("NFD", symbol)
    s = "".join(ch for ch in s if ch not in LUMP_STRIP)
    s = unicodedata.normalize("NFC", s)
    s = "".join(LUMP_MAP.get(ch, ch) for ch in s)
    return s if s else symbol


def light_lump(symbol: str) -> str:
    """Diacritic-strip only (keeps aspiration and rhotic identity).

    Used to normalize the Allophones column for display: [t̠ʃ] as an "allophone"
    of /tʃ/ is pure notation noise and is folded away, while genuinely
    informative realizations like [kʰ] for /k/ or [ɾ] for /r/ are kept.
    """
    keep = LUMP_STRIP - {"ʰ", "ʱ"}
    s = unicodedata.normalize("NFD", symbol)
    s = "".join(ch for ch in s if ch not in keep)
    return unicodedata.normalize("NFC", s) or symbol


# "Wide phoneme" candidate classes (principles §3.4): unions of lumped symbols
# that plausibly form one recognizable category across languages. Reported as
# extra rows with level="class".
WIDE_CLASSES = {
    "R-class (r ɾ ɹ ɻ ɽ ʀ ʁ)": {"r", "ʀ", "ʁ"},          # r already contains taps/approximants
    "SH-class (ʃ ʂ ɕ)": {"ʃ", "ʂ", "ɕ"},
    "CH-class (tʃ tʂ tɕ c)": {"tʃ", "tʂ", "tɕ", "c"},
    "H-class (h x χ ħ)": {"h", "x", "χ", "ħ"},
    "F-class (f ɸ)": {"f", "ɸ"},
    "W-class (w ʋ)": {"w", "ʋ"},
    "L-class (l ɭ ʎ)": {"l", "ɭ", "ʎ"},
}


# ---------------------------------------------------------------------------
# CLDR total-speaker counts (BCP-47 -> ISO 639-3)
# ---------------------------------------------------------------------------
# CLDR macrolanguage / umbrella codes mapped to the individual ISO 639-3 language
# that carries the bulk of the speakers (lossy - documented in the report).
MACRO_MAP = {
    "zho": "cmn",  # Chinese -> Mandarin
    "ara": "arb",  # Arabic -> Modern Standard Arabic
    "msa": "zsm",  # Malay -> Standard Malay
    "fas": "pes",  # Persian -> Iranian Persian
    "swa": "swh",  # Swahili -> coastal Swahili
    "kur": "kmr",  # Kurdish -> Northern Kurdish (Kurmanji)
    "aze": "azj",  # Azerbaijani -> North Azerbaijani
    "uzb": "uzn",  # Uzbek -> Northern Uzbek
    "orm": "gaz",  # Oromo -> West Central Oromo
    "pus": "pbu",  # Pashto -> Northern Pashto
    "que": "quz",  # Quechua -> Cusco Quechua
    "grn": "gug",  # Guarani -> Paraguayan Guarani
    "mlg": "plt",  # Malagasy -> Plateau Malagasy
    "mon": "khk",  # Mongolian -> Halh Mongolian
    "nep": "npi",  # Nepali
    "ori": "ory",  # Odia
    "sqi": "als",  # Albanian -> Tosk
    "est": "ekk",  # Estonian
    "lav": "lvs",  # Latvian
    "yid": "ydd",  # Yiddish -> Eastern Yiddish
    "ful": "fuv",  # Fulah -> Nigerian Fulfulde
    "aym": "ayr",  # Aymara -> Central Aymara
    "zha": "zyb",  # Zhuang -> Yongbei Zhuang
    "srd": "src",  # Sardinian -> Logudorese
    "lah": "pnb",  # Lahnda -> Western Panjabi (101M in CLDR)
    "bal": "bcc",  # Balochi -> Southern Balochi
    "nor": "nob",  # Norwegian -> Bokmål
    "aka": "twi",  # Akan -> Twi
    "mwr": "rwr",  # Marwari (India)
    "kok": "knn",  # Konkani -> Maharashtrian Konkani
    "doi": "dgo",  # Dogri
    "bik": "bcl",  # Bikol -> Central Bikol
    "zza": "diq",  # Zaza -> Dimli
    "man": "emk",  # Mandingo -> Eastern Maninkakan
    "kpe": "gkp",  # Kpelle -> Guinea Kpelle
    "gon": "gno",  # Gondi -> Northern Gondi
    "tmh": "thv",  # Tamashek -> Tahaggart Tamahaq
    "kon": "kng",  # Kongo -> Koongo
}


def cldr_totals() -> tuple[dict[str, float], pd.DataFrame]:
    """Total (any-proficiency) speakers per ISO 639-3 code from CLDR."""
    iso_tab = pd.read_csv(ISO_TAB, sep="\t", dtype=str)
    part1_to_3 = dict(zip(iso_tab["Part1"].dropna(), iso_tab.loc[iso_tab["Part1"].notna(), "Id"]))
    macro_codes = set(iso_tab.loc[iso_tab["Scope"] == "M", "Id"])

    root = ET.parse(CLDR_XML).getroot()
    totals: Counter[str] = Counter()
    for terr in root.iter("territory"):
        pop = float(terr.get("population", 0) or 0)
        if pop <= 0:
            continue
        for lp in terr.findall("languagePopulation"):
            code = lp.get("type")
            pct = float(lp.get("populationPercent", 0) or 0)
            base = code.split("_")[0]  # zh_Hant -> zh, pa_Arab -> pa (lossy, documented)
            totals[base] += pop * pct / 100.0

    mapped: Counter[str] = Counter()
    unmapped_macros: Counter[str] = Counter()
    for code, n in totals.items():
        iso3 = part1_to_3.get(code, code) if len(code) == 2 else code
        if iso3 in macro_codes:
            if iso3 in MACRO_MAP:
                iso3 = MACRO_MAP[iso3]
            else:
                unmapped_macros[iso3] += n
        mapped[iso3] += n
    big_unmapped = {k: v for k, v in unmapped_macros.items() if v > 1e6}
    if big_unmapped:
        print(f"  NOTE: unmapped macrolanguage codes with >1M speakers: {big_unmapped}")
    report = pd.DataFrame(
        sorted(mapped.items(), key=lambda kv: -kv[1]), columns=["iso639_3", "total_speakers"]
    )
    return dict(mapped), report


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    values = pd.read_csv(PHOIBLE / "values.csv", low_memory=False)
    langs = pd.read_csv(PHOIBLE / "languages.csv")
    params = pd.read_csv(PHOIBLE / "parameters.csv", low_memory=False)
    seg_class = dict(zip(params["ID"], params["SegmentClass"]))
    values["segment_class"] = values["Parameter_ID"].map(seg_class)

    # Marginal policy: exclude marginal segments. (This CLDF export contains no
    # Marginal=True rows - only False/blank - so this is a documented no-op.)
    values = values[values["Marginal"] != True]  # noqa: E712

    n_inv_per_lang = values.groupby("Language_ID")["Inventory_ID"].nunique()

    # --- population weights per PHOIBLE language --------------------------
    l1 = pd.read_csv(L1_CSV)
    l1_by_iso = dict(zip(l1["iso639_3"], l1["l1_speakers"]))
    l1_by_glotto = dict(
        zip(l1.loc[l1["glottocode"].notna(), "glottocode"],
            l1.loc[l1["glottocode"].notna(), "l1_speakers"])
    )
    totals_by_iso, _ = cldr_totals()

    lang_meta = langs.set_index("ID")
    weights = {}
    n_l1_joined = n_total_joined = 0
    for lid in n_inv_per_lang.index:
        iso = lang_meta.at[lid, "ISO639P3code"] if lid in lang_meta.index else None
        glotto = lang_meta.at[lid, "Glottocode"] if lid in lang_meta.index else None
        w_l1 = l1_by_iso.get(iso, l1_by_glotto.get(glotto))
        if w_l1 is not None:
            n_l1_joined += 1
        else:
            w_l1 = L1_DEFAULT
        w_total = totals_by_iso.get(iso)
        if w_total is not None:
            n_total_joined += 1
        else:
            w_total = w_l1  # CLDR-missing fallback: total := L1 (principles §3.8)
        weights[lid] = (float(w_l1), float(w_total))

    W = pd.DataFrame.from_dict(weights, orient="index", columns=["w_l1", "w_total"])
    sum_l1, sum_total, n_langs = W["w_l1"].sum(), W["w_total"].sum(), len(W)
    print(f"PHOIBLE languages: {n_langs}")
    print(f"  joined to L1 source: {n_l1_joined} ({n_l1_joined / n_langs:.1%}); "
          f"L1 population covered: {sum_l1:,.0f} "
          f"({sum_l1 / l1['l1_speakers'].sum():.1%} of L1-source world total)")
    print(f"  joined to CLDR totals: {n_total_joined}; person-language weight total: {sum_total:,.0f}")

    # --- presence per (language, symbol) at both levels --------------------
    values["lumped"] = values["Value"].map(lump)

    def presence(df: pd.DataFrame, col: str) -> pd.DataFrame:
        """Majority-across-inventories presence: (Language_ID, symbol) rows."""
        cnt = (
            df.drop_duplicates(["Language_ID", "Inventory_ID", col])
            .groupby(["Language_ID", col])
            .size()
            .rename("n_inv_with")
            .reset_index()
        )
        cnt["n_inv"] = cnt["Language_ID"].map(n_inv_per_lang)
        return cnt[cnt["n_inv_with"] * 2 >= cnt["n_inv"]][["Language_ID", col]].rename(
            columns={col: "symbol"}
        )

    # --- allophone tallies (deduped per language) ---------------------------
    allo_rows = values.dropna(subset=["Allophones"])

    def allophone_summary(sym_col: str) -> dict[str, str]:
        """Per symbol: observed allophones ranked by number of languages listing them."""
        counters: dict[str, Counter[str]] = {}
        seen = set()
        for lid, sym, allo in zip(
            allo_rows["Language_ID"], allo_rows[sym_col], allo_rows["Allophones"]
        ):
            for a in str(allo).split():
                a = light_lump(a)
                key = (lid, sym, a)
                if key in seen or a == sym or a == light_lump(sym):
                    continue
                seen.add(key)
                counters.setdefault(sym, Counter())[a] += 1
        return {
            sym: " ".join(f"{a}({n})" for a, n in c.most_common(8))
            for sym, c in counters.items()
        }

    results = []
    for level, col in (("strict", "Value"), ("lumped", "lumped")):
        pres = presence(values, col)
        # modal segment class per symbol
        cls = (
            values.groupby(col)["segment_class"]
            .agg(lambda s: s.mode().iat[0] if len(s.mode()) else "")
            .to_dict()
        )
        pres = pres.join(W, on="Language_ID")
        agg = pres.groupby("symbol").agg(
            n_languages=("Language_ID", "nunique"),
            l1_with=("w_l1", "sum"),
            total_with=("w_total", "sum"),
        )
        allo = allophone_summary(col)
        agg["level"] = level
        agg["segment_class"] = agg.index.map(cls)
        agg["pct_languages"] = agg["n_languages"] / n_langs
        agg["pct_l1_weighted"] = agg["l1_with"] / sum_l1
        agg["pct_total_weighted"] = agg["total_with"] / sum_total
        agg["top_allophones"] = agg.index.map(lambda s: allo.get(s, ""))
        if level == "lumped":
            variants = (
                values[values["Value"] != values["lumped"]]
                .groupby("lumped")["Value"]
                .agg(lambda s: " ".join(sorted(set(s))))
                .to_dict()
            )
            agg["merged_strict_variants"] = agg.index.map(lambda s: variants.get(s, ""))
        else:
            agg["merged_strict_variants"] = ""
        results.append(agg.reset_index())
        if level == "lumped":
            lumped_pres = pres  # keep for wide-class unions below

    # --- wide-class unions (level="class") ---------------------------------
    class_rows = []
    for cname, members in WIDE_CLASSES.items():
        sub = lumped_pres[lumped_pres["symbol"].isin(members)]
        by_lang = sub.drop_duplicates("Language_ID")
        class_rows.append(
            {
                "symbol": cname,
                "level": "class",
                "segment_class": "consonant",
                "n_languages": len(by_lang),
                "l1_with": by_lang["w_l1"].sum(),
                "total_with": by_lang["w_total"].sum(),
                "pct_languages": len(by_lang) / n_langs,
                "pct_l1_weighted": by_lang["w_l1"].sum() / sum_l1,
                "pct_total_weighted": by_lang["w_total"].sum() / sum_total,
                "top_allophones": "",
                "merged_strict_variants": " ".join(sorted(members)),
            }
        )
    results.append(pd.DataFrame(class_rows))

    out = pd.concat(results, ignore_index=True)
    out = out[out["segment_class"] != "tone"]  # tones are not candidate segments
    out = out.sort_values(["level", "pct_l1_weighted"], ascending=[False, False])
    out = out[
        ["level", "symbol", "segment_class", "n_languages", "pct_languages",
         "pct_l1_weighted", "pct_total_weighted", "l1_with", "total_with",
         "top_allophones", "merged_strict_variants"]
    ]
    for c in ("pct_languages", "pct_l1_weighted", "pct_total_weighted"):
        out[c] = out[c].round(5)
    out[["l1_with", "total_with"]] = out[["l1_with", "total_with"]].round(0).astype("int64")
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(OUT_CSV, index=False)
    print(f"Wrote {OUT_CSV}: {len(out)} rows "
          f"({(out['level'] == 'strict').sum()} strict, {(out['level'] == 'lumped').sum()} lumped)")

    top = out[out["level"] == "lumped"].head(20)
    print("\nTop 20 (lumped, by L1-weighted share):")
    print(
        top[["symbol", "segment_class", "pct_l1_weighted", "pct_total_weighted", "pct_languages"]]
        .to_string(index=False)
    )


if __name__ == "__main__":
    main()
