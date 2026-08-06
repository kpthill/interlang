"""Lexicon milestone 1: a small, sanity-checkable word list (~140 words).

The first thing in the project that produces actual interlang WORDS.  It is a
sanity check on the machinery, not the lexicon: everything here is meant to be
read, argued with and re-run, and every number it prints is reproducible from
data on disk plus one Wikipedia API endpoint.

Three word groups (notes/lexicon-milestone1.md interprets the output):

  G1 GRAMMAR    the complete closed class of principles.md 3.2 + 3.2's gap
                closure - 20 words, all monosyllabic.
  G2 CORE       the top 50 concepts of the ranked Leipzig-Jakarta list
                (Concepticon `Tadmor-2009-100`), minus the ones G1 already
                covers, plus the numerals 0-10 and the nine generic nouns the
                grammar leans on (person/thing/place/time/reason/manner/
                quality/action/tool).  All monosyllabic.
  G3 TECHNICAL  ~50 words for talking about the project itself.  These are
                international borrowings, rendered by src/interlang/translit.py,
                and they are POLYSYLLABIC BY CONSTRUCTION - which is the point:
                they cost nothing from the monosyllable budget.  A borrowing
                that the phonotactic repair has DAMAGED, and that buys no
                measured recognition in exchange, falls back to a compound of
                native roots (judgment call 12).

Inputs
------
  data/raw/wold/cldf/{parameters,forms,languages}.csv   donor word forms, and
      the false-friend reference set (Semantic_category == "Function word")
  data/raw/concepticon/Tadmor-2009-100.tsv              the ranked core list
  data/raw/concepticon/Swadesh-1955-100.tsv             cross-check only
      (both fetched by this script on first run; --offline reuses the cache)
  data/processed/l1_speakers.csv                        L1 populations
  data/raw/cldr_supplementalData.xml + data/raw/iso639/ total-speaker weights
  data/raw/wals/cldf/*                                  WALS 12A, for the
      rejected sC-onset option (judgment call 13)
  data/raw/wikipedia_langlinks/*.json                   recognition panel
      (fetched on first run, same cache as scripts/international_vocab.py)

Output
------
  data/processed/lexicon_milestone1.csv   one row per word, with the form,
      syllable count, donor language + family, the segment cost it paid, the
      false-friend and separation terms it paid, and the recognition estimate
      with the threshold it met.

Usage: uv run python scripts/lexicon_milestone1.py [--offline] [--hard-distance2]
  --offline         never hit the network; use the cached lists and langlinks
  --hard-distance2  the priced alternative arm of judgment call 10 (see below)

READING THE OUTPUT CSV - `nan` IS A REAL WORD.  The 2PL pronoun is the string
`nan`, which `pandas.read_csv` silently turns into a float NaN under its default
NA handling: the word disappears on read and the `form` column stops being a
string column.  EVERY read in this script goes through `read_csv()` below, which
sets `keep_default_na=False, na_values=[""]`, and main() asserts on the written
file that every form reads back as a str.  `interlang.populations.
read_l1_speakers` documents the identical trap for ISO 639-3 `nan` (Min Nan).
Any future reader of `data/processed/lexicon_milestone1.csv` needs the same
kwargs.  `nan` is deliberately kept in the legal monosyllable pool.

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
   computed under a stated policy.  `nan` is in the pool and stays there.

4. DONOR FORMS COME FROM WOLD (41 languages, 24 families, 6 macroareas),
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

       score = W_EASE * ease(donor)          # objective 1
             - cost(form)                    # 3.3/3.6 discouragement x freq
             - W_REP  * n_roots_from_family  # objective 2
             - separation penalty            # judgment call 10
             - W_FF   * false-friend score   # judgment call 11

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

   KNOWN FAILURE MODE, and it bites judgment call 12: the instrument compares
   whole ARTICLE TITLES.  Where the article title is a longer derivative of the
   international word (`Methodology` vs *methodo*, `Computer program` vs
   *programa*, `Conceptual model` vs *modello*), the score collapses to near
   zero for reasons that have nothing to do with recognizability.  This is why
   call 12 cannot be a bare recognition threshold.

8. FINAL-CODA POLICY: this script uses `final_policy="epenthesize"`.
   principles.md 3.6 is FIRM that an illegal word-final consonant takes a
   support vowel (*bank* -> *banki*, *virus* -> *firusi*).  translit.py's
   default USED to be `"delete"` and was fixed to `"epenthesize"` on
   2026-08-06; this script always passed the argument explicitly, so the fix
   changes nothing here (main() asserts that the default now matches).

10. SEPARATION IS PERCEPTUAL, NOT A HAMMING CODE (revised 2026-08-06, Patrick).
   The earlier arm treated a monosyllable as a 3-symbol codeword (onset, vowel,
   coda) and penalised distance-1 neighbours.  That is the wrong instrument:
   a Singleton bound caps a distance-2 code at 15 words and the closed class
   needs 20, and adding consonants provably does not help (see main()'s
   printout).  The rule now is: MAXIMISE PERCEPTUAL SEPARATION using the
   feature-distance metric of src/interlang/metric.py.  A candidate pays

       W_SEP * (freq/3) * max(0, (s - SEP_FLOOR) / (1 - SEP_FLOOR))

   where `s` is its highest metric-v0 similarity to any monosyllable already
   assigned, W_SEP = 0.90 and SEP_FLOOR = 0.70.  This generalises 3.3's two
   FIRM minimal-pair bans (l~r, h~r) from "these two segments" to "any pair the
   metric says is too close", and it disagrees with the Hamming rule in both
   directions, which is the point: `di`~`ti` (voicing only, s=0.983) is now
   expensive while `na`~`nan` (a whole extra segment, s=0.667) is free, and
   `mi`~`ti` (s=0.733) never was a problem.

11. FALSE FRIENDS ARE PRICED, WEAKLY (new 2026-08-06, Patrick).  Review of the
   first run found five forms that read as a DIFFERENT high-frequency word in a
   big language - `mi` "drink" vs Spanish *mi*, `bu` "this" vs Mandarin *bù*
   "not", `si` "they" vs Spanish *sí* "yes", `da` "hit" vs Russian *da* "yes",
   `je` "3sg" vs French *je* "I" - three of them pointing at a concept WE ALSO
   HAVE, which is the worst case.  A candidate therefore pays

       W_FF * sum over colliding languages of  L1share(lang) * mult

   with W_FF = 0.50 and mult = 3.0 when the colliding meaning is itself a
   concept in our word list, else 1.0.  Only the strongest collision per
   language counts.  A collision is: our form equals the reference word's
   written form, OR metric v0 similarity >= 0.90 (near-homophony).  Meanings
   identical to our own concept do not count - that is a donor, not a friend.

   IT IS DELIBERATELY THE WEAKEST TERM IN THE SCORE ("some of this is
   inevitable" - Patrick).  Its largest attainable value is ~0.40 (a Mandarin-
   sized language colliding with a concept we have), against ease in [0,1],
   W_REP 0.35 per family root already spent, and segment costs up to ~3.  It
   breaks ties and steers away from the worst collisions; it does not drive the
   assignment.  The three-arm before/after is printed by main().

   THE REFERENCE SET IS TWO-PART, AND THE HALVES HAVE DIFFERENT PROVENANCE:
     (a) [measured] every WOLD form whose parameter has
         Semantic_category == "Function word" (122 parameters, 4,522 forms).
         WOLD's own categorisation, not a hand pick: function words are where
         the false-friend effect lives, because they are what a listener cannot
         help hearing.  Content-word collisions (`ki` "person" also being
         Japanese *ki* "wood") are inevitable and are deliberately NOT priced.
     (b) [recall] HAND_FUNCTION_WORDS below - high-frequency function words in
         17 large languages WOLD does not contain (Spanish, Hindi, Bengali,
         Portuguese, Russian, Panjabi, Marathi, Turkish, Korean, French,
         German, Italian, Persian, Javanese, Filipino, Polish, Ukrainian,
         Arabic).  NO SOURCE WAS CHECKED for any of these forms.  Without them
         the term is blind to four of the five collisions the review found,
         because WOLD contains no Spanish, French or Russian.  Arabic is
         weighted by Egyptian Arabic's L1 (64.6M) because MSA has no L1 count
         in l1_speakers.csv, which understates it.  Replace this table with a
         measured source (IDS, or Wiktionary translation tables) before the
         term is trusted for anything but tie-breaking.

12. G3 FALLBACK TO A NATIVE COMPOUND (new 2026-08-06, Patrick).
   lexicon-plan.md 2 already says a concept gets a compound when no recognisable
   international form exists; milestone 1 did not apply it to G3 and produced
   `kiwesitione`, `sitatisitika`, `dikitionario`, `adijekitifo`.  THE RULE IS
   NOT "compound the technical vocabulary" - a technical community that already
   uses the Latin term must be able to pick this language up with almost no
   learning, so `gramatika`, `fonema`, `silaba`, `data`, `metodo`, `nota` stay.
   The rule is:

     TRANSLITERATE BY DEFAULT.  A borrowing falls back to a compound only when
       (a) the repair DAMAGED it - it gained >= 2 epenthetic syllables, or the
           repaired form is >= 6 syllables; AND
       (b) it fails both recognition escapes - recognition <= 30% of world L1
           (Patrick's SHOULD threshold) and <= 50% of the measured panel
           (i.e. it would not clear MUST even if the panel generalised); AND
       (c) a compound of existing roots passes lexicon-plan.md 2.4's two-way
           inferability test, written out in COMPOUNDS below.

   (a) is the "only buying length" test and it is measured on the repair, not
   on the recognition number, because 7's failure mode makes a bare recognition
   threshold impossible: `metodo` (0.021) and `programa` (0.031) - which
   Patrick requires be kept - score BELOW `kiwesitione` (0.065), which he
   requires be dropped.  No threshold on that column can separate the two
   lists.  Syllable damage can, and does, exactly.

   (c) is a veto, not a criterion, and it follows lexicon-plan.md 2.2's stated
   asymmetry: a misleading compound is worse than a long root, so where no
   compound passes the reverse test the borrowing is KEPT and flagged.  Five of
   the nine words selected by (a)+(b) are kept for this reason.

13. sC ONSETS WERE MEASURED AND REJECTED (2026-08-06).  Adding {sp st sk sm sn
   sl} to the licensed onsets is the obvious repair for the s+stop damage of
   7.4.  main() runs the arm: it improves 6 of the 26 inflated G3 words and
   saves 7 of 215 syllables (3.3%; 6.2% of the affected words' syllables),
   because the real damage is WORD-INTERNAL - /kt/ in *dictionario*,
   *adjectivo*, *traductione*, /ks/ from <x> in *syntaxis* - and no onset rule
   can touch it.  Against that, WALS 12A puts simple or moderately complex
   syllable structure at 57.4% of the L1 it codes (59.0% of world L1), so an
   /st/ onset is genuinely hard for a majority of humanity.  NOT ADOPTED.
   Recorded here so it is not re-proposed.

14. WHICH INTERNATIONAL SPELLING a G3 word starts from is the one decision
   principles.md 7 says is lexical rather than rule-resolvable.  It is a hand
   choice per word, listed in TECH below, and it is [recall]: no source was
   checked for "the international form of X".  The recognition estimate then
   MEASURES whether the choice was any good.  ALT_SPELLINGS prices a handful of
   alternatives that the write-up recommends but this run does NOT adopt.
"""

from __future__ import annotations

import argparse
import json
import math
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


def read_csv(path, **kw) -> pd.DataFrame:
    """The ONLY csv reader in this script.  See the module docstring on `nan`.

    `keep_default_na=False, na_values=[""]` keeps the strings "nan", "NA",
    "null" and "None" as strings.  Every numeric column downstream is coerced
    explicitly with pd.to_numeric, because this reader will hand back "" rather
    than NaN for an empty numeric cell.
    """
    kw.setdefault("keep_default_na", False)
    kw.setdefault("na_values", [""])
    return pd.read_csv(path, **kw)


# ---------------------------------------------------------------------------
# POLICY CONSTANTS  (judgment calls 1-3, 6, 7, 10-13)
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
W_SEP = 0.90                        # perceptual separation (judgment call 10)
SEP_FLOOR = 0.85                    # similarity below which separation is free
W_DIST_HAMMING = 0.90               # the RETIRED code-distance term, kept only
                                    # so main() can print the before/after arm
W_FF = 0.30                         # false friends (judgment call 11)
FF_SIM = 1.00                       # "phonetically very close" = IDENTICAL.
                                    # Near-neighbours (di~ti at 0.983) are
                                    # deliberately NOT counted: all five
                                    # collisions the review found are exact,
                                    # and a looser gate makes the term the
                                    # strongest in the score instead of the
                                    # weakest (measured: at 0.90 it rewrote 72
                                    # of 84 roots).
FF_OWN_MULT = 3.0                   # colliding meaning is a concept we have

RECOG_THRESHOLD = 0.60              # headline arm: similarity = "recognized"
RECOG_THRESHOLD_STRICT = 0.70       # strict arm, reported as a band
MUST_SHARE, SHOULD_SHARE = 0.50, 0.30

# judgment call 12
G3_MIN_INFLATION = 2                # epenthetic syllables that count as damage
G3_MAX_SYLLABLES = 6                # a repaired form this long is damage too
G3_KEEP_WORLD = SHOULD_SHARE        # recognition escape, world L1
G3_KEEP_PANEL = MUST_SHARE          # recognition escape, share of the panel

VOWELS = "aeiou"
CODAS = ["", "n", "m"]
ALL_ONSETS = [""] + list("ptkbdgmnfshjwlr")

# ---------------------------------------------------------------------------
# GROUP 1: the closed class (principles.md 3.2 as amended by 3.2's gap closure
# - 20 words, not 19: grammar-gap-closure.md 1 added a second demonstrative).
# `wold` is the WOLD parameter ID whose forms are used as donor candidates;
# None = no WOLD concept exists, so the word is coined from the free pool.
#
# NOTE ON THE DEMONSTRATIVES.  The grammar bill counts 20 words including ONE
# demonstrative (the distal `that`); the proximal `this` was always assumed to
# be an ordinary lexical item and it arrives here through the Leipzig-Jakarta
# core list at rank 38.  So G1 below issues `that` and G2 issues `this`.  That
# split is an artefact of how the word bill was kept, not a design statement -
# flagged in the write-up as a thing Patrick may want to tidy.
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
    ("THAT", "that (distal demonstrative; `this` is the G2 core root)", "24-08"),
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
# The spelling column is judgment call 14 and is [recall].
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

# Judgment call 12(c).  A G3 concept that (a) and (b) select falls back to a
# compound ONLY if it appears here.  Each element is ("G12", concept-id) for a
# native monosyllabic root or ("G3", gloss) for an already-established
# borrowing; the forms are resolved after assignment, so the table survives a
# change of donor.  `note` is the two-way inferability test of
# lexicon-plan.md 2.4: forward = meaning -> parts, reverse = parts -> meaning.
COMPOUNDS = {
    "question": ([("G12", "WHAT"), ("G12", "THING")], "what-thing",
                 "forward: a question IS a what-thing; reverse: what-thing "
                 "reads as 'a matter asked about'.  Both directions hold."),
    "adjective": ([("G12", "QUALITY"), ("G3", "word")], "quality-word",
                  "the generic-noun derivation pattern of 3.2 Tiers 4-5, "
                  "applied to a word class.  Reverse: quality-word -> a word "
                  "that names a quality."),
    "adverb": ([("G12", "MANNER"), ("G3", "word")], "manner-word",
               "same pattern, same reverse test, and it makes the two word "
               "classes a visible pair."),
    "syntax": ([("G3", "sentence"), ("G12", "MANNER")], "sentence-manner",
               "forward: syntax is the manner of sentences; reverse: "
               "sentence-manner -> how sentences are put together.  Built on "
               "`frase` rather than `word` so it does not become an anagram "
               "of the adverb compound."),
}

# Judgment call 14, priced but NOT adopted.  Alternative international
# spellings for the words the fallback rule flags: the point is that for three
# of them a different source spelling beats both the current borrowing and any
# compound, which is a cheaper fix than either.  Reported by main().
ALT_SPELLINGS = {
    "dictionary": ["dizionario"],
    "translation": ["traduzione"],
    "adjective": ["adjetivo"],
    "adverb": ["adverbo"],
    "syntax": ["sintaxe"],
    "structure": ["struktura"],
    "linguistics": ["lingwistika"],
    "corpus": ["korpus"],
    "question": ["chestione"],
    "statistics": ["estatistica"],
}

# ---------------------------------------------------------------------------
# Judgment call 11(b).  [recall] - NO SOURCE CHECKED.  High-frequency function
# words in large languages WOLD does not contain.  Columns:
#   (iso639-3, as commonly written in Latin script, interlang approximation,
#    English gloss, the concept-id in OUR list it collides with or "")
# The written column matters on its own: a written interlang word is read by a
# French speaker with French letter values, so `je` collides with *je*
# orthographically whatever it sounds like.
# ---------------------------------------------------------------------------
HAND_FUNCTION_WORDS = [
    # Spanish
    ("spa", "yo", "jo", "I", "1SG"), ("spa", "tu", "tu", "you", "2SG"),
    ("spa", "mi", "mi", "my/me", "1SG"), ("spa", "me", "me", "me", "1SG"),
    ("spa", "te", "te", "you (obj)", "2SG"), ("spa", "se", "se", "reflexive", "SELF"),
    ("spa", "si", "si", "yes", "YES"), ("spa", "no", "no", "no/not", "NO"),
    ("spa", "y", "i", "and", "AND"), ("spa", "o", "o", "or", "OR"),
    ("spa", "de", "de", "of", ""), ("spa", "en", "en", "in", ""),
    ("spa", "que", "ke", "that (rel)", "REL"), ("spa", "un", "un", "one", "ONE"),
    ("spa", "dos", "dos", "two", "TWO"), ("spa", "es", "es", "is", "COP"),
    ("spa", "la", "la", "the", ""), ("spa", "lo", "lo", "the", ""),
    ("spa", "con", "kon", "with", ""), ("spa", "mas", "mas", "more", "THAN"),
    ("spa", "nos", "nos", "us", "1PL"), ("spa", "ya", "ja", "already", ""),
    # Portuguese
    ("por", "eu", "eu", "I", "1SG"), ("por", "tu", "tu", "you", "2SG"),
    ("por", "me", "me", "me", "1SG"), ("por", "te", "te", "you (obj)", "2SG"),
    ("por", "se", "se", "reflexive", "SELF"), ("por", "sim", "sim", "yes", "YES"),
    ("por", "nao", "naun", "no/not", "NO"), ("por", "e", "e", "and", "AND"),
    ("por", "ou", "ou", "or", "OR"), ("por", "de", "de", "of", ""),
    ("por", "em", "em", "in", ""), ("por", "que", "ke", "that (rel)", "REL"),
    ("por", "um", "um", "one", "ONE"), ("por", "com", "kom", "with", ""),
    ("por", "nos", "nos", "we/us", "1PL"), ("por", "mas", "mas", "but", ""),
    # Italian
    ("ita", "io", "io", "I", "1SG"), ("ita", "tu", "tu", "you", "2SG"),
    ("ita", "mi", "mi", "me", "1SG"), ("ita", "ti", "ti", "you (obj)", "2SG"),
    ("ita", "si", "si", "reflexive/yes", "SELF"), ("ita", "no", "no", "no", "NO"),
    ("ita", "non", "non", "not", "NEG"), ("ita", "e", "e", "and", "AND"),
    ("ita", "o", "o", "or", "OR"), ("ita", "di", "di", "of", ""),
    ("ita", "in", "in", "in", ""), ("ita", "che", "ke", "that (rel)", "REL"),
    ("ita", "un", "un", "one", "ONE"), ("ita", "due", "due", "two", "TWO"),
    ("ita", "il", "il", "the", ""), ("ita", "la", "la", "the", ""),
    ("ita", "con", "kon", "with", ""), ("ita", "ma", "ma", "but", ""),
    ("ita", "se", "se", "if", "IF"), ("ita", "da", "da", "from", ""),
    # French
    ("fra", "je", "je", "I", "1SG"), ("fra", "tu", "tu", "you", "2SG"),
    ("fra", "il", "il", "he", "3SG"), ("fra", "me", "me", "me", "1SG"),
    ("fra", "te", "te", "you (obj)", "2SG"), ("fra", "se", "se", "reflexive", "SELF"),
    ("fra", "si", "si", "if/yes", "IF"), ("fra", "non", "non", "no", "NO"),
    ("fra", "et", "e", "and", "AND"), ("fra", "ou", "u", "or", "OR"),
    ("fra", "de", "de", "of", ""), ("fra", "en", "an", "in", ""),
    ("fra", "que", "ke", "that (rel)", "REL"), ("fra", "un", "un", "one", "ONE"),
    ("fra", "le", "le", "the", ""), ("fra", "la", "la", "the", ""),
    ("fra", "ne", "ne", "not", "NEG"), ("fra", "on", "on", "one/we", "1PL"),
    ("fra", "ce", "se", "this", "THIS"), ("fra", "oui", "wi", "yes", "YES"),
    ("fra", "pas", "pa", "not", "NEG"), ("fra", "moi", "mwa", "me", "1SG"),
    # German
    ("deu", "ich", "ik", "I", "1SG"), ("deu", "du", "du", "you", "2SG"),
    ("deu", "er", "er", "he", "3SG"), ("deu", "mir", "mir", "me", "1SG"),
    ("deu", "ja", "ja", "yes", "YES"), ("deu", "nein", "nain", "no", "NO"),
    ("deu", "und", "unt", "and", "AND"), ("deu", "oder", "oder", "or", "OR"),
    ("deu", "von", "fon", "from", ""), ("deu", "zu", "tsu", "to", ""),
    ("deu", "in", "in", "in", ""), ("deu", "das", "das", "the/that", "THAT"),
    ("deu", "der", "der", "the", ""), ("deu", "die", "di", "the", ""),
    ("deu", "ein", "ain", "one", "ONE"), ("deu", "zwei", "tswai", "two", "TWO"),
    ("deu", "nicht", "nikt", "not", "NEG"), ("deu", "mit", "mit", "with", ""),
    ("deu", "wir", "wir", "we", "1PL"), ("deu", "sie", "si", "she/they", "3PL"),
    ("deu", "es", "es", "it", "3SG"), ("deu", "was", "was", "what", "WHAT"),
    ("deu", "wer", "wer", "who", ""), ("deu", "so", "so", "so", "MANNER"),
    # Russian
    ("rus", "ja", "ja", "I", "1SG"), ("rus", "ty", "ti", "you", "2SG"),
    ("rus", "on", "on", "he", "3SG"), ("rus", "my", "mi", "we", "1PL"),
    ("rus", "vy", "wi", "you (pl)", "2PL"), ("rus", "oni", "oni", "they", "3PL"),
    ("rus", "da", "da", "yes", "YES"), ("rus", "net", "net", "no", "NO"),
    ("rus", "i", "i", "and", "AND"), ("rus", "ili", "ili", "or", "OR"),
    ("rus", "v", "w", "in", ""), ("rus", "na", "na", "on", ""),
    ("rus", "ne", "ne", "not", "NEG"), ("rus", "to", "to", "that", "THAT"),
    ("rus", "eto", "eto", "this", "THIS"), ("rus", "kto", "kito", "who", ""),
    ("rus", "chto", "sito", "what", "WHAT"), ("rus", "s", "s", "with", ""),
    ("rus", "tak", "tak", "so", "MANNER"), ("rus", "kak", "kak", "how", "MANNER"),
    # Polish
    ("pol", "ja", "ja", "I", "1SG"), ("pol", "ty", "ti", "you", "2SG"),
    ("pol", "on", "on", "he", "3SG"), ("pol", "my", "mi", "we", "1PL"),
    ("pol", "wy", "wi", "you (pl)", "2PL"), ("pol", "oni", "oni", "they", "3PL"),
    ("pol", "tak", "tak", "yes", "YES"), ("pol", "nie", "ne", "no/not", "NO"),
    ("pol", "i", "i", "and", "AND"), ("pol", "lub", "lub", "or", "OR"),
    ("pol", "w", "w", "in", ""), ("pol", "na", "na", "on", ""),
    ("pol", "do", "do", "to", ""), ("pol", "to", "to", "this", "THIS"),
    ("pol", "co", "tso", "what", "WHAT"), ("pol", "kto", "kito", "who", ""),
    # Ukrainian
    ("ukr", "ja", "ja", "I", "1SG"), ("ukr", "ty", "ti", "you", "2SG"),
    ("ukr", "my", "mi", "we", "1PL"), ("ukr", "vy", "wi", "you (pl)", "2PL"),
    ("ukr", "tak", "tak", "yes", "YES"), ("ukr", "ni", "ni", "no", "NO"),
    ("ukr", "i", "i", "and", "AND"), ("ukr", "ne", "ne", "not", "NEG"),
    ("ukr", "na", "na", "on", ""), ("ukr", "tse", "tse", "this", "THIS"),
    # Hindi
    ("hin", "main", "main", "I", "1SG"), ("hin", "tu", "tu", "you", "2SG"),
    ("hin", "tum", "tum", "you", "2SG"), ("hin", "ham", "ham", "we", "1PL"),
    ("hin", "na", "na", "not", "NEG"), ("hin", "nahin", "nahin", "not", "NEG"),
    ("hin", "han", "han", "yes", "YES"), ("hin", "aur", "aur", "and", "AND"),
    ("hin", "ya", "ja", "or", "OR"), ("hin", "se", "se", "from", ""),
    ("hin", "ko", "ko", "to (obj)", ""), ("hin", "ka", "ka", "of", ""),
    ("hin", "hai", "hai", "is", "COP"), ("hin", "ek", "ek", "one", "ONE"),
    ("hin", "do", "do", "two", "TWO"), ("hin", "ye", "je", "this", "THIS"),
    ("hin", "vo", "wo", "that/he", "THAT"), ("hin", "ki", "ki", "that (rel)", "REL"),
    ("hin", "kya", "kja", "question particle", "Q"),
    ("hin", "kaun", "kaun", "who", ""), ("hin", "mein", "mein", "in", ""),
    # Urdu (same stock; kept separate because the population is separate)
    ("urd", "main", "main", "I", "1SG"), ("urd", "tum", "tum", "you", "2SG"),
    ("urd", "nahin", "nahin", "not", "NEG"), ("urd", "han", "han", "yes", "YES"),
    ("urd", "aur", "aur", "and", "AND"), ("urd", "se", "se", "from", ""),
    ("urd", "ko", "ko", "to (obj)", ""), ("urd", "ka", "ka", "of", ""),
    ("urd", "hai", "hai", "is", "COP"), ("urd", "ek", "ek", "one", "ONE"),
    ("urd", "do", "do", "two", "TWO"), ("urd", "kya", "kja", "question particle", "Q"),
    # Bengali
    ("ben", "ami", "ami", "I", "1SG"), ("ben", "tumi", "tumi", "you", "2SG"),
    ("ben", "se", "se", "he/she", "3SG"), ("ben", "na", "na", "no/not", "NO"),
    ("ben", "ha", "ha", "yes", "YES"), ("ben", "ar", "ar", "and", "AND"),
    ("ben", "ba", "ba", "or", "OR"), ("ben", "e", "e", "this", "THIS"),
    ("ben", "o", "o", "that", "THAT"), ("ben", "ek", "ek", "one", "ONE"),
    ("ben", "dui", "dui", "two", "TWO"), ("ben", "ki", "ki", "what/Q", "Q"),
    ("ben", "ke", "ke", "who", ""),
    # Marathi
    ("mar", "mi", "mi", "I", "1SG"), ("mar", "tu", "tu", "you", "2SG"),
    ("mar", "to", "to", "he", "3SG"), ("mar", "nahi", "nahi", "not", "NEG"),
    ("mar", "hoy", "hoi", "yes", "YES"), ("mar", "ani", "ani", "and", "AND"),
    ("mar", "ek", "ek", "one", "ONE"), ("mar", "don", "don", "two", "TWO"),
    ("mar", "he", "he", "this", "THIS"), ("mar", "te", "te", "that", "THAT"),
    # Panjabi
    ("pan", "main", "main", "I", "1SG"), ("pan", "tu", "tu", "you", "2SG"),
    ("pan", "asi", "asi", "we", "1PL"), ("pan", "nahi", "nahi", "not", "NEG"),
    ("pan", "han", "han", "yes", "YES"), ("pan", "te", "te", "and", "AND"),
    ("pan", "ik", "ik", "one", "ONE"), ("pan", "do", "do", "two", "TWO"),
    ("pan", "eh", "eh", "this", "THIS"), ("pan", "oh", "oh", "that/he", "THAT"),
    # Turkish
    ("tur", "ben", "ben", "I", "1SG"), ("tur", "sen", "sen", "you", "2SG"),
    ("tur", "o", "o", "he/that", "3SG"), ("tur", "biz", "bis", "we", "1PL"),
    ("tur", "siz", "sis", "you (pl)", "2PL"), ("tur", "evet", "efet", "yes", "YES"),
    ("tur", "hayir", "hajir", "no", "NO"), ("tur", "ve", "we", "and", "AND"),
    ("tur", "veya", "weja", "or", "OR"), ("tur", "bir", "bir", "one", "ONE"),
    ("tur", "iki", "iki", "two", "TWO"), ("tur", "bu", "bu", "this", "THIS"),
    ("tur", "su", "su", "that", "THAT"), ("tur", "mi", "mi", "question particle", "Q"),
    ("tur", "ne", "ne", "what", "WHAT"), ("tur", "kim", "kim", "who", ""),
    ("tur", "yok", "jok", "there is not", "NEG"),
    ("tur", "var", "far", "there is", "COP"), ("tur", "de", "de", "also", ""),
    # Korean
    ("kor", "na", "na", "I", "1SG"), ("kor", "neo", "no", "you", "2SG"),
    ("kor", "ne", "ne", "yes", "YES"), ("kor", "ani", "ani", "no", "NO"),
    ("kor", "i", "i", "this", "THIS"), ("kor", "geu", "gu", "that", "THAT"),
    ("kor", "do", "do", "also", ""), ("kor", "wa", "wa", "and/with", "AND"),
    ("kor", "han", "han", "one", "ONE"), ("kor", "du", "du", "two", "TWO"),
    ("kor", "mwo", "mwo", "what", "WHAT"), ("kor", "ga", "ga", "subject marker", ""),
    ("kor", "neun", "nun", "topic marker", ""), ("kor", "eul", "ul", "object marker", ""),
    # Arabic (weighted by Egyptian Arabic; MSA has no L1 count)
    ("arz", "ana", "ana", "I", "1SG"), ("arz", "anta", "anta", "you", "2SG"),
    ("arz", "huwa", "huwa", "he", "3SG"), ("arz", "la", "la", "no/not", "NO"),
    ("arz", "naam", "naam", "yes", "YES"), ("arz", "wa", "wa", "and", "AND"),
    ("arz", "aw", "au", "or", "OR"), ("arz", "fi", "fi", "in", ""),
    ("arz", "min", "min", "from", ""), ("arz", "ma", "ma", "what/not", "WHAT"),
    ("arz", "man", "man", "who", ""), ("arz", "hada", "hada", "this", "THIS"),
    # Persian
    ("pes", "man", "man", "I", "1SG"), ("pes", "to", "to", "you", "2SG"),
    ("pes", "u", "u", "he", "3SG"), ("pes", "ma", "ma", "we", "1PL"),
    ("pes", "na", "na", "no", "NO"), ("pes", "bale", "bale", "yes", "YES"),
    ("pes", "va", "wa", "and", "AND"), ("pes", "ya", "ja", "or", "OR"),
    ("pes", "dar", "dar", "in", ""), ("pes", "az", "as", "from", ""),
    ("pes", "be", "be", "to", ""), ("pes", "in", "in", "this", "THIS"),
    ("pes", "an", "an", "that", "THAT"), ("pes", "yek", "jek", "one", "ONE"),
    ("pes", "do", "do", "two", "TWO"), ("pes", "ke", "ke", "that (rel)", "REL"),
    ("pes", "che", "ce", "what", "WHAT"),
    # Javanese
    ("jav", "aku", "aku", "I", "1SG"), ("jav", "kowe", "kowe", "you", "2SG"),
    ("jav", "ora", "ora", "not", "NEG"), ("jav", "iya", "ija", "yes", "YES"),
    ("jav", "lan", "lan", "and", "AND"), ("jav", "iki", "iki", "this", "THIS"),
    ("jav", "iku", "iku", "that", "THAT"), ("jav", "siji", "siji", "one", "ONE"),
    ("jav", "loro", "loro", "two", "TWO"), ("jav", "apa", "apa", "what", "WHAT"),
    # Filipino
    ("fil", "ako", "ako", "I", "1SG"), ("fil", "ka", "ka", "you", "2SG"),
    ("fil", "siya", "sija", "he/she", "3SG"), ("fil", "hindi", "hindi", "no/not", "NO"),
    ("fil", "oo", "o", "yes", "YES"), ("fil", "at", "at", "and", "AND"),
    ("fil", "sa", "sa", "in/to", ""), ("fil", "isa", "isa", "one", "ONE"),
    ("fil", "ito", "ito", "this", "THIS"), ("fil", "ba", "ba", "question particle", "Q"),
    ("fil", "ko", "ko", "my", "1SG"), ("fil", "mo", "mo", "your", "2SG"),
    ("fil", "na", "na", "already/rel", "REL"),
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


def distinctiveness(syl: str, assigned) -> int:
    """RETIRED metric (judgment call 10): Hamming distance over (O, V, C).

    Still computed and written to the CSV, because it is what the previous
    milestone reported and because main() prices the arm that used it.
    """
    if not assigned:
        return 3
    a = _ovc(syl)
    return min(sum(x != y for x, y in zip(a, _ovc(o)))
               for o in assigned if len(o) <= 3)


_SIM_MEMO: dict[tuple[str, str], float] = {}


def sim(a: str, b: str) -> float:
    """Memoized metric-v0 similarity between two interlang forms."""
    key = (a, b) if a <= b else (b, a)
    if key not in _SIM_MEMO:
        _SIM_MEMO[key] = metric.similarity(translit.to_ipa(a), translit.to_ipa(b))
    return _SIM_MEMO[key]


def nearest_sim(syl: str, assigned) -> float:
    """Highest metric similarity to any monosyllable already assigned."""
    others = [o for o in assigned if len(o) <= 4 and o != syl]
    return max((sim(syl, o) for o in others), default=0.0)


def separation_penalty(syl: str, assigned, freq_w: float) -> float:
    """Judgment call 10: pay for landing perceptually close to an existing word."""
    s = nearest_sim(syl, assigned)
    return (W_SEP * (freq_w / 3.0)
            * max(0.0, (s - SEP_FLOOR) / (1.0 - SEP_FLOOR)))


def hamming_penalty(syl: str, assigned, freq_w: float) -> float:
    """The RETIRED term, kept so main() can print the before/after arm."""
    return (W_DIST_HAMMING * (freq_w / 3.0)
            * max(0, 2 - distinctiveness(syl, assigned)))


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
    df = read_csv(path, sep="\t")
    for col in ("RANK", "NUMBER", "CONCEPTICON_ID"):
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def load_wold() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    d = RAW / "wold" / "cldf"
    params = read_csv(d / "parameters.csv")
    forms = read_csv(d / "forms.csv", low_memory=False)
    langs = read_csv(d / "languages.csv")
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
# false friends  (judgment call 11)
# ---------------------------------------------------------------------------
def false_friend_reference(params: pd.DataFrame, forms: pd.DataFrame,
                           langs: pd.DataFrame, by_iso: dict,
                           world_l1: float) -> list[dict]:
    """The reference set: high-frequency words in high-population languages.

    Returns one row per (language, meaning, surface form) with the language's
    L1 share of the world attached.  Two provenances, kept distinguishable in
    the `source` column: WOLD function words [measured] and the hand table
    [recall].
    """
    ref: list[dict] = []
    fw_params = params[params["Semantic_category"].astype(str) == "Function word"]
    pname = dict(zip(fw_params["ID"], fw_params["Name"]))
    key = langs.set_index("ID")
    sub = forms[forms["Parameter_ID"].isin(set(fw_params["ID"]))]
    for _, r in sub.iterrows():
        iso = str(key["ISO639P3code"].get(r["Language_ID"], "") or "")
        pop = float(by_iso.get(iso, 0.0))
        if pop <= 0:
            continue                      # weightless; skip for speed
        written = strip_marks(str(r["Form"]))
        adapted = adapt(str(r["Form"]))
        if not adapted or len(adapted) > 4:
            continue                      # cannot be near-homophonous with a
        ref.append({"lang": r["Language_ID"], "iso": iso,          # monosyllable
                    "share": pop / world_l1, "meaning": r["Parameter_ID"],
                    "gloss": pname.get(r["Parameter_ID"], ""),
                    "written": written, "approx": adapted,
                    "source": "wold"})
    for iso, written, approx, gloss, concept in HAND_FUNCTION_WORDS:
        pop = float(by_iso.get(iso, 0.0))
        if pop <= 0:
            continue
        ref.append({"lang": iso, "iso": iso, "share": pop / world_l1,
                    "meaning": f"hand:{gloss}", "gloss": gloss,
                    "written": written, "approx": approx,
                    "our_concept": concept, "source": "hand"})
    return ref


def ff_index(pool: list[str], ref: list[dict],
             param_to_concept: dict) -> dict[str, list[dict]]:
    """For every monosyllable in the pool, the reference words it collides with.

    A collision is an identical written form, or metric-v0 similarity >= FF_SIM
    ("phonetically very close").  Precomputed once because the greedy loop asks
    for it thousands of times.
    """
    idx: dict[str, list[dict]] = {s: [] for s in pool}
    for e in ref:
        concept = e.get("our_concept", "") or param_to_concept.get(e["meaning"], "")
        for s in pool:
            if s == e["written"] or s == e["approx"] or sim(s, e["approx"]) >= FF_SIM:
                idx[s].append({"lang": e["lang"], "share": e["share"],
                               "meaning": e["meaning"], "gloss": e["gloss"],
                               "written": e["written"], "concept": concept,
                               "source": e["source"]})
    return idx


def ff_score(syl: str, concept: str, our_param: str | None,
             idx: dict[str, list[dict]]) -> tuple[float, str]:
    """Judgment call 11.  Population-weighted false-friend load of `syl`.

    Only the strongest collision per language counts, so a language with three
    matching function words does not pay three times.  A reference word whose
    meaning IS our concept is not a false friend - it is a donor.
    """
    best: dict[str, tuple[float, dict]] = {}
    for h in idx.get(syl, ()):
        if h["concept"] and h["concept"] == concept:
            continue
        if our_param and h["meaning"] == our_param:
            continue
        w = h["share"] * (FF_OWN_MULT if h["concept"] else 1.0)
        if w > best.get(h["lang"], (0.0, None))[0]:
            best[h["lang"]] = (w, h)
    total = sum(w for w, _ in best.values())
    top = "; ".join(
        f"{h['lang']}:{h['written']}={h['gloss']}"
        for _, h in sorted(best.values(), key=lambda x: -x[0])[:4])
    return total, top


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
           ffidx: dict[str, list[dict]] | None = None,
           w_ff: float = W_FF, separation: str = "metric",
           hard_distance2: bool = False) -> list[dict]:
    """Greedy form assignment (judgment call 6).

    `separation` selects the arm of judgment call 10: "metric" is the perceptual
    term now in force, "hamming" the retired code-distance term, "none" neither.
    `w_ff` scales judgment call 11; 0.0 turns it off.  main() runs all three
    arms so the before/after is measured rather than asserted.

    `hard_distance2` turns the retired Hamming preference into a hard constraint
    inside the closed class and the numerals.  It is OFF by default and the
    reason is measured, not assumed: the constraint is provably unsatisfiable
    (see the Singleton bound printed by main()), so it holds for the first ~15
    words and then degrades, and paying for it costs four more coined - i.e.
    donor-less, representation-free - grammatical words.
    """
    pool = monosyllable_pool()
    pop = {}
    for lid, grp in donors.groupby("Language_ID"):
        iso = str(grp["iso"].iloc[0])
        pop[lid] = float(tot.get(iso, 0.0)) or float(by_iso.get(iso, 0.0))
    max_pop = max(pop.values()) if pop else 1.0
    ease = {k: math.log1p(v) / math.log1p(max_pop) for k, v in pop.items()}

    def sep(syl, fw):
        if separation == "metric":
            return separation_penalty(syl, taken, fw)
        if separation == "hamming":
            return hamming_penalty(syl, taken, fw)
        return 0.0

    rows = []
    for c in concepts:
        fw = FREQ_WEIGHT[c["group"]]
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
                    ff, _top = (ff_score(syl, c["concept"], c["wold"], ffidx)
                                if (ffidx and w_ff) else (0.0, ""))
                    score = (W_EASE * ease.get(d["Language_ID"], 0.0)
                             - form_cost(syl, fw)
                             - W_REP * family_count.get(d["family"], 0)
                             - sep(syl, fw)
                             - w_ff * ff)
                    cands.append((score, d["Language_ID"], d["family"],
                                  d["macroarea"], d["Form"], form, syl))
            cands.sort(key=lambda x: (-x[0], x[1]))
            if cands:
                score, lid, fam, area, raw, full, syl = cands[0]
                chosen = (score, lid, fam, area, raw, full, syl, "wold", len(cands))
                break
            # Coined: cheapest free syllable, under the same separation and
            # false-friend terms.  Without them the coined particles come out as
            # a minimal-pair set, which is the worst possible outcome for the
            # most frequent words in the language.
            free = [s for s in pool if s not in taken
                    and not breaks_minimal_pair_ban(s, set(taken))
                    and distinctiveness(s, taken) >= min_dist]

            def coined_key(s):
                ff, _t = (ff_score(s, c["concept"], None, ffidx)
                          if (ffidx and w_ff) else (0.0, ""))
                return (form_cost(s, fw) + sep(s, fw) + w_ff * ff, s)

            free.sort(key=coined_key)
            if free:
                syl = free[0]
                chosen = (0.0, "(coined)", "(none)", "(none)", "", syl,
                          syl, "coined", 0)
                break
        score, lid, fam, area, raw, full, syl, src, ncand = chosen
        dist = distinctiveness(syl, taken)
        nsim = nearest_sim(syl, taken)
        ff, fftop = (ff_score(syl, c["concept"], c["wold"], ffidx)
                     if ffidx else (0.0, ""))
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
                     "nearest_word_similarity": round(nsim, 3),
                     "false_friend_score": round(ff, 4),
                     "false_friend_top": fftop,
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
            s = metric.similarity(ours, rom)
        except Exception:
            continue
        if s >= RECOG_THRESHOLD:
            hits.append((iso, title, round(s, 3), pop))
            hit_pop += pop
        if s >= RECOG_THRESHOLD_STRICT:
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
# the rejected sC-onset option  (judgment call 13)
# ---------------------------------------------------------------------------
SC_VARIANT = translit.Variant(
    "V3CS", frozenset("nm"),
    frozenset(translit.ONSET_CLUSTERS) | {"sp", "st", "sk", "sm", "sn", "sl"},
    label="V3C + sC onsets (measured, rejected)")


def price_sc_onsets() -> dict:
    """Measure what adding sC onsets would buy on the G3 list."""
    base = extra = 0
    inflated = improved = 0
    saved: list[str] = []
    aff_base = aff_sc = 0
    for gloss, intl, _t in TECH:
        a = translit.render(intl, "V3C", epen="labial_u",
                            final_policy="epenthesize")
        b = translit.render(intl, SC_VARIANT, epen="labial_u",
                            final_policy="epenthesize")
        base += a["syl_after"]
        extra += b["syl_after"]
        internal = any(t.startswith("B4 epenthesis (initial cluster)")
                       or t.startswith("B4 epenthesis (medial cluster)")
                       for t in a["trace"])
        if internal:
            aff_base += a["syl_after"]
            aff_sc += b["syl_after"]
        if a["syl_after"] > a["syl_before"]:
            inflated += 1
        if b["syl_after"] < a["syl_after"]:
            improved += 1
            saved.append(f"{gloss}: {a['form']}({a['syl_after']}) -> "
                         f"{b['form']}({b['syl_after']})")
    return {"syllables_v3c": base, "syllables_sc": extra,
            "inflated_words": inflated, "improved_words": improved,
            "pct_all": 100 * (base - extra) / base,
            "pct_affected": 100 * (aff_base - aff_sc) / aff_base,
            "detail": saved}


def wals_12a(by_iso: dict) -> dict:
    """WALS 12A syllable structure, L1-weighted (judgment call 13's other half)."""
    d = RAW / "wals" / "cldf"
    langs = read_csv(d / "languages.csv")
    vals = read_csv(d / "values.csv", low_memory=False)
    codes = read_csv(d / "codes.csv")
    l1 = read_l1_speakers(PROC / "l1_speakers.csv")
    by_gc = dict(zip(l1["glottocode"], l1["l1_speakers"]))
    world = float(l1["l1_speakers"].sum())
    v = vals[vals["Parameter_ID"] == "12A"].copy()
    key = langs.set_index("ID")
    v["gc"] = v["Language_ID"].map(key["Glottocode"])
    v["iso"] = v["Language_ID"].map(key["ISO639P3code"]).fillna("")
    v = v[v["gc"].astype(str) != ""].drop_duplicates("gc")
    v["pop"] = [float(by_iso.get(i, 0.0)) or float(by_gc.get(g, 0.0))
                for i, g in zip(v["iso"], v["gc"])]
    v["name"] = v["Code_ID"].map(dict(zip(codes["ID"], codes["Name"])))
    g = v.groupby("name")["pop"].sum()
    coded = float(g.sum())
    return {"by_value": {k: 100 * val / coded for k, val in g.items()},
            "simple_or_moderate": 100 * (g.get("Simple", 0)
                                         + g.get("Moderately complex", 0)) / coded,
            "coded_share_of_world": 100 * coded / world,
            "n_languages": int(len(v))}


# ---------------------------------------------------------------------------
def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--offline", action="store_true",
                    help="never hit the network; use cached langlinks/lists only")
    ap.add_argument("--hard-distance2", action="store_true",
                    help="enforce >=2-feature distinctness inside the closed "
                         "class and the numerals (the retired alternative arm)")
    args = ap.parse_args()

    # judgment call 8: translit.py's default was fixed on 2026-08-06.  This
    # script always passed the argument explicitly, so the fix must be a no-op
    # here; assert it rather than claim it.
    import inspect
    dflt = inspect.signature(translit.repair).parameters["final_policy"].default
    assert dflt == "epenthesize", f"translit.repair default is {dflt!r}"
    for probe in ("computer", "syntaxis", "virus"):
        a = translit.render(probe, "V3C", epen="labial_u",
                            final_policy="epenthesize")["form"]
        b = translit.render(probe, "V3C", epen="labial_u")["form"]
        assert a == b, f"{probe}: explicit {a} != default {b}"
    print("=== loading ===")
    print("  translit.final_policy default is now 'epenthesize' and matches the "
          "explicit argument this script passes: G3 forms are UNAFFECTED by the fix")

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
    p2 = params.copy()
    p2["cc"] = pd.to_numeric(p2["Concepticon_ID"], errors="coerce")
    cid_to_param = (p2.dropna(subset=["cc"]).assign(cc=lambda d: d.cc.astype(int))
                    .drop_duplicates("cc").set_index("cc")["ID"].to_dict())
    sw_ids = set(pd.to_numeric(sw["CONCEPTICON_ID"], errors="coerce").dropna())
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

    # ---- false-friend reference (judgment call 11) ------------------------
    print("\n=== false-friend reference set ===")
    ref = false_friend_reference(params, forms, langs, by_iso, world_l1)
    n_wold = sum(1 for e in ref if e["source"] == "wold")
    print(f"  {n_wold} WOLD function-word forms [measured] + "
          f"{len(ref)-n_wold} hand-listed function words [recall], "
          f"{len({e['lang'] for e in ref})} languages, "
          f"{100*sum({e['iso']: e['share'] for e in ref}.values()):.1f}% of world L1")
    param_to_concept = {c["wold"]: c["concept"] for c in concepts if c["wold"]}
    pool = monosyllable_pool()
    ffidx = ff_index(pool, ref, param_to_concept)
    print(f"  {sum(1 for s in pool if ffidx[s])} of {len(pool)} usable "
          f"monosyllables collide with at least one of them - which is why the "
          f"term is population-weighted and weak, not a filter")

    # ---- assign monosyllables, three arms --------------------------------
    print("\n=== assigning monosyllabic roots (G1 + G2) ===")
    arms = {}
    for name, kw in (("A: hamming separation, no false friends",
                      dict(separation="hamming", w_ff=0.0)),
                     ("B: metric separation, no false friends",
                      dict(separation="metric", w_ff=0.0)),
                     ("C: metric separation + false friends (DEFAULT)",
                      dict(separation="metric", w_ff=W_FF))):
        taken_a: dict[str, str] = {}
        fam_a: dict[str, int] = {}
        arms[name] = assign(concepts, donors, by_iso, tot, taken_a, fam_a,
                            ffidx=ffidx, hard_distance2=args.hard_distance2,
                            **kw)
    names = list(arms)
    print(f"  arm A = the milestone-1 rule (retired), arm B = judgment call 10, "
          f"arm C = 10 + 11")
    changed = [(a["concept"], a["form"], b["form"], c["form"])
               for a, b, c in zip(*(arms[n] for n in names))
               if not (a["form"] == b["form"] == c["form"])]
    print(f"  {len(changed)} of {len(concepts)} forms differ across the arms:")
    print(f"    {'concept':22s} {'A(old)':>8s} {'B(sep)':>8s} {'C(sep+ff)':>10s}")
    for cid, fa, fb, fc in changed:
        mark = "  <- false friends" if fb != fc else ""
        print(f"    {cid:22s} {fa:>8s} {fb:>8s} {fc:>10s}{mark}")

    rows = arms[names[2]]
    taken = {r["form"]: r["concept"] for r in rows}
    family_count: dict[str, int] = {}
    for r in rows:
        if r["donor_family"] != "(none)":
            family_count[r["donor_family"]] = family_count.get(r["donor_family"], 0) + 1

    ff_paid = [r for r in rows if r["false_friend_score"] > 0]
    ff_paid.sort(key=lambda r: -r["false_friend_score"])
    print(f"\n  false-friend load actually carried by the chosen forms "
          f"({len(ff_paid)} of {len(rows)} pay anything):")
    for r in ff_paid[:12]:
        print(f"    {r['form']:5s} {r['concept']:22s} "
              f"ff={r['false_friend_score']:.3f} "
              f"(penalty {W_FF*r['false_friend_score']:.3f})  {r['false_friend_top']}")

    pool = monosyllable_pool()
    print(f"\n  monosyllable budget: {len(pool)} usable (policy in docstring); "
          f"{len(taken)} assigned; {len(pool)-len(taken)} free "
          f"({100*(len(pool)-len(taken))/len(pool):.0f}% left unassigned)")
    n_ons, n_vow, n_cod = 12, 5, 3
    bound = n_ons * n_vow * n_cod // max(n_ons, n_vow, n_cod)
    near = sum(1 for r in rows if r["nearest_word_distance"] < 2)
    print(f"  arm: {'HARD distance-2 in G1+numerals' if args.hard_distance2 else 'soft perceptual separation (default)'}")
    print(f"  distance-2 bound: at most {bound} monosyllables of this shape can "
          f"be pairwise >=2 features apart (Singleton bound on "
          f"{n_ons}x{n_vow}x{n_cod}); the closed class alone needs "
          f"{len(GRAMMAR)}, so the code framing is dead and "
          f"{near} of {len(rows)} roots sit one feature from another word")
    g1 = [r["form"] for r in rows if r["group"] == "grammar"]
    worst = max(((sim(a, b), a, b) for i, a in enumerate(g1) for b in g1[i+1:]),
                default=(0, "", ""))
    print(f"  closed-class perceptual separation: worst pair is "
          f"{worst[1]}~{worst[2]} at similarity {worst[0]:.3f} "
          f"(the term charges above {SEP_FLOOR})")

    # ---- G2 recognition against the WOLD panel ---------------------------
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
        names_hit = []
        for _, d in sub.iterrows():
            other = adapt(d["Form"])
            if not other:
                continue
            n += 1
            s = metric.similarity(translit.to_ipa(r["form"]),
                                  translit.to_ipa(other))
            if s >= RECOG_THRESHOLD:
                hit += wold_pop.get(d["Language_ID"], 0.0)
                names_hit.append(d["Language_ID"])
            if s >= RECOG_THRESHOLD_STRICT:
                strict += wold_pop.get(d["Language_ID"], 0.0)
        r.update(recog_share_world_l1=hit / world_l1,
                 recog_share_world_l1_strict=strict / world_l1,
                 recog_share_panel=hit / wold_panel_pop if wold_panel_pop else 0.0,
                 panel_languages=n, n_recognizing=len(names_hit),
                 top_recognizers="; ".join(names_hit[:6]))

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
               "wiki_title": title or "",
               "syllable_inflation": res["syl_after"] - res["syl_before"]}
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

    # ---- judgment call 12: the tier-3 fallback ---------------------------
    print("\n=== G3 fallback rule (judgment call 12) ===")
    print(f"  damaged  = inflation >= {G3_MIN_INFLATION} syllables OR "
          f"repaired form >= {G3_MAX_SYLLABLES} syllables")
    print(f"  escapes  = recognition > {G3_KEEP_WORLD:.2f} of world L1 OR "
          f"> {G3_KEEP_PANEL:.2f} of the measured panel")
    print(f"  veto     = no compound in COMPOUNDS passes lexicon-plan 2.4's "
          f"two-way test -> keep the borrowing (lexicon-plan 2.2 asymmetry)")
    by_gloss = {r["gloss"]: r for r in tech_rows}
    g12_form = {r["concept"]: r["form"] for r in rows}
    selected, fell_back, kept_no_compound = [], [], []
    for r in tech_rows:
        s = r["recog_share_world_l1"]
        p = r["recog_share_panel"]
        damaged = (r["syllable_inflation"] >= G3_MIN_INFLATION
                   or r["syllables"] >= G3_MAX_SYLLABLES)
        escapes = ((s == s and s > G3_KEEP_WORLD)
                   or (p == p and p > G3_KEEP_PANEL))
        r["fallback_flag"] = ""
        if not damaged or escapes:
            continue
        selected.append(r)
        if r["gloss"] not in COMPOUNDS:
            r["fallback_flag"] = "flagged: no transparent compound (kept)"
            kept_no_compound.append(r)
            continue
        parts, cgloss, why = COMPOUNDS[r["gloss"]]
        pieces = [g12_form[p_id] if kind == "G12" else by_gloss[p_id]["form"]
                  for kind, p_id in parts]
        compound = "".join(pieces)
        assert translit.is_legal(compound, translit.VARIANTS["V3C"]), compound
        r["borrowing_form"] = r["form"]
        r["borrowing_syllables"] = r["syllables"]
        r["borrowing_recog_world"] = s
        r["borrowing_recog_panel"] = p
        r["form"] = compound
        r["syllables"] = translit.syllables(compound)
        r["source"] = "compound"
        r["donor"] = "(native compound)"
        r["donor_family"] = "(none)"
        r["donor_macroarea"] = "(none)"
        r["donor_adapted"] = compound
        r["compound_parts"] = "+".join(pieces)
        r["compound_gloss"] = cgloss
        r["compound_note"] = why
        r["seg_cost"] = round(form_cost(compound, 1.0), 3)
        r["fallback_flag"] = "fell back to a native compound"
        r["recog_instrument"] = "wikipedia_langlinks (compound; expect ~0)"
        if r["wiki_title"] and wiki2iso:
            blob = fetch_langlinks(r["wiki_title"], args.offline)
            r.update(recognition(compound, langlink_titles(blob), wiki2iso,
                                 by_iso, world_l1))
        fell_back.append(r)
    print(f"\n  {len(selected)} of {len(tech_rows)} borrowings selected by "
          f"(damaged AND no recognition escape):")
    for r in selected:
        tag = "COMPOUND" if r in fell_back else "kept (no compound)"
        print(f"    {r['gloss']:22s} {r.get('borrowing_form', r['form']):14s} "
              f"infl={r['syllable_inflation']} syl="
              f"{r.get('borrowing_syllables', r['syllables'])} "
              f"world={r['borrowing_recog_world'] if r in fell_back else r['recog_share_world_l1']:.3f} "
              f"-> {tag}"
              + (f" {r['form']} ({r['compound_gloss']})" if r in fell_back else ""))
    print(f"\n  {len(fell_back)} fell back, {len(kept_no_compound)} kept and flagged")

    # ---- judgment call 14: alternative source spellings, priced not adopted
    print("\n=== alternative international spellings (priced, NOT adopted) ===")
    for gloss, alts in ALT_SPELLINGS.items():
        r = by_gloss[gloss]
        cur = r.get("borrowing_form", r["form"])
        cur_recog = r.get("borrowing_recog_world", r["recog_share_world_l1"])
        cur_syl = r.get("borrowing_syllables", r["syllables"])
        title = r["wiki_title"]
        for alt in alts:
            res = translit.render(alt, "V3C", epen="labial_u",
                                  final_policy="epenthesize")
            rec = float("nan")
            if title and wiki2iso:
                blob = fetch_langlinks(title, args.offline)
                rec = recognition(res["form"], langlink_titles(blob), wiki2iso,
                                  by_iso, world_l1)["recog_share_world_l1"]
            better = (res["syl_after"] < cur_syl and rec >= cur_recog - 0.005)
            print(f"    {gloss:14s} {cur:14s} {cur_syl}syl {cur_recog:.3f}   ->  "
                  f"{alt:13s} {res['form']:14s} {res['syl_after']}syl {rec:.3f}"
                  f"{'   <- dominates' if better else ''}")

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
    print(f"  'nan' is in the legal monosyllable pool: {'nan' in monosyllable_pool()}"
          f"; assigned to: {taken.get('nan', '(free)')}")

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
              f"stress on '{syllabify(res['form'])[0]}')"
              + (f"   [FELL BACK to {by_gloss[gloss]['form']}]"
                 if by_gloss[gloss].get("source") == "compound" else ""))
    ex = next(r for r in rows if r["concept"] == "FIRE")
    print(f"\n  FIRE (G2 core, rank 1): donor {ex['donor']} '{ex['donor_form']}' "
          f"-> adapted '{ex['donor_adapted']}' -> first syllable '{ex['form']}' "
          f"({ex['n_donor_candidates']} donor candidates competed)")

    # ---- the rejected sC-onset option ------------------------------------
    print("\n=== sC onsets: measured and REJECTED (judgment call 13) ===")
    sc = price_sc_onsets()
    print(f"  {sc['inflated_words']} of {len(TECH)} G3 words gain syllables under "
          f"V3C; adding {{sp st sk sm sn sl}} improves {sc['improved_words']} of "
          f"them")
    print(f"  total G3 syllables {sc['syllables_v3c']} -> {sc['syllables_sc']} "
          f"({sc['pct_all']:.1f}% of all G3 syllables, {sc['pct_affected']:.1f}% "
          f"of the affected words')")
    for line in sc["detail"]:
        print(f"      {line}")
    print("  the damage sC cannot touch is word-INTERNAL: /kt/ in dictionario, "
          "adjectivo, traductione, projecto, dialecto; /ks/ from <x> in "
          "syntaxis, texto, lexicon")
    w = wals_12a(by_iso)
    print(f"  WALS 12A ({w['n_languages']} languages, covering "
          f"{w['coded_share_of_world']:.1f}% of world L1): "
          + ", ".join(f"{k} {v:.1f}%" for k, v in sorted(w["by_value"].items())))
    print(f"  simple or moderately complex = {w['simple_or_moderate']:.1f}% of the "
          f"L1 WALS codes, so an /st/ onset is hard for a majority.  NOT ADOPTED.")

    # ---- write -----------------------------------------------------------
    df = pd.DataFrame(all_rows)
    PROC.mkdir(parents=True, exist_ok=True)
    cols = ["group", "concept", "gloss", "form", "syllables", "donor",
            "donor_family", "donor_macroarea", "donor_form", "donor_adapted",
            "source", "seg_cost", "seg_cost_weighted", "score",
            "nearest_word_distance", "nearest_word_similarity",
            "false_friend_score", "false_friend_top",
            "n_donor_candidates", "recog_instrument", "wiki_title",
            "syllable_inflation", "fallback_flag", "borrowing_form",
            "borrowing_syllables", "borrowing_recog_world", "compound_parts",
            "compound_gloss",
            "panel_languages", "panel_share_world_l1", "n_recognizing",
            "recog_share_world_l1", "recog_share_world_l1_strict",
            "recog_share_panel", "threshold",
            "top_recognizers", "rank", "concepticon", "wold"]
    df = df.reindex(columns=[c for c in cols if c in df.columns])
    df.to_csv(OUT_CSV, index=False)

    # REGRESSION ASSERTION for the `nan` trap.  Read the file back the way the
    # module docstring tells callers to, and fail loudly if any form is not a
    # str - which is exactly what happens when keep_default_na is left on.
    back = read_csv(OUT_CSV)
    bad = [(i, v) for i, v in enumerate(back["form"]) if not isinstance(v, str)]
    assert not bad, f"form column did not round-trip as strings: {bad[:5]}"
    assert list(back["form"]) == list(df["form"]), "form column changed on round-trip"
    naive = pd.read_csv(OUT_CSV)
    n_lost = sum(1 for v in naive["form"] if not isinstance(v, str))
    print(f"\n  round-trip check: {len(back)} forms read back as strings; a NAIVE "
          f"pd.read_csv would corrupt {n_lost} of them "
          f"({[f for f, v in zip(df['form'], naive['form']) if not isinstance(v, str)]})")

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
    print("\n=== recognition thresholds (G3 borrowings) ===")
    t = df[(df.group == "technical") & (df.source != "compound")]
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
    print("\n=== the full word list ===")
    for grp in ("grammar", "numeral", "generic", "core", "technical"):
        g = df[df.group == grp]
        print(f"\n  {grp} ({len(g)}):")
        for _, r in g.iterrows():
            extra = ""
            if r.source == "compound":
                extra = f"  <- compound {r.compound_parts} '{r.compound_gloss}'"
            elif r.source == "coined":
                extra = "  (coined)"
            elif r.group != "technical":
                extra = f"  <- {r.donor} '{r.donor_form}' ({r.donor_family})"
            print(f"    {r.form:14s} {r.concept:24s}{extra}")
    print(f"\nwrote {OUT_CSV}")


if __name__ == "__main__":
    main()
