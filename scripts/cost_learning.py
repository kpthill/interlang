"""Learn substitution + epenthesis costs from WOLD loanword adaptations.

Executes notes/cost-learning-spec.md; interpreted in notes/cost-learning.md.
Replaces panphon's hand-guessed feature weights (and its flat insertion/deletion
price) with a cost vector fitted JOINTLY to attested loanword adaptations under
a discriminative objective, evaluated by recipient-grouped cross-validation.

INPUTS
  data/processed/wold_pairs.csv      (scripts/wold_pipeline.py; WOLD commit
                                      recorded in that script's output)
  data/processed/contrast_costs.csv  (scripts/contrast_study.py; guardrail 5)
  data/raw/phoible/cldf/             (guardrail 3 listener inventory)

OUTPUTS (all committed)
  data/processed/learned_costs.csv          fitted parameters per model:
        panphon default, full-data fit, and the leave-one-recipient-out
        mean/sd/min/max that carry the R3 stability claim.
  data/processed/cost_learning_cv.csv       one row per (model, held-out
        recipient): n_pairs, held-out AUC under default weights, under the
        learned weights, and that fold's parameters.
  data/processed/cost_learning_lambda.csv   the regularization-strength sweep
        that selects LAMBDA (see below).
  data/processed/cost_learning_guardrails.csv    guardrails 1-5, pass/fail.
  data/processed/cost_learning_contrast_check.csv  guardrail 5 detail.

TWO COST MODELS, BOTH BEHIND THE R4 SEAM (src/interlang/costs.py)
  `feature`  22 panphon feature weights + 4 indel prices (del_C, del_V, ins_C,
             ins_V).  This is the shipped model of the spec's agreed call 1.
  `context`  the same, but vowel insertion is priced by CONTEXT: cheap between
             two source consonants (cluster repair) or at a consonantal word
             edge (prothesis/paragoge), normal elsewhere.  This is the spec's
             explicit R2 STRETCH GOAL.  It is included because the flat model
             cannot reach the guardrail-4 target without also making every
             negative control cheaper, and the difference between the two is
             the cleanest measurement of that we can make.
  Both are fitted with the identical objective, folds, controls and guardrails,
  so the comparison is like for like.

WHAT IS OPTIMIZED, AND WHY (spec R6)
  AUC is a flat staircase in the parameters and is never optimized.  The
  training objective is the smooth pairwise logistic surrogate plus a prior:

      L(p) = mean_r  mean_{k in r}  -log sigmoid( (s+_k - s-_k) / TAU )
             + LAMBDA * mean_j ( log p_j - log p_j^panphon )^2

  - The outer mean-over-recipients IS the R5 rebalancing: each recipient counts
    equally however many pairs it has, so Berber/Romani/Romanian cannot
    dominate.  Donor rebalancing is NOT done — logged as a caveat; the
    Spanish/Latin/Arabic donor skew survives into the fit.
  - The LAMBDA term shrinks toward panphon's hand-guessed values in log space.
    It is NOT decoration.  Unregularized, the fit drives the major-class
    features (syl, son, cons) to ~0.04 — it discovers that making a vowel and a
    consonant cheap to interchange is a crude substitute for the epenthesis
    machinery it lacks, and the result scores /d/->/i/ as CHEAPER than /d/->/f/
    (guardrail 2 fails outright).  The prior is the statement that panphon's
    guesses are a weak but real prior and the data must earn deviations from
    them.  LAMBDA is chosen by the sweep in `lambda_sweep()`, on held-out AUC
    under grouped 5-fold CV; the chosen value and the whole curve are written
    to cost_learning_lambda.csv.  Selection optimism: LAMBDA is picked using
    all 41 recipients and then reused for the leave-one-recipient-out run, so
    the LORO numbers are very slightly optimistic.  The curve is flat enough
    (see the CSV) that this is worth far less than the AUC differences we
    report; it is disclosed rather than paid for with a 7x nested run.

  Optimizer: derivative-free Nelder-Mead (scipy) on log-parameters, inside an
  EM-style outer loop that re-aligns between inner optimizations.  Both
  sanctioned R6 routes are used together, deliberately:
    - the surrogate is smooth, so the simplex has a real landscape to descend
      instead of AUC's staircase;
    - derivative-free search plus explicit re-alignment handles the alignment
      discontinuity R6 flags.  Within one inner optimization the alignment (and
      the choice of which word normalizes) is FROZEN, which makes the distance
      exactly linear in the parameters and each objective evaluation a single
      matmul (~0.4 ms over 13.6k pairs); between outer iterations we re-align
      under the new parameters and recompute the honest objective, accepting an
      outer step only if the re-aligned objective improved.
  AUC is computed only on held-out folds, on the clamped metric-faithful
  similarity, and never touches the fit.

NEGATIVE CONTROLS (spec R7)
  For every attested pair (source a_k -> recipient word b_k) in recipient r the
  control is (a_j -> b_k) with a_j another source word FROM THE SAME
  RECIPIENT'S OWN SOURCE POOL.  Never the global pool: with global shuffling
  the model can win by learning which donor pool a recipient draws from, signal
  that does not exist in the recognition task the costs are wanted for.  One
  control per attested pair, seed CONTROL_SEED.
  For the record: the original 0.923 harness did NOT do this — see
  scripts/wold_pipeline.py:legacy_validation, whose controls come from the
  global sample.  That is one reason the honest numbers here differ.

CROSS-VALIDATION (spec R3 — the primary result)
  Full leave-one-recipient-out over all 41 recipients: fit on 40, report
  held-out AUC and the fitted parameters for the 41st.  Pairs are never split
  within a recipient.  The headline is the DISTRIBUTION of held-out AUC and of
  the learned weights, not a point estimate.  Runtime is ~30 s/fold, so the
  spec's grouped-K-fold fallback was not needed.

JUDGMENT CALLS BAKED IN
  - Pairs restricted to source_relation == 'immediate' (13,595 of 16,687); see
    scripts/wold_pipeline.py for why.
  - Training compares the donor string to the recipient word DIRECTLY; it does
    not first project the donor string onto the recipient's PHOIBLE inventory,
    even though the deployed metric does listener projection.  Reason: the
    projection is itself computed with the cost model being fitted, which would
    put the parameters on both sides of the objective.  Consequence: the fitted
    costs absorb some of the work projection does at deploy time.  (Only 30 of
    the 41 recipients have a PHOIBLE inventory at all — see
    scripts/wold_coverage.py — so projection was not free to add anyway.)
  - Training similarity is UNCLAMPED (`1 - d/norm` may go negative) so hopeless
    pairs still carry signal; AUC uses the clamped, metric-faithful value.
  - TAU = 0.1: the attested-minus-control gap is ~0.3, so most pairs sit in the
    responsive part of the logistic.  Not tuned.
  - Segment types are interned over the WHOLE corpus (train + held out).  That
    is an encoding table, not a fitted quantity; no held-out pair's score
    depends on any other held-out pair.

Usage:
  uv run python scripts/cost_learning.py                 # full run (~1 h)
  uv run python scripts/cost_learning.py --quick         # 3-fold smoke test
  uv run python scripts/cost_learning.py --lam 0.03      # skip the sweep
"""

from __future__ import annotations

import argparse
import random
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.optimize import minimize
from scipy.stats import spearmanr

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))

from interlang import costs, metric  # noqa: E402
import wold_pipeline as wp  # noqa: E402

PROC = ROOT / "data" / "processed"
PAIRS_CSV = PROC / "wold_pairs.csv"
CONTRAST_CSV = PROC / "contrast_costs.csv"
PHOIBLE = ROOT / "data" / "raw" / "phoible" / "cldf"

RELATION = "immediate"
CONTROL_SEED = 20260804
TAU = 0.1
N_OUTER = 3            # EM re-alignment rounds (the loss plateaus by round 2)
#: Nelder-Mead iterations per inner optimization. A compute-budget choice, not
#: a convergence claim, but a measured one: at 26 parameters the simplex
#: reaches surrogate loss 0.13557 by iteration 1500 and only 0.13484 by 4000
#: (0.5% better for 2.8x the time), and a full run needs 87 fits.
NM_MAXITER = 1500
NM_RESTARTS = 2
LAMBDA_GRID = [0.0, 0.01, 0.03, 0.1, 0.3]
SWEEP_K = 5            # grouped folds used to pick LAMBDA

#: The prior is NOT uniform. syl/son/cons are panphon's MAJOR-CLASS features -
#: they are what makes a vowel a vowel and a consonant a consonant. The
#: unregularized fit drives all three to ~0.04 (see the module docstring), and
#: no amount of uniform shrinkage fixes it at a tolerable AUC cost, because the
#: data genuinely prefers cheap vowel/consonant interchange: WOLD source strings
#: are orthographic, so vowels are routinely unwritten (Semitic transliteration)
#: or inserted by convention, and vowel/consonant confusion is partly an
#: artifact of the transcription rather than a fact about perception.
#: A metric in which a listener may hear a vowel as a consonant for free is not
#: a recognizability metric under any theory, so these three carry a prior
#: MAJOR_PRIOR_MULT times stronger than the rest. This is a judgment call, it is
#: the single most consequential one in this script, and its AUC cost is
#: measured and reported (notes/cost-learning.md §5, guardrail 2).
MAJOR_CLASS = ("syl", "son", "cons")
MAJOR_PRIOR_MULT = 100.0
MAJOR_MULT_OVERRIDE: float | None = None   # set by --major-mult


# ---------------------------------------------------------------------------
# Data assembly
# ---------------------------------------------------------------------------

class Corpus:
    """Attested pairs + within-recipient controls (R7), encoded and batched."""

    def __init__(self, df: pd.DataFrame):
        self.df = df.reset_index(drop=True)
        self.recipients = self.df["recipient"].to_numpy()
        srcs = [metric.segments(s) for s in self.df["source_ipa"]]
        tgts = [metric.segments(s) for s in self.df["target_ipa"]]

        rng = random.Random(CONTROL_SEED)
        by_recipient: dict[str, list[int]] = {}
        for i, r in enumerate(self.recipients):
            by_recipient.setdefault(r, []).append(i)
        ctrl = np.empty(len(srcs), dtype=np.int64)
        for r, idx in by_recipient.items():
            for i in idx:
                j = i
                for _ in range(20):
                    j = rng.choice(idx)
                    if j != i and self.df.at[j, "source_ipa"] != self.df.at[i, "source_ipa"]:
                        break
                ctrl[i] = j
        self.ctrl_idx = ctrl
        self.space = costs.build_space(srcs, tgts)
        self._srcs, self._tgts = srcs, tgts
        self.pos = costs.PairBatch(self.space, srcs, tgts)
        self.neg = costs.PairBatch(self.space, [srcs[j] for j in ctrl], tgts)

    def align(self, params: np.ndarray, model_cls):
        m = model_cls(self.space, params)
        _, phi_p = costs.align_batch(self.pos, m)
        _, phi_n = costs.align_batch(self.neg, m)
        return phi_p, costs.normalizer_rows(self.pos, m), phi_n, costs.normalizer_rows(self.neg, m)


def recipient_groups(recipients: np.ndarray, mask: np.ndarray):
    """R5 rebalancing as a sparse averaging operator.

    Returns (rows, weights) such that `np.bincount(rows, w*x, n_groups).mean()`
    is the mean-over-recipients-of-mean-over-that-recipient's-pairs of x.
    Written this way, not as a Python loop over 41 index arrays, because the
    inner optimizer evaluates the objective tens of thousands of times per fit
    and the loop was the whole cost.
    """
    idx = np.where(mask)[0]
    codes, uniq = pd.factorize(recipients[idx])
    counts = np.bincount(codes, minlength=len(uniq)).astype(float)
    return idx, codes, 1.0 / counts[codes], len(uniq)


# ---------------------------------------------------------------------------
# Objective + fit
# ---------------------------------------------------------------------------

def prior_weights(model_cls, mult: float | None = None) -> np.ndarray:
    """Per-parameter prior strength; see MAJOR_PRIOR_MULT.

    `--major-mult 1` makes the prior uniform, which reproduces the comparison
    curve in notes/cost-learning.md §5 (uniform shrinkage restores the /da/
    gradient too, but only at lambda >= 0.1, and by then it has also undone
    most of the place-of-articulation correction we came for).
    """
    w = np.ones(model_cls.n_params())
    for name in MAJOR_CLASS:
        w[model_cls.param_names().index(name)] = (
            MAJOR_PRIOR_MULT if mult is None else mult)
    return w


def surrogate_loss(params, phi_p, psi_p, phi_n, psi_n, groups, lam,
                   log_prior, pw) -> float:
    sp = costs.similarity_from(phi_p, psi_p, params, clamp=False)
    sn = costs.similarity_from(phi_n, psi_n, params, clamp=False)
    nll = np.logaddexp(0.0, -(sp - sn) / TAU)      # -log sigmoid, computed stably
    idx, codes, w, n_groups = groups
    base = float(np.bincount(codes, weights=w * nll[idx], minlength=n_groups).mean())
    if lam <= 0:
        return base
    dev = np.log(np.maximum(params, 1e-9)) - log_prior
    return base + lam * float(np.mean(pw * dev ** 2))


def held_out_auc(params, phi_p, psi_p, phi_n, psi_n, idx) -> float:
    sp = costs.similarity_from(phi_p[idx], psi_p[idx], params, clamp=True)
    sn = costs.similarity_from(phi_n[idx], psi_n[idx], params, clamp=True)
    return costs.auc(sp, sn)


def fit(corpus: Corpus, train_mask: np.ndarray, model_cls, lam: float,
        n_outer: int = N_OUTER, verbose: bool = False):
    """EM-style outer loop; Nelder-Mead on log-params inside (spec R6)."""
    prior = model_cls.default_params()
    log_prior = np.log(prior)
    pw = prior_weights(model_cls, MAJOR_MULT_OVERRIDE)
    p = model_cls.normalize(prior)
    groups = recipient_groups(corpus.recipients, train_mask)
    history, best_p, best = [], p, np.inf
    for outer in range(n_outer):
        al = corpus.align(p, model_cls)                 # re-align under current p
        honest = surrogate_loss(p, *al, groups, lam, log_prior, pw)
        history.append(honest)
        if honest < best - 1e-9:
            best, best_p = honest, p
        elif outer > 0:
            break                                       # re-aligned loss stopped improving

        def obj(theta):
            return surrogate_loss(model_cls.normalize(np.exp(theta)),
                                  *al, groups, lam, log_prior, pw)

        theta = np.log(np.maximum(p, 1e-4))
        res = None
        for _ in range(NM_RESTARTS):
            res = minimize(obj, theta, method="Nelder-Mead",
                           options=dict(maxiter=NM_MAXITER, xatol=1e-4,
                                        fatol=1e-8, adaptive=True))
            theta = res.x
        p = model_cls.normalize(np.exp(theta))
        if verbose:
            print(f"    outer {outer}: re-aligned {honest:.5f} -> inner {res.fun:.5f}",
                  flush=True)
    return best_p, history


def grouped_folds(recipients: np.ndarray, k: int, seed: int = 0) -> list[list[str]]:
    r = list(pd.unique(recipients))
    order = np.random.default_rng(seed).permutation(len(r))
    return [[r[i] for i in order[f::k]] for f in range(k)]


def lambda_sweep(corpus: Corpus, model_cls, n_outer: int) -> pd.DataFrame:
    """Pick LAMBDA on held-out AUC under grouped K-fold CV. See module docstring."""
    folds = grouped_folds(corpus.recipients, SWEEP_K)
    rows = []
    for lam in LAMBDA_GRID:
        t0 = time.time()
        aucs, ps = [], []
        for f in folds:
            test = np.isin(corpus.recipients, f)
            p, _ = fit(corpus, ~test, model_cls, lam, n_outer=n_outer)
            ps.append(p)
            al = corpus.align(p, model_cls)
            for r in f:
                aucs.append(held_out_auc(p, *al, np.where(corpus.recipients == r)[0]))
        pm = np.mean(ps, axis=0)
        ok, ladder = da_ladder(pm, model_cls)
        rows.append(dict(model=model_cls.__name__, lam=lam,
                         auc_mean=float(np.mean(aucs)), auc_sd=float(np.std(aucs, ddof=1)),
                         da_ladder_ok=ok,
                         sutoraiku=sutoraiku(pm, model_cls),
                         seconds=round(time.time() - t0, 1)))
        print(f"    lambda {lam:<6} held-out AUC {rows[-1]['auc_mean']:.4f} "
              f"(sd {rows[-1]['auc_sd']:.4f})  /da/-ladder {'OK' if ok else 'BAD'}  "
              f"sutoraiku {rows[-1]['sutoraiku']:.3f}  [{rows[-1]['seconds']:.0f}s]",
              flush=True)
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Guardrails
# ---------------------------------------------------------------------------

LADDER = ["ta", "ða", "ɡa", "fa", "ma", "ia"]
CONTRAST_DETAIL: list[pd.DataFrame] = []
JAPANESE_FALLBACK = ("a", "e", "i", "o", "ɯ", "k", "ɡ", "s", "z", "t", "d", "n",
                     "h", "b", "p", "m", "j", "ɾ", "w", "ɲ", "ç", "ɸ", "ɕ", "ʑ", "ɴ")


def da_ladder(params, model_cls) -> tuple[bool, list[float]]:
    s = [costs.similarity(metric.segments("da"), metric.segments(x), params, model_cls)
         for x in LADDER]
    return bool(all(s[i] > s[i + 1] for i in range(len(s) - 1))), s


def sutoraiku(params, model_cls) -> float:
    return costs.similarity(metric.segments("stɹaik"), metric.segments("sɯtoɾaikɯ"),
                            params, model_cls)


def japanese_inventory() -> tuple[str, ...]:
    """Japanese phonemes from PHOIBLE (majority vote across its inventories)."""
    try:
        vals = pd.read_csv(PHOIBLE / "values.csv", low_memory=False)
        sub = vals[vals["Language_ID"] == "nucl1643"]     # Language_ID is the Glottocode
        if sub.empty:
            return JAPANESE_FALLBACK
        n_inv = sub["Inventory_ID"].nunique()
        counts = sub.groupby("Value")["Inventory_ID"].nunique()
        keep = [v for v, c in counts.items() if c >= max(1, n_inv / 2)]
        keep = [v for v in keep if len(metric.segments(v)) == 1]
        return tuple(keep) or JAPANESE_FALLBACK
    except Exception:
        return JAPANESE_FALLBACK


def project_nearest(seg: str, inventory: tuple[str, ...], params: np.ndarray):
    space = costs.SegmentSpace([seg] + list(inventory))
    sub = costs.FeatureWeightCosts(space, params[:costs.N_FEATURES]).sub_matrix()
    out = [(p, float(sub[space.index[seg], space.index[p]]))
           for p in inventory if p in space.index and p != seg]
    out.sort(key=lambda x: x[1])
    return out


def contrast_crosscheck(params_learned: np.ndarray, model_name: str) -> dict:
    """Guardrail 5: non-loanword anchor. Do learned costs track PHOIBLE contrasts?

    contrast_costs.csv prices each contrast by the share of humanity whose
    native phonology distinguishes it. A widely MERGED contrast (low
    pct_l1_both, many merger_langs) should be CHEAP under a cost model that
    captures perceptual distinguishability, so we expect substitution cost to
    correlate positively with pct_l1_both and negatively with merger_langs.
    What matters is whether the LEARNED costs track it BETTER than panphon's
    defaults: any feature metric gets some of this for free, because
    phonetically close pairs are both cheap and often merged.
    """
    cdf = pd.read_csv(CONTRAST_CSV)
    rows = []
    for r in cdf.itertuples(index=False):
        if "/" not in r.contrast:
            continue
        a, b = [x.strip() for x in r.contrast.split("/", 1)]
        if len(metric.segments(a)) != 1 or len(metric.segments(b)) != 1:
            continue
        sa, sb = metric.segments(a)[0], metric.segments(b)[0]
        rows.append(dict(contrast=r.contrast, a=sa, b=sb, pct_l1_both=r.pct_l1_both,
                         merger=float(r.merger_langs) if pd.notna(r.merger_langs) else 0.0,
                         cost_default=costs.substitution_cost(sa, sb, costs.PANPHON_WEIGHTS),
                         cost_learned=costs.substitution_cost(
                             sa, sb, params_learned[:costs.N_FEATURES])))
    t = pd.DataFrame(rows)
    r_d = spearmanr(t.cost_default, t.pct_l1_both)
    r_l = spearmanr(t.cost_learned, t.pct_l1_both)
    rho_d, rho_l = r_d.statistic, r_l.statistic
    m_d = spearmanr(t.cost_default, t.merger).statistic
    m_l = spearmanr(t.cost_learned, t.merger).statistic
    t.insert(0, "model", model_name)
    CONTRAST_DETAIL.append(t)
    # PASS CRITERION: the learned costs must show a rank correlation with
    # contrast prevalence that is BOTH positive AND distinguishable from noise
    # (p < 0.05 at n ~ 23). "rho went up a bit" is not convergence with an
    # independent anchor, it is a coin landing the right way up; an earlier,
    # looser criterion (rho_l > rho_d) scored a rho of +0.06 as a pass, which
    # is exactly the kind of vacuous green tick this guardrail exists to avoid.
    return dict(
        guardrail="5 contrast-study cross-check (non-loanword anchor)",
        detail=(f"n={len(t)} single-segment contrasts. rho(cost, pct_l1_both): default "
                f"{rho_d:+.3f} (p={r_d.pvalue:.2f}) -> learned {rho_l:+.3f} "
                f"(p={r_l.pvalue:.2f}); want positive and significant. "
                f"rho(cost, merger_langs): default {m_d:+.3f} -> learned {m_l:+.3f} "
                f"(want negative and lower)"),
        value=float(rho_l), passed=bool(rho_l > 0 and r_l.pvalue < 0.05))


def guardrails(params, model_cls, cv: pd.DataFrame) -> list[dict]:
    d = model_cls.default_params()
    rows = []

    dl, dfa = cv["auc_learned"], cv["auc_default"]
    rows.append(dict(
        guardrail="1 learned >= default under identical recipient-grouped CV",
        detail=(f"held-out AUC mean {dl.mean():.4f} (sd {dl.std(ddof=1):.4f}, "
                f"min {dl.min():.4f}) vs default {dfa.mean():.4f} "
                f"(sd {dfa.std(ddof=1):.4f}, min {dfa.min():.4f}); learned wins on "
                f"{(dl > dfa).sum()}/{len(cv)} recipients; paired delta "
                f"{(dl - dfa).mean():+.4f} +- {(dl - dfa).std(ddof=1):.4f}"),
        value=float((dl - dfa).mean()), passed=bool(dl.mean() > dfa.mean())))

    ok, s_new = da_ladder(params, model_cls)
    _, s_old = da_ladder(d, model_cls)
    rows.append(dict(
        guardrail="2 /da/ sanity gradient ta > dha > ga > fa > ma > ia",
        detail=("learned " + " ".join(f"{l}={v:.3f}" for l, v in zip(LADDER, s_new))
                + " | default " + " ".join(f"{l}={v:.3f}" for l, v in zip(LADDER, s_old))),
        value=float(min(np.diff(s_new))), passed=ok))

    inv = japanese_inventory()
    n_new, n_old = project_nearest("v", inv, params), project_nearest("v", inv, d)
    rows.append(dict(
        guardrail="3 /v/ projected onto a Japanese-like inventory -> /b/ not /z/",
        detail=(f"learned top-3 {[(x, round(c, 3)) for x, c in n_new[:3]]} | default "
                f"top-3 {[(x, round(c, 3)) for x, c in n_old[:3]]} (inventory n={len(inv)})"),
        value=float(n_new[0][1]), passed=bool(n_new[0][0] == "b")))

    s4o, s4n = sutoraiku(d, model_cls), sutoraiku(params, model_cls)
    rows.append(dict(
        guardrail="4 sutoraiku vs strike (target 0.62 -> 0.9s)",
        detail=f"default {s4o:.3f} -> learned {s4n:.3f}",
        value=float(s4n), passed=bool(s4n >= 0.85)))

    rows.append(contrast_crosscheck(params, model_cls.__name__))
    for r in rows:
        r["model"] = model_cls.__name__
    return rows


# ---------------------------------------------------------------------------

def run_model(corpus, model_cls, lam, folds, n_outer, verbose=True):
    t0 = time.time()
    p_full, hist = fit(corpus, np.ones(corpus.pos.n, bool), model_cls, lam,
                       n_outer=n_outer, verbose=verbose)
    print(f"  full-data fit: loss {hist[0]:.5f} -> {min(hist):.5f} "
          f"({time.time() - t0:.0f}s)", flush=True)

    default = model_cls.default_params()
    al_def = corpus.align(default, model_cls)
    rows = []
    for n, held in enumerate(folds, 1):
        t0 = time.time()
        test = corpus.recipients == held
        p_fold, h = fit(corpus, ~test, model_cls, lam, n_outer=n_outer)
        idx = np.where(test)[0]
        a_def = held_out_auc(default, *al_def, idx)
        a_lrn = held_out_auc(p_fold, *corpus.align(p_fold, model_cls), idx)
        row = dict(model=model_cls.__name__, held_out_recipient=held,
                   n_pairs=int(test.sum()), auc_default=a_def, auc_learned=a_lrn,
                   train_loss_start=h[0], train_loss_end=min(h))
        row.update({f"w_{k}": v for k, v in zip(model_cls.param_names(), p_fold)})
        rows.append(row)
        print(f"  [{n:2d}/{len(folds)}] {held:18s} n={row['n_pairs']:5d}  AUC "
              f"{a_def:.4f} -> {a_lrn:.4f}  ({time.time() - t0:.0f}s)", flush=True)
    return p_full, pd.DataFrame(rows)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--quick", action="store_true", help="3 folds, 2 outer, tiny sweep")
    ap.add_argument("--lam", type=float, default=None, help="skip the sweep, use this lambda")
    ap.add_argument("--models", default="feature,context")
    ap.add_argument("--major-mult", type=float, default=None,
                    help="override MAJOR_PRIOR_MULT (1 = uniform prior)")
    ap.add_argument("--report-only", action="store_true",
                    help="recompute the guardrails from the committed CSVs, no fitting")
    args = ap.parse_args()
    if args.major_mult is not None:
        global MAJOR_MULT_OVERRIDE
        MAJOR_MULT_OVERRIDE = args.major_mult
        print(f"major-class prior multiplier overridden to {args.major_mult}")

    if args.report_only:
        cv_all = pd.read_csv(PROC / "cost_learning_cv.csv")
        pr = pd.read_csv(PROC / "learned_costs.csv")
        rows = []
        for name in args.models.split(","):
            cls = costs.MODELS[name]
            sub = pr[pr["model"] == cls.__name__]
            p_full = sub.set_index("parameter").loc[cls.param_names(), "learned_full"].to_numpy()
            rows.extend(guardrails(p_full, cls, cv_all[cv_all["model"] == cls.__name__]))
        pd.DataFrame(rows).to_csv(PROC / "cost_learning_guardrails.csv", index=False)
        if CONTRAST_DETAIL:
            pd.concat(CONTRAST_DETAIL, ignore_index=True).to_csv(
                PROC / "cost_learning_contrast_check.csv", index=False)
        for r in rows:
            print(f"  [{'PASS' if r['passed'] else 'FAIL'}] ({r['model']}) {r['guardrail']}")
            print(f"          {r['detail']}")
        return

    pairs = wp.load_pairs(PAIRS_CSV)
    pairs = pairs[pairs["source_relation"] == RELATION].reset_index(drop=True)
    print(f"pairs {len(pairs)}  recipients {pairs['recipient'].nunique()}  "
          f"donors {pairs['donor'].nunique()}  (source_relation == '{RELATION}')")
    t0 = time.time()
    corpus = Corpus(pairs)
    print(f"segment types {len(corpus.space)}  corpus built in {time.time() - t0:.1f}s\n")

    n_outer = 2 if args.quick else N_OUTER
    recipients = list(pd.unique(corpus.recipients))
    folds = recipients[:3] if args.quick else recipients
    model_names = args.models.split(",")
    primary = costs.MODELS[model_names[0]]

    # --- LAMBDA selection ---------------------------------------------------
    if args.lam is not None:
        lam, sweep = args.lam, None
        print(f"lambda fixed at {lam} (sweep skipped)")
    else:
        print(f"lambda sweep on {primary.__name__} (grouped {SWEEP_K}-fold):")
        global LAMBDA_GRID
        if args.quick:
            LAMBDA_GRID = [0.0, 0.03]
        sweep = lambda_sweep(corpus, primary, n_outer)
        sweep.to_csv(PROC / "cost_learning_lambda.csv", index=False)
        # SELECTION RULE: highest held-out AUC AMONG the lambdas that preserve
        # the /da/ sanity gradient (guardrail 2). Unregularized always wins on
        # raw AUC, and always produces a metric in which /d/->/i/ is cheaper
        # than /d/->/f/. Trading a phonetically incoherent metric for a
        # fraction of a point of AUC is not a trade this project wants, and
        # making the rule explicit is better than quietly deleting lambda=0
        # from the grid. The whole curve, lambda=0 included, is in the CSV so
        # the price of the constraint is visible.
        ok = sweep[sweep["da_ladder_ok"]]
        if ok.empty:
            lam = float(sweep.loc[sweep["auc_mean"].idxmax(), "lam"])
            print("  !! no lambda preserves the /da/ gradient; falling back to max AUC")
        else:
            lam = float(ok.loc[ok["auc_mean"].idxmax(), "lam"])
        print(f"  -> LAMBDA = {lam}  (best AUC among ladder-preserving lambdas)\n")

    # --- per-model LORO -----------------------------------------------------
    all_cv, all_params, all_guard = [], [], []
    for name in model_names:
        cls = costs.MODELS[name]
        print(f"=== model '{name}' ({cls.__name__}), lambda {lam} ===", flush=True)
        p_full, cv = run_model(corpus, cls, lam, folds, n_outer)
        all_cv.append(cv)
        wcols = [f"w_{k}" for k in cls.param_names()]
        params = pd.DataFrame(dict(
            model=cls.__name__, parameter=cls.param_names(),
            panphon_default=cls.default_params(), learned_full=p_full,
            loro_mean=cv[wcols].mean().to_numpy(), loro_sd=cv[wcols].std(ddof=1).to_numpy(),
            loro_min=cv[wcols].min().to_numpy(), loro_max=cv[wcols].max().to_numpy()))
        params["ratio_to_default"] = params["loro_mean"] / params["panphon_default"]
        params["rel_sd"] = params["loro_sd"] / params["loro_mean"]
        all_params.append(params)
        all_guard.extend(guardrails(p_full, cls, cv))

        print(f"\n--- R3 held-out AUC, leave-one-recipient-out ({name}) ---")
        for col in ("auc_default", "auc_learned"):
            s = cv[col]
            print(f"  {col:12s} mean {s.mean():.4f}  sd {s.std(ddof=1):.4f}  "
                  f"min {s.min():.4f}  med {s.median():.4f}  max {s.max():.4f}")
        dlt = cv["auc_learned"] - cv["auc_default"]
        print(f"  paired delta {dlt.mean():+.4f} sd {dlt.std(ddof=1):.4f}  "
              f"wins {(dlt > 0).sum()}/{len(cv)}   pair-weighted: default "
              f"{np.average(cv.auc_default, weights=cv.n_pairs):.4f} learned "
              f"{np.average(cv.auc_learned, weights=cv.n_pairs):.4f}")
        print(params.to_string(index=False, float_format=lambda x: f"{x:8.3f}"))
        print()

    cv = pd.concat(all_cv, ignore_index=True)
    cv.to_csv(PROC / "cost_learning_cv.csv", index=False)
    pd.concat(all_params, ignore_index=True).to_csv(PROC / "learned_costs.csv", index=False)
    pd.DataFrame(all_guard).to_csv(PROC / "cost_learning_guardrails.csv", index=False)
    if CONTRAST_DETAIL:
        pd.concat(CONTRAST_DETAIL, ignore_index=True).to_csv(
            PROC / "cost_learning_contrast_check.csv", index=False)

    print("=== guardrails ===")
    for r in all_guard:
        print(f"  [{'PASS' if r['passed'] else 'FAIL'}] ({r['model']}) {r['guardrail']}")
        print(f"          {r['detail']}")
    print(f"\nwrote {PROC}/(learned_costs|cost_learning_cv|cost_learning_lambda|"
          f"cost_learning_guardrails|cost_learning_contrast_check).csv")


if __name__ == "__main__":
    main()
