"""Recognizability metric v0.

Scores how likely a listener is to recognize a word of our constructed
language as the word they already know (in some language of theirs).

STATUS 2026-08-04: v0 is still the DEFAULT and the deployed metric.  The
cost-learning study (notes/cost-learning.md) fitted an alternative cost vector
to WOLD's attested loanword adaptations; it wins decisively on held-out
recipient AUC but fails two of the five guardrails, so it is NOT the default.
Every function here takes an optional `params` argument: pass
`np.loadtxt`-style values from `data/processed/learned_costs.csv` (or
`interlang.costs.FeatureWeightCosts.default_params()`) to score with the
learned costs instead.  `params=None` reproduces v0 exactly.

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


def similarity(a: str, b: str, params=None) -> float:
    """Normalized recognizability in [0, 1] between two IPA strings.

    Normalizer: the cost of deleting the longer word entirely, i.e. the
    distance between the longer word and silence. Anything scoring 0 by
    this measure is "no more similar than an arbitrary word".

    `params`: optional learned cost vector (see module docstring). None uses
    panphon's default weights, i.e. exactly v0.
    """
    if params is not None:
        from . import costs as _costs
        return _costs.similarity(segments(a), segments(b), params)
    a_segs, b_segs = "".join(segments(a)), "".join(segments(b))
    if not a_segs or not b_segs:
        return 0.0
    d = _dist.weighted_feature_edit_distance(a_segs, b_segs)
    norm = max(_deletion_cost(a_segs), _deletion_cost(b_segs))
    if norm <= 0:
        return 0.0
    return max(0.0, 1.0 - d / norm)


@lru_cache(maxsize=100_000)
def _nearest_in_inventory(seg: str, inventory: tuple[str, ...],
                          params_key: tuple[float, ...] | None = None) -> str:
    """Map one segment to the perceptually nearest phoneme in an inventory."""
    if seg in inventory:
        return seg
    if params_key is not None:
        from . import costs as _costs
        import numpy as _np
        space = _costs.SegmentSpace([seg, *inventory])
        sub = _costs.FeatureWeightCosts(
            space, _np.asarray(params_key[:_costs.N_FEATURES])).sub_matrix()
        row = [(p, sub[space.index[seg], space.index[p]])
               for p in inventory if p in space.index]
        return min(row, key=lambda x: x[1])[0] if row else seg
    best, best_d = seg, float("inf")
    for phon in inventory:
        d = _dist.weighted_feature_edit_distance(seg, phon)
        if d < best_d:
            best, best_d = phon, d
    return best


def project(ipa: str, inventory: tuple[str, ...], params=None) -> str:
    """Assimilate a word into a listener's phoneme inventory.

    Models first-pass loanword perception: each segment is heard as the
    nearest native category. (No epenthesis/deletion modeling in v0.)
    """
    key = None if params is None else tuple(float(x) for x in params)
    return "".join(_nearest_in_inventory(s, inventory, key) for s in segments(ipa))


def recognizability(
    candidate: str,
    known_word: str,
    listener_inventory: tuple[str, ...] | None = None,
    params=None,
) -> float:
    """How recognizable is `candidate` to someone who knows `known_word`?

    Both words are IPA. If `listener_inventory` is given (tuple of IPA
    phonemes, e.g. from PHOIBLE), both words are first assimilated into
    that inventory, so contrasts the listener lacks are free.
    """
    if listener_inventory is not None:
        candidate = project(candidate, listener_inventory, params)
        known_word = project(known_word, listener_inventory, params)
    return similarity(candidate, known_word, params)
