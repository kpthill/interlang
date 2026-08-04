"""Swappable phonetic cost models + a fast batched aligner (spec R2/R4/R6).

The recognizability metric (metric.py v0) is panphon's weighted feature edit
distance with panphon's *hand-guessed* default weights. This module factors the
cost structure out from behind that call so it can be (a) learned from data and
(b) replaced later by a richer model, without rewriting the study around it.

THE INTERFACE (R4)
  A cost model answers three questions over a fixed `SegmentSpace`:
      sub_matrix()  -> (n_types, n_types) cost of substituting type i by type j
      del_vector()  -> (n_types,)         cost of deleting type i (in source,
                                          absent from recipient)
      ins_vector()  -> (n_types,)         cost of inserting type j (in
                                          recipient, absent from source)
  Anything satisfying that shape drops into `align_batch` / `score_pairs`.
  `FeatureWeightCosts` (shipped) is the panphon-feature-weight model; a
  segment-pair matrix, a low-rank interaction term, or asymmetric costs can be
  added as new classes without touching the aligner, the CV harness, or the
  guardrails.

THE SHIPPED MODEL (spec's agreed call 1 + R2)
  26 parameters, all non-negative:
    - 22 panphon feature weights (panphon supplies 22 weights for the first 22
      of its 24 feature dimensions; the two tone dimensions are unweighted and
      we follow that).  Substitution cost = sum_k w_k * |f_i[k] - f_j[k]|,
      exactly panphon's form (values in {-1,0,1}, no halving: one full feature
      flip costs 2*w_k), so setting w to panphon's defaults reproduces v0.
    - 4 indel parameters: del_C, del_V, ins_C, ins_V, where V = [+syllabic].
      This is the epenthesis machinery (R2): a cheap ins_V lets a vowel be
      inserted to repair an illegal cluster ("strike" -> "sutoraiku") without
      making every insertion cheap.  panphon's default is a single flat
      sum(weights) = 7.25 for all four.

  SCALE: multiplying all 26 parameters by a constant leaves the normalized
  similarity unchanged (both the distance and its normalizer scale), so the
  objective has an exact flat direction.  We remove it by rescaling every
  parameter vector so that sum(feature weights) = 7.25, panphon's default sum.
  Learned weights are therefore directly comparable to panphon's, unit for
  unit.

  ASYMMETRY: substitution is symmetric here (a feature-weight model cannot be
  otherwise), but insertion and deletion are separately parameterized, which is
  where the source->recipient directionality actually lives.  Asymmetric
  substitution is the documented next model behind the R4 seam.

SIMILARITY
  Faithful to metric.similarity: `sim = max(0, 1 - d / norm)` with
  `norm = max(total_del_cost(source), total_del_cost(target))`, i.e. the cost of
  deleting the longer word entirely.  `score_pairs(..., clamp=False)` returns
  the unclamped ratio, used for the training surrogate so that hopeless pairs
  still carry gradient; AUC is always computed on the clamped, metric-faithful
  value.

WHY THE ALIGNER IS BATCHED, AND THE EM STRUCTURE (R6)
  Fitting needs the objective evaluated thousands of times.  Two facts make
  that cheap:
    1. Given a FIXED alignment, the total distance is exactly LINEAR in the 26
       parameters: d = phi . p, where phi counts per-feature disagreement over
       substituted positions plus indels by class.  Same for the normalizer.
       So `align_batch` returns those phi vectors once, and the inner optimizer
       then evaluates millions of candidate parameter vectors with a matmul.
    2. The alignment itself only changes at discrete parameter values (the R6
       "alignment wrinkle").  We therefore re-align between inner optimizations
       — an EM-style outer loop — instead of pretending the objective is smooth
       through the argmin.
  The DP is vectorized across pairs of identical (len_src, len_tgt) shape, so a
  full pass over ~14k pairs is a fraction of a second.

Usage is via scripts/cost_learning.py; nothing here reads or writes files.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass

import numpy as np
import panphon

_ft = panphon.FeatureTable()

#: panphon's default per-feature weights (22 of its 24 feature dimensions).
PANPHON_WEIGHTS = np.asarray(_ft.weights, dtype=np.float64)
N_FEATURES = len(PANPHON_WEIGHTS)          # 22
FEATURE_NAMES = list(_ft.names[:N_FEATURES])
WEIGHT_SUM = float(PANPHON_WEIGHTS.sum())  # 7.25
#: panphon's indel cost is flat = sum(weights); our 4 indel params default to it
PANPHON_INDEL = WEIGHT_SUM
N_PARAMS = N_FEATURES + 4
INDEL_NAMES = ["del_C", "del_V", "ins_C", "ins_V"]
PARAM_NAMES = FEATURE_NAMES + INDEL_NAMES

DEFAULT_PARAMS = np.concatenate([PANPHON_WEIGHTS, np.full(4, PANPHON_INDEL)])

_SYL_IDX = FEATURE_NAMES.index("syl")


# ---------------------------------------------------------------------------
# Segment space
# ---------------------------------------------------------------------------

class SegmentSpace:
    """Interns the segment types of a corpus and caches their feature vectors.

    Everything downstream works with integer type ids, so the DP never touches
    a string and the substitution cost is a single (n, n) array lookup.
    """

    def __init__(self, seg_types: list[str]):
        self.types = list(dict.fromkeys(seg_types))
        self.index = {s: i for i, s in enumerate(self.types)}
        vecs = []
        for s in self.types:
            v = _ft.word_to_vector_list(s, numeric=True)
            vecs.append(v[0][:N_FEATURES] if v else [0] * N_FEATURES)
        self.vectors = np.asarray(vecs, dtype=np.float64)   # (n, 22) in {-1,0,1}
        # per-feature disagreement.  panphon's weighted_substitution_cost is
        # sum_k w_k * |f_i[k] - f_j[k]| with values in {-1,0,1} and NO division
        # by 2, so one full feature flip costs 2*w_k and the maximum possible
        # substitution cost (2 * 7.25 = 14.5) is twice the flat indel cost.
        # We keep that convention exactly, so DEFAULT_PARAMS reproduces v0.
        self.diff = np.abs(self.vectors[:, None, :] - self.vectors[None, :, :])
        self.is_vowel = (self.vectors[:, _SYL_IDX] > 0).astype(np.float64)  # (n,)

    def __len__(self) -> int:
        return len(self.types)

    def encode(self, segs: list[str]) -> np.ndarray:
        return np.asarray([self.index[s] for s in segs], dtype=np.int32)


# ---------------------------------------------------------------------------
# Cost models (R4 interface)
# ---------------------------------------------------------------------------

class CostModel:
    """Interface: three arrays over a SegmentSpace."""

    def sub_matrix(self) -> np.ndarray: raise NotImplementedError
    def del_vector(self) -> np.ndarray: raise NotImplementedError
    def ins_vector(self) -> np.ndarray: raise NotImplementedError


def normalize_params(p: np.ndarray) -> np.ndarray:
    """Fix the scale degeneracy: rescale so sum(feature weights) == 7.25."""
    p = np.abs(np.asarray(p, dtype=np.float64))
    s = p[:N_FEATURES].sum()
    if s <= 0:
        return DEFAULT_PARAMS.copy()
    return p * (WEIGHT_SUM / s)


@dataclass
class FeatureWeightCosts(CostModel):
    """panphon-style feature weights + 4 class-conditioned indel costs."""

    space: SegmentSpace
    params: np.ndarray = None  # type: ignore[assignment]

    def __post_init__(self) -> None:
        if self.params is None:
            self.params = DEFAULT_PARAMS.copy()
        self.params = normalize_params(self.params)

    @property
    def weights(self) -> np.ndarray:
        return self.params[:N_FEATURES]

    def sub_matrix(self) -> np.ndarray:
        return self.space.diff @ self.weights

    def del_vector(self) -> np.ndarray:
        v = self.space.is_vowel
        return self.params[N_FEATURES + 0] * (1 - v) + self.params[N_FEATURES + 1] * v

    def ins_vector(self) -> np.ndarray:
        v = self.space.is_vowel
        return self.params[N_FEATURES + 2] * (1 - v) + self.params[N_FEATURES + 3] * v


# ---------------------------------------------------------------------------
# Batched alignment
# ---------------------------------------------------------------------------

class PairBatch:
    """Encoded (source, target) pairs, bucketed by shape for vectorized DP."""

    def __init__(self, space: SegmentSpace, srcs: list[list[str]], tgts: list[list[str]]):
        self.space = space
        self.n = len(srcs)
        buckets: dict[tuple[int, int], list[int]] = defaultdict(list)
        for k, (a, b) in enumerate(zip(srcs, tgts)):
            buckets[(len(a), len(b))].append(k)
        self.groups = []
        for (la, lb), idx in buckets.items():
            A = np.stack([space.encode(srcs[k]) for k in idx])   # (N, la)
            B = np.stack([space.encode(tgts[k]) for k in idx])   # (N, lb)
            self.groups.append((np.asarray(idx, dtype=np.int64), A, B))
        # one-hot-ish class counts for the normalizer (linear in the 4 indels)
        self.src_nV = np.asarray([space.is_vowel[space.encode(a)].sum() for a in srcs])
        self.src_nC = np.asarray([len(a) for a in srcs]) - self.src_nV
        self.tgt_nV = np.asarray([space.is_vowel[space.encode(b)].sum() for b in tgts])
        self.tgt_nC = np.asarray([len(b) for b in tgts]) - self.tgt_nV


def align_batch(batch: PairBatch, model: CostModel) -> tuple[np.ndarray, np.ndarray]:
    """Align every pair under `model`; return (distance, phi).

    `phi` is (n_pairs, N_PARAMS): the per-feature disagreement totals over the
    chosen alignment's substitutions, then the counts of deleted consonants,
    deleted vowels, inserted consonants, inserted vowels.  By construction
    `distance == phi @ model.params`, and for ANY other parameter vector p,
    `phi @ p` is the distance under p *holding this alignment fixed*.
    """
    space = batch.space
    sub = model.sub_matrix()
    dvec = model.del_vector()
    ivec = model.ins_vector()
    dist = np.zeros(batch.n)
    phi = np.zeros((batch.n, N_PARAMS))

    for idx, A, B in batch.groups:
        N, la = A.shape
        lb = B.shape[1]
        S = sub[A[:, :, None], B[:, None, :]]          # (N, la, lb)
        dA = dvec[A]                                   # (N, la)
        iB = ivec[B]                                   # (N, lb)
        D = np.empty((N, la + 1, lb + 1))
        D[:, 0, 0] = 0.0
        D[:, 1:, 0] = np.cumsum(dA, axis=1)
        D[:, 0, 1:] = np.cumsum(iB, axis=1)
        # back-pointer: 0 = substitute, 1 = delete (from source), 2 = insert
        BP = np.zeros((N, la + 1, lb + 1), dtype=np.int8)
        BP[:, 1:, 0] = 1
        BP[:, 0, 1:] = 2
        for i in range(1, la + 1):
            Dim1 = D[:, i - 1]
            Di = D[:, i]
            for j in range(1, lb + 1):
                c_sub = Dim1[:, j - 1] + S[:, i - 1, j - 1]
                c_del = Dim1[:, j] + dA[:, i - 1]
                c_ins = Di[:, j - 1] + iB[:, j - 1]
                stacked = np.stack([c_sub, c_del, c_ins])
                arg = np.argmin(stacked, axis=0)
                Di[:, j] = stacked[arg, np.arange(N)]
                BP[:, i, j] = arg
        dist[idx] = D[:, la, lb]

        # traceback, vectorized over the batch
        i = np.full(N, la, dtype=np.int64)
        j = np.full(N, lb, dtype=np.int64)
        rows = np.arange(N)
        acc = np.zeros((N, N_PARAMS))
        for _ in range(la + lb):
            active = (i > 0) | (j > 0)
            if not active.any():
                break
            op = BP[rows, i, j]
            op = np.where(active, op, -1)
            m_sub = op == 0
            if m_sub.any():
                r = rows[m_sub]
                acc[r, :N_FEATURES] += space.diff[A[r, i[m_sub] - 1], B[r, j[m_sub] - 1]]
            m_del = op == 1
            if m_del.any():
                r = rows[m_del]
                v = space.is_vowel[A[r, i[m_del] - 1]]
                acc[r, N_FEATURES + 0] += 1 - v
                acc[r, N_FEATURES + 1] += v
            m_ins = op == 2
            if m_ins.any():
                r = rows[m_ins]
                v = space.is_vowel[B[r, j[m_ins] - 1]]
                acc[r, N_FEATURES + 2] += 1 - v
                acc[r, N_FEATURES + 3] += v
            i = i - (m_sub | m_del).astype(np.int64)
            j = j - (m_sub | m_ins).astype(np.int64)
        phi[idx] = acc
    return dist, phi


def normalizer_rows(batch: PairBatch, model: CostModel) -> np.ndarray:
    """Rows psi with `norm = psi @ params`, choosing the longer word under `model`.

    metric.similarity normalizes by the cost of deleting the LONGER word
    entirely.  Which word that is can flip when the indel parameters move, so
    the choice is made from the current parameters and then held fixed for the
    inner optimization, exactly like the alignment (see module docstring).
    """
    p = model.params
    src = batch.src_nC * p[N_FEATURES + 0] + batch.src_nV * p[N_FEATURES + 1]
    tgt = batch.tgt_nC * p[N_FEATURES + 0] + batch.tgt_nV * p[N_FEATURES + 1]
    use_src = src >= tgt
    psi = np.zeros((batch.n, N_PARAMS))
    psi[use_src, N_FEATURES + 0] = batch.src_nC[use_src]
    psi[use_src, N_FEATURES + 1] = batch.src_nV[use_src]
    psi[~use_src, N_FEATURES + 0] = batch.tgt_nC[~use_src]
    psi[~use_src, N_FEATURES + 1] = batch.tgt_nV[~use_src]
    return psi


def similarity_from(phi: np.ndarray, psi: np.ndarray, params: np.ndarray,
                    clamp: bool = True) -> np.ndarray:
    """sim = 1 - (phi@p)/(psi@p), optionally clamped at 0 as metric.py does."""
    d = phi @ params
    norm = psi @ params
    norm = np.where(norm <= 0, 1e-9, norm)
    s = 1.0 - d / norm
    return np.maximum(s, 0.0) if clamp else s


# ---------------------------------------------------------------------------
# Single-pair convenience (guardrails, diagnostics)
# ---------------------------------------------------------------------------

def build_space(*seg_lists: list[list[str]]) -> SegmentSpace:
    seen: list[str] = []
    for lst in seg_lists:
        for segs in lst:
            seen.extend(segs)
    return SegmentSpace(seen)


def similarity(a_segs: list[str], b_segs: list[str], params: np.ndarray,
               space: SegmentSpace | None = None) -> float:
    """One-off similarity under `params` (builds a tiny SegmentSpace if needed)."""
    if not a_segs or not b_segs:
        return 0.0
    space = space or SegmentSpace(list(a_segs) + list(b_segs))
    model = FeatureWeightCosts(space, params)
    batch = PairBatch(space, [list(a_segs)], [list(b_segs)])
    _, phi = align_batch(batch, model)
    psi = normalizer_rows(batch, model)
    return float(similarity_from(phi, psi, model.params)[0])


def substitution_cost(a: str, b: str, params: np.ndarray) -> float:
    """Cost of substituting one segment for another under `params`."""
    space = SegmentSpace([a, b])
    return float(FeatureWeightCosts(space, params).sub_matrix()[0, 1])


def auc(pos: np.ndarray, neg: np.ndarray) -> float:
    """Mann-Whitney AUC with ties counted at 0.5."""
    pos = np.asarray(pos, dtype=np.float64)
    neg = np.asarray(neg, dtype=np.float64)
    if len(pos) == 0 or len(neg) == 0:
        return float("nan")
    allv = np.concatenate([pos, neg])
    order = np.argsort(allv, kind="mergesort")
    ranks = np.empty(len(allv))
    sv = allv[order]
    i = 0
    while i < len(sv):
        j = i
        while j < len(sv) and sv[j] == sv[i]:
            j += 1
        ranks[order[i:j]] = (i + j + 1) / 2.0
        i = j
    n_p, n_n = len(pos), len(neg)
    return float((ranks[:n_p].sum() - n_p * (n_p + 1) / 2) / (n_p * n_n))
