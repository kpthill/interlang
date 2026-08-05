"""Punctuation and capitalization survey: what do the world's writing systems do?

The letters of the interlang orthography are settled (principles.md 3.7: ASCII IPA,
one letter per phoneme, `p t k b d g m n f s h j w l r a e i o u`). What is not
settled is the *conventions* layered on top - sentence-final marks, question and
exclamation marks, commas, quotation marks, capitalization, word spacing, number
separators. This script ranks the options in each of those areas by how many of the
world's speakers already use them.

Weighting is **total (L1+L2) speakers**, i.e. the ease-of-learning objective's
weighting (principles.md 2). An L1-weighted column is emitted alongside it where it
is available, but the total-weighted column is the headline.

FRAMING: our orthography is ASCII Latin and left-to-right. A convention used by 20%
of the world but requiring a non-ASCII character is *context*, not a candidate. Every
row therefore carries `ascii_available`, computed from whether the option's glyph is
pure ASCII (options with no glyph - "no mark at all", "no spaces" - count as
available). Read the ranked table for what the world does; read the ascii_available
subset for what we can actually choose.

Jargon, for a non-linguist reader
---------------------------------
  bicameral     a script that has two cases, capitals and lower case (Latin, Cyrillic,
                Greek, Armenian). unicameral = one case only, no capitals at all
                (Arabic, Devanagari, Han, Hangul, Thai, Hebrew, Ethiopic, ...).
  danda         the vertical bar `|` (U+0964) used as a full stop in Devanagari,
                Bengali and Gurmukhi.
  scriptio      writing with no spaces between words (Chinese, Japanese, Thai).
  continua
  locale        a language + optional script + region, e.g. `es_MX`. CLDR's unit of
                data. Regional variation is real here: `es` uses `1.000,50` but
                `es_MX` uses `1,000.50`.
  numbering     which digits a locale writes numbers with. `latn` = 0-9,
  system        `arab` = Arabic-Indic digits, `deva` = Devanagari digits.

TWO KINDS OF ROW - THIS MATTERS, DO NOT CONFLATE THEM
------------------------------------------------------
  source="cldr"       Derived from a real database. CLDR `common/main/*.xml` has
                      genuine per-locale `<delimiters>` (quotation marks) and
                      `<numbers>` (decimal/grouping separators and grouping pattern).
                      These are extracted per locale, with CLDR's inheritance
                      (the "same as parent" marker) and `parentLocales` overrides
                      resolved, then weighted by that locale's speaker population.
  source="knowledge"  ASSEMBLED FROM THE AUTHOR'S OWN KNOWLEDGE, NOT FROM A DATASET.
                      No database of sentence-final punctuation, capitalization rules
                      or word spacing exists in machine-readable form, so the
                      table in `LANGUAGE_CONVENTIONS` below was written out by hand
                      for the top 50 languages by CLDR total-speaker count. It is
                      recalled, not measured. The population weights attached to it
                      are real; the convention labels are not dataset output. Given
                      the stakes (a one-session survey to pick a punctuation
                      convention) this was judged acceptable - see
                      notes/punctuation-survey.md, which repeats the warning.

Judgment calls
--------------
  - Ranked set = the top 50 languages by CLDR total-speaker weight (>=34M speakers),
    covering 82.7% of the world's total-speaker weight. Knowledge-row percentages are
    shares of *that set*, not of the world; `pct_world_total_weighted` gives the
    unadjusted share so the coverage gap is visible.
  - A handful of languages outside the top 50 carry conventions that are the whole
    reason a reader would ask (Greek `;` for question, Khmer/Lao no word spacing,
    Armenian `:`). They are in `CONTEXT_LANGUAGES`, are reported separately, and are
    deliberately EXCLUDED from the percentages - hand-picking languages because they
    have an unusual convention would inflate that convention's prevalence.
  - One convention per language. Real usage is mixed (Hindi writes both `|` and `.`;
    Amharic writes both `?` and `?`(U+1367 family)). The dominant/prescribed form is
    recorded and the mixed cases are noted in the write-up.
  - Script assignment is the dominant modern script: Punjabi is split (pan =
    Gurmukhi in India, pnb = Shahmukhi/Arabic in Pakistan), Uzbek is Latin, Hausa is
    Boko (Latin), Javanese is Latin.
  - CLDR rows are weighted at the (language, territory) grain, which is finer than
    the project's usual per-ISO-639-3 total. This is deliberate: `es_MX` and `es_AR`
    genuinely differ on decimals. The per-language sums are asserted to reproduce
    `populations.cldr_totals()` so the two weightings stay reconcilable.
  - `n_units` on a CLDR row counts distinct (language name, territory) labels, not
    raw locale rows, so two subtags that collapse to the same ISO 639-3 in the same
    territory (`zh` and `zh_Hant` in TW) are counted once. 1583 locale rows ->
    1565 labels. Weights are unaffected; only the count column is.
  - CLDR's inheritance marker is a literal `UP UP UP` (U+2191 x3) meaning "checked,
    same as parent". That is a positive statement, so it counts. A locale whose
    whole chain is silent below `root` was never surveyed and silently picks up
    root's curly quotes and `.`/`,` - which inflates exactly the options we are
    minded to pick. 12.7% of the quotation weight and 13.4% of the number weight is
    of that kind, so every CLDR row also carries `pct_stated_only`, the share
    within the surveyed subset. Both numbers are reported in the write-up; they
    differ by ~3 points and change no ranking.
  - Number separators are read for the locale's *default* numbering system, so
    Arabic locales show the Arabic-Indic U+066B/U+066C they actually use. A
    numbering system that defines digits but no separators (`beng`, `deva`, `mymr`)
    falls back to `latn`, which is what CLDR itself does. A second block of rows
    reports the `latn` separators unconditionally, i.e. what the locale does when
    it writes with 0-9 digits - the question relevant to us.

Inputs:
  data/raw/cldr/common/main/*.xml              (CLDR locale data; see README)
  data/raw/cldr_supplementalData.xml           (populations + parentLocales)
  data/raw/iso639/{iso-639-3.tab|language-codes-full.csv}
  data/processed/l1_speakers.csv

Output:
  data/processed/punctuation_survey.csv        one row per (area, option)

Usage: uv run python scripts/punctuation_survey.py
"""

from __future__ import annotations

import sys
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from interlang.populations import (  # noqa: E402
    MACRO_MAP,
    _iso_tables,
    cldr_totals,
    read_l1_speakers,
)

CLDR_MAIN = ROOT / "data" / "raw" / "cldr" / "common" / "main"
CLDR_SUPP = ROOT / "data" / "raw" / "cldr_supplementalData.xml"
ISO_DIR = ROOT / "data" / "raw" / "iso639"
L1_CSV = ROOT / "data" / "processed" / "l1_speakers.csv"
OUT_CSV = ROOT / "data" / "processed" / "punctuation_survey.csv"

TOP_N = 50

# ---------------------------------------------------------------------------
# KNOWLEDGE-ASSEMBLED TABLE.  Everything below this line until the next banner
# is recalled, not measured.  See the module docstring.
#
# Fields per language:
#   script            dominant modern script
#   case              "bicameral" (has capitals) / "unicameral" (no case at all)
#   sentence_final    the mark that ends a declarative sentence
#   question          the question mark
#   exclamation       the exclamation mark
#   comma             the mid-sentence separator
#   spacing           "spaces" / "none" (scriptio continua) / "syllables"
#   caps              capitalization rule bundle, unicameral scripts get "n/a"
# ---------------------------------------------------------------------------

DANDA = "।"  # | Devanagari danda, also used for Bengali and Gurmukhi
URDU_FS = "۔"  # . Arabic full stop (Urdu, Pashto, Sindhi, Shahmukhi Punjabi)
ARQ = "؟"  # ? Arabic question mark
ACOM = "،"  # , Arabic comma
IDEO_FS = "。"  # . ideographic full stop
IDEO_COM = "、"  # , ideographic comma
FW_Q = "？"  # ? fullwidth question mark
FW_EX = "！"  # ! fullwidth exclamation mark
ETH_FS = "።"  # Ethiopic full stop
ETH_COM = "፣"  # Ethiopic comma
ETH_Q = "፧"  # Ethiopic question mark

# convention bundles, to keep the per-language table short
LATIN = dict(sentence_final=".", question="?", exclamation="!", comma=",",
             spacing="spaces", case="bicameral",
             caps="sentence-initial + proper nouns")
CYRILLIC = dict(LATIN, script="Cyrillic")
HAN = dict(sentence_final=IDEO_FS, question=FW_Q, exclamation=FW_EX,
           comma=IDEO_COM, spacing="none", case="unicameral", caps="n/a (no case)")
ARABIC = dict(sentence_final=".", question=ARQ, exclamation="!", comma=ACOM,
              spacing="spaces", case="unicameral", caps="n/a (no case)")
PERSO = dict(ARABIC, sentence_final=URDU_FS)  # Urdu/Pashto/Sindhi/Shahmukhi style
INDIC_DANDA = dict(sentence_final=DANDA, question="?", exclamation="!", comma=",",
                   spacing="spaces", case="unicameral", caps="n/a (no case)")
INDIC_DOT = dict(INDIC_DANDA, sentence_final=".")


def _lang(script: str, base: dict, **over) -> dict:
    return dict(base, script=script, **over)


LANGUAGE_CONVENTIONS: dict[str, dict] = {
    # --- Latin-script, plain English-style punctuation ---
    "eng": _lang("Latin", LATIN, caps="sentence-initial + proper nouns + `I`"),
    "fra": _lang("Latin", LATIN),
    "por": _lang("Latin", LATIN),
    "swh": _lang("Latin", LATIN),
    "ind": _lang("Latin", LATIN),
    "zsm": _lang("Latin", LATIN),
    "jav": _lang("Latin", LATIN),
    "vie": _lang("Latin", LATIN, spacing="syllables"),
    "tur": _lang("Latin", LATIN),
    "fil": _lang("Latin", LATIN),
    "ita": _lang("Latin", LATIN),
    "pcm": _lang("Latin", LATIN),
    "hau": _lang("Latin", LATIN),
    "pol": _lang("Latin", LATIN),
    "uzn": _lang("Latin", LATIN),
    "gaz": _lang("Latin", LATIN),
    "deu": _lang("Latin", LATIN, caps="sentence-initial + ALL nouns"),
    "spa": _lang("Latin", LATIN, question="¿?", exclamation="¡!"),
    # --- Cyrillic ---
    "rus": _lang("Cyrillic", CYRILLIC),
    # --- Han / Japanese: scriptio continua, fullwidth marks ---
    "cmn": _lang("Han", HAN),
    "yue": _lang("Han", HAN),
    "wuu": _lang("Han", HAN),
    "hsn": _lang("Han", HAN),
    "nan": _lang("Han", HAN),
    "hak": _lang("Han", HAN),
    "jpn": _lang("Japanese", HAN),
    # --- Korean: Hangul, unicameral, but Latin-style marks and word spaces ---
    "kor": _lang("Hangul", dict(sentence_final=".", question="?", exclamation="!",
                                comma=",", spacing="spaces", case="unicameral",
                                caps="n/a (no case)")),
    # --- Arabic script ---
    "arb": _lang("Arabic", ARABIC),
    "arz": _lang("Arabic", ARABIC),
    "apc": _lang("Arabic", ARABIC),
    "arq": _lang("Arabic", ARABIC),
    "pes": _lang("Arabic", ARABIC),
    "urd": _lang("Arabic", PERSO),
    "pnb": _lang("Arabic", PERSO),
    "pbu": _lang("Arabic", PERSO),
    "snd": _lang("Arabic", PERSO),
    # --- Brahmic, danda-final ---
    "hin": _lang("Devanagari", INDIC_DANDA),
    "mar": _lang("Devanagari", INDIC_DANDA),
    "bho": _lang("Devanagari", INDIC_DANDA),
    "ben": _lang("Bengali", INDIC_DANDA),
    "pan": _lang("Gurmukhi", INDIC_DANDA),
    # --- Brahmic, full-stop-final in modern usage ---
    "tel": _lang("Telugu", INDIC_DOT),
    "tam": _lang("Tamil", INDIC_DOT),
    "guj": _lang("Gujarati", INDIC_DOT),
    "kan": _lang("Kannada", INDIC_DOT),
    "mal": _lang("Malayalam", INDIC_DOT),
    "ory": _lang("Odia", INDIC_DOT),
    # --- Others ---
    "tha": _lang("Thai", dict(sentence_final="(space)", question="(none)",
                              exclamation="!", comma="(space)", spacing="none",
                              case="unicameral", caps="n/a (no case)")),
    "mya": _lang("Myanmar", dict(sentence_final="။", question="?",
                                 exclamation="!", comma="၊", spacing="none",
                                 case="unicameral", caps="n/a (no case)")),
    "amh": _lang("Ethiopic", dict(sentence_final=ETH_FS, question=ETH_Q,
                                  exclamation="!", comma=ETH_COM, spacing="spaces",
                                  case="unicameral", caps="n/a (no case)")),
}

# Outside the top 50; reported as context only, NEVER in the percentages.
CONTEXT_LANGUAGES: dict[str, dict] = {
    "ell": _lang("Greek", LATIN, question=";", case="bicameral",
                 caps="sentence-initial + proper nouns"),
    "hye": _lang("Armenian", LATIN, sentence_final="։", question="՞",
                 exclamation="՜", case="bicameral"),
    "khm": _lang("Khmer", dict(sentence_final="។", question="?",
                               exclamation="!", comma="(space)", spacing="none",
                               case="unicameral", caps="n/a (no case)")),
    "lao": _lang("Lao", dict(sentence_final="(space)", question="?",
                             exclamation="!", comma="(space)", spacing="none",
                             case="unicameral", caps="n/a (no case)")),
    "heb": _lang("Hebrew", dict(sentence_final=".", question="?", exclamation="!",
                                comma=",", spacing="spaces", case="unicameral",
                                caps="n/a (no case)")),
    "kat": _lang("Georgian", dict(sentence_final=".", question="?", exclamation="!",
                                  comma=",", spacing="spaces", case="unicameral",
                                  caps="n/a (Mkhedruli is caseless in modern use)")),
}

# Apostrophe / hyphen notes, area 8. Also knowledge-assembled; there is nothing to
# count here, so these are emitted as zero-weight annotation rows.
APOSTROPHE_HYPHEN_NOTES = [
    ("apostrophe", "elision / possessive marker (`don't`, `l'eau`, `John's`)",
     "'", "English, French, Italian, Catalan, Dutch, Afrikaans"),
    ("apostrophe", "letter of the alphabet - glottal stop or ejective",
     "'", "Hawaiian okina, Guarani, many Latin-script African orthographies"),
    ("apostrophe", "not used at all",
     "", "Han, Japanese, Korean, Thai, Devanagari, Arabic (native text)"),
    ("hyphen", "compound joiner and end-of-line word break",
     "-", "most Latin-script and Cyrillic orthographies"),
    ("hyphen", "reduplication and affix marker",
     "-", "Indonesian/Malay `orang-orang`, Swahili, Tagalog"),
    ("hyphen", "not used at all",
     "", "Han, Japanese, Thai (CJK uses U+30FB / U+FF1D-style marks instead)"),
]

# ---------------------------------------------------------------------------
# END of the knowledge-assembled table.  Everything below is dataset code.
# ---------------------------------------------------------------------------

FIELD_TO_AREA = {
    "sentence_final": "1_sentence_final",
    "question": "2_question_mark",
    "exclamation": "2_exclamation_mark",
    "comma": "3_comma",
    "case": "5_case_system",
    "caps": "5_capitalization_rule",
    "spacing": "6_word_spacing",
}

INHERIT = "↑↑↑"  # CLDR's "same as parent" marker


def ascii_ok(glyph: str) -> bool:
    """Can this option be written in our ASCII Latin orthography?

    An option with no glyph ("no mark at all", "no spaces between words") is
    trivially available - it is the absence of a character, not a character.
    """
    return all(ord(c) < 128 for c in glyph)


# --- CLDR locale parsing ----------------------------------------------------


def parent_locales(supp: Path) -> dict[str, str]:
    """Explicit parent overrides from supplementalData (`en_GB` -> `en_001`)."""
    root = ET.parse(supp).getroot()
    out: dict[str, str] = {}
    for pl in root.iter("parentLocale"):
        parent = pl.get("parent")
        for loc in (pl.get("locales") or "").split():
            out[loc] = parent
    return out


def load_locales(main_dir: Path) -> dict[str, dict]:
    """Raw (unresolved) delimiter and number data per locale file."""
    locales: dict[str, dict] = {}
    for path in sorted(main_dir.glob("*.xml")):
        root = ET.parse(path).getroot()
        rec: dict = {}
        delim = root.find("delimiters")
        if delim is not None:
            for tag in ("quotationStart", "quotationEnd",
                        "alternateQuotationStart", "alternateQuotationEnd"):
                el = delim.find(tag)
                if el is not None and el.text:
                    rec[tag] = el.text
        numbers = root.find("numbers")
        if numbers is not None:
            dns = numbers.find("defaultNumberingSystem")
            if dns is not None and dns.text:
                rec["defaultNumberingSystem"] = dns.text
            for sym in numbers.findall("symbols"):
                ns = sym.get("numberSystem")
                for tag in ("decimal", "group"):
                    el = sym.find(tag)
                    if el is not None and el.text:
                        rec[f"{tag}@{ns}"] = el.text
            for fmts in numbers.findall("decimalFormats"):
                ns = fmts.get("numberSystem")
                for length in fmts.findall("decimalFormatLength"):
                    if length.get("type"):  # "long"/"short" = compact notation
                        continue
                    pat = length.find("./decimalFormat/pattern")
                    if pat is not None and pat.text:
                        rec[f"pattern@{ns}"] = pat.text
        locales[path.stem] = rec
    return locales


class LocaleData:
    """CLDR locale data with inheritance (`^^^` and parentLocales) resolved."""

    def __init__(self, main_dir: Path, supp: Path):
        self.raw = load_locales(main_dir)
        self.parents = parent_locales(supp)
        self._cache: dict[tuple[str, str], str | None] = {}

    def parent(self, loc: str) -> str | None:
        if loc == "root":
            return None
        if loc in self.parents:
            return self.parents[loc]
        return loc.rsplit("_", 1)[0] if "_" in loc else "root"

    def get(self, loc: str, key: str) -> str | None:
        hit = self._cache.get((loc, key))
        if hit is not None:
            return hit
        cur: str | None = loc
        while cur is not None:
            val = self.raw.get(cur, {}).get(key)
            if val is not None and val != INHERIT:
                self._cache[(loc, key)] = val
                return val
            cur = self.parent(cur)
        return None

    def states(self, loc: str, key: str) -> bool:
        """Did CLDR actually survey this locale for this field?

        A `^^^` entry in a locale file is a positive statement ("checked, same as
        the parent"), so it counts as stated. A locale whose whole chain is silent
        below `root` was never surveyed and silently picks up root's fallback -
        that weight inflates whatever root happens to say (`" "`, `.`, `,`), so it
        is tracked separately.
        """
        cur: str | None = loc
        while cur is not None and cur != "root":
            if key in self.raw.get(cur, {}):
                return True
            cur = self.parent(cur)
        return False

    def numbering_system(self, loc: str) -> str:
        return self.get(loc, "defaultNumberingSystem") or "latn"

    def separators(self, loc: str, ns: str) -> tuple[str | None, str | None, str | None]:
        """Decimal, grouping and pattern for a numbering system.

        Falls back to `latn` when the numbering system has no symbols anywhere in
        the chain, which is what CLDR itself does: `beng`, `deva`, `mymr` etc.
        define digits but not separators, so Bengali writes Bengali digits with
        the Latin `.` and `,`.
        """
        return (self.get(loc, f"decimal@{ns}") or self.get(loc, "decimal@latn"),
                self.get(loc, f"group@{ns}") or self.get(loc, "group@latn"),
                self.get(loc, f"pattern@{ns}") or self.get(loc, "pattern@latn"))


def locale_populations(supp: Path) -> list[tuple[str, str, float]]:
    """(cldr_language_subtag, territory, total speakers) from supplementalData.

    Same arithmetic as populations.cldr_totals(), but kept at the territory grain
    so that es_MX / es_AR can differ. Reconciled against cldr_totals() in main().
    """
    root = ET.parse(supp).getroot()
    out: list[tuple[str, str, float]] = []
    for terr in root.iter("territory"):
        pop = float(terr.get("population", 0) or 0)
        if pop <= 0:
            continue
        code = terr.get("type")
        for lp in terr.findall("languagePopulation"):
            pct = float(lp.get("populationPercent", 0) or 0)
            n = pop * pct / 100.0
            if n > 0:
                out.append((lp.get("type"), code, n))
    return out


def to_iso3(subtag: str, part1: dict[str, str], macros: set[str]) -> str:
    """CLDR language subtag -> ISO 639-3, matching populations.cldr_totals()."""
    base = subtag.split("_")[0]
    iso3 = part1.get(base, base) if len(base) == 2 else base
    if iso3 in macros or iso3 in MACRO_MAP:
        iso3 = MACRO_MAP.get(iso3, iso3)
    return iso3


# --- classification of CLDR values -----------------------------------------

SPACE_CHARS = {" ": "NBSP", " ": "NNBSP", " ": "thin space",
               " ": "space", "’": "apostrophe"}


def sep_label(ch: str | None) -> str:
    if ch is None:
        return "(missing)"
    if ch in SPACE_CHARS:
        return f"{SPACE_CHARS[ch]} (U+{ord(ch):04X})"
    return ch


def grouping_label(pattern: str | None) -> str:
    if not pattern:
        return "(missing)"
    intpart = pattern.split(".")[0]
    groups = intpart.split(",")
    if len(groups) <= 1:
        return "no grouping"
    sizes = [len(g) for g in groups[1:]]
    if sizes == [3]:
        return "3-digit (1,000,000)"
    if sizes == [2, 3]:
        return "Indian 2-2-3 (10,00,000)"
    return f"other ({intpart})"


# --- table assembly ---------------------------------------------------------


# Areas whose "option" is a description, not a character: an ASCII-availability
# flag would be meaningless (every one of them is expressible in ASCII).
NON_GLYPH_AREAS = {"5_case_system", "5_capitalization_rule", "6_word_spacing",
                   "7_grouping_pattern"}


def rank_rows(area: str, counts: dict[str, dict], denom_w: float, denom_l1: float,
              world_w: float, source: str, glyphs: dict[str, str],
              unit: str, denom_stated: float = 0.0) -> list[dict]:
    rows = []
    for opt, agg in counts.items():
        glyph = glyphs.get(opt, opt)
        rows.append({
            "area": area,
            "option": opt,
            "example": glyph,
            "ascii_available": None if area in NON_GLYPH_AREAS else ascii_ok(glyph),
            "source": source,
            "unit": unit,
            "n_units": agg["n"],
            "pct_total_weighted": 100 * agg["w"] / denom_w if denom_w else 0.0,
            "pct_l1_weighted": (100 * agg["l1"] / denom_l1
                                if denom_l1 and agg["l1"] is not None else None),
            "pct_world_total_weighted": 100 * agg["w"] / world_w if world_w else 0.0,
            "pct_stated_only": (100 * agg.get("w_stated", 0.0) / denom_stated
                                if denom_stated else None),
            "top_examples": ", ".join(agg["names"][:5]),
        })
    return sorted(rows, key=lambda r: -r["pct_total_weighted"])


def main() -> None:
    if not CLDR_MAIN.exists():
        raise FileNotFoundError(
            f"{CLDR_MAIN} missing - clone CLDR (see README data table):\n"
            f"  git clone --depth 1 --filter=blob:none --sparse "
            f"https://github.com/unicode-org/cldr data/raw/cldr && "
            f"cd data/raw/cldr && git sparse-checkout set common/main"
        )

    part1, macros = _iso_tables(ISO_DIR)
    l1 = read_l1_speakers(L1_CSV)
    l1_by_iso = dict(zip(l1["iso639_3"], l1["l1_speakers"].astype(float)))
    name_by_iso = dict(zip(l1["iso639_3"], l1["name"]))
    world_l1 = float(l1["l1_speakers"].sum())

    totals = cldr_totals(CLDR_SUPP, ISO_DIR)
    world_total = sum(totals.values())
    print(f"World weights: {world_total / 1e9:.3f}B total-speaker, "
          f"{world_l1 / 1e9:.3f}B L1")

    # ---- knowledge-assembled areas -------------------------------------
    ranked = sorted(totals.items(), key=lambda kv: -kv[1])[:TOP_N]
    ranked_isos = [k for k, _ in ranked]
    missing = [k for k in ranked_isos if k not in LANGUAGE_CONVENTIONS]
    if missing:
        raise SystemExit(f"top-{TOP_N} languages not annotated: {missing}")
    set_w = sum(totals[k] for k in ranked_isos)
    set_l1 = sum(l1_by_iso.get(k, 0.0) for k in ranked_isos)
    print(f"Knowledge set: top {TOP_N} languages, {set_w / 1e9:.3f}B total-speaker "
          f"weight = {100 * set_w / world_total:.1f}% of world")

    rows: list[dict] = []
    for field, area in FIELD_TO_AREA.items():
        counts: dict[str, dict] = defaultdict(
            lambda: {"n": 0, "w": 0.0, "l1": 0.0, "names": []})
        for iso in ranked_isos:
            opt = LANGUAGE_CONVENTIONS[iso][field]
            agg = counts[opt]
            agg["n"] += 1
            agg["w"] += totals[iso]
            agg["l1"] += l1_by_iso.get(iso, 0.0)
            agg["names"].append(name_by_iso.get(iso, iso))
        for agg in counts.values():
            order = {n: totals.get(i, 0) for i, n in
                     ((i, name_by_iso.get(i, i)) for i in ranked_isos)}
            agg["names"].sort(key=lambda n: -order.get(n, 0))
        rows += rank_rows(area, counts, set_w, set_l1, world_total,
                          "knowledge", {}, "languages")

    # context languages: listed, never counted
    for iso, conv in CONTEXT_LANGUAGES.items():
        for field, area in FIELD_TO_AREA.items():
            rows.append({
                "area": area, "option": conv[field], "example": conv[field],
                "ascii_available": ascii_ok(conv[field]),
                "source": "knowledge (context, excluded from %)",
                "unit": "languages", "n_units": 1,
                "pct_total_weighted": None, "pct_l1_weighted": None,
                "pct_world_total_weighted": 100 * totals.get(iso, 0.0) / world_total,
                "top_examples": name_by_iso.get(iso, iso),
            })

    # ---- CLDR-derived areas --------------------------------------------
    ld = LocaleData(CLDR_MAIN, CLDR_SUPP)
    pops = locale_populations(CLDR_SUPP)

    # reconcile with the project's per-language totals
    check: Counter[str] = Counter()
    for subtag, _terr, n in pops:
        check[to_iso3(subtag, part1, macros)] += n
    drift = max(abs(check[k] - v) for k, v in totals.items())
    assert drift < 1.0, f"territory-grain weights disagree with cldr_totals by {drift}"
    print(f"Reconciled with populations.cldr_totals(): max drift {drift:.4f} speakers")

    cldr_w = sum(n for _, _, n in pops)
    quote_counts: dict[str, dict] = defaultdict(
        lambda: {"n": 0, "w": 0.0, "w_stated": 0.0, "l1": None, "names": []})
    alt_counts: dict[str, dict] = defaultdict(
        lambda: {"n": 0, "w": 0.0, "w_stated": 0.0, "l1": None, "names": []})
    dec_counts: dict[str, dict] = defaultdict(
        lambda: {"n": 0, "w": 0.0, "w_stated": 0.0, "l1": None, "names": []})
    dec_latn: dict[str, dict] = defaultdict(
        lambda: {"n": 0, "w": 0.0, "w_stated": 0.0, "l1": None, "names": []})
    grp_counts: dict[str, dict] = defaultdict(
        lambda: {"n": 0, "w": 0.0, "w_stated": 0.0, "l1": None, "names": []})
    combo_counts: dict[str, dict] = defaultdict(
        lambda: {"n": 0, "w": 0.0, "w_stated": 0.0, "l1": None, "names": []})
    seen: dict[str, set[str]] = defaultdict(set)
    glyph_of: dict[str, str] = {}  # readable label -> the actual characters
    stated_w: Counter[str] = Counter()  # weight CLDR actually surveyed, per field

    for subtag, terr, n in pops:
        loc = f"{subtag}_{terr}"
        iso = to_iso3(subtag, part1, macros)
        label = f"{name_by_iso.get(iso, iso)} ({terr})"

        qs, qe = ld.get(loc, "quotationStart"), ld.get(loc, "quotationEnd")
        aqs, aqe = (ld.get(loc, "alternateQuotationStart"),
                    ld.get(loc, "alternateQuotationEnd"))
        ns = ld.numbering_system(loc)
        dec, grp, pat = ld.separators(loc, ns)
        ldec, lgrp, lpat = ld.separators(loc, "latn")

        q_stated = ld.states(loc, "quotationStart")
        n_stated = ld.states(loc, f"decimal@{ns}") or ld.states(loc, "decimal@latn")
        if q_stated:
            stated_w["quotes"] += n
        if n_stated:
            stated_w["numbers"] += n

        for counts, key, glyph, stated in (
            (quote_counts, f"{qs} {qe}" if qs else "(missing)",
             f"{qs or ''}{qe or ''}", q_stated),
            (alt_counts, f"{aqs} {aqe}" if aqs else "(missing)",
             f"{aqs or ''}{aqe or ''}", q_stated),
            (dec_counts, f"decimal {sep_label(dec)} / group {sep_label(grp)}"
                         f"  [{ns} digits]", f"{dec or ''}{grp or ''}", n_stated),
            (dec_latn, f"decimal {sep_label(ldec)} / group {sep_label(lgrp)}",
             f"{ldec or ''}{lgrp or ''}", n_stated),
            (grp_counts, grouping_label(pat or lpat), "", n_stated),
            (combo_counts, f"1{sep_label(lgrp)}000{ldec or '?'}50",
             f"1{lgrp or ''}000{ldec or ''}50", n_stated),
        ):
            glyph_of[key] = glyph
            agg = counts[key]
            agg["w"] += n
            if stated:
                agg["w_stated"] += n
            if label not in seen[f"{id(counts)}|{key}"]:
                seen[f"{id(counts)}|{key}"].add(label)
                agg["n"] += 1
                agg["names"].append(label)

    for counts in (quote_counts, alt_counts, dec_counts, dec_latn, grp_counts,
                   combo_counts):
        for agg in counts.values():
            agg["names"].sort()

    print(f"CLDR states a quotation convention for "
          f"{100 * stated_w['quotes'] / cldr_w:.1f}% of the weight and a number "
          f"format for {100 * stated_w['numbers'] / cldr_w:.1f}%; the rest silently "
          f"inherits root's fallback (see pct_stated_only)")

    for area, counts, field in (
        ("4_quotation_primary", quote_counts, "quotes"),
        ("4_quotation_alternate", alt_counts, "quotes"),
        ("7_number_default_digits", dec_counts, "numbers"),
        ("7_number_latin_digits", dec_latn, "numbers"),
        ("7_grouping_pattern", grp_counts, "numbers"),
        ("7_number_example", combo_counts, "numbers"),
    ):
        rows += rank_rows(area, counts, cldr_w, 0.0, cldr_w, "cldr", glyph_of,
                          "language x territory locales", stated_w[field])

    # ---- area 8, annotation only ---------------------------------------
    for area, opt, glyph, examples in APOSTROPHE_HYPHEN_NOTES:
        rows.append({
            "area": f"8_{area}", "option": opt, "example": glyph,
            "ascii_available": ascii_ok(glyph), "source": "knowledge (note only)",
            "unit": "-", "n_units": None, "pct_total_weighted": None,
            "pct_l1_weighted": None, "pct_world_total_weighted": None,
            "top_examples": examples,
        })

    out = pd.DataFrame(rows)
    for c in ("pct_total_weighted", "pct_l1_weighted", "pct_world_total_weighted",
              "pct_stated_only"):
        out[c] = out[c].astype(float).round(3)
    out["n_units"] = out["n_units"].astype("Int64")
    out = out.sort_values(
        ["area", "pct_total_weighted"], ascending=[True, False], na_position="last")
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(OUT_CSV, index=False)
    print(f"\nWrote {OUT_CSV}: {len(out)} rows")

    for area in sorted(out["area"].unique()):
        t = out[(out["area"] == area) & out["pct_total_weighted"].notna()]
        if t.empty:
            t = out[out["area"] == area]
        print(f"\n--- {area} ---")
        print(t[["option", "example", "ascii_available", "n_units",
                 "pct_total_weighted", "pct_l1_weighted", "pct_stated_only"]]
              .head(12).to_string(index=False))


if __name__ == "__main__":
    main()
