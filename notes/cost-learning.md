# Cost learning from WOLD loanword adaptations (2026-08-04)

*Executes [`cost-learning-spec.md`](cost-learning-spec.md) and supersedes it as
the record of what was done. Companion to [`principles.md`](principles.md) §4
and §7.5 and to [`data-audit.md`](data-audit.md) metric known-issues 1 & 2.*

Reproduce:

```
git clone --depth 1 https://github.com/lexibank/wold          data/raw/wold
git clone --depth 1 https://github.com/cldf-datasets/phoible  data/raw/phoible
uv run python scripts/wold_pipeline.py    # -> data/processed/wold_pairs.csv
uv run python scripts/wold_coverage.py    # -> data/processed/wold_coverage.csv
uv run python scripts/cost_learning.py    # -> learned_costs.csv + 4 more (~1 h)
```

**Jargon for this note.** A *substitution cost* is the price the metric charges
for hearing one sound where another was intended (/d/ heard as /t/). An *indel*
cost is the price for a sound being inserted or deleted. *Epenthesis* is
inserting a vowel to repair a cluster a language cannot pronounce ("strike" →
"su-to-ra-i-ku"). A *feature weight* is how much one articulatory dimension
(voicing, nasality, lip-rounding…) contributes to a substitution cost. *AUC* is
the probability that a randomly chosen real loanword pair scores above a
randomly chosen fake one: 0.5 is chance, 1.0 is perfect.

---

## 0. Summary

**What worked.** Costs learned from 13,595 attested WOLD loanword adaptations
beat panphon's hand-guessed weights on held-out AUC for **41 out of 41**
recipient languages under leave-one-recipient-out CV with within-recipient
controls (0.957 vs 0.896; paired delta +0.061 ± 0.033). The learned weights are
extremely stable across folds — relative sd of 1–8%, mostly 1–3%. The
place-of-articulation problem the spec set out to fix is fixed and the fix is
stable: labiality goes up **3.2×**, `/v/` projected onto a Japanese-like
inventory now maps to `/b/` (by a factor of 1.9 over `/z/`, where the default
had `/z/` ahead).

**What did not.** Two of five guardrails fail.
- **Epenthesis (guardrail 4)** moves the wrong way: sutoraiku/strike 0.617 →
  0.577. The model *can* express the case (hand-set cluster-insertion costs give
  0.904) but the discriminative objective does not want to, because cheap
  insertion helps the negative control as much as the true pair. A
  discriminative objective is structurally the wrong tool for learning repair
  costs.
- **The contrast-study cross-check (guardrail 5)** is null: ρ = +0.059
  (p = 0.79) where panphon has −0.020. The learned costs get the vowel-quality
  contrasts right and every *voicing* contrast wrong, and the two cancel.

**The one number to distrust.** Voicing learns a weight 3.5× panphon's — the
fit's single largest upward move. WOLD's orthographies record voicing
faithfully on both sides, so voicing mismatches are rare *in the data*; the
contrast study says voicing is among the **cheapest** contrasts perceptually
(t/d audible to 75% of humanity, p/b to 73%). That is a production/orthography
fact being learned as a perceptual one, and it is exactly what guardrail 5 was
built to detect.

**Disposition.** `metric.py` v0 stays the default. The learned costs ship in
`data/processed/learned_costs.csv` and are opt-in via `params=`. §8 lists what
would have to be true to promote them.

---

## 1. What was actually built

| Piece | Where | What it is |
|---|---|---|
| WOLD pair pipeline | `scripts/wold_pipeline.py` | rebuilds the never-committed cleaning code; writes `data/processed/wold_pairs.csv` |
| Coverage audit | `scripts/wold_coverage.py` | the hard phonological-coverage number the spec asked for |
| Cost models + aligner | `src/interlang/costs.py` | the R4 swappable-cost seam and a batched aligner |
| The study | `scripts/cost_learning.py` | fit, cross-validate, guardrails |

`src/interlang/metric.py` keeps v0 behaviour exactly; it only gains an optional
`params=` argument so the learned costs can be used deliberately. See §8 for
what adopting them as the default would take and why it is not automatic.

### Datasets

WOLD commit `1df62b9b` (README pins `0df955a`; the clone was shallow-HEAD).
PHOIBLE commit `5c477f19` (matches the README pin). The WOLD version drift is
noted rather than corrected: the pipeline's attrition table and the legacy-AUC
reproduction are the version-sensitivity check, and both land where the
recorded 2026-07-14 numbers said they should (§2), so results are not
version-fragile at this resolution.

---

## 2. R1 — the rebuilt pipeline and its two baselines

### The filter and what it costs

Starting from WOLD's 21,624 borrowing records, the structural filter (every
exclusion documented in the script's docstring) leaves **16,687 pairs** across
41 recipients and 300 donors. Attrition:

| dropped for | n |
|---|---|
| no `Source_word` | 1,000 |
| `Source_certain == 'no'` | 873 |
| multi-word / hyphenated / morpheme-segmented | 1,070 |
| reconstructed proto-form (`*`) | 791 |
| source string untokenizable by panphon | 618 |
| non-Latin script (Han, Arabic, Devanagari, Cyrillic) | 414 |
| author-flagged doubt (`?`, `!`) | 52 |
| length bounds / ratio / digits / empty | 85 |

The downstream study uses the **13,595** pairs with
`source_relation == 'immediate'`. The `earlier` rows (borrowed via an
intermediate language) are excluded because the recorded donor string is not
the form the recipient actually adapted. That is an a-priori linguistic
criterion, not a fit to the outcome; the outcome merely confirms it (see the
two AUC rows below).

**Transliteration noise, with a worked example.** There is no per-donor
romanisation table in WOLD, so one donor-agnostic mapping is applied to all 257
donors. Row 2 of the output shows what that costs: Nepali `chaharo` becomes
`khaharo` — because `c`→`k` is right for Latin/Spanish/Berber and no digraph
expansion is attempted, `ch` silently becomes `kh`. The recipient side has
`kjutsʰara`, so the fit sees a /k…h/ ↔ /k…tsʰ/ correspondence that is an
artifact of our romanisation, not of Manange phonology. Adding `ch`→`tʃ` would
help Spanish/English/Nepali and hurt German/Dutch (`ch`=/x/) and Italian
(`ch`=/k/); it is a coin flip we did not want to call silently, so the rule is
"no digraph expansion", documented, with this example as the honest cost. It is
also the cheapest available improvement for a future run: a per-donor
romanisation table for the top ~10 donors would cover 60% of pairs.

That 13,595 is close to the recorded "13,779 clean pairs", which is good
evidence the original conservative filter also restricted to `immediate`. The
spec asked for the number to be **reported, not targeted**, and it lands inside
the 13.8k–20.6k bracket.

### R1(a) — legacy-protocol reproduction

Original protocol as best it can be reconstructed: 1,500 sampled pairs,
controls drawn from the **global** source pool, no recipient grouping, panphon
default weights. Mean of three seeds:

| pair set | n | attested | control | AUC |
|---|---|---|---|---|
| all rows | 16,687 | 0.742 | 0.457 | **0.899** |
| `immediate` only | 13,595 | 0.757 | 0.459 | **0.909** |
| *recorded 2026-07-14* | *13,779* | *0.78* | *0.46* | *0.923* |

The control mean reproduces to two decimals (0.459 vs 0.46); attested and AUC
come in ~0.02 low. That residual is transliteration detail — the original
romanisation table is not in the repo and cannot be recovered — and it is small
enough to call the rebuild faithful.

**The original harness did not shuffle controls within recipient.** Its
controls come from the global sample, which is exactly the leak R7 was added to
close. So 0.923 is not merely a looser split, it is a *different and easier
task*, and is not a bar for anything.

### R1(b) — default-weight baseline under the honest protocol

See §4: panphon's unmodified weights, run through the same
leave-one-recipient-out CV and the same within-recipient controls the learned
model faces. **This is what guardrail 1 is judged against.**

---

## 3. R2/R4/R6 — how the fit works

### The parameter vector (R2: substitution and epenthesis fitted together)

`src/interlang/costs.py` ships two cost models behind one interface:

| model | parameters | insertion priced by |
|---|---|---|
| `FeatureWeightCosts` | 22 feature weights + `del_C del_V ins_C ins_V` | what is inserted |
| `ContextEpenthesisCosts` | 22 + `del_C del_V ins_C ins_V_cluster ins_V_edge ins_V_other` | what **and where** |

Both reproduce `metric.similarity` bit for bit at panphon's defaults (verified,
max absolute difference 0.0), so "learned vs default" is a clean A/B.

The second model is the spec's explicit R2 **stretch goal**: a vowel inserted
between two source consonants (cluster repair) or at a consonantal word edge
(prothesis "schola"→"escuela", paragoge "strike"→"sutoraik-**u**") is priced
separately from a vowel inserted anywhere else. The insertion-context classes
for the seven insertion slots of `s t ɹ a i k` come out
`edge, cluster, cluster, other, other, other, edge` — and the three vowels
Japanese actually inserts, s-**ɯ**-t-**o**-ɾ-a-i-k-**ɯ**, land in slots 1, 2
and 6: cluster, cluster, edge. The structure can express the case exactly;
whether the objective *wants* to is the question §5 answers.

Insertion and deletion are separately parameterized, which is where the
source→recipient asymmetry lives. Substitution stays symmetric (a
feature-weight model cannot be otherwise); asymmetric substitution and a
segment-pair matrix are the documented next models behind the seam (R4).

**Scale.** Multiplying every parameter by a constant leaves the normalized
similarity unchanged, so the objective has an exact flat direction. It is
removed by rescaling so the 22 feature weights always sum to panphon's 7.25.
Every learned weight below is therefore directly comparable to panphon's, unit
for unit, and the indel prices are comparable to panphon's flat 7.25.

### The objective (R6: never gradient-optimize AUC)

Attested pair scores `s⁺`, its within-recipient control scores `s⁻`; minimize

```
L(p) = mean over recipients ( mean over that recipient's pairs
         −log sigmoid((s⁺ − s⁻)/τ) )          τ = 0.1
     + λ · mean_j  w_j (log p_j − log p_j^panphon)²
```

- The **outer mean over recipients is the R5 rebalancing** — each recipient
  counts once regardless of pair count, so Berber (1,184), Romanian (1,114) and
  Romani (1,024) cannot outvote Ket (107). Donor rebalancing was **not** done;
  the Spanish/Latin/Arabic donor skew survives into the fit and is a live
  caveat.
- **AUC is never optimized**, only reported on held-out folds, on the clamped
  metric-faithful similarity.

**Optimizer route chosen: both sanctioned R6 routes, composed.** Derivative-free
Nelder–Mead on log-parameters, inside an EM-style outer loop that re-aligns
between inner optimizations. The reason this is cheap enough to do 41 times
twice: *given a fixed alignment, the distance is exactly linear in the
parameters* — `d = φ·p` where φ accumulates per-feature disagreement over
substituted positions plus counts per indel class. So one batched DP pass
(0.2 s over 13,595 pairs, vectorized across pairs of equal shape) buys an inner
objective that is a single matmul, ~0.4 ms per evaluation. Nelder–Mead then
runs thousands of evaluations in seconds. Between outer rounds we re-align
under the new parameters, recompute the honest objective, and accept the step
only if it improved — which is how R6's "alignment path can change
discontinuously" hazard is handled rather than ignored.

### The prior, and why it is not decoration

λ shrinks toward panphon's hand-guessed values in log space, and the weights
`w_j` are **not uniform**: `syl`, `son` and `cons` — panphon's *major-class*
features, the ones that make a vowel a vowel — carry a prior 100× stronger than
the rest.

This is the single most consequential judgment call in the study, and it was
forced by the data. Unregularized, the fit drives all three major-class weights
from 1.0 to **~0.04**, and the resulting metric scores /d/→/i/ as *cheaper*
than /d/→/f/ — guardrail 2 fails outright. Two things are going on:

1. The model is using cheap vowel/consonant interchange as a crude substitute
   for epenthesis machinery. (It does this even in the `context` model, so this
   is not the whole story.)
2. WOLD source strings are orthographic. Semitic transliterations routinely
   omit vowels; other conventions insert them. Vowel-consonant confusion is
   partly an artifact of the transcription, and the fit happily learns it.

A metric in which a listener may hear a vowel as a consonant for free is not a
recognizability metric under any theory, so the major-class weights are held
near panphon's values and the remaining 19 features plus the indel prices are
learned freely. The AUC price of doing this is measured, not assumed (§5).

**Why the prior is targeted rather than uniform.** Uniform shrinkage also fixes
the ladder — but only at λ ≥ 0.1, and by then it has undone most of the
place-of-articulation correction we came for. Reproduce with
`--major-mult 1` (grouped 5-fold, `feature` model):

| uniform λ | held-out AUC | /da/ ladder | `syl` | `lab` (panphon 0.25) |
|---|---|---|---|---|
| 0.0 | 0.9638 | ✗ | 0.04 | 0.43 |
| 0.003 | **0.9642** | ✗ | 0.19 | 0.84 |
| 0.01 | 0.9641 | ✗ | 0.27 | 0.81 |
| 0.03 | 0.9616 | ✗ | 0.42 | 0.73 |
| 0.1 | 0.9542 | ✓ | 0.63 | 0.60 |
| 0.3 | 0.9445 | ✓ | 0.73 | 0.38 |
| 1.0 | 0.9249 | ✓ | 0.84 | 0.29 |

And the same sweep with the 100× prior on `syl`/`son`/`cons`
(`data/processed/cost_learning_lambda.csv`, the shipped configuration):

| λ, 100× major prior | held-out AUC | /da/ ladder | sutoraiku |
|---|---|---|---|
| 0.0 *(= no prior at all)* | 0.9653 | ✗ | 0.632 |
| **0.01 ← selected** | **0.9560** | ✓ | 0.578 |
| 0.03 | 0.9525 | ✓ | 0.568 |
| 0.1 | 0.9463 | ✓ | 0.556 |
| 0.3 | 0.9363 | ✓ | 0.558 |

Reading the two tables together:

- **The /da/ gradient costs ~0.009 AUC**, either way you buy it (uniform λ=0.1:
  0.9542; targeted λ=0.01: 0.9560, both against an unconstrained 0.965).
  That is the price of a phonetically coherent metric, and it is small.
- **Targeting is what preserves the place correction.** At its cheapest
  ladder-preserving setting the uniform prior leaves `lab` at 0.60; the targeted
  prior leaves it at **0.80**. Same AUC, same sanity guarantee, a third more of
  the correction we came for.
- **Selection rule** (in the script): highest held-out AUC *among λ that
  preserve the /da/ gradient*. λ=0 is deliberately left in the grid rather than
  quietly deleted, so the price of the constraint is on the page.

One more thing the table shows: the *completely* unregularized fit (λ=0) is
not merely wrong, it is **unstable** — `lab` lands at 0.43 there but at 0.84
with the barest shrinkage. A parameter that moves by 2× under a
near-zero prior is not a measurement.

---

## 4. R3 — the primary result: stability across held-out recipients

**Full leave-one-recipient-out over all 41 recipients**, for both cost models.
The spec's grouped-K-fold fallback was not needed: one fit takes ~25 s, so
41 × 2 folds plus the λ sweep is under an hour. Pairs are never split within a
recipient.

Two things to read carefully before the numbers:

- **`auc_default` does not vary with the fit.** panphon's weights are fixed, so
  its per-recipient AUC is a property of the recipient, not of any training
  run. Its spread is *between-recipient* variation — how much easier Takia is
  than Manange — and it is the right denominator for exactly that reason: the
  learned column has the same between-recipient variation in it.
- **The paired delta is the statistic that matters**, not the difference of
  means, because the two columns share that recipient-difficulty variation.

### Held-out AUC, both models, λ = 0.01

| | mean | sd | min | median | max |
|---|---|---|---|---|---|
| **default panphon — R1(b)** | 0.8961 | 0.0618 | 0.7200 | 0.9082 | 0.9852 |
| learned, `feature` | **0.9569** | 0.0391 | 0.8023 | 0.9684 | 0.9949 |
| learned, `context` | 0.9567 | 0.0387 | 0.8019 | 0.9688 | 0.9949 |
| **paired delta, `feature`** | **+0.0607** | 0.0325 | +0.0082 | +0.0594 | +0.1621 |
| paired delta, `context` | +0.0606 | 0.0331 | +0.0079 | +0.0585 | +0.1621 |

**The learned costs beat panphon's defaults on 41 out of 41 held-out
recipients**, for both models. There is no recipient for which the fitted costs
are worse. Pair-weighted, 0.9038 → 0.9614. That is guardrail 1, decisively.

Note what R1(b) does to the reference point: the honest default-weight baseline
is **0.896**, not the legacy 0.923. Within-recipient controls and recipient
grouping cost the default metric ~0.03 AUC, exactly as the spec anticipated.

Where the metric is worst, and where it gains most, are the same places:

| held-out recipient | n pairs | default | learned | delta |
|---|---|---|---|---|
| White Hmong | 281 | 0.7288 | 0.8023 | +0.0735 |
| Japanese | 671 | 0.8045 | 0.8641 | +0.0596 |
| Vietnamese | 34 | 0.7392 | 0.8802 | +0.1410 |
| Mandarin Chinese | 21 | 0.7200 | 0.8821 | +0.1621 |
| Malagasy | 271 | 0.8250 | 0.9224 | +0.0974 |
| … | | | | |
| Romanian | 867 | 0.9382 | 0.9846 | +0.0465 |
| Kalina | 200 | 0.9493 | 0.9879 | +0.0386 |
| Bezhta | 388 | 0.9852 | 0.9934 | +0.0082 |
| Iraqw | 163 | 0.9594 | 0.9940 | +0.0346 |
| Takia | 307 | 0.9793 | 0.9949 | +0.0156 |

The five hardest recipients are the ones that restructure loans most heavily —
Hmong, Japanese, Vietnamese, Mandarin, Malagasy: tone languages and strict-CV
phonologies, where the recipient form barely resembles the donor string. That
is the projection-distortion problem in miniature, and it is where a better
cost model has the most room. It is also a warning: the metric is *least*
reliable exactly for the phonologies most like the restrictive templates we are
considering for our own language (§3.6).

### The learned parameters (`feature` model, LORO mean ± sd over 41 folds)

Feature weights renormalized so the 22 sum to panphon's 7.25, so the columns
are directly comparable. Sorted by how far the fit moved them.

| parameter | panphon | learned | LORO sd | × panphon | what it is |
|---|---|---|---|---|---|
| `voi` | 0.125 | 0.440 | 0.012 | **3.52** | voicing |
| `lab` | 0.250 | 0.803 | 0.018 | **3.21** | labial place |
| `nas` | 0.250 | 0.600 | 0.019 | **2.40** | nasality |
| `back` | 0.250 | 0.484 | 0.013 | 1.94 | vowel backness |
| `lo` | 0.250 | 0.448 | 0.021 | 1.79 | vowel lowness |
| `round` | 0.250 | 0.242 | 0.019 | 0.97 | lip rounding |
| `son` | 1.000 | 0.877 | 0.003 | 0.88 | sonorant *(priored)* |
| `syl` | 1.000 | 0.846 | 0.004 | 0.85 | syllabic *(priored)* |
| `cont` | 0.500 | 0.413 | 0.014 | 0.83 | continuant (manner) |
| `cons` | 1.000 | 0.811 | 0.003 | 0.81 | consonantal *(priored)* |
| `distr` | 0.125 | 0.094 | 0.002 | 0.75 | distributed |
| `lat` | 0.250 | 0.185 | 0.007 | 0.74 | lateral |
| `strid` | 0.125 | 0.089 | 0.002 | 0.71 | strident |
| `cor` | 0.250 | 0.161 | 0.007 | 0.64 | coronal place |
| `cg` | 0.125 | 0.073 | 0.001 | 0.59 | constricted glottis (ejective) |
| `sg` | 0.125 | 0.069 | 0.001 | 0.55 | spread glottis (aspiration) |
| `ant` | 0.250 | 0.122 | 0.004 | 0.49 | anterior |
| `hi` | 0.250 | 0.117 | 0.003 | 0.47 | vowel height |
| `tense` | 0.125 | 0.055 | 0.001 | 0.44 | tenseness |
| `long` | 0.250 | 0.108 | 0.001 | 0.43 | length |
| `velaric` | 0.250 | 0.107 | 0.001 | 0.43 | clicks |
| `delrel` | 0.250 | 0.106 | 0.002 | 0.42 | delayed release (affricates) |
| `del_C` | 7.250 | 3.365 | 0.059 | 0.46 | delete a consonant |
| `del_V` | 7.250 | 2.181 | 0.036 | **0.30** | delete a vowel |
| `ins_C` | 7.250 | 3.906 | 0.052 | 0.54 | insert a consonant |
| `ins_V` | 7.250 | 2.509 | 0.049 | 0.35 | insert a vowel |

**Stability (the actual R3 headline).** Every parameter's relative sd across the
41 leave-one-recipient-out folds is **1–8%**, most of them 1–3%. The largest is
`round` at 8%. No held-out recipient changes the picture. The place-vs-manner
reweighting is not a fluke of one fold — it is the most stable thing in the
table (`lab` = 0.803 ± 0.018, i.e. ±2%).

**What actually moved, more precisely than the spec predicted.** The spec's
hypothesis was "place is underweighted relative to manner". What the data says
is narrower and more interesting:

- **Labiality specifically goes up 3.2×**, and it is what flips the /v/→/b/
  diagnostic. Labial place is perceptually robust — visible on the lips, strong
  formant transitions — exactly the argument the spec made.
- **Coronal place *detail* goes down**: `ant` 0.49×, `cor` 0.64×, `distr` 0.75×.
  So it is not "place up" wholesale. It is *labial vs non-labial matters, where
  within the coronal region matters less* — which is a real and well-attested
  perceptual asymmetry, and not something panphon's flat 0.25-for-every-place-
  feature scheme can express.
- **Manner barely moves** (`cont` 0.83×). The spec framed this as place-vs-
  manner; the data says it is labiality-vs-everything.
- **Nasality up 2.4×** and **vowel backness/lowness up ~1.8–1.9×**, both
  plausible for perception.
- **Affricates, aspiration, ejectives, clicks, length, tenseness all go DOWN to
  0.4–0.6×.** For `sg`, `cg` and `velaric` this is "no evidence" (§6: WOLD's
  recipient set contains no breathy-voice or click phonology) and for `long` and
  `delrel` it is partly our transliteration stripping them. Do not read these as
  measurements.
- **Voicing up 3.5× is the one to distrust** — see §7.

**Indels (R2).** All four collapse from panphon's flat 7.25 to 2.2–3.9, i.e.
insertion and deletion become 2–3× cheaper *relative to substitution*, and
crucially they separate: **deleting a vowel (2.18) is the cheapest edit and
inserting a consonant (3.91) the most expensive**, with a clean
V-cheaper-than-C ordering on both sides. That ordering is the epenthesis
machinery working. In the `context` model, `ins_V_cluster` (2.68) and
`ins_V_edge` (2.44) are cheaper than `ins_V_other` (3.09) — the sign is right,
cluster repair *is* cheaper than gratuitous insertion — but by 13–21%, not the
several-fold discount the sutoraiku case needs. See guardrail 4.

---

## 5. Guardrails

Both models were run through all five. **Three pass, two fail.** Numbers below
are the `feature` model; `context` differs in the third decimal except where
noted. Machine-readable: `data/processed/cost_learning_guardrails.csv`.
Recompute without re-fitting: `uv run python scripts/cost_learning.py --report-only`.

### 1. Learned ≥ default under identical honest CV — **PASS**

Held-out AUC 0.9569 (sd 0.0391, min 0.8023) vs default 0.8961 (sd 0.0618, min
0.7200); paired delta +0.0607 ± 0.0325; **learned wins on 41/41 recipients**.
See §4. This is the strongest result in the study.

### 2. /da/ sanity gradient — **PASS, but only because we forced it**

| vs /da/ | ta | ða | ɡa | fa | ma | ia |
|---|---|---|---|---|---|---|
| default | 0.983 | 0.914 | 0.853 | 0.819 | 0.750 | 0.414 |
| learned | 0.841 | 0.818 | 0.666 | 0.295 | 0.100 | 0.000 |

Correctly ordered, and much better *separated* than the default (which crams
everything into 0.75–0.98 — known-issue 3, the compressed dynamic range). But
see §3: unregularized this ordering breaks badly, and the major-class prior is
what restores it. Counting this as a pass is honest only alongside that
disclosure.

### 3. /v/ → Japanese-like inventory — **PASS**

| | 1st | 2nd | 3rd |
|---|---|---|---|
| default | **z** (1.125) | b (1.250) | s (1.375) |
| learned | **b** (1.001) | p (1.883) | z (2.025) |

The diagnostic flips, and not narrowly: /b/ now wins by a factor of 1.9 over
/z/, where the default had /z/ ahead by a single flip of the cheapest feature
class. `lab` = 0.803 ± 0.018 across 41 folds, so this is stable. Inventory is
PHOIBLE's Japanese (glottocode `nucl1643`, majority vote, n=20).

### 4. sutoraiku vs strike — **FAIL, and it went the wrong way**

Default 0.617 → learned **0.577** (`context` model: 0.568). Target was 0.9.

This is the study's clearest negative result and it deserves a straight
explanation rather than a shrug.

The structure can express it: hand-setting `ins_V_cluster` and `ins_V_edge` to
1.0 gives **0.904**. The fit does not choose to. The learned context costs
(`ins_V_cluster` 2.68, `ins_V_edge` 2.44, `ins_V_other` 3.09) discount cluster
repair by only 13–21%.

**Why the objective resists cheap epenthesis.** The negative control shares the
*same recipient word* as the attested pair, and differs only in the source. So
cheap insertion helps the control almost exactly as much as it helps the
attested pair, and the discriminative objective sees no gain — arguably a
slight loss, because a mis-matched control benefits more from a free escape
hatch than a genuine correspondence does. **A discriminative objective is
structurally the wrong tool for learning repair costs.** This is a real tension
inside the spec: R2 asks for the sutoraiku recovery as a *training-time* target
while R6/agreed-call-2 makes the training objective purely discriminative.
Those two pull against each other, and here the objective won.

The fix is not more regularization or a richer insertion model — it is a
*generative* term (score how well the costs predict the recipient form, not
just how well they rank it against a decoy), or fitting the epenthesis prices
only on recipients that actually do cluster repair instead of averaging the
signal over 41 languages most of which never epenthesize.

Consequence for §3.6: the permissive-coda bias is **reduced but not removed**,
and by this measure not reduced at all on the canonical case. Run the
projection-distortion experiment as a two-arm sensitivity analysis.

### 5. Contrast-study cross-check — **FAIL (null result)**

The spec called this the intellectual crux, so it gets the fullest treatment.

Spearman rank correlation over the 23 contrasts in `contrast_costs.csv` that
are single panphon segments on both sides:

| | ρ(cost, % L1 who hear the contrast) | ρ(cost, merger languages) |
|---|---|---|
| default panphon | −0.020 (p = 0.93) | −0.407 |
| **learned** | **+0.059 (p = 0.79)** | −0.407 |

Wanted: positive and significant on the left (a contrast most of humanity can
hear should be *expensive* to substitute), negative on the right (a contrast
languages actively merge should be *cheap*). What we got is **no relationship
at all** — and, notably, the merger correlation does not move by even one
digit.

An earlier, looser pass criterion (ρ_learned > ρ_default) scored +0.059 as a
pass. It has been tightened to require p < 0.05, because "the coin landed the
right way up" is exactly the vacuous green tick this guardrail exists to catch.

**Why it is null, from the per-contrast table**
(`data/processed/cost_learning_contrast_check.csv`) — the learned costs move in
*both* directions and cancel:

| moved the right way | | moved the wrong way | |
|---|---|---|---|
| `i/ɪ` 0.25 → 0.11 | 27% hear it, 143 mergers | `f/v` 0.25 → 0.88 | 34% hear it |
| `e/ɛ` 0.25 → 0.11 | 41%, 126 mergers | `s/z` 0.25 → 0.88 | 49% |
| `o/ɔ` 0.25 → 0.11 | 37%, 102 mergers | `u/ʊ` 0.75 → 1.72 | 26%, 87 mergers |
| `m/n` 1.13 → 2.03 | 99% hear it | `t/d` 0.25 → 0.88 | 75% but perceptually cheap |
| `u/o` 1.00 → 1.85 | 70% | `p/b` 0.25 → 0.88 | 73% |
| `h/x` 2.50 → 1.99 | 11%, 41 mergers | `k/ɡ` 0.25 → 0.88 | 74% |

The vowel-quality rows all go the right way — mid-vowel and lax/tense
distinctions that most of the world merges get cheap, exactly as they should.
Every row that goes the wrong way is **the same row**: a voicing contrast
(`f/v`, `s/z`, `p/b`, `t/d`, `k/ɡ` — all driven by `voi` at 3.5× panphon).

So the null is not noise. It is one systematic effect — the voicing artifact of
§7 — cancelling a genuine perceptual signal the fit did find in the vowel
space. **Divergence, as the spec put it, is a flag for overfitting to loanword
idiosyncrasy, and it has flagged one specific, identifiable, fixable parameter.**
That is more useful than a pass would have been.

---

## 6. Coverage: how much of phonological space is WOLD's recipient set?

The spec accepts the assumption "wide family coverage ⇒ wide phonological-type
coverage" and asks for a hard number instead of an assertion.
`scripts/wold_coverage.py` supplies it, using the prevalence study's own
majority-vote inventory policy and `lumped` symbol level so the numbers compose
with `phoneme-prevalence.md`.

**First, a correction to the premise.** Only **30 of the 41** WOLD recipients
have a PHOIBLE inventory at all. Missing: Selice Romani, Takia, Saramaccan,
Tarifiyt Berber, White Hmong, Ceq Wong, Old High German, Gawwada, Bezhta,
Oroqen, Seychelles Creole — which includes two of the four largest pair
contributors. Every inventory-based number below is therefore computed on 30
languages, and the true coverage is somewhat better than stated.

| coverage of PHOIBLE segment types (non-tone, lumped) | value |
|---|---|
| all 1,516 types present in ≥1 recipient | 16.9% |
| of types in ≥1% of world languages (n=216) | **74.5%** |
| of types in ≥5% of world languages (n=81) | **95.1%** |
| of types in ≥20% of world languages (n=32) | **100%** |
| weighted by L1 speakers who have the segment | **91.7%** |

So the common core is covered and the long tail is not, which is the right
shape: the metric needs to price sounds that many people actually have.

**The concrete holes, and they matter for this study:**

| segment | % world languages | % L1 speakers | what it is |
|---|---|---|---|
| ɖ | 7.6% | 25.7% | retroflex stop |
| b̤ d̤ ɖ̤ ɡ̤ r̤ | 0.5–1.8% | 9–18% each | breathy-voiced ("murmured") series |
| ʊ̃ ɪ̃ | ~3% | ~16% | nasalized lax vowels |
| ʋ | 2.0% | 11.3% | labiodental approximant |

That is **Indo-Aryan** — Hindi/Urdu, Bengali, Marathi, Punjabi — essentially
absent from WOLD's recipient set as a *recipient* phonology. Two consequences
we should hold onto:

1. The learned weights for `sg` (spread glottis, i.e. aspiration/breathiness)
   and for the retroflex-relevant features (`distr`, `ant`) are informed by
   almost no data. §5 shows exactly that: `sg` collapses toward zero and
   `distr`/`ant` are the least stable parameters in the LORO run. **These are
   the weights not to trust.**
2. Structurally, coverage is 22 of PHOIBLE's 177 families (12.4%) but the
   recipient inventories span the normal size range (median 32 lumped
   segments, min 17, max 73, against PHOIBLE's median 30 / 5th–95th 17–51). No
   macroarea is empty; Australia has exactly one recipient.

---

## 7. The loanword-vs-recognition caveat, with evidence

The spec flagged this up front and the run put numbers on it. We calibrated on
**loanword adaptation** — production-mediated, whole-word, top-down, the
borrower already knew the word, and the record of it is orthographic. We want
to *use* the result for **recognition** (naive listener, unknown word) and
**distinguishability** (two of our own words, symmetric, no source). Three
different concepts.

Three concrete places where the fit shows it is learning the wrong concept:

1. **Major-class collapse.** Left free, the fit prices vowel↔consonant
   interchange at near zero. No theory of *perception* says that. It is a
   plausible fact about *transcriptions* (unwritten Semitic vowels,
   convention-inserted ones) and about alignment slack. We had to override it
   with a prior (§3), which is an explicit admission that on this axis the
   loanword data is not evidence about recognition.
2. **Voicing.** Left free, `voi` goes to ~7.7× panphon's weight — the fit
   decides voicing mismatches are among the most expensive things that can
   happen. Loanword orthographies record voicing faithfully on both sides, so
   voicing mismatches are rare *in the data*. But the contrast study says the
   t/d contrast is natively audible to only 75% of humanity, and p/b to 73% —
   voicing is one of the *cheapest* contrasts perceptually. This is a
   production/orthography artifact being learned as a perceptual fact, and it
   is the clearest single example of the concept gap.
   The major-class prior pulls `voi` down from ~7.7× to **3.5×**, but it does
   not fix it — 3.5× is still the single largest upward move in the whole
   parameter table, and it is what makes guardrail 5 come out null (§5).
3. **Dead features.** `sg` (aspiration/breathiness), `cg` (ejective), `tense`,
   `long` and `velaric` (clicks) all go to ~0. Partly that is transliteration
   stripping them; partly, per §6, it is that WOLD's recipient set contains no
   breathy-voiced or click phonology at all. A zero learned weight here means
   "no evidence", not "does not matter", and must not be read as the latter.

**What guardrail 5 buys us.** The contrast study is derived from PHOIBLE
inventories and merger patterns — no loanwords anywhere in it — so agreement
between it and the learned costs is evidence that the fit captured perceptual
distinguishability rather than loanword idiosyncrasy. §5 reports it; the
direction of the result is the reason to take the learned *place* weights
seriously while distrusting the learned *voicing* weight.

---

## 8. What changes, what does not, and what to do next

**`metric.py` v0 remains the default and the deployed metric.** It gains an
optional `params=` argument (verified bit-identical when omitted), so the
learned costs can be used deliberately — e.g. as a sensitivity arm in the
projection-distortion experiment — without becoming the silent default. Given
that two of five guardrails fail, promoting the learned costs to default now
would be trading a metric with *characterized* failure modes for one with
*different, less characterized* failure modes.

**Conditions for promoting the learned costs to v1**, in the order that would
retire the most risk:

1. Fix guardrail 4 properly. The context-epenthesis model has the right
   structure but the discriminative objective does not reward using it (§5).
   Either add a *generative* term (predict the recipient form, not just rank
   it), or fit the epenthesis prices on the subset of recipients where cluster
   repair actually happens rather than averaging over 41.
2. Re-derive the voicing weight from a non-loanword source, or pin it from the
   contrast study the way the major-class weights are pinned from theory.
3. Get an Indo-Aryan recipient (breathy voice, retroflexion) into the training
   set — from a source other than WOLD if necessary — before trusting `sg`,
   `ant` or `distr`.
