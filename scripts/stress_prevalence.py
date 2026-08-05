"""Word-stress prevalence study: which stress rule is native to the most people?

We need ONE hard-and-fast stress rule for the interlang, stated in a sentence and
applied mechanically. This script ranks broad stress-rule categories by how many
of the world's native speakers already have them, alongside the unweighted share
of languages (the two disagree - see notes/phoneme-prevalence.md finding 3).

Jargon, for a non-linguist reader
---------------------------------
  stress          the syllable of a word that is said louder/longer/higher
                  ("PHOtograph" vs "phoTOgrapher"). "Fixed" stress means its
                  position is predictable from the shape of the word alone.
  penultimate     second-from-last syllable; antepenultimate = third from last;
                  ultimate/final = last.
  syllable weight some languages count a syllable as "heavy" if it has a long
                  vowel or ends in a consonant, and stress the heavy one. That is
                  still a rule, just a conditional one.
  tone            languages like Mandarin or Yoruba use pitch to distinguish
                  words. Most of them have no word stress in the European sense
                  at all - see the TONE POLICY section below.

Source
------
WALS (data/raw/wals), chapters:
  13A Tone                                       (tone policy input)
  14A Fixed Stress Locations                     (backbone: 502 languages)
  15A Weight-Sensitive Stress                    (splits WALS's "no fixed stress")
  16A Weight Factors in Weight-Sensitive Systems (spots lexical/diacritic "weight")
  17A Rhythm Types                               (trochaic/iambic, used by TIER B)

StressTyp2, the specialist database, was NOT used: it has no CLDF release (no
cldf-datasets/stresstyp2, clld/stresstyp2 or lexibank/stresstyp2 repository
exists) and its own distribution host st2.ullet.net is outside this environment's
network allowlist. Its ~750 languages would roughly double coverage, so this is a
logged limitation, not a closed question - see notes/stress-prevalence.md.

Two classification schemes (both are emitted; they answer different questions)
-----------------------------------------------------------------------------
TIER A, scheme="wals_rule" - "what kind of system is it?", faithful to WALS:
  14A in {Initial, Second, Third, Antepenultimate, Penultimate, Ultimate}
      -> that fixed location.
  14A = "No fixed stress":
      15A = "Not predictable"  OR  16A = "Lexical stress" -> lexically unpredictable
          (16A's "Lexical stress: lexical stress, diacritic weight" is WALS saying
          the "weight" is a per-word diacritic, i.e. memorised. This is what moves
          Russian, Turkish, Portuguese and Italian out of "weight-sensitive".)
      any other 15A value                                 -> weight-sensitive
      15A missing                                         -> unclassified

TIER B, scheme="nearest_fixed" - "which single fixed rule is closest?". This is
the actionable table: we cannot adopt "it depends on syllable weight" as our rule,
so every weight-sensitive system is collapsed onto the location a learner defaults
to, using the edge orientation in 15A and the foot type in 17A:
      Left-edge (first or second)      -> second if 17A=Iambic else initial
      Left-oriented (one of first 3)   -> initial
      Right-edge (ultimate/penult)     -> final if 17A=Iambic else penultimate
      Right-oriented (one of last 3)   -> final if 17A=Iambic else penultimate
      Unbounded / Combined / Not predictable -> no default (unpredictable)
  Trochaic is the fallback when 17A is missing or undetermined because trochaic
  outnumbers iambic 153:31 in WALS. This is deliberate over-simplification and it
  misfires on individual languages - French (right-edge, 17A undetermined) comes
  out penultimate when it is really phrase-final. Known misfires are listed in
  the write-up; none of them is large enough to change the ranking.

TONE POLICY (the most consequential judgment call - see the write-up)
---------------------------------------------------------------------
WALS has no "no word stress" value, and its chapters 14/15 do classify Mandarin
(918M L1) as "no fixed stress / not predictable / lexical stress" - i.e. as a
Russian-style memorise-it-per-word system. That is not what Mandarin is. Three
policies are emitted so the reader can see the effect:
  policy="wals_as_is"           nothing is reassigned. Mandarin stays "lexically
                                unpredictable".
  policy="tone_aware"           a language with 13A = "Complex tone system" whose
                                TIER A category came out "lexically unpredictable"
                                is reassigned to "no lexical stress". Restricted
                                to that bucket on purpose: tonal languages for
                                which WALS *does* state a stress rule (Zulu:
                                penultimate) keep it.
  policy="tone_aware_extended"  as tone_aware, plus WALS languages that have
                                13A = "Complex tone system" and NO 14A value at
                                all are added to the universe as "no lexical
                                stress" (Cantonese, Wu, Min Nan, Hakka,
                                Vietnamese, Thai, Yoruba, Burmese, ... 448M L1).
                                Rationale: WALS's stress chapters declined to
                                classify them, which for a complex-tone language
                                is evidence of absence, and dropping them silently
                                would bias the denominator.
"Simple tone system" languages are deliberately NOT reassigned or added under any
policy: that class contains Japanese, whose pitch accent IS a lexically
unpredictable word-prominence system, plus Hausa/Igbo/Somali. Leaving them out is
the conservative direction (it understates "no lexical stress").

Other judgment calls
--------------------
  - Join key: ISO 639-3 from WALS, falling back to Glottocode. WALS is
    doculect-level (11 Basque dialects, 10 Arabic varieties); rows sharing a key
    are collapsed to ONE language by modal category, ties broken by the fixed
    CATEGORY_ORDER, so a population is never counted twice.
  - Languages missing from the L1 source get L1_DEFAULT = 10,000 speakers, as in
    the phoneme prevalence study: it keeps them in the unweighted universe at a
    negligible weight cost.
  - Percentages are shares of the COVERED population, not of the world. Coverage
    is printed and reported in the write-up (WALS 14A reaches ~60% of world L1).

Inputs:
  data/raw/wals/cldf/{values,languages,codes}.csv
  data/processed/l1_speakers.csv
  data/raw/cldr_supplementalData.xml           (optional; total-weighted column)
  data/raw/iso639/{iso-639-3.tab|language-codes-full.csv}   (optional, same)

Outputs:
  data/processed/stress_prevalence.csv   ranked categories x scheme x policy
  data/processed/stress_by_language.csv  per-language classification (audit trail)

Usage: uv run python scripts/stress_prevalence.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from interlang.populations import cldr_totals, read_l1_speakers  # noqa: E402

WALS = ROOT / "data" / "raw" / "wals" / "cldf"
L1_CSV = ROOT / "data" / "processed" / "l1_speakers.csv"
CLDR_XML = ROOT / "data" / "raw" / "cldr_supplementalData.xml"
ISO_DIR = ROOT / "data" / "raw" / "iso639"
OUT_CSV = ROOT / "data" / "processed" / "stress_prevalence.csv"
OUT_LANG_CSV = ROOT / "data" / "processed" / "stress_by_language.csv"

L1_DEFAULT = 10_000

FIXED = {
    "Initial": "initial",
    "Second": "second",
    "Third": "third",
    "Antepenultimate": "antepenultimate",
    "Penultimate": "penultimate",
    "Ultimate": "final",
}
# Deterministic tie-break order when one join key has conflicting doculects, and
# the display order of the output table.
CATEGORY_ORDER = [
    "initial", "second", "third", "antepenultimate", "penultimate", "final",
    "weight-sensitive", "lexically unpredictable", "no default (unpredictable)",
    "no lexical stress", "unclassified",
]

# TIER B: 15A code name -> which edge of the word the stress window sits at.
EDGE = {
    "Left-edge: First or second": "left2",
    "Left-oriented: One of the first three": "left3",
    "Right-edge: Ultimate or penultimate": "right",
    "Right-oriented: One of the last three": "right",
    "Unbounded: Stress can be anywhere": None,
    "Combined: Right-edge and unbounded": None,
    "Not predictable": None,
}

POLICIES = ["wals_as_is", "tone_aware", "tone_aware_extended"]


# ---------------------------------------------------------------------------
# Load
# ---------------------------------------------------------------------------
def load_wals() -> pd.DataFrame:
    values = pd.read_csv(WALS / "values.csv", low_memory=False)
    langs = pd.read_csv(WALS / "languages.csv", keep_default_na=False, na_values=[""])
    code_name = pd.read_csv(WALS / "codes.csv").set_index("ID")["Name"].to_dict()

    feats = ["13A", "14A", "15A", "16A", "17A"]
    sub = values[values["Parameter_ID"].isin(feats)]
    wide = sub.pivot_table(
        index="Language_ID", columns="Parameter_ID", values="Code_ID", aggfunc="first"
    )
    for f in feats:
        wide[f] = wide[f].map(code_name) if f in wide else None

    meta = langs.set_index("ID")
    wide["wals_name"] = wide.index.map(meta["Name"])
    wide["iso639_3"] = wide.index.map(meta["ISO639P3code"])
    wide["glottocode"] = wide.index.map(meta["Glottocode"])
    wide["family"] = wide.index.map(meta["Family"])
    wide["macroarea"] = wide.index.map(meta["Macroarea"])
    return wide.reset_index().rename(columns={"Language_ID": "wals_code"})


def attach_weights(df: pd.DataFrame) -> pd.DataFrame:
    """Add join key, L1 weight and total-speaker weight to every WALS doculect."""
    l1 = read_l1_speakers(L1_CSV)
    by_iso = dict(zip(l1["iso639_3"], l1["l1_speakers"]))
    has_gc = l1[l1["glottocode"].notna()]
    by_gc = dict(zip(has_gc["glottocode"], has_gc["l1_speakers"]))

    if CLDR_XML.exists() and (
        (ISO_DIR / "iso-639-3.tab").exists() or (ISO_DIR / "language-codes-full.csv").exists()
    ):
        totals_by_iso = cldr_totals(CLDR_XML, ISO_DIR)
    else:
        print("  NOTE: CLDR/ISO tables absent - total-weighted column falls back to L1")
        totals_by_iso = {}

    keys, w_l1, w_total, joined = [], [], [], []
    for iso, gc in zip(df["iso639_3"], df["glottocode"]):
        iso = iso if isinstance(iso, str) else None
        gc = gc if isinstance(gc, str) else None
        if iso is not None and iso in by_iso:
            key, pop, hit = f"iso:{iso}", float(by_iso[iso]), True
        elif gc is not None and gc in by_gc:
            key, pop, hit = f"gc:{gc}", float(by_gc[gc]), True
        else:
            key = f"iso:{iso}" if iso else (f"gc:{gc}" if gc else "wals:unknown")
            pop, hit = float(L1_DEFAULT), False
        keys.append(key)
        w_l1.append(pop)
        joined.append(hit)
        # CLDR-missing fallback: total := L1 (project convention, principles 3.8)
        w_total.append(float(totals_by_iso.get(iso, pop)) if iso else pop)
    df = df.copy()
    df["join_key"] = keys
    df["l1_speakers"] = w_l1
    df["total_speakers"] = w_total
    df["l1_joined"] = joined
    return df


# ---------------------------------------------------------------------------
# Classification
# ---------------------------------------------------------------------------
def tier_a(row) -> str:
    f14 = row["14A"]
    if f14 in FIXED:
        return FIXED[f14]
    if f14 != "No fixed stress":
        return "unclassified"
    f15 = row["15A"]
    if not isinstance(f15, str):
        return "unclassified"
    if f15 == "Not predictable" or row["16A"] == "Lexical stress":
        return "lexically unpredictable"
    return "weight-sensitive"


def tier_b(row, cat_a: str) -> str:
    if cat_a in FIXED.values():
        return cat_a
    edge = EDGE.get(row["15A"])
    iambic = row["17A"] == "Iambic"
    if edge == "left2":
        return "second" if iambic else "initial"
    if edge == "left3":
        return "initial"
    if edge == "right":
        return "final" if iambic else "penultimate"
    return "no default (unpredictable)"


def classify(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["wals_rule"] = [tier_a(r) for _, r in df.iterrows()]
    df["nearest_fixed"] = [tier_b(r, a) for (_, r), a in zip(df.iterrows(), df["wals_rule"])]
    return df


def apply_policy(df: pd.DataFrame, policy: str, ext: pd.DataFrame) -> pd.DataFrame:
    """Universe + categories for one tone policy."""
    out = df.copy()
    if policy == "wals_as_is":
        return out
    # Reassigned in BOTH schemes on the same criterion - TIER A said "lexically
    # unpredictable" - so a tonal language for which WALS does state a rule keeps
    # it under both schemes.
    reassign = (out["13A"] == "Complex tone system") & (
        out["wals_rule"] == "lexically unpredictable"
    )
    out.loc[reassign, ["wals_rule", "nearest_fixed"]] = "no lexical stress"
    if policy == "tone_aware_extended":
        add = ext.copy()
        add["wals_rule"] = "no lexical stress"
        add["nearest_fixed"] = "no lexical stress"
        out = pd.concat([out, add], ignore_index=True)
    return out


def dedup(df: pd.DataFrame, scheme: str) -> pd.DataFrame:
    """One row per population join key: modal category, ties by CATEGORY_ORDER."""
    rank = {c: i for i, c in enumerate(CATEGORY_ORDER)}
    rows = []
    for _, grp in df.groupby("join_key", sort=False):
        counts = grp[scheme].value_counts()
        best = [c for c in counts.index if counts[c] == counts.iloc[0]]
        pick = sorted(best, key=lambda c: rank.get(c, 99))[0]
        row = grp.iloc[0].copy()
        row[scheme] = pick
        row["n_doculects"] = len(grp)
        rows.append(row)
    return pd.DataFrame(rows)


def summarise(df: pd.DataFrame, scheme: str, policy: str) -> pd.DataFrame:
    d = dedup(df, scheme)
    n, sum_l1, sum_tot = len(d), d["l1_speakers"].sum(), d["total_speakers"].sum()
    agg = d.groupby(scheme).agg(
        n_languages=("wals_code", "size"),
        l1_with=("l1_speakers", "sum"),
        total_with=("total_speakers", "sum"),
    )
    agg["scheme"] = scheme
    agg["policy"] = policy
    agg["pct_languages"] = agg["n_languages"] / n
    agg["pct_l1_weighted"] = agg["l1_with"] / sum_l1
    agg["pct_total_weighted"] = agg["total_with"] / sum_tot
    agg["n_languages_universe"] = n
    agg["l1_universe"] = sum_l1
    return agg.reset_index().rename(columns={scheme: "category"})


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    wals = attach_weights(load_wals())
    stressed = classify(wals[wals["14A"].notna()])
    # Coverage extension universe (used only by tone_aware_extended)
    ext = wals[(wals["14A"].isna()) & (wals["13A"] == "Complex tone system")].copy()

    l1 = read_l1_speakers(L1_CSV)
    world_l1 = l1["l1_speakers"].sum()
    base = dedup(stressed, "wals_rule")
    ext_ded = ext.drop_duplicates("join_key")
    print(f"WALS doculects with a 14A value: {len(stressed)} -> {len(base)} languages after dedup")
    print(f"  L1 covered: {base['l1_speakers'].sum():,.0f} "
          f"({base['l1_speakers'].sum() / world_l1:.1%} of the L1 source's world total "
          f"{world_l1:,.0f})")
    print(f"  complex-tone coverage extension: {len(ext_ded)} languages, "
          f"{ext_ded['l1_speakers'].sum():,.0f} L1 "
          f"(+{ext_ded['l1_speakers'].sum() / world_l1:.1%})")
    missing = l1[~l1["iso639_3"].isin(
        {k[4:] for k in base["join_key"] if k.startswith("iso:")}
    ) & ~l1["glottocode"].isin(
        {k[3:] for k in base["join_key"] if k.startswith("gc:")}
    )]
    print("  biggest uncovered languages: "
          + ", ".join(f"{r['name']} {r.l1_speakers / 1e6:.0f}M"
                      for _, r in missing.nlargest(12, "l1_speakers").iterrows()))

    frames = []
    for policy in POLICIES:
        universe = apply_policy(stressed, policy, ext)
        for scheme in ("wals_rule", "nearest_fixed"):
            frames.append(summarise(universe, scheme, policy))
    out = pd.concat(frames, ignore_index=True)
    rank = {c: i for i, c in enumerate(CATEGORY_ORDER)}
    out["_o"] = out["category"].map(rank)
    out = out.sort_values(["policy", "scheme", "pct_l1_weighted"], ascending=[True, True, False])
    out = out[["scheme", "policy", "category", "n_languages", "pct_languages",
               "pct_l1_weighted", "pct_total_weighted", "l1_with", "total_with",
               "n_languages_universe", "l1_universe"]]
    for c in ("pct_languages", "pct_l1_weighted", "pct_total_weighted"):
        out[c] = out[c].round(5)
    for c in ("l1_with", "total_with", "l1_universe"):
        out[c] = out[c].round(0).astype("int64")
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(OUT_CSV, index=False)
    print(f"\nWrote {OUT_CSV}: {len(out)} rows")

    # per-language audit trail, under the headline policy (tone_aware_extended)
    per_lang = dedup(apply_policy(stressed, "tone_aware_extended", ext), "wals_rule")
    nf = dedup(apply_policy(stressed, "tone_aware_extended", ext), "nearest_fixed")
    per_lang["nearest_fixed"] = per_lang["join_key"].map(
        dict(zip(nf["join_key"], nf["nearest_fixed"]))
    )
    per_lang = per_lang[
        ["wals_code", "wals_name", "iso639_3", "glottocode", "family", "macroarea",
         "13A", "14A", "15A", "16A", "17A", "wals_rule", "nearest_fixed",
         "l1_speakers", "total_speakers", "l1_joined", "n_doculects"]
    ].sort_values("l1_speakers", ascending=False)
    per_lang.to_csv(OUT_LANG_CSV, index=False)
    print(f"Wrote {OUT_LANG_CSV}: {len(per_lang)} languages")

    for policy in POLICIES:
        for scheme in ("wals_rule", "nearest_fixed"):
            t = out[(out["policy"] == policy) & (out["scheme"] == scheme)]
            print(f"\n--- {scheme} / {policy} "
                  f"({t['n_languages_universe'].iat[0]} languages, "
                  f"{t['l1_universe'].iat[0] / 1e9:.3f}B L1) ---")
            print(t[["category", "n_languages", "pct_languages", "pct_l1_weighted",
                     "pct_total_weighted"]].to_string(index=False))


if __name__ == "__main__":
    main()
