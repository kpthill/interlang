"""Tier 2 Q8: the pronoun system.

Agenda: notes/grammar-plan.md 4 Q8.  The last Tier 2 question with real content -
Q10 (questions) is small - and the one that decides the largest single block of
closed-class vocabulary the language will have.

Sub-questions:
  (a) how many persons and numbers?     - the size of the block
  (b) clusivity (we/you-and-me)?        - side-evidence in Tier 0 said no; re-cut
  (c) gender?                           - side-evidence said no; re-cut
  (d) politeness (T/V)?                 - genuinely split, the real decision here
  (e) CASE FORMS (I/me)?                - the flagged route by which ALIGNMENT
                                          comes back (principles.md 7, deferred);
                                          if pronouns carry case, alignment has to
                                          be decided after all
  (f) 3rd person = demonstrative?       - Q7 gave the demonstrative article duty;
                                          if 3sg is the same word, that is one
                                          fewer form to learn and one fewer to coin
  (g) reflexives, possessives, duals    - extra forms that would enlarge the block

Evidence policy: notes/grammar-plan.md 2 and 5 - contact evidence stratified
restricted pidgin / expanded pidgin / creole with the pidgin columns read first;
world distributions deduplicated on Glottocode and weighted by L1 and total
speakers; Rule 2 run on the Euro-coded members of the set.

Usage:   uv run python scripts/grammar_tier2_pronouns.py
Inputs:  data/raw/{wals,grambank,apics}/cldf/*.csv, data/processed/l1_speakers.csv
Outputs: data/processed/grammar_tier2_pronouns.csv
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

OUT = ROOT / "data" / "processed" / "grammar_tier2_pronouns.csv"

APICS_PRON = {
    "13": "gender distinctions in personal pronouns",
    "15": "inclusive/exclusive distinction",
    "18": "politeness distinctions in 2nd person",
    "14": "dual in independent pronouns",
    "16": "person syncretism",
    "17": "special dependent forms for subject and object",
    "59": "alignment of case marking of personal pronouns",
    "25": "nominal plural marker and 3rd-person-plural pronoun",
}
GB_PRON = {
    "GB028": "inclusive/exclusive distinction",
    "GB030": "gender in independent 3rd person pronouns",
    "GB196": "male/female distinction in 2nd person pronouns",
    "GB031": "dual for all person categories",
    "GB071": "morphological case on pronominal core arguments",
    "GB305": "phonologically independent reflexive pronoun",
    "GB313": "special adnominal possessive pronouns",
    "GB167": "logophoric pronoun",
}
WALS_PRON = {"39A": "inclusive/exclusive distinction", "44A": "gender in pronouns",
             "45A": "politeness distinctions", "43A": "3rd person pronouns and demonstratives"}


def main() -> None:
    (l1m, tot, W1, WT) = populations()
    rows = []

    ap_l, _p, ap_v = load("apics")
    ap_l["ctype"] = [contact_type(n) for n in ap_l.Name]
    ap_l["grp"] = ""
    cmap = dict(zip(*pd.read_csv(ROOT / "data/raw/apics/cldf/codes.csv")[["ID", "Name"]].values.T))

    print("=" * 78)
    print("PART 1  CONTACT LANGUAGES  (pidgin columns first)")
    print("=" * 78)
    for pid, label in APICS_PRON.items():
        print(f"\n--- APiCS {pid}: {label} ---")
        _v, ct = apics_table(pid, ap_v, ap_l, cmap)
        ct["total"] = ct.sum(axis=1)
        print(ct.sort_values("total", ascending=False).to_string())
        for opt, r in ct.iterrows():
            rows.append(dict(part="contact", feature=label, source="apics", option=opt,
                             restricted=r[TYPE_ORDER[0]], expanded=r[TYPE_ORDER[1]],
                             creole=r[TYPE_ORDER[2]]))

    print("\n" + "=" * 78)
    print("PART 2  THE WORLD")
    print("=" * 78)
    gb_l, _p2, gb_v = load("grambank")
    gb_l = gb_l[gb_l.level == "language"]
    gb_v = gb_v[gb_v.Language_ID.isin(set(gb_l.ID))]
    gb_l = weight(gb_l, l1m, tot)
    gk = gb_l.set_index("ID")
    v = gb_v[gb_v.Parameter_ID.isin(GB_PRON) & gb_v.Value.astype(str).isin(["0", "1"])].copy()
    v["gc"] = v.Language_ID.map(gk.Glottocode)
    v["l1"] = v.Language_ID.map(gk.l1).fillna(0.0)
    v["tot"] = v.Language_ID.map(gk.total).fillna(0.0)
    v = v[v.gc.notna()].drop_duplicates(["gc", "Parameter_ID"])
    print(f"\n  {'feature':50s} {'n':>5s} {'%lang':>6s} {'%L1':>6s} {'%tot':>6s}")
    for fid, label in GB_PRON.items():
        g = v[v.Parameter_ID == fid]
        if not len(g):
            continue
        yes = g[g.Value.astype(str) == "1"]
        pl, p1, pt = (100 * len(yes) / len(g), 100 * yes.l1.sum() / g.l1.sum(),
                      100 * yes.tot.sum() / g.tot.sum())
        print(f"  {label:50s} {len(g):5d} {pl:6.1f} {p1:6.1f} {pt:6.1f}")
        rows.append(dict(part="world", feature=label, source="grambank", option="yes",
                         n=len(g), by_lang=round(pl, 1), by_L1=round(p1, 1),
                         by_total=round(pt, 1)))
    for wid, label in WALS_PRON.items():
        w = wals_dist(wid, l1m, tot)
        print(f"\n  WALS {wid} {label} (n={int(w.n.sum())})")
        print("  " + w.head(5).to_string().replace("\n", "\n  "))
        for opt, r in w.iterrows():
            rows.append(dict(part="world", feature=label, source="wals", option=opt,
                             n=r.n, by_lang=r.by_lang, by_L1=r.by_L1, by_total=r.by_total))

    print("\n" + "=" * 78)
    print("PART 3  RULE 2 - the Euro-coded members: gender, politeness, case, possessives")
    print("=" * 78)
    val = {(r.Language_ID, r.Parameter_ID): str(r.Value) for r in gb_v.itertuples()
           if r.Parameter_ID in GB_PRON}
    names = dict(zip(gb_l.ID, gb_l.Name))
    recs = []
    for creole, (lex, lex_label, _n) in LEXIFIER_OF.items():
        for fid, label in GB_PRON.items():
            c, l = val.get((creole, fid), "?"), val.get((lex, fid), "?")
            if c in ("0", "1") and l in ("0", "1"):
                recs.append(dict(feature=label, creole=names.get(creole, creole),
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
