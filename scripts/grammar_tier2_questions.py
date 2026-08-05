"""Tier 2 Q10: question formation.

Agenda: notes/grammar-plan.md 4 Q10.  The last Tier 2 question, and the smallest -
three sub-questions, of which two are heavily constrained by earlier decisions:

  (a) polar questions          - how is "did you eat?" marked at all?  Two of the
                                 attested strategies are already dead: verbal
                                 morphology needs affixes (Tier 0) and tone needs
                                 a phonology we do not have (3.3).  That leaves
                                 intonation, a particle, and word order.
  (b) content questions        - does the question word front, or stay in the slot
                                 the noun would have occupied?  Fronting is a
                                 movement rule in a language where linear position
                                 is the ONLY marker of argument role (Tier 0), so
                                 this is not a free choice.
  (c) the interrogative words  - the word-bill part.  APiCS 19 asks whether a
                                 language lists its interrogatives as simple words
                                 or builds them compositionally; 3.6 makes
                                 compounding FIRM and free, so building them is
                                 available to us in a way it is not to every
                                 language in the sample.

  NOT CODED ANYWHERE - flagged rather than measured: whether a language that has a
  polar question particle ALSO uses it in content questions.  Every one of the
  twelve Grambank features below is scoped to *polar* interrogation explicitly and
  GB326 covers only the position of content interrogatives, so no source in this
  project can answer it.  The write-up settles it by design argument and says so.

Evidence policy: notes/grammar-plan.md 2 and 5 - contact evidence stratified
restricted pidgin / expanded pidgin / creole with the pidgin columns read first;
world distributions deduplicated on Glottocode and weighted by L1 and total
speakers; Rule 2 run on the Euro-coded members of the set.

Two source caveats this study turns on, both worth reading before the numbers:

  WALS 116A AND GRAMBANK GB257 LOOK CONTRADICTORY AND ARE NOT.  WALS asks which
  strategy is DOMINANT (intonation-only: 6.2% of L1); Grambank asks whether
  intonation alone CAN mark a polar question (77.4% of L1).  Both are true.
  Intonation is near-universally available and almost nowhere the primary marker.
  Any write-up quoting one without the other misleads.

  THE GRAMBANK POLAR FEATURES ARE NON-EXCLUSIVE.  GB257/260/262/263/264/285/286/
  291/297 each ask "can the language do this", so one language can score 1 on
  several and the columns do not sum to 100.  Only WALS 116A gives a partition.

Usage:   uv run python scripts/grammar_tier2_questions.py
Inputs:  data/raw/{wals,grambank,apics}/cldf/*.csv, data/processed/l1_speakers.csv
Outputs: data/processed/grammar_tier2_questions.csv
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

OUT = ROOT / "data" / "processed" / "grammar_tier2_questions.csv"

APICS_Q = {
    "103": "polar questions",
    "12": "position of interrogative phrases in content questions",
    "19": "interrogative pronouns (simple words vs compounds)",
}
GB_Q = {
    "GB257": "polar Q markable by intonation ONLY",
    "GB260": "polar Q markable by special word order (inversion)",
    "GB262": "clause-INITIAL polar Q particle",
    "GB263": "clause-FINAL polar Q particle",
    "GB264": "polar Q particle neither initial nor final",
    "GB285": "polar Q by particle AND verbal morphology",
    "GB286": "polar Q by verbal morphology only",
    "GB291": "polar Q markable by tone",
    "GB297": "polar Q by V-not-V construction",
    "GB324": "interrogative VERB for content questions",
    "GB325": "count/mass distinction in interrogative quantifiers",
    "GB326": "content interrogatives normally occur IN SITU",
}
WALS_Q = {"116A": "polar questions (dominant strategy)",
          "92A": "position of polar question particles",
          "93A": "position of interrogative phrases in content questions"}

# The strategies earlier decisions have already removed from our option set, and
# what removed them.  Printed with the numbers so the write-up cannot quietly
# present a three-way choice as a seven-way one.
FORECLOSED = {
    "Interrogative verb morphology": "Tier 0: no inflectional affixes (3.2)",
    "polar Q by verbal morphology only": "Tier 0: no inflectional affixes (3.2)",
    "polar Q markable by tone": "3.3: the phoneme inventory is not tonal",
}


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
    for pid, label in APICS_Q.items():
        print(f"\n--- APiCS {pid}: {label} ---")
        _v, ct = apics_table(pid, ap_v, ap_l, cmap)
        ct["total"] = ct.sum(axis=1)
        print(ct.sort_values("total", ascending=False).to_string())
        for opt, r in ct.iterrows():
            rows.append(dict(part="contact", feature=label, source="apics", option=opt,
                             restricted=r[TYPE_ORDER[0]], expanded=r[TYPE_ORDER[1]],
                             creole=r[TYPE_ORDER[2]],
                             foreclosed_by=FORECLOSED.get(opt, "")))

    print("\n" + "=" * 78)
    print("PART 2  THE WORLD")
    print("=" * 78)
    print("  NB Grambank polar features are NON-EXCLUSIVE ('can the language do X?'),")
    print("     so they do not sum to 100.  Only WALS 116A partitions.")
    gb_l, _p2, gb_v = load("grambank")
    gb_l = gb_l[gb_l.level == "language"]
    gb_v = gb_v[gb_v.Language_ID.isin(set(gb_l.ID))]
    gb_l = weight(gb_l, l1m, tot)
    gk = gb_l.set_index("ID")
    v = gb_v[gb_v.Parameter_ID.isin(GB_Q) & gb_v.Value.astype(str).isin(["0", "1"])].copy()
    v["gc"] = v.Language_ID.map(gk.Glottocode)
    v["l1"] = v.Language_ID.map(gk.l1).fillna(0.0)
    v["tot"] = v.Language_ID.map(gk.total).fillna(0.0)
    v = v[v.gc.notna()].drop_duplicates(["gc", "Parameter_ID"])
    print(f"\n  {'feature':48s} {'n':>5s} {'%lang':>6s} {'%L1':>6s} {'%tot':>6s}")
    for fid, label in GB_Q.items():
        g = v[v.Parameter_ID == fid]
        if not len(g):
            continue
        yes = g[g.Value.astype(str) == "1"]
        pl, p1, pt = (100 * len(yes) / len(g), 100 * yes.l1.sum() / g.l1.sum(),
                      100 * yes.tot.sum() / g.tot.sum())
        flag = "  [foreclosed]" if label in FORECLOSED else ""
        print(f"  {label:48s} {len(g):5d} {pl:6.1f} {p1:6.1f} {pt:6.1f}{flag}")
        rows.append(dict(part="world", feature=label, source="grambank", option="yes",
                         n=len(g), by_lang=round(pl, 1), by_L1=round(p1, 1),
                         by_total=round(pt, 1), foreclosed_by=FORECLOSED.get(label, "")))
    for wid, label in WALS_Q.items():
        w = wals_dist(wid, l1m, tot)
        print(f"\n  WALS {wid} {label} (n={int(w.n.sum())})")
        print("  " + w.to_string().replace("\n", "\n  "))
        for opt, r in w.iterrows():
            rows.append(dict(part="world", feature=label, source="wals", option=opt,
                             n=r.n, by_lang=r.by_lang, by_L1=r.by_L1, by_total=r.by_total,
                             foreclosed_by=FORECLOSED.get(opt, "")))

    print("\n" + "=" * 78)
    print("PART 3  WHO USES INVERSION  (WALS 116A 'interrogative word order', by L1)")
    print("=" * 78)
    print("  The inversion strategy is 20.1% of world L1 on 1.4% of languages, so the")
    print("  question is whether that mass is one areal group or a real spread.")
    w_l, _wp, w_v = load("wals")
    w_l = weight(w_l, l1m, tot)
    wk = w_l.set_index("ID")
    wcodes = pd.read_csv(ROOT / "data/raw/wals/cldf/codes.csv")
    wcm = dict(zip(wcodes.ID, wcodes.Name))
    q = w_v[w_v.Parameter_ID == "116A"].copy()
    q["label"] = q.Code_ID.map(wcm)
    q["l1"] = q.Language_ID.map(wk.l1).fillna(0.0)
    q["nm"] = q.Language_ID.map(wk.Name)
    inv = q[q.label == "Interrogative word order"].nlargest(10, "l1")
    print(inv[["nm", "l1"]].to_string(index=False))
    for _i, r in inv.iterrows():
        rows.append(dict(part="inversion_who", feature="interrogative word order",
                         source="wals", option=r.nm, n=r.l1))

    print("\n" + "=" * 78)
    print("PART 4  RULE 2 - creole vs its own lexifier")
    print("=" * 78)
    print("  The Euro-coded item here is INVERSION (GB260): every lexifier in the set")
    print("  has it.  Rule 2 asks whether the creoles kept it.")
    val = {(r.Language_ID, r.Parameter_ID): str(r.Value) for r in gb_v.itertuples()
           if r.Parameter_ID in GB_Q}
    names = dict(zip(gb_l.ID, gb_l.Name))
    recs = []
    for creole, (lex, lex_label, _n) in LEXIFIER_OF.items():
        for fid, label in GB_Q.items():
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
