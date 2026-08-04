# Data audit (2026-07-14)

All datasets live in `data/raw/` (gitignored; re-fetch via shallow git clone / curl).
Everything joins on **Glottocode** (and usually ISO 639-3).

## Datasets in hand

### PHOIBLE (`data/raw/phoible/cldf/`)
- 105,459 phoneme rows · 3,020 inventories · 2,177 languages.
- `values.csv`: one row per phoneme per inventory, with **`Allophones`**
  (realization sets — direct input for "wide phonemes" with multiple
  acceptable realizations) and `Marginal` flags.
- `languages.csv` has Glottocode, ISO, macroarea, family.
- Role: phoneme/contrast prevalence study; listener inventories for the
  recognizability metric; allophonic latitude data.
- Caveat: multiple inventories per language (avg ~1.4) from different
  sources — need a policy (union? preferred source ranking?).

### ASJP (`data/raw/asjp/cldf/`)
- 568,820 forms · 11,540 doculects · 100 concepts (core 40 well covered).
- `Segments` is already tokenized IPA-ish (CLTS) — no ASJP-code conversion
  needed for panphon.
- Role: maximal-breadth word forms for projection-distortion experiments
  and cross-family similarity; the fairness denominator (it approximates
  "all the world's languages").

### WOLD (`data/raw/wold/cldf/`)
- 64,289 words · 41 recipient languages · 21,624 borrowing records.
- `Source_Form_ID` is empty; source words are strings
  (`Source_word`, `Source_languoid`) in mixed orthography/transliteration.
- **Cleaning is now committed** (`scripts/wold_pipeline.py`, 2026-08-04):
  **16,687 pairs** survive the structural filter, **13,595** of them with
  `Source_relation == 'immediate'` (the set every study uses). The old
  uncommitted "13,779" almost certainly used the same `immediate` restriction.
  Full attrition table and every judgment call: the script's docstring and
  [`cost-learning.md`](cost-learning.md) §2.
- **Known noise, unavoidable:** there is no per-donor romanisation table, so
  one donor-agnostic transliteration is applied to all 257 donors. `c→k` is
  wrong for Romanian, `j→j` is wrong for Spanish/French, `x→x` is wrong for
  Spanish/English. Donor-specific systematic mis-mappings are real and bound
  how far any single learned substitution weight should be trusted.
- **Recipient-set coverage** (`scripts/wold_coverage.py`): only 30 of the 41
  recipients have a PHOIBLE inventory. Of segments present in ≥5% of the
  world's languages, 95.1% appear in ≥1 recipient; weighted by L1 speakers,
  91.7%. The hole is **Indo-Aryan**: retroflex /ɖ/ (25.7% of L1 speakers) and
  the whole breathy-voiced series are absent from the recipient set.
- Role: validation set for the recognizability metric; source of the learned
  substitution/epenthesis costs ([`cost-learning.md`](cost-learning.md)).

### Glottolog CLDF (`data/raw/glottolog-cldf/`)
- 27,177 languoids; family tree (`Family_ID`), macroarea, ISO mapping.
- Role: family/area assignments for fairness weighting and aggregation.

### CLDR language populations (`data/raw/cldr_supplementalData.xml`)
- 799 languages × territories, ~1,631 entries.
- Top-15 sanity check passes (en 1.73B, zh 1.29B, hi 580M, es 512M …).
- **These are total-speaker (any proficiency) figures** → good for the
  L2-weighted *ease* term. A separate **L1** source is still needed for
  the *representation* term (candidates: Wikipedia native-speaker lists,
  Ethnologue-derived tables). Codes are BCP-47 → need mapping to ISO 639-3.

## Not yet pulled (known, deferred)
- **Concepticon / CLICS** — concept list + colexification; needed at the
  vocabulary stage, not for phonology.
- **Lexibank / IDS / NorthEuraLex** — deeper wordlists (hundreds–1,300
  concepts) for actual lexicon sourcing; ASJP's 100 concepts are too few
  for the real lexicon but right for phonology experiments.
- **L1 speaker counts** — see above.

## Recognizability metric v0 (`src/interlang/metric.py`)
- panphon weighted feature edit distance, normalized to [0,1] similarity
  (normalizer = cost of deleting the longer word).
- Optional listener conditioning: project both words onto the listener's
  phoneme inventory (nearest native category per segment) before scoring —
  contrasts the listener lacks become free (verified: /l/~/ɾ/ = 1.0 for a
  Japanese-like inventory).
- **Validation vs WOLD (updated 2026-08-04)**: the recorded **AUC 0.923 is
  retired**. Its controls were sampled from the *global* source pool, so a model
  could win by detecting donor pools rather than adaptation structure. Rebuilt
  under that same loose protocol the pipeline gives 0.909 (attested 0.757,
  control 0.459 — the control mean reproduces exactly). Under the honest
  protocol — leave-one-recipient-out over all 41 recipients, controls shuffled
  *within* recipient — the default-weight metric scores **0.8961 ± 0.0618**.
  That is the real baseline. See [`cost-learning.md`](cost-learning.md) §2/§4.
- Sanity gradient (vs /da/): ta 0.98 > ða 0.91 > ɡa 0.85 > fa 0.82 >
  ma 0.75 > ia 0.41 — orders as desired (/d/→/t/ ≫ /d/→/f/).

### Known metric issues / calibration notes
1. panphon default feature weights underweight place-of-articulation:
   projection maps /v/ → /z/ (cost 1.125) ahead of /v/ → /b/ (1.250) for a
   Japanese-like inventory, where real loanword adaptation gives /b/.
   **BOUNDED 2026-08-04** — costs learned from WOLD raise the labial weight to
   3.2× panphon's (0.803 ± 0.018 over 41 folds) and flip the diagnostic, /b/
   now ahead of /z/ by 1.9×. It is labiality specifically: coronal place detail
   goes *down*. Learned costs in `data/processed/learned_costs.csv`, opt-in via
   `metric.similarity(..., params=...)`; not the default (see issue 5).
2. No epenthesis modeling: "sutoraiku" vs "strike" scores 0.617.
   **BOUNDED 2026-08-04, NOT fixed.** The cost model now prices insertion and
   deletion separately by segment class and (optionally) by position, fitted
   jointly with the substitution weights: indels drop from panphon's flat 7.25
   to 2.2–3.9 and order correctly (vowel deletion cheapest at 2.18). But the
   canonical case gets *worse*, 0.617 → 0.577, because a discriminative
   objective will not buy cheap epenthesis — the negative control shares the
   recipient word, so cheap insertion helps it equally. Hand-setting the
   cluster-insertion prices gives 0.904, so the structure is right and the
   objective is wrong. **The permissive-coda bias is characterized, not
   removed**: run the syllable-template experiment as a two-arm sensitivity
   analysis (v0 costs and learned costs) and trust only agreeing conclusions.
3. Baseline inflation: random CV-ish word pairs score ~0.46, so the
   usable dynamic range is roughly [0.45, 1.0]. Consider recalibrating
   (e.g. score' = max(0, (s - s_random)/(1 - s_random))).
4. ASCII `g`, `:` etc. are normalized to proper IPA in `segments()` —
   watch for more lookalike glyphs when ingesting new sources.
5. **NEW: the learned costs encode orthography as perception.** Voicing learns
   3.5× panphon's weight (7× unregularized) because loanword orthographies
   record voicing faithfully on both sides — yet the contrast study prices
   voicing as one of the *cheapest* contrasts perceptually (t/d audible to 75%
   of humanity). This single effect makes the contrast-study cross-check come
   out null (ρ = +0.059, p = 0.79). Aspiration (`sg`), ejectivity (`cg`),
   clicks (`velaric`) and length all learn ≈ 0, which means "no evidence in
   WOLD's recipient set", not "does not matter". These are the weights not to
   trust; see [`cost-learning.md`](cost-learning.md) §7.
