"""WOLD loanword pipeline: build attested source->recipient adaptation pairs.

This is step zero of the cost-learning study (notes/cost-learning-spec.md, R1).
It rebuilds the WOLD cleaning + validation code that produced the recorded
"13,779 clean pairs, AUC 0.923" figure but which was never committed, and emits
a committed pair table that every downstream script reads.

WHAT A "PAIR" IS
  WOLD records, for each borrowed word in a recipient language, the donor-
  language string it came from (`borrowings.csv:Source_word`). The recipient
  side is a real transcription (`forms.csv:Segments`, CLTS-tokenized); the
  donor side is a raw orthography/transliteration string in whatever convention
  the contributing author used. A pair is (source string -> recipient word),
  i.e. one attested act of loanword adaptation.

INPUTS
  data/raw/wold/cldf/{borrowings,forms,languages}.csv   (git clone, see README)
  Recorded dataset commit is written into the output CSV header comment and
  printed at run time. README pins 0df955a; this run used whatever HEAD the
  shallow clone gave (printed). Pair counts are reported per version so
  version-sensitivity is visible rather than assumed away.

OUTPUT
  data/processed/wold_pairs.csv  - one row per surviving pair:
      recipient, recipient_glottocode, family, macroarea,
      donor, source_raw, source_ipa, target_form, target_ipa,
      n_src_segs, n_tgt_segs, source_certain, source_relation

JUDGMENT CALLS BAKED INTO THE FILTER (all of them cost pairs; each is a choice)

  Row-level exclusions, in order:
  1. `Source_word` empty                      -> drop. (21,624 -> 20,624)
  2. `Source_certain == 'no'`                 -> drop. WOLD's own uncertainty
     flag; a wrong etymology is a mislabeled training example.
  3. `Source_relation == 'earlier'`           -> kept in THIS table, excluded
     downstream. These reached the recipient via an intermediate language, so
     the recorded donor string is not the form the recipient actually adapted.
     This table keeps them (16,687 rows) so the choice is reversible; the
     cost-learning study restricts to `immediate` (13,595 rows) and says so.
     A priori reason: indirect borrowing = less direct phonological mapping.
     Confirmation (not the reason): under the legacy protocol the `immediate`
     subset separates at AUC 0.909 vs 0.899 for the full set, i.e. the
     `earlier` rows are measurably noisier labels.
  4. Comma/semicolon-separated alternates     -> first alternate only. WOLD
     uses these for spelling variants and for "form, gloss" pairs.
  5. Parenthesised and bracketed material     -> stripped. It is optional
     material (`ḏurrīya(t)`) or an editorial note.
  6. Contains `*`                             -> drop (reconstructed proto-form,
     not an attested string).
  7. Contains `?`                             -> drop (author-flagged doubt).
  8. Still contains a space, hyphen or `+`    -> drop (phrase, or a morpheme-
     segmented citation form; we cannot tell where the word boundary is).
  9. Contains a Unicode "other letter" (Lo)   -> drop. This removes Han
     characters, Arabic script, Devanagari etc. — scripts we have no
     transliteration for.

  Transliteration (the big judgment call): donor strings are in MIXED
  orthographies and there is no per-donor romanisation table in WOLD. We apply
  ONE donor-agnostic mapping, chosen for the majority convention across WOLD's
  donor pool (which is transliteration-heavy: Arabic, Berber, Sanskrit,
  Russian, plus Romance/Germanic orthography):
      š->ʃ  ž->ʒ  č->tʃ  ǧ/ǰ->dʒ  ñ->ɲ  ġ->ɣ  ḥ->ħ  ʿ/ˁ/ʻ->ʕ  ʾ/ˀ->ʔ
      c->k   (right for Latin/Spanish/Berber; WRONG for Romanian/Italian /tʃ/)
      y->j   (glide; wrong for Spanish-orthography rows where y is a vowel)
      j->j   (glide: right for Latin/German/Hungarian/most transliterations;
              WRONG for Spanish /x/, French/English /ʒ~dʒ/)
      x->x   (velar fricative: right for Arabic/Berber/Russian translit;
              WRONG for Spanish /x/-as-j and English /ks/)
      q->q, g->ɡ, ’/'->ʼ, :->ː, digits and remaining marks dropped
  Remaining combining diacritics (acute, grave, macron, breve, diaeresis,
  circumflex, cedilla, dot-below, tilde) are STRIPPED after the digraph
  mappings above: they encode stress, vowel length, emphatics and nasality that
  the recipient side mostly does not record either.
  NO digraph expansion (sh/ch/kh/gh/th) is attempted: it is right for
  transliterated Semitic and wrong for English/Hungarian, and we have no donor
  signal to condition on. Consequence: donor-specific systematic mis-mappings
  are real noise in this dataset — see notes/cost-learning.md "orthography
  noise" for why this bounds how much we should trust any single learned
  substitution weight.

  Recipient side: `Segments` is CLTS-tokenized. We strip CLTS grapheme
  annotations (`á/a` -> `a`), tone digits (⁵⁵, ²¹⁴), the `+` morpheme boundary,
  and re-tokenize the joined string with panphon (which splits affricates like
  tʃ into t+ʃ and drops prenasalisation on ⁿɡ — documented losses).

  Post-transliteration filters:
  10. panphon must tokenize the string with >= 90% of its characters consumed
      (guards against strings that are mostly unknown glyphs).
  11. 2 <= n_segments <= 14 on both sides.
  12. Length ratio between the two sides must be <= 3x (guards against a
      citation form aligned to a single-syllable recipient stub).

VALIDATION (R1(a): legacy-protocol reproduction)
  Reproduces the original "AUC 0.923" protocol as best it can be reconstructed:
  a random sample of pairs, controls drawn from the GLOBAL source pool (not
  within recipient), scored with metric.similarity under panphon's default
  weights, no recipient grouping. This exists ONLY to confirm the pipeline
  rebuild is faithful; it is not a bar for anything. The honest
  recipient-grouped baseline is R1(b), in scripts/cost_learning.py.

Usage: uv run python scripts/wold_pipeline.py
"""

from __future__ import annotations

import random
import re
import subprocess
import sys
import unicodedata
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from interlang import metric  # noqa: E402

WOLD = ROOT / "data" / "raw" / "wold" / "cldf"
OUT_CSV = ROOT / "data" / "processed" / "wold_pairs.csv"

MAX_SEGS = 14
MIN_SEGS = 2
MAX_LEN_RATIO = 3.0
MIN_CHAR_COVERAGE = 0.90

# --- transliteration ------------------------------------------------------
# Applied to the NFC form before diacritic stripping, so that letter+caron
# digraph conventions (š ž č ǧ) survive.
_DIGRAPH_MAP = {
    "š": "ʃ", "Š": "ʃ", "ş": "ʃ", "ś": "ʃ",
    "ž": "ʒ", "Ž": "ʒ",
    "č": "tʃ", "Č": "tʃ", "ć": "tʃ",
    "ǧ": "dʒ", "ǰ": "dʒ", "ğ": "ɣ", "ġ": "ɣ",
    "ñ": "ɲ", "ń": "ɲ",
    "ḥ": "ħ", "ḫ": "x", "ẖ": "x",
    "ʿ": "ʕ", "ˁ": "ʕ", "ʻ": "ʕ", "ˤ": "ʕ",
    "ʾ": "ʔ", "ˀ": "ʔ", "ʼ": "ʔ",
    "þ": "θ", "ð": "ð", "ß": "s", "æ": "æ", "ø": "ø", "œ": "ø",
    "å": "o", "ł": "w",
}
# single-letter orthography -> IPA, applied after diacritic stripping
_LETTER_MAP = str.maketrans({
    "g": "ɡ", "y": "j", "c": "k", "’": "ʼ", "'": "ʼ", "ʔ": "ʔ", ":": "ː",
})
# combining marks judged orthographic (stress / length / emphatic / nasality)
_STRIP_MARKS = set("̧́̀̄̆̈̂̌̋"
                   "̣̱̮̰̤̥̹̞̃"
                   "̴̵̨̠̩̇̊͜͡")


def transliterate(s: str) -> str:
    """Donor-agnostic orthography -> quasi-IPA. See module docstring."""
    s = unicodedata.normalize("NFC", s)
    for k, v in _DIGRAPH_MAP.items():
        s = s.replace(k, v)
    s = s.lower()
    d = unicodedata.normalize("NFD", s)
    d = "".join(ch for ch in d if ch not in _STRIP_MARKS)
    d = unicodedata.normalize("NFC", d)
    return d.translate(_LETTER_MAP)


_ALT_SPLIT = re.compile(r"[,;/]")
_PAREN = re.compile(r"\([^)]*\)|\[[^\]]*\]|\{[^}]*\}")


def clean_source(raw: str) -> tuple[str | None, str]:
    """Structural cleaning of a WOLD Source_word. Returns (string, reason)."""
    s = str(raw)
    s = _ALT_SPLIT.split(s)[0]
    s = _PAREN.sub("", s).strip()
    if not s:
        return None, "empty"
    if "*" in s:
        return None, "reconstruction"
    if "?" in s or "!" in s:
        return None, "author_doubt"
    if re.search(r"[\s\-+=.]", s):
        return None, "multiword"
    if any(unicodedata.category(ch) == "Lo" for ch in unicodedata.normalize("NFD", s)):
        return None, "non_latin_script"
    if any(ch.isdigit() for ch in s):
        return None, "contains_digit"
    return s, "ok"


_CLTS_ANNOT = re.compile(r"^.*/")
_TONE = re.compile(r"[⁰-₟²³¹]+")


def clean_target(segments_field: str) -> str:
    """CLTS `Segments` field -> a plain IPA string for panphon."""
    out = []
    for tok in str(segments_field).split():
        if tok in ("+", "_"):
            continue
        tok = _CLTS_ANNOT.sub("", tok)  # 'á/a' -> 'a'
        tok = _TONE.sub("", tok)
        if tok:
            out.append(tok)
    return "".join(out)


def to_ipa_segments(s: str) -> list[str]:
    """panphon tokenization + the character-coverage guard."""
    if not s:
        return []
    segs = metric.segments(s)
    kept = sum(len(x) for x in segs)
    total = len(s.translate(metric._GLYPH_FIXES))
    if total == 0 or kept / total < MIN_CHAR_COVERAGE:
        return []
    return segs


def load_pairs(path: Path = OUT_CSV) -> pd.DataFrame:
    """Read the committed pair table.

    `keep_default_na=False` matters: the donor string "Null" -> "null" and the
    Japanese recipient "na" would otherwise be parsed as missing values.
    """
    return pd.read_csv(path, keep_default_na=False, na_values=[])


def dataset_commit(path: Path) -> str:
    try:
        return subprocess.run(
            ["git", "-C", str(path), "rev-parse", "HEAD"],
            capture_output=True, text=True, check=True).stdout.strip()[:12]
    except Exception:
        return "unknown"


def build() -> tuple[pd.DataFrame, dict[str, int]]:
    borrowings = pd.read_csv(WOLD / "borrowings.csv")
    forms = pd.read_csv(WOLD / "forms.csv", low_memory=False)
    langs = pd.read_csv(WOLD / "languages.csv")

    df = borrowings.merge(
        forms[["ID", "Language_ID", "Form", "Segments"]],
        left_on="Target_Form_ID", right_on="ID", how="left", suffixes=("", "_form"))
    df = df.merge(
        langs[["ID", "Glottocode", "Family", "Macroarea"]].rename(columns={"ID": "Language_ID"}),
        on="Language_ID", how="left")

    drops: dict[str, int] = {"total_borrowings": len(df)}
    rows = []
    for r in df.itertuples(index=False):
        raw = getattr(r, "Source_word")
        if not isinstance(raw, str) or not raw.strip():
            drops["no_source_word"] = drops.get("no_source_word", 0) + 1
            continue
        if getattr(r, "Source_certain") == "no":
            drops["source_uncertain"] = drops.get("source_uncertain", 0) + 1
            continue
        cleaned, reason = clean_source(raw)
        if cleaned is None:
            drops[reason] = drops.get(reason, 0) + 1
            continue
        src_ipa_raw = transliterate(cleaned)
        src_segs = to_ipa_segments(src_ipa_raw)
        if not src_segs:
            drops["src_untokenizable"] = drops.get("src_untokenizable", 0) + 1
            continue
        tgt_ipa_raw = clean_target(getattr(r, "Segments"))
        tgt_segs = to_ipa_segments(tgt_ipa_raw)
        if not tgt_segs:
            drops["tgt_untokenizable"] = drops.get("tgt_untokenizable", 0) + 1
            continue
        ns, nt = len(src_segs), len(tgt_segs)
        if not (MIN_SEGS <= ns <= MAX_SEGS) or not (MIN_SEGS <= nt <= MAX_SEGS):
            drops["length_bounds"] = drops.get("length_bounds", 0) + 1
            continue
        if max(ns, nt) / min(ns, nt) > MAX_LEN_RATIO:
            drops["length_ratio"] = drops.get("length_ratio", 0) + 1
            continue
        rows.append(dict(
            recipient=getattr(r, "Language_ID"),
            recipient_glottocode=getattr(r, "Glottocode"),
            family=getattr(r, "Family"),
            macroarea=getattr(r, "Macroarea"),
            donor=getattr(r, "Source_languoid"),
            source_raw=raw,
            source_ipa="".join(src_segs),
            target_form=getattr(r, "Form"),
            target_ipa="".join(tgt_segs),
            n_src_segs=ns,
            n_tgt_segs=nt,
            source_certain=getattr(r, "Source_certain"),
            source_relation=getattr(r, "Source_relation"),
        ))
    return pd.DataFrame(rows), drops


# --- R1(a) legacy-protocol reproduction ------------------------------------

def auc(pos: list[float], neg: list[float]) -> float:
    """Mann-Whitney AUC (ties count 0.5)."""
    scores = [(s, 1) for s in pos] + [(s, 0) for s in neg]
    scores.sort(key=lambda x: x[0])
    ranks, i = {}, 0
    total = 0.0
    while i < len(scores):
        j = i
        while j < len(scores) and scores[j][0] == scores[i][0]:
            j += 1
        avg_rank = (i + j + 1) / 2.0  # 1-based average rank of the tie block
        for k in range(i, j):
            if scores[k][1] == 1:
                total += avg_rank
        i = j
    del ranks
    n_pos, n_neg = len(pos), len(neg)
    return (total - n_pos * (n_pos + 1) / 2) / (n_pos * n_neg)


def legacy_validation(pairs: pd.DataFrame, n: int = 1500, seed: int = 0) -> dict:
    """The original loose protocol: global shuffle, sampled pairs, no grouping."""
    rng = random.Random(seed)
    idx = rng.sample(range(len(pairs)), min(n, len(pairs)))
    sub = pairs.iloc[idx].reset_index(drop=True)
    sources = sub["source_ipa"].tolist()
    pos, neg = [], []
    for i, row in enumerate(sub.itertuples(index=False)):
        pos.append(metric.similarity(row.source_ipa, row.target_ipa))
        j = rng.randrange(len(sources))
        while j == i:
            j = rng.randrange(len(sources))
        neg.append(metric.similarity(sources[j], row.target_ipa))
    return dict(n=len(pos), mean_attested=sum(pos) / len(pos),
                mean_control=sum(neg) / len(neg), auc=auc(pos, neg))


def main() -> None:
    commit = dataset_commit(WOLD.parent)
    print(f"WOLD dataset commit: {commit}  (README pins 0df955a)")
    pairs, drops = build()
    print("\nFilter attrition:")
    for k, v in drops.items():
        print(f"  {k:24s} {v:6d}")
    print(f"\nsurviving pairs: {len(pairs)}  "
          f"recipients: {pairs['recipient'].nunique()}  "
          f"donors: {pairs['donor'].nunique()}")
    print(f"  of which source_relation=='immediate': "
          f"{(pairs['source_relation'] == 'immediate').sum()}")
    print("\npairs per recipient (head/tail):")
    vc = pairs["recipient"].value_counts()
    print(vc.head(6).to_string())
    print("  ...")
    print(vc.tail(6).to_string())
    print(f"  median {vc.median():.0f}")

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    pairs.to_csv(OUT_CSV, index=False)
    print(f"\nwrote {OUT_CSV}")

    print("\nR1(a) legacy-protocol reproduction "
          "(global shuffle, n=1500 sampled, no recipient grouping, default panphon "
          "weights) — recorded target: attested 0.78 / control 0.46 / AUC 0.923")
    variants = {
        "all rows": pairs,
        "immediate only": pairs[pairs["source_relation"] == "immediate"],
    }
    for label, sub in variants.items():
        sub = sub.reset_index(drop=True)
        res = [legacy_validation(sub, seed=s) for s in (0, 1, 2)]
        print(f"  {label:16s} n={len(sub):6d}  attested "
              f"{sum(r['mean_attested'] for r in res) / 3:.3f}  control "
              f"{sum(r['mean_control'] for r in res) / 3:.3f}  AUC "
              f"{sum(r['auc'] for r in res) / 3:.4f}  "
              f"(per-seed {[round(r['auc'], 4) for r in res]})")


if __name__ == "__main__":
    main()
