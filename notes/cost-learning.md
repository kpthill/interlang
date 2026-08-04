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

## 1. What was actually built

| Piece | Where | What it is |
|---|---|---|
| WOLD pair pipeline | `scripts/wold_pipeline.py` | rebuilds the never-committed cleaning code; writes `data/processed/wold_pairs.csv` |
| Coverage audit | `scripts/wold_coverage.py` | the hard phonological-coverage number the spec asked for |
| Cost models + aligner | `src/interlang/costs.py` | the R4 swappable-cost seam and a batched aligner |
| The study | `scripts/cost_learning.py` | fit, cross-validate, guardrails |

`src/interlang/metric.py` is **unchanged** by this study; see §8 for what
adopting the learned costs would take and why it is not automatic.

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
for `s t ɹ a i k` come out `edge, cluster, cluster, other, other, other, edge`
— exactly the su-**t**o-ra-i-**ku** pattern.

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

Reading the table: the ladder and the place correction are being traded against
each other by a single knob, because that knob shrinks *everything*. Targeting
the prior at exactly the three features the data cannot inform buys the sanity
guarantee without spending the correction — see §5 for the numbers under the
100× prior.

One more thing the table shows: the *completely* unregularized fit (λ=0) is
not merely wrong, it is **unstable** — `lab` lands at 0.43 there but at 0.84
with the barest shrinkage. A parameter that moves by 2× under a
near-zero prior is not a measurement.

---

## 4. R3 — the primary result: stability across held-out recipients

RESULTS_PLACEHOLDER_R3

---

## 5. Guardrails

RESULTS_PLACEHOLDER_GUARDRAILS

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
   (With the major-class prior in place `voi` settles much lower — the two
   were competing for the same probability mass.)
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
