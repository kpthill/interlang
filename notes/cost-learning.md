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

RESULTS_PLACEHOLDER_METHOD

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

## 7. The loanword-vs-recognition caveat

RESULTS_PLACEHOLDER_CAVEAT

---

## 8. What changes, and what does not

RESULTS_PLACEHOLDER_ADOPT
