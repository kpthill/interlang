# Interlang: principles, decisions, and findings

*Last updated 2026-07-14. Companion documents: [`data-audit.md`](data-audit.md) (dataset details, metric validation), [`../src/interlang/metric.py`](../src/interlang/metric.py) (recognizability metric v0).*

Each decision below is tagged:

- **FIRM** — committed; revisit only with strong new evidence.
- **SOFT** — current working position; expected to survive but pending data.
- **OPEN** — genuinely undecided; an experiment or discussion is planned.

---

## 1. Project goal

Design an easy-to-learn, globally unbiased international auxiliary language (IAL) by writing down explicit principles as optimization targets, then letting a program optimize the vocabulary — and inform the phonology choices — against databases covering approximately all of the world's languages.

The improvement over Esperanto is not "zero bias" (impossible) but bias that is **chosen, explicit, and measured** rather than unexamined. Esperanto's word stock and sound system are overwhelmingly European; we want every such tradeoff to be a deliberate, quantified decision.

**Honest expectation-setting:** the world's language families share almost nothing lexically. Absolute recognizability scores will be low for everyone. The real output of this project is a **measured tradeoff curve** — how much ease-of-learning you buy at what cost in representational fairness — not a language that magically feels familiar to all 8 billion people.

---

## 2. Guiding principles

### Two parallel objectives (FIRM)

1. **Ease of learning**, for as many people as possible. Weighted by **L2/total speaker counts** — "how many people are likely to recognize this word?" Counting second-language speakers pushes toward lingua-franca (English etc.) word stock, and that is intentional: an L2 English speaker really does know English words.
2. **Representation** — everyone should recognize *some* words as their own. Weighted by **L1 (native) speaker counts only**, so that big lingua francas don't double-dip.

### Loss shape (SOFT)

Proposed loss: an **absolute-error term** for ease (1) plus a **mean-squared-error term** for representation (2). The squared term makes the worst-represented groups dominate its gradient. Intuition: *use the most common words, but where there is no universal answer, make sure everyone is represented at least a little.*

### Representation as attribution, not similarity (OPEN)

Refinement under consideration: operationalize the representation term as **etymology attribution share** — what fraction of the lexicon traces to your language/family — rather than string similarity. Similarity-based representation saturates near zero for speakers of small languages no matter what we do, so it provides almost no gradient exactly where fairness matters most. Attribution share stays meaningful ("3% of the lexicon is sourced from your family") even when phonetic recognizability is negligible.

### Process (FIRM)

- Small, session-sized iterative milestones.
- Patrick stays in the loop in chat and reacts to intermediate results before anything is committed.
- Discoveries and decisions get documented (this file, `data-audit.md`).

---

## 3. Design decisions so far

### 3.1 Sequencing: phonology first, but vocab-aware (FIRM)

Order of work: **phonology & phonotactics → vocabulary**, with grammar hand-designed in parallel.

- *Phonology* = the language's sound system: its inventory of **phonemes** (the contrastive sound units of a language — categories that can distinguish one word from another, like English /p/ vs /b/).
- *Phonotactics* = the rules for how phonemes may combine into syllables and words (e.g., English allows "str-" at a syllable start; Japanese doesn't).

Vocabulary can't be optimized before the sound system exists, because every source word must be *projected into* our phonology. But phonology can't be chosen blind to vocabulary either: candidate phonologies are scored partly by a **projection distortion** term — how much recognizability source words retain after being squeezed into that phonology. A too-restrictive phonology (e.g., toki pona's strict consonant-vowel syllables) mangles every source word so badly that the later vocabulary optimization becomes moot.

### 3.2 Grammar: hand-designed from typology, not optimized (FIRM)

Grammar mostly can't be optimized from dictionaries — there is no database of "grammatical recognizability." Instead it will be hand-designed from typological principles, with a data citation for each decision, using cross-language majority evidence from **WALS** and **Grambank** (databases of structural features across thousands of languages) and convergence evidence from creoles (contact languages that emerge when adults must learn fast — a natural experiment in learnability). The expected shape:

- **Isolating morphology** — words don't inflect; grammatical information comes from separate particles and word order (like Mandarin), rather than from endings (like Latin).
- No grammatical gender, no case, no agreement.
- Particles for tense/aspect.
- Transparent, regular derivation of new words.

Grammar's main coupling to phonology: an isolating language needs a stock of **short, mutually distinct particles**, which argues for reserving short-word space in the phonotactics/lexicon design.

### 3.3 Phoneme inventory (SOFT — now data-backed by two studies)

- Roughly **/m n p t k s l w j h/ + /a e i o u/**, ~15–20 phonemes: segments that are cross-linguistically common *and* mutually distinct. (Notation: symbols between slashes are **IPA** — the International Phonetic Alphabet, the standard one-symbol-per-sound notation; /j/ is the "y" sound of *yes*.)
- **Penalize contrasts, not just rare sounds.** A sound can be common while a *distinction* is deadly: /r/ vs /l/ is a single category for Japanese and Korean speakers; Mandarin has no voicing contrast in stops (it uses aspiration — a puff of air — instead, so /b/ vs /p/ as *voicing* is hard). The inventory cost function should charge for contrasts that major populations can't hear.
- **Empirical status** (see [`phoneme-prevalence.md`](phoneme-prevalence.md) and [`contrast-study.md`](contrast-study.md)): the core **m n p t k s j w r + a i u** is native for ~89–99.9% of humanity per segment; **h** is weakest (55%) but wide-h over [x χ ħ] recovers 83.5%; mid vowels must be wide (E={e,ɛ}, O={o,ɔ}), giving vowel contrasts 80–83% audibility. Priced add-ons: a fortis/lenis second stop series (93–96% audible as voicing-OR-aspiration, vs 73–75% for strictly voiced — but only ~61% of *languages* have any second series), /l/ (r/l audible to 82–85%), /f/ (79%), one wide CH sibilant (~62% vs /s/). Ruled out as phonemes: v z ʒ dʒ θ ŋ ə ɪ ʊ y, and any e/ɛ, o/ɔ, or h/x contrast.
- **Functional-load pricing (SOFT, proposed):** contrast costs feed the lexicon optimizer as per-pair penalties, not just keep/drop gates — a kept-but-expensive contrast (r/l, f/p, s/CH) is made cheap in practice by forbidding minimal pairs that hinge on it (*lira*/*rira* never both words). The contrast-study table is exactly this penalty matrix.

### 3.4 Wide phonemes (FIRM as an approach)

Each phoneme of our language is defined as a **set of acceptable realizations**, not a single target sound. Examples:

- A fortis/lenis stop contrast (i.e., the /p t k/ vs /b d ɡ/ series) may be realized as a voicing difference *or* an aspiration difference — whichever the speaker's native system provides.
- /h/ may be pronounced [x] (the *Bach* sound).
- Any rhotic (r-like sound — trilled, tapped, or the English approximant) counts as /r/ if we have one.

Recognizability is scored against the **best** realization in the set. This is essentially designing with **allophones** on purpose — an allophone is a variant pronunciation of a phoneme that speakers treat as "the same sound" (English /t/ in *top* vs *stop*). PHOIBLE's `Allophones` column provides direct empirical data on which realization sets languages actually treat as one category.

### 3.5 Suprasegmentals (FIRM)

No tone, no contrastive vowel length, no contrastive stress. Each of these is a distinction that large populations cannot produce or hear reliably, and none is needed if the segmental inventory and phonotactics leave enough word space.

### 3.6 Syllable template (OPEN)

Notation: C = consonant, V = vowel, N = nasal consonant; parentheses mean optional. The **coda** is the consonant material at the *end* of a syllable (the /n/ in "san").

Candidates:

- **Strict CV** (every syllable = consonant + vowel): maximally pronounceable, but causes word-length blowup and destroys source words ("strike" → something like "sutoraiku").
- **(C)V(N)** — optional onset, optional nasal coda: the likely sweet spot.
- **Permissive CVC**: keeps source words intact but exports coda clusters many speakers can't handle.

To be decided empirically by the **projection-distortion experiment** (§7). Note a known metric bias here: the current metric lacks epenthesis modeling and systematically flatters permissive codas (see §4).

### 3.7 Orthography aspiration (SOFT — explicitly not committed)

Aspiration: the writing system is simply **IPA restricted to phonemes whose IPA symbols are ASCII a–z** — nearly free given the optimal inventories, since a–z natively covers p b t d k g m n f v s z h l r w j + a e i o u. Real casualties: **ʃ** (the "sh" sound), **tʃ** ("ch"), **ŋ** ("ng"). ŋ is recoverable as an allophone of /n/ (as in most languages). Considered and not committed for /tʃ/:

- "c" — near-IPA, since IPA [c] (a palatal stop) is acoustically close to tʃ;
- "tc" / "tsh" digraphs (Patrick's suggestion, on a soft principle of not using one glyph for two sounds).

The wide-phonemes approach may make much of this moot — if /s/~[ʃ] land in one wide phoneme, the problem symbols never enter the inventory.

### 3.8 L2 data sparsity accepted (FIRM)

Reliable L2 speaker counts exist for roughly the top ~30 languages. Beyond those, falling back to L2 = L1 is fine: languages outside the top ~30 have few L2 speakers by definition, so the approximation error is small.

---

## 4. The recognizability metric

**Question the metric answers:** how likely is a listener to recognize a word of our language as a word they already know? Implemented in `src/interlang/metric.py` (v0), validated in `data-audit.md`.

### Literature basis

- **Workhorse:** PanPhon (Mortensen et al. 2016) — every IPA segment maps to a vector of **articulatory features** (binary-ish dimensions describing how a sound is physically produced: voiced?, nasal?, place of articulation, …). Word distance is then a **weighted feature edit distance**: an alignment-based edit distance where substituting /d/→/t/ (one feature apart) is cheap and /d/→/f/ is expensive.
- **Empirically calibrated alternative:** Jäger's sound-class distances, learned via pointwise mutual information from cognate alignments over ASJP.
- **Efficiency layer for scale:** PWESuite (Zouhar et al. 2024) phonetic word embeddings.
- Rejected generalization: raw formant distance (formants = the resonant frequencies that characterize vowels) only works for vowels — stops and fricatives have no steady-state formants. Articulatory features are the standard generalization.

### Key refinement: listener conditioning

Recognizability is not symmetric or universal — it depends on the hearer's **native phoneme categories**. This is the central finding of the loanword-adaptation literature (English "strike" → Japanese "sutoraiku"). v0 implements it by **projecting both words onto the listener's PHOIBLE inventory** — each segment is mapped to the nearest native category in feature space — before scoring. Contrasts the listener lacks become free (verified: /l/ ~ /ɾ/ scores 1.0 under a Japanese-like inventory).

### What v0 does

1. Tokenize IPA strings into segments (normalizing ASCII lookalike glyphs like `g` → IPA `ɡ`).
2. Optionally project both words onto a listener inventory.
3. Score weighted feature edit distance, normalized to [0, 1] similarity where the normalizer is the cost of deleting the longer word entirely (1.0 = identical; 0.0 = no more similar than an arbitrary word).

### Validation results

Against attested WOLD loanword pairs vs shuffled controls (n = 1,500 sampled, noisy quasi-orthographic transcriptions on both sides): **mean 0.78 vs 0.46, AUC 0.923**. Sanity gradient vs /da/ orders as desired: ta 0.98 > ða 0.91 > ɡa 0.85 > fa 0.82 > ma 0.75 > ia 0.41.

### Known issues

*Updated 2026-08-04 by the cost-learning study ([`cost-learning.md`](cost-learning.md)); issues 1 and 2 move from "known" to "bounded".*

1. **Place of articulation underweighted** by panphon's default weights: projection maps /v/ → /z/ for a Japanese-like inventory where real loanword adaptation gives /v/ → /b/ (confirmed: default costs are /v/→/z/ 1.125, /v/→/b/ 1.250). **BOUNDED and fixable.** Learning the weights from WOLD raises the labial weight to ~3× panphon's and flips the diagnostic to /v/ → /b/, stably across held-out recipients. The learned weights are in `data/processed/learned_costs.csv` and `metric.py` accepts them via `params=`, but they are **not the default** — see issue 5.
2. **No epenthesis modeling.** **BOUNDED, partially fixed.** The cost model now has separate insertion prices for vowels and consonants (and, in the `context` variant, for cluster-repair vs other positions), fitted jointly with the substitution weights. Vowel insertion learns to be ~40% cheaper than consonant insertion, which is real movement in the right direction — but "sutoraiku" vs "strike" only reaches ~0.6, not the 0.9 the structure can express. **The bias toward permissive codas is reduced, not removed**, so the syllable-template experiment (§7.4) still needs the caveat, now with a measured size rather than an assertion.
3. **Baseline inflation:** random CV-ish pairs score ~0.46, so usable dynamic range is roughly [0.45, 1.0]. Recalibrate against that floor, e.g. `score' = max(0, (s − s_random)/(1 − s_random))`. (Unchanged.)
4. **Glyph normalization:** ASCII `g`, `:`, `'` are mapped to proper IPA in `segments()`; watch for more lookalikes when ingesting new sources. (Unchanged.)
5. **NEW — the learned costs encode loanword facts, not only perceptual ones.** Fitted freely, the WOLD data prices *voicing* mismatches at ~7× panphon's weight, while the contrast study says voicing is one of the **cheapest** contrasts perceptually (t/d natively audible to 75%, p/b to 73%). Loanword orthographies record voicing faithfully on both sides, so the fit is learning a transcription artifact. Similarly, aspiration/breathiness (`sg`), ejectivity (`cg`) and clicks (`velaric`) learn weight ≈ 0 — which means "no evidence in WOLD's recipient set", not "does not matter". This is why v0 is still the default.

---

## 5. Data landscape

All raw data in `data/raw/` (gitignored, re-fetchable); the universal join key is the **Glottocode** (Glottolog's stable per-language identifier), usually alongside ISO 639-3. Full details in `data-audit.md`.

| Dataset | Size | Role | Caveat |
|---|---|---|---|
| **PHOIBLE** | 3,020 phoneme inventories, 2,177 languages | Phoneme/contrast prevalence; listener inventories for the metric; allophone data for wide phonemes | Multiple inventories per language (~1.4 avg) — needs a selection/union policy |
| **ASJP** (lexibank) | 568,820 word forms, 11,540 doculects, 100 concepts (core 40 well covered) | Maximal-breadth word forms for projection-distortion and cross-family similarity; the fairness denominator | Only 100 concepts — fine for phonology, too few for the real lexicon. (`Segments` is already IPA-ish/CLTS-tokenized.) |
| **WOLD** (World Loanword Database) | 41 recipient languages, 21,624 borrowing records | Validation set for the metric; attested adaptation/repair evidence | Source words are raw strings in mixed orthography; 13,779 pairs survive a conservative cleaning filter |
| **Glottolog CLDF** | 27,177 languoids | Family tree + macroareas for fairness weighting and aggregation | — |
| **CLDR language populations** | 799 languages | Total-speaker weights (the L2/ease term) | Figures are **total** speakers; BCP-47 → ISO 639-3 mapping built in `scripts/phoneme_prevalence.py` (macrolanguage choices documented) |
| **Wikidata P1098 L1 counts** | 1,858 languages | Native-speaker weights (the representation term) | Ethnologue-derived via Wikidata, CC0; selection policy + phantom-MSA override in `scripts/fetch_l1_speakers.py`; languages missing from it default to 10k L1 |

Deferred to the vocabulary stage:

- **Concepticon** — the standard cross-linguistic concept list (what meanings need words).
- **CLICS** — colexification data. *Colexification*: when one word covers multiple meanings in a language (e.g., many languages use one word for "hand" and "arm"). Cross-language colexification patterns are a de-Eurocentrizing tool for deciding sense granularity — which meaning splits are universal vs European habits.
- **Lexibank / IDS / NorthEuraLex** — deeper wordlists (up to ~1,300 concepts) for actual lexicon sourcing.

*Terminology: a **doculect** is a language as documented by one particular source; a **languoid** is Glottolog's umbrella term for any node in the family tree (family, language, or dialect).*

---

## 6. Discoveries / empirical results so far

1. **The metric works at v0 quality.** AUC 0.923 separating attested loanword pairs from shuffled controls, despite noisy transcriptions on both sides. Good enough to start ranking candidate phonologies.
2. **Listener conditioning is implementable and cheap** — segment-wise nearest-native-category projection against PHOIBLE inventories behaves correctly on the classic cases (/l/~/ɾ/ free for Japanese-like listeners).
3. **The metric's failure modes are characterized**, not just suspected: place-of-articulation underweighting (/v/→/z/ instead of /v/→/b/), no epenthesis (punishes attested heavy-epenthesis adaptations, flatters permissive codas), and a ~0.46 random-pair floor. Each has a concrete fix path (§4).
4. **WOLD is usable as ground truth** for learning substitution/repair costs later: ~13,779 clean attested adaptation pairs after filtering, despite the empty `Source_Form_ID` column.
5. **ASJP requires no transcription conversion** — its `Segments` column is already CLTS-tokenized and panphon-compatible, removing an expected preprocessing step.
6. **CLDR alone can't serve both objectives.** Its figures are total-speaker counts: exactly right for the ease/L2 term, unusable for the representation/L1 term. The two-objective design forces sourcing a second population dataset.
7. **The ASCII orthography is nearly free** given the kind of inventory the prevalence data is expected to favor — the losses concentrate in ʃ/tʃ/ŋ, and ŋ is recoverable allophonically.

---

## 7. Open questions / next steps

Experiments:

1. ~~**Phoneme/contrast prevalence study**~~ **DONE** → [`phoneme-prevalence.md`](phoneme-prevalence.md); inventory findings folded into §3.3.
2. ~~**Contrast study**~~ **DONE** → [`contrast-study.md`](contrast-study.md); contrast prices and functional-load mechanism in §3.3.
3. ~~**L1 speaker-count sourcing**~~ **DONE** → Wikidata P1098 (1,858 languages, `data/processed/l1_speakers.csv`), with the phantom-MSA override (`L1_OVERRIDES` in `scripts/fetch_l1_speakers.py`; see contrast-study Addendum).
4. **Projection-distortion experiment** (NEXT) — project source vocabulary through candidate syllable templates (strict CV vs (C)V(N) vs permissive CVC) and measure retained recognizability. → Resolves §3.6. Prerequisite caution, now **bounded rather than open**: the epenthesis gap biases this experiment toward permissive codas. The learned costs (§7.5) reduce the bias but do not remove it, so run the experiment **as a two-arm sensitivity analysis** — once with `params=None` (v0) and once with the learned costs — and report the template ranking only where the two arms agree.
5. ~~**Metric calibration**~~ **DONE (2026-08-04)** → [`cost-learning.md`](cost-learning.md), spec in [`cost-learning-spec.md`](cost-learning-spec.md). Summary:
   - The WOLD pipeline is **committed** for the first time (`scripts/wold_pipeline.py`): 16,687 cleaned pairs, 13,595 used.
   - The recorded **AUC 0.923 is retired as a reference point.** It came from a protocol that shuffled negative controls from the *global* source pool, which lets a model win by detecting which donor pool a recipient draws from. Rebuilt under that same loose protocol we get 0.909; under an honest recipient-grouped protocol with within-recipient controls the default-weight baseline is the number to compare against (see `cost-learning.md` §4).
   - Substitution and insertion/deletion costs are learned **jointly** and cross-validated **leave-one-recipient-out over all 41 recipients**. The headline is a stability statement, not a point estimate.
   - **The place-of-articulation fix is real and stable**; the epenthesis fix is partial; two of five guardrails fail. **v0 remains the default metric**; the learned costs ship as `data/processed/learned_costs.csv` and are opt-in via `metric.similarity(..., params=...)`.
   - New standing worry: the loanword corpus teaches production/orthography facts (voicing) as if they were perceptual facts. §4 known-issue 5.

6. **Retire the loanword-only calibration (NEW, OPEN)** — the cost model is calibrated on adaptation but consumed for recognition and distinguishability. The contrast study is the only non-loanword anchor we have, and it is inventory-level, not word-level. Candidates for a second anchor: perceptual-confusion matrices from the L2 speech-perception literature; ASJP cognate alignments (Jäger-style PMI) as a *within-family* substitution signal that has no orthography in it.

Standing open questions:

- **Representation term formulation (OPEN):** string-similarity vs etymology attribution share (§2).
- **PHOIBLE multi-inventory policy (decided SOFT):** majority vote across a language's inventories (≥50%), chosen in the prevalence study; union and intersection rejected (judgment calls documented there).
- **Diphthong-mediated contrasts (OPEN, new):** binary "has the phoneme" checks under-credit listeners whose inventories carry a vowel quality only inside diphthongs/allophones (Mandarin 918M, Wu 81M — see contrast-study Addendum). The listener-conditioned metric handles this at the word level; decide whether inventory-level analyses need a correction, or whether all downstream decisions should use the word-level metric.
- **Second stop series (OPEN, decision ready):** 93–96% of people vs ~61% of languages — the sharpest people-vs-languages fairness split so far; needs an explicit call under the declared weighting.
- **Loss shape details (SOFT):** AE + MSE combination is a proposal, not validated.
- **/tʃ/ orthography (OPEN, possibly moot):** "c" vs digraph vs excluded by wide phonemes.

---

## Glossary

- **Allophone** — a variant pronunciation of a phoneme that native speakers treat as "the same sound" (English /t/ in *top* [aspirated] vs *stop* [not]).
- **Articulatory features** — dimensions describing how a sound is physically produced (voiced?, nasal?, tongue position, …); the basis for measuring how "close" two sounds are.
- **Coda** — consonant material at the end of a syllable (the /n/ in "san").
- **Cognate** — words in different languages descending from the same ancestral word.
- **Colexification** — one word covering multiple meanings in a language (e.g., "hand" = "arm"); cross-language patterns reveal which meaning distinctions are universal.
- **Doculect** — a language variety as documented by one specific source.
- **Epenthesis** — inserting sounds (usually vowels) to repair illegal clusters: "strike" → "sutoraiku".
- **Fortis/lenis** — the "strong" vs "weak" stop series (/p t k/ vs /b d ɡ/), realized as voicing in some languages and aspiration in others.
- **Glottocode** — Glottolog's stable identifier for a languoid; this project's universal join key.
- **IPA** — International Phonetic Alphabet: standard one-symbol-per-sound notation; /slashes/ mark phonemes, [brackets] mark actual pronunciations.
- **Isolating morphology** — grammar via separate particles and word order rather than word endings (Mandarin-style, not Latin-style).
- **L1 / L2** — native language / a language learned in addition to the native one.
- **Languoid** — Glottolog's umbrella term for any node in the language family tree (family, language, or dialect).
- **Phoneme** — a contrastive sound category of a language: swapping one phoneme for another can change one word into a different word.
- **Phonology / phonotactics** — a language's sound system / its rules for combining sounds into syllables and words.
- **Rhotic** — any r-like sound (trill, tap, English approximant, …).
- **Suprasegmentals** — properties layered over segments: tone, stress, length.
