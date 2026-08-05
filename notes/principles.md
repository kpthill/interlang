# Interlang: principles, decisions, and findings

*Last updated 2026-08-05 (§3.3 inventory FIRM; §3.5 stress decided; §3.6 phonotactics; §3.7 orthography). Companion documents: [`data-audit.md`](data-audit.md) (dataset details, metric validation), [`cost-learning.md`](cost-learning.md) (learned substitution/epenthesis costs), [`../src/interlang/metric.py`](../src/interlang/metric.py) (recognizability metric v0).*

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

### 3.3 Phoneme inventory (**FIRM** — decided 2026-08-05 by Patrick)

**The inventory is closed. 15 consonants + 5 vowels = 20 phonemes.**

| | |
|---|---|
| **Consonants** | **p t k b d ɡ m n f s h j w l r** |
| **Vowels** | **a e i o u** (mids are wide: E = {e, ɛ}, O = {o, ɔ}) |

Rules that come with it:

- **One stop series contrast, defined widely (fortis/lenis).** /p t k/ vs /b d ɡ/ may be
  realized as a voicing difference, an aspiration difference, or both — whichever the
  speaker's native system provides. Voiceless implies aspirated: [pʰ tʰ kʰ] and [p t k]
  are both fine for /p t k/, [b d ɡ] and unaspirated [p t k] both fine for /b d ɡ/. This
  is the §3.4 wide-phoneme mechanism doing its most important work: 93–96% of humanity
  can hear the contrast under this definition, vs 73–75% if it were strictly voicing.
- **No other consonant makes a voicing or aspiration distinction.** /f/ and /s/ have no
  voiced counterparts (so [v] and [z] are acceptable *realizations*, not separate
  phonemes); /m n l r j w/ likewise. This is what keeps the ruled-out set (v z ʒ dʒ θ)
  ruled out rather than sneaking back in as allophonic contrasts.
- **No second sibilant.** The wide CH/SH category was offered by the contrast study and
  **declined** — at 61.9% audibility against /s/ it was the weakest of the priced add-ons.
- **/r/ and /h/ are broadly defined**; exact realization sets are delegated to the build
  agent (§3.4 gives the shape: any rhotic for /r/, h~[x~χ~ħ] for /h/).
- **Two contrasts are protected by minimal-pair bans** (the §3.3 functional-load
  mechanism, now concrete):
  - **/l/ ~ /r/** — never a minimal pair. Japanese and Korean speakers hear one category
    (81.9% audible, 45 attested mergers).
  - **/h/ ~ /r/** — never a minimal pair. **New constraint (2026-08-05).** Wide /h/
    admits [x ~ χ] and wide /r/ admits uvular [ʁ ~ ʀ]; a French or German speaker's
    rhotic and a Russian or Spanish speaker's /h/ can land on nearly the same sound.
    The two wide definitions overlap at their edges, so the contrast must not carry
    lexical weight. *This is a cost of the wide-phoneme approach, not of either segment
    individually — worth noting as the first case where two wide sets collide.*
- **Segment discouragement ranking** (a preference for the lexicon optimizer where a
  choice exists, not a ban): **/r/ and /h/** strongly discouraged; **/l/** moderately;
  **/b d ɡ/** mildly. Everything else is free. Applies with extra force to particles and
  basic vocabulary. *This needs to become a numeric penalty before the optimizer runs —
  currently an ordinal ranking (§7).*

Retained context behind the decision:

- Notation: symbols between slashes are **IPA** — the International Phonetic Alphabet, the standard one-symbol-per-sound notation; /j/ is the "y" sound of *yes*.
- **Penalize contrasts, not just rare sounds.** A sound can be common while a *distinction* is deadly: /r/ vs /l/ is a single category for Japanese and Korean speakers; Mandarin has no voicing contrast in stops (it uses aspiration — a puff of air — instead, so /b/ vs /p/ as *voicing* is hard). The inventory cost function should charge for contrasts that major populations can't hear.
- **Empirical status** (see [`phoneme-prevalence.md`](phoneme-prevalence.md) and [`contrast-study.md`](contrast-study.md)): the core **m n p t k s j w r + a i u** is native for ~89–99.9% of humanity per segment; **h** is weakest (55%) but wide-h over [x χ ħ] recovers 83.5%; mid vowels must be wide (E={e,ɛ}, O={o,ɔ}), giving vowel contrasts 80–83% audibility. Priced add-ons: a fortis/lenis second stop series (93–96% audible as voicing-OR-aspiration, vs 73–75% for strictly voiced — but only ~61% of *languages* have any second series), /l/ (r/l audible to 82–85%), /f/ (79%), one wide CH sibilant (~62% vs /s/). Ruled out as phonemes: v z ʒ dʒ θ ŋ ə ɪ ʊ y, and any e/ɛ, o/ɔ, or h/x contrast.
- **Functional-load pricing (SOFT → partly FIRM):** contrast costs feed the lexicon optimizer as per-pair penalties, not just keep/drop gates — a kept-but-expensive contrast is made cheap in practice by forbidding minimal pairs that hinge on it (*lira*/*rira* never both words). The contrast-study table is exactly this penalty matrix. Two bans are now FIRM (l/r, h/r, above); **f/p** (77.2% audible) remains a SOFT candidate for low functional load rather than a hard ban.

### 3.4 Wide phonemes (FIRM as an approach)

Each phoneme of our language is defined as a **set of acceptable realizations**, not a single target sound. Examples:

- A fortis/lenis stop contrast (i.e., the /p t k/ vs /b d ɡ/ series) may be realized as a voicing difference *or* an aspiration difference — whichever the speaker's native system provides.
- /h/ may be pronounced [x] (the *Bach* sound).
- Any rhotic (r-like sound — trilled, tapped, or the English approximant) counts as /r/ if we have one.

Recognizability is scored against the **best** realization in the set. This is essentially designing with **allophones** on purpose — an allophone is a variant pronunciation of a phoneme that speakers treat as "the same sound" (English /t/ in *top* vs *stop*). PHOIBLE's `Allophones` column provides direct empirical data on which realization sets languages actually treat as one category.

### 3.5 Suprasegmentals (FIRM)

No tone, no contrastive vowel length, no contrastive stress. Each of these is a distinction that large populations cannot produce or hear reliably, and none is needed if the segmental inventory and phonotactics leave enough word space.

**Stress placement: always the first syllable** (decided 2026-08-05). Stress carries no meaning — this rule exists only to give every word a single citation pronunciation.

Why initial rather than penultimate, given the study ([`stress-prevalence.md`](stress-prevalence.md)) headlined penultimate at 50.4% of covered L1 speakers: that headline collapses weight-sensitive systems onto penult via a trochaic default. Read faithfully, penultimate is a **3.4%** rule and **initial (7.5%) is twice as common** among languages with a genuinely fixed rule. The two also **coincide on one- and two-syllable words**, so they only differ on longer forms. Initial wins on simplicity — "stress the first syllable" is the shortest statable rule, and it never moves under compounding or affixation. Chosen deliberately over the more familiar Esperanto-style penultimate.

### 3.6 Phonotactics (partly decided 2026-08-05)

Notation: C = consonant, V = vowel, N = nasal consonant; parentheses mean optional. The **coda** is the consonant material at the *end* of a syllable (the /n/ in "san"); the **onset** is the consonant material at the start.

#### Syllable template (SOFT — baseline chosen, two extensions pending a study)

**Baseline: (C)V(N)** — optional onset, optional nasal coda. Chosen over strict CV (word-length blowup) and permissive CVC (exports coda clusters many speakers can't produce).

Two extensions are live and **pending the international-vocabulary study** (§7), which prices them against the goal that internationally-shared scientific vocabulary stay near-instantly recognizable:

- **Liquid codas** — (C)V(N,l,r). Latin/Greek international vocabulary has disproportionately many /r l s k t/ codas, not nasal ones (`elektron`, `alkohol`, `molekul`).
- **Onset clusters** — Cr/Cl types (pr tr kr pl kl br dr ɡr fr fl). `proton` survives intact with them and becomes *po-ro-ton* without. **If adopted, the permitted set must be enumerated exhaustively** — no productive cluster rule.

Known metric bias affecting this decision: the metric lacks a working epenthesis model and systematically **flatters permissive codas** (§4, cost-learning guardrail 4). Syllable-count inflation must be read alongside any metric score, not instead of it.

#### Decided rules (**FIRM**, 2026-08-05)

- **No geminates within a morpheme**, but **geminates are allowed across a compound boundary** (`kan` + `nomi` → `kannomi`, revised 2026-08-05). This preserves compound transparency, which matters more than the marginal pronunciation cost: degemination would destroy the visible seam and risk collisions with real words. Possibly moot — compounding may be dropped entirely (§7).
- **Hiatus is avoided by glide insertion**, written into the spelling: `oa` → `owa`. Hiatus is **permitted as a fallback for loanwords** where neither /j/ nor /w/ is the natural glide. *Open sub-case: the exact glide-selection rule, especially after /a/. See §7.*
- **No sandhi, no alternations, no deviation from "pronounce what is written."** This is a strong constraint and it has a consequence: every repair above is **orthographic**, applied when the word is formed, not a pronunciation rule layered on top. There is never a gap between spelling and speech. (Interacts with §3.7: the ASCII orthography is one letter per phoneme, so "what is written" is unambiguous.)

#### Loanword adaptation: `<v>` → /f/ (**SOFT** — decided 2026-08-05 by Patrick)

International vocabulary is projected into the inventory by the ruleset in
[`../src/interlang/translit.py`](../src/interlang/translit.py). Its one genuinely
arbitrary segment mapping — what to do with `<v>`, which §3.3's inventory does not have —
is settled: **`<v>` → /f/** (*virus* → *firusi*, *vitamin* → *fitamin*, *television* →
*telefision*). /b/ was tied with it on recognizability (0.810 vs 0.811 over 52
international words); /w/, the earlier placeholder, is 0.015 worse. The tiebreak is
inventory-internal, not metric: /f/ keeps /w/ free to render `<w>`, and §3.3 mildly
discourages /b d ɡ/. Evidence and the full ruleset:
[`international-vocab.md`](international-vocab.md) §4.1, §6.4, §7.1.

SOFT rather than FIRM because the rest of the adaptation ruleset is still pending §3.6's
template decision, and because z→s, th→t and now v→f all pile onto the same two
consonants — homophony pressure the vocabulary optimizer may want re-priced at lexicon
scale.

#### Deferred

- **Root shape bounds** (min/max syllables) — deferred until after grammar. Patrick is leaning **analytic**, in which case there may be no root-vs-inflected-word distinction to bound separately.
- **Functional-load policy** (numeric contrast penalties) — deferred; blocks only the lexicon chooser (§7). The two hard minimal-pair bans (l/r, h/r) are already FIRM in §3.3 and are sufficient for hand-designing the grammatical particles.

### 3.7 Orthography (**resolved** by the §3.3 inventory decision, 2026-08-05)

**Decided (2026-08-05): the orthography is diacritic-free IPA restricted to ASCII.** One
character per phoneme, one phoneme per character, with **each character standing for the
phoneme's whole realization class** (§3.4 wide phonemes) rather than a single sound — `h`
means the whole h~[x~χ~ħ] set, `r` any rhotic, `p` fortis [p~pʰ]. IPA values, not English
ones: **`j` is the "y" of *yes*, never English "j".** No digraphs, no diacritics, no silent
letters, and — with §3.6's no-sandhi rule — no gap whatsoever between spelling and speech.

Punctuation and capitalization are **pending a survey** (§7): the policy is "whatever is
most common among the world's languages weighted by total speakers, with English-style as
the default."

**The ASCII orthography is free, with zero casualties.** The closed inventory maps
one-to-one onto 20 ASCII letters:

```
p t k b d g m n f s h j w l r   a e i o u
```

Every §3.7 problem symbol is gone: **ʃ** and **tʃ** disappeared with the declined CH
sibilant, and **ŋ** was never in the inventory (it survives as an allophone of /n/, as in
most languages). The /tʃ/ spelling question ("c" vs digraph) is **moot** — c, q, v, x, y, z
are simply unused. The wide-phonemes approach did exactly what §3.4 predicted it might:
the problem symbols never entered the inventory, so the orthography never had to
compromise. Remaining orthographic decisions are conventions only (capitalization,
punctuation, how compounds are written).

*Note /j/ is IPA-valued ("y" of yes), not English-valued — the one place where an
English-reading learner is actively misled by the ASCII choice.*

#### Prior discussion (superseded, kept for the record)

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

### Validation results (revised 2026-08-04)

The old headline "AUC 0.923" is **retired**: its negative controls were drawn from the *global* pool of source words, so a model could score well by detecting which donor pool a recipient borrows from rather than by modelling adaptation. Under the honest protocol — leave-one-recipient-out over all 41 WOLD recipients, controls shuffled *within* recipient — v0 scores **AUC 0.8961 ± 0.0618** (min 0.720 for Mandarin, max 0.985 for Bezhta). Costs learned from the same data score **0.9569 ± 0.0391** and beat v0 on **41 of 41** held-out recipients. Full detail: [`cost-learning.md`](cost-learning.md).

Sanity gradient vs /da/ under v0 orders as desired: ta 0.98 > ða 0.91 > ɡa 0.85 > fa 0.82 > ma 0.75 > ia 0.41 (though compressed into 0.75–0.98; the learned costs order the same way with far better separation, 0.84 down to 0.00).

### Known issues

*Updated 2026-08-04 by the cost-learning study ([`cost-learning.md`](cost-learning.md)); issues 1 and 2 move from "known" to "bounded".*

1. **Place of articulation underweighted** by panphon's default weights: projection maps /v/ → /z/ for a Japanese-like inventory where real loanword adaptation gives /v/ → /b/ (confirmed: default costs are /v/→/z/ 1.125, /v/→/b/ 1.250). **BOUNDED and fixable.** Learning the weights from WOLD raises the labial weight to 3.2× panphon's (0.803 ± 0.018 across 41 leave-one-recipient-out folds) and flips the diagnostic: /v/ → /b/ now wins over /z/ by a factor of 1.9. More precisely than expected, it is *labiality* that was underweighted, not place in general — coronal place detail (`ant`, `cor`, `distr`) goes **down** and manner (`cont`) barely moves. The learned weights are in `data/processed/learned_costs.csv` and `metric.py` accepts them via `params=`, but they are **not the default** — see issue 5.
2. **No epenthesis modeling.** **BOUNDED, partially fixed.** The cost model now has separate insertion prices for vowels and consonants (and, in the `context` variant, for cluster-repair vs other positions), fitted jointly with the substitution weights. Insertion and deletion drop from panphon's flat 7.25 to 2.2–3.9 and separate correctly (deleting a vowel is the cheapest edit at 2.18, inserting a consonant the dearest at 3.91), and cluster-repair insertion is 13–21% cheaper than gratuitous insertion. But "sutoraiku" vs "strike" goes 0.617 → **0.577** — the wrong way — where hand-setting the cluster-insertion prices gives 0.904. The reason is structural: the negative control shares the recipient word, so cheap insertion helps it as much as the true pair, and a **discriminative objective cannot learn repair costs**. Fixing it needs a generative term, not a richer insertion model. **The bias toward permissive codas is reduced, not removed**, so the syllable-template experiment (§7.4) still needs the caveat, now with a measured size rather than an assertion.
3. **Baseline inflation:** random CV-ish pairs score ~0.46, so usable dynamic range is roughly [0.45, 1.0]. Recalibrate against that floor, e.g. `score' = max(0, (s − s_random)/(1 − s_random))`. (Unchanged.)
4. **Glyph normalization:** ASCII `g`, `:`, `'` are mapped to proper IPA in `segments()`; watch for more lookalikes when ingesting new sources. (Unchanged.)
5. **NEW — the learned costs encode loanword facts, not only perceptual ones.** Fitted freely the WOLD data prices *voicing* at ~7× panphon's weight; even with the major-class prior it settles at **3.5×**, the single largest upward move in the parameter table. The contrast study says voicing is one of the **cheapest** contrasts perceptually (t/d natively audible to 75%, p/b to 73%). Loanword orthographies record voicing faithfully on both sides, so the fit is learning a transcription artifact — and this single effect is what makes the contrast-study cross-check come out null (ρ = +0.059, p = 0.79): the vowel-quality contrasts move correctly, every voicing contrast moves wrongly, and they cancel. Similarly, aspiration/breathiness (`sg`), ejectivity (`cg`) and clicks (`velaric`) learn weight ≈ 0 — which means "no evidence in WOLD's recipient set", not "does not matter". This is why v0 is still the default.

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

1. **The metric works at v0 quality — but the original number was measured too generously.** Under an honest protocol (recipient-grouped CV, controls shuffled within recipient) v0 separates attested loanword pairs from controls at **AUC 0.896 ± 0.062**, not the 0.923 first recorded; the difference is that the old controls came from the global source pool, so part of that 0.923 was a donor-pool detector. 0.896 is still good separation given noisy transcriptions on both sides, and good enough to rank candidate phonologies. (2026-08-04)
2. **Listener conditioning is implementable and cheap** — segment-wise nearest-native-category projection against PHOIBLE inventories behaves correctly on the classic cases (/l/~/ɾ/ free for Japanese-like listeners).
3. **The metric's failure modes are characterized**, not just suspected: place-of-articulation underweighting (/v/→/z/ instead of /v/→/b/), no epenthesis (punishes attested heavy-epenthesis adaptations, flatters permissive codas), and a ~0.46 random-pair floor. Each has a concrete fix path (§4). **Update 2026-08-04:** the place problem is fixed by learning the weights (labial ×3.2, diagnostic flips, stable across 41 held-out recipients); the epenthesis problem is *not* — see finding 8.
4. **WOLD is usable as ground truth** for learning substitution costs: **13,595** clean attested adaptation pairs after a now-committed filter (`scripts/wold_pipeline.py`), despite the empty `Source_Form_ID` column. It is *not* usable for repair costs — see finding 8.
5. **ASJP requires no transcription conversion** — its `Segments` column is already CLTS-tokenized and panphon-compatible, removing an expected preprocessing step.
6. **CLDR alone can't serve both objectives.** Its figures are total-speaker counts: exactly right for the ease/L2 term, unusable for the representation/L1 term. The two-objective design forces sourcing a second population dataset.
7. **The ASCII orthography is nearly free** given the kind of inventory the prevalence data is expected to favor — the losses concentrate in ʃ/tʃ/ŋ, and ŋ is recoverable allophonically.
8. **A discriminative objective cannot learn repair costs (2026-08-04, new).** Fitting costs so attested loanword pairs outrank shuffled controls buys a large, stable win on substitution structure and **no** improvement on epenthesis — because the negative control shares the recipient word, so a cheap vowel insertion helps the decoy as much as the truth. This is a general lesson for the project's method, not a WOLD quirk: ranking objectives learn what *discriminates*, and repair operations do not discriminate. Anything we want the metric to *predict* (rather than rank) needs a generative term.
9. **Learning from loanwords teaches orthography as perception (2026-08-04, new).** The fit prices voicing at 3.5× panphon's weight because loanword transcriptions record voicing faithfully on both sides — while the independent contrast study prices voicing as one of the cheapest contrasts for real listeners. The two disagree so sharply that the contrast-study cross-check comes out null overall (ρ = +0.059). Calibration data has to be chosen for the *concept* being calibrated.

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
   - Learned costs beat panphon's defaults on **41 of 41** held-out recipients (0.9569 vs 0.8961; paired delta +0.061 ± 0.033), with learned weights stable to 1–8% relative sd across folds. The honest default-weight baseline is **0.896**, not 0.923.
   - **The place-of-articulation fix is real and stable**; the epenthesis fix moves the wrong way; **two of five guardrails fail** (4 and 5). **v0 remains the default metric**; the learned costs ship as `data/processed/learned_costs.csv` and are opt-in via `metric.similarity(..., params=...)`.
   - A phonetically coherent metric costs ~0.009 AUC: unconstrained fits reach 0.965 but score /d/→/i/ cheaper than /d/→/f/. The three major-class features (`syl`, `son`, `cons`) had to be held near panphon's values by a targeted prior — the data as we can clean it does not inform them.
   - New standing worry: the loanword corpus teaches production/orthography facts (voicing) as if they were perceptual facts. §4 known-issue 5.

6. **Retire the loanword-only calibration (NEW, OPEN)** — the cost model is calibrated on adaptation but consumed for recognition and distinguishability. The contrast study is the only non-loanword anchor we have, and it is inventory-level, not word-level. Candidates for a second anchor: perceptual-confusion matrices from the L2 speech-perception literature; ASJP cognate alignments (Jäger-style PMI) as a *within-family* substitution signal that has no orthography in it.

Standing open questions:

- **Representation term formulation (OPEN):** string-similarity vs etymology attribution share (§2).
- **PHOIBLE multi-inventory policy (decided SOFT):** majority vote across a language's inventories (≥50%), chosen in the prevalence study; union and intersection rejected (judgment calls documented there).
- **Diphthong-mediated contrasts (OPEN, new):** binary "has the phoneme" checks under-credit listeners whose inventories carry a vowel quality only inside diphthongs/allophones (Mandarin 918M, Wu 81M — see contrast-study Addendum). The listener-conditioned metric handles this at the word level; decide whether inventory-level analyses need a correction, or whether all downstream decisions should use the word-level metric.
- ~~**Second stop series**~~ **DECIDED 2026-08-05: taken** (§3.3), on the people-weighted reading of §2. The ~61%-of-languages figure is the accepted cost.
- **Glide-selection rule for hiatus (OPEN, new, small):** §3.6 fixes *that* hiatus is repaired by glide insertion but not *which* glide. Patrick's example `oa`→`owa` implies the **preceding** vowel selects it (o is round → w). The unresolved case is /a/, which is neither front nor round and is our most common vowel: `ai ao au ae` have no preceding-vowel answer. Candidate rule: pick the glide from whichever vowel of the pair is high/peripheral (j if either is i/e, w if either is u/o, preceding wins ties), leaving only `aa` unresolved.
- **Onset-cluster inventory (OPEN, conditional):** if the international-vocabulary study says onset clusters pay for themselves, the permitted set must be enumerated exhaustively rather than left to a productive rule.
- **Segment discouragement weights (OPEN, new):** §3.3 ranks /r/ /h/ > /l/ > /b d ɡ/ as segments to avoid where the lexicon has a choice. This is currently an ordinal ranking and must become a numeric penalty before the lexicon optimizer runs.
- ~~**Stress rule**~~ **DECIDED 2026-08-05: first syllable** (§3.5). See [`stress-prevalence.md`](stress-prevalence.md); initial was chosen over the headline penultimate on simplicity, and because the penultimate lead depends on collapsing weight-sensitive systems.
- **Punctuation & capitalization (OPEN, survey running):** policy is "most common among the world's languages, weighted by total speakers; English-style as default." Note a majority of humanity writes in a **caseless** script, so "capital letters at all?" is a real question.
- **Compounding: keep or drop (OPEN, new):** §3.6 now permits geminates across compound boundaries to protect compound transparency, but Patrick may eschew compounding entirely, which would moot it. Bears on derivation (§3.2) and on root-shape bounds.
- **Loss shape details (SOFT):** AE + MSE combination is a proposal, not validated.
- ~~**/tʃ/ orthography**~~ **MOOT** — the §3.3 inventory has no /tʃ/; the ASCII orthography is free (§3.7).

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
