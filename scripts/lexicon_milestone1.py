"""Lexicon milestone 1: a small, sanity-checkable word list (~130 words).

The first thing in the project that produces actual interlang WORDS.  It is a
sanity check on the machinery, not the lexicon: everything here is meant to be
read, argued with and re-run, and every number it prints is reproducible from
data on disk plus one Wikipedia API endpoint.

Three word groups (notes/lexicon-milestone1.md interprets the output):

  G1 GRAMMAR    the complete closed class of principles.md 3.2 - 19 words,
                all monosyllabic.
  G2 CORE       the top 50 concepts of the ranked Leipzig-Jakarta list
                (Concepticon `Tadmor-2009-100`), minus the ones G1 already
                covers, plus the numerals 0-10 and the nine generic nouns the
                grammar leans on (person/thing/place/time/reason/manner/
                quality/action/tool).  All monosyllabic.
  G3 TECHNICAL  ~50 words for talking about the project itself.  These are
                international borrowings, rendered by src/interlang/translit.py,
                and they are POLYSYLLABIC BY CONSTRUCTION - which is the point:
                they cost nothing from the monosyllable budget.

Inputs
------
  data/raw/wold/cldf/{parameters,forms,languages}.csv   donor word forms
  data/raw/concepticon/Tadmor-2009-100.tsv              the ranked core list
  data/raw/concepticon/Swadesh-1955-100.tsv             cross-check only
      (both fetched by this script on first run; --offline reuses the cache)
  data/processed/l1_speakers.csv                        L1 populations
  data/raw/cldr_supplementalData.xml + data/raw/iso639/ total-speaker weights
  data/raw/wikipedia_langlinks/*.json                   recognition panel
      (fetched on first run, same cache as scripts/international_vocab.py)

Output
------
  data/processed/lexicon_milestone1.csv   one row per word, with the form,
      syllable count, donor language + family, the segment cost it paid, and
      the recognition estimate with the threshold it met.

Usage: uv run python scripts/lexicon_milestone1.py [--offline] [--hard-distance2]
  --offline         never hit the network; use the cached lists and langlinks
  --hard-distance2  the priced alternative arm of judgment call 10 (see below)

NOTE ON READING THE OUTPUT CSV: the 2PL pronoun is the string `nan`, which
pandas parses as a float NaN.  Read it with `keep_default_na=False`, the same
trap `interlang.populations.read_l1_speakers` documents for ISO code `nan`.

===========================================================================
JUDGMENT CALLS BAKED INTO THIS SCRIPT.  All of them are PROVISIONAL and are
repeated in notes/lexicon-milestone1.md.
===========================================================================

1. DISCOURAGEMENT WEIGHTS ARE INVENTED HERE (principles.md 3.3/3.6/7 leave them
   ordinal).  Cost per occurrence in a form, before the frequency multiplier:

       /r/ 1.00   /h/ 1.00        (3.3: "strongly discouraged")
       /l/ 0.50                   (3.3: "moderately")
       /b/ /d/ /g/ 0.20 each      (3.3: "mildly")
       Cr/Cl onset cluster 0.40   (3.6: a structural item on the same footing)
       root-internal hiatus 0.15, root-internal geminate 0.30
                                  (3.7/7: both are compound-boundary signals
                                   and should not be spent inside a root)
       NO ONSET (a bare V or VN root) 0.30
                                  (NEW HERE, not in principles.md.  An
                                   onsetless root guarantees a hiatus at every
                                   compound seam that precedes it, which spends
                                   the boundary signal 3.7 wants to keep.  It
                                   is added because without it the cost
                                   function has a degenerate optimum: the five
                                   bare vowels are the cheapest forms in the
                                   language, so the first five coined
                                   particles took a/e/i/o/u.  In G1/G2 it is
                                   escalated to a ban, with r/h/l, for the same
                                   reason - at cost 0.30 a big-donor bid still
                                   won it, and *i* "stone" is not a root this
                                   language should spend.  Borrowed G3 stems
                                   may be vowel-initial and pay nothing.)

   Frequency multiplier (lexicon-plan.md 2.6 - "penalty = base x frequency"):
       G1 grammar x3.0 · numerals/generic nouns x2.0 · G2 core x1.5 · G3 x0.0

   G3 is x0.0 rather than x1.0 on purpose: 3.6 requires the cluster and segment
   penalties never to override recognizability on a borrowed stem, and the
   simplest way to guarantee that is to let borrowed stems pay nothing.  The
   costs are still REPORTED for G3 so the bill is visible.

2. IN G1 AND G2, /r/ /h/ /l/ ARE BANNED FROM ROOTS, NOT MERELY PENALISED.
   A stricter reading of 3.3's "applies with extra force to particles and basic
   vocabulary".  Taken for three reasons: it makes both minimal-pair bans (l~r,
   h~r) automatically satisfied inside G1+G2; it makes the budget arithmetic
   clean; and it keeps the segments free for the borrowed stems that cannot
   avoid them.  /b d g/ are allowed and pay.

3. THE MONOSYLLABLE BUDGET is computed, not assumed.  Onsets {12 C} (15 minus
   r, h, l; no onsetless syllables, per call 1) x 5 vowels x codas {none, n, m}
   = 180, minus the six homorganic glide+high-vowel syllables
   ji/jin/jim/wu/wun/wum, which no inventory of this shape should spend
   = 174 usable.  lexicon-plan.md 1 says "~180"; this is the same number
   computed under a stated policy.

4. DONOR FORMS COME FROM WOLD (41 languages, 25 families, 6 macroareas),
   filtered to `unanalyzable` forms with Borrowed_score <= 0.25 - i.e. the
   language's OWN word, not something it borrowed - because a borrowed donor
   form would attribute representation to the wrong family.  WOLD forms are
   quasi-phonetic transcriptions in mixed conventions; they are stripped of
   tone digits, length marks, ejectives and diacritics and then read by
   translit.to_phonemes with LATIN values (rule A0).  This is ROUGH and it is
   the largest source of error in G1/G2.

5. MONOSYLLABIFICATION: a donor's contribution is the FIRST SYLLABLE of its
   adapted form ((C)V(N), initial-stress position, so the most salient one).
   `moto` -> mo, `kütral` -> ku, `bank` -> ban.  Candidates whose first
   syllable is banned by (2) or (3) are dropped, not repaired.

6. FORM ASSIGNMENT IS GREEDY, NOT GLOBAL.  Concepts are processed in a fixed
   order (grammar, numerals, generic nouns, then core by Leipzig-Jakarta rank);
   each takes the best free syllable available at that point.  A global
   assignment would score better; this is a milestone, and greedy is
   inspectable.  Score per candidate:

       score = W_EASE * ease(donor) - cost(form) - W_REP * n_roots_from_family

   `ease` is log1p(total speakers)/log1p(max) - objective 1 of principles.md 2,
   weighted by total (L1+L2) speakers.  The W_REP term is objective 2: each
   root already taken from a family makes the next one from that family worse,
   which is the cheap greedy stand-in for 2's squared representation term.

7. RECOGNIZABILITY ESTIMATE = PATRICK'S APPROXIMATION (2026-08-06), stated by
   him as: *if language A borrowed a word from source S recently and without
   much later change, and we take the same word from S under our
   transliteration rule, a speaker of A will recognize ours.*  He knows it is
   false in general and wants it as a tractable approximation.  Implemented as:

     - take the Wikipedia article title of the concept in every language that
       has one (the langlinks API, same cache as international_vocab.py);
     - romanise it with the tables in scripts/international_vocab.py;
     - score it against OUR form with metric v0;
     - count the language as recognizing if similarity >= 0.60, and sum the L1
       speakers of the languages that do, over world L1.

   The threshold is reported as a TWO-ARM SENSITIVITY, not a point: 0.60 is the
   headline arm and 0.70 the strict arm, because inspection of the hits shows
   the instrument failing in both directions at 0.60 - Turkish *bilgisayar*
   scores 0.648 against `komputeri` (a false positive: it is a native coinage)
   while English *grammar* scores 0.609 against `gramatika` (a false negative
   only because 0.60 is so close).  Read the band, not the number.

   Every part of that is arguable.  In particular: 0.60 is a hand-set threshold
   over a metric whose random floor is ~0.46 (notes/data-audit.md); the panel
   is "languages with a Wikipedia article AND a script we can romanise", so
   Chinese, Japanese-in-kanji, Bengali, Telugu, Amharic and others fall out and
   are counted as NOT recognizing; and listener conditioning (metric.py's
   projection onto the listener's PHOIBLE inventory) is NOT applied.  All three
   push the estimate DOWN, so the numbers are lower bounds.  Thresholds, from
   Patrick: >50% MUST be adopted directly, >30% SHOULD be by default.

8. FINAL-CODA POLICY: this script uses `final_policy="epenthesize"`, NOT
   translit.py's `"delete"` default.  principles.md 3.6 is FIRM that an illegal
   word-final consonant takes a support vowel (*bank* -> *banki*, *virus* ->
   *firusi*); "delete" is a leftover study arm from the template comparison.
   Logged as a defect in translit.py's default rather than silently worked
   around.

10. DISTINCTIVENESS IS PRICED, not just banned.  3.3 makes l~r and h~r hard
   minimal-pair bans and says a kept-but-expensive contrast can be made cheap
   "in practice by forbidding minimal pairs that hinge on it".  This script
   generalises that into a soft term: a monosyllable that differs from a word
   already assigned in only ONE of (onset, vowel, coda) pays W_DIST = 0.5.
   Without it the greedy assignment happily produced *jo* "you" beside *je*
   "he/she/it" - a vowel-only contrast between the two most confusable and most
   frequent words in the language.

11. WHICH INTERNATIONAL SPELLING a G3 word starts from is the one decision
   principles.md 7 says is lexical rather than rule-resolvable.  It is a hand
   choice per word, listed in TECH below, and it is [recall]: no source was
   checked for "the international form of X".  The recognition estimate then
   MEASURES whether the choice was any good.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
import unicodedata
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))

from interlang import metric, translit                      # noqa: E402
from interlang.populations import cldr_totals, read_l1_speakers  # noqa: E402

# Romanisation tables live in the international-vocabulary study.  Importing a
# script from a script is a deviation from the one-study-per-file convention;
# the alternative was copying ~120 lines of script tables, and duplicated
# tables drift.  If a third caller appears, move them to src/interlang/.
import international_vocab as iv                            # noqa: E402

RAW = ROOT / "data" / "raw"
PROC = ROOT / "data" / "processed"
LANGLINKS = RAW / "wikipedia_langlinks"
CONCEPTICON = RAW / "concepticon"
OUT_CSV = PROC / "lexicon_milestone1.csv"

API = "https://en.wikipedia.org/w/api.php"
CONCEPTICON_URL = ("https://raw.githubusercontent.com/concepticon/concepticon-data/"
                   "master/concepticondata/conceptlists/{}.tsv")
USER_AGENT = ("interlang-research/0.1 (https://github.com/pthill; "
              "kevin.patrick.thill@gmail.com)")

# ---------------------------------------------------------------------------
# POLICY CONSTANTS  (judgment calls 1-3, 6, 7)
# ---------------------------------------------------------------------------
SEG_COST = {"r": 1.00, "h": 1.00, "l": 0.50, "b": 0.20, "d": 0.20, "g": 0.20}
CLUSTER_COST = 0.40
HIATUS_COST = 0.15
GEMINATE_COST = 0.30
NO_ONSET_COST = 0.30

FREQ_WEIGHT = {"grammar": 3.0, "numeral": 2.0, "generic": 2.0,
               "core": 1.5, "technical": 0.0}

BANNED_ONSETS = set("rhl")          # in monosyllabic roots only (call 2)
BANNED_SYLLABLES = {"ji", "jin", "jim", "wu", "wun", "wum"}

W_EASE = 1.00
W_REP = 0.35
W_DIST = 0.90                       # penalty for landing 1 feature from a word
                                    # already assigned, scaled by the frequency
                                    # class (see judgment call 10)
RECOG_THRESHOLD = 0.60              # headline arm: similarity = "recognized"
RECOG_THRESHOLD_STRICT = 0.70       # strict arm, reported as a band
MUST_SHARE, SHOULD_SHARE = 0.50, 0.30

VOWELS = "aeiou"
CODAS = ["", "n", "m"]
ALL_ONSETS = [""] + list("ptkbdgmnfshjwlr")

# ---------------------------------------------------------------------------
# GROUP 1: the closed class (principles.md 3.2).  `wold` is the WOLD parameter
# ID whose forms are used as donor candidates; None = no WOLD concept exists,
# so the word is coined from the free pool.
# ---------------------------------------------------------------------------
GRAMMAR = [
    ("1SG", "I (speaker)", "2-91"),
    ("2SG", "you (one addressee)", "2-92"),
    ("3SG", "he/she/it", "2-93"),
    ("1PL", "we", "2-94"),
    ("2PL", "you (more than one)", "2-95"),
    ("3PL", "they", "2-96"),
    ("SELF", "reflexive, invariant; also the passive marker", None),
    ("NEG", "negator, immediately before the verb", "24-06"),
    ("Q", "question particle, clause-initial", None),
    ("WHAT", "the one interrogative root; who = WHAT+person", "17-64"),
    ("COP", "copula; alone = existential", "24-01"),
    ("AND", "and", "17-51"),
    ("OR", "or", "17-54"),
    ("THAN", "comparative standard marker", None),
    ("IF", "if; conditional", "17-53"),
    ("REL", "relativizer / complementizer", None),
    ("ORD", "ordinal marker (ORD + numeral)", None),
    ("YES", "yes - answers the fact, not the polarity", "17-55"),
    ("NO", "no - answers the fact, not the polarity", "17-56"),
]

NUMERALS = [
    ("ZERO", "0", "13"), ("ONE", "1", "13-01"), ("TWO", "2", "13-02"),
    ("THREE", "3", "13-03"), ("FOUR", "4", "13-04"), ("FIVE", "5", "13-05"),
    ("SIX", "6", "13-06"), ("SEVEN", "7", "13-07"), ("EIGHT", "8", "13-08"),
    ("NINE", "9", "13-09"), ("TEN", "10", "13-1"),
]

# The nine generic nouns that principles.md 3.2 (Tiers 4-5) makes carry four
# constructions at once: interrogatives, adverbial clauses, indefinites and
# derivation.  They are the heaviest compounding elements in the language, so
# they get monosyllables.
GENERIC = [
    ("PERSON", "person (agent nouns: X-person)", "2-1"),
    ("THING", "thing (object nouns: X-thing)", "11-18"),
    ("PLACE", "place (where: WHAT-place)", "12-11"),
    ("TIME", "time (when: WHAT-time)", "14-11"),
    ("REASON", "reason (why: WHAT-reason)", "17-42"),
    ("MANNER", "manner (how: WHAT-manner)", "17-49"),
    ("QUALITY", "quality (abstract nouns: X-quality)", None),
    ("ACTION", "action (X-action)", "9-12"),
    ("TOOL", "tool (instrument nouns: X-tool)", "9-422"),
]

# Concepts G1/G2 already cover, so they must not be re-issued from the core
# list.  WHO is excluded for a different reason: 3.2's Q10 builds it by
# compounding (WHAT+PERSON), so it is not a root at all.
CORE_SKIP = {
    "I": "G1 1SG", "THOU": "G1 2SG", "HE OR SHE OR IT": "G1 3SG",
    "WHAT": "G1 WHAT", "ONE": "G2 numeral ONE",
    "WHO": "compound WHAT+PERSON (3.2 Q10)",
}

# ---------------------------------------------------------------------------
# GROUP 3: project vocabulary.  (gloss, international spelling fed to
# translit, Wikipedia article title for the recognition panel or None).
# The spelling column is judgment call 9 and is [recall].
# ---------------------------------------------------------------------------
TECH = [
    ("language", "lingua", "Language"),
    ("word", "lexi", "Word"),
    ("sentence", "frase", "Sentence (linguistics)"),
    ("grammar", "grammatica", "Grammar"),
    ("verb", "verbum", "Verb"),
    ("noun", "nomen", "Noun"),
    ("adjective", "adjectivo", "Adjective"),
    ("adverb", "adverbio", "Adverb"),
    ("syllable", "syllaba", "Syllable"),
    ("consonant", "consonanta", "Consonant"),
    ("vowel", "vocala", "Vowel"),
    ("phoneme", "phonema", "Phoneme"),
    ("morpheme", "morphema", "Morpheme"),
    ("compound", "composito", "Compound (linguistics)"),
    ("root (of a word)", "radika", "Root (linguistics)"),
    ("lexicon", "lexicon", "Lexicon"),
    ("dictionary", "dictionario", "Dictionary"),
    ("translation", "traductione", "Translation"),
    ("meaning", "sensu", None),
    ("sound", "phono", None),
    ("letter", "litera", "Letter (alphabet)"),
    ("number", "numero", "Number"),
    ("question", "questione", "Question"),
    ("example", "exemplo", None),
    ("rule", "regula", None),
    ("system", "systema", "System"),
    ("structure", "structura", "Structure"),
    ("phonology", "phonologia", "Phonology"),
    ("phonetics", "phonetica", "Phonetics"),
    ("syntax", "syntaxis", "Syntax"),
    ("semantics", "semantica", "Semantics"),
    ("typology", "typologia", "Linguistic typology"),
    ("linguistics", "linguistica", "Linguistics"),
    ("dialect", "dialecto", "Dialect"),
    ("alphabet", "alphabeto", "Alphabet"),
    ("text", "texto", "Text (literary theory)"),
    ("corpus", "corpus", "Text corpus"),
    ("data", "data", "Data"),
    ("computer", "computer", "Computer"),
    ("program", "programa", "Computer program"),
    ("model", "modello", "Conceptual model"),
    ("method", "methodo", "Methodology"),
    ("analysis", "analysis", "Analysis"),
    ("statistics", "statistica", "Statistics"),
    ("frequency", "frequentia", "Frequency"),
    ("population", "populatione", "Population"),
    ("family (of languages)", "familia", "Language family"),
    ("project", "projecto", "Project"),
    ("version", "versione", None),
    ("category", "categoria", "Categorization"),
    ("form", "forma", None),
    ("list", "lista", "List"),
    ("table", "tabella", "Table (information)"),
    ("note", "nota", None),
]

# Worked examples printed in full (judgment call: chosen to cover one case of
# each interesting rule - v->f, th->t, ph->f, an illegal s+stop onset, a kept
# Cr cluster, x->ks, final epenthesis, and a G2 monosyllabification).
WORKED = ["vowel", "grammar", "structure", "phoneme", "syntax", "program",
          "computer", "system"]

# ---------------------------------------------------------------------------
# Greek needs a table; international_vocab.py has none (it never met a Greek
# title).  Monotonic Greek only, rough, same spirit as that file's tables.
# ---------------------------------------------------------------------------
GREEK = {
    "α": "a", "β": "v", "γ": "g", "δ": "d", "ε": "e", "ζ": "z", "η": "i",
    "θ": "θ", "ι": "i", "κ": "k", "λ": "l", "μ": "m", "ν": "n", "ξ": "ks",
    "ο": "o", "π": "p", "ρ": "r", "σ": "s", "ς": "s", "τ": "t", "υ": "i",
    "φ": "f", "χ": "x", "ψ": "ps", "ω": "o",
}


# ---------------------------------------------------------------------------
# form machinery
# ---------------------------------------------------------------------------
def strip_marks(s: str) -> str:
    """WOLD transcription -> plain letters (judgment call 4)."""
    s = s.split(",")[0].split("(")[0].split("/")[0].strip().lower()
    s = s.replace("ʔ", "").replace("ʼ", "").replace("'", "").replace("’", "")
    s = s.replace("ː", "").replace("ˀ", "").replace("_", "").replace("-", "")
    s = unicodedata.normalize("NFD", s)
    # Mn = combining marks; Lm/Sk = modifier letters (ʷ ˤ ʰ ˈ), which WOLD uses
    # for secondary articulation and which we have no phoneme for
    s = "".join(c for c in s
                if unicodedata.category(c) not in ("Mn", "Lm", "Sk"))
    # digits are tone marks in WOLD's Mandarin/Hmong transcriptions
    return "".join(c for c in s if c.isalpha())


def syllabify(form: str) -> list[str]:
    """Split a legal interlang word into syllables (onset-maximal)."""
    out, cur = [], ""
    i = 0
    while i < len(form):
        c = form[i]
        cur += c
        if c in VOWELS:
            # a following nasal is a coda only if it is not itself an onset
            if (i + 1 < len(form) and form[i + 1] in "nm"
                    and (i + 2 >= len(form) or form[i + 2] not in VOWELS)):
                cur += form[i + 1]
                i += 1
            out.append(cur)
            cur = ""
        i += 1
    if cur:
        out.append(cur)          # should not happen on a legal form
    return out


def first_syllable(form: str) -> str | None:
    """Judgment call 5: the donor's contribution is its first syllable."""
    syls = syllabify(form)
    if not syls:
        return None
    s = syls[0]
    return s if s and any(c in VOWELS for c in s) else None


def form_cost(form: str, freq_w: float) -> float:
    """Provisional discouragement cost (judgment call 1), x frequency weight."""
    c = sum(SEG_COST.get(ch, 0.0) for ch in form)
    for syl in syllabify(form):
        onset = syl[:len(syl) - len(syl.lstrip("ptkbdgmnfshjwlr"))]
        if len(onset) == 2:
            c += CLUSTER_COST
        elif not onset:
            c += NO_ONSET_COST
    for a, b in zip(form, form[1:]):
        if a in VOWELS and b in VOWELS:
            c += HIATUS_COST
        elif a == b:
            c += GEMINATE_COST
    return c * freq_w


def monosyllable_pool() -> list[str]:
    """The budget (judgment call 3): usable monosyllabic roots for G1/G2."""
    pool = []
    for o in [c for c in "ptkbdgmnfshjwlr" if c not in BANNED_ONSETS]:
        for v in VOWELS:
            for coda in CODAS:
                s = o + v + coda
                if s not in BANNED_SYLLABLES:
                    pool.append(s)
    return pool


def _ovc(syl: str) -> tuple[str, str, str]:
    """A monosyllable as (onset, vowel, coda)."""
    i = 0
    while i < len(syl) and syl[i] not in VOWELS:
        i += 1
    return syl[:i], syl[i:i + 1], syl[i + 1:]


def distinctiveness(syl: str, assigned: dict) -> int:
    """Positions of (onset, vowel, coda) differing from the NEAREST word so far."""
    if not assigned:
        return 3
    a = _ovc(syl)
    return min(sum(x != y for x, y in zip(a, _ovc(o)))
               for o in assigned if len(o) <= 3)


def breaks_minimal_pair_ban(form: str, assigned: set[str]) -> str | None:
    """3.3 FIRM: no two words may differ only by l~r, and none only by h~r."""
    for other in assigned:
        if len(other) != len(form):
            continue
        diffs = [(a, b) for a, b in zip(form, other) if a != b]
        if len(diffs) == 1 and set(diffs[0]) in ({"l", "r"}, {"h", "r"}):
            return other
    return None


# ---------------------------------------------------------------------------
# data
# ---------------------------------------------------------------------------
def fetch_concepticon(name: str, offline: bool) -> pd.DataFrame:
    CONCEPTICON.mkdir(parents=True, exist_ok=True)
    path = CONCEPTICON / f"{name}.tsv"
    if not path.exists():
        if offline:
            raise FileNotFoundError(f"{path} missing and --offline given")
        import requests
        r = requests.get(CONCEPTICON_URL.format(name), timeout=60,
                         headers={"User-Agent": USER_AGENT})
        r.raise_for_status()
        path.write_text(r.text)
        print(f"  fetched {name}")
    return pd.read_csv(path, sep="\t")


def load_wold() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    d = RAW / "wold" / "cldf"
    params = pd.read_csv(d / "parameters.csv")
    forms = pd.read_csv(d / "forms.csv", low_memory=False)
    langs = pd.read_csv(d / "languages.csv")
    return params, forms, langs


def donor_table(forms: pd.DataFrame, langs: pd.DataFrame) -> pd.DataFrame:
    """Judgment call 4: the language's own unanalyzable word, one per language."""
    f = forms[["Language_ID", "Parameter_ID", "Form", "Borrowed_score",
               "Analyzability"]].copy()
    f = f[f["Analyzability"].astype(str) == "unanalyzable"]
    f["Borrowed_score"] = pd.to_numeric(f["Borrowed_score"], errors="coerce").fillna(1.0)
    f = f[f["Borrowed_score"] <= 0.25]
    f = f.sort_values(["Parameter_ID", "Language_ID", "Borrowed_score"])
    f = f.drop_duplicates(["Parameter_ID", "Language_ID"], keep="first")
    key = langs.set_index("ID")
    f["family"] = f["Language_ID"].map(key["Family"]).fillna("(unknown)")
    f["macroarea"] = f["Language_ID"].map(key["Macroarea"]).fillna("(unknown)")
    f["iso"] = f["Language_ID"].map(key["ISO639P3code"]).fillna("")
    return f


def populations() -> tuple[dict, dict, float]:
    l1 = read_l1_speakers(PROC / "l1_speakers.csv")
    by_iso = dict(zip(l1["iso639_3"], l1["l1_speakers"]))
    world_l1 = float(l1["l1_speakers"].sum())
    try:
        tot = cldr_totals(RAW / "cldr_supplementalData.xml", RAW / "iso639")
    except Exception as e:                                   # pragma: no cover
        print(f"  ! CLDR totals unavailable ({e}); using L1 for the ease term")
        tot = {}
    return by_iso, tot, world_l1


# ---------------------------------------------------------------------------
# assignment
# ---------------------------------------------------------------------------
def adapt(raw_form: str) -> str | None:
    """WOLD form -> a legal interlang word under the FIRM template."""
    cleaned = strip_marks(raw_form)
    if not cleaned:
        return None
    try:
        ph, _ = translit.to_phonemes(cleaned)
        if not ph or not any(c in VOWELS for c in ph):
            return None
        form, _ = translit.repair(ph, translit.VARIANTS["V3C"],
                                  epen="labial_u", final_policy="epenthesize")
    except Exception:
        return None
    return form or None


def assign(concepts: list[dict], donors: pd.DataFrame, by_iso: dict,
           tot: dict, taken: dict, family_count: dict,
           hard_distance2: bool = False) -> list[dict]:
    """Greedy form assignment (judgment call 6).

    `hard_distance2` turns judgment call 10's distinctiveness preference into a
    hard constraint inside the closed class and the numerals.  It is OFF by
    default and the reason is measured, not assumed: the constraint is provably
    unsatisfiable (see the Singleton bound printed by main()), so it holds for
    the first ~15 words and then degrades, and paying for it costs four more
    coined - i.e. donor-less, representation-free - grammatical words.  Run
    with --hard-distance2 to reproduce that arm.
    """
    pool = monosyllable_pool()
    pop = {}
    for lid, grp in donors.groupby("Language_ID"):
        iso = str(grp["iso"].iloc[0])
        pop[lid] = float(tot.get(iso, 0.0)) or float(by_iso.get(iso, 0.0))
    max_pop = max(pop.values()) if pop else 1.0
    import math
    ease = {k: math.log1p(v) / math.log1p(max_pop) for k, v in pop.items()}

    rows = []
    for c in concepts:
        fw = FREQ_WEIGHT[c["group"]]
        # Judgment call 10, hard half: inside the closed class and the numerals,
        # no two words may be one feature apart.  19 + 11 words in a 12x5x3
        # space leaves plenty of room for a distance-2 code, and these are the
        # words where a misheard vowel changes the sentence rather than a noun.
        want = 2 if (hard_distance2 and c["group"] in ("grammar", "numeral")) else 1
        chosen = None
        for min_dist in (want, 1):     # graceful fallback: see the bound below
            cands = []
            if c["wold"]:
                sub = donors[donors["Parameter_ID"] == c["wold"]]
                for _, d in sub.iterrows():
                    form = adapt(d["Form"])
                    if not form:
                        continue
                    syl = first_syllable(form)
                    if syl is None or syl in BANNED_SYLLABLES:
                        continue
                    if any(ch in BANNED_ONSETS for ch in syl):
                        continue          # judgment call 2
                    if syl[0] in VOWELS:
                        continue          # judgment call 1 (onsetless ban)
                    if syl in taken:
                        continue
                    if breaks_minimal_pair_ban(syl, set(taken)):
                        continue
                    if distinctiveness(syl, taken) < min_dist:
                        continue
                    score = (W_EASE * ease.get(d["Language_ID"], 0.0)
                             - form_cost(syl, fw)
                             - W_REP * family_count.get(d["family"], 0)
                             - W_DIST * (fw / 3.0)
                             * max(0, 2 - distinctiveness(syl, taken)))
                    cands.append((score, d["Language_ID"], d["family"],
                                  d["macroarea"], d["Form"], form, syl))
            cands.sort(key=lambda x: (-x[0], x[1]))
            if cands:
                score, lid, fam, area, raw, full, syl = cands[0]
                chosen = (score, lid, fam, area, raw, full, syl, "wold", len(cands))
                break
            # Coined: cheapest free syllable; ties broken by DISTINCTIVENESS
            # (how many of onset/vowel/coda differ from the nearest word
            # already assigned), then alphabetically for determinism.  Without
            # the distinctiveness term the coined particles come out as a
            # minimal-pair set, which is the worst possible outcome for the
            # most frequent words in the language.
            free = [s for s in pool if s not in taken
                    and not breaks_minimal_pair_ban(s, set(taken))
                    and distinctiveness(s, taken) >= min_dist]
            free.sort(key=lambda s: (form_cost(s, fw), -distinctiveness(s, taken), s))
            if free:
                syl = free[0]
                chosen = (0.0, "(coined)", "(none)", "(none)", "", syl,
                          syl, "coined", 0)
                break
        score, lid, fam, area, raw, full, syl, src, ncand = chosen
        dist = distinctiveness(syl, taken)
        taken[syl] = c["concept"]
        if fam != "(none)":
            family_count[fam] = family_count.get(fam, 0) + 1
        rows.append({**c, "form": syl, "syllables": 1, "donor": lid,
                     "donor_family": fam, "donor_macroarea": area,
                     "donor_form": raw, "donor_adapted": full,
                     "source": src, "score": round(score, 4),
                     "seg_cost": round(form_cost(syl, 1.0), 3),
                     "seg_cost_weighted": round(form_cost(syl, fw), 3),
                     "nearest_word_distance": dist,
                     "n_donor_candidates": ncand})
    return rows


# ---------------------------------------------------------------------------
# recognition panel  (judgment call 7)
# ---------------------------------------------------------------------------
def fetch_langlinks(title: str, offline: bool) -> dict:
    LANGLINKS.mkdir(parents=True, exist_ok=True)
    path = LANGLINKS / f"{title.replace('/', '_')}.json"
    if path.exists():
        return json.loads(path.read_text())
    if offline:
        return {}
    import requests
    params = {"action": "query", "format": "json", "prop": "langlinks",
              "titles": title, "lllimit": "500", "redirects": "1"}
    r = requests.get(API, params=params, timeout=60,
                     headers={"User-Agent": USER_AGENT})
    r.raise_for_status()
    path.write_text(json.dumps(r.json(), ensure_ascii=False))
    time.sleep(0.3)
    return r.json()


def langlink_titles(blob: dict) -> dict[str, str]:
    out = {}
    for page in blob.get("query", {}).get("pages", {}).values():
        for ll in page.get("langlinks", []):
            out[ll["lang"]] = ll["*"]
    return out


def detect_script(s: str) -> str:
    for ch in s:
        if not ch.isalpha():
            continue
        o = ord(ch)
        if o < 0x0250 or 0x1E00 <= o < 0x2000:
            return "latin"
        if 0x0370 <= o < 0x0400:
            return "greek"
        if 0x0400 <= o < 0x0530:
            return "cyrillic"
        if 0x0590 <= o < 0x0600:
            return "hebrew"
        if 0x0600 <= o < 0x0700 or 0x0750 <= o < 0x0780:
            return "arabic"
        if 0x0900 <= o < 0x0980:
            return "devanagari"
        if 0x0B80 <= o < 0x0C00:
            return "tamil"
        if 0x30A0 <= o < 0x3100:
            return "kana"
        if 0xAC00 <= o < 0xD7A4:
            return "hangul"
        return "other"
    return "other"


def romanise_any(title: str) -> tuple[str, str]:
    """(IPA-ish string, script).  '' means we could not romanise it."""
    t = title.split("(")[0].strip()
    script = detect_script(t)
    try:
        if script == "latin":
            return iv.rom_latin(t, "latin_generic"), script
        if script == "cyrillic":
            return iv.rom_cyrillic(t), script
        if script == "greek":
            return "".join(GREEK.get(c, "" if c.isalpha() else "")
                           for c in unicodedata.normalize("NFD", t.lower())
                           if unicodedata.category(c) != "Mn"), script
        if script == "devanagari":
            return iv.rom_devanagari(t), script
        if script == "tamil":
            return iv.rom_tamil(t), script
        if script == "arabic":
            return iv.rom_abjad(t, iv.ARABIC), script
        if script == "hebrew":
            return iv.rom_abjad(t, iv.HEBREW), script
        if script == "kana":
            return iv.rom_kana(t), script
        if script == "hangul":
            return iv.rom_hangul(t), script
    except Exception:
        return "", script
    return "", script


def wiki_to_iso(iso_tables) -> dict:
    part1, _ = iso_tables
    extra = {"zh": "cmn", "nb": "nob", "nn": "nno", "pt": "por", "arz": "arz",
             "ary": "ary", "yue": "yue", "wuu": "wuu", "nan": "nan",
             "bgn": "bgn", "pnb": "pnb", "azb": "azb", "ckb": "ckb",
             "sh": "hbs", "simple": "eng", "als": "als", "diq": "diq"}
    m = dict(part1)
    m.update(extra)
    return m


def recognition(form: str, titles: dict[str, str], wiki2iso: dict,
                by_iso: dict, world_l1: float) -> dict:
    ours = translit.to_ipa(form)
    hits, hit_pop, strict_pop, panel_pop, n_panel = [], 0.0, 0.0, 0.0, 0
    seen = set()
    for code, title in titles.items():
        iso = wiki2iso.get(code, code if len(code) == 3 else None)
        if not iso or iso in seen:
            continue
        pop = float(by_iso.get(iso, 0.0))
        if pop <= 0:
            continue
        seen.add(iso)
        rom, _script = romanise_any(title)
        n_panel += 1
        panel_pop += pop
        if not rom:
            continue
        try:
            sim = metric.similarity(ours, rom)
        except Exception:
            continue
        if sim >= RECOG_THRESHOLD:
            hits.append((iso, title, round(sim, 3), pop))
            hit_pop += pop
        if sim >= RECOG_THRESHOLD_STRICT:
            strict_pop += pop
    hits.sort(key=lambda x: -x[3])
    return {"recog_share_world_l1": hit_pop / world_l1 if world_l1 else 0.0,
            "recog_share_world_l1_strict": strict_pop / world_l1 if world_l1 else 0.0,
            "recog_share_panel": hit_pop / panel_pop if panel_pop else 0.0,
            "panel_languages": n_panel,
            "panel_share_world_l1": panel_pop / world_l1 if world_l1 else 0.0,
            "n_recognizing": len(hits),
            "top_recognizers": "; ".join(f"{i}:{t}({s})" for i, t, s, _ in hits[:6])}


# ---------------------------------------------------------------------------
def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--offline", action="store_true",
                    help="never hit the network; use cached langlinks/lists only")
    ap.add_argument("--hard-distance2", action="store_true",
                    help="enforce >=2-feature distinctness inside the closed "
                         "class and the numerals (the priced alternative arm)")
    args = ap.parse_args()

    print("=== loading ===")
    params, forms, langs = load_wold()
    donors = donor_table(forms, langs)
    by_iso, tot, world_l1 = populations()
    lj = fetch_concepticon("Tadmor-2009-100", args.offline)
    sw = fetch_concepticon("Swadesh-1955-100", args.offline)
    print(f"  WOLD donors: {len(donors):,} forms, {donors.Language_ID.nunique()} "
          f"languages, {donors.family.nunique()} families")
    print(f"  world L1 denominator: {world_l1/1e9:.2f}bn over "
          f"{len(by_iso):,} languages")

    # ---- concept list ----------------------------------------------------
    concepts: list[dict] = []
    for cid, gloss, w in GRAMMAR:
        concepts.append({"group": "grammar", "concept": cid, "gloss": gloss,
                         "wold": w, "rank": "", "concepticon": ""})
    for cid, gloss, w in NUMERALS:
        concepts.append({"group": "numeral", "concept": cid, "gloss": gloss,
                         "wold": w, "rank": "", "concepticon": ""})
    for cid, gloss, w in GENERIC:
        concepts.append({"group": "generic", "concept": cid, "gloss": gloss,
                         "wold": w, "rank": "", "concepticon": ""})

    top = lj[lj["RANK"] <= 50].sort_values(["RANK", "NUMBER"])
    cid_to_param = (params.dropna(subset=["Concepticon_ID"])
                    .assign(cc=lambda d: d.Concepticon_ID.astype(int))
                    .drop_duplicates("cc").set_index("cc")["ID"].to_dict())
    sw_ids = set(sw["CONCEPTICON_ID"])
    skipped = []
    for _, r in top.iterrows():
        g = r["CONCEPTICON_GLOSS"]
        if g in CORE_SKIP:
            skipped.append((g, CORE_SKIP[g]))
            continue
        concepts.append({"group": "core", "concept": g,
                         "gloss": str(r["ENGLISH"]),
                         "wold": cid_to_param.get(int(r["CONCEPTICON_ID"])),
                         "rank": int(r["RANK"]),
                         "concepticon": int(r["CONCEPTICON_ID"]),
                         "in_swadesh_1955": int(r["CONCEPTICON_ID"]) in sw_ids})
    print(f"  Leipzig-Jakarta top-50: {len(top)} concepts, "
          f"{len(skipped)} already covered by G1/G2 -> {len(top)-len(skipped)} core roots")
    for g, why in skipped:
        print(f"      overlap: {g:18s} -> {why}")

    # ---- assign monosyllables -------------------------------------------
    print("\n=== assigning monosyllabic roots (G1 + G2) ===")
    taken: dict[str, str] = {}
    family_count: dict[str, int] = {}
    rows = assign(concepts, donors, by_iso, tot, taken, family_count,
                  hard_distance2=args.hard_distance2)
    pool = monosyllable_pool()
    print(f"  monosyllable budget: {len(pool)} usable (policy in docstring); "
          f"{len(taken)} assigned; {len(pool)-len(taken)} free "
          f"({100*(len(pool)-len(taken))/len(pool):.0f}% left unassigned)")
    # The distance-2 result.  A monosyllable is a 3-symbol word over alphabets
    # of size (onsets, vowels, codas); the Singleton bound caps a code with
    # minimum Hamming distance 2 at product/max(alphabet).
    n_ons, n_vow, n_cod = 12, 5, 3
    bound = n_ons * n_vow * n_cod // max(n_ons, n_vow, n_cod)
    near = sum(1 for r in rows if r["nearest_word_distance"] < 2)
    print(f"  arm: {'HARD distance-2 in G1+numerals' if args.hard_distance2 else 'soft distinctiveness only (default)'}")
    print(f"  distance-2 bound: at most {bound} monosyllables of this shape can "
          f"be pairwise >=2 features apart (Singleton bound on "
          f"{n_ons}x{n_vow}x{n_cod}); the closed class alone needs 19, so "
          f"{near} of {len(rows)} roots sit one feature from another word")

    # ---- G2 recognition against the WOLD panel ---------------------------
    # A separate, much smaller instrument than G3's langlinks panel: for a core
    # concept there is no international word to look up, so the question is
    # whether our root happens to resemble the 41 WOLD languages' own words.
    wold_pop = {}
    for lid, grp in donors.groupby("Language_ID"):
        wold_pop[lid] = float(by_iso.get(str(grp["iso"].iloc[0]), 0.0))
    wold_panel_pop = sum(wold_pop.values())
    for r in rows:
        r["recog_instrument"] = "wold41"
        if not r["wold"]:
            r.update(recog_share_world_l1=0.0, recog_share_world_l1_strict=0.0,
                     recog_share_panel=0.0, panel_languages=0,
                     n_recognizing=0, top_recognizers="")
            continue
        sub = donors[donors["Parameter_ID"] == r["wold"]]
        hit = strict = 0.0
        n = 0
        names = []
        for _, d in sub.iterrows():
            other = adapt(d["Form"])
            if not other:
                continue
            n += 1
            sim = metric.similarity(translit.to_ipa(r["form"]),
                                    translit.to_ipa(other))
            if sim >= RECOG_THRESHOLD:
                hit += wold_pop.get(d["Language_ID"], 0.0)
                names.append(d["Language_ID"])
            if sim >= RECOG_THRESHOLD_STRICT:
                strict += wold_pop.get(d["Language_ID"], 0.0)
        r.update(recog_share_world_l1=hit / world_l1,
                 recog_share_world_l1_strict=strict / world_l1,
                 recog_share_panel=hit / wold_panel_pop if wold_panel_pop else 0.0,
                 panel_languages=n, n_recognizing=len(names),
                 top_recognizers="; ".join(names[:6]))

    # ---- G3: international borrowings ------------------------------------
    print("\n=== rendering international borrowings (G3) ===")
    iso_tables = None
    try:
        from interlang.populations import _iso_tables
        iso_tables = _iso_tables(RAW / "iso639")
    except Exception as e:                                   # pragma: no cover
        print(f"  ! no ISO table ({e}); recognition panel disabled")
    wiki2iso = wiki_to_iso(iso_tables) if iso_tables else {}

    tech_rows = []
    for gloss, intl, title in TECH:
        res = translit.render(intl, "V3C", epen="labial_u",
                              final_policy="epenthesize")
        form = res["form"]
        row = {"group": "technical", "concept": gloss.upper(), "gloss": gloss,
               "wold": None, "rank": "", "concepticon": "",
               "form": form, "syllables": res["syl_after"],
               "donor": "international (Latin/Greek)", "donor_family": "Indo-European",
               "donor_macroarea": "Eurasia", "donor_form": intl,
               "donor_adapted": form, "source": "translit", "score": "",
               "seg_cost": round(form_cost(form, 1.0), 3),
               "seg_cost_weighted": 0.0, "n_donor_candidates": 1,
               "recog_instrument": "wikipedia_langlinks",
               "wiki_title": title or ""}
        if title and wiki2iso:
            blob = fetch_langlinks(title, args.offline)
            titles = langlink_titles(blob)
            row.update(recognition(form, titles, wiki2iso, by_iso, world_l1))
        else:
            row.update(recog_share_world_l1=float("nan"),
                       recog_share_world_l1_strict=float("nan"),
                       recog_share_panel=float("nan"),
                       panel_languages=0, panel_share_world_l1=float("nan"),
                       n_recognizing=0, top_recognizers="")
        tech_rows.append(row)
        print(f"  {gloss:22s} {intl:14s} -> {form:16s} "
              f"{res['syl_after']}syl  recog={row['recog_share_world_l1']:.3f}"
              if row["recog_share_world_l1"] == row["recog_share_world_l1"]
              else f"  {gloss:22s} {intl:14s} -> {form:16s} {res['syl_after']}syl  recog=n/a")

    # ---- thresholds ------------------------------------------------------
    for r in tech_rows:
        s = r["recog_share_world_l1"]
        r["threshold"] = ("MUST (>50%)" if s == s and s > MUST_SHARE else
                          "SHOULD (>30%)" if s == s and s > SHOULD_SHARE else
                          "" if s != s else "below 30%")
    for r in rows:
        r["threshold"] = ""
        r["wiki_title"] = ""
        r["panel_share_world_l1"] = wold_panel_pop / world_l1

    # ---- integrity checks ------------------------------------------------
    all_rows = rows + tech_rows
    print("\n=== integrity checks ===")
    forms_all = [r["form"] for r in all_rows]
    dupes = {f for f in forms_all if forms_all.count(f) > 1}
    print(f"  homophones: {sorted(dupes) if dupes else 'none'}")
    bans = []
    for i, a in enumerate(forms_all):
        for b in forms_all[i + 1:]:
            if len(a) != len(b):
                continue
            diffs = [(x, y) for x, y in zip(a, b) if x != y]
            if len(diffs) == 1 and set(diffs[0]) in ({"l", "r"}, {"h", "r"}):
                bans.append((a, b))
    print(f"  l~r / h~r minimal pairs: {bans if bans else 'none'}")
    illegal = [r["form"] for r in all_rows
               if not translit.is_legal(r["form"], translit.VARIANTS["V3C"])]
    print(f"  illegal forms: {illegal if illegal else 'none'}")

    # ---- worked examples -------------------------------------------------
    print("\n=== worked examples (source -> form, every rule that fired) ===")
    for gloss, intl, _t in TECH:
        if gloss not in WORKED:
            continue
        res = translit.render(intl, "V3C", epen="labial_u",
                              final_policy="epenthesize")
        print(f"\n  {gloss}: {intl}")
        print(f"    stage 1 phonemes: {res['phonemes']}")
        for t in res["trace"]:
            print(f"      {t}")
        print(f"    -> {res['form']}  ({res['syl_after']} syllables, "
              f"stress on '{syllabify(res['form'])[0]}')")
    ex = next(r for r in rows if r["concept"] == "FIRE")
    print(f"\n  FIRE (G2 core, rank 1): donor {ex['donor']} '{ex['donor_form']}' "
          f"-> adapted '{ex['donor_adapted']}' -> first syllable '{ex['form']}' "
          f"({ex['n_donor_candidates']} donor candidates competed)")

    # ---- summaries -------------------------------------------------------
    df = pd.DataFrame(all_rows)
    PROC.mkdir(parents=True, exist_ok=True)
    cols = ["group", "concept", "gloss", "form", "syllables", "donor",
            "donor_family", "donor_macroarea", "donor_form", "donor_adapted",
            "source", "seg_cost", "seg_cost_weighted", "score",
            "nearest_word_distance",
            "n_donor_candidates", "recog_instrument", "wiki_title",
            "panel_languages", "panel_share_world_l1", "n_recognizing",
            "recog_share_world_l1", "recog_share_world_l1_strict",
            "recog_share_panel", "threshold",
            "top_recognizers", "rank", "concepticon", "wold"]
    df = df.reindex(columns=[c for c in cols if c in df.columns])
    df.to_csv(OUT_CSV, index=False)

    print("\n=== counts ===")
    print(df.groupby("group").agg(n=("form", "size"),
                                  syl=("syllables", "mean")).round(2).to_string())
    print("\n=== donor family breakdown (G1+G2 roots) ===")
    fam = (df[df.group != "technical"].groupby("donor_family")
           .agg(n=("form", "size")).sort_values("n", ascending=False))
    fam["pct"] = (100 * fam.n / fam.n.sum()).round(1)
    print(fam.to_string())
    print("\n=== donor macroarea breakdown (G1+G2 roots) ===")
    area = (df[df.group != "technical"].groupby("donor_macroarea")
            .agg(n=("form", "size")).sort_values("n", ascending=False))
    area["pct"] = (100 * area.n / area.n.sum()).round(1)
    print(area.to_string())
    print("\n=== recognition thresholds (G3) ===")
    t = df[df.group == "technical"]
    print(t["threshold"].value_counts().to_string())
    print("\n  top 15 by recognition share of world L1 "
          f"(sim>={RECOG_THRESHOLD} | strict sim>={RECOG_THRESHOLD_STRICT} | "
          "share of the panel | panel coverage):")
    for _, r in t.sort_values("recog_share_world_l1", ascending=False).head(15).iterrows():
        print(f"    {r.gloss:22s} {r.form:14s} {r.recog_share_world_l1:.3f} | "
              f"{r.recog_share_world_l1_strict:.3f} | {r.recog_share_panel:.3f} | "
              f"{r.panel_share_world_l1:.3f}   {r.threshold}")
    n_panel50 = int((t.recog_share_panel > MUST_SHARE).sum())
    print(f"\n  words clearing >50% of world L1 outright: "
          f"{int((t.recog_share_world_l1 > MUST_SHARE).sum())}")
    print(f"  words clearing >50% OF THE PANEL (i.e. would clear it if the "
          f"languages the panel misses behaved like those it covers): {n_panel50}")
    print(f"\n  G2 core roots: max recognition share (WOLD-41 instrument) = "
          f"{df[df.group=='core'].recog_share_world_l1.max():.4f} - "
          f"nothing in basic vocabulary comes close to either threshold, which "
          f"is why G2 is free to optimise for representation instead.")
    print(f"\nwrote {OUT_CSV}")


if __name__ == "__main__":
    main()
