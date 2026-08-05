"""Tier 2 Q11 + Q7: noun-phrase order, and the categories the noun carries.

Agenda: notes/grammar-plan.md 4.  Two questions run together because they
compete for the same real estate - an article, a demonstrative and a numeral all
want the same slot next to the noun.

  Q11 NP-INTERNAL ORDER.  Demoted out of Tier 0 when head-directionality turned
      out not to be a single parameter: creoles split 8:7 on adjective, numeral
      and possessor order, three coin flips in a row (grammar-tier0.md 1).
  Q7  NOMINAL CATEGORIES.  Obligatory number?  Articles?  Classifiers?  What
      does a bare noun mean?

Q11 is run FIRST and Q11a (adverb placement) inherits from it, on Patrick's
design principle (2026-08-05): **modifiers should behave the same way whatever
they modify.**  If adjectives precede nouns then adverbs precede verbs - one
"modifier position" rule instead of two.  That makes the harmony test in part 2
the load-bearing analysis of this study rather than a curiosity.

The three analyses
------------------
1. ORDER, stratified by contact type and weighted for the world.  Tier 0 used
   pooled APiCS; this re-cuts it as restricted pidgin / expanded pidgin / creole
   per grammar-plan.md 5, which was not available when Tier 0 ran.

2. NP-INTERNAL HARMONY - the new one.  Within a single language, do adjective,
   numeral and demonstrative sit on the SAME side of the noun?  This is what
   decides whether "one modifier rule" is a natural design or an invented
   regularity: if the world's languages are internally consistent, adopting one
   rule copies them; if they are not, we are imposing a pattern that no
   population has a head start on.  Grambank codes all three on a common scale
   (1 = modifier-before-noun, 2 = noun-before-modifier, 3 = both), so this is a
   like-for-like comparison inside each language.

3. Q7's categories, same treatment, with the Rule 2 contrapositive run on
   ARTICLES specifically - the Euro-coded feature in this part of the grammar,
   and the one most likely to be adopted by default.

Policies baked in here
----------------------
  - Contact-type stratification, doculect dedup, `?`-is-not-coverage and
    population weighting are all inherited from scripts/grammar_sources.py and
    scripts/grammar_tier2_tam.py; see those docstrings.
  - Grambank value 3 ("both orders") is kept as its own category, never merged
    into either side - a language with free order is evidence for neither.
  - The harmony test only counts languages with a non-`?`, non-"both" value on
    all three features, so "harmonic" means genuinely committed on all three.
  - APiCS 23 (expression of plural) mixes strategy with position; only its
    "plural word preceding/following" values are read as order evidence.

Usage:   uv run python scripts/grammar_tier2_np.py
Inputs:  data/raw/{wals,grambank,apics}/cldf/*.csv, data/processed/l1_speakers.csv
Outputs: data/processed/grammar_tier2_np.csv
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
from grammar_tier2_tam import TYPE_ORDER, contact_type  # noqa: E402

OUT = ROOT / "data" / "processed" / "grammar_tier2_np.csv"

# (label, APiCS param, WALS chapter, Grambank feature, grambank "modifier first" code)
ORDER = [
    ("adjective & noun",     "3", "87A", "GB193", "1"),
    ("numeral & noun",       "6", "89A", "GB024", "1"),
    ("demonstrative & noun", "5", "88A", "GB025", "1"),
    ("possessor & noun",     "2", "86A", "GB065", "1"),
]
HARMONY_FEATURES = ["GB193", "GB024", "GB025"]     # adjective, numeral, demonstrative

# Q7: what the noun carries.  (APiCS param, label)
APICS_Q7 = {
    "22": "occurrence of nominal plural markers",
    "28": "definite articles",
    "29": "indefinite articles",
    "36": "sortal numeral classifiers",
    "9":  "position of the definite article",
}
GB_Q7 = {
    "GB020": "definite/specific articles",
    "GB021": "indefinite articles",
    "GB022": "prenominal articles",
    "GB023": "postnominal articles",
    "GB044": "productive plural marking on nouns",
    "GB057": "numeral classifiers",
    "GB058": "possessive classifiers",
}
WALS_Q7 = {"33A": "coding of nominal plurality", "37A": "definite articles",
           "38A": "indefinite articles", "55A": "numeral classifiers"}


def apics_table(pid, ap_v, ap_l, cmap):
    v = ap_v[ap_v.Parameter_ID.astype(str) == str(pid)].copy()
    v["label"] = v.Code_ID.map(cmap)
    v = v.join(ap_l.set_index("ID")[["Name", "ctype", "grp"]], on="Language_ID")
    v = v.sort_values("Frequency", ascending=False).drop_duplicates("Language_ID")
    ct = pd.crosstab(v.label, v.ctype)
    for t in TYPE_ORDER:
        if t not in ct:
            ct[t] = 0
    return v, ct[TYPE_ORDER]


def wals_dist(fid, l1m, tot):
    langs, _p, vals = load("wals")
    langs = weight(langs, l1m, tot)
    cm = dict(zip(*pd.read_csv(ROOT / "data/raw/wals/cldf/codes.csv")[["ID", "Name"]].values.T))
    v = vals[(vals.Parameter_ID == fid) & (vals.Value.astype(str) != "?")].copy()
    k = langs.set_index("ID")
    v["gc"] = v.Language_ID.map(k.Glottocode)
    v["l1"] = v.Language_ID.map(k.l1).fillna(0.0)
    v["tot"] = v.Language_ID.map(k.total).fillna(0.0)
    v = v[v.gc.notna()].drop_duplicates("gc")
    v["label"] = v.Code_ID.map(cm).fillna(v.Value.astype(str))
    g = v.groupby("label").agg(n=("gc", "size"), l1=("l1", "sum"), t=("tot", "sum"))
    g["by_lang"] = (100 * g.n / g.n.sum()).round(1)
    g["by_L1"] = (100 * g.l1 / g.l1.sum()).round(1)
    g["by_total"] = (100 * g.t / g.t.sum()).round(1)
    return g.sort_values("by_lang", ascending=False)[["n", "by_lang", "by_L1", "by_total"]]


def main() -> None:
    (l1m, tot, W1, WT) = populations()
    rows = []

    ap_l, _ap_p, ap_v = load("apics")
    ap_l["ctype"] = [contact_type(n) for n in ap_l.Name]
    ap_l["grp"] = ""
    cmap = dict(zip(*pd.read_csv(ROOT / "data/raw/apics/cldf/codes.csv")[["ID", "Name"]].values.T))

    gb_l, _p, gb_v = load("grambank")
    gb_l = gb_l[gb_l.level == "language"]
    gb_v = gb_v[gb_v.Language_ID.isin(set(gb_l.ID))]
    gb_l = weight(gb_l, l1m, tot)
    gk = gb_l.set_index("ID")
    gbc = dict(zip(*pd.read_csv(ROOT / "data/raw/grambank/cldf/codes.csv")[["ID", "Description"]].values.T))

    # =================================================================
    print("=" * 76)
    print("Q11  NP-INTERNAL ORDER")
    print("=" * 76)
    for label, apid, wals_id, gb_id, _first in ORDER:
        print(f"\n--- {label} ---")
        _v, ct = apics_table(apid, ap_v, ap_l, cmap)
        ct["total"] = ct.sum(axis=1)
        print(ct.sort_values("total", ascending=False).to_string())
        w = wals_dist(wals_id, l1m, tot)
        print(f"  WALS {wals_id} (n={int(w.n.sum())}): " +
              "; ".join(f"{k} {r.by_lang}%/L1 {r.by_L1}%" for k, r in w.head(3).iterrows()))
        for opt, r in ct.iterrows():
            rows.append(dict(part="order", feature=label, source="apics", option=opt,
                             restricted=r[TYPE_ORDER[0]], expanded=r[TYPE_ORDER[1]],
                             creole=r[TYPE_ORDER[2]]))
        for opt, r in w.iterrows():
            rows.append(dict(part="order", feature=label, source="wals", option=opt,
                             n=r.n, by_lang=r.by_lang, by_L1=r.by_L1, by_total=r.by_total))

    # =================================================================
    print("\n" + "=" * 76)
    print("Q11 PART 2  NP-INTERNAL HARMONY - do modifiers agree on a side?")
    print("=" * 76)
    print("\nWithin one language: adjective, numeral and demonstrative order, from")
    print("Grambank's common 1=Mod-N / 2=N-Mod / 3=both scale.  'Committed' means a")
    print("non-'?', non-'both' value on all three.\n")
    h = gb_v[gb_v.Parameter_ID.isin(HARMONY_FEATURES)].copy()
    h["gc"] = h.Language_ID.map(gk.Glottocode)
    h = h[h.gc.notna() & h.Value.astype(str).isin(["1", "2"])]
    p = h.pivot_table(index="gc", columns="Parameter_ID", values="Value", aggfunc="first")
    p = p.dropna()
    l1_of = h.drop_duplicates("gc").set_index("gc")["Language_ID"].map(gk.l1).fillna(0.0)
    p["pattern"] = p[HARMONY_FEATURES].agg("".join, axis=1)
    p["harmonic"] = p.pattern.isin(["111", "222"])
    n = len(p)
    hl1 = l1_of.reindex(p[p.harmonic].index).fillna(0).sum() / l1_of.reindex(p.index).fillna(0).sum()
    print(f"  {n} languages committed on all three.")
    print(f"  ALL THREE ON THE SAME SIDE: {p.harmonic.sum()} ({100*p.harmonic.mean():.0f}% of "
          f"languages, {100*hl1:.0f}% of their L1 mass)")
    names = {"1": "Mod-N", "2": "N-Mod"}
    tally = p.pattern.value_counts()
    print("\n  pattern (adjective, numeral, demonstrative):")
    for pat, cnt in tally.items():
        l1 = 100 * l1_of.reindex(p[p.pattern == pat].index).fillna(0).sum() / \
            l1_of.reindex(p.index).fillna(0).sum()
        star = "  <- harmonic" if pat in ("111", "222") else ""
        print(f"    {' / '.join(names[c] for c in pat):26s} {cnt:4d}  "
              f"{100*cnt/n:5.1f}% of languages  {l1:5.1f}% of L1{star}")
        rows.append(dict(part="harmony", feature="Adj/Num/Dem pattern", source="grambank",
                         option=" / ".join(names[c] for c in pat), n=cnt,
                         by_lang=round(100 * cnt / n, 1), by_L1=round(l1, 1)))
    # pairwise agreement, to see WHICH pair is the odd one out
    print("\n  pairwise agreement:")
    lab = {"GB193": "adjective", "GB024": "numeral", "GB025": "demonstrative"}
    for a, b in (("GB193", "GB024"), ("GB193", "GB025"), ("GB024", "GB025")):
        agree = (p[a] == p[b]).mean()
        print(f"    {lab[a]} vs {lab[b]:14s} agree {100*agree:.0f}%")
        rows.append(dict(part="harmony", feature=f"{lab[a]} vs {lab[b]}",
                         source="grambank", option="agree", by_lang=round(100 * agree, 1)))

    # =================================================================
    print("\n" + "=" * 76)
    print("Q7  WHAT THE NOUN CARRIES")
    print("=" * 76)
    for pid, label in APICS_Q7.items():
        print(f"\n--- APiCS {pid}: {label} ---")
        _v, ct = apics_table(pid, ap_v, ap_l, cmap)
        ct["total"] = ct.sum(axis=1)
        print(ct.sort_values("total", ascending=False).to_string())
        for opt, r in ct.iterrows():
            rows.append(dict(part="q7", feature=label, source="apics", option=opt,
                             restricted=r[TYPE_ORDER[0]], expanded=r[TYPE_ORDER[1]],
                             creole=r[TYPE_ORDER[2]]))

    print("\n--- world (Grambank binaries): share of languages with the feature ---")
    print(f"  {'feature':34s} {'n':>5s} {'%lang':>6s} {'%L1':>6s} {'%tot':>6s}")
    v = gb_v[gb_v.Parameter_ID.isin(GB_Q7) & gb_v.Value.astype(str).isin(["0", "1"])].copy()
    v["gc"] = v.Language_ID.map(gk.Glottocode)
    v["l1"] = v.Language_ID.map(gk.l1).fillna(0.0)
    v["tot"] = v.Language_ID.map(gk.total).fillna(0.0)
    v = v[v.gc.notna()].drop_duplicates(["gc", "Parameter_ID"])
    for fid, label in GB_Q7.items():
        g = v[v.Parameter_ID == fid]
        if not len(g):
            continue
        yes = g[g.Value.astype(str) == "1"]
        pl, p1, pt = (100 * len(yes) / len(g), 100 * yes.l1.sum() / g.l1.sum(),
                      100 * yes.tot.sum() / g.tot.sum())
        print(f"  {label:34s} {len(g):5d} {pl:6.1f} {p1:6.1f} {pt:6.1f}")
        rows.append(dict(part="q7", feature=label, source="grambank", option="yes",
                         n=len(g), by_lang=round(pl, 1), by_L1=round(p1, 1),
                         by_total=round(pt, 1)))

    print("\n--- world (WALS chapters) ---")
    for wid, label in WALS_Q7.items():
        w = wals_dist(wid, l1m, tot)
        print(f"\n  WALS {wid} {label} (n={int(w.n.sum())})")
        print("  " + w.head(4).to_string().replace("\n", "\n  "))
        for opt, r in w.iterrows():
            rows.append(dict(part="q7", feature=label, source="wals", option=opt,
                             n=r.n, by_lang=r.by_lang, by_L1=r.by_L1, by_total=r.by_total))

    # ---- Rule 2 on ADJECTIVE ORDER, the directional test --------------
    # Asked by Patrick 2026-08-05: when contact languages change adjective order
    # from their lexifier, which way do they go?  Lexifier values come from WALS
    # 87A rather than by hand.  Bantu and the "Other" lexifiers have no clean
    # WALS entry and are dropped rather than guessed.
    LEX_WALS = {"English": "English", "French": "French", "Spanish": "Spanish",
                "Portuguese": "Portuguese", "Dutch": "Dutch",
                "Arabic": "Arabic (Egyptian)", "Malay": "Indonesian"}
    wl, _wp, wv = load("wals")
    wcm = dict(zip(*pd.read_csv(ROOT / "data/raw/wals/cldf/codes.csv")[["ID", "Name"]].values.T))
    a = wv[wv.Parameter_ID == "87A"].copy()
    a["lang"] = a.Language_ID.map(wl.set_index("ID")["Name"])
    wals_adj = dict(zip(a.lang, a.Code_ID.map(wcm)))
    va, _ct = apics_table("3", ap_v, ap_l, cmap)
    va = va.join(ap_l.set_index("ID")[["Lexifier"]], on="Language_ID")
    side = {"Modifying adjective precedes noun": "Adj-N",
            "Modifying adjective follows noun": "N-Adj"}
    lex_side = {"Adjective-Noun": "Adj-N", "Noun-Adjective": "N-Adj"}
    va["creole_side"] = va.label.map(side)
    va["lex_side"] = va.Lexifier.map(
        lambda lx: lex_side.get(wals_adj.get(LEX_WALS.get(lx, ""), ""), None))
    j = va.dropna(subset=["creole_side", "lex_side"])
    j = j[j.ctype != "0 mixed (excluded)"]
    j["verdict"] = ["SAME" if x == y else "CHANGED"
                    for x, y in zip(j.creole_side, j.lex_side)]
    print("\n--- Rule 2 DIRECTIONAL: when adjective order changes, which way? ---")
    print(f"  {len(j)} contact languages pairable with a WALS-coded lexifier")
    print(pd.crosstab(j.ctype, j.verdict).to_string())
    print("\n  by the lexifier's own order:")
    print("  " + pd.crosstab(j.lex_side, j.verdict).to_string().replace("\n", "\n  "))
    moved = j[j.verdict == "CHANGED"]
    print(f"\n  of the {len(moved)} that changed, direction of travel: "
          + "; ".join(f"{k} {v}" for k, v in
                      (moved.lex_side + " -> " + moved.creole_side).value_counts().items()))
    for _i, r in j.iterrows():
        rows.append(dict(part="rule2-adj", feature="adjective order", source="apics+wals",
                         option=r.verdict, creole=r.Name, n=1,
                         by_lang=None, by_L1=None))

    # ---- Rule 2 on articles, the Euro-coded feature here -------------
    print("\n--- Rule 2: articles, creole vs its own lexifier (identical features) ---")
    val = {(r.Language_ID, r.Parameter_ID): str(r.Value) for r in gb_v.itertuples()
           if r.Parameter_ID in ("GB020", "GB021", "GB044", "GB057")}
    names_gb = dict(zip(gb_l.ID, gb_l.Name))
    recs = []
    for creole, (lex, lex_label, _n) in LEXIFIER_OF.items():
        for fid in ("GB020", "GB021", "GB044", "GB057"):
            c, l = val.get((creole, fid), "?"), val.get((lex, fid), "?")
            if c in ("0", "1") and l in ("0", "1"):
                recs.append(dict(feature=GB_Q7[fid], creole=names_gb.get(creole, creole),
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
