"""Speech vocabulary lookup: the flat list Patrick actually translates from.

One study per script (CLAUDE.md), and this one is deliberately dumb: it does no
selection, no scoring and no linguistics.  It reads the lexicon that
`scripts/lexicon_milestone1.py` builds and flattens it into a two-column-plus
lookup, adding the COMPOUNDS - words the language expresses by putting two
existing roots together rather than by coining a root.

Inputs
------
  data/processed/lexicon_milestone1.csv   every root and borrowing

Output
------
  data/processed/speech_vocab.csv
      english_gloss, interlang_form, group, derivation

  `group` is one of
      grammar / numeral / generic / core / core-poly   native roots
      technical                                        international borrowing
      name                                             proper name
      compound                                         built from other rows

  `derivation` names the donor language for a native root, the international
  spelling for a borrowing, or the parts for a compound.

JUDGMENT CALLS
--------------
C1. COMPOUNDS ARE PREFERRED WHERE ONE ALREADY WORKS.  principles.md 3.7 makes
    compounding head-final (modifier precedes head), and lexicon-plan.md 2.4
    requires a compound to pass a two-way inferability test.  The compounds
    below are hand-written and each carries its reading; they are NOT new
    roots and cost nothing from any budget.

C2. `because` IS NOT COINED.  The generic noun `fo` "reason" already carries
    the adverbial-clause construction of principles.md 3.2 Tiers 4-5, so
    "because X" is `fo X` and no new word is needed.  Checked against the
    grammar, not assumed.

C3. `dataset` IS A COMPOUND, not a borrowing, even though the brief listed it
    with the international vocabulary: `data` and SET are both already in the
    lexicon and data-set is exactly what the compound says.

C4. THE MULTIWORD ENTRIES ARE PHRASES, NOT WORDS.  `lingua familia` and
    `mimmo lingua` are written with a space because they are noun-noun phrases
    under 3.2's head-final NP, not single compounded roots.  A reader who
    writes them solid is not wrong, but the space keeps the parts visible.

Usage: uv run python scripts/speech_vocab.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from interlang import translit                                   # noqa: E402

PROC = ROOT / "data" / "processed"
LEX = PROC / "lexicon_milestone1.csv"
OUT = PROC / "speech_vocab.csv"


def read_csv(path, **kw):
    """See lexicon_milestone1.py's docstring: `nan` is a real word."""
    kw.setdefault("keep_default_na", False)
    kw.setdefault("na_values", [""])
    return pd.read_csv(path, **kw)


# (english gloss, [concept ids of the parts], reading, note).  Parts are
# resolved to forms from the lexicon; head-final, so the LAST part is the head.
COMPOUNDS = [
    ("loanword", ["BORROW", "WORD"], "borrow-word",
     "a word that was borrowed"),
    ("learnability", ["LEARN", "QUALITY"], "learn-quality",
     "the generic-noun derivation of 3.2 Tiers 4-5: X-quality = the abstract "
     "noun of X"),
    ("recognizability", ["RECOGNIZE", "QUALITY"], "recognize-quality",
     "same pattern, on the borrowed stem"),
    ("dataset", ["DATA", "SET"], "data-set", "judgment call C3"),
    ("conlang / constructed language", ["DO OR MAKE", "LANGUAGE"],
     "make-language", "the head is `language`; the modifier is the verb root "
     "`fum` 'do/make'"),
    # question / adjective / adverb / syntax are NOT listed here: milestone 1
    # already ships them as compound rows in the lexicon, so they arrive above
    # with their own derivation and listing them again would duplicate a form.
    ("who", ["WHAT", "PERSON"], "what-person", "principles.md 3.2 Q10"),
    ("where", ["WHAT", "PLACE"], "what-place", "principles.md 3.2 Q10"),
    ("when", ["WHAT", "TIME"], "what-time", "principles.md 3.2 Q10"),
    ("why", ["WHAT", "REASON"], "what-reason", "principles.md 3.2 Q10"),
    ("how", ["WHAT", "MANNER"], "what-manner", "principles.md 3.2 Q10"),
    ("speaker (agent noun)", ["SPEAK", "PERSON"], "speak-person",
     "the agent-noun pattern of 3.2 Tiers 4-5"),
    ("researcher", ["STUDY", "PERSON"], "study-person",
     "same pattern, on the borrowed stem `studia`"),
    ("wordlist", ["WORD", "LIST"], "word-list", "head-final"),
    ("word class", ["WORD", "CATEGORY"], "word-category", "head-final"),
    ("sound system", ["SOUND", "SYSTEM"], "sound-system", "head-final"),
    ("mother tongue / first language", ["ORD", "ONE", "LANGUAGE"],
     "ordinal-one language",
     "ORD+numeral is the ordinal of 3.2; `mimmo` = 'first', then the head"),
    ("language family", ["LANGUAGE", "FAMILY (OF LANGUAGES)"],
     "language family",
     "written as two words: a head-final noun-noun phrase, not a root"),
]

# Entries that are not rows in the lexicon and not compounds: constructions the
# grammar already supplies.  (gloss, form, derivation)
GRAMMAR_NOTES = [
    ("because", "fo", "judgment call C2: the generic noun `fo` 'reason' in "
                      "3.2's adverbial-clause construction; no new root"),
]

# Multiword compounds, written with a space (judgment call C4).
SPACED = {"mother tongue / first language", "language family"}


def main() -> None:
    lex = read_csv(LEX)
    by_concept = {c: f for c, f in zip(lex["concept"], lex["form"])}
    by_concept_gloss = {c: g for c, g in zip(lex["concept"], lex["gloss"])}

    out = []
    for _, r in lex.iterrows():
        if r["source"] == "coined":
            deriv = "coined from the free monosyllable pool (no donor)"
        elif r["source"] == "compound":
            deriv = f"native compound {r['compound_parts']} ({r['compound_gloss']})"
        elif r["source"] == "translit":
            deriv = (f"international <{r['donor_form']}>"
                     if r["group"] == "technical"
                     else f"proper name <{r['donor_form']}>")
        else:
            deriv = (f"{r['donor']} ({r['donor_family']}) "
                     f"<{r['donor_form']}>").replace("  ", " ")
        out.append({"english_gloss": r["gloss"], "interlang_form": r["form"],
                    "group": r["group"], "derivation": deriv})

    for gloss, parts, reading, note in COMPOUNDS:
        missing = [p for p in parts if p not in by_concept]
        if missing:
            print(f"  ! skipping compound {gloss}: no root for {missing}")
            continue
        pieces = [by_concept[p] for p in parts]
        if "".join(pieces) in {r["interlang_form"] for r in out}:
            print(f"  ! {gloss}: {''.join(pieces)} is already a lexicon row; "
                  f"not duplicated")
            continue
        joiner = " " if gloss in SPACED else ""
        if gloss in SPACED and len(pieces) == 3:      # ORD+ONE, then the head
            form = pieces[0] + pieces[1] + " " + pieces[2]
        else:
            form = joiner.join(pieces)
        for piece in ([form] if joiner == "" else form.split()):
            assert translit.is_legal(piece, translit.VARIANTS["V3C"]), \
                f"{gloss}: {piece} is not a legal word"
        out.append({"english_gloss": gloss, "interlang_form": form,
                    "group": "compound",
                    "derivation": f"{'+'.join(pieces)} = {reading}; {note}"})

    for gloss, form, note in GRAMMAR_NOTES:
        out.append({"english_gloss": gloss, "interlang_form": form,
                    "group": "construction", "derivation": note})

    df = pd.DataFrame(out)
    order = {g: i for i, g in enumerate(
        ["grammar", "numeral", "generic", "core", "core-poly", "compound",
         "construction", "technical", "name"])}
    df["_o"] = df["group"].map(order).fillna(99)
    df = df.sort_values(["_o", "english_gloss"]).drop(columns="_o")
    PROC.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT, index=False)

    # `construction` rows are deliberate aliases of an existing root (a word
    # the grammar already supplies), so they are exempt from the dupe check.
    forms = [f for f, g in zip(df["interlang_form"], df["group"])
             if " " not in f and g != "construction"]
    dupes = sorted({f for f in forms if forms.count(f) > 1})
    print(f"  wrote {OUT} - {len(df)} entries")
    print(f"  duplicate single-word forms: {dupes if dupes else 'none'}")
    assert not dupes, f"duplicate forms in speech_vocab: {dupes}"
    print(df.groupby("group").size().to_string())
    _ = by_concept_gloss


if __name__ == "__main__":
    main()
