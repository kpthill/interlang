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
  (`Source_word`, `Source_languoid`) in mixed orthography/transliteration
  — usable after cleaning (13,779 pairs survive a conservative filter).
- Role: validation set for the recognizability metric; later, evidence on
  which adaptations/repairs languages actually perform.

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
- **Validation vs WOLD**: attested loan pairs mean 0.78 vs random-control
  mean 0.46, **AUC 0.923** (n=1,500 sampled pairs, noisy quasi-orthographic
  transcriptions on both sides) — good separation for a v0.
- Sanity gradient (vs /da/): ta 0.98 > ða 0.91 > ɡa 0.85 > fa 0.82 >
  ma 0.75 > ia 0.41 — orders as desired (/d/→/t/ ≫ /d/→/f/).

### Known metric issues / calibration notes
1. panphon default feature weights underweight place-of-articulation:
   projection mapped /v/ → /z/ for a Japanese-like inventory where real
   loanword adaptation gives /v/ → /b/. Consider reweighting or learning
   substitution costs from WOLD adaptations (or Jäger-style PMI costs).
2. No epenthesis modeling: "sutoraiku" vs "strike" scores 0.61 — attested
   adaptations with heavy vowel epenthesis are punished; listener-side
   projection is segment-wise only. Fine for ranking, revisit if it skews
   phonotactic conclusions (it systematically favors permissive codas).
3. Baseline inflation: random CV-ish word pairs score ~0.46, so the
   usable dynamic range is roughly [0.45, 1.0]. Consider recalibrating
   (e.g. score' = max(0, (s - s_random)/(1 - s_random))).
4. ASCII `g`, `:` etc. are normalized to proper IPA in `segments()` —
   watch for more lookalike glyphs when ingesting new sources.
