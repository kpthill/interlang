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

# CONTACT-LANGUAGE TYPE.  Revised 2026-08-05 after Patrick pointed out that the
# first cut had this exactly backwards.  We are designing an AUXILIARY language:
# nobody's first language, built by adults who share no language.  That is what a
# PIDGIN is.  A creole is what happens once children nativise a pidgin - a
# different process with a different learner.  So pidgins are not a contaminant in
# the creole sample, they are the closest analogue to the use case, and where
# pidgins and creoles disagree the PIDGIN evidence should win.
#
# Three-way, hand-assembled from standard creolistics (`model-recall` provenance
# per international-vocab.md 3.3 - it is not in the APiCS data):
#
#   restricted pidgin  no native speakers, limited domains.  Closest to our case.
#   expanded pidgin    a community's main language, often nativising.  Adult-built
#                      in origin, so still strong evidence, but drifting toward
#                      creole - reported separately rather than merged either way.
#   creole             nativised.  Still evidence, but one generation removed from
#                      the process we care about.
#
# Boundary calls, all debatable and all logged: Chinuk Wawa is a restricted pidgin
# but its Grand Ronde variety creolised, so the two lects are typed differently;
# Tok Pisin, Bislama and Nigerian Pidgin are expanded pidgins with growing L1
# populations; Kinubi is the nativised descendant of Juba Arabic and is typed
# creole while Juba Arabic itself is typed expanded.  Mixed languages (Michif,
# Media Lengua, Ma'a/Mbugu, Gurindji Kriol) arise in BILINGUAL communities, not
# from a no-shared-language situation, and are excluded from this cut entirely.
RESTRICTED_PIDGINS = {
    "Chinese Pidgin English", "Chinese Pidgin English (European)",
    "Chinese Pidgin Russian", "Chinese Pidgin Russian (depidginized)",
    "Chinuk Wawa", "Eskimo Pidgin", "Fanakalo", "Pidgin Hawaiian",
    "Pidgin Hindustani", "Singapore Bazaar Malay", "Yimas-Arafundi Pidgin",
}
EXPANDED_PIDGINS = {
    "Bislama", "Cameroon Pidgin English", "Ghanaian Pidgin English",
    "Ghanaian Pidgin English (Acrolectal Ghanaian Pidgin English)",
    "Ghanaian Pidgin English (Student Pidgin)", "Juba Arabic",
    "Juba Arabic (Arabic interference)", "Juba Arabic (basilectal)",
    "Kikongo-Kituba", "Lingala", "Nigerian Pidgin", "Sango", "Sango (written)",
    "Tok Pisin",
}
MIXED_LANGUAGES = {"Michif", "Media Lengua",
                   "Media Lengua (Imbabura Media Lengua (data Gómez Rendón))",
                   "Mixed Ma\u2019a/Mbugu", "Gurindji Kriol"}


def contact_type(name: str) -> str:
    if name in RESTRICTED_PIDGINS:
        return "1 restricted pidgin"
    if name in EXPANDED_PIDGINS:
        return "2 expanded pidgin"
    if name in MIXED_LANGUAGES:
        return "0 mixed (excluded)"
    return "3 creole"


TYPE_ORDER = ["1 restricted pidgin", "2 expanded pidgin", "3 creole"]

# Per-category prevalence: the individual tenses/aspects/moods that were
# considered for the particle inventory, and where each one's prevalence comes
# from.  APiCS codes presence indirectly, via a "no overt X marker" option on the
# feature that otherwise describes X.
APICS_CATEGORY = {
    "past":        ("45", "No overt past marker exists"),
    "progressive": ("46", "No overt progressive marker"),
    "habitual":    ("48", "No overt habitual marker"),
}
WALS_CATEGORY = {
    "65A": "perfective/imperfective",
    "66A": "past tense",
    "67A": "future tense",
    "68A": "the perfect",
}


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


def weighted_dist_local(fid, l1m, tot):
    """WALS distribution for one chapter, deduplicated and population-weighted."""
    langs, _p, vals = load("wals")
    langs = weight(langs, l1m, tot)
    codes = pd.read_csv(ROOT / "data/raw/wals/cldf/codes.csv")
    cm = dict(zip(codes.ID, codes.Name))
    v = vals[(vals.Parameter_ID == fid) & (vals.Value.astype(str) != "?")].copy()
    k = langs.set_index("ID")
    v["gc"] = v.Language_ID.map(k.Glottocode)
    v["l1"] = v.Language_ID.map(k.l1).fillna(0.0)
    v["tot"] = v.Language_ID.map(k.total).fillna(0.0)
    v = v[v.gc.notna()].drop_duplicates("gc")
    v["label"] = v.Code_ID.map(cm).fillna(v.Value.astype(str))
    g = v.groupby("label").agg(n=("gc", "size"), l1=("l1", "sum"), t=("tot", "sum"))
    g["by_lang_pct"] = (100 * g.n / g.n.sum()).round(1)
    g["by_l1_pct"] = (100 * g.l1 / g.l1.sum()).round(1)
    g["by_total_pct"] = (100 * g.t / g.t.sum()).round(1)
    return g.sort_values("by_lang_pct", ascending=False)


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
    ap_l["ctype"] = [contact_type(n) for n in ap_l.Name]
    info = ap_l.set_index("ID")[["Name", "Lexifier", "grp", "ctype"]]

    print("=" * 74)
    print("PART 0  THE SAMPLE, STRATIFIED BY CONTACT TYPE")
    print("=" * 74)
    print("\nPidgins are the closest analogue to an auxiliary language: adults, no")
    print("shared language, no native speakers.  Creoles are one generation further")
    print("on.  Where the two disagree, the pidgin evidence should win.\n")
    print(pd.crosstab(ap_l.ctype, ap_l.grp).to_string())

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
        # the cut that matters: what do the PIDGINS do, of any lexifier?
        for t in TYPE_ORDER:
            sub = v[v.ctype == t]
            if len(sub):
                vc = sub.label.value_counts()
                print(f"    {t:20s} (n={len(sub):2d}): "
                      + "; ".join(f"{k} {n}" for k, n in vc.head(4).items()))
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

    # ------------------------------------------------------------------
    print("\n" + "=" * 74)
    print("PART 4  THE CANDIDATE CATEGORIES, ONE BY ONE")
    print("=" * 74)
    print("\nEvery tense/aspect/mood category considered for the particle")
    print("inventory, with how common it is in the world and in contact languages.")

    print("\n--- world: WALS chapters, deduplicated and weighted ---")
    for wid, what in WALS_CATEGORY.items():
        w = weighted_dist_local(wid, l1m, tot)
        print(f"\n  WALS {wid} {what} (n={int(w.n.sum())} languages)")
        print("  " + w[["n", "by_lang_pct", "by_l1_pct", "by_total_pct"]]
              .head(5).to_string().replace("\n", "\n  "))
        for opt, r in w.iterrows():
            rows.append(dict(part="category", source="wals", feature_id=wid,
                             feature=what, option=opt, n_total=int(r.n),
                             pct_lang=r.by_lang_pct, pct_l1=r.by_l1_pct,
                             pct_total=r.by_total_pct))

    print("\n--- world: Grambank, share of languages that mark the category at all ---")
    print(f"  {'category':34s} {'n':>5s} {'%lang':>6s} {'%L1':>6s} {'%tot':>6s}")
    for fid, label, kind in GB_TAM:
        if fid in tab.index and kind in ("morphology", "context"):
            r = tab.loc[fid]
            print(f"  {label:34s} {int(r.n):5d} {r.pct_lang:6.1f} {r.pct_l1:6.1f} "
                  f"{r.pct_total:6.1f}")

    print("\n--- contact languages: does the category have an overt marker at all? ---")
    print(f"  {'category':13s} {'restricted pidgin':>19s} {'expanded pidgin':>17s} {'creole':>12s}")
    for cat, (pid, absent_label) in APICS_CATEGORY.items():
        v = ap_v[ap_v.Parameter_ID.astype(str) == pid].copy()
        v["label"] = v.Code_ID.map(cmap)
        v = v.join(info, on="Language_ID")
        v = v.sort_values("Frequency", ascending=False).drop_duplicates("Language_ID")
        cells = []
        for t in TYPE_ORDER:
            sub = v[v.ctype == t]
            has = (sub.label != absent_label).sum()
            cells.append(f"{has}/{len(sub)}" if len(sub) else "-")
            rows.append(dict(part="category", source="apics", feature_id=pid,
                             feature=cat, option=t, n_total=len(sub),
                             pct_lang=round(100 * has / len(sub), 1) if len(sub) else None))
        print(f"  {cat:13s} {cells[0]:>19s} {cells[1]:>17s} {cells[2]:>12s}")
    print("\n  (APiCS codes presence indirectly, via the 'no overt X marker' option on")
    print("   the feature that otherwise describes X.)")

    print("\n--- contact languages: what an UNMARKED verb means (APiCS 51) ---")
    v = ap_v[ap_v.Parameter_ID.astype(str) == "51"].copy()
    v["label"] = v.Code_ID.map(cmap)
    v = v.join(info, on="Language_ID")
    v = v.sort_values("Frequency", ascending=False).drop_duplicates("Language_ID")
    print(pd.crosstab(v.label, v.ctype).to_string())

    pd.DataFrame(rows).to_csv(OUT, index=False)
    print(f"\nwrote {OUT}")


if __name__ == "__main__":
    main()
