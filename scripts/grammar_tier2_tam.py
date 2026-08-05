"""Tier 2 Q6: tense, aspect and mood.

Agenda: notes/grammar-plan.md 4, question 6 - the first and largest Tier 2
decision, and the one most likely to hide a European default.  Four questions:

  (a) Is TENSE marked at all, or is the system aspectual?
  (b) Is TAM carried by MORPHOLOGY or by PARTICLES - and where a language lacks
      tense morphology, does it have a tense particle instead?  ("no tense" and
      "tense somewhere else" are different answers and the binary features do
      not distinguish them on their own.)
  (c) WHERE do the markers go, and in what order when there are several?
  (d) Does negation disturb TAM marking?  (One rule or two is a pure
      learnability question, and negation is Tier 2 Q9's dependency on this one.)

Evidence policy: notes/grammar-plan.md 2 and 5.  Creoles are the north star
(Rule 1 = convergence across lexifier families, Rule 2 = divergence from the
lexifier); Grambank supplies the world picture; every creole claim quotes the
non-European-lexifier n rather than the APiCS total.

The morphology-vs-particle pairing is what makes this study work
---------------------------------------------------------------
Grambank codes the same three categories twice over, once as bound morphology
and once as a free particle:

    tense    GB082/083/084 (present/past/future morphology)   vs GB521 (particle)
    aspect   GB086 (perfective/imperfective morphology)       vs GB520 (particle)
    mood     GB312 (mood morphology)                          vs GB519 (particle)

so "does the world mark tense?" and "does the world mark tense the way WE would
have to - with a free word?" are separable questions.  3.6 and the Tier 0
morphology finding rule out bound marking for us, so the particle columns are
the ones that bear on the decision and the morphology columns are context.

Policies baked in here
----------------------
  - Same doculect/dialect deduplication, `?`-is-not-coverage and population
    weighting as scripts/grammar_sources.py; the Grambank Glottocode->ISO bridge
    is inherited from there.
  - APiCS is multivalued: highest-`Frequency` value per (language, feature).
  - The creole/lexifier pairs are LEXIFIER_OF from scripts/grammar_tier0.py -
    the same 14 languages scored on identical Grambank features on both sides.
  - Feature GB309 (multiple pasts/futures graded by remoteness) is reported as
    context only: it prices an option we are not seriously considering, and is
    here so that "we did not consider graded tense" is a recorded decision
    rather than an oversight.

Usage:   uv run python scripts/grammar_tier2_tam.py
Inputs:  data/raw/{grambank,apics}/cldf/*.csv, data/processed/l1_speakers.csv
Outputs: data/processed/grammar_tier2_tam.csv  (one row per source x feature x option)
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
from grammar_tier0 import LEXIFIER_OF  # noqa: E402

OUT = ROOT / "data" / "processed" / "grammar_tier2_tam.csv"

# A bias control that turned up while reading the results and applies to EVERY
# Rule 1 claim, not just this study: the non-European-lexifier subsample is
# disproportionately PIDGINS rather than creoles.  A pidgin has less grammar by
# definition, so any feature counted as "creoles converge on not having X" is
# partly counting "pidgins do not have much of anything".  Rough classification -
# name contains "Pidgin", plus three known pidgins whose names do not say so.
PIDGINISH_EXTRA = {"Fanakalo", "Chinuk Wawa", "Singapore Bazaar Malay"}


def is_pidginish(name: str) -> bool:
    return "pidgin" in name.lower() or name in PIDGINISH_EXTRA


APICS_TAM = {
    "43": "position of TAM markers relative to the verb",
    "44": "internal order of T, A and M markers",
    "49": "tense-aspect system type",
    "50": "TAM marking in negated clauses",
    "47": "what the progressive marker also covers",
    "48": "what the habitual marker also covers",
}

# (feature, label, "morphology" | "particle")
GB_TAM = [
    ("GB082", "present tense", "morphology"),
    ("GB083", "past tense", "morphology"),
    ("GB084", "future tense", "morphology"),
    ("GB086", "perfective/imperfective", "morphology"),
    ("GB312", "mood", "morphology"),
    ("GB521", "tense", "particle"),
    ("GB520", "aspect", "particle"),
    ("GB519", "mood", "particle"),
    ("GB309", "multiple pasts/futures (remoteness)", "context"),
    ("GB110", "verb suppletion for tense/aspect", "context"),
]


def gb_binary(vals, langs, feats):
    """Per-feature share of languages coding 1, unweighted / L1 / total-speaker."""
    k = langs.set_index("ID")
    v = vals[vals.Parameter_ID.isin(feats) & vals.Value.astype(str).isin(["0", "1"])].copy()
    v["gc"] = v.Language_ID.map(k.Glottocode)
    v["l1"] = v.Language_ID.map(k.l1).fillna(0.0)
    v["tot"] = v.Language_ID.map(k.total).fillna(0.0)
    v = v[v.gc.notna()].drop_duplicates(["gc", "Parameter_ID"])
    out = []
    for fid, g in v.groupby("Parameter_ID"):
        yes = g[g.Value.astype(str) == "1"]
        out.append(dict(feature_id=fid, n=len(g),
                        pct_lang=round(100 * len(yes) / len(g), 1),
                        pct_l1=round(100 * yes.l1.sum() / g.l1.sum(), 1) if g.l1.sum() else None,
                        pct_total=round(100 * yes.tot.sum() / g.tot.sum(), 1) if g.tot.sum() else None))
    return pd.DataFrame(out).set_index("feature_id")


def main() -> None:
    (l1m, tot, W1, WT) = populations()
    rows = []

    # ------------------------------------------------------------------
    ap_l, ap_p, ap_v = load("apics")
    ap_l["grp"] = [OTHER_GROUP.get(n, "non-european") if lx == "Other"
                   else LEXIFIER_GROUP.get(lx, "?")
                   for n, lx in zip(ap_l.Name, ap_l.Lexifier)]
    ap_codes = pd.read_csv(ROOT / "data/raw/apics/cldf/codes.csv")
    cmap = dict(zip(ap_codes.ID, ap_codes.Name))
    ap_l["pidginish"] = [is_pidginish(n) for n in ap_l.Name]
    info = ap_l.set_index("ID")[["Name", "Lexifier", "grp", "pidginish"]]

    skew = pd.crosstab(ap_l.grp, ap_l.pidginish)
    print("=" * 74)
    print("PART 0  A BIAS CONTROL ON RULE 1 ITSELF")
    print("=" * 74)
    print("\nHow many of each lexifier group are pidgins rather than creoles?")
    print(skew.rename(columns={False: "creole", True: "pidgin-ish"}).to_string())
    ne = ap_l[ap_l.grp == "non-european"]
    print(f"\n  {ne.pidginish.sum()} of {len(ne)} non-European-lexifier lects "
          f"({100*ne.pidginish.mean():.0f}%) are pidgins, against "
          f"{100*ap_l[ap_l.grp=='european'].pidginish.mean():.0f}% of the European group.")
    print("  A pidgin has less grammar BY DEFINITION, so any Rule 1 finding of the")
    print("  form 'creoles converge on NOT having X' is partly counting that skew.")
    print("  Applies to every Rule 1 claim in the project, not just this study.")

    print("\n" + "=" * 74)
    print("PART 1  WHAT CREOLES DO  (Rule 1: the non-European-lexifier column is")
    print("        the evidence; the European column is the inheritance control)")
    print("=" * 74)
    for pid, label in APICS_TAM.items():
        v = ap_v[ap_v.Parameter_ID.astype(str) == pid].copy()
        v["label"] = v.Code_ID.map(cmap)
        v = v.join(info, on="Language_ID")
        v = v.sort_values("Frequency", ascending=False).drop_duplicates("Language_ID")
        ct = pd.crosstab(v.label, v.grp)
        for c in ("non-european", "european", "mixed"):
            if c not in ct:
                ct[c] = 0
        ct = ct[["non-european", "european", "mixed"]]
        ct["total"] = ct.sum(axis=1)
        ct = ct.sort_values("total", ascending=False)
        ne = int(ct["non-european"].sum())
        top_share = 100 * ct["non-european"].iloc[0] / ne if ne else float("nan")
        print(f"\n--- APiCS {pid}: {label} ---")
        print(ct.to_string())
        print(f"  Rule 1: top option is {ct.index[0]!r} at "
              f"{ct['non-european'].iloc[0]}/{ne} non-European-lexifier "
              f"({top_share:.0f}%)")
        # robustness: drop the pidgins, which are over-represented in that group
        cre = v[(v.grp == "non-european") & (~v.pidginish)]
        if len(cre):
            vc = cre.label.value_counts()
            print(f"  ...excluding pidgins (n={len(cre)}): "
                  + "; ".join(f"{k} {n}" for k, n in vc.items()))
        for opt, r in ct.iterrows():
            rows.append(dict(part="creole", source="apics", feature_id=pid,
                             feature=label, option=opt,
                             n_non_european=r["non-european"],
                             n_european=r["european"], n_total=r["total"]))

    # ------------------------------------------------------------------
    gb_l, _p, gb_v = load("grambank")
    gb_l = gb_l[gb_l.level == "language"]
    gb_v = gb_v[gb_v.Language_ID.isin(set(gb_l.ID))]
    gb_l = weight(gb_l, l1m, tot)
    feats = [f for f, _, _ in GB_TAM]
    tab = gb_binary(gb_v, gb_l, feats)

    print("\n" + "=" * 74)
    print("PART 2  WHAT THE WORLD DOES: morphology vs particle, weighted")
    print("=" * 74)
    print(f"\n{'':52s} {'n':>5s} {'%lang':>6s} {'%L1':>6s} {'%tot':>6s}")
    for fid, label, kind in GB_TAM:
        if fid not in tab.index:
            continue
        r = tab.loc[fid]
        print(f"  {kind:11s} {label:38s} {int(r.n):5d} {r.pct_lang:6.1f} "
              f"{r.pct_l1:6.1f} {r.pct_total:6.1f}")
        rows.append(dict(part="world", source="grambank", feature_id=fid,
                         feature=f"{kind}: {label}", option="yes", n_total=int(r.n),
                         pct_lang=r.pct_lang, pct_l1=r.pct_l1, pct_total=r.pct_total))

    # the question the binaries cannot answer on their own -------------
    print("\n--- Does 'no tense morphology' mean 'no tense', or 'tense by particle'? ---")
    k = gb_l.set_index("ID")
    w = gb_v[gb_v.Parameter_ID.isin(["GB083", "GB521", "GB086", "GB520"])].copy()
    w["gc"] = w.Language_ID.map(k.Glottocode)
    w["l1"] = w.Language_ID.map(k.l1).fillna(0.0)
    w = w[w.gc.notna() & w.Value.astype(str).isin(["0", "1"])]
    p = w.pivot_table(index="gc", columns="Parameter_ID", values="Value",
                      aggfunc="first")
    l1_of = w.drop_duplicates("gc").set_index("gc")["l1"]
    for morph, part, what in (("GB083", "GB521", "past tense"),
                              ("GB086", "GB520", "perfective/imperfective")):
        q = p[[morph, part]].dropna()
        ct = pd.crosstab(q[morph], q[part])
        ct.index = [f"{what} morphology = {i}" for i in ct.index]
        ct.columns = [f"particle = {c}" for c in ct.columns]
        print(f"\n  {what} (n={len(q)} languages)")
        print("  " + ct.to_string().replace("\n", "\n  "))
        neither = q[(q[morph] == "0") & (q[part] == "0")]
        l1share = 100 * l1_of.reindex(neither.index).fillna(0).sum() / \
            l1_of.reindex(q.index).fillna(0).sum()
        print(f"  neither morphology nor particle: {len(neither)}/{len(q)} languages "
              f"= {l1share:.1f}% of the L1 mass in this subset")
        rows.append(dict(part="world", source="grambank", feature_id=f"{morph}x{part}",
                         feature=f"{what}: neither morphology nor particle",
                         option="neither", n_total=len(neither), pct_lang=round(100*len(neither)/len(q), 1),
                         pct_l1=round(l1share, 1)))

    # ------------------------------------------------------------------
    print("\n" + "=" * 74)
    print("PART 3  RULE 2: creole vs its own lexifier, identical features")
    print("=" * 74)
    val = {(r.Language_ID, r.Parameter_ID): str(r.Value) for r in gb_v.itertuples()
           if r.Parameter_ID in set(feats)}
    names = dict(zip(gb_l.ID, gb_l.Name))
    ap_grp = dict(zip(ap_l.Glottocode, ap_l.grp))
    recs = []
    for creole, (lex, lex_label, _note) in LEXIFIER_OF.items():
        for fid, label, kind in GB_TAM:
            if kind == "context":
                continue
            c, l = val.get((creole, fid), "?"), val.get((lex, fid), "?")
            if c not in ("0", "1") or l not in ("0", "1"):
                continue
            recs.append(dict(kind=kind, feature=f"{kind}: {label}",
                             creole=names.get(creole, creole), lexifier=lex_label,
                             lexifier_group=ap_grp.get(creole, "?"),
                             verdict={("1", "1"): "KEPT", ("1", "0"): "LOST",
                                      ("0", "1"): "GAINED",
                                      ("0", "0"): "ABSENT"}[(l, c)]))
    r2 = pd.DataFrame(recs)
    for kind in ("morphology", "particle"):
        b = r2[r2.kind == kind]
        ct = b.verdict.value_counts()
        print(f"\n  TAM by {kind}: " + "; ".join(f"{k} {v}" for k, v in ct.items()))
        grp = pd.crosstab(b.lexifier_group, b.verdict)
        print("  " + grp.to_string().replace("\n", "\n  "))
        for opt, n in ct.items():
            rows.append(dict(part="rule2", source="grambank",
                             feature=f"TAM by {kind}", option=opt, n_total=int(n)))
    print("\n  per-feature detail, particles only:")
    print("  " + pd.crosstab(r2[r2.kind == "particle"].feature,
                             r2[r2.kind == "particle"].verdict)
          .to_string().replace("\n", "\n  "))

    pd.DataFrame(rows).to_csv(OUT, index=False)
    print(f"\nwrote {OUT}")


if __name__ == "__main__":
    main()
