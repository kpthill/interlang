"""Population weights shared by the prevalence studies.

Two weighting conventions are used across the project (see
`notes/phoneme-prevalence.md`):

  L1-weighted     share of *native* speakers, from `data/processed/l1_speakers.csv`
                  (Wikidata P1098, built by `scripts/fetch_l1_speakers.py`).
  total-weighted  share of *speaker-language pairs* weighted by CLDR total-speaker
                  (L1 + L2) counts. A person counts once per language they speak,
                  so multilinguals are overcounted; the denominator absorbs most of
                  it. This is a weighting convention, not a head count.

This module owns the CLDR side, which is the fiddly half: CLDR keys its
`languagePopulation` records by BCP-47 code, everything else in the project joins
on ISO 639-3, and CLDR uses macrolanguage codes where we use individual ones.

Judgment calls baked in here (they match `notes/phoneme-prevalence.md` §6, which
is where they were first made and documented):
  - Script and region subtags are stripped and summed (`zh_Hant` + `zh` -> `zh`).
    Lossy: `pa_Arab` is really Western Panjabi but folds into `pa`/`pan`.
  - Macrolanguage codes are mapped to their dominant individual language
    (`MACRO_MAP`), attributing all of the macro population to one member.
  - ISO 639-1 -> 639-3 needs a code table. `iso-639-3.tab` from SIL is preferred;
    `language-codes-full.csv` (the datasets/language-codes mirror) is accepted as
    a fallback because sil.org is not always reachable. The fallback lacks the
    `Scope` column, so the "unmapped macrolanguage" warning is silently skipped
    when it is used - `MACRO_MAP` is still applied.

NOTE: `scripts/phoneme_prevalence.py` still carries an older inline copy of this
logic. It was left alone so that a finished study keeps producing byte-identical
output; migrate it here the next time that script is touched.
"""

from __future__ import annotations

import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path

import pandas as pd

# CLDR macrolanguage / umbrella codes -> the individual ISO 639-3 language that
# carries the bulk of the speakers (lossy - documented in the study write-ups).
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
    "lah": "pnb",  # Lahnda -> Western Panjabi
    "bal": "bcc",  # Balochi -> Southern Balochi
    "nor": "nob",  # Norwegian -> Bokmal
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


def read_l1_speakers(path: Path) -> pd.DataFrame:
    """Read `l1_speakers.csv` without letting pandas eat ISO code `nan`.

    ISO 639-3 `nan` is Min Nan Chinese (50.1M L1). With pandas' default NA
    handling it is parsed as a float NaN, which both loses the language and turns
    the code column into a NaN-keyed trap for `dict.get(...)` lookups on any
    other language whose code is missing. Always read it through here.
    """
    return pd.read_csv(path, keep_default_na=False, na_values=[""])


def cldr_totals(cldr_xml: Path, iso_dir: Path) -> dict[str, float]:
    """Total (any-proficiency) speakers per ISO 639-3 code, from CLDR."""
    part1_to_3, macro_codes = _iso_tables(iso_dir)

    root = ET.parse(cldr_xml).getroot()
    totals: Counter[str] = Counter()
    for terr in root.iter("territory"):
        pop = float(terr.get("population", 0) or 0)
        if pop <= 0:
            continue
        for lp in terr.findall("languagePopulation"):
            base = lp.get("type").split("_")[0]  # zh_Hant -> zh (lossy, documented)
            pct = float(lp.get("populationPercent", 0) or 0)
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
        elif iso3 in MACRO_MAP:  # fallback table has no Scope column
            iso3 = MACRO_MAP[iso3]
        mapped[iso3] += n
    big = {k: round(v) for k, v in unmapped_macros.items() if v > 1e6}
    if big:
        print(f"  NOTE: unmapped macrolanguage codes with >1M speakers: {big}")
    return dict(mapped)


def _iso_tables(iso_dir: Path) -> tuple[dict[str, str], set[str]]:
    """(ISO 639-1 -> 639-3 map, set of macrolanguage codes) from whichever table is present."""
    sil = iso_dir / "iso-639-3.tab"
    if sil.exists():
        tab = pd.read_csv(sil, sep="\t", dtype=str)
        part1 = dict(zip(tab["Part1"].dropna(), tab.loc[tab["Part1"].notna(), "Id"]))
        return part1, set(tab.loc[tab["Scope"] == "M", "Id"])

    mirror = iso_dir / "language-codes-full.csv"
    if mirror.exists():
        tab = pd.read_csv(mirror, dtype=str)
        # alpha3-t (terminological) where it exists, else alpha3-b (bibliographic):
        # 639-2/B differs from 639-3 for ~20 languages (ger/deu, fre/fra, ...).
        iso3 = tab["alpha3-t"].fillna(tab["alpha3-b"])
        part1 = dict(zip(tab["alpha2"].dropna(), iso3[tab["alpha2"].notna()]))
        return part1, set()  # no Scope column; MACRO_MAP is applied unconditionally

    raise FileNotFoundError(
        f"no ISO 639 code table under {iso_dir}: expected iso-639-3.tab "
        f"(scripts/fetch_l1_speakers.py) or language-codes-full.csv (see README)"
    )
