"""Tier 2 Q9: negation.

Agenda: notes/grammar-plan.md 4 Q9.  Six sub-questions, of which two are already
constrained by earlier decisions and four are open:

  (a) affix or word?           - settled: Tier 0 rules out affixes.  Checked
                                 against the world anyway, because if negation
                                 were overwhelmingly affixal we would be paying
                                 an unusual cost and should know it.
  (b) position?                - PARTLY PRE-ANSWERED.  Q11's modifier rule says
                                 modifiers precede their head, and a negator is a
                                 modifier of the verb, so preverbal is predicted.
                                 This study is a check on that prediction, not an
                                 open choice - and a prediction that fails would
                                 be evidence against the modifier rule itself.
  (c) one negator or several?  - GB140 asks exactly the learnability question:
                                 is verbal predication negated the same way as
                                 locational, existential and nominal?  One rule
                                 or four.
  (d) prohibitive             - is "don't!" negated like a statement?
  (e) bipartite negation      - the ne...pas trap, a European speciality.
  (f) negative indefinites    - does "nobody came" also need the verb negated?

  (g) scope over TAM adverbs  - THE DEBT FROM Q6.  Making TAM lexical created a
      scope ambiguity that a fixed particle slot would have prevented: "I not run
      in-the-past" can be not(run in past) or (not run) in past.  No source codes
      this directly - APiCS 50 is the closest, and it asks whether TAM MARKING
      changes under negation, not how the two scope.  So (g) is answered by
      design argument in the write-up, informed by (b) and by APiCS 50.

Evidence policy: notes/grammar-plan.md 2 and 5 - contact evidence stratified
restricted pidgin / expanded pidgin / creole, pidgin columns read first; world
distributions deduplicated on Glottocode and weighted by L1 and total speakers.

Usage:   uv run python scripts/grammar_tier2_negation.py
Inputs:  data/raw/{wals,grambank,apics}/cldf/*.csv, data/processed/l1_speakers.csv
Outputs: data/processed/grammar_tier2_negation.csv
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))

from grammar_sources import load, populations, weight  # noqa: E402
from grammar_tier0 import LEXIFIER_OF  # noqa: E402
from grammar_tier2_np import apics_table, wals_dist  # noqa: E402
from grammar_tier2_tam import TYPE_ORDER, contact_type  # noqa: E402

OUT = ROOT / "data" / "processed" / "grammar_tier2_negation.csv"

APICS_NEG = {
    "101": "position of standard negation",
    "100": "negative morpheme type",
    "56":  "the prohibitive",
    "102": "negation and indefinite pronouns",
    "50":  "TAM marking in negated clauses",
}
GB_NEG = {
    "GB299": "standard negation by a non-inflecting word (particle)",
    "GB298": "standard negation by an inflecting word (auxiliary)",
    "GB107": "standard negation by an affix/clitic on the verb",
    "GB138": "standard negation can be clause-initial",
    "GB137": "standard negation can be clause-final",
    "GB140": "SAME negator for verbal, locational, existential and nominal predication",
    "GB139": "prohibitive differs from declarative negation",
}
WALS_NEG = {"112A": "negative morphemes", "143A": "order of negative morpheme and verb",
            "71A": "the prohibitive", "115A": "negative indefinites and predicate negation"}


def main() -> None:
    (l1m, tot, W1, WT) = populations()
    rows = []

    ap_l, _p, ap_v = load("apics")
    ap_l["ctype"] = [contact_type(n) for n in ap_l.Name]
    ap_l["grp"] = ""
    cmap = dict(zip(*pd.read_csv(ROOT / "data/raw/apics/cldf/codes.csv")[["ID", "Name"]].values.T))

    print("=" * 76)
    print("PART 1  WHAT CONTACT LANGUAGES DO  (pidgin columns first)")
    print("=" * 76)
    for pid, label in APICS_NEG.items():
        print(f"\n--- APiCS {pid}: {label} ---")
        _v, ct = apics_table(pid, ap_v, ap_l, cmap)
        ct["total"] = ct.sum(axis=1)
        print(ct.sort_values("total", ascending=False).to_string())
        for opt, r in ct.iterrows():
            rows.append(dict(part="contact", feature=label, source="apics", option=opt,
                             restricted=r[TYPE_ORDER[0]], expanded=r[TYPE_ORDER[1]],
                             creole=r[TYPE_ORDER[2]]))

    print("\n" + "=" * 76)
    print("PART 2  THE WORLD")
    print("=" * 76)
    gb_l, _p2, gb_v = load("grambank")
    gb_l = gb_l[gb_l.level == "language"]
    gb_v = gb_v[gb_v.Language_ID.isin(set(gb_l.ID))]
    gb_l = weight(gb_l, l1m, tot)
    gk = gb_l.set_index("ID")
    v = gb_v[gb_v.Parameter_ID.isin(GB_NEG) & gb_v.Value.astype(str).isin(["0", "1"])].copy()
    v["gc"] = v.Language_ID.map(gk.Glottocode)
    v["l1"] = v.Language_ID.map(gk.l1).fillna(0.0)
    v["tot"] = v.Language_ID.map(gk.total).fillna(0.0)
    v = v[v.gc.notna()].drop_duplicates(["gc", "Parameter_ID"])
    print(f"\n  {'feature':58s} {'n':>5s} {'%lang':>6s} {'%L1':>6s} {'%tot':>6s}")
    for fid, label in GB_NEG.items():
        g = v[v.Parameter_ID == fid]
        if not len(g):
            continue
        yes = g[g.Value.astype(str) == "1"]
        pl, p1, pt = (100 * len(yes) / len(g), 100 * yes.l1.sum() / g.l1.sum(),
                      100 * yes.tot.sum() / g.tot.sum())
        print(f"  {label:58s} {len(g):5d} {pl:6.1f} {p1:6.1f} {pt:6.1f}")
        rows.append(dict(part="world", feature=label, source="grambank", option="yes",
                         n=len(g), by_lang=round(pl, 1), by_L1=round(p1, 1),
                         by_total=round(pt, 1)))

    for wid, label in WALS_NEG.items():
        w = wals_dist(wid, l1m, tot)
        print(f"\n  WALS {wid} {label} (n={int(w.n.sum())})")
        print("  " + w.head(5).to_string().replace("\n", "\n  "))
        for opt, r in w.iterrows():
            rows.append(dict(part="world", feature=label, source="wals", option=opt,
                             n=r.n, by_lang=r.by_lang, by_L1=r.by_L1, by_total=r.by_total))

    print("\n" + "=" * 76)
    print("PART 3  RULE 2: negation, creole vs its own lexifier")
    print("=" * 76)
    val = {(r.Language_ID, r.Parameter_ID): str(r.Value) for r in gb_v.itertuples()
           if r.Parameter_ID in GB_NEG}
    names = dict(zip(gb_l.ID, gb_l.Name))
    recs = []
    for creole, (lex, lex_label, _n) in LEXIFIER_OF.items():
        for fid, label in GB_NEG.items():
            c, l = val.get((creole, fid), "?"), val.get((lex, fid), "?")
            if c in ("0", "1") and l in ("0", "1"):
                recs.append(dict(feature=label, creole=names.get(creole, creole),
                                 lexifier=lex_label,
                                 verdict={("1", "1"): "KEPT", ("1", "0"): "LOST",
                                          ("0", "1"): "GAINED",
                                          ("0", "0"): "ABSENT"}[(l, c)]))
    r2 = pd.DataFrame(recs)
    print(pd.crosstab(r2.feature, r2.verdict).to_string())
    for _i, r in r2.iterrows():
        rows.append(dict(part="rule2", feature=r.feature, source="grambank",
                         option=r.verdict, creole=r.creole))

    pd.DataFrame(rows).to_csv(OUT, index=False)
    print(f"\nwrote {OUT}")


if __name__ == "__main__":
    main()
