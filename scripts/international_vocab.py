"""International (Latin/Greek + Wanderwort) vocabulary under candidate syllable templates.

Answers two questions for principles.md 3.6 (syllable template, OPEN):

  (A) RECOGNIZABILITY - do internationally shared words survive projection into
      our phonology (3.3, FIRM) under each candidate template?
  (B) PREDICTABILITY  - is there a deterministic, learnable, ideally invertible
      path from the international form to our form?

Pipeline
--------
1. WORDS below: 52 hand-picked international items (selection policy documented
   in notes/international-vocab.md 2 and in the `why` field of every row).
2. Attested renderings are fetched from the **Wikipedia langlinks API** (the
   article title of the same concept in each of 18 recipient languages) and
   cached under data/raw/wikipedia_langlinks/.  Non-Latin scripts are
   romanised/phonemicised by the tables in this file.
3. Each attested form is classified LOAN vs NATIVE/CALQUE by similarity to the
   international form (metric v0), which is the evidence for the premise check
   ("does every language except Chinese adapt the Latin/Greek root?").
4. interlang.translit renders each word under six phonotactic variants.
5. Every rendering is scored against the attested LOAN forms with metric v0,
   alongside syllable counts and length inflation.

Output: data/processed/international_vocab.csv, one row per word x variant.

DATA PROVENANCE - READ THIS
---------------------------
Three provenance classes, carried per attested form in the `provenance` column
of the long-form CSV and summarised in the study CSV:

  `wikipedia`    - the langlink title, verbatim from the cached API response.
                   Sourced, reproducible, citable.
  `model-recall` - a form supplied from the author model's own knowledge, used
                   ONLY where the Wikipedia title is a purist/calque form but
                   the everyday spoken word in that language is a loan (Hindi
                   and Tamil especially).  These are flagged, reported
                   separately, and NEVER used in the headline numbers.
  `derived`      - a romanisation/phonemicisation of one of the above.

The romanisation and phonemicisation tables in this file are ROUGH.  They are
hand-written approximations, not a validated transliteration standard; Arabic
and Hebrew in particular are abjads whose short vowels are unwritten, so their
romanised forms are consonant skeletons.  Consequences, all documented in
notes/international-vocab.md 3:
  - ar/he are used for the premise check (loan vs calque, judged on the
    consonant skeleton) but EXCLUDED from the recognizability scoring.
  - absolute similarity levels are noisy; VARIANT COMPARISONS are safe, because
    every variant is scored against exactly the same attested targets, so
    romanisation error is a constant offset shared by all six variants.

METRIC CAVEAT (principles.md 4, known issue 2)
----------------------------------------------
The recognizability metric has NO WORKING EPENTHESIS MODEL.  Inserting a repair
vowel is charged at nearly full price, so the metric SYSTEMATICALLY FLATTERS
PERMISSIVE CODAS: every metric-based comparison in this study is biased in
favour of V4/V5 and against V1/V2/V3.  The counterweight is non-metric:
syllable inflation and length inflation, reported side by side and prominently.
Read them together; the metric alone will always recommend the most permissive
template.

Usage: uv run python scripts/international_vocab.py [--offline] [--quick]
  --offline  do not hit the network; rebuild from the cached langlink JSON
  --quick    skip the ambiguity-arm sensitivity runs (faster)
Inputs:  data/raw/wikipedia_langlinks/*.json (fetched on first run)
Outputs: data/processed/international_vocab.csv       (word x variant)
         data/processed/international_vocab_forms.csv (word x language, attested)
"""

from __future__ import annotations

import json
import sys
import time
import unicodedata
from pathlib import Path

import pandas as pd
import requests

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

RAW_DIR = ROOT / "data" / "raw" / "wikipedia_langlinks"
OUT_CSV = ROOT / "data" / "processed" / "international_vocab.csv"
OUT_FORMS = ROOT / "data" / "processed" / "international_vocab_forms.csv"

API = "https://en.wikipedia.org/w/api.php"
USER_AGENT = "interlang-research/0.1 (https://github.com/pthill; kevin.patrick.thill@gmail.com)"

# ---------------------------------------------------------------------------
# Recipient languages.  Selection policy: the 14 languages named in the study
# brief (typological + geographic spread, all with large speaker populations),
# plus he/is/hu/cs because they are the *expected complications* for the
# premise check - the known purist / calquing traditions.
# ---------------------------------------------------------------------------
LANGS = {
    "ja": ("Japanese", "japanese"),
    "zh": ("Mandarin", "hanzi"),
    "ko": ("Korean", "hangul"),
    "hi": ("Hindi", "devanagari"),
    "ar": ("Arabic", "arabic"),
    "sw": ("Swahili", "latin_generic"),
    "id": ("Indonesian", "latin_id"),
    "tr": ("Turkish", "latin_tr"),
    "ru": ("Russian", "cyrillic"),
    "es": ("Spanish", "latin_es"),
    "fi": ("Finnish", "latin_fi"),
    "vi": ("Vietnamese", "latin_vi"),
    "ha": ("Hausa", "latin_generic"),
    "ta": ("Tamil", "tamil"),
    "he": ("Hebrew", "hebrew"),
    "is": ("Icelandic", "latin_is"),
    "hu": ("Hungarian", "latin_hu"),
    "cs": ("Czech", "latin_cs"),
}

# Scripts whose orthography does not write short vowels: usable for the
# loan/calque premise check (consonant skeleton), not for phonological scoring.
ABJAD = {"ar", "he"}
# Mandarin is written in a script that carries no phonological information we
# can extract without a reading dictionary; classified by hand (ZH_LOAN below).
NO_ROMANISER = {"zh"}

# ---------------------------------------------------------------------------
# The word set.  Fields:
#   key        - our identifier
#   wiki       - en.wikipedia title for the langlink query (None = no usable
#                article; the concept's article is about the number/abstraction
#                rather than the word, e.g. "zero" -> the article "0")
#   intl       - the INTERNATIONAL FORM fed to the transliteration ruleset.
#                Policy (notes/international-vocab.md 2.2): the Latin-script
#                shape shared by the largest number of the 18 recipient
#                languages, written with classical Latin/Greek digraphs (ph, th,
#                ch, x, c, y) so that the ruleset - not the word list - does the
#                sound mapping.  Where the classical form is NOT the
#                internationally shared shape (sugar, coffee, tea), the modern
#                shared shape is used and flagged in `intl_note`.
#   domain     - coverage bucket
#   why        - what this word tests (selection rationale, per CLAUDE.md)
# ---------------------------------------------------------------------------
W = lambda key, wiki, intl, domain, why, intl_note="": dict(  # noqa: E731
    key=key, wiki=wiki, intl=intl, domain=domain, why=why, intl_note=intl_note)

WORDS = [
    # --- chemistry / physics -------------------------------------------------
    W("atom", "Atom", "atom", "chem/phys",
      "the canonical case; vowel-initial, final /m/ - the one coda V3 buys and V2 does not"),
    W("proton", "Proton", "proton", "chem/phys",
      "initial /pr/ onset cluster + final /n/: the V3+onsets test in one word"),
    W("electron", "Electron", "electron", "chem/phys",
      "worst case: /kt/ medial cluster AND /tr/ onset cluster AND final /n/"),
    W("molecule", "Molecule", "molecula", "chem/phys",
      "final /l/ in most shapes; c before u vs e (the c->k/s rule)", "es/ru/cs/hu shape molekula"),
    W("oxygen", "Oxygen", "oxygen", "chem/phys",
      "x -> ks (cluster), g before a front vowel (soft-g ambiguity), y as a vowel"),
    W("hydrogen", "Hydrogen", "hydrogen", "chem/phys",
      "y as a vowel (i or u?), soft-g again, three syllables of Greek stem"),
    W("carbon", "Carbon", "carbon", "chem/phys",
      "/r/ coda - the V4 test case; final /n/"),
    W("energy", "Energy", "energia", "chem/phys",
      "soft g between vowels; final -ia ending", "ru/es/tr/id/hu shape energi(a)"),
    W("plastic", "Plastic", "plastic", "chem/phys",
      "/pl/ onset cluster, /st/ medial cluster, final /k/ - three repairs in one word"),
    # --- biology / medicine --------------------------------------------------
    W("virus", "Virus", "virus", "bio/med",
      "the /v/ three-way ambiguity plus the -us ending; adapted worldwide"),
    W("bacteria", "Bacteria", "bacteria", "bio/med",
      "/kt/ medial cluster, -ia ending, c->k before t"),
    W("antibiotic", "Antibiotic", "antibiotic", "bio/med",
      "long word: does length inflation compound? /nt/ cluster, final /k/"),
    W("vitamin", "Vitamin", "vitamin", "bio/med",
      "/v/ again, in a word with no clusters at all - isolates the /v/ decision"),
    W("protein", "Protein", "protein", "bio/med",
      "/pr/ onset, vowel hiatus /ei/, final /n/"),
    W("hormone", "Hormone", "hormon", "bio/med",
      "/r/ coda mid-word, silent final -e in English but not internationally",
      "tr/ru/id/cs/hu shape hormon"),
    W("malaria", "Malaria", "malaria", "bio/med",
      "already legal under V1 except for the -ia hiatus: a floor case"),
    W("insulin", "Insulin", "insulin", "bio/med",
      "/ns/ medial cluster with a legal nasal coda - V2/V3 should shine here"),
    W("vaccine", "Vaccine", "vaccin", "bio/med",
      "/v/, geminate cc -> /ks/ or /k/, final /n/", "tr/ru/id/hu shape vaksin/vakcina"),
    # --- mathematics / units -------------------------------------------------
    W("mathematics", "Mathematics", "mathematica", "math/units",
      "th -> t or s (the theta ambiguity) in a high-frequency academic word"),
    W("algebra", "Algebra", "algebra", "math/units",
      "Arabic-origin Wanderwort; /lg/ medial cluster and /br/ onset cluster"),
    W("geometry", "Geometry", "geometria", "math/units",
      "initial soft g (the single worst g case), vowel hiatus /eo/"),
    W("zero", None, "zero", "math/units",
      "Arabic-origin; initial /z/ - the z->s merger with no cluster noise"),
    W("million", None, "million", "math/units",
      "geminate ll, final /n/; the numeral system is internationally shared"),
    W("meter", "Metre", "meter", "math/units",
      "SI unit, near-universal; final /r/ - a V4 test with a very short word"),
    W("kilogram", "Kilogram", "kilogram", "math/units",
      "SI, compound, /gr/ onset cluster and final /m/"),
    # --- technology ----------------------------------------------------------
    W("telephone", "Telephone", "telephon", "technology",
      "ph -> f; the classic 19th-century internationalism", "shared shape telefon"),
    W("computer", "Computer", "computer", "technology",
      "/mp/ cluster with a legal nasal coda, final /r/; c->k"),
    W("radio", "Radio", "radio", "technology",
      "already almost legal under V1 - the best case, and a control"),
    W("internet", "Internet", "internet", "technology",
      "/rn/ medial cluster (illegal coda under V3) and final /t/"),
    W("television", "Television", "television", "technology",
      "/v/ plus -sion; long, and adapted nearly everywhere"),
    W("video", "Video", "video", "technology",
      "/v/ with no other difficulty - the second /v/ isolate"),
    W("machine", "Machine", "machina", "technology",
      "ch: Greek /k/ or French /sh/? the ch ambiguity, priced", "Latin machina; tr makine"),
    W("motor", None, "motor", "technology",
      "final /r/, otherwise CV throughout - isolates the liquid-coda decision"),
    W("film", "Film", "film", "technology",
      "final /lm/ CLUSTER coda - illegal under every variant including V5"),
    W("robot", "Robot", "robot", "technology",
      "Czech-origin internationalism; final /t/ - a non-nasal stop coda"),
    # --- institutions / society ----------------------------------------------
    W("democracy", "Democracy", "democratia", "institutions",
      "the -cy/-tia ending family; c->k then c->s in one word", "shared shape demokrat-"),
    W("police", "Police", "policia", "institutions",
      "c->s before i; one of the most widely borrowed institutional words",
      "shared shape polis/polisi/policia"),
    W("university", "University", "universitat", "institutions",
      "/v/ in a long word; the -itas/-ity ending family", "Latin universitas"),
    W("president", "President", "president", "institutions",
      "/pr/ onset, /nt/ pre-final cluster, final /t/"),
    W("hospital", "Hospital", "hospital", "institutions",
      "/sp/ medial cluster, final /l/ - the other V4 test"),
    W("bank", "Bank", "bank", "institutions",
      "final /nk/ cluster coda: legal nasal + illegal stop, the cleanest deletion test"),
    W("system", "System", "system", "institutions",
      "y as a vowel, /st/ medial cluster, final /m/ - V3's showcase"),
    W("program", None, "program", "institutions",
      "/pr/ and /gr/ onset clusters in one word, final /m/"),
    # --- non-technical Wanderwoerter ----------------------------------------
    W("coffee", "Coffee", "cafe", "wanderwort",
      "the archetypal Wanderwort; tests whether the ruleset handles non-classical shapes",
      "shared shape kaf-/kahv-, not English 'coffee'"),
    W("tea", "Tea", "te", "wanderwort",
      "two-phoneme word, two rival Wanderwort shapes (te vs chai) - a control on shortness",
      "te-family; the cha/chai family is the rival"),
    W("chocolate", "Chocolate", "chocolate", "wanderwort",
      "Nahuatl via Spanish; ch is /sh~ch/ here, so the ch->k rule is at its worst"),
    W("sugar", "Sugar", "sukar", "wanderwort",
      "Sanskrit->Arabic->Europe; travelled in many shapes, tests intl-form selection",
      "modern shared shape sukar/sukkar/sakar, not Latin saccharum"),
    W("banana", "Banana", "banana", "wanderwort",
      "West African origin; already fully legal under V1 - the floor case"),
    W("taxi", "Taxicab", "taxi", "wanderwort",
      "x -> ks medially; short and near-universal"),
    W("hotel", "Hotel", "hotel", "wanderwort",
      "final /l/, initial /h/ (silent in several donors) - a second V4 liquid test"),
    W("tomato", "Tomato", "tomate", "wanderwort",
      "Nahuatl Wanderwort, fully legal under V1 - second floor case"),
    W("theory", "Theory", "theoria", "wanderwort",
      "th again, plus /eo/ hiatus; the abstract-vocabulary counterpart to mathematics"),
]

# ---------------------------------------------------------------------------
# Mandarin: hand-classified, because Chinese characters carry no phonological
# information we can extract without a reading dictionary.  Value = the pinyin
# of the standard term when it is a PHONETIC loan, or None when the standard
# term is a calque / native compound.  PROVENANCE: model-recall, spot-checked
# against the cached langlink titles (which are shown in the CSV).
# ---------------------------------------------------------------------------
ZH_LOAN = {
    "coffee": "kafei",       # 咖啡
    "chocolate": "qiaokeli",  # 巧克力
    "taxi": "dishi",         # 的士 (HK/Cantonese-origin; mainland 出租车 is a calque)
    "meter": "mi",           # 米 (phonetic-semantic, one syllable)
    "vitamin": "weitaming",  # 维他命 (older loan; 维生素 is the modern calque)
    "gene": "jiyin",         # not in the word set; kept for the record
    "bank": None,            # 银行 calque
    "hotel": None,           # 酒店 calque
    "banana": None,          # 香蕉 calque
    "sugar": None,           # 糖 native
    "tea": "cha",            # 茶 - the SOURCE of the word, not a loan; see write-up
    "tomato": None,          # 番茄 native compound
}


def strip_diacritics(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", s)
                   if unicodedata.category(c) != "Mn")


# ---------------------------------------------------------------------------
# Fetching
# ---------------------------------------------------------------------------
def cache_path(title: str) -> Path:
    safe = title.replace("/", "_").replace(" ", "_")
    return RAW_DIR / f"{safe}.json"


def fetch_langlinks(offline: bool = False) -> dict[str, dict[str, str]]:
    """title -> {lang: native title}, cached one JSON per title under data/raw/."""
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    out: dict[str, dict[str, str]] = {}
    for w in WORDS:
        title = w["wiki"]
        if title is None:
            continue
        path = cache_path(title)
        if not path.exists():
            if offline:
                print(f"  [offline] missing cache for {title}", file=sys.stderr)
                continue
            r = requests.get(API, params={
                "action": "query", "titles": title, "prop": "langlinks",
                "lllimit": "500", "format": "json", "redirects": "1",
            }, headers={"User-Agent": USER_AGENT}, timeout=60)
            r.raise_for_status()
            path.write_text(r.text, encoding="utf-8")
            time.sleep(0.2)
        data = json.loads(path.read_text(encoding="utf-8"))
        pages = data.get("query", {}).get("pages", {})
        page = next(iter(pages.values())) if pages else {}
        out[title] = {ll["lang"]: ll["*"] for ll in page.get("langlinks", [])}
    return out


# ---------------------------------------------------------------------------
# Romanisation / phonemicisation.
#
# ALL OF THIS IS ROUGH AND HAND-WRITTEN.  It converts an attested written form
# into an IPA-ish string good enough for the recognizability metric.  It is not
# a transliteration standard and it does not model allophony, stress or tone.
# Known systematic errors are listed in notes/international-vocab.md 3.
# The comparison across our six variants is unaffected: every variant is scored
# against the same targets, so romanisation error is a shared constant.
# ---------------------------------------------------------------------------

# Applied in order, before the shared Latin fallback.  UPPERCASE letters are
# placeholders that no later rule matches; PLACEHOLDERS resolves them last.
# (Without them, e.g. Czech <ch> -> x would then be caught by the shared x ->
# ks rule, and Turkish <ü> -> y by the shared y -> j rule.)
LATIN_RULES = {
    "latin_generic": [("ch", "C"), ("sh", "ʃ"), ("ny", "ɲ"), ("ng", "ŋ"),
                      ("ɓ", "b"), ("ɗ", "d"), ("ƙ", "k"), ("j", "dZ"), ("y", "J")],
    "latin_id": [("sy", "ʃ"), ("kh", "X"), ("ny", "ɲ"), ("ng", "ŋ"),
                 ("c", "C"), ("j", "dZ"), ("y", "J")],
    "latin_tr": [("ç", "C"), ("ş", "ʃ"), ("ı", "ɯ"), ("ö", "ø"), ("ü", "Y"),
                 ("ğ", ""), ("â", "a"), ("j", "ʒ"), ("c", "dZ"), ("y", "J")],
    "latin_es": [("qu", "k"), ("gue", "ge"), ("gui", "gi"), ("ch", "C"),
                 ("ll", "J"), ("ñ", "ɲ"), ("ce", "se"), ("ci", "si"),
                 ("j", "X"), ("z", "s"), ("v", "b"), ("h", ""), ("y", "J")],
    "latin_fi": [("ä", "æ"), ("ö", "ø"), ("y", "Y"), ("ng", "ŋ"), ("j", "J")],
    "latin_vi": [("đ", "D"), ("ngh", "ŋ"), ("ng", "ŋ"), ("nh", "ɲ"), ("ph", "f"),
                 ("th", "t"), ("kh", "X"), ("gh", "ɣ"), ("tr", "ʈ"), ("ch", "C"),
                 ("gi", "Zi"), ("qu", "kw"), ("x", "S"), ("d", "Z"), ("r", "Z"),
                 ("ơ", "ə"), ("ư", "ɯ"), ("ô", "o"), ("ê", "e"), ("â", "ə"),
                 ("ă", "a"), ("y", "i")],
    # (acute/grave/tilde/hook/dot are stripped before these tables run, so
    #  Icelandic <ó á é> arrive as plain o a e and lose their diphthongs)
    "latin_is": [("þ", "θ"), ("ð", "ð"), ("hv", "kv"), ("ll", "tl"), ("æ", "ai"),
                 ("ö", "ø"), ("y", "i"), ("au", "øi"), ("j", "J")],
    "latin_hu": [("sz", "S"), ("zs", "ʒ"), ("cs", "C"), ("gy", "ɟ"), ("ny", "ɲ"),
                 ("ly", "J"), ("ty", "c"), ("s", "ʃ"), ("c", "ts"), ("j", "J"),
                 ("ö", "ø"), ("ü", "Y"), ("ő", "ø"), ("ű", "Y")],
    "latin_cs": [("ch", "X"), ("č", "C"), ("š", "ʃ"), ("ž", "ʒ"), ("ř", "r"),
                 ("ě", "Je"), ("c", "ts"), ("y", "i"), ("j", "J")],
}

# Shared fallback for anything the per-language table left behind.
LATIN_FALLBACK = [("ph", "f"), ("th", "θ"), ("qu", "kw"), ("ck", "k"), ("x", "ks"),
                  ("ce", "se"), ("ci", "si"), ("c", "k"), ("q", "k"), ("y", "J"),
                  ("w", "w")]

PLACEHOLDERS = [("dZ", "dʒ"), ("C", "tʃ"), ("X", "x"), ("Y", "y"), ("J", "j"),
                ("D", "d"), ("Z", "z"), ("S", "s")]

CYRILLIC = {"а": "a", "б": "b", "в": "v", "г": "g", "д": "d", "е": "e", "ё": "jo",
            "ж": "ʒ", "з": "z", "и": "i", "й": "j", "к": "k", "л": "l", "м": "m",
            "н": "n", "о": "o", "п": "p", "р": "r", "с": "s", "т": "t", "у": "u",
            "ф": "f", "х": "x", "ц": "ts", "ч": "tʃ", "ш": "ʃ", "щ": "ʃ", "ъ": "",
            "ы": "ɨ", "ь": "", "э": "e", "ю": "ju", "я": "ja"}

KANA_BASE = {
    "ア": "a", "イ": "i", "ウ": "u", "エ": "e", "オ": "o",
    "カ": "ka", "キ": "ki", "ク": "ku", "ケ": "ke", "コ": "ko",
    "ガ": "ga", "ギ": "gi", "グ": "gu", "ゲ": "ge", "ゴ": "go",
    "サ": "sa", "シ": "ʃi", "ス": "su", "セ": "se", "ソ": "so",
    "ザ": "za", "ジ": "dʒi", "ズ": "zu", "ゼ": "ze", "ゾ": "zo",
    "タ": "ta", "チ": "tʃi", "ツ": "tsu", "テ": "te", "ト": "to",
    "ダ": "da", "ヂ": "dʒi", "ヅ": "zu", "デ": "de", "ド": "do",
    "ナ": "na", "ニ": "ni", "ヌ": "nu", "ネ": "ne", "ノ": "no",
    "ハ": "ha", "ヒ": "hi", "フ": "ɸu", "ヘ": "he", "ホ": "ho",
    "バ": "ba", "ビ": "bi", "ブ": "bu", "ベ": "be", "ボ": "bo",
    "パ": "pa", "ピ": "pi", "プ": "pu", "ペ": "pe", "ポ": "po",
    "マ": "ma", "ミ": "mi", "ム": "mu", "メ": "me", "モ": "mo",
    "ヤ": "ja", "ユ": "ju", "ヨ": "jo",
    "ラ": "ra", "リ": "ri", "ル": "ru", "レ": "re", "ロ": "ro",
    "ワ": "wa", "ヲ": "o", "ン": "n", "ヴ": "vu",
}
KANA_SMALL = {"ァ": "a", "ィ": "i", "ゥ": "u", "ェ": "e", "ォ": "o"}
KANA_YOON = {"ャ": "ja", "ュ": "ju", "ョ": "jo"}

HANGUL_INI = ["k", "k", "n", "t", "t", "r", "m", "p", "p", "s", "s", "",
              "tʃ", "tʃ", "tʃ", "k", "t", "p", "h"]
HANGUL_MED = ["a", "e", "ja", "je", "ʌ", "e", "jʌ", "je", "o", "wa", "we", "we",
              "jo", "u", "wʌ", "we", "wi", "ju", "ɯ", "ɯi", "i"]
HANGUL_FIN = ["", "k", "k", "k", "n", "n", "n", "t", "l", "k", "m", "p", "l", "l",
              "p", "l", "m", "p", "p", "t", "t", "ŋ", "t", "t", "k", "t", "p", "t"]

DEVA_CONS = {"क": "k", "ख": "kʰ", "ग": "g", "घ": "g", "ङ": "ŋ", "च": "tʃ", "छ": "tʃ",
             "ज": "dʒ", "झ": "dʒ", "ञ": "ɲ", "ट": "ʈ", "ठ": "ʈ", "ड": "ɖ", "ढ": "ɖ",
             "ण": "ɳ", "त": "t", "थ": "t", "द": "d", "ध": "d", "न": "n", "प": "p",
             "फ": "pʰ", "ब": "b", "भ": "b", "म": "m", "य": "j", "र": "r", "ल": "l",
             "व": "v", "श": "ʃ", "ष": "ʃ", "स": "s", "ह": "h", "ळ": "l",
             "क़": "q", "ख़": "x", "ग़": "ɣ", "ज़": "z", "ड़": "ɽ", "ढ़": "ɽ", "फ़": "f"}
DEVA_VOW = {"अ": "a", "आ": "a", "इ": "i", "ई": "i", "उ": "u", "ऊ": "u", "ए": "e",
            "ऐ": "ɛ", "ओ": "o", "औ": "ɔ", "ऑ": "ɔ", "ऍ": "ɛ", "ऋ": "ri"}
DEVA_MAT = {"ा": "a", "ि": "i", "ी": "i", "ु": "u", "ू": "u", "े": "e", "ै": "ɛ",
            "ो": "o", "ौ": "ɔ", "ॉ": "ɔ", "ॅ": "ɛ", "ृ": "ri"}

TAMIL_VOW = {"அ": "a", "ஆ": "a", "இ": "i", "ஈ": "i", "உ": "u", "ஊ": "u", "எ": "e",
             "ஏ": "e", "ஐ": "ai", "ஒ": "o", "ஓ": "o", "ஔ": "au"}
TAMIL_CONS = {"க": "k", "ங": "ŋ", "ச": "s", "ஞ": "ɲ", "ட": "ʈ", "ண": "ɳ", "த": "t",
              "ந": "n", "ப": "p", "ம": "m", "ய": "j", "ர": "r", "ல": "l", "வ": "v",
              "ழ": "ɻ", "ள": "ɭ", "ற": "r", "ன": "n", "ஜ": "dʒ", "ஷ": "ʃ", "ஸ": "s",
              "ஹ": "h", "க்ஷ": "kʃ"}
TAMIL_SIGN = {"ா": "a", "ி": "i", "ீ": "i", "ு": "u", "ூ": "u", "ெ": "e", "ே": "e",
              "ை": "ai", "ொ": "o", "ோ": "o", "ௌ": "au"}
TAMIL_PULLI = "்"

ARABIC = {"ا": "a", "أ": "a", "إ": "i", "آ": "a", "ب": "b", "ت": "t", "ث": "θ",
          "ج": "dʒ", "ح": "h", "خ": "x", "د": "d", "ذ": "ð", "ر": "r", "ز": "z",
          "س": "s", "ش": "ʃ", "ص": "s", "ض": "d", "ط": "t", "ظ": "ð", "ع": "ʕ",
          "غ": "ɣ", "ف": "f", "ق": "q", "ك": "k", "ل": "l", "م": "m", "ن": "n",
          "ه": "h", "و": "u", "ي": "i", "ى": "a", "ة": "a", "ء": "ʔ", "ئ": "ʔ",
          "ؤ": "ʔ", "ﭬ": "v", "ڤ": "v", "پ": "p", "چ": "tʃ", "گ": "g"}

# Hebrew: aleph/vav/yod are read as the vowels they most often spell in loans
# (a / u / i) rather than as consonants - a deliberately loan-friendly reading,
# since the premise check is about whether a loan is there at all.  This is a
# systematic distortion for native words (which is where it matters least).
HEBREW = {"א": "a", "ב": "b", "ג": "g", "ד": "d", "ה": "h", "ו": "u", "ז": "z",
          "ח": "x", "ט": "t", "י": "i", "כ": "k", "ך": "k", "ל": "l", "מ": "m",
          "ם": "m", "נ": "n", "ן": "n", "ס": "s", "ע": "", "פ": "p", "ף": "f",
          "צ": "ts", "ץ": "ts", "ק": "k", "ר": "r", "ש": "ʃ", "ת": "t", "'": ""}


def _apply(rules, s: str) -> str:
    for a, b in rules:
        s = s.replace(a, b)
    return s


# Combining marks that carry stress, length or tone only - stripped BEFORE the
# per-language tables, so that e.g. Spanish <policía> still matches the ci -> si
# rule and Vietnamese tone marks do not block anything.  Marks that change the
# vowel (diaeresis, caron, ring, horn, breve, circumflex, cedilla) are kept.
_NOISE_MARKS = "̣́̀̉̃̇"


def _pre_strip(s: str) -> str:
    s = unicodedata.normalize("NFD", s)
    return unicodedata.normalize("NFC",
                                 "".join(c for c in s if c not in _NOISE_MARKS))


def rom_latin(form: str, script: str) -> str:
    s = _pre_strip(form.lower())
    s = _apply(LATIN_RULES.get(script, LATIN_RULES["latin_generic"]), s)
    s = _apply(LATIN_FALLBACK, s)
    s = _apply(PLACEHOLDERS, s)
    return strip_diacritics(s)


def rom_cyrillic(form: str) -> str:
    return "".join(CYRILLIC.get(c, "" if not c.isalpha() else c) for c in form.lower())


def rom_kana(form: str) -> str:
    out = []
    i = 0
    while i < len(form):
        c = form[i]
        nxt = form[i + 1] if i + 1 < len(form) else ""
        if c in KANA_BASE:
            syl = KANA_BASE[c]
            if nxt in KANA_SMALL:                      # フィ = fi, ヴァ = va
                syl = syl[:-1] + KANA_SMALL[nxt]
                i += 1
            elif nxt in KANA_YOON:                     # キャ = kja
                syl = syl[:-1] + KANA_YOON[nxt]
                i += 1
            out.append(syl)
        elif c == "ー":                                # long vowel: no length contrast
            pass
        elif c == "ッ":                                # gemination: not modelled
            pass
        i += 1
    return "".join(out)


def rom_hangul(form: str) -> str:
    out = []
    for c in form:
        o = ord(c)
        if 0xAC00 <= o <= 0xD7A3:
            k = o - 0xAC00
            out.append(HANGUL_INI[k // 588] + HANGUL_MED[(k % 588) // 28]
                       + HANGUL_FIN[k % 28])
    return "".join(out)


def rom_devanagari(form: str) -> str:
    out = []
    last_inherent = False
    i = 0
    while i < len(form):
        c = form[i]
        nxt = form[i + 1] if i + 1 < len(form) else ""
        two = c + nxt
        if two in DEVA_CONS:
            cons, i = DEVA_CONS[two], i + 1
        elif c in DEVA_CONS:
            cons = DEVA_CONS[c]
        else:
            cons = None
        if cons is not None:
            j = i + 1
            follow = form[j] if j < len(form) else ""
            if follow in DEVA_MAT:
                out.append(cons + DEVA_MAT[follow])
                last_inherent = False
                i = j + 1
            elif follow == "्":                    # virama: bare consonant
                out.append(cons)
                last_inherent = False
                i = j + 1
            else:
                out.append(cons + "a")                  # inherent vowel
                last_inherent = True
                i = j
            continue
        if c in DEVA_VOW:
            out.append(DEVA_VOW[c])
            last_inherent = False
        elif c in ("ं", "ँ"):
            out.append("n")
            last_inherent = False
        i += 1
    s = "".join(out)
    if last_inherent and s.endswith("a"):   # Hindi word-final schwa deletion
        s = s[:-1]
    return s


def rom_tamil(form: str) -> str:
    out = []
    i = 0
    while i < len(form):
        c = form[i]
        if c in TAMIL_CONS:
            nxt = form[i + 1] if i + 1 < len(form) else ""
            if nxt == TAMIL_PULLI:
                out.append(TAMIL_CONS[c])
                i += 2
                continue
            if nxt in TAMIL_SIGN:
                out.append(TAMIL_CONS[c] + TAMIL_SIGN[nxt])
                i += 2
                continue
            out.append(TAMIL_CONS[c] + "a")
        elif c in TAMIL_VOW:
            out.append(TAMIL_VOW[c])
        i += 1
    return "".join(out)


def rom_abjad(form: str, table: dict) -> str:
    return "".join(table.get(c, "") for c in form)


def romanise(form: str, script: str) -> str:
    """Attested written form -> IPA-ish string (see the caveats at the top)."""
    form = form.split("(")[0].strip()
    if script.startswith("latin"):
        return rom_latin(form, script)
    if script == "cyrillic":
        return rom_cyrillic(form)
    if script == "japanese":
        return rom_kana(form)
    if script == "hangul":
        return rom_hangul(form)
    if script == "devanagari":
        return rom_devanagari(form)
    if script == "tamil":
        return rom_tamil(form)
    if script == "arabic":
        return rom_abjad(form, ARABIC)
    if script == "hebrew":
        return rom_abjad(form, HEBREW)
    return ""


# The reference reading of the international form: the same Latin-script
# spelling read with the sound values the DONOR languages actually use (so
# <v> = /v/, <z> = /z/, <ch> = /tʃ/, <th> = /θ/).  This is the target our
# transliteration is scored against - the gap between this reading and our
# ruleset's Latin reading is exactly the segment-mapping cost being measured.
INTL_READ = [("sch", "sk"), ("ph", "f"), ("th", "θ"), ("ch", "tʃ"), ("sh", "ʃ"),
             ("qu", "kw"), ("ae", "e"), ("oe", "e"), ("x", "ks"), ("ce", "se"),
             ("ci", "si"), ("cy", "si"), ("c", "k"), ("q", "k"), ("y", "i"),
             ("g", "ɡ")]


def intl_ipa(intl: str) -> str:
    return strip_diacritics(_apply(INTL_READ, intl.lower()))


# ---------------------------------------------------------------------------
# Loan vs calque classification (the premise check)
#
# POLICY.  A recipient form counts as an ADAPTATION of the international word
# when its best-matching part scores >= LOAN_THRESHOLD against the reference
# reading of the international form under metric v0.  "Best-matching part"
# means: the whole title, or any whitespace-separated token, or that token
# truncated to the length of the international form - so a compound that
# CONTAINS the international stem (Czech "Radiokomunikace", Hungarian
# "Telefonkeszulek", Hausa "Kwayar cutar Bakteriya") counts as an adaptation,
# which is what the premise is actually about.
#
# The measure is NOT metric v0.  v0 is length-biased at this decision boundary
# (short words score high by chance against anything - its random-pair floor is
# ~0.46, principles.md 4 issue 3), which made short loans like Spanish "metro"
# and short calques like Korean "sanso" inseparable.  Instead: a weighted edit
# distance over a COARSE CONSONANT-CLASS SKELETON, which is what actually
# survives borrowing.  Consonants collapse to 8 place/manner classes, vowels to
# a single class, and vowel insertion/deletion costs 0.4 against 1.0 for a
# consonant - so epenthesis (Japanese "intaneto", Swahili "protini") is nearly
# free while a different root is not.
#
# LOAN_THRESHOLD = 0.62 was set by inspecting the score distribution and
# hand-auditing a stratified sample of 60 forms (notes/international-vocab.md
# 1.2 reports the measured error rate of the classifier).
# ---------------------------------------------------------------------------
LOAN_THRESHOLD = 0.62
IPA_VOWELS = set("aeiouɛɔəɯøyæʌɨ")

_CLASS = {}
for _ch in "pbfvɸw":
    _CLASS[_ch] = "P"      # labial
for _ch in "tdʈɖθðc":
    _CLASS[_ch] = "T"      # coronal/dorsal stop, non-sibilant
for _ch in "szʃʒɕʐ":
    _CLASS[_ch] = "S"      # sibilant
for _ch in "kgxɣqħʕʔ":
    _CLASS[_ch] = "K"      # velar/uvular/guttural
for _ch in "mnŋɲɳ":
    _CLASS[_ch] = "N"      # one nasal class: place assimilation is universal
                           # in adaptation ("computer" -> konpjuta, kompyuter)
for _ch in "lrɾɽɭɻʎ":
    _CLASS[_ch] = "L"
_CLASS["j"] = "J"
for _ch in IPA_VOWELS:
    _CLASS[_ch] = "V"

# affricates collapse into the sibilant class; aspiration is not contrastive
_AFFRICATES = [("ts", "s"), ("tʃ", "s"), ("dʒ", "s"), ("dz", "s"),
               ("kʰ", "k"), ("tʰ", "t"), ("pʰ", "p"), ("ʰ", ""), ("ː", "")]


def skeleton(s: str) -> str:
    for a, b in _AFFRICATES:
        s = s.replace(a, b)
    return "".join(_CLASS.get(c, "") for c in s)


def _cost(sym: str) -> float:
    return 0.4 if sym == "V" else 1.0


def shape_similarity(a: str, b: str) -> float:
    """1.0 = same consonant-class skeleton; 0.0 = nothing in common."""
    A, B = skeleton(a), skeleton(b)
    if not A or not B:
        return 0.0
    prev = [0.0] * (len(B) + 1)
    for j in range(1, len(B) + 1):
        prev[j] = prev[j - 1] + _cost(B[j - 1])
    for i in range(1, len(A) + 1):
        cur = [prev[0] + _cost(A[i - 1])] + [0.0] * len(B)
        for j in range(1, len(B) + 1):
            sub = prev[j - 1] + (0.0 if A[i - 1] == B[j - 1] else 1.0)
            cur[j] = min(sub, prev[j] + _cost(A[i - 1]), cur[j - 1] + _cost(B[j - 1]))
        prev = cur
    norm = max(sum(_cost(c) for c in A), sum(_cost(c) for c in B))
    return max(0.0, 1.0 - prev[-1] / norm)


def loan_score(title: str, script: str, ref: str, abjad: bool) -> tuple[float, str]:
    """Best match between any part of `title` and the international form."""
    cands = [title] + title.replace("-", " ").split()
    best, best_form = 0.0, ""
    for cand in cands:
        rom = romanise(cand, script)
        if not rom:
            continue
        variants = [rom, rom[:len(ref) + 1]] if len(rom) > len(ref) + 1 else [rom]
        for var in variants:
            a, b = var, ref
            if abjad:   # short vowels are unwritten: compare skeletons only
                a = "".join(c for c in a if c not in IPA_VOWELS)
                b = "".join(c for c in b if c not in IPA_VOWELS)
            s = shape_similarity(a, b)
            if s > best:
                best, best_form = s, rom
    return best, best_form


# Everyday spoken loans that the Wikipedia title hides behind a purist or
# calqued headword.  PROVENANCE: model-recall (author model's own knowledge),
# NOT dataset-derived.  Used only for the sensitivity check in
# notes/international-vocab.md 1.3 - never in a headline number.
MODEL_RECALL = {
    ("hi", "telephone"): "टेलीफोन",
    ("hi", "virus"): "वायरस",
    ("hi", "bacteria"): "बैक्टीरिया",
    ("hi", "atom"): "एटम",
    ("hi", "computer"): "कंप्यूटर",
    ("hi", "internet"): "इंटरनेट",
    ("hi", "hospital"): "हॉस्पिटल",
    ("hi", "police"): "पुलिस",
    ("hi", "university"): "यूनिवर्सिटी",
    ("hi", "energy"): "एनर्जी",
    ("ta", "telephone"): "டெலிபோன்",
    ("ta", "computer"): "கம்ப்யூட்டர்",
    ("ta", "bus"): "பஸ்",
    ("ta", "coffee"): "காபி",
    ("ja", "computer"): "コンピューター",
    ("ko", "computer"): "컴퓨터",
    ("vi", "radio"): "ra-đi-ô",
    ("is", "banana"): "banani",
}


def build_forms(ll: dict) -> pd.DataFrame:
    """One row per (word, language): the attested form, romanised and classified."""
    rows = []
    for w in WORDS:
        ref = intl_ipa(w["intl"])
        titles = ll.get(w["wiki"], {}) if w["wiki"] else {}
        for code, (lname, script) in LANGS.items():
            title = titles.get(code)
            provenance = "wikipedia"
            if title is None:
                supp = MODEL_RECALL.get((code, w["key"]))
                if supp is None:
                    continue
                title, provenance = supp, "model-recall"
            if code in NO_ROMANISER:
                pin = ZH_LOAN.get(w["key"], "__unknown__")
                rows.append(dict(
                    word=w["key"], lang=code, language=lname, title=title,
                    romanised=pin if isinstance(pin, str) and pin != "__unknown__" else "",
                    provenance="model-recall" if pin != "__unknown__" else "unclassified",
                    loan_score=float("nan"),
                    is_loan={"__unknown__": None}.get(pin, pin is not None),
                    scored=False))
                continue
            score, rom = loan_score(title, script, ref, code in ABJAD)
            rows.append(dict(
                word=w["key"], lang=code, language=lname, title=title,
                romanised=rom, provenance=provenance, loan_score=round(score, 4),
                is_loan=bool(score >= LOAN_THRESHOLD),
                scored=(code not in ABJAD and provenance == "wikipedia")))
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# The template comparison
# ---------------------------------------------------------------------------
VARIANT_ORDER = ["V1", "V2", "V3", "V4", "V5", "V3C"]

# Recipient languages that must themselves repair clusters and codas (open
# syllables or a very small coda set): they show what an adapting language
# does, so scoring against them is the check on whether the metric's known
# pro-permissive bias is driving the variant ranking.  Classified from standard
# descriptions, not from data in this repo - a judgment call.
RESTRICTIVE = {"ja", "ko", "sw", "ta", "ha", "vi"}

# Default ruleset settings (the recommendation; each is priced in the
# sensitivity arms below and audited in notes/international-vocab.md 6).
DEFAULTS = dict(v_target="w", th_target="t", epen="i", final_policy="delete")


def learned_params():
    """The FeatureWeightCosts vector from the cost-learning study (opt-in arm)."""
    p = pd.read_csv(ROOT / "data" / "processed" / "learned_costs.csv")
    p = p[p.model == "FeatureWeightCosts"]
    return p.set_index("parameter")["learned_full"].to_numpy()


def _mean(xs) -> float:
    return round(sum(xs) / len(xs), 4) if xs else float("nan")


def score_variants(forms: pd.DataFrame, quick: bool = False) -> pd.DataFrame:
    """One row per word x variant x final-coda policy."""
    from interlang import metric, translit

    params = learned_params()
    scored = forms[forms.scored & forms.is_loan.fillna(False)]
    by_word = {k: g for k, g in scored.groupby("word")}
    rows = []
    for w in WORDS:
        ref = intl_ipa(w["intl"])
        g = by_word.get(w["key"])
        targets = list(g.romanised) if g is not None else []
        langs = list(g.lang) if g is not None else []
        restr = [t for t, la in zip(targets, langs) if la in RESTRICTIVE]
        perm = [t for t, la in zip(targets, langs) if la not in RESTRICTIVE]
        # reference points, independent of variant
        ceiling = ([metric.similarity(ref, t) for t in targets])
        pairwise = [metric.similarity(targets[i], targets[j])
                    for i in range(len(targets)) for j in range(i + 1, len(targets))]
        for vname in VARIANT_ORDER:
            for fp in ("delete", "epenthesize"):
                kw = dict(DEFAULTS, final_policy=fp)
                r = translit.render(w["intl"], vname, **kw)
                ipa = translit.to_ipa(r["form"])
                sims = [metric.similarity(ipa, t) for t in targets]
                sims_l = ([] if quick else
                          [metric.similarity(ipa, t, params=params) for t in targets])
                rows.append(dict(
                    word=w["key"], domain=w["domain"], intl=w["intl"],
                    variant=vname, final_policy=fp,
                    form=r["form"], phonemes=r["phonemes"],
                    syl_before=r["syl_before"], syl_after=r["syl_after"],
                    syl_inflation=round(r["syl_after"] / r["syl_before"], 4),
                    len_before=r["len_before"], len_after=r["len_after"],
                    len_inflation=round(r["len_after"] / r["len_before"], 4),
                    n_epenthesis=r["n_epenthesis"], n_deleted=r["n_deleted"],
                    n_lossy_segment=sum(1 for x in r["trace"]
                                        if x.startswith("LOSSY:A")),
                    n_attested=len(targets), attested_langs="|".join(langs),
                    sim_attested=round(sum(sims) / len(sims), 4) if sims else float("nan"),
                    sim_attested_min=round(min(sims), 4) if sims else float("nan"),
                    sim_restrictive=_mean([metric.similarity(ipa, t) for t in restr]),
                    sim_permissive=_mean([metric.similarity(ipa, t) for t in perm]),
                    sim_attested_learned=(round(sum(sims_l) / len(sims_l), 4)
                                          if sims_l else float("nan")),
                    sim_ceiling=(round(sum(ceiling) / len(ceiling), 4)
                                 if ceiling else float("nan")),
                    sim_attested_pairwise=(round(sum(pairwise) / len(pairwise), 4)
                                           if pairwise else float("nan")),
                    why=w["why"], intl_note=w["intl_note"],
                ))
    df = pd.DataFrame(rows)
    df["retention"] = (df.sim_attested / df.sim_ceiling).round(4)
    return df


# ---------------------------------------------------------------------------
# The predictability audit (deliverable B)
#
# INVERSE table: for each interlang phoneme, which international graphemes can
# produce it under the stage-1 rules.  A phoneme with >1 possible source is a
# point where the learner going BACKWARDS (interlang -> international word) has
# to guess.  Deletions are worse than ambiguities: they are unrecoverable.
# ---------------------------------------------------------------------------
INVERSE = {
    "k": ["k", "c", "q(u)", "ch", "ck"],
    "s": ["s", "c(e/i)", "z", "sh", "th(arm s)"],
    "t": ["t", "th"],
    "f": ["f", "ph"],
    "w": ["w", "v"],
    "i": ["i", "y"],
    "j": ["j", "y(_V)"],
    "e": ["e", "ae", "oe"],
    "g": ["g", "gh"],
    "r": ["r", "rh"],
}


def audit(forms: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    from interlang import translit
    from collections import Counter

    fired = Counter()
    per_word = []
    seen: dict[str, list[str]] = {}
    for w in WORDS:
        r = translit.render(w["intl"], "V3", **DEFAULTS)
        for t in r["trace"]:
            if t.startswith("LOSSY:"):
                fired[t.split(" ", 1)[0].removeprefix("LOSSY:") + " " + t.split(" ", 1)[1]] += 1
        amb = sum(1 for c in r["form"] if c in INVERSE)
        per_word.append(dict(word=w["key"], form=r["form"],
                             n_phonemes=len(r["form"]),
                             n_ambiguous_phonemes=amb,
                             n_deleted=r["n_deleted"],
                             fully_invertible=(amb == 0 and r["n_deleted"] == 0)))
        seen.setdefault(r["form"], []).append(w["key"])
    rules = (pd.DataFrame(sorted(fired.items(), key=lambda x: -x[1]),
                          columns=["lossy_rule", "n_words"]))
    collisions = {k: v for k, v in seen.items() if len(v) > 1}
    return rules, pd.DataFrame(per_word), collisions


def sensitivity(forms: pd.DataFrame) -> pd.DataFrame:
    """Price each open decision point of the ruleset, under V3."""
    from interlang import metric, translit

    scored = forms[forms.scored & forms.is_loan.fillna(False)]
    by_word = {k: list(g.romanised) for k, g in scored.groupby("word")}
    arms = []
    for key, options in [("v_target", ["w", "b", "f"]),
                         ("th_target", ["t", "s"]),
                         ("epen", ["i", "u", "echo"]),
                         ("final_policy", ["delete", "epenthesize"]),
                         ("g_soft", [False, True])]:
        for opt in options:
            kw = dict(DEFAULTS)
            kw[key] = opt
            sims, syls = [], []
            for w in WORDS:
                targets = by_word.get(w["key"], [])
                r = translit.render(w["intl"], "V3", **kw)
                syls.append(r["syl_after"] / r["syl_before"])
                ipa = translit.to_ipa(r["form"])
                sims += [metric.similarity(ipa, t) for t in targets]
            arms.append(dict(decision=key, option=str(opt),
                             mean_sim=round(sum(sims) / len(sims), 4),
                             mean_syl_inflation=round(sum(syls) / len(syls), 4)))
    return pd.DataFrame(arms)


def main() -> None:
    offline = "--offline" in sys.argv
    quick = "--quick" in sys.argv
    ll = fetch_langlinks(offline=offline)
    forms = build_forms(ll)

    df = score_variants(forms, quick=quick)

    # attach the V3 similarity per attested form, for the forms CSV
    from interlang import metric, translit
    v3 = {w["key"]: translit.to_ipa(translit.render(w["intl"], "V3", **DEFAULTS)["form"])
          for w in WORDS}
    forms["v3_form"] = forms.word.map(v3)
    forms["sim_to_v3"] = [
        round(metric.similarity(v3[r.word], r.romanised), 4)
        if isinstance(r.romanised, str) and r.romanised and r.scored else float("nan")
        for r in forms.itertuples()]
    forms.to_csv(OUT_FORMS, index=False)
    df.to_csv(OUT_CSV, index=False)

    # ---- console summary --------------------------------------------------
    pd.set_option("display.width", 200)
    print(f"\n{len(forms)} attested forms, "
          f"{int(forms.is_loan.fillna(False).sum())} classified as adaptations, "
          f"{int(forms.scored.sum())} usable for scoring\n")

    print("=== PREMISE CHECK: share of the word set adapted from the "
          "international root, by language ===")
    prem = (forms[forms.provenance == "wikipedia"]
            .groupby(["lang", "language"])
            .agg(n=("word", "size"), adapted=("is_loan", "sum")))
    prem["pct_adapted"] = (100 * prem.adapted / prem.n).round(1)
    print(prem.sort_values("pct_adapted", ascending=False).to_string())

    print("\n=== VARIANT COMPARISON (52 words) ===")
    agg = df.groupby(["final_policy", "variant"]).agg(
        syl_before=("syl_before", "mean"), syl_after=("syl_after", "mean"),
        syl_inflation=("syl_inflation", "mean"),
        len_inflation=("len_inflation", "mean"),
        epenthesis=("n_epenthesis", "mean"), deleted=("n_deleted", "mean"),
        sim=("sim_attested", "mean"), sim_learned=("sim_attested_learned", "mean"),
        sim_restr=("sim_restrictive", "mean"), sim_perm=("sim_permissive", "mean"),
        retention=("retention", "mean"))
    idx = [(f, v) for f in ("delete", "epenthesize") for v in VARIANT_ORDER]
    print(agg.reindex(idx).round(4).to_string())
    print("\nreference points: mean similarity of the international form itself "
          f"to the attested set = {df.sim_ceiling.mean():.4f}; "
          "mean pairwise similarity AMONG the attested adaptations = "
          f"{df.sim_attested_pairwise.mean():.4f}")

    print("\n=== V3 RENDERINGS (both final-coda policies) ===")
    v3 = df[(df.variant == "V3") & (df.final_policy == "delete")].set_index("word")
    v3e = df[(df.variant == "V3") & (df.final_policy == "epenthesize")].set_index("word")
    tbl = pd.DataFrame({
        "intl": v3.intl, "V3_delete": v3.form, "V3_epen": v3e.form,
        "syl_in": v3.syl_before, "syl_del": v3.syl_after, "syl_epen": v3e.syl_after,
        "sim_del": v3.sim_attested, "sim_epen": v3e.sim_attested,
        "ceiling": v3.sim_ceiling})
    print(tbl.to_string())

    print("\n=== where the coda set actually matters (V2 vs V3 vs V4 vs V3C, delete) ===")
    d = df[df.final_policy == "delete"].pivot_table(
        index="word", columns="variant", values="form", aggfunc="first")
    diff = d[d.V2 != d.V4][["V2", "V3", "V4", "V5", "V3C"]]
    print(diff.to_string())

    print("\n=== SENSITIVITY: pricing each open decision (V3) ===")
    print(sensitivity(forms).to_string(index=False))

    print("\n=== PREDICTABILITY AUDIT ===")
    rules, per_word, collisions = audit(forms)
    print(rules.to_string(index=False))
    print(f"\nwords whose V3 form contains at least one ambiguous phoneme: "
          f"{int((per_word.n_ambiguous_phonemes > 0).sum())}/{len(per_word)}; "
          f"fully invertible words: {int(per_word.fully_invertible.sum())}; "
          f"words losing a segment to final deletion: "
          f"{int((per_word.n_deleted > 0).sum())}")
    print(f"ambiguous-source phonemes: "
          f"{per_word.n_ambiguous_phonemes.sum()}/{per_word.n_phonemes.sum()} "
          f"({100 * per_word.n_ambiguous_phonemes.sum() / per_word.n_phonemes.sum():.1f}%), "
          f"mean {per_word.n_ambiguous_phonemes.mean():.2f} per word")
    print(f"rendering collisions within the word set: {collisions or 'none'}")

    print("\n=== by domain (V3, delete) ===")
    dom = (df[(df.variant == "V3") & (df.final_policy == "delete")]
           .groupby("domain")
           .agg(n=("word", "size"), syl_inflation=("syl_inflation", "mean"),
                sim=("sim_attested", "mean"), ceiling=("sim_ceiling", "mean")))
    print(dom.round(4).to_string())

    print(f"\nwrote {OUT_CSV}\nwrote {OUT_FORMS}")


if __name__ == "__main__":
    main()
