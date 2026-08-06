"""THE FINAL GRAMMAR BIAS AUDIT: where the finished grammar actually lands.

Promised by notes/grammar-plan.md 1: *"This grammar is 90% Standard Average
European with a Mandarin TAM system" should be a measured statement we publish,
not a bias we absorb.*  The grammar closed on 2026-08-06 at 19 words and 7 rules
(principles.md 3.2); this script is the measurement.  Write-up:
notes/grammar-bias-audit.md.

Three parts, only the first of which is a computation:

  PART 1  WHERE DOES INTERLANG LAND?  Encode every grammar decision that maps
          cleanly onto a Grambank feature (and, for the contact comparison, onto
          an APiCS parameter), then score agreement with every language in each
          database over the features both sides define.  Report the nearest and
          furthest languages, aggregate by family and macroarea BY LANGUAGE and
          BY L1 POPULATION (the by-language/by-people reversal has driven most of
          this project's decisions), name-check the languages a reader will ask
          about, and - the sharpest test - ask whether we landed near the pidgins
          and creoles the grammar was designed from.

  PART 2  THE POPULATION OVERRIDES.  Every decision taken against a majority of
          world L1, RE-MEASURED here from the source feature rather than quoted
          from the write-up that made the decision, and ranked by population cost.

  PART 3  THE UNMAPPED FEATURE SCAN.  Grambank features on which interlang has no
          value are, by construction, either genuinely uncodable or things nobody
          decided.  The Tier 3 cleanup found four features that had been silently
          assumed (grammar-tier3-cleanup.md), so this is a real search: the script
          prints the unmapped list and the write-up triages it by hand.

WHY GRAMBANK AND NOT WALS
-------------------------
grammar-plan.md 3.1: Grambank is 4.7x denser (0.75 vs 0.16) and covers the big
languages WALS misses (Mandarin, Wu and German are absent from the WALS word-order
and morphology chapters).  A similarity score is a per-language quantity, so
density is decisive here in a way it is not for a marginal percentage.  WALS is
used in PART 2 only, where a specific write-up quoted a specific WALS chapter.

THE MAIN JUDGMENT CALL, AND IT IS A BIG ONE
-------------------------------------------
INTERLANG_GB and INTERLANG_APICS below ARE the study.  Every entry is a claim that
one of our decisions is the same thing a Grambank/APiCS coder would have coded, and
a different analyst would code some of them differently.  Policies:

  1. EVERY entry carries a one-line rationale naming the decision it comes from.
  2. Entries flagged `contested=True` are ones where a defensible coder could
     choose the other value.  The script re-runs the whole of PART 1 with every
     contested feature flipped and reports how far the headline moves.  If the
     conclusion survives the flip it does not rest on our coding taste.
  3. WHERE A DECISION MAPS ONTO NO CODED FEATURE, IT IS LEFT OUT rather than
     forced onto an adjacent one.  ("A feature name is not a feature definition"
     - grammar-tier3-combination.md 7, where WALS 123A and 94A were both misapplied.)
  4. Decisions that are the ABSENCE of a category are still coded 0 where Grambank
     asks "is there an X?".  That is what Grambank means by 0, and refusing to
     code it would silently drop most of the grammar.

THE CALIBRATION THAT KEEPS THE HEADLINE HONEST
----------------------------------------------
Grambank is 68% zeros, and interlang is a minimal isolating language whose vector
is also mostly zeros.  A raw agreement of 0.75 therefore means nothing on its own.
Three baselines are computed on the identical feature set and reported alongside
every interlang number:

  ALL-ZERO      a hypothetical language with none of the coded features.  This is
                the "you scored well by having nothing" floor, and it is the one
                that matters most for us.
  ALL-MODE      the majority value of each feature - the best possible "average
                language" strawman.
  LANGUAGE-PAIR the distribution of agreement between two randomly drawn real
                languages.  This is what "similar" means empirically.

Other policies baked in here
----------------------------
  - Doculect/dialect dedup, `?`-is-not-coverage and population weighting are all
    inherited from scripts/grammar_sources.py (populations/weight/load).
  - Grambank `level == 'language'` only; family- and dialect-level rows dropped.
  - A language is ranked only if it shares >= MIN_SHARED features with us, so the
    "most similar language" is never a language with eight coded features.
  - Grambank multi-state features (GB024/025/065/130/193/203) are compared on the
    full 1/2/3 scale; value 3 ("both orders") is a genuine mismatch with our
    committed value, not a half-credit.  Same policy as grammar_tier2_np.py.
  - APiCS is multivalued: highest-`Frequency` value per (language, parameter),
    as in grammar_tier2_np.apics_table.  Contact type comes from
    grammar_tier2_tam.contact_type and lexifier group from grammar_sources.
  - MIXED languages (Michif, Media Lengua, Ma'a/Mbugu, Gurindji Kriol) are
    excluded from the APiCS comparison, as everywhere else in this project: they
    arise in bilingual communities, not from a no-shared-language situation.
  - Grambank classifies creoles inside their LEXIFIER's family (Haitian is
    Indo-European, Tok Pisin is Indo-European).  For the family/macroarea
    aggregation the 14 Grambank-coded contact languages are pulled out into their
    own "contact language" group, otherwise they inflate Indo-European.

Usage:   uv run python scripts/grammar_bias_audit.py
Inputs:  data/raw/{grambank,apics,wals}/cldf/*.csv, data/processed/l1_speakers.csv
Outputs: data/processed/grammar_bias_audit.csv        (one row per language x database)
         data/processed/grammar_bias_audit_features.csv (the encoded vector, with
                                                         rationale and per-feature
                                                         world-agreement rates)
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))

from grammar_sources import load, populations, weight  # noqa: E402
from grammar_tier2_np import wals_dist  # noqa: E402
from grammar_tier2_tam import contact_type  # noqa: E402

OUT = ROOT / "data" / "processed" / "grammar_bias_audit.csv"
OUT_FEAT = ROOT / "data" / "processed" / "grammar_bias_audit_features.csv"

MIN_SHARED = 60          # Grambank features a language must share to be ranked
MIN_SHARED_APICS = 25    # ditto for APiCS
RNG_SEED = 20260806
N_PAIRS = 40_000         # random language pairs for the pair baseline


# ===========================================================================
# THE VECTOR.  (grambank_id, value, contested, rationale)
# `value` is a string because Grambank values are strings ('0'/'1', or '1'/'2'/'3'
# for the six order features).  `contested` marks a coding another analyst could
# defensibly flip; the sensitivity run flips all of them at once.
# ===========================================================================
INTERLANG_GB: list[tuple[str, str, bool, str]] = [
    # ---- constituent order and head-directionality (Tier 0) ----------------
    ("GB130", "1", False, "SVO: S precedes V in intransitives"),
    ("GB131", "0", False, "SVO: not verb-initial"),
    ("GB132", "1", False, "SVO: verb-medial"),
    ("GB133", "0", False, "SVO: not verb-final"),
    ("GB136", "1", False, "argument order is fixed - it is the ONLY marker of role"),
    ("GB134", "1", True,  "same order in subordinate clauses; no rule says otherwise "
                          "(GB134 is 96.4% of L1) - entailed, never explicitly decided"),
    ("GB135", "1", True,  "complement clauses fill the object slot (Tier 3), so clausal "
                          "and nominal objects sit in the same place"),
    ("GB074", "1", False, "prepositions (Tier 0)"),
    ("GB075", "0", False, "no postpositions (Tier 0)"),

    # ---- noun-phrase order: the modifier rule (Q11) -------------------------
    ("GB193", "1", False, "modifier rule: property word precedes noun"),
    ("GB024", "1", False, "modifier rule: numeral precedes noun"),
    ("GB025", "1", False, "modifier rule: demonstrative precedes noun"),
    ("GB065", "1", False, "modifier rule: possessor precedes possessed"),
    ("GB203", "1", False, "modifier rule: 'all' precedes noun"),
    ("GB026", "0", False, "no discontinuous NPs - fixed order, no movement"),
    ("GB327", "1", False, "relative clause follows the noun (Tier 0 / Tier 3)"),
    ("GB328", "0", False, "relative clause never precedes"),
    ("GB329", "0", False, "no internally-headed relatives"),
    ("GB330", "0", False, "no correlatives"),

    # ---- articles and nominal categories (Q7) -------------------------------
    ("GB020", "0", False, "no definite article - the demonstrative does the work"),
    ("GB021", "0", False, "no indefinite article - 'one' does the work"),
    ("GB022", "0", False, "no articles at all, so none prenominal"),
    ("GB023", "0", False, "no articles at all, so none postnominal"),
    ("GB042", "0", False, "no morphology: no singular marking"),
    ("GB043", "0", False, "no dual"),
    ("GB044", "0", False, "no plural MORPHOLOGY (we use a free word - see GB318)"),
    ("GB046", "0", False, "no associative plural"),
    ("GB039", "0", False, "no morphology, so no allomorphy of number markers"),
    ("GB041", "0", False, "no suppletive nouns for number"),
    ("GB316", "0", False, "no dedicated singular word"),
    ("GB317", "0", False, "no dual"),
    ("GB318", "1", True,  "optional plural WORD (Q7). Grambank says 'regularly marked'; "
                          "ours is optional, so a coder might say 0"),
    ("GB319", "0", False, "no trial"),
    ("GB320", "0", False, "no paucal"),
    ("GB165", "0", False, "no trial marking on nouns"),
    ("GB166", "0", False, "no paucal marking on nouns"),
    ("GB057", "0", False, "no numeral classifiers (Q7) - a deliberate override, see PART 2"),
    ("GB058", "0", False, "no possessive classifiers (Tier 3 predication)"),
    ("GB059", "0", False, "no alienable/inalienable split (Tier 3 predication)"),
    ("GB038", "0", False, "no demonstrative classifiers"),
    ("GB036", "0", False, "no elevation deixis"),
    ("GB037", "0", False, "no visible/non-visible deixis"),

    # ---- gender and noun class (Tier 0, Q8) ---------------------------------
    ("GB051", "0", False, "no gender/noun class"),
    ("GB052", "0", False, "no gender/noun class"),
    ("GB053", "0", False, "no gender/noun class"),
    ("GB054", "0", False, "no gender/noun class"),
    ("GB192", "0", False, "no gender/noun class"),
    ("GB321", "0", False, "no gender/noun class"),
    ("GB170", "0", False, "no agreement of any kind"),
    ("GB171", "0", False, "no agreement of any kind"),
    ("GB172", "0", False, "no articles and no agreement"),
    ("GB184", "0", False, "no number agreement"),
    ("GB185", "0", False, "no number agreement"),
    ("GB186", "0", False, "no articles and no agreement"),
    ("GB198", "0", False, "no numeral agreement"),
    ("GB314", "0", False, "no gender, so no augmentative by class shift"),
    ("GB315", "0", False, "no gender, so no diminutive by class shift"),

    # ---- case and alignment (Tier 0, Q8) ------------------------------------
    ("GB070", "0", False, "no case on nouns (Tier 0)"),
    ("GB071", "0", False, "no case on pronouns (Q8) - this is what killed alignment"),
    ("GB072", "0", False, "no oblique case - prepositions instead"),
    ("GB073", "0", False, "no oblique case on pronouns"),
    ("GB408", "0", False, "no flagging at all, so no accusative alignment"),
    ("GB409", "0", False, "no flagging at all, so no ergative alignment"),
    ("GB410", "1", True,  "neutral alignment: S, A and P are all unflagged. A coder "
                          "might read GB410 as requiring a flagging system to exist"),

    # ---- verbal morphology and agreement (Tier 0) ---------------------------
    ("GB079", "0", False, "no affixes (Tier 0)"),
    ("GB080", "0", False, "no affixes (Tier 0)"),
    ("GB081", "0", False, "no affixes (Tier 0)"),
    ("GB089", "0", False, "no person indexing on the verb"),
    ("GB090", "0", False, "no person indexing on the verb"),
    ("GB091", "0", False, "no person indexing on the verb"),
    ("GB092", "0", False, "no person indexing on the verb"),
    ("GB093", "0", False, "no person indexing on the verb"),
    ("GB094", "0", False, "no person indexing on the verb"),
    ("GB095", "0", False, "no marking to vary"),
    ("GB096", "0", False, "no marking to vary"),
    ("GB098", "0", False, "no marking to vary"),
    ("GB099", "0", False, "no stem alternation - invariant word forms"),
    ("GB400", "0", False, "no person marking anywhere to neutralise"),
    ("GB111", "0", False, "no conjugation classes - nothing inflects"),
    ("GB109", "0", False, "no verb suppletion for participant number"),
    ("GB110", "0", False, "no verb suppletion for tense/aspect"),
    ("GB300", "0", False, "no suppletion; regularity is a stated design goal"),
    ("GB402", "0", False, "no suppletion"),
    ("GB403", "0", False, "no suppletion"),

    # ---- TAM (Q6): there is no TAM grammar ----------------------------------
    ("GB082", "0", False, "no tense morphology (Q6)"),
    ("GB083", "0", False, "no tense morphology (Q6)"),
    ("GB084", "0", False, "no tense morphology (Q6)"),
    ("GB086", "0", False, "no aspect morphology (Q6)"),
    ("GB312", "0", False, "no mood morphology (Q6)"),
    ("GB309", "0", False, "no graded remoteness tenses (Q6 context feature)"),
    ("GB119", "0", False, "no inflecting words at all"),
    ("GB120", "0", False, "no inflecting words at all"),
    ("GB121", "0", False, "no inflecting words at all"),
    ("GB519", "0", True,  "Q6: mood is an OPEN-CLASS ADVERB, not an auxiliary particle. "
                          "A coder who reads 'non-inflecting word' loosely would say 1"),
    ("GB520", "0", True,  "Q6: aspect is an open-class adverb, not a particle"),
    ("GB521", "0", True,  "Q6: tense is an open-class adverb, not a particle"),
    ("GB322", "0", False, "no grammatical evidentiality (entailed by Q6, never stated)"),
    ("GB323", "0", False, "no grammatical evidentiality (entailed by Q6, never stated)"),

    # ---- valency and voice --------------------------------------------------
    ("GB103", "0", False, "no applicatives - no affixes"),
    ("GB104", "0", False, "no applicatives - no affixes"),
    ("GB105", "0", False, "indirect-object ditransitive: the recipient takes a "
                          "preposition, so it is NOT marked like a monotransitive patient"),
    ("GB113", "0", False, "no transitivising affixes"),
    ("GB114", "0", False, "reflexive is a free word, not bound"),
    ("GB115", "0", False, "no bound reciprocal"),
    ("GB147", "0", False, "no morphological passive - Tier 3 cleanup 2a"),
    ("GB148", "0", False, "no antipassive"),
    ("GB149", "0", False, "no inverse marking"),
    ("GB155", "0", False, "no causative affixes (Tier 0)"),
    ("GB156", "0", False, "no 'say'-causative"),
    ("GB302", "1", False, "preverbal `self` IS a phonologically free passive marker "
                          "(Tier 3 cleanup 2a; the 64.6%-of-L1 strategy)"),
    ("GB303", "0", False, "no antipassive"),
    ("GB304", "1", False, "the agent is expressible: `window self break by man`"),
    ("GB305", "1", False, "one invariant free reflexive pronoun (Q8)"),
    ("GB116", "0", False, "no shape-classifying verbs"),
    ("GB124", "0", False, "no noun incorporation"),
    ("GB127", "0", False, "no obligatory posture verbs"),
    ("GB146", "0", False, "no controlled/uncontrolled distinction"),
    ("GB401", "0", True,  "patient-labile verbs ('the window broke') were NEVER DECIDED; "
                          "coded 0 because the passive was adopted to do that job"),

    # ---- negation (Q9) ------------------------------------------------------
    ("GB107", "0", False, "negation is a free word, not an affix (Q9)"),
    ("GB298", "0", False, "the negator does not inflect"),
    ("GB299", "1", False, "one free negative particle (Q9)"),
    ("GB137", "0", False, "negation is preverbal, never clause-final"),
    ("GB138", "0", False, "negation is preverbal; with an obligatory subject it is "
                          "never clause-initial"),
    ("GB139", "0", False, "the prohibitive uses the same negator (Q9) - a population "
                          "override, see PART 2"),
    ("GB140", "1", False, "one negator for verbal, locational, existential and nominal "
                          "predication (Q9)"),

    # ---- predication, possession, existence (Tier 3) ------------------------
    ("GB117", "1", False, "one invariant copula for predicate nominals"),
    ("GB068", "0", False, "adjectives take the copula; they are not verbs"),
    ("GB069", "0", False, "attributive adjectives are not treated like verbs"),
    ("GB126", "1", True,  "the copula used intransitively IS the existential. A coder "
                          "wanting a DEDICATED existential verb would say 0"),
    ("GB250", "1", False, "predicative possession is a transitive 'have' (Tier 3)"),
    ("GB252", "0", False, "no locational possession"),
    ("GB253", "0", False, "no dative possession - no case"),
    ("GB254", "0", False, "no adnominal-style predicative possession"),
    ("GB256", "0", False, "no comitative possession"),
    ("GB430", "0", False, "no possessive affixes"),
    ("GB431", "0", False, "no possessive affixes"),
    ("GB432", "0", False, "no possessive affixes"),
    ("GB433", "0", False, "no possessive affixes"),
    ("GB313", "0", False, "no special possessive pronouns - the plain pronoun in the "
                          "possessor slot is the possessive (Q8)"),

    # ---- pronouns (Q8) ------------------------------------------------------
    ("GB028", "0", False, "no clusivity (Q8)"),
    ("GB030", "0", False, "no gender in 3rd person pronouns (Q8) - override, PART 2"),
    ("GB031", "0", False, "no dual (Q8)"),
    ("GB196", "0", False, "no gender in 2nd person pronouns"),
    ("GB197", "0", False, "no gender in 1st person pronouns"),
    ("GB167", "0", False, "no logophoric pronoun (Q8)"),
    ("GB415", "0", False, "no politeness distinction (Q8, Tier 5 13) - the largest "
                          "override in the project, PART 2"),
    ("GB522", "0", False, "no pro-drop; the subject is obligatory (Tier 3 cleanup) - "
                          "override, PART 2"),

    # ---- questions (Q10) ----------------------------------------------------
    ("GB257", "1", True,  "intonation remains available, never required (Q10). Grambank "
                          "asks 'can', so 1; a coder reading it as 'is it the strategy' "
                          "would say 0"),
    ("GB260", "0", False, "inversion rejected - Rule 2 LOST 8 / KEPT 0 (Q10)"),
    ("GB262", "1", False, "one clause-initial polar question particle (Q10)"),
    ("GB263", "0", False, "not clause-final"),
    ("GB264", "0", False, "not second-position"),
    ("GB285", "0", False, "no verbal morphology"),
    ("GB286", "0", False, "no verbal morphology"),
    ("GB291", "0", False, "no tone (phonology, 3.3)"),
    ("GB297", "0", False, "no V-not-V (Q10, considered and declined)"),
    ("GB324", "0", False, "no interrogative verb (Q10)"),
    ("GB325", "0", False, "no count/mass distinction in interrogative quantifiers (Q10)"),
    ("GB326", "1", False, "content interrogatives stay in situ (Q10)"),

    # ---- coordination, comparison, subordination (Tier 3) -------------------
    ("GB027", "1", False, "'and' and 'with' are different words (Tier 3)"),
    ("GB301", "0", False, "no inclusory construction (Tier 3)"),
    ("GB265", "0", False, "no 'exceed' comparative (Tier 3)"),
    ("GB266", "0", False, "no locational standard marker (Tier 3)"),
    ("GB270", "0", False, "no conjoined comparative (0.0% of L1)"),
    ("GB273", "1", False, "dedicated standard marker 'than' (Tier 3)"),
    ("GB275", "0", False, "no bound degree marker - no affixes"),
    ("GB276", "0", False, "adjective left unmarked; no free 'more' either (Tier 3) - "
                          "override, PART 2"),
    ("GB421", "1", False, "the relativizer doubles as an optional PREPOSED complementizer"),
    ("GB422", "0", False, "never postposed"),
    ("GB150", "0", False, "no clause chaining - coordination and subordination only"),
    ("GB151", "0", False, "no switch reference"),
    ("GB152", "0", False, "no simultaneous/sequential marking"),

    # ---- word formation (Tier 0, Tier 4, lexicon-plan) ----------------------
    ("GB047", "0", True,  "'run-thing' is a COMPOUND, not a derivational morpheme "
                          "(Tier 4 2). A coder counting compounding as morphology says 1"),
    ("GB048", "0", True,  "'teach-person' is a compound (Tier 4 2)"),
    ("GB049", "0", True,  "'X-thing' is a compound (Tier 4 2)"),
    ("GB187", "0", True,  "diminutive is 'small X', an ordinary modifier"),
    ("GB188", "0", True,  "augmentative is 'big X', an ordinary modifier"),
    ("GB122", "1", False, "verb compounding is regular - it is our only word-formation "
                          "device (Tier 0, Tier 4 2)"),
    ("GB123", "0", True,  "verb-adjunct/light-verb constructions were never decided; "
                          "coded 0 because `water-do` is analysed as a compound"),
    ("GB158", "1", True,  "reduplication ADOPTED as optional and emphatic - but by "
                          "lexicon-plan.md 6, AFTER the grammar closed, and it is SOFT"),
    ("GB159", "1", True,  "as GB158"),
    ("GB333", "1", False, "decimal numerals (Tier 4 4)"),
    ("GB334", "0", False, "no quinary element"),
    ("GB335", "0", False, "no vigesimal element"),
    ("GB336", "0", False, "no body-part tallying"),
    ("GB204", "1", False, "'all' and 'every' differ (Tier 4 5)"),
    ("GB118", "0", False, "no serial verbs (Tier 3 cleanup 1) - override, PART 2"),
]

# Grambank features deliberately NOT encoded, with the reason.  PART 3's scan
# prints everything unmapped; these are the ones already triaged, so the scan's
# output minus this set is the genuinely-new list.
GB_DELIBERATELY_UNMAPPED = {
    "GB035": "number of deictic distance contrasts - a lexicon question, undecided",
    "GB306": "independent reciprocal pronoun - RECIPROCALS WERE NEVER DECIDED (PART 3)",
    "GB129": "size of the verb-root inventory - lexicon stage, undecided",
    "GB160": "reduplication of non-verbs/non-nouns - too specific to call",
    "GB296": "ideophones - lexicon stage, undecided",
    "GB331": "non-adjacent (extraposed) relative clauses - undecided (PART 3)",
    "GB177": "verbal animacy marking - subsumed by 'no verbal morphology', but the "
             "feature is about a marker we could not have; not forced",
    "GB108": "directional/locative marking ON THE VERB - morphological, so 0, but this "
             "is the nearest thing Grambank has to the satellite-framing commitment "
             "and reading it that way would be a category error (PART 3)",
}


# ===========================================================================
# THE APiCS VECTOR.  (parameter_id, code NUMBER, contested, rationale)
#
# CAREFUL: APiCS `codes.csv` has BOTH an `ID` (e.g. "1-2") and a `Number` (the
# display order).  values.csv stores the ID's suffix, NOT the Number, and for
# many parameters the two disagree - parameter 1's SVO is Number 1 but suffix 2.
# The values below are NUMBERs, because that is what the published feature tables
# in the write-ups quote, and `apics_number_to_value()` converts them.  Getting
# this backwards silently scores every language at zero, which is how it was
# caught.
# ===========================================================================
INTERLANG_APICS: list[tuple[str, str, bool, str]] = [
    ("1",   "1", False, "SVO"),
    ("2",   "1", False, "possessor-possessum (modifier rule)"),
    ("3",   "1", False, "adjective precedes noun"),
    ("4",   "1", False, "prepositions"),
    ("5",   "1", False, "demonstrative precedes noun"),
    ("6",   "1", False, "numeral precedes noun"),
    ("7",   "1", False, "relative clause follows noun"),
    ("8",   "1", False, "degree word precedes adjective (modifier rule)"),
    ("9",   "4", False, "no definite article"),
    ("10",  "3", False, "no indefinite article"),
    ("11",  "2", False, "adverb-verb-object (modifier rule, Q11a)"),
    ("12",  "2", False, "interrogative phrase not initial - in situ (Q10)"),
    ("13",  "1", False, "no gender in pronouns (Q8)"),
    ("14",  "1", False, "no dual (Q8)"),
    ("15",  "1", False, "no clusivity (Q8)"),
    ("16",  "1", False, "no person syncretism - all six forms distinct (Q8)"),
    ("17",  "1", False, "no dependent subject/object forms (Q8)"),
    ("18",  "1", False, "no politeness distinction (Q8)"),
    ("19",  "5", True,  "interrogatives are built by compounding; we have five compound "
                        "expressions and APiCS's top code is 'four'"),
    ("20",  "1", False, "plain pronoun conjunction, no inclusory (Tier 3)"),
    ("21",  "2", False, "generic-noun-based indefinites (Tier 4 6)"),
    ("22",  "3", True,  "optional plural marking on any noun; APiCS's 'variable' codes "
                        "are graded by animacy, which we do not condition on"),
    ("23",  "7", False, "plural WORD preceding the noun (Q7 + modifier rule)"),
    ("26",  "2", True,  "reduplication with iconic functions only - lexicon-plan.md 6, "
                        "adopted after the grammar closed, SOFT"),
    ("28",  "4", True,  "neither definite nor indefinite article. A coder could call our "
                        "definiteness-by-demonstrative code 2"),
    ("29",  "4", False, "neither indefinite nor definite article"),
    ("31",  "4", False, "no definite article exists"),
    ("35",  "3", False, "all ordinals derived from cardinals, no suppletion (Tier 4 4)"),
    ("36",  "1", False, "no numeral classifiers (Q7)"),
    ("37",  "1", False, "pronominal possessor is a preceding word (Q8 + Q11)"),
    ("38",  "2", False, "possessor NPs are unmarked - position alone (Q11)"),
    ("39",  "1", False, "independent possessive = the plain pronoun (Q8)"),
    ("41",  "2", False, "adjective is not marked in comparatives (Tier 3)"),
    ("42",  "4", False, "particle marking of the standard - 'than' (Tier 3)"),
    ("43",  "5", False, "NO TAM MARKERS - the Q6 taste-based departure, in one cell"),
    ("49",  "4", False, "no tense/aspect markers at all (Q6)"),
    ("50",  "5", False, "no TAM markers, so negation cannot disturb them (Q6/Q9)"),
    ("51",  "4", False, "no TAM markers (Q6)"),
    ("56",  "1", False, "normal imperative construction and normal negator (Q9)"),
    ("59",  "1", False, "neutral alignment in pronouns (Q8)"),
    ("60",  "2", False, "indirect-object ditransitive (Tier 3 cleanup 4)"),
    ("61",  "2", False, "S-V-theme-recipient: `I give book to he`"),
    ("64",  "2", False, "no expletive subject (Tier 3)"),
    ("71",  "2", False, "'and' differentiated from comitative 'with' (Tier 3)"),
    ("72",  "1", False, "one overt 'and' for nouns and clauses (Tier 3)"),
    ("73",  "1", False, "invariant copula with predicate nominals (Tier 3)"),
    ("74",  "1", False, "invariant copula with predicate adjectives - overrides 8 of 9 "
                        "restricted pidgins (Tier 3)"),
    ("75",  "1", False, "invariant copula with predicate locatives (Tier 3)"),
    ("77",  "1", False, "transitive 'have' (Tier 3)"),
    ("78",  "2", False, "existential (the copula) differentiated from 'have' (Tier 3)"),
    ("84",  "2", False, "no directional serials (Tier 3 cleanup 1)"),
    ("85",  "5", False, "no 'take' serials (Tier 3 cleanup 1)"),
    ("86",  "4", False, "no 'give' serials (Tier 3 cleanup 1)"),
    ("87",  "6", False, "dedicated invariant reflexive pronoun (Q8)"),
    ("90",  "2", True,  "passive without verbal coding - preverbal free `self`. Could be "
                        "coded 1 ('typical passive'); this code is 30 European to 1 "
                        "non-European in APiCS and the choice matters (Tier 3 cleanup 2a)"),
    ("92",  "2", False, "relative particle + gap, subject relatives (Tier 3)"),
    ("93",  "2", False, "relative particle + gap, object relatives (Tier 3)"),
    ("95",  "3", False, "complementizer unrelated to 'say' (it is the relativizer)"),
    ("96",  "3", False, "complementizer unrelated to 'say'"),
    ("100", "2", False, "negative particle (Q9)"),
    ("101", "1", False, "standard negation before the verb (Q9)"),
    ("102", "1", False, "indefinites co-occur with predicate negation - `not come "
                        "any-person` (Q9)"),
    ("103", "3", False, "initial question particle (Q10)"),
    ("106", "1", True,  "'also' precedes its host by the modifier rule - but we declined "
                        "to have a focus PARTICLE at all (Tier 5 9), so this codes an "
                        "ordinary adverb into a focus-particle feature"),
    ("107", "5", False, "no vocative marker (Tier 5 10)"),
]

APICS_DELIBERATELY_UNMAPPED = {
    "25": "plural word vs 3PL pronoun identity - explicitly left to the lexicon (Q8)",
    "88": "intensifiers vs reflexives - never decided (PART 3)",
    "89": "RECIPROCAL CONSTRUCTIONS - never decided (PART 3)",
    "104": "focusing of the NP - every code names a construction; we have none, and "
           "APiCS offers no 'no dedicated focus construction' value",
    "44": "internal order of TAM markers - we have no TAM markers to order",
}


# ---- named comparison sets ------------------------------------------------
# Glottocodes.  Grambank has no German, Spanish, Yoruba, Bengali or Persian at
# all; those absences are reported rather than substituted.
SPOTLIGHT = {
    "mand1415": "Mandarin", "hind1269": "Hindi", "swah1253": "Swahili",
    "indo1316": "Indonesian", "nucl1643": "Japanese", "stan1318": "Standard Arabic",
    "egyp1253": "Egyptian Arabic", "nucl1301": "Turkish", "stan1293": "English",
    "stan1290": "French", "russ1263": "Russian", "kore1280": "Korean",
    "viet1252": "Vietnamese", "thai1261": "Thai", "taga1270": "Tagalog",
    "nucl1417": "Igbo", "akan1250": "Akan", "haus1257": "Hausa",
    "zulu1248": "Zulu", "ewee1241": "Ewe", "tami1289": "Tamil",
    "nucl1310": "Burmese", "java1254": "Javanese", "mara1378": "Marathi",
}
MISSING_FROM_GRAMBANK = ["German", "Spanish", "Yoruba", "Bengali", "Persian",
                         "Punjabi (Eastern is present, Standard is not)"]

# Standard Average European.  Haspelmath's (2001) nucleus is French, German,
# Dutch, northern Italian and Romansh; German is absent from Grambank, so the
# nucleus here is four languages and that is stated in the write-up.
SAE_NUCLEUS = {"stan1290": "French", "dutc1256": "Dutch", "ital1282": "Italian",
               "roma1326": "Romansh"}
SAE_WIDE = dict(SAE_NUCLEUS, **{
    "stan1293": "English", "port1283": "Portuguese", "stan1289": "Catalan",
    "occi1239": "Occitan", "gali1258": "Galician", "dani1285": "Danish",
    "swed1254": "Swedish", "icel1247": "Icelandic", "mode1248": "Modern Greek",
    "czec1258": "Czech", "poli1260": "Polish", "russ1263": "Russian",
    "ukra1253": "Ukrainian", "sout1528": "Serbian-Croatian-Bosnian",
    "lith1251": "Lithuanian", "latv1249": "Latvian", "hung1274": "Hungarian",
    "nort2671": "Northern Tosk Albanian", "west2354": "Western Frisian",
})

# Contact languages that Grambank codes.  Glottolog - and therefore Grambank -
# classifies a creole INSIDE its lexifier's family (Haitian is Indo-European,
# Tok Pisin is Indo-European), so they have to be pulled out by hand or they
# inflate whichever family lent them their words.  The first 14 are the APiCS
# overlap grammar-tier0.md 2.1 used; the last 5 are contact languages Grambank
# codes that APiCS does not.  Tetun Dili is deliberately EXCLUDED: it is a
# contact-influenced Austronesian variety, not a creole, and including it would
# be the kind of "a feature name is not a feature definition" error this project
# has made twice already.
CONTACT_IN_GB = {
    "ambo1250": "Ambonese Malay", "baba1267": "Baba Malay",
    "baha1260": "Bahamas Creole English", "berb1259": "Berbice Creole Dutch",
    "bisl1239": "Bislama", "hait1244": "Haitian",
    "jama1262": "Jamaican Creole English", "ling1263": "Kinshasa Lingala",
    "nubi1253": "Nubi", "sana1297": "San Andres Creole English",
    "sara1340": "Saramaccan", "sril1245": "Sri Lanka Malay",
    "suda1237": "South Sudanese Creole Arabic", "tokp1240": "Tok Pisin",
    "beli1260": "Belize Kriol English", "nica1252": "Nicaragua Creole English",
    "limo1249": "Limonese Creole", "piji1239": "Pijin",
    "torr1261": "Torres Strait-Lockhart River Creole",
}
CONTACT_IN_APICS_TOO = {"ambo1250", "baba1267", "baha1260", "berb1259", "bisl1239",
                        "hait1244", "jama1262", "ling1263", "nubi1253", "sana1297",
                        "sara1340", "sril1245", "suda1237", "tokp1240"}


# ===========================================================================
# PART 2 table.  Each row names the decision, the source feature, the figure the
# write-up quoted, and (where the feature is in a database we hold) how to
# re-measure it here so the audit does not merely repeat the write-up.
# recheck = (source, feature_id, value_selector) where value_selector picks the
# option(s) whose share is the population the decision overrode.
# ===========================================================================
OVERRIDES = [
    dict(decision="No politeness distinction in pronouns",
         note="grammar-tier2-pronouns.md 3; confirmed system-wide, grammar-tier45.md 13",
         quoted=85.0, source="wals", feature="45A",
         against=["Binary politeness distinction", "Multiple politeness distinctions",
                  "Pronouns avoided for politeness"],
         reason="an obligatory social judgment on every utterance addressed to a "
                "person: highest frequency and highest cost of error of any "
                "obligatory category. Stays expressible lexically (titles)."),
    dict(decision="No gender in pronouns",
         note="grammar-tier2-pronouns.md 2", quoted=77.9, source="wals", feature="44A",
         against=["3rd person singular only", "3rd person only, but also non-singular",
                  "In 3rd person + 1st and/or 2nd person",
                  "1st or 2nd person but not 3rd", "3rd person non-singular only"],
         reason="the learning burden is one-directional: a gendered-system speaker "
                "loses a nuance, a genderless-system speaker acquires an obligatory "
                "judgment. Rule 2 LOST 9 / KEPT 2 / GAINED 1."),
    dict(decision="No pro-drop - the subject is obligatory",
         note="grammar-tier3-cleanup.md 3", quoted=66.9, source="grambank",
         feature="GB522", against=["1"],
         reason="nothing could recover the dropped subject (no agreement), and it "
                "would collide with the imperative, which Q9 made a bare subjectless "
                "verb phrase."),
    dict(decision="The prohibitive uses the ordinary negator",
         note="grammar-tier2-negation.md 3", quoted=54.7, source="wals", feature="71A",
         against=["Normal imperative + special negative",
                  "Special imperative + special negative"],
         reason="7 of 8 restricted pidgins use the ordinary negator; saves a word and "
                "a rule. The weakest call in Q9."),
    dict(decision="No numeral classifiers",
         note="grammar-tier2-np.md 4.3", quoted=36.4, source="grambank",
         feature="GB057", against=["1"],
         reason="68 of 72 contact languages have none, including 9 of 9 expanded "
                "pidgins. The clearest case of the two objectives pulling apart."),
    dict(decision="No serial verb constructions",
         note="grammar-tier3-cleanup.md 1", quoted=48.4, source="grambank",
         feature="GB118", against=["1"],
         reason="everything they do is available from coordination, prepositions and "
                "the indirect-object construction, and a learner would have to work "
                "out argument sharing with nothing marking it."),
    dict(decision="A relativizer, not the bare gap",
         note="grammar-tier3-combination.md 3", quoted=65.4, source="wals",
         feature="122A", against=["Gap"],
         reason="gap-strategy languages have case, agreement or verb morphology to "
                "mark the clause edge; we have none, and the clause follows the noun."),
    dict(decision="No comparative degree marker ('more', '-er')",
         note="grammar-tier3-combination.md 2", quoted=56.7, source="grambank",
         feature="GB276", against=["1"],
         reason="the 'than' phrase already signals the comparison; 6 of 9 restricted "
                "pidgins leave the adjective unmarked. One word saved."),
    dict(decision="No 'exceed' comparative",
         note="grammar-tier3-combination.md 2", quoted=41.5, source="grambank",
         feature="GB265", against=["1"],
         reason="downstream of the copula: `I COP tall exceed you` is two predicates "
                "in one clause, which is serial-verb machinery we rejected. Overrides "
                "7 of 9 expanded pidgins."),
    dict(decision="No clusivity",
         note="grammar-tier2-pronouns.md 1", quoted=37.3, source="grambank",
         feature="GB028", against=["1"],
         reason="a majority by language count (52.6%) and a minority by people; "
                "9 of 9 restricted pidgins lack it. Included because the by-language "
                "majority makes it look like an override and by people it is not."),
    dict(decision="Adjectives take the copula, they are not stative verbs",
         note="grammar-tier3-predication.md 2", quoted=43.7, source="grambank",
         feature="GB068", against=["1"],
         reason="overrides the strongest single pidgin signal in the project (8 of 9). "
                "Stative adjectives would break attributive order: if 'big' is a verb, "
                "`big house` is a relative clause, which Tier 0 puts AFTER the noun."),
    dict(decision="No dual",
         note="grammar-tier2-pronouns.md 1", quoted=1.4, source="grambank",
         feature="GB031", against=["1"],
         reason="26.3% of languages, 1.4% of L1. The cheapest rejection in the project "
                "- listed to show the bottom of the ranking."),
]

# The one that has to be told as a process story rather than a number.
PASSIVE_REVERSAL = dict(
    decision="A passive: preverbal `self`",
    note="grammar-tier3-cleanup.md 2 and 2a",
    reason="REJECTED ON A FALSE PREMISE, THEN REVERSED. The rejection reasoned "
           "'a passive needs verb morphology or a participle and we have neither' "
           "straight to 'impossible' without checking what strategies fit inside our "
           "constraints. GB302 refutes it: a phonologically FREE passive marker is "
           "10.5% of languages but 64.6% of L1, Mandarin bei being the model. Had the "
           "rejection stood it would have been the largest population override in the "
           "project.",
    check_wals="107A", check_gb="GB302")


# ===========================================================================
# machinery
# ===========================================================================
def gb_frame(l1m, tot) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Grambank as a (glottocode x feature) value matrix, plus language metadata."""
    langs, _p, vals = load("grambank")
    langs = langs[langs.level == "language"].copy()
    vals = vals[vals.Language_ID.isin(set(langs.ID))]
    langs = weight(langs, l1m, tot)
    k = langs.set_index("ID")
    v = vals[vals.Value.astype(str) != "?"].copy()
    v["gc"] = v.Language_ID.map(k.Glottocode)
    v = v[v.gc.notna()].drop_duplicates(["gc", "Parameter_ID"])
    mat = v.pivot(index="gc", columns="Parameter_ID", values="Value").astype("string")
    meta = (langs[langs.Glottocode.notna()].drop_duplicates("Glottocode")
            .set_index("Glottocode")[["Name", "Family_name", "Macroarea", "l1", "total"]])
    meta = meta.reindex(mat.index)
    # creoles sit inside their lexifier's family in Glottolog; pull them out
    meta["group"] = ["contact language" if g in CONTACT_IN_GB else f
                     for g, f in zip(meta.index, meta.Family_name.fillna("(isolate)"))]
    return mat, meta


def score(mat: pd.DataFrame, vec: dict[str, str]) -> pd.DataFrame:
    """Agreement of every row of `mat` with `vec`, over the features both define."""
    cols = [c for c in vec if c in mat.columns]
    sub = mat[cols]
    arr = sub.fillna("").to_numpy(dtype=str)
    defined = arr != ""
    tgt = np.array([vec[c] for c in cols], dtype=str)
    same = (arr == tgt) & defined
    n = defined.sum(axis=1)
    with np.errstate(invalid="ignore"):
        agr = same.sum(axis=1) / np.where(n == 0, np.nan, n)
    return pd.DataFrame({"n_shared": n, "n_agree": same.sum(axis=1),
                         "agreement": agr}, index=sub.index)


def weighted_mean(df: pd.DataFrame, wcol: str) -> float:
    w = df[wcol].fillna(0.0)
    return float((df.agreement * w).sum() / w.sum()) if w.sum() else float("nan")


def pair_baseline(mat: pd.DataFrame, cols: list[str], n_pairs: int,
                  min_shared: int) -> np.ndarray:
    """Agreement between two randomly drawn real languages on the same features."""
    rng = np.random.default_rng(RNG_SEED)
    sub = mat[cols]
    arr = sub.fillna("").to_numpy(dtype=str)
    ok = arr != ""
    idx = np.arange(len(sub))
    a = rng.choice(idx, n_pairs)
    b = rng.choice(idx, n_pairs)
    keep = a != b
    a, b = a[keep], b[keep]
    both = ok[a] & ok[b]
    n = both.sum(axis=1)
    eq = (arr[a] == arr[b]) & both
    with np.errstate(invalid="ignore"):
        r = eq.sum(axis=1) / np.where(n == 0, np.nan, n)
    return r[n >= min_shared]


def apics_number_to_value(codes: pd.DataFrame) -> dict[tuple[str, str], str]:
    """(parameter, display Number) -> the string that appears in values.csv."""
    out = {}
    for r in codes.itertuples():
        out[(str(r.Parameter_ID), str(r.Number))] = str(r.ID).split("-")[-1]
    return out


def banner(s: str) -> None:
    print("\n" + "=" * 78 + f"\n{s}\n" + "=" * 78)


# ===========================================================================
def main() -> None:
    (l1m, tot, W1, WT) = populations()
    rows: list[dict] = []

    vec = {f: v for f, v, _c, _r in INTERLANG_GB}
    contested = {f for f, _v, c, _r in INTERLANG_GB if c}
    print(f"interlang encoded on {len(vec)} Grambank features "
          f"({sum(v == '1' for v in vec.values())} positive, "
          f"{sum(v == '0' for v in vec.values())} negative, "
          f"{len(contested)} flagged contested)")

    mat, meta = gb_frame(l1m, tot)
    cols = [c for c in vec if c in mat.columns]
    print(f"Grambank: {len(mat)} languages x {len(mat.columns)} features; "
          f"{len(cols)} of our {len(vec)} features are in it")

    s = score(mat, vec).join(meta)
    ranked = s[s.n_shared >= MIN_SHARED].copy()
    print(f"{len(ranked)} languages share >= {MIN_SHARED} features and are rankable "
          f"(median shared {int(ranked.n_shared.median())})")

    # ---------------- baselines ------------------------------------------
    banner("PART 1a  CALIBRATION - what does an agreement number mean here?")
    zero_vec = {c: "0" for c in cols}
    mode_vec = {c: mat[c].mode().iloc[0] for c in cols if mat[c].notna().any()}
    # the population-optimal fixed vector: per feature, the value the most PEOPLE
    # have.  This is the ceiling any single designed grammar could reach on the
    # by-L1 column, and it is the number interlang should be judged against,
    # because principles.md 2 counts people.
    l1mode_vec = {}
    for c in cols:
        col = mat[c].dropna()
        if not len(col):
            continue
        w = meta.l1.reindex(col.index).fillna(0.0)
        l1mode_vec[c] = w.groupby(col).sum().idxmax()
    z = score(mat, zero_vec).join(meta)
    z = z[z.n_shared >= MIN_SHARED]
    m = score(mat, mode_vec).join(meta)
    m = m[m.n_shared >= MIN_SHARED]
    lm = score(mat, l1mode_vec).join(meta)
    lm = lm[lm.n_shared >= MIN_SHARED]
    n_diff = sum(1 for c in l1mode_vec if vec.get(c) != l1mode_vec[c])
    pairs = pair_baseline(mat, cols, N_PAIRS, MIN_SHARED)

    cal = pd.DataFrame([
        dict(vector="INTERLANG", by_language=ranked.agreement.mean(),
             by_L1=weighted_mean(ranked, "l1"), by_total=weighted_mean(ranked, "total")),
        dict(vector="all-zero (a language with none of these features)",
             by_language=z.agreement.mean(), by_L1=weighted_mean(z, "l1"),
             by_total=weighted_mean(z, "total")),
        dict(vector="all-mode (the majority value of every feature, by LANGUAGE)",
             by_language=m.agreement.mean(), by_L1=weighted_mean(m, "l1"),
             by_total=weighted_mean(m, "total")),
        dict(vector="all-mode by L1 (the population-OPTIMAL fixed vector = ceiling)",
             by_language=lm.agreement.mean(), by_L1=weighted_mean(lm, "l1"),
             by_total=weighted_mean(lm, "total")),
        dict(vector=f"random real language pair (n={len(pairs)})",
             by_language=float(np.nanmean(pairs)), by_L1=float("nan"),
             by_total=float("nan")),
    ])
    print(cal.round(3).to_string(index=False))
    print(f"\ninterlang differs from the population-optimal vector on {n_diff} of "
          f"{len(l1mode_vec)} features. Those {n_diff} are the whole of the "
          f"population cost of the grammar; they are listed in PART 1f and PART 2.")
    print(f"\nlanguage-pair baseline: median {np.nanmedian(pairs):.3f}, "
          f"90th pct {np.nanpercentile(pairs, 90):.3f}, "
          f"99th pct {np.nanpercentile(pairs, 99):.3f}, max {np.nanmax(pairs):.3f}")
    print(f"interlang's mean agreement sits at the "
          f"{100 * (pairs < ranked.agreement.mean()).mean():.1f}th percentile "
          f"of the real-language-pair distribution.")
    for _i, r in cal.iterrows():
        rows.append(dict(part="calibration", database="grambank", entity=r.vector,
                         agreement=round(r.by_language, 4), by_L1=round(r.by_L1, 4)
                         if pd.notna(r.by_L1) else None))

    # ---------------- nearest and furthest ---------------------------------
    banner("PART 1b  NEAREST AND FURTHEST LANGUAGES")
    show = ["Name", "group", "Macroarea", "n_shared", "agreement", "l1M"]
    ranked["l1M"] = (ranked.l1 / 1e6).round(1)
    print("\n--- 25 MOST similar to interlang ---")
    print(ranked.nlargest(25, "agreement")[show].to_string(index=False))
    print("\n--- 15 LEAST similar to interlang ---")
    print(ranked.nsmallest(15, "agreement")[show].to_string(index=False))
    print("\n--- 20 most similar among the 60 largest languages by L1 ---")
    big = ranked.nlargest(60, "l1")
    print(big.nlargest(20, "agreement")[show].to_string(index=False))
    print("\n--- and the 10 LEAST similar among those 60 ---")
    print(big.nsmallest(10, "agreement")[show].to_string(index=False))
    for gc, r in ranked.iterrows():
        rows.append(dict(part="language", database="grambank", entity=r.Name,
                         glottocode=gc, family=r.Family_name, group=r.group,
                         macroarea=r.Macroarea, l1=r.l1, n_shared=int(r.n_shared),
                         agreement=round(r.agreement, 4)))

    # ---------------- by family and macroarea ------------------------------
    banner("PART 1c  BY FAMILY AND BY MACROAREA - languages vs people")
    for key, label, minn in (("group", "family (contact languages pulled out)", 8),
                             ("Macroarea", "macroarea", 1)):
        g = (ranked.groupby(key)
             .apply(lambda d: pd.Series({
                 "n_lang": len(d),
                 "by_language": d.agreement.mean(),
                 "by_L1": weighted_mean(d, "l1"),
                 "L1_Mn": d.l1.sum() / 1e6}), include_groups=False)
             .sort_values("by_language", ascending=False))
        g = g[g.n_lang >= minn]
        print(f"\n--- {label} (n >= {minn}) ---")
        print(g.round(3).to_string())
        for name, r in g.iterrows():
            rows.append(dict(part=f"by_{key}", database="grambank", entity=name,
                             n_shared=int(r.n_lang), agreement=round(r.by_language, 4),
                             by_L1=round(r.by_L1, 4), l1=r.L1_Mn * 1e6))

    # ---------------- named languages --------------------------------------
    banner("PART 1d  THE LANGUAGES A READER WILL ASK ABOUT")
    spot = ranked.loc[[g for g in SPOTLIGHT if g in ranked.index]].copy()
    spot["label"] = [SPOTLIGHT[g] for g in spot.index]
    spot["pctile"] = [round(100 * (ranked.agreement < a).mean())
                      for a in spot.agreement]
    print(spot.sort_values("agreement", ascending=False)
          [["label", "group", "n_shared", "agreement", "pctile", "l1M"]]
          .to_string(index=False))
    print("`pctile` = where that language sits in the distribution of all 2,299 "
          "Grambank languages' agreement with interlang.")
    print(f"\nNOT IN GRAMBANK AT ALL: {', '.join(MISSING_FROM_GRAMBANK)}")
    for gc, r in spot.iterrows():
        rows.append(dict(part="spotlight", database="grambank", entity=r.label,
                         glottocode=gc, n_shared=int(r.n_shared),
                         agreement=round(r.agreement, 4), l1=r.l1))

    print("\n--- Standard Average European ---")
    for name, st in (("SAE nucleus (Haspelmath, minus German: absent)", SAE_NUCLEUS),
                     ("SAE wide (western + central Europe)", SAE_WIDE)):
        got = ranked.loc[[g for g in st if g in ranked.index]]
        miss = [st[g] for g in st if g not in ranked.index]
        pct = 100 * (ranked.agreement < got.agreement.mean()).mean()
        print(f"{name}: n={len(got)}, mean agreement {got.agreement.mean():.3f} "
              f"(the {pct:.0f}th percentile of all Grambank languages), "
              f"L1-weighted {weighted_mean(got, 'l1'):.3f}"
              + (f"  [missing: {', '.join(miss)}]" if miss else ""))
        print("   " + "; ".join(f"{st[g]} {got.loc[g].agreement:.3f}"
                                for g in got.index))
        rows.append(dict(part="spotlight-set", database="grambank", entity=name,
                         n_shared=len(got), agreement=round(got.agreement.mean(), 4),
                         by_L1=round(weighted_mean(got, "l1"), 4)))

    # ---------------- contact languages in Grambank ------------------------
    banner("PART 1e  DID WE LAND NEAR THE CONTACT LANGUAGES? (Grambank half)")
    con = ranked.loc[[g for g in CONTACT_IN_GB if g in ranked.index]].copy()
    con["label"] = [CONTACT_IN_GB[g] for g in con.index]
    con["in_apics"] = [g in CONTACT_IN_APICS_TOO for g in con.index]
    print(con.sort_values("agreement", ascending=False)
          [["label", "in_apics", "n_shared", "agreement"]].to_string(index=False))
    print(f"\ncontact-language mean {con.agreement.mean():.3f} vs "
          f"world by-language mean {ranked.agreement.mean():.3f} "
          f"(difference {con.agreement.mean() - ranked.agreement.mean():+.3f})")
    print(f"contact languages occupy percentile "
          f"{100 * (ranked.agreement < con.agreement.mean()).mean():.0f} of the "
          f"world agreement distribution.")
    print(f"NOTE: n={len(con)}, of which {int(con.in_apics.sum())} are the APiCS "
          "overlap grammar-tier0.md 2.1 used. Grambank codes creoles inside their "
          "lexifier's family, so this group had to be pulled out by hand. The APiCS "
          "run below is the larger contact test.")
    for gc, r in con.iterrows():
        rows.append(dict(part="contact-grambank", database="grambank", entity=r.label,
                         glottocode=gc, n_shared=int(r.n_shared),
                         agreement=round(r.agreement, 4)))

    # ---------------- per-feature world agreement --------------------------
    feat_rows = []
    for f, v, c, why in INTERLANG_GB:
        if f not in mat.columns:
            feat_rows.append(dict(feature=f, interlang=v, contested=c, rationale=why,
                                  n=0, pct_lang=None, pct_L1=None))
            continue
        col = mat[f].dropna()
        w = meta.l1.reindex(col.index).fillna(0.0)
        hit = col == v
        feat_rows.append(dict(
            feature=f, interlang=v, contested=c, rationale=why, n=len(col),
            pct_lang=round(100 * hit.mean(), 1),
            pct_L1=round(100 * w[hit].sum() / w.sum(), 1) if w.sum() else None))
    fdf = pd.DataFrame(feat_rows)
    fdf["popular_value"] = [l1mode_vec.get(f) for f in fdf.feature]
    fdf["costs_population"] = fdf.interlang != fdf.popular_value
    banner("PART 1f  PER-FEATURE: how many people already have OUR value?")
    cost = fdf[fdf.costs_population].sort_values("pct_L1")
    print(f"\n--- the {len(cost)} features where interlang differs from the value the "
          f"most PEOPLE have ---")
    print(cost[["feature", "interlang", "popular_value", "pct_L1", "rationale"]]
          .to_string(index=False, max_colwidth=60))
    print("\n--- the 20 features where we agree with the FEWEST people ---")
    print(fdf.dropna(subset=["pct_L1"]).nsmallest(20, "pct_L1")
          [["feature", "interlang", "n", "pct_lang", "pct_L1", "rationale"]]
          .to_string(index=False, max_colwidth=58))
    print(f"\nunweighted mean over encoded features: by language "
          f"{fdf.pct_lang.mean():.1f}%, by L1 {fdf.pct_L1.mean():.1f}%")

    # ---------------- sensitivity to the contested codings -----------------
    banner("PART 1g  SENSITIVITY - flip every contested coding at once")
    flip = dict(vec)
    for f in contested:
        if vec[f] in ("0", "1"):
            flip[f] = "1" if vec[f] == "0" else "0"
    s2 = score(mat, flip).join(meta)
    r2 = s2[s2.n_shared >= MIN_SHARED]
    print(f"{len(contested)} contested features flipped.")
    print(f"  by-language mean  {ranked.agreement.mean():.3f} -> {r2.agreement.mean():.3f}")
    print(f"  by-L1 mean        {weighted_mean(ranked, 'l1'):.3f} -> "
          f"{weighted_mean(r2, 'l1'):.3f}")
    top1 = ranked.nlargest(10, "agreement").Name.tolist()
    top2 = r2.join(meta[["Name"]], rsuffix="_x").nlargest(10, "agreement").Name.tolist()
    print(f"  top-10 nearest languages, overlap {len(set(top1) & set(top2))}/10")
    print(f"    baseline: {', '.join(top1[:6])}")
    print(f"    flipped : {', '.join(top2[:6])}")
    for label, keys in (("SAE wide", SAE_WIDE), ("contact languages", CONTACT_IN_GB),
                        ("Mandarin", {"mand1415": ""}), ("Hindi", {"hind1269": ""}),
                        ("English", {"stan1293": ""})):
        ks = [g for g in keys if g in ranked.index and g in r2.index]
        print(f"  {label:20s} {ranked.loc[ks].agreement.mean():.3f} -> "
              f"{r2.loc[ks].agreement.mean():.3f}")
    rows.append(dict(part="sensitivity", database="grambank",
                     entity="all contested flipped",
                     agreement=round(r2.agreement.mean(), 4),
                     by_L1=round(weighted_mean(r2, "l1"), 4)))

    # =======================================================================
    banner("PART 1h  THE SHARPEST TEST - APiCS, the contact languages we designed from")
    ap_l, _ap_p, ap_v = load("apics")
    ap_l = ap_l.copy()
    ap_l["ctype"] = [contact_type(n) for n in ap_l.Name]
    ap_l["grp"] = ""
    acodes = pd.read_csv(ROOT / "data/raw/apics/cldf/codes.csv")
    cmap = dict(zip(acodes.ID, acodes.Name))
    n2v = apics_number_to_value(acodes)
    avec, alabel = {}, {}
    for p, num, _c, _r in INTERLANG_APICS:
        val = n2v.get((p, num))
        if val is None:
            print(f"  ! APiCS {p}: no code with Number {num}; dropped")
            continue
        avec[p] = val
        alabel[p] = cmap.get(f"{p}-{val}", "?")
    av = ap_v[ap_v.Parameter_ID.astype(str).isin(avec)].copy()
    av["pid"] = av.Parameter_ID.astype(str)
    # APiCS Value is int64; cast BEFORE the pivot, or the NaN-widened float column
    # stringifies to "2.0" and never matches "2".  (This scored every language at
    # zero the first time it was run.)
    av["val"] = av.Value.astype(str)
    av = (av.sort_values("Frequency", ascending=False)
          .drop_duplicates(["Language_ID", "pid"]))
    amat = av.pivot(index="Language_ID", columns="pid", values="val").astype("string")
    ameta = ap_l.set_index("ID")[["Name", "ctype", "Lexifier", "Region"]].reindex(amat.index)
    amat = amat[~ameta.ctype.eq("0 mixed (excluded)")]
    ameta = ameta.reindex(amat.index)
    acols = [c for c in avec if c in amat.columns]
    print(f"interlang encoded on {len(avec)} APiCS parameters, {len(acols)} present; "
          f"{len(amat)} non-mixed contact lects")

    asc = score(amat, avec).join(ameta)
    ask = asc[asc.n_shared >= MIN_SHARED_APICS].copy()
    apairs = pair_baseline(amat, acols, N_PAIRS, MIN_SHARED_APICS)
    # APiCS has no natural "all-zero" vector (its codes are alternatives, not
    # presence/absence), so the contact-language pair distribution is the only null.

    print(f"\nrankable lects: {len(ask)} (median {int(ask.n_shared.median())} shared)")
    print(f"\nINTERLANG mean agreement with contact languages: {ask.agreement.mean():.3f}")
    print(f"CONTACT LANGUAGES WITH EACH OTHER (the null): mean "
          f"{np.nanmean(apairs):.3f}, median {np.nanmedian(apairs):.3f}, "
          f"90th pct {np.nanpercentile(apairs, 90):.3f}, max {np.nanmax(apairs):.3f}")
    print(f"interlang sits at the {100 * (apairs < ask.agreement.mean()).mean():.1f}th "
          f"percentile of contact-language-to-contact-language similarity.")

    print("\n--- by contact stratum (read the pidgin rows first) ---")
    strat = (ask.groupby("ctype")
             .agg(n=("agreement", "size"), mean=("agreement", "mean"),
                  median=("agreement", "median"), best=("agreement", "max")))
    # within-stratum null: how similar is a restricted pidgin to another restricted
    # pidgin?  This is the fair comparison for "did we land where a pidgin lands".
    nulls = {}
    for ct in strat.index:
        ids = ameta.index[ameta.ctype == ct]
        p = pair_baseline(amat.loc[ids], acols, 4000, MIN_SHARED_APICS)
        nulls[ct] = float(np.nanmean(p)) if len(p) else float("nan")
    strat["within_stratum_null"] = [nulls[i] for i in strat.index]
    print(strat.round(3).to_string())
    print("`within_stratum_null` = mean agreement of two languages of that stratum "
          "with EACH OTHER,\non the same 65 parameters. It is the score interlang "
          "would get if it were an ordinary\nmember of that stratum.")
    print("\n--- by lexifier ---")
    lex = (ask.groupby("Lexifier")
           .agg(n=("agreement", "size"), mean=("agreement", "mean"))
           .sort_values("mean", ascending=False))
    print(lex.round(3).to_string())
    print("\n--- 15 nearest contact languages ---")
    print(ask.nlargest(15, "agreement")[["Name", "ctype", "Lexifier", "n_shared",
                                         "agreement"]].to_string(index=False))
    print("\n--- 10 furthest ---")
    print(ask.nsmallest(10, "agreement")[["Name", "ctype", "Lexifier", "n_shared",
                                          "agreement"]].to_string(index=False))
    for lid, r in ask.iterrows():
        rows.append(dict(part="contact-apics", database="apics", entity=r.Name,
                         group=r.ctype, family=r.Lexifier, macroarea=r.Region,
                         n_shared=int(r.n_shared), agreement=round(r.agreement, 4)))
    for name, r in strat.iterrows():
        rows.append(dict(part="apics-stratum", database="apics", entity=name,
                         n_shared=int(r.n), agreement=round(r["mean"], 4)))

    print("\n--- the APiCS parameters where we agree with the FEWEST contact lects ---")
    ar = []
    for p, _num, c, why in INTERLANG_APICS:
        if p not in amat.columns:
            continue
        v = avec[p]
        col = amat[p].dropna()
        ar.append(dict(param=p, interlang=v, label=alabel[p], n=len(col),
                       pct=round(100 * (col == v).mean(), 1),
                       restricted=int(((col == v) & ameta.ctype.eq(
                           "1 restricted pidgin").reindex(col.index).fillna(False)).sum()),
                       n_restricted=int(ameta.ctype.eq("1 restricted pidgin")
                                        .reindex(col.index).fillna(False).sum()),
                       contested=c))
    adf = pd.DataFrame(ar)
    print(adf.nsmallest(18, "pct")[["param", "label", "n", "pct", "restricted",
                                    "n_restricted", "contested"]]
          .to_string(index=False, max_colwidth=52))
    print(f"\nmean over encoded APiCS parameters: {adf.pct.mean():.1f}% of contact "
          f"lects share our value")
    adf.to_csv(ROOT / "data/processed/grammar_bias_audit_apics_features.csv", index=False)

    # =======================================================================
    banner("PART 1  HEADLINE")
    fam = (ranked.groupby("group").agg(n=("agreement", "size"),
                                       a=("agreement", "mean")))
    fam = fam[fam.n >= 8].sort_values("a", ascending=False)
    print("nearest family/group (n>=8):  " +
          "; ".join(f"{i} {r.a:.3f} (n={int(r.n)})" for i, r in fam.head(4).iterrows()))
    print("furthest family/group (n>=8): " +
          "; ".join(f"{i} {r.a:.3f} (n={int(r.n)})" for i, r in fam.tail(3).iterrows()))
    print(f"\nby LANGUAGE  interlang agrees with the average Grambank language on "
          f"{ranked.agreement.mean():.3f} of shared features")
    print(f"by PEOPLE    ... with the average person's native language on "
          f"{weighted_mean(ranked, 'l1'):.3f}, against a ceiling of "
          f"{weighted_mean(lm, 'l1'):.3f} and a floor of {weighted_mean(z, 'l1'):.3f}")
    floor, ceil = weighted_mean(z, "l1"), weighted_mean(lm, "l1")
    got = weighted_mean(ranked, "l1")
    print(f"             i.e. {100 * (got - floor) / (ceil - floor):.0f}% of the way from "
          f"'a language with no features' to the population optimum")
    sae = ranked.loc[[g for g in SAE_WIDE if g in ranked.index]]
    print(f"\nSAE (wide, n={len(sae)})                {sae.agreement.mean():.3f}")
    print(f"Mandarin                        {ranked.loc['mand1415'].agreement:.3f}")
    print(f"contact languages in Grambank   {con.agreement.mean():.3f}  (n={len(con)})")
    print(f"restricted pidgins in APiCS     {strat.loc['1 restricted pidgin', 'mean']:.3f}"
          f"  (n={int(strat.loc['1 restricted pidgin', 'n'])}, on a different feature set, "
          f"against a contact-to-contact null of {np.nanmean(apairs):.3f})")
    print("\nSo: by language count interlang is a MAINLAND-SOUTHEAST-ASIAN-shaped isolating\n"
          "language and is NOT close to Standard Average European; by population it lands\n"
          "well above the featureless floor but short of the population optimum; and within\n"
          "the contact record it is nearest to exactly the stratum the project said to\n"
          "weight most - restricted pidgins.")

    # =======================================================================
    banner("PART 2  THE POPULATION OVERRIDES, RE-MEASURED")
    print("`quoted` is the figure the deciding write-up gave; `measured` is recomputed\n"
          "here from the same feature. They should agree; where they do not, the\n"
          "write-up's number is the one to distrust.\n")
    ov = []
    gb_l1 = meta.l1
    for o in OVERRIDES:
        if o["source"] == "grambank":
            col = mat[o["feature"]].dropna()
            w = gb_l1.reindex(col.index).fillna(0.0)
            hit = col.isin(o["against"])
            pct_l1 = 100 * w[hit].sum() / w.sum()
            pct_lang = 100 * hit.mean()
            n = len(col)
        else:
            d = wals_dist(o["feature"], l1m, tot)
            sel = [i for i in d.index if i in o["against"]]
            if len(sel) != len(o["against"]):
                print(f"  ! WALS {o['feature']}: label mismatch, have {list(d.index)}")
            pct_l1 = d.loc[sel, "by_L1"].sum()
            pct_lang = d.loc[sel, "by_lang"].sum()
            n = int(d.n.sum())
        ov.append(dict(decision=o["decision"], source=f"{o['source']} {o['feature']}",
                       n=n, quoted=o["quoted"], measured_L1=round(pct_l1, 1),
                       measured_lang=round(pct_lang, 1), note=o["note"],
                       reason=o["reason"]))
    ovdf = pd.DataFrame(ov).sort_values("measured_L1", ascending=False)
    print(ovdf[["decision", "source", "n", "quoted", "measured_L1", "measured_lang"]]
          .to_string(index=False))
    for _i, r in ovdf.iterrows():
        rows.append(dict(part="override", database=r.source.split()[0], entity=r.decision,
                         n_shared=r.n, agreement=r.measured_L1, by_L1=r.measured_L1,
                         group=r.measured_lang))

    print("\n--- the one that was reversed ---")
    d = wals_dist(PASSIVE_REVERSAL["check_wals"], l1m, tot)
    print(f"WALS 107A (passive present/absent), n={int(d.n.sum())}:")
    print("  " + d.to_string().replace("\n", "\n  "))
    col = mat["GB302"].dropna()
    w = gb_l1.reindex(col.index).fillna(0.0)
    print(f"GB302 free passive marker: {100 * (col == '1').mean():.1f}% of "
          f"{len(col)} languages, {100 * w[col == '1'].sum() / w.sum():.1f}% of L1")
    print(f"\n{PASSIVE_REVERSAL['reason']}")
    rows.append(dict(part="override-reversed", database="wals",
                     entity=PASSIVE_REVERSAL["decision"],
                     agreement=float(d.loc["Present", "by_L1"]) if "Present" in d.index
                     else None))

    # =======================================================================
    banner("PART 3  WHAT DID WE NEVER DECIDE? (the unmapped-feature scan)")
    _gl, gb_p, _gv = load("grambank")
    names = dict(zip(gb_p.ID, gb_p.Name))
    unmapped = [f for f in mat.columns if f not in vec]
    known = set(GB_DELIBERATELY_UNMAPPED)
    print(f"{len(unmapped)} of {len(mat.columns)} Grambank features carry no interlang "
          f"value.\n{len(known & set(unmapped))} of those are already triaged in this "
          f"script's GB_DELIBERATELY_UNMAPPED; the rest are printed for hand triage.\n")
    print("--- already triaged ---")
    for f in sorted(known & set(unmapped)):
        print(f"  {f}  {names.get(f, '?')[:74]}\n        -> {GB_DELIBERATELY_UNMAPPED[f]}")
    print("\n--- NOT triaged: read every line ---")
    for f in sorted(set(unmapped) - known):
        col = mat[f].dropna()
        w = gb_l1.reindex(col.index).fillna(0.0)
        pos = col.isin(["1"])
        print(f"  {f}  ({100 * pos.mean():4.1f}% lang / "
              f"{100 * w[pos].sum() / w.sum() if w.sum() else 0:4.1f}% L1)  "
              f"{names.get(f, '?')[:70]}")
        rows.append(dict(part="unmapped", database="grambank", entity=f,
                         group=names.get(f, ""), agreement=round(100 * pos.mean(), 1),
                         by_L1=round(100 * w[pos].sum() / w.sum(), 1) if w.sum() else None))
    print("\n--- MAPPED, but by ENTAILMENT rather than by a decision anyone took ---")
    print("(rationale contains 'never decided' or 'entailed'; these are commitments "
          "the grammar has\nwithout a write-up behind them, which is exactly the class "
          "the Tier 3 cleanup found)")
    for f, v, _c, why in INTERLANG_GB:
        if "never" in why.lower() or "entailed" in why.lower():
            row = fdf[fdf.feature == f].iloc[0]
            print(f"  {f} = {v}  ({row.pct_lang}% lang / {row.pct_L1}% L1)  "
                  f"{names.get(f, '?')[:62]}\n        -> {why}")
            rows.append(dict(part="unchosen", database="grambank", entity=f,
                             group=names.get(f, ""), agreement=row.pct_lang,
                             by_L1=row.pct_L1))

    print("\n--- APiCS parameters deliberately unmapped ---")
    for p, why in APICS_DELIBERATELY_UNMAPPED.items():
        print(f"  APiCS {p}: {why}")
    print("\nNOT CODED BY ANY SOURCE WE HOLD, and therefore not measurable here:")
    for line in ("satellite- vs verb-framing of motion events (Talmy) - "
                 "lexicon-plan.md 4.5 checked and found no database coding it",
                 "topicalization / fronting for information structure - Grambank codes "
                 "no word-order-flexibility feature and APiCS 104 codes only clefts",
                 "whether the polar question particle also appears in content questions "
                 "(grammar-tier2-questions.md 5)",
                 "yes/no answering the fact vs the question's polarity (Tier 5 7)",
                 "proper-name classification (Tier 5 14)",
                 "ellipsis under coordination (Tier 5 11)"):
        print(f"  - {line}")

    # =======================================================================
    fdf.to_csv(OUT_FEAT, index=False)
    pd.DataFrame(rows).to_csv(OUT, index=False)
    print(f"\nwrote {OUT}\nwrote {OUT_FEAT}")
    print(f"wrote {ROOT / 'data/processed/grammar_bias_audit_apics_features.csv'}")


if __name__ == "__main__":
    main()
