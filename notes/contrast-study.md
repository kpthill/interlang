# Contrast study (2026-07-14)

> **Rev 2 (same day):** numbers regenerated after the phantom-MSA L1 fix (see
> Addendum). Stop-series and vowel rows rose ~2-5 points; r/l, s/θ, s/ʃ
> dipped slightly (Arabic has those).

*What share of humanity can natively hear each candidate distinction?*
Companion to [`phoneme-prevalence.md`](phoneme-prevalence.md) (which prices
*segments*; this prices *pairs*). Resolves inputs for
[`principles.md`](principles.md) §3.3–§3.4. Reproduce:

```
uv run python scripts/contrast_study.py   # -> data/processed/contrast_costs.csv
```

## Method

Same universe, weights, and policies as the prevalence study (2,177 PHOIBLE
languages, majority-vote inventories, lumped symbols, Wikidata L1 / CLDR total
weights). For each contrast (A, B):

- **% both** — share whose native language has *both* members as phonemes →
  the contrast is natively audible. Reported for L1 speakers, total
  (person-language pairs), and unweighted languages.
- **% exactly-one** — the native system has one category where we'd have two:
  the worst case, since foreign A and B both assimilate to that one category.
- **Merger langs** — languages where PHOIBLE lists one member as an
  *allophone* of the other while lacking it as a phoneme (e.g. [ɾ] as an
  allophone of /l/ in Korean) — direct evidence of an active merger.

The **stop-series rows** ask the wide fortis/lenis question (§3.4): does the
language have ≥2 stop categories at that place of articulation, counting
plain/aspirated/voiced/breathy as different categories (strict symbol level,
since aspiration is deliberately stripped at the lumped level).

**Caveats.** (1) "Has both" ≈ "hears the contrast" is approximate in both
directions: motivated listeners can learn some non-native contrasts, and
having both segments doesn't guarantee they contrast in every position.
(2) Vowel rows are noisy because languages differ in whether mid vowels are
analyzed as monophthongs or diphthongs — English's majority PHOIBLE analysis
has no plain /o/ (it's /oʊ/), Mandarin's monophthongs are ~/a ə i u y/. The
wide-vowel rows (i/E-cls etc.) partially correct for this; treat narrow vowel
rows as lower bounds. (3) Contrast audibility is necessary but not sufficient:
cost also depends on how much lexical weight (functional load) we put on the
contrast — see Implications.

## Results (sorted by L1-weighted "both")

| Contrast | % L1 both | % total both | % langs both | % L1 exactly-one | Merger langs | Note |
|---|---|---|---|---|---|---|
| m / n | 99.0 | 99.4 | 93.9 | 0.9 | 2 | control: should be ~universal |
| e / i vs a | 98.5 | 98.7 | 97.5 | 1.5 | 1 | sanity control |
| 2-way coronal stops (t tʰ d dʱ) | 96.5 | 97.5 | 63.1 | 2.6 |  | fortis/lenis wide contrast |
| 2-way velar stops (k kʰ ɡ ɡʱ) | 95.1 | 92.6 | 61.3 | 4.7 |  | fortis/lenis wide contrast |
| 2-way labial stops (p pʰ b bʱ) | 93.5 | 91.9 | 60.3 | 6.3 |  | fortis/lenis wide contrast |
| R-cls / L-cls | 84.6 | 88.8 | 65.3 | 14.3 | 45 | widest liquid classes |
| O-cls / a | 83.1 | 82.2 | 80.9 | 16.0 | 12 | wide mid-back vs low |
| r / l | 81.9 | 84.0 | 64.0 | 17.0 | 45 | the classic |
| E-cls / a | 81.8 | 81.4 | 83.6 | 17.8 | 11 | wide mid-front vs low |
| i / E-cls | 81.7 | 81.2 | 82.4 | 18.2 | 16 | wide mid-front vs high |
| u / O-cls | 80.2 | 80.1 | 76.4 | 19.2 | 29 | wide mid-back vs high |
| f / p | 77.2 | 81.4 | 39.2 | 21.9 | 20 | matters where f is missing |
| t / d | 75.1 | 79.8 | 59.5 | 24.0 | 58 | voiced-series cost, coronal |
| k / ɡ | 73.7 | 74.7 | 56.1 | 26.2 | 77 | voiced-series cost, velar |
| i / e | 73.0 | 74.8 | 74.5 | 26.6 | 19 | narrow (see caveat 2) |
| p / b | 72.7 | 74.6 | 56.7 | 27.1 | 81 | voiced-series cost, labial |
| u / o | 70.2 | 60.3 | 69.9 | 26.8 | 30 | narrow (see caveat 2) |
| s / SH-cls | 61.9 | 74.0 | 35.7 | 37.1 | 82 | s vs any hushing sibilant |
| s / ʃ | 58.6 | 71.9 | 32.1 | 40.3 | 79 | ʃ is s's top allophone |
| n / ŋ | 57.9 | 64.8 | 63.2 | 41.9 | 95 | ŋ is n's top allophone |
| w / b | 51.6 | 60.8 | 53.5 | 47.2 | 2 |  |
| s / z | 49.2 | 62.6 | 32.3 | 49.3 | 30 |  |
| a / ə | 47.9 | 58.3 | 23.7 | 51.7 | 45 |  |
| ʃ / tʃ | 43.6 | 55.2 | 25.9 | 27.9 | 7 |  |
| e / ɛ | 40.7 | 52.5 | 30.7 | 41.8 | 126 | must be one wide phoneme |
| o / ɔ | 36.5 | 35.6 | 30.6 | 46.8 | 102 | must be one wide phoneme |
| f / v | 34.3 | 43.5 | 25.0 | 45.4 | 16 |  |
| v / b | 31.2 | 41.1 | 24.1 | 48.0 | 6 |  |
| j / dʒ | 30.6 | 44.7 | 25.9 | 60.5 | 7 |  |
| tʃ / dʒ | 28.5 | 39.9 | 24.7 | 31.0 | 21 | voicing in affricates |
| i / ɪ | 26.6 | 38.2 | 13.3 | 73.3 | 143 | English-style lax vowel |
| w / v | 26.2 | 36.8 | 22.4 | 57.0 | 24 |  |
| u / ʊ | 26.2 | 37.9 | 12.0 | 71.2 | 87 |  |
| u / y | 25.4 | 24.6 | 5.6 | 71.0 | 13 | front rounded — expected floor |
| ts / tʃ | 21.1 | 17.6 | 15.4 | 48.9 | 46 |  |
| s / θ | 16.5 | 28.8 | 2.8 | 82.3 | 3 | expected near-floor |
| h / x | 10.9 | 14.5 | 10.7 | 72.4 | 41 | wide-H members — never contrast |

## Findings

1. **The wide fortis/lenis stop contrast is the study's big winner.** A second
   stop series distinguished by voicing OR aspiration is audible to 93–96% of
   humanity, vs only 73–75% for a strictly *voiced* second series — the wide
   definition buys ~20 points of the world. Coronal (t-family) is the
   strongest place (96.5%), labial the weakest (93.5%). Note the flip side:
   only ~60–63% of *languages* have any two-way series — single-series
   languages (much of Australia, parts of the Americas) are numerous but
   small. A second stop series is well-supported by people-weighted fairness
   and poorly by language-weighted fairness.
2. **r/l is audible to 5 in 6 people, actively merged for the rest.** 81.9%
   L1 (84.6% with widest classes), with 45 languages showing one liquid as an
   allophone of the other. Keeping both /r/ and /l/ is defensible but the
   ~16% (Japanese, Korean, and many smaller languages) is real; see
   Implications for the mitigation.
3. **The sibilant space collapses to: /s/ plus at most one wide hushing
   category, unvoiced.** s vs any hushing sibilant: 61.9%. ʃ vs tʃ: 43.6%.
   ts vs tʃ: 21.1%. tʃ vs dʒ: 28.5%. So a second sibilant category is already
   marginal, and *internal* distinctions among hushing sounds (ʃ/tʃ/ts/dʒ) are
   inaudible to most of the world — if we take a second sibilant at all it
   should be one wide CH/SH category (any of [tʃ ʃ tɕ tʂ c] accepted).
4. **Voiced fricatives are out.** f/v 34.3%, s/z 49.2%, v/b 31.2%, w/v 26.2%.
   /v/ and /z/ cannot carry contrast for most of humanity. /f/ itself is fine
   (79% prevalence), but f/p at 77.2% deserves low functional load.
5. **The five-vowel system survives, with mandatory wide mids.** With wide
   E={e,ɛ} and O={o,ɔ}, every height contrast lands at 80–83% L1 — the
   narrow-row shortfalls (i/e 73%) are partly artifacts of diphthong-heavy
   analyses (caveat 2). e/ɛ (40.7%, 126 mergers) and o/ɔ (36.5%, 102) confirm
   the mids must each be ONE wide phoneme. The residual ~18% shortfall is
   mostly the Mandarin/Wu diphthong-analysis question (see Addendum); the
   genuinely three-vowel populations (Maghrebi Arabic, Berber, Quechua,
   Cebuano...) are a few percent of humanity — a 3-vowel /a i u/ design would
   be maximally safe but pays heavily in word length and source-word
   fidelity; keep 5 (SOFT).
6. **No schwa, no lax vowels, no ŋ, no /v z dʒ ʒ θ y ʊ ɪ/.** a/ə 47.9%,
   i/ɪ 26.6%, u/ʊ 26.2%, n/ŋ 57.9% — all well below viability. i/ɪ and u/ʊ
   have the highest merger counts in the study (143, 87): most languages that
   have the lax member treat it as the same category as the tense one.
7. **Controls behaved**, validating the method: m/n 99.0%, the vowel sanity
   row 98.5%, u/y 25.4% (front rounded vowels are famously parochial),
   s/θ 16.5%, and h/x 10.9% — h and x must indeed be one wide phoneme (72.4%
   of humanity has exactly one of the two and will map anything we say onto
   it, for free).

## Implications for the design (proposed, not yet committed)

- Emerging consonant core, in descending confidence: **m n p t k s j w r h**
  (h wide over [x χ ħ]), then **f**, then *one* of: a fortis/lenis second
  stop series (93–96% audible), **l** (82–85%), one wide CH sibilant (~62%
  vs /s/). Each addition buys shorter words and better source fidelity at a
  measured perceptual cost.
- Vowels: **a i u + wide E + wide O**.
- **Contrast cost should become functional-load pricing in the lexicon
  optimizer, not just keep/drop decisions.** A kept-but-expensive contrast
  (r/l, f/p, s/CH) can be made nearly free in practice by penalizing minimal
  pairs that hinge on it — "keep /l/, but never let *lira* and *rira* both be
  words." This turns the table above into per-pair penalty weights, which is
  strictly more information than a binary inventory choice. (Proposed
  mechanism for principles §3.3.)
- The stop-series decision is the clearest case where people-weighted and
  language-weighted fairness disagree (93–96% of people vs ~61% of languages);
  it should be decided explicitly under the project's declared weighting, not
  by default.

## Addendum: decomposing the mid-vowel shortfall (finding 5)

Patrick asked how much of the ~22% i/E and u/O shortfall is Classical/Standard
Arabic, and how much is mitigated by colloquial varieties. Answer: most of the
shortfall was two artifacts.

1. **Phantom MSA (data bug, to fix).** Wikidata's `arb` "Standard Arabic" L1
   figure (335M) is really the macro-Arabic total; MSA has ~no native
   speakers, and the real varieties are listed separately (≈300M summed) — so
   Arabic was double-counted, with the phantom half attached to PHOIBLE's
   3-vowel MSA inventory. Colloquial varieties mostly DO have mid vowels
   (Egyptian/Sudanese/Libyan/Najdi `a e i o u`, from *ai/au*
   monophthongization); the genuinely 3-vowel-ish Arabic is Maghrebi
   (Moroccan `i u ə`; with Algerian/Tunisian ≈ 80M). **Fix:** set arb L1 ≈ 0
   in l1_speakers.csv (affects all three studies — pharyngeals and the
   /p/-gap were also overweighted by 335M).
2. **Mandarin's diphthong analysis (policy question, OPEN).** Mandarin (918M
   = 13.3 points of the shortfall) and Wu (81M) count as lacking /e o/
   because their mid-vowel qualities live inside diphthongs (*ei ie ou uo*)
   and allophones of /ə/, not as standalone phonemes. Whether such listeners
   recover an /e/-vs-/i/ contrast is exactly what the listener-conditioned
   metric models better than binary inventory membership.

Corrected estimates: remove phantom MSA → i/E 81.7%, u/O 80.2%; also credit
Mandarin → 96.6% / 95.2%. The residual genuinely-3-vowel population (Maghrebi
Arabic, Berber, Quechua, Cebuano...) is a few percent of humanity, not ~22%.
Finding 5 restated: **five vowels with wide mids costs ~3–8% of humanity.**

*Status: the MSA fix is now applied (`L1_OVERRIDES` in
`scripts/fetch_l1_speakers.py`) and the tables above reflect it. The
Mandarin/Wu diphthong question remains OPEN — logged in principles.md.*

## Not yet measured

- **Positional effects**: a contrast can be audible in onsets but not codas
  (Mandarin: no voicing anywhere, but also NO codas beyond n/ŋ). Interacts
  with the syllable-template experiment.
- **Asymmetric assimilation**: % exactly-one says two categories collapse,
  not *which way* — the listener-conditioned metric handles this per-word.
- **Functional load in source languages** (how hard each contrast works in
  the vocabulary we'll actually borrow) — belongs to the lexicon stage.
