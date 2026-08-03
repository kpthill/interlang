"""Recognizability metric v0.

Scores how likely a listener is to recognize a word of our constructed
language as the word they already know (in some language of theirs).

v0 approach:
  - Words are IPA strings, tokenized into segments by panphon.
  - Base distance: panphon weighted feature edit distance (alignment-based;
    substitution cost grows with articulatory feature disagreement, so
    /d/->/t/ is cheap and /d/->/f/ is expensive).
  - Similarity is normalized to [0, 1]: 1.0 = identical, 0.0 = at least as
    far apart as two unrelated words of this length.
  - Optional listener conditioning: before comparing, project both words
    onto the listener's native phoneme inventory (each segment maps to its
    nearest native category in feature space). Distinctions the listener
    cannot hear then cost nothing.
"""

from __future__ import annotations

from functools import lru_cache

import panphon
import panphon.distance

_ft = panphon.FeatureTable()
_dist = panphon.distance.Distance()


# ASCII lookalikes that panphon would otherwise silently drop.
_GLYPH_FIXES = str.maketrans({"g": "ɡ", ":": "ː", "'": "ʼ"})


def segments(ipa: str) -> list[str]:
    """Tokenize an IPA string into panphon segments (drops unknown chars)."""
    return _ft.ipa_segs(ipa.translate(_GLYPH_FIXES))


def _deletion_cost(ipa: str) -> float:
    """Distance from a word to the empty string under the same metric."""
    return _dist.weighted_feature_edit_distance(ipa, "")


def similarity(a: str, b: str) -> float:
    """Normalized recognizability in [0, 1] between two IPA strings.

    Normalizer: the cost of deleting the longer word entirely, i.e. the
    distance between the longer word and silence. Anything scoring 0 by
    this measure is "no more similar than an arbitrary word".
    """
    a_segs, b_segs = "".join(segments(a)), "".join(segments(b))
    if not a_segs or not b_segs:
        return 0.0
    d = _dist.weighted_feature_edit_distance(a_segs, b_segs)
    norm = max(_deletion_cost(a_segs), _deletion_cost(b_segs))
    if norm <= 0:
        return 0.0
    return max(0.0, 1.0 - d / norm)


@lru_cache(maxsize=100_000)
def _nearest_in_inventory(seg: str, inventory: tuple[str, ...]) -> str:
    """Map one segment to the perceptually nearest phoneme in an inventory."""
    if seg in inventory:
        return seg
    best, best_d = seg, float("inf")
    for phon in inventory:
        d = _dist.weighted_feature_edit_distance(seg, phon)
        if d < best_d:
            best, best_d = phon, d
    return best


def project(ipa: str, inventory: tuple[str, ...]) -> str:
    """Assimilate a word into a listener's phoneme inventory.

    Models first-pass loanword perception: each segment is heard as the
    nearest native category. (No epenthesis/deletion modeling in v0.)
    """
    return "".join(_nearest_in_inventory(s, inventory) for s in segments(ipa))


def recognizability(
    candidate: str,
    known_word: str,
    listener_inventory: tuple[str, ...] | None = None,
) -> float:
    """How recognizable is `candidate` to someone who knows `known_word`?

    Both words are IPA. If `listener_inventory` is given (tuple of IPA
    phonemes, e.g. from PHOIBLE), both words are first assimilated into
    that inventory, so contrasts the listener lacks are free.
    """
    if listener_inventory is not None:
        candidate = project(candidate, listener_inventory)
        known_word = project(known_word, listener_inventory)
    return similarity(candidate, known_word)
