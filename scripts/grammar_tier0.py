"""Tier 0: head-directionality and morphological type.

The first grammar study.  Answers the two decisions that everything downstream
inherits (agenda: notes/grammar-plan.md 4):

  (1) HEAD-DIRECTIONALITY - is the language head-initial, and does "head
      directionality" behave as one parameter at all?
  (2) MORPHOLOGICAL TYPE  - how isolating?  Specifically Patrick's question
      (2026-08-05): when creoles differ from their lexifier, do they GAIN
      derivational affixes or LOSE them?

Evidence policy is notes/grammar-plan.md 2 and 5:
  - creoles are the north star; Rule 1 = convergence ACROSS lexifier families,
    Rule 2 = divergence FROM the lexifier;
  - every creole claim quotes the non-European-lexifier n, never the APiCS total;
  - Grambank is the default typological source, WALS the supplement, and any WALS
    morphology chapter is quoted with its (small) n.

Design of part 2, and why it is stronger than the part-1 design
--------------------------------------------------------------
Rule 2 normally needs hand-supplied lexifier values, because APiCS does not
contain lexifiers.  For morphology it does not: **14 APiCS contact languages are
also in Grambank, and so are their lexifiers**, so creole and lexifier are scored
on the SAME feature definitions by the same project.  Every pair below is
therefore a like-for-like comparison with no hand-coding on either side - the
cleanest Rule 2 test available anywhere in the project.

Per (creole, feature) the verdict is one of:
    LOST    lexifier has it, creole does not     <- the learnability signal
    KEPT    both have it
    GAINED  creole has it, lexifier does not
    ABSENT  neither has it (uninformative)
`?` on either side is dropped, not counted as 0 - Grambank's `?` means unknown.

Policies baked in here
----------------------
  - LEXIFIER_OF is a hand-built map (creole glottocode -> lexifier glottocode).
    Judgment calls, each defended in the table: Juba Arabic and Kinubi are paired
    with Standard Arabic because Grambank has no Sudanese Arabic; the Malay
    creoles with Standard Malay; Lingala with Bobangi; Berbice Dutch with Dutch
    (its Eastern Ijo substrate is not in Grambank, so only half the input is
    represented - flagged, and it is the one pair whose LOST verdicts should be
    read as "lost from Dutch", not "lost from the whole input").
  - Spanish is absent from Grambank, so Spanish-lexifier creoles cannot be
    paired.  None of the 14 has a Spanish lexifier, so nothing is lost here, but
    a larger sample would hit this.
  - Word-order distributions are deduplicated on Glottocode and weighted by L1
    and by total speakers, both reported (they disagree, and 2 says count people).
  - APiCS is multivalued; the highest-`Frequency` value per (language, feature)
    is taken, matching scripts/grammar_sources.py.

Usage:   uv run python scripts/grammar_tier0.py
Inputs:  data/raw/{wals,grambank,apics}/cldf/*.csv, data/processed/l1_speakers.csv
Outputs: data/processed/grammar_tier0_order.csv       (word order, all 3 sources)
         data/processed/grammar_tier0_morphology.csv  (creole vs lexifier, paired)
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))

from grammar_sources import (LEXIFIER_GROUP, OTHER_GROUP, load,  # noqa: E402
                             populations, weight)

OUT_ORDER = ROOT / "data" / "processed" / "grammar_tier0_order.csv"
OUT_MORPH = ROOT / "data" / "processed" / "grammar_tier0_morphology.csv"

# --- part 1: the correlated word-order set --------------------------------
# (label, APiCS parameter, WALS chapter, Grambank feature)
ORDER_SET = [
    ("subject/object/verb",   "1",  "81A", "GB132"),
    ("adposition & NP",       "4",  "85A", "GB074"),
    ("possessor & possessum", "2",  "86A", "GB065"),
    ("adjective & noun",      "3",  "87A", "GB193"),
    ("demonstrative & noun",  "5",  "88A", "GB025"),
    ("numeral & noun",        "6",  "89A", "GB024"),
    ("relative clause & noun", "7", "90A", "GB327"),
]

# --- part 2: morphology ----------------------------------------------------
# Grambank features that ARE derivational word-formation - the direct answer to
# "do creoles gain or lose derivational affixes".
DERIVATION = {
    "GB047": "action/state noun from verb (nominalisation)",
    "GB048": "agent noun from verb",
    "GB049": "object noun from verb",
    "GB187": "diminutive on the noun",
    "GB188": "augmentative on the noun",
    "GB155": "causative by affix/clitic on the verb",
    "GB113": "transitivising affix/clitic",
}
# Inflection and bound morphology generally - the "how isolating" context the
# derivation question sits in.
INFLECTION = {
    "GB044": "productive plural marking on nouns",
    "GB070": "morphological case on core arguments",
    "GB072": "morphological case on obliques",
    "GB079": "verb prefixes/proclitics (beyond argument marking)",
    "GB080": "verb suffixes/enclitics (beyond argument marking)",
    "GB082": "present-tense marking on the verb",
    "GB083": "past-tense marking on the verb",
    "GB084": "future-tense marking on the verb",
    "GB086": "perfective/imperfective on the verb",
    "GB089": "S indexed by suffix on the verb (agreement)",
    "GB092": "A indexed by prefix on the verb (agreement)",
    "GB147": "morphological passive on the lexical verb",
}
# Alternatives to affixation - if creoles lose affixes, what replaces them?
PERIPHRASIS = {
    "GB122": "verb compounding is a regular process",
    "GB158": "verbs are reduplicated",
    "GB159": "nouns are reduplicated",
}

# creole glottocode -> (lexifier glottocode, lexifier label, note)
LEXIFIER_OF = {
    "sana1297": ("stan1293", "English", ""),
    "baha1260": ("stan1293", "English", ""),
    "tokp1240": ("stan1293", "English", ""),
    "bisl1239": ("stan1293", "English", ""),
    "sara1340": ("stan1293", "English", "Portuguese-influenced maroon creole"),
    "jama1262": ("stan1293", "English", ""),
    "hait1244": ("stan1290", "French", ""),
    "berb1259": ("dutc1256", "Dutch", "Eastern Ijo substrate absent from Grambank"),
    "ling1263": ("bang1354", "Bobangi", "non-European lexifier"),
    "nubi1253": ("stan1318", "Standard Arabic",
                 "Sudanese Arabic absent from Grambank; non-European lexifier"),
    "suda1237": ("stan1318", "Standard Arabic",
                 "Sudanese Arabic absent from Grambank; non-European lexifier"),
    "sril1245": ("stan1306", "Standard Malay", "non-European lexifier"),
    "baba1267": ("stan1306", "Standard Malay", "non-European lexifier"),
    "ambo1250": ("stan1306", "Standard Malay", "non-European lexifier"),
}


def apics_dist(pid: str, ap_l, ap_v, cmap) -> pd.DataFrame:
    v = ap_v[ap_v.Parameter_ID.astype(str) == str(pid)].copy()
    v["label"] = v.Code_ID.map(cmap)
    v = v.join(ap_l.set_index("ID")[["Name", "Lexifier", "grp"]], on="Language_ID")
    return v.sort_values("Frequency", ascending=False).drop_duplicates("Language_ID")


def weighted_dist(ds: str, fid: str, l1m, tot) -> pd.DataFrame:
    langs, _params, vals = load(ds)
    if ds == "grambank":
        langs = langs[langs.level == "language"]
    langs = weight(langs, l1m, tot)
    codes = pd.read_csv(ROOT / "data" / "raw" / ds / "cldf" / "codes.csv")
    cmap = dict(zip(codes.ID, codes.Name))
    v = vals[(vals.Parameter_ID == fid) & (vals.Value.astype(str) != "?")].copy()
    k = langs.set_index("ID")
    v["gc"] = v.Language_ID.map(k.Glottocode)
    v["l1"] = v.Language_ID.map(k.l1).fillna(0.0)
    v["tot"] = v.Language_ID.map(k.total).fillna(0.0)
    v = v[v.gc.notna()].drop_duplicates("gc")
    v["label"] = v.Code_ID.map(cmap).fillna(v.Value.astype(str))
    g = v.groupby("label").agg(n=("gc", "size"), l1=("l1", "sum"), tot=("tot", "sum"))
    g["by_lang_pct"] = (100 * g.n / g.n.sum()).round(1)
    g["by_l1_pct"] = (100 * g.l1 / g.l1.sum()).round(1)
    g["by_total_pct"] = (100 * g.tot / g.tot.sum()).round(1)
    return g.sort_values("by_lang_pct", ascending=False)


def main() -> None:
    (l1m, tot, W1, WT) = populations()
    ap_l, ap_p, ap_v = load("apics")
    ap_l["grp"] = [OTHER_GROUP.get(n, "non-european") if lx == "Other"
                   else LEXIFIER_GROUP.get(lx, "?")
                   for n, lx in zip(ap_l.Name, ap_l.Lexifier)]
    ap_codes = pd.read_csv(ROOT / "data/raw/apics/cldf/codes.csv")
    ap_cmap = dict(zip(ap_codes.ID, ap_codes.Name))

    # =====================================================================
    print("=" * 72)
    print("PART 1  HEAD-DIRECTIONALITY: does it behave as one parameter?")
    print("=" * 72)
    rows = []
    for label, apid, wals_id, gb_id in ORDER_SET:
        d = apics_dist(apid, ap_l, ap_v, ap_cmap)
        ne = d[d.grp == "non-european"]
        eu = d[d.grp == "european"]
        top_ne = ne.label.value_counts()
        share = 100 * top_ne.iloc[0] / len(ne) if len(ne) else float("nan")
        print(f"\n--- {label} ---")
        print(f"  creoles, non-European lexifier (n={len(ne)}): "
              + "; ".join(f"{k} {v}" for k, v in top_ne.items()))
        print(f"  creoles, European lexifier (n={len(eu)}):     "
              + "; ".join(f"{k} {v}" for k, v in eu.label.value_counts().head(3).items()))
        w = weighted_dist("wals", wals_id, l1m, tot)
        print(f"  WALS {wals_id} (n={int(w.n.sum())}): "
              + "; ".join(f"{k} {r.by_lang_pct}%/L1 {r.by_l1_pct}%"
                          for k, r in w.head(3).iterrows()))
        verdict = ("CONVERGES" if share >= 75 else
                   "leans" if share >= 60 else "SPLIT - no creole signal")
        print(f"  -> Rule 1 verdict: {verdict} "
              f"({top_ne.index[0] if len(top_ne) else '-'}, {share:.0f}% of {len(ne)})")
        for k, r in w.iterrows():
            rows.append(dict(part="order", feature=label, source="wals", option=k,
                             n=r.n, by_lang_pct=r.by_lang_pct, by_l1_pct=r.by_l1_pct,
                             by_total_pct=r.by_total_pct))
        for grp in ("non-european", "european", "mixed"):
            for k, n in d[d.grp == grp].label.value_counts().items():
                rows.append(dict(part="order", feature=label, source=f"apics:{grp}",
                                 option=k, n=n, by_lang_pct=None,
                                 by_l1_pct=None, by_total_pct=None))
    pd.DataFrame(rows).to_csv(OUT_ORDER, index=False)

    # =====================================================================
    print("\n" + "=" * 72)
    print("PART 2  MORPHOLOGICAL TYPE: do creoles gain or lose derivation?")
    print("=" * 72)
    gb_l, _gb_p, gb_v = load("grambank")
    gb_l = gb_l[gb_l.level == "language"]
    names = dict(zip(gb_l.ID, gb_l.Name))
    val = {(r.Language_ID, r.Parameter_ID): str(r.Value)
           for r in gb_v.itertuples() if r.Parameter_ID in
           {**DERIVATION, **INFLECTION, **PERIPHRASIS}}

    ap_grp = dict(zip(ap_l.Glottocode, ap_l.grp))
    recs = []
    for creole, (lex, lex_label, note) in LEXIFIER_OF.items():
        for block, feats in (("derivation", DERIVATION), ("inflection", INFLECTION),
                             ("periphrasis", PERIPHRASIS)):
            for fid, fname in feats.items():
                c, l = val.get((creole, fid), "?"), val.get((lex, fid), "?")
                if c not in ("0", "1") or l not in ("0", "1"):
                    verdict = "unknown"
                else:
                    verdict = {("1", "1"): "KEPT", ("1", "0"): "LOST",
                               ("0", "1"): "GAINED", ("0", "0"): "ABSENT"}[(l, c)]
                recs.append(dict(block=block, feature_id=fid, feature=fname,
                                 creole=names.get(creole, creole),
                                 creole_gc=creole, lexifier=lex_label,
                                 lexifier_group=ap_grp.get(creole, "?"),
                                 creole_value=c, lexifier_value=l, verdict=verdict,
                                 note=note))
    m = pd.DataFrame(recs)
    m.to_csv(OUT_MORPH, index=False)

    print(f"\n{m.creole.nunique()} contact languages paired with their lexifier, "
          f"all values from Grambank on both sides.")
    print(f"lexifier groups: "
          f"{m.drop_duplicates('creole').lexifier_group.value_counts().to_dict()}")

    for block in ("derivation", "inflection", "periphrasis"):
        b = m[(m.block == block) & (m.verdict != "unknown")]
        print(f"\n--- {block.upper()}  ({len(b)} informative creole x feature cells) ---")
        ct = b.verdict.value_counts()
        informative = ct.get("LOST", 0) + ct.get("GAINED", 0) + ct.get("KEPT", 0)
        print("  " + "; ".join(f"{k} {v}" for k, v in ct.items()))
        if informative:
            print(f"  of the {informative} cells where either side has the feature: "
                  f"LOST {100*ct.get('LOST',0)/informative:.0f}%, "
                  f"KEPT {100*ct.get('KEPT',0)/informative:.0f}%, "
                  f"GAINED {100*ct.get('GAINED',0)/informative:.0f}%")
        piv = (b.pivot_table(index="feature", columns="verdict",
                            values="creole", aggfunc="count")
                .fillna(0).astype(int))
        for col in ("LOST", "KEPT", "GAINED", "ABSENT"):
            if col not in piv:
                piv[col] = 0
        print(piv[["LOST", "KEPT", "GAINED", "ABSENT"]].to_string())
        # RULE 1: does the pattern survive the lexifier-family split, or is it
        # a European-lexifier artifact?  This is the check that matters.
        grp = (b.pivot_table(index="lexifier_group", columns="verdict",
                             values="feature", aggfunc="count").fillna(0).astype(int))
        for col in ("LOST", "KEPT", "GAINED", "ABSENT"):
            if col not in grp:
                grp[col] = 0
        grp = grp[["LOST", "KEPT", "GAINED", "ABSENT"]]
        grp["LOST:KEPT"] = [f"{r.LOST}:{r.KEPT}" for r in grp.itertuples()]
        print("  Rule 1 check - same table split by lexifier family:")
        print("  " + grp.to_string().replace("\n", "\n  "))

    print("\n--- per creole: derivation only ---")
    d = m[(m.block == "derivation") & (m.verdict != "unknown")]
    per = d.pivot_table(index=["creole", "lexifier", "lexifier_group"],
                        columns="verdict", values="feature", aggfunc="count").fillna(0).astype(int)
    for col in ("LOST", "KEPT", "GAINED", "ABSENT"):
        if col not in per:
            per[col] = 0
    print(per[["LOST", "KEPT", "GAINED", "ABSENT"]].to_string())

    print("\n--- the same question asked of the world, for scale (WALS, small n) ---")
    for wals_id, what in (("20A", "fusion of inflectional formatives"),
                          ("22A", "inflectional synthesis of the verb"),
                          ("26A", "prefixing vs suffixing")):
        w = weighted_dist("wals", wals_id, l1m, tot)
        print(f"\n  WALS {wals_id} {what} (n={int(w.n.sum())} languages)")
        print("  " + w[["n", "by_lang_pct", "by_l1_pct", "by_total_pct"]]
              .head(4).to_string().replace("\n", "\n  "))

    print(f"\nwrote {OUT_ORDER}\nwrote {OUT_MORPH}")


if __name__ == "__main__":
    main()
