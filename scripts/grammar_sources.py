"""Audit the three grammar-typology sources BEFORE any number from them is quoted.

principles.md 3.2 says grammar is hand-designed from typology with a data citation
per decision, and 7 records that WALS's coverage is population-correlated in a way
that already flipped one conclusion (the stress rule).  This script is the
equivalent check for the grammar phase: it establishes, per source, what fraction
of humanity is actually behind any given percentage, before the grammar agenda
starts leaning on them.

Sources audited
---------------
  WALS      typological features, doculect-level, already in data/raw (192 features)
  Grambank  binary morphosyntactic features, language-level (195 features)
  APiCS     contact-language features, the LEARNABILITY anchor (336 features)

Division of labour agreed with Patrick 2026-08-05:
  - APiCS/creoles are the NORTH STAR - they are the natural experiment in what
    adults converge on under time pressure, which is the actual objective.
  - Grambank is a SANITY CHECK and tiebreaker, used mainly to catch Eurocentric
    defaults, not as a source of answers.
  - WALS supplies the word-order chapters Grambank does not code.

The two creole rules this script operationalises (both are bias controls, and
both are the same move as the cluster-repairing/European recipient split in
international-vocab.md 6.2):

  RULE 1 (cross-lexifier convergence).  A creole feature counts as evidence of
  learnability only where creoles converge ACROSS LEXIFIER FAMILIES.  80% of
  APiCS has a Western-European lexifier, so agreement among those alone is
  indistinguishable from inheritance.

  RULE 2 (divergence from the lexifier).  Where creoles DIFFER from their own
  lexifier, that is strong evidence even within one lexifier family, because
  inheritance is exactly what it rules out - the feature was available and was
  dropped (Patrick, 2026-08-05).  Its contrapositive is the useful sanity check
  on any Euro-coded feature we are minded to keep: do European-lexifier creoles
  keep it too?  Requires the lexifier's own value, so it only runs on the 48
  APiCS parameters carrying a WALS_ID.

Policies baked in here
----------------------
  - Doculect deduplication.  WALS is doculect-level (11 Basque varieties, 10
    Arabic).  Everything is deduplicated on Glottocode before any population
    weighting, taking the FIRST value for a (glottocode, feature); otherwise a
    well-described language counts many times.
  - Grambank dialects and family-level entries are dropped (level == 'language'
    only), for the same reason.
  - Population weighting reuses interlang.populations: L1 from Wikidata P1098,
    total (L1+L2) from CLDR, joined on ISO 639-3 with Glottocode as the fallback
    key.  Both are reported because they disagree and the disagreement matters.
  - LEXIFIER GROUPING is a hand-made judgment call (LEXIFIER_GROUP below).
    APiCS's own `Lexifier` column has an "Other" bucket of 13 mixed cases; each
    is classified individually and the reasoning is in the table.  Russian-
    lexifier Chinese Pidgin Russian counts as European; Michif (French + Cree)
    counts as mixed and is excluded from both sides of Rule 1.
  - "Coverage" always means: has a non-'?' value.  Grambank codes uncertainty as
    '?' and it is frequent; counting it as coverage would overstate every number
    in this audit.

Usage:   uv run python scripts/grammar_sources.py
Inputs:  data/raw/{wals,grambank,apics}/cldf/*.csv
         data/processed/l1_speakers.csv, data/raw/cldr_supplementalData.xml
Outputs: data/processed/grammar_source_coverage.csv  (dataset x feature)
         data/processed/apics_lexifiers.csv          (APiCS language x lexifier group)
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from interlang.populations import cldr_totals, read_l1_speakers  # noqa: E402

RAW = ROOT / "data" / "raw"
L1_CSV = ROOT / "data" / "processed" / "l1_speakers.csv"
CLDR_XML = RAW / "cldr_supplementalData.xml"
ISO_DIR = RAW / "iso639"
OUT_COV = ROOT / "data" / "processed" / "grammar_source_coverage.csv"
OUT_LEX = ROOT / "data" / "processed" / "apics_lexifiers.csv"

GC_TO_ISO: dict[str, str] = {}   # filled by populations(); see the note there

# APiCS lexifier -> group.  Rule 1 needs "is this lexifier Western European?",
# because that is the bloc large enough to fake a universal on its own.
LEXIFIER_GROUP = {
    "English": "european", "Portuguese": "european", "French": "european",
    "Spanish": "european", "Dutch": "european",
    "Arabic": "non-european", "Bantu": "non-european", "Malay": "non-european",
}
# The 13 "Other" cases, classified by hand from the lexifier named in APiCS.
OTHER_GROUP = {
    "Sango": "non-european",                      # Ngbandi (Atlantic-Congo)
    "Sango (written)": "non-european",
    "Chinese Pidgin Russian": "european",         # Russian lexifier
    "Chinese Pidgin Russian (depidginized)": "european",
    "Chinuk Wawa": "non-european",                # Chinookan
    "Chinuk Wawa (Grand Ronde CW)": "non-european",
    "Mixed Ma’a/Mbugu": "non-european",           # Bantu + Cushitic
    "Yimas-Arafundi Pidgin": "non-european",      # Lower Sepik
    "Pidgin Hindustani": "non-european",          # Indo-Aryan, not European
    "Pidgin Hawaiian": "non-european",            # Austronesian
    "Eskimo Pidgin": "non-european",              # Eskimo-Aleut
    "Gurindji Kriol": "mixed",                    # Gurindji + English-lexifier Kriol
    "Michif": "mixed",                            # Cree + French
}

# Features the Tier 0 / Tier 1 grammar decisions actually rest on.
SPOTLIGHT_WALS = {
    "81A": "Order of Subject, Object and Verb",
    "85A": "Order of Adposition and NP",
    "86A": "Order of Genitive and Noun",
    "87A": "Order of Adjective and Noun",
    "90A": "Order of Relative Clause and Noun",
    "95A": "OV/VO vs adposition order (the correlation itself)",
    "20A": "Fusion of inflectional formatives",
    "22A": "Inflectional synthesis of the verb",
    "26A": "Prefixing vs suffixing",
    "30A": "Number of genders",
    "49A": "Number of cases",
    "98A": "Alignment of case marking",
    "100A": "Alignment of verbal person marking",
}
SPOTLIGHT_GB = {
    "GB130": "order of S and V (intransitive)",
    "GB131": "verb-initial?",
    "GB132": "verb-medial?",
    "GB133": "verb-final?",
    "GB136": "is core argument order fixed?",
    "GB074": "are there prepositions?",
    "GB065": "order of possessor and possessed",
    "GB024": "order of numeral and noun",
    "GB193": "order of property word and noun",
    "GB327": "can the relative clause follow the noun?",
    "GB020": "definite articles?",
    "GB021": "indefinite articles?",
    "GB051": "gender/noun class?",
    "GB082": "tense marking?",
}


# ---------------------------------------------------------------------------
# loading
# ---------------------------------------------------------------------------
def load(ds: str) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    d = RAW / ds / "cldf"
    langs = pd.read_csv(d / "languages.csv")
    params = pd.read_csv(d / "parameters.csv")
    vals = pd.read_csv(d / "values.csv", low_memory=False)
    return langs, params, vals


def populations() -> tuple[dict, dict, float, float]:
    l1 = read_l1_speakers(L1_CSV)
    by_iso = dict(zip(l1["iso639_3"], l1["l1_speakers"]))
    gc = l1[l1["glottocode"].astype(str) != ""]
    by_gc = dict(zip(gc["glottocode"], gc["l1_speakers"]))
    # Grambank carries NO ISO codes at all - it is Glottocode-only - so the
    # CLDR total-speaker table (keyed by ISO) is unreachable without this map.
    global GC_TO_ISO
    GC_TO_ISO = dict(zip(gc["glottocode"], gc["iso639_3"]))
    world_l1 = l1["l1_speakers"].sum()
    try:
        tot_iso = cldr_totals(CLDR_XML, ISO_DIR)
    except Exception as e:                                # pragma: no cover
        print(f"  ! CLDR totals unavailable ({e}); total-weighted columns omitted")
        tot_iso = {}
    world_tot = sum(tot_iso.values())
    return (by_iso, by_gc), tot_iso, world_l1, world_tot


def weight(langs: pd.DataFrame, l1_maps, tot_iso) -> pd.DataFrame:
    """Attach L1 and total-speaker weights to a CLDF languages table."""
    by_iso, by_gc = l1_maps
    iso = langs["ISO639P3code"].fillna("").astype(str)
    gcs = langs["Glottocode"].fillna("").astype(str)
    langs = langs.copy()
    langs["l1"] = [by_iso.get(i) or by_gc.get(g) or 0.0 for i, g in zip(iso, gcs)]
    langs["total"] = [tot_iso.get(i or GC_TO_ISO.get(g, ""), 0.0)
                      for i, g in zip(iso, gcs)]
    return langs


# ---------------------------------------------------------------------------
# coverage
# ---------------------------------------------------------------------------
def coverage(ds: str, langs: pd.DataFrame, vals: pd.DataFrame,
             params: pd.DataFrame, world_l1: float, world_tot: float,
             drop_unknown: bool = True) -> pd.DataFrame:
    v = vals[["Language_ID", "Parameter_ID", "Value"]].copy()
    if drop_unknown:
        v = v[v["Value"].astype(str) != "?"]
    key = langs.set_index("ID")
    v["glottocode"] = v["Language_ID"].map(key["Glottocode"])
    v["l1"] = v["Language_ID"].map(key["l1"]).fillna(0.0)
    v["total"] = v["Language_ID"].map(key["total"]).fillna(0.0)
    # doculect dedup: one value per (glottocode, feature)
    v = v[v["glottocode"].notna()]
    v = v.drop_duplicates(subset=["glottocode", "Parameter_ID"], keep="first")
    dedup_l1 = v.drop_duplicates("glottocode").set_index("glottocode")["l1"]
    dedup_tot = v.drop_duplicates("glottocode").set_index("glottocode")["total"]
    v["l1"] = v["glottocode"].map(dedup_l1)
    v["total"] = v["glottocode"].map(dedup_tot)

    g = v.groupby("Parameter_ID").agg(
        n_languages=("glottocode", "nunique"),
        l1_covered=("l1", "sum"), total_covered=("total", "sum"))
    g["l1_share"] = (100 * g["l1_covered"] / world_l1).round(1)
    g["total_share"] = (100 * g["total_covered"] / world_tot).round(1) if world_tot else float("nan")
    g["dataset"] = ds
    g["feature"] = g.index.map(params.set_index("ID")["Name"])
    return g.reset_index().rename(columns={"Parameter_ID": "feature_id"})


def top_language_check(langs: pd.DataFrame, vals: pd.DataFrame,
                       feature_ids: list[str], n: int = 20) -> pd.DataFrame:
    """Do the biggest languages actually have values? The population-correlation test."""
    big = (langs[langs["l1"] > 0].drop_duplicates("Glottocode")
           .nlargest(n, "l1")[["ID", "Name", "l1"]])
    v = vals[vals["Parameter_ID"].isin(feature_ids)]
    v = v[v["Value"].astype(str) != "?"]
    have = v.groupby("Language_ID")["Parameter_ID"].nunique()
    big = big.copy()
    big["features_present"] = big["ID"].map(have).fillna(0).astype(int)
    big["of"] = len(feature_ids)
    return big


def main() -> None:
    (l1_maps, tot_iso, world_l1, world_tot) = populations()
    print(f"world L1 in table: {world_l1/1e9:.2f}B; "
          f"CLDR total-speaker mass: {world_tot/1e9:.2f}B\n")

    cov_all, summary = [], []
    for ds in ("wals", "grambank", "apics"):
        langs, params, vals = load(ds)
        if ds == "grambank":
            langs = langs[langs["level"] == "language"]
            vals = vals[vals["Language_ID"].isin(set(langs["ID"]))]
        langs = weight(langs, l1_maps, tot_iso)
        cov = coverage(ds, langs, vals, params, world_l1, world_tot)
        cov_all.append(cov)
        n_lang = langs["Glottocode"].nunique()
        scored = vals[vals["Value"].astype(str) != "?"]
        summary.append(dict(
            dataset=ds, languages=n_lang, features=len(params),
            values=len(vals), values_scored=len(scored),
            density=round(len(scored) / (n_lang * len(params)), 3),
            median_feature_l1_share=cov["l1_share"].median(),
            max_feature_l1_share=cov["l1_share"].max()))
        globals()[f"_{ds}"] = (langs, params, vals)

    print("=== SOURCE SIZES AND DENSITY ===")
    print(pd.DataFrame(summary).to_string(index=False))
    print("\n`density` = scored values / (languages x features). `?` is not scored.")

    # ---- the population-correlation test ---------------------------------
    print("\n=== IS COVERAGE POPULATION-CORRELATED? "
          "(top 20 languages by L1, Tier-0/1 features only) ===")
    for ds, spot in (("wals", SPOTLIGHT_WALS), ("grambank", SPOTLIGHT_GB)):
        langs, params, vals = globals()[f"_{ds}"]
        t = top_language_check(langs, vals, list(spot))
        full = (t.features_present == t["of"]).sum()
        none = (t.features_present == 0).sum()
        print(f"\n{ds}: {full}/20 of the biggest languages have ALL "
              f"{len(spot)} spotlight features; {none}/20 have none")
        print(t.assign(l1=(t.l1 / 1e6).round(0))
              .rename(columns={"l1": "L1 (M)"})[["Name", "L1 (M)", "features_present", "of"]]
              .to_string(index=False))

    # ---- spotlight coverage ----------------------------------------------
    cov = pd.concat(cov_all, ignore_index=True)
    print("\n=== COVERAGE OF THE FEATURES TIER 0/1 RESTS ON ===")
    for ds, spot in (("wals", SPOTLIGHT_WALS), ("grambank", SPOTLIGHT_GB)):
        s = cov[(cov.dataset == ds) & (cov.feature_id.isin(spot))].copy()
        s["what"] = s.feature_id.map(spot)
        print(f"\n{ds}")
        print(s[["feature_id", "what", "n_languages", "l1_share", "total_share"]]
              .sort_values("l1_share", ascending=False).to_string(index=False))

    # ---- APiCS lexifier audit --------------------------------------------
    ap_l, ap_p, ap_v = globals()["_apics"]
    ap_l = ap_l.copy()
    ap_l["lexifier_group"] = [
        OTHER_GROUP.get(n, "non-european") if lx == "Other" else LEXIFIER_GROUP.get(lx, "?")
        for n, lx in zip(ap_l["Name"], ap_l["Lexifier"])]
    print("\n=== APiCS: THE CONFOUND, MEASURED ===")
    grp = ap_l.groupby(["lexifier_group", "Lexifier"]).size().rename("n").reset_index()
    print(grp.to_string(index=False))
    tot = ap_l.lexifier_group.value_counts()
    ded = ap_l.drop_duplicates("Glottocode")
    dtot = ded.lexifier_group.value_counts()
    print(f"\ndeduplicated on Glottocode: {len(ded)} independent languages "
          f"({dtot.get('european',0)} european / {dtot.get('non-european',0)} non-european "
          f"/ {dtot.get('mixed',0)} mixed)")
    print(f"\n{tot.get('european', 0)} of {len(ap_l)} APiCS lects "
          f"({100*tot.get('european',0)/len(ap_l):.0f}%) have a Western-European lexifier.")
    print(f"{tot.get('non-european', 0)} non-European, {tot.get('mixed', 0)} mixed.")
    joinable = ap_p["WALS_ID"].notna().sum()
    print(f"\nRule 2 (divergence from lexifier) needs the lexifier's own value, so it can "
          f"only run on the {joinable} of {len(ap_p)} APiCS parameters carrying a WALS_ID.")
    print("Rule 1 (cross-lexifier convergence) runs on all of them, but rests on the "
          f"{tot.get('non-european', 0)} non-European-lexifier lects above — that is the "
          "real sample size for any claim of a creole universal.")

    ap_l[["ID", "Name", "Glottocode", "Lexifier", "lexifier_group", "Region"]].to_csv(
        OUT_LEX, index=False)
    cov.to_csv(OUT_COV, index=False)
    print(f"\nwrote {OUT_COV}\nwrote {OUT_LEX}")


if __name__ == "__main__":
    main()
