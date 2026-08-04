# Study spec: learning substitution + epenthesis costs for the recognizability metric

*Status: SPEC (not yet run). Written 2026-08-03; amended 2026-08-04 (R1 two
baselines, R6 objective mechanics, R7 within-recipient controls, guardrail 1
restated, environment/runtime notes — see "Amendments" at the end). Companion to
[`principles.md`](principles.md) §4 and §7.5, [`data-audit.md`](data-audit.md)
(metric known-issues 1 & 2). This document is the agreed plan; the eventual
study script and its `notes/` write-up supersede it once the work is done.*

## Motivation

The recognizability metric (`src/interlang/metric.py`, v0) uses panphon's
**default feature weights**, which are hand-assigned subjective guesses (all
powers of two; never fitted to data — the file's own docstring says the weights
reflect "the subjective probability of the feature changing in phonological
alternation and loanword contexts"). Two characterized failure modes follow:

1. **Place of articulation underweighted.** panphon has no single "place"
   feature; place is smeared across several cheap binary features (ant, cor,
   lab, distr @ 0.125–0.25) while manner has one heavyweight feature
   (continuant @ 0.5). Net effect on a diagnostic case: `/v/→/z/` costs 1.125
   but `/v/→/b/` costs 1.250, so projection onto a Japanese-like inventory maps
   /v/→/z/ where real loanword adaptation gives /v/→/b/. The margin is one flip
   of the cheapest feature class — a knife-edge decided the wrong way. The
   weight hierarchy encodes phonological *stability* (how often a feature
   alternates within a grammar), but loanword/recognition perception is a
   *salience* task, and labiality is perceptually robust (visible on the lips,
   strong formant transitions). Wrong prior for the job.

2. **No epenthesis modeling.** Insertion/deletion cost in panphon is just
   `sum(weights)` — a flat per-segment price with no notion that inserting a
   vowel to repair an illegal cluster is cheap. "sutoraiku" vs "strike" scores
   only ~0.62. Consequence: the metric **systematically flatters permissive
   codas**, which is exactly the bias that would corrupt the next planned
   experiment (projection distortion across syllable templates, §3.6 / §7.4).

## Goal

Replace the hand-guessed cost structure with one **learned from WOLD's attested
loanword adaptations** (~20,615 usable recipient/source pairs after filtering).
Substitution and insertion/deletion costs are learned **jointly** — they are
one optimization, not two (see Requirement R2).

## The five agreed calls (from discussion 2026-08-03)

1. **Cost form: fit panphon's per-feature weights** (the ~22-vector), not a full
   segment×segment matrix — comfortable parameter/data ratio, generalizes to
   unseen segment pairs, interpretable, drops into the existing metric with no
   structural change. The matrix (Jäger-style PMI) stays a documented later
   upgrade. **But** the harness must keep the cost function **swappable behind
   an interface** (R4), because a single global weight-per-feature cannot express
   two things we may need: **asymmetry** (foreign→native is directional; /v/→/b/
   common, /b/→/v/ not — though listener-projection already absorbs much of this
   structurally) and **feature interactions** ("place matters more for stops than
   vowels"). Expressiveness is a dial tuned against the stability curve (R3), not
   guessed up front.
2. **Objective: discriminative** — optimize the weights so attested pairs
   outscore shuffled controls (the quantity the metric is actually consumed for:
   ranking). EM-style alignment may *initialize* it. AUC is the *evaluation*
   quantity; what actually gets optimized is a smooth surrogate or a
   derivative-free search — see R6.
3. **Epenthesis rides along as a REQUIREMENT**, not a stretch goal (R2).
4. **Guardrails** (see Requirements): beat the default-weight baseline on
   held-out recipients under identical CV (amended — see guardrail 1, which
   supersedes the original "hold/beat AUC 0.923" wording); preserve the /da/
   sanity gradient; flip the /v/→/b/ diagnostic;
   report sutoraiku/strike before-after; **cross-check learned costs against the
   contrast study** as a non-loanword anchor.
5. **Per-recipient rebalancing** of the training objective so a few
   data-heavy recipients don't dominate (see R5).

## WOLD recipient sample — measured composition (2026-08-03)

41 recipient languages, 20,615 usable pairs (usable = non-empty `Source_word`).
Measured from `data/raw/wold/cldf/` joined to `data/processed/l1_speakers.csv`:

- **Typological breadth is good and is WOLD's design strength:** 24 families
  across all 6 macroareas (Eurasia 19 recipients / 10,777 pairs, Africa 8 /
  4,664, South America 6 / 2,179, Papunesia 3, North America 4, Australia 1).
  Berber, Romani, Japanese, Saramaccan creole, Gurindji, Sakha, White Hmong,
  Quechua, Mayan, Malagasy, Ket, etc.
- **Population coverage is poor and anti-correlated with data volume:**
  recipients sum to ~1.69B L1 ≈ 21% of world, but Mandarin (918M) + English
  (379M) are ~77% of that L1 mass while contributing only 107 and 1,085 usable
  pairs. **This is accepted, not a defect** (see Assumptions): we are not
  population-weighting.
- **Pair counts are top-heavy but not pathological:** largest recipients are
  Tarifiyt Berber (1,454), Selice Romani (1,511), Romanian (1,383), Indonesian
  (1,077), English (1,085); median ~410. English is *not* wildly
  overrepresented by pairs. The tail is thin: Old High German (92), Manange
  (122), Ket (122), Oroqen (152) — several recipients have only ~100–300 pairs,
  **too few for a single held-out AUC to be stable** → drives R3.
- **Donors are more concentrated and skew European/classical:** Spanish
  (2,125), Chinese (1,167), English (1,157), Arabic (1,132), French (1,113),
  Latin, Hungarian, Russian, Sanskrit, Classical Arabic. Donors supply the
  *source* string, so a substitution model can overfit "how European/classical
  phonologies map into these 41 languages" → logged caveat, optional donor
  rebalancing.

## Assumptions we are accepting (Patrick, 2026-08-03)

- **Poor L1 coverage is fine.** Assimilative/adaptation processes are similar
  for phonologically similar languages, so learning from a typologically wide
  sample transfers to unseen languages that are phonologically near a sample
  member. We calibrate to *phonological* structure, not to a population sample.
- **Wide family coverage ⇒ wide phonological-type coverage.** 24 families across
  6 macroareas is taken as adequate coverage of the phonological space. (The
  write-up should still *report* a hard coverage number — see Deliverables — but
  the assumption is that it will come out adequate.)

## Requirements

**R1 — Reconstruct + commit the WOLD pipeline first.** The cleaning/validation
code that produced "13,779 clean pairs, AUC 0.923" is **not in the repo** (grep
confirms no script references WOLD). Step zero: rebuild WOLD source-word
cleaning and the AUC validation as a committed script under `scripts/`, per the
"one study per script" convention, reproducing (approximately) the recorded
baseline before changing anything. Document the cleaning filter's judgment calls
in its docstring.

R1 must produce **two** baselines, not one:

- **(a) Legacy-protocol reproduction** — approximately recover AUC 0.923 under
  the original loose protocol (sampled pairs, not recipient-grouped). This
  exists only to confirm the pipeline reconstruction is faithful.
- **(b) Honest-protocol default-weight baseline** — run **unmodified panphon
  default weights** through the *same* recipient-grouped CV (R3) and the same
  control-construction rule (R7) that the learned model will face.

Rationale: 0.923 came from a possibly-leaky, non-recipient-grouped split.
Comparing learned-weights-under-honest-CV against default-weights-under-legacy-
protocol is apples to oranges. Guardrail 1 is judged on (b).

The **working pair set is whatever the rebuilt cleaning filter yields**; the
spec's ~20,615 (usable = non-empty `Source_word`) and the recorded 13,779
(conservatively cleaned) bracket the plausible range. Report the actual number
and the filter's judgment calls rather than targeting either figure.

Also record the **WOLD commit hash** used (README pins `0df955a`) in the
script's output/docstring. Results should not be sensitive to the dataset
version — if they are, that is itself a finding worth flagging — but the version
is recorded for posterity.

**R2 — Joint substitution + epenthesis fit (hard requirement).** Insertion/
deletion cost currently = `sum(weights)`, which *moves* when substitution
weights are retrained; holding it stale contaminates the alignments and thus the
substitution counts learned from them. Fit the parameter vector
`{feature weights} ∪ {insertion/deletion cost structure}` **together**. The
sutoraiku/strike recovery is a training-time target, not a post-hoc check.
Context-sensitive epenthesis (insertion cheap *only* adjacent to an illegal
cluster) remains an explicit **stretch goal**, not part of the required joint fit.

**R3 — Repeated recipient-level cross-validation is the PRIMARY result**, not a
nicety. Because recipients are few and uneven, any single split's AUC is noise.
Do **leave-one-recipient-out** (all 41) and/or repeated grouped K-fold **grouped
by recipient** (never split pairs within a recipient — that leaks
recipient-specific adaptation patterns and inflates AUC). Report the
**distribution** of held-out AUC and of the learned weights across folds. The
headline deliverable is a *stability* statement, e.g. "the place-vs-manner
reweighting is stable across held-out recipients: lab weight = X ± b."

**R4 — Swappable cost model.** Build train/eval/guardrail scaffolding with the
cost function behind an interface, so a richer model (small segment-pair matrix,
low-rank feature-interaction term, asymmetric costs) can be dropped in later
without rewriting the study. Ship the feature-weight model; leave the seam.

**R5 — Per-recipient objective rebalancing.** Weight the discriminative loss so
data-heavy recipients (Berber, Romani, Romanian) don't dominate — e.g. equal
weight per recipient, or inverse-frequency. **Do NOT population-weight** (that
collapses everything onto Mandarin+English and discards the typological breadth
that makes WOLD worth using). Optional: per-donor rebalancing to blunt the
Spanish/Latin/Arabic skew; if not done, log it as a caveat.

**R6 — Do not gradient-optimize AUC directly.** AUC is a pure ranking measure:
as a function of the weights it is a **flat staircase** — zero derivative
almost everywhere, discrete jumps of 1/(n₊·n₋) when a pair swaps order. A
gradient optimizer reads that flatness as "already optimal" and stops. Two
sanctioned routes (agent picks and documents; both are acceptable):

- **Smooth pairwise surrogate.** For an attested pair scoring `s⁺` and its
  matched control scoring `s⁻`, minimize `−log(sigmoid(s⁺ − s⁻))` (logistic) or
  `max(0, m − (s⁺ − s⁻))` (margin/hinge), summed over pairs with R5
  rebalancing. Nonzero gradient everywhere it matters.
- **Derivative-free optimization** (Nelder–Mead, CMA-ES) on AUC or the
  surrogate directly. Entirely feasible at ~23 parameters and it sidesteps the
  alignment problem below. Mild default given the low dimension.

**Alignment wrinkle:** similarity is the output of an edit-distance alignment,
so `s⁺ − s⁻` is not a clean smooth function of the weights — the optimal
alignment path can change discontinuously as weights move. This is the R2
"epenthesis moves the alignments" problem in another guise. Derivative-free
optimization avoids it; the gradient route must handle it EM-style (hold
alignments fixed within a step, re-align, refit).

**AUC is computed on held-out folds as the report card only** — never touched
during fitting.

**R7 — Negative controls must be shuffled WITHIN recipient.** Draw each
control's source word from *the same recipient language's own source pool*,
never from the global pool.

Why this is load-bearing: with global shuffling, a Japanese output can be paired
against an Arabic source that really belongs to Berber. The model then wins the
discrimination task by learning a **recipient/donor-pool detector** ("Japanese
output rarely comes from a pharyngeal-heavy source") rather than adaptation
structure. Held-out AUC looks excellent and the learned weights are worthless
for our purpose, because the exploited signal — which donor pool a recipient
draws from — does not exist in the recognition task at all. Within-recipient
shuffling makes the control's source equally plausible as a donor, so the only
way to separate attested from control is to notice that the segments actually
map (`strike`→`sutoraiku` does; `television`→`sutoraiku` does not).

This is a cheap structural defense against the concept caveat below (fitting
loanword-specific artifacts instead of perceptual substitution structure).
Tightening further to within-donor-language shuffling is optional; the
within-recipient rule is the requirement. **R1 should report whether the
original 0.923 harness did this** — if it did not, that is further reason to
treat the honest recipient-grouped number as the real reset point.

## Guardrails (must all be reported, pass/fail)

1. **Learned ≥ default under identical honest CV.** Held-out AUC (R3
   distribution) for the learned costs must beat the R1(b) default-panphon-weight
   baseline run through the *same* recipient-grouped CV and the same R7 controls.
   Report both distributions, not just point estimates. The legacy 0.923 is a
   reference point for the R1(a) reconstruction only — it is **not** the bar,
   since it came from a looser protocol; the honest numbers may both land lower
   and that is expected, not a failure.
2. `/da/` sanity gradient preserved: ta > ða > ɡa > fa > ma > ia.
3. **Diagnostic flip:** /v/ projected onto a Japanese-like inventory → /b/, not
   /z/.
4. sutoraiku vs strike reported before/after (target: 0.62 → 0.9s).
5. **Contrast-study cross-check (non-loanword anchor).** Learned costs should
   agree with the independent PHOIBLE-derived contrast numbers
   (`data/processed/contrast_costs.csv`) — e.g. pairs the contrast study prices
   as widely-merged (r/l for the relevant listeners, h/x) should come out cheap
   in the learned costs. Convergence = evidence the costs capture perceptual
   distinguishability/recognition, not just loanword-specific (production-
   mediated, orthography-contaminated) artifacts. Divergence = flag for
   overfitting to loanword idiosyncrasy.

## Concept caveat baked into the interpretation (discussion point 3)

We calibrate on **loanword adaptation** (production-mediated, whole-word,
top-down, listener *already knew the word*, orthography-influenced) but *use*
the result for **recognition** (naive listener, unknown word) and
**distinguishability** (two of our own words, symmetric, no source). These are
three different concepts. Protection: fit to the *segmental substitution/
insertion* structure (what maps to what), be skeptical of anything that looks
like fitting an orthographic/morphological artifact of one donor, and use
guardrail 5 as the independent perceptual anchor. One learned perceptual cost
model, validated against a non-loanword source before we trust it for (a)/(b).

## Deliverables (project conventions)

- `scripts/wold_pipeline.py` (or similar) — R1, committed, docstring documents
  cleaning judgment calls.
- The cost-learning study script — reads WOLD + panphon, writes learned params
  to `data/processed/` (committed), runs R3 CV, emits all guardrails.
- A `notes/` write-up interpreting results, with: the R3 stability tables, a
  **hard phonological-coverage figure** (fraction of common PHOIBLE segments
  appearing in ≥1 recipient inventory; which regions/inventory-types are
  thin/absent), the loanword-vs-recognition caveat, and updates to
  `data-audit.md` known-issues 1 & 2 (from "known" toward "fixed/bounded").
- Update `principles.md` §4 and §7.5 to reflect the new metric version.

## Sequencing for the agent

0. **Environment.** `data/raw/` is gitignored and absent in a fresh checkout —
   re-fetch WOLD (and PHOIBLE, needed for the guardrail-3 listener inventory and
   for R4/guardrail-5 work) per the README's clone commands, and install panphon.
   Record dataset commit hashes.
1. R1: reconstruct + commit WOLD pipeline; produce baseline (a) legacy-protocol
   reproduction and (b) default-weight honest-CV baseline.
2. Joint cost-learning (R2) with the discriminative objective (R6 surrogate or
   derivative-free), R7 within-recipient controls, feature-weight model behind
   the R4 interface, R5 rebalancing.
3. R3 repeated recipient-level CV; collect weight + AUC distributions.
   **Prefer full leave-one-recipient-out (all 41).** If runtime is prohibitive
   — 41 optimization runs with alignment in the inner loop — fall back to
   repeated grouped K-fold and *document the fallback and its reason*; do not
   stall on this.
4. Guardrails 1–5; write-up + notes/data-audit updates.

## Amendments (2026-08-04, Patrick + Claude)

Four changes agreed before handing the study to an agent. None changes the
study's shape; each closes a "looks great, means nothing" trap.

1. **Guardrail 1 needed a same-protocol baseline.** The original wording
   compared learned-weights-under-honest-CV to the legacy 0.923, which was
   measured under a looser protocol. R1 now produces a default-panphon-weight
   baseline under the identical recipient-grouped CV, and guardrail 1 is judged
   against *that*.
2. **AUC is not differentiable** — added R6. Optimize a smooth pairwise
   surrogate or use derivative-free search; AUC stays the evaluation quantity.
   The edit-distance alignment makes the objective non-smooth regardless, which
   is the same hazard R2 flags for epenthesis.
3. **Controls must be shuffled within recipient** — added R7. Global shuffling
   lets the model win by detecting donor pools instead of learning adaptation
   structure.
4. **Environment + runtime** — `data/raw/` must be re-fetched; dataset commit
   hashes recorded for posterity (results should not be version-sensitive);
   full LORO preferred with a documented K-fold fallback rather than stalling.
   The working pair-set size is whatever the rebuilt filter yields (~13.8k–20.6k
   bracket), reported rather than targeted.
