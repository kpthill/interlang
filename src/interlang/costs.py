"""Swappable phonetic cost models + a fast batched aligner (spec R2/R4/R6).

The recognizability metric (metric.py v0) is panphon's weighted feature edit
distance with panphon's *hand-guessed* default weights. This module factors the
cost structure out from behind that call so it can be (a) learned from data and
(b) replaced later by a richer model, without rewriting the study around it.

THE INTERFACE (R4)
  A cost model is a parameter vector plus three answers over a `SegmentSpace`:

      sub_matrix()                -> (n_types, n_types) substitution costs
      del_classes(A)              -> (N, la) int, which indel parameter prices
                                     deleting each source segment
      ins_classes(A, B)           -> (N, la+1, lb) int, which indel parameter
                                     prices inserting each target segment AT
                                     each source position

  The `ins_classes` signature is what makes context-sensitive epenthesis
  expressible: the price of inserting a vowel may depend on *where* in the
  source word it is being inserted (between two consonants = cluster repair)
  rather than only on what is being inserted.  A model that does not care about
  context simply broadcasts.

  Parameters are always laid out as [22 feature weights | indel classes], so
  the aligner, the fitter, the CV harness and the guardrails are written once
  and work for any model.  Two are shipped:

    FeatureWeightCosts        22 + 4  (del_C, del_V, ins_C, ins_V)
    ContextEpenthesisCosts    22 + 6  (del_C, del_V, ins_C,
                                       ins_V_cluster, ins_V_edge, ins_V_other)

  Still behind the seam, unbuilt: a segment-pair matrix (Jager-style PMI), a
  low-rank feature-interaction term, asymmetric substitution.

THE SUBSTITUTION MODEL (spec's agreed call 1)
  Substitution cost = sum_k w_k * |f_i[k] - f_j[k]| over panphon's first 22
  feature dimensions, with values in {-1, 0, +1} and NO halving -- exactly
  panphon's `weighted_substitution_cost`, so DEFAULT_PARAMS reproduces the v0
  metric bit for bit.  (panphon ships 22 weights for its 24 dimensions; the two
  tone dimensions are unweighted and we follow that.)  One full feature flip
  costs 2*w_k, so the maximum substitution cost is 2 * 7.25 = 14.5.

THE INDEL MODEL (spec R2 -- epenthesis is a requirement, fitted jointly)
  panphon prices every insertion and every deletion at a flat sum(weights) =
  7.25, which is why "sutoraiku" vs "strike" scores only 0.62.  Splitting that
  flat price by segment class (and, in the context model, by position) is the
  epenthesis machinery, and it is fitted in the SAME optimization as the
  feature weights -- never bolted on afterwards, because the indel prices
  determine the alignments that the substitution counts are read off.

  SCALE: multiplying every parameter by a constant leaves the normalized
  similarity unchanged, so the objective has an exact flat direction.  It is
  removed by rescaling every parameter vector so the 22 feature weights sum to
  7.25, panphon's default sum.  Learned weights are therefore directly
  comparable to panphon's, unit for unit.

  ASYMMETRY: substitution is symmetric (a feature-weight model cannot be
  otherwise), but insertion and deletion are separately parameterized, which is
  where source->recipient directionality actually lives.

SIMILARITY
  Faithful to metric.similarity: `sim = max(0, 1 - d / norm)` with
  `norm = max(total_del_cost(source), total_del_cost(target))`, the cost of
  deleting the longer word entirely.  `similarity_from(..., clamp=False)`
  returns the unclamped ratio, used for the training surrogate so hopeless
  pairs still carry signal; AUC is always computed on the clamped value.

WHY THE ALIGNER IS BATCHED, AND THE EM STRUCTURE (spec R6)
  Fitting needs the objective evaluated thousands of times.  Two facts make it
  cheap:
    1. Given a FIXED alignment, the total distance is exactly LINEAR in the
       parameters: d = phi . p, where phi accumulates per-feature disagreement
       over substituted positions plus counts per indel class.  Same for the
       normalizer.  `align_batch` returns those phi rows once, after which the
       inner optimizer evaluates candidate parameter vectors with a matmul
       (~0.4 ms over 13.6k pairs).
    2. The alignment only changes at discrete parameter values (R6's "alignment
       wrinkle").  So we re-align between inner optimizations -- an EM-style
       outer loop -- instead of pretending the objective is smooth through the
       argmin.
  The DP is vectorized across all pairs of identical (len_src, len_tgt) shape;
  a full pass over 13.6k pairs takes ~0.2 s.

Nothing here reads or writes files; see scripts/cost_learning.py.
"""

from __future__ import annotations

from collections import defaultdict

import numpy as np
import panphon

_ft = panphon.FeatureTable()

#: panphon's default per-feature weights (22 of its 24 feature dimensions).
PANPHON_WEIGHTS = np.asarray(_ft.weights, dtype=np.float64)
N_FEATURES = len(PANPHON_WEIGHTS)          # 22
FEATURE_NAMES = list(_ft.names[:N_FEATURES])
WEIGHT_SUM = float(PANPHON_WEIGHTS.sum())  # 7.25
PANPHON_INDEL = WEIGHT_SUM                 # panphon's flat indel price

_SYL_IDX = FEATURE_NAMES.index("syl")


# ---------------------------------------------------------------------------
# Segment space
# ---------------------------------------------------------------------------

class SegmentSpace:
    """Interns segment types and caches their panphon feature vectors.

    Everything downstream works with integer type ids, so the DP never touches
    a string and substitution cost is one (n, n) array lookup.
    """

    def __init__(self, seg_types: list[str]):
        self.types = list(dict.fromkeys(seg_types))
        self.index = {s: i for i, s in enumerate(self.types)}
        vecs = []
        for s in self.types:
            v = _ft.word_to_vector_list(s, numeric=True)
            vecs.append(v[0][:N_FEATURES] if v else [0] * N_FEATURES)
        self.vectors = np.asarray(vecs, dtype=np.float64)   # (n, 22) in {-1,0,1}
        self.diff = np.abs(self.vectors[:, None, :] - self.vectors[None, :, :])
        self.is_vowel = (self.vectors[:, _SYL_IDX] > 0).astype(np.int64)  # (n,)

    def __len__(self) -> int:
        return len(self.types)

    def encode(self, segs: list[str]) -> np.ndarray:
        return np.asarray([self.index[s] for s in segs], dtype=np.int32)


# ---------------------------------------------------------------------------
# Cost models (the R4 seam)
# ---------------------------------------------------------------------------

class CostModel:
    """Base: parameter layout [22 feature weights | indel classes]."""

    indel_names: list[str] = []

    def __init__(self, space: SegmentSpace, params: np.ndarray | None = None):
        self.space = space
        p = self.default_params() if params is None else np.asarray(params, float)
        self.params = self.normalize(p)

    # -- parameter bookkeeping ------------------------------------------
    @classmethod
    def n_params(cls) -> int:
        return N_FEATURES + len(cls.indel_names)

    @classmethod
    def param_names(cls) -> list[str]:
        return FEATURE_NAMES + cls.indel_names

    @classmethod
    def default_params(cls) -> np.ndarray:
        """panphon's defaults: hand-guessed weights, flat indel price."""
        return np.concatenate([PANPHON_WEIGHTS,
                               np.full(len(cls.indel_names), PANPHON_INDEL)])

    @staticmethod
    def normalize(p: np.ndarray) -> np.ndarray:
        """Remove the scale degeneracy: feature weights always sum to 7.25."""
        p = np.abs(np.asarray(p, dtype=np.float64))
        s = p[:N_FEATURES].sum()
        if s <= 0:
            return p
        return p * (WEIGHT_SUM / s)

    @property
    def weights(self) -> np.ndarray:
        return self.params[:N_FEATURES]

    # -- the three answers ----------------------------------------------
    def sub_matrix(self) -> np.ndarray:
        return self.space.diff @ self.weights

    def del_classes(self, A: np.ndarray) -> np.ndarray:
        raise NotImplementedError

    def ins_classes(self, A: np.ndarray, B: np.ndarray) -> np.ndarray:
        raise NotImplementedError


class FeatureWeightCosts(CostModel):
    """22 feature weights + 4 class-conditioned indel prices (the shipped model).

    V = [+syllabic].  Insertion price depends only on WHAT is inserted, which
    is the minimum needed to express "epenthetic vowels are cheap".
    """

    indel_names = ["del_C", "del_V", "ins_C", "ins_V"]

    def del_classes(self, A: np.ndarray) -> np.ndarray:
        return self.space.is_vowel[A]                     # 0 = del_C, 1 = del_V

    def ins_classes(self, A: np.ndarray, B: np.ndarray) -> np.ndarray:
        N, lb = B.shape
        la = A.shape[1]
        cls = 2 + self.space.is_vowel[B]                  # 2 = ins_C, 3 = ins_V
        return np.broadcast_to(cls[:, None, :], (N, la + 1, lb))


class ContextEpenthesisCosts(CostModel):
    """Stretch goal (spec R2): vowel insertion priced by WHERE it happens.

    A vowel inserted between two source consonants ("strike" -> "sutoraiku",
    "s_t_r") is repairing an illegal cluster and should be cheap.  A vowel
    inserted next to a vowel, or in the middle of an already-legal sequence, is
    not repairing anything and should not be.  Three insertion contexts for
    vowels:

      ins_V_cluster  between two source consonants (true cluster repair)
      ins_V_edge     before the first / after the last source segment when that
                     segment is a consonant (prothesis "schola" -> "escuela",
                     paragoge "strike" -> "sutoraik-u")
      ins_V_other    anywhere else

    This is what separates attested epenthesis from insertions that would help
    a negative control equally, which is why the flat model cannot get the
    sutoraiku case without also making every control cheaper.
    """

    indel_names = ["del_C", "del_V", "ins_C",
                   "ins_V_cluster", "ins_V_edge", "ins_V_other"]

    def del_classes(self, A: np.ndarray) -> np.ndarray:
        return self.space.is_vowel[A]

    def ins_classes(self, A: np.ndarray, B: np.ndarray) -> np.ndarray:
        N, la = A.shape
        lb = B.shape[1]
        isv_A = self.space.is_vowel[A]                    # (N, la)
        cons = 1 - isv_A
        # context of insertion slot i (0..la): between A[i-1] and A[i]
        ctx = np.zeros((N, la + 1), dtype=np.int64)       # 0 other, 1 cluster, 2 edge
        if la >= 2:
            interior = cons[:, :-1] & cons[:, 1:]         # (N, la-1) slots 1..la-1
            ctx[:, 1:la] = np.where(interior, 1, 0)
        if la >= 1:
            ctx[:, 0] = np.where(cons[:, 0], 2, 0)
            ctx[:, la] = np.where(cons[:, -1], 2, 0)
        isv_B = self.space.is_vowel[B]                    # (N, lb)
        out = np.empty((N, la + 1, lb), dtype=np.int64)
        out[:] = 2                                        # ins_C
        vowel = isv_B[:, None, :].astype(bool)
        ctx3 = np.broadcast_to(ctx[:, :, None], (N, la + 1, lb))
        vcls = np.select([ctx3 == 1, ctx3 == 2], [3, 4], default=5)
        return np.where(vowel, vcls, out)


MODELS = {"feature": FeatureWeightCosts, "context": ContextEpenthesisCosts}


# ---------------------------------------------------------------------------
# Batched alignment
# ---------------------------------------------------------------------------

class PairBatch:
    """Encoded (source, target) pairs, bucketed by shape for a vectorized DP."""

    def __init__(self, space: SegmentSpace, srcs: list[list[str]], tgts: list[list[str]]):
        self.space = space
        self.n = len(srcs)
        buckets: dict[tuple[int, int], list[int]] = defaultdict(list)
        for k, (a, b) in enumerate(zip(srcs, tgts)):
            buckets[(len(a), len(b))].append(k)
        self.groups = []
        for (_la, _lb), idx in buckets.items():
            A = np.stack([space.encode(srcs[k]) for k in idx])
            B = np.stack([space.encode(tgts[k]) for k in idx])
            self.groups.append((np.asarray(idx, dtype=np.int64), A, B))
        self.src_nV = np.asarray([int(space.is_vowel[space.encode(a)].sum()) for a in srcs], float)
        self.src_nC = np.asarray([len(a) for a in srcs], float) - self.src_nV
        self.tgt_nV = np.asarray([int(space.is_vowel[space.encode(b)].sum()) for b in tgts], float)
        self.tgt_nC = np.asarray([len(b) for b in tgts], float) - self.tgt_nV


def align_batch(batch: PairBatch, model: CostModel) -> tuple[np.ndarray, np.ndarray]:
    """Align every pair under `model`; return (distance, phi).

    phi is (n_pairs, model.n_params()): per-feature disagreement summed over the
    chosen alignment's substitutions, then a count per indel class.  By
    construction distance == phi @ model.params, and for any other p, phi @ p is
    the distance under p *holding this alignment fixed*.
    """
    space = batch.space
    npar = model.n_params()
    sub = model.sub_matrix()
    indel = model.params[N_FEATURES:]
    dist = np.zeros(batch.n)
    phi = np.zeros((batch.n, npar))

    for idx, A, B in batch.groups:
        N, la = A.shape
        lb = B.shape[1]
        S = sub[A[:, :, None], B[:, None, :]]              # (N, la, lb)
        dcls = model.del_classes(A)                        # (N, la)
        icls = model.ins_classes(A, B)                     # (N, la+1, lb)
        dA = indel[dcls]                                   # (N, la)
        iB = indel[icls]                                   # (N, la+1, lb)

        D = np.empty((N, la + 1, lb + 1))
        BP = np.zeros((N, la + 1, lb + 1), dtype=np.int8)  # 0 sub, 1 del, 2 ins
        D[:, 0, 0] = 0.0
        D[:, 1:, 0] = np.cumsum(dA, axis=1)
        D[:, 0, 1:] = np.cumsum(iB[:, 0, :], axis=1)
        BP[:, 1:, 0] = 1
        BP[:, 0, 1:] = 2
        rows = np.arange(N)
        for i in range(1, la + 1):
            Dim1, Di = D[:, i - 1], D[:, i]
            for j in range(1, lb + 1):
                stacked = np.stack([
                    Dim1[:, j - 1] + S[:, i - 1, j - 1],
                    Dim1[:, j] + dA[:, i - 1],
                    Di[:, j - 1] + iB[:, i, j - 1],
                ])
                arg = np.argmin(stacked, axis=0)
                Di[:, j] = stacked[arg, rows]
                BP[:, i, j] = arg
        dist[idx] = D[:, la, lb]

        # traceback, vectorized over the batch
        i = np.full(N, la, dtype=np.int64)
        j = np.full(N, lb, dtype=np.int64)
        acc = np.zeros((N, npar))
        for _ in range(la + lb):
            active = (i > 0) | (j > 0)
            if not active.any():
                break
            op = np.where(active, BP[rows, i, j], -1)
            m = op == 0
            if m.any():
                r = rows[m]
                acc[r, :N_FEATURES] += space.diff[A[r, i[m] - 1], B[r, j[m] - 1]]
            m_del = op == 1
            if m_del.any():
                r = rows[m_del]
                np.add.at(acc, (r, N_FEATURES + dcls[r, i[m_del] - 1]), 1.0)
            m_ins = op == 2
            if m_ins.any():
                r = rows[m_ins]
                np.add.at(acc, (r, N_FEATURES + icls[r, i[m_ins], j[m_ins] - 1]), 1.0)
            i = i - (m | m_del).astype(np.int64)
            j = j - (m | m_ins).astype(np.int64)
        phi[idx] = acc
    return dist, phi


def normalizer_rows(batch: PairBatch, model: CostModel) -> np.ndarray:
    """psi with `norm = psi @ params`, picking the longer word under `model`.

    metric.similarity normalizes by the cost of deleting the LONGER word
    entirely.  Which word that is can flip when the indel parameters move, so
    the choice is made from the current parameters and then held fixed for the
    inner optimization, exactly like the alignment.
    """
    p = model.params
    d_c, d_v = p[N_FEATURES + 0], p[N_FEATURES + 1]
    src = batch.src_nC * d_c + batch.src_nV * d_v
    tgt = batch.tgt_nC * d_c + batch.tgt_nV * d_v
    use_src = src >= tgt
    psi = np.zeros((batch.n, model.n_params()))
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
# Convenience: back-compat aliases + single-pair helpers (guardrails)
# ---------------------------------------------------------------------------

DEFAULT_PARAMS = FeatureWeightCosts.default_params()
PARAM_NAMES = FeatureWeightCosts.param_names()
N_PARAMS = FeatureWeightCosts.n_params()


def normalize_params(p: np.ndarray) -> np.ndarray:
    return CostModel.normalize(p)


def build_space(*seg_lists: list[list[str]]) -> SegmentSpace:
    seen: list[str] = []
    for lst in seg_lists:
        for segs in lst:
            seen.extend(segs)
    return SegmentSpace(seen)


def similarity(a_segs, b_segs, params, model_cls=FeatureWeightCosts) -> float:
    """One-off similarity under `params` (builds a tiny SegmentSpace)."""
    a_segs, b_segs = list(a_segs), list(b_segs)
    if not a_segs or not b_segs:
        return 0.0
    space = SegmentSpace(a_segs + b_segs)
    model = model_cls(space, params)
    batch = PairBatch(space, [a_segs], [b_segs])
    _, phi = align_batch(batch, model)
    psi = normalizer_rows(batch, model)
    return float(similarity_from(phi, psi, model.params)[0])


def substitution_cost(a: str, b: str, params: np.ndarray) -> float:
    """Cost of substituting one segment for another under `params`."""
    space = SegmentSpace([a, b])
    return float(FeatureWeightCosts(space, params).sub_matrix()[0, 1])


def auc(pos: np.ndarray, neg: np.ndarray) -> float:
    """Mann-Whitney AUC with ties counted at 0.5."""
    pos, neg = np.asarray(pos, float), np.asarray(neg, float)
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
