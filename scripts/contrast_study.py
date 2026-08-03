"""Contrast study: what share of humanity can natively hear each distinction?

Segment prevalence (scripts/phoneme_prevalence.py) says how many people have a
sound; this study prices CONTRASTS - a minimal pair in our language is only
recoverable for listeners whose native phonology distinguishes the two
categories. For each candidate contrast (A, B):

  pct_*_both     share (of languages / L1 speakers / person-language pairs)
                 whose language has BOTH members -> contrast natively audible.
  pct_*_one      exactly one member -> foreign A and B collapse onto the same
                 native category (worst case for minimal pairs).
  pct_*_neither  neither member present.
  merger_langs   languages where PHOIBLE lists one member as an ALLOPHONE of
                 the other - direct evidence the pair is actively "the same
                 sound" there (e.g. [ɾ] as allophone of /l/ in Korean).

Interpretive caveats (documented in notes/contrast-study.md):
  - "has both" ~= "hears the contrast" is an approximation in both directions:
    listeners can sometimes perceive non-native contrasts, and having both
    segments does not guarantee they contrast in every position.
  - Weighted columns use the same L1 / CLDR-total weights and majority-vote
    inventory policy as the prevalence study.

Stop-series rows: the fortis/lenis wide contrast (principles §3.4) - whether a
language has >= 2 stop categories at a place of articulation counting voicing
OR aspiration as the differentiator - is computed at the STRICT symbol level
(aspiration is stripped at the lumped level, deliberately).

Usage: uv run python scripts/contrast_study.py
Inputs: same as phoneme_prevalence.py. Output: data/processed/contrast_costs.csv
"""

from __future__ import annotations

import sys
import unicodedata
from collections import Counter
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import phoneme_prevalence as pp  # noqa: E402  (reuse lump(), cldr_totals(), policies)

OUT_CSV = ROOT / "data" / "processed" / "contrast_costs.csv"

# ---------------------------------------------------------------------------
# Candidate contrasts (lumped-level symbols). Each entry: (label, A, B, note)
# A/B may be sets to express wide classes. Chosen for relevance to the
# candidate inventory in principles.md §3.3/§3.4, plus controls.
# ---------------------------------------------------------------------------
S = lambda *xs: set(xs)  # noqa: E731
CONTRASTS = [
    # liquids / glides
    ("r / l",        S("r"), S("l"),  "the classic; r is already tap+trill+approximant+retroflex"),
    ("R-cls / L-cls", S("r", "ʀ", "ʁ"), S("l", "ɭ", "ʎ"), "widest liquid classes"),
    ("w / v",        S("w"), S("v"),  "hard for Hindi, German, ..."),
    ("v / b",        S("v"), S("b"),  "Spanish, Japanese adaptations"),
    ("w / b",        S("w"), S("b"),  ""),
    ("j / dʒ",       S("j"), S("dʒ"), "Spanish y/j territory"),
    # stop voicing (lumped level: aspiration already stripped, so these ask
    # specifically about a VOICED second series)
    ("p / b",        S("p"), S("b"),  "voiced-series cost, labial"),
    ("t / d",        S("t"), S("d"),  "voiced-series cost, coronal"),
    ("k / ɡ",        S("k"), S("ɡ"),  "voiced-series cost, velar"),
    # fricatives / affricates
    ("f / v",        S("f"), S("v"),  ""),
    ("f / p",        S("f"), S("p"),  "matters where f is missing"),
    ("s / z",        S("s"), S("z"),  ""),
    ("s / ʃ",        S("s"), S("ʃ"),  "ʃ is s's top allophone"),
    ("s / SH-cls",   S("s"), S("ʃ", "ʂ", "ɕ"), "s vs any hushing sibilant"),
    ("ʃ / tʃ",       S("ʃ"), S("tʃ"), ""),
    ("ts / tʃ",      S("ts"), S("tʃ"), ""),
    ("tʃ / dʒ",      S("tʃ"), S("dʒ"), "voicing in affricates"),
    ("s / θ",        S("s"), S("θ"),  "expected near-floor"),
    ("h / x",        S("h"), S("x"),  "wide-H members - should NOT be contrasted by us"),
    # nasals
    ("m / n",        S("m"), S("n"),  "control: should be ~universal"),
    ("n / ŋ",        S("n"), S("ŋ"),  "ŋ is n's top allophone"),
    # vowels
    ("i / e",        S("i"), S("e"),  "5- vs 3-vowel systems"),
    ("u / o",        S("u"), S("o"),  "5- vs 3-vowel systems"),
    # wide-vowel versions: many languages (English, Mandarin) analyze mid vowels
    # only as lax monophthongs or inside diphthongs, so the narrow rows above
    # undercount audible height distinctions
    ("i / E-cls",    S("i"), S("e", "ɛ"), "wide mid-front vs high"),
    ("u / O-cls",    S("u"), S("o", "ɔ"), "wide mid-back vs high"),
    ("E-cls / a",    S("e", "ɛ"), S("a"), "wide mid-front vs low"),
    ("O-cls / a",    S("o", "ɔ"), S("a"), "wide mid-back vs low"),
    ("e / ɛ",        S("e"), S("ɛ"),  "should NOT be contrasted by us (wide e)"),
    ("o / ɔ",        S("o"), S("ɔ"),  "should NOT be contrasted by us (wide o)"),
    ("i / ɪ",        S("i"), S("ɪ"),  "English-style lax vowel"),
    ("u / ʊ",        S("u"), S("ʊ"),  ""),
    ("a / ə",        S("a"), S("ə"),  ""),
    ("e / i vs a",   S("e", "i"), S("a"), "sanity control"),
    ("u / y",        S("u"), S("y"),  "front rounded - expected floor"),
]

# Fortis/lenis stop series (strict level): >= 2 distinct categories at a place,
# counting plain / aspirated / voiced / breathy as different categories.
SERIES = {
    "2-way labial stops (p pʰ b bʱ)":  ["p", "pʰ", "b", "bʱ"],
    "2-way coronal stops (t tʰ d dʱ)": ["t", "tʰ", "d", "dʱ"],
    "2-way velar stops (k kʰ ɡ ɡʱ)":   ["k", "kʰ", "ɡ", "ɡʱ"],
}


def strip_variants(sym: str) -> str:
    """Light normalization for strict-level series detection: drop sub-place
    and similar noise diacritics but KEEP aspiration/voicing/breathiness."""
    keep_out = pp.LUMP_STRIP - {"ʰ", "ʱ"}
    s = unicodedata.normalize("NFD", sym)
    s = "".join(ch for ch in s if ch not in keep_out)
    return unicodedata.normalize("NFC", s)


def main() -> None:
    values = pd.read_csv(pp.PHOIBLE / "values.csv", low_memory=False)
    langs = pd.read_csv(pp.PHOIBLE / "languages.csv")
    values = values[values["Marginal"] != True]  # noqa: E712  (no-op, documented)
    values["lumped"] = values["Value"].map(pp.lump)
    values["strictn"] = values["Value"].map(strip_variants)
    n_inv = values.groupby("Language_ID")["Inventory_ID"].nunique()

    # --- weights (same policy as prevalence study) --------------------------
    l1 = pd.read_csv(pp.L1_CSV)
    l1_by_iso = dict(zip(l1["iso639_3"], l1["l1_speakers"]))
    l1_by_glotto = dict(zip(l1.loc[l1["glottocode"].notna(), "glottocode"],
                            l1.loc[l1["glottocode"].notna(), "l1_speakers"]))
    totals_by_iso, _ = pp.cldr_totals()
    meta = langs.set_index("ID")
    rows = {}
    for lid in n_inv.index:
        iso = meta.at[lid, "ISO639P3code"] if lid in meta.index else None
        glotto = meta.at[lid, "Glottocode"] if lid in meta.index else None
        w_l1 = l1_by_iso.get(iso, l1_by_glotto.get(glotto))
        w_l1 = float(pp.L1_DEFAULT if w_l1 is None else w_l1)  # explicit 0 stays 0
        rows[lid] = (w_l1, float(totals_by_iso.get(iso, w_l1)))
    W = pd.DataFrame.from_dict(rows, orient="index", columns=["w_l1", "w_total"])
    sum_l1, sum_total, n_langs = W["w_l1"].sum(), W["w_total"].sum(), len(W)

    # --- majority-vote presence sets per language ---------------------------
    def presence_sets(col: str) -> dict[str, set]:
        cnt = (values.drop_duplicates(["Language_ID", "Inventory_ID", col])
               .groupby(["Language_ID", col]).size().rename("k").reset_index())
        cnt["n"] = cnt["Language_ID"].map(n_inv)
        cnt = cnt[cnt["k"] * 2 >= cnt["n"]]
        return cnt.groupby("Language_ID")[col].agg(set).to_dict()

    lumped_sets = presence_sets("lumped")
    strict_sets = presence_sets("strictn")

    # --- allophone merger evidence ------------------------------------------
    # (language, lumped_phoneme) -> set of lumped allophones listed for it
    allo = values.dropna(subset=["Allophones"])
    allo_map: dict[tuple, set] = {}
    for lid, sym, al in zip(allo["Language_ID"], allo["lumped"], allo["Allophones"]):
        allo_map.setdefault((lid, sym), set()).update(pp.lump(a) for a in str(al).split())

    def merger_count(a_set: set, b_set: set) -> int:
        """Languages where some member of one side is an allophone of a phoneme
        from the other side (and the language lacks the first side as a phoneme
        of its own - i.e., a genuine merger, not free variation on top)."""
        n = 0
        for lid, inv in lumped_sets.items():
            has_a, has_b = bool(inv & a_set), bool(inv & b_set)
            if has_a == has_b:
                continue  # merger evidence only meaningful when exactly one side present
            present, absent = (a_set, b_set) if has_a else (b_set, a_set)
            if any(allo_map.get((lid, p), set()) & absent for p in present & inv):
                n += 1
        return n

    # --- score contrasts -----------------------------------------------------
    out = []

    def add_row(label: str, note: str, has_fn) -> None:
        both = one = neither = 0.0
        both_t = one_t = 0.0
        nb = n1 = 0
        for lid in lumped_sets:
            k = has_fn(lid)
            wl, wt = W.at[lid, "w_l1"], W.at[lid, "w_total"]
            if k == 2:
                both += wl; both_t += wt; nb += 1
            elif k == 1:
                one += wl; one_t += wt; n1 += 1
            else:
                neither += wl
        out.append({
            "contrast": label,
            "pct_l1_both": both / sum_l1,
            "pct_total_both": both_t / sum_total,
            "pct_langs_both": nb / n_langs,
            "pct_l1_one": one / sum_l1,
            "pct_langs_one": n1 / n_langs,
            "note": note,
        })

    for label, a_set, b_set, note in CONTRASTS:
        def has(lid, a=a_set, b=b_set):
            inv = lumped_sets.get(lid, set())
            return bool(inv & a) + bool(inv & b)
        add_row(label, note, has)
        out[-1]["merger_langs"] = merger_count(a_set, b_set)

    for label, members in SERIES.items():
        def has(lid, m=members):
            k = len(strict_sets.get(lid, set()) & set(m))
            return 2 if k >= 2 else k
        add_row(label, "fortis/lenis wide contrast, strict level", has)
        out[-1]["merger_langs"] = None

    df = pd.DataFrame(out).sort_values("pct_l1_both", ascending=False)
    for c in [c for c in df.columns if c.startswith("pct_")]:
        df[c] = df[c].round(4)
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT_CSV, index=False)
    print(f"Wrote {OUT_CSV} ({len(df)} contrasts)\n")
    show = df[["contrast", "pct_l1_both", "pct_total_both", "pct_langs_both",
               "pct_l1_one", "merger_langs", "note"]]
    print(show.to_string(index=False))


if __name__ == "__main__":
    main()
