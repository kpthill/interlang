# Word-stress prevalence study (2026-08-05)

*Which word-stress rule is native to the most people?* We want **one**
hard-and-fast stress rule for the interlang — stateable in a sentence, applicable
mechanically by a learner who has never seen the word before. This study ranks
broad stress-rule categories by native-speaker population, and asks whether there
is a clear winner or whether "no lexical stress at all" (the French/Esperanto-free
compromise) is the honest fallback.

Reproduce with:

```
git clone --depth 1 https://github.com/cldf-datasets/wals data/raw/wals
uv run python scripts/stress_prevalence.py   # -> data/processed/stress_prevalence.csv
                                             #    data/processed/stress_by_language.csv
```

## Answer up front

**Penultimate wins, and not narrowly.** Under the classification we consider most
honest (see *Tone languages* below), the stress rule closest to what people
already have is:

| Nearest single fixed rule | % L1-weighted | % total-weighted | % of languages |
|---|---|---|---|
| **penultimate** (second-from-last syllable) | **50.4** | **61.6** | 32.9 |
| no lexical stress (tone languages) | 30.1 | 24.7 | 14.4 |
| initial (first syllable) | 8.4 | 5.2 | 22.2 |
| no single default (genuinely unpredictable) | 6.6 | 5.0 | 14.6 |
| final (last syllable) | 4.1 | 3.1 | 10.8 |
| antepenultimate | 0.5 | 0.2 | 2.1 |
| second syllable | 0.0 | 0.0 | 2.8 |
| third syllable | 0.0 | 0.0 | 0.2 |

Percentages are shares of the **covered** population (4.54B L1 = 66% of the world;
see *Coverage*), not of the world. `nearest_fixed` / `tone_aware_extended` rows of
`data/processed/stress_prevalence.csv`.

The result survives aggressive discounting. Even if you throw out the three
largest and most arguable members of the penultimate bucket — English, French and
Hindi, all of which are really weight-sensitive rather than flatly penultimate —
penultimate still leads at **32.9%**, ahead of the 30.1% "no lexical stress" bloc.
Nothing else is close: initial, the runner-up positional rule, is a sixth its
size.

So: **fixed penultimate stress**, and flat/no-stress is *not* forced on us as a
compromise. The full argument, and the caveats that could still push us to flat,
are in *What this implies* at the end.

## Jargon (for a non-linguist reader)

- **stress** — the syllable said louder / longer / higher: *PHO-to-graph* vs
  *pho-TO-gra-pher*. "Fixed" stress means you can predict its position from the
  shape of the word alone, without knowing the word.
- **penultimate / antepenultimate / ultimate (final)** — second-from-last,
  third-from-last, last syllable.
- **syllable weight** — many languages count a syllable as *heavy* if it has a
  long vowel or ends in a consonant, and stress the heavy one. That is still a
  rule, just a conditional one; it is a different kind of thing from "you have to
  memorise it per word".
- **tone** — languages like Mandarin, Vietnamese, Yoruba use *pitch* to
  distinguish words (Mandarin *mā* "mother" vs *mà* "scold"). Most of them have
  no word stress in the European sense at all.
- **trochaic / iambic** — a rhythm description: trochaic = strong-weak
  (*TA-ta*), iambic = weak-strong (*ta-TA*). Used here only to decide which end
  of a two-syllable window a language leans on.
- **doculect** — one described variety. WALS describes *Arabic (Egyptian)* and
  *Arabic (Beirut)* separately; both are doculects, neither is "Arabic".

## Method

Universe: **WALS**, chapters 13–17. Backbone is **14A Fixed Stress Locations**
(502 doculects). Where 14A says only "no fixed stress", **15A Weight-Sensitive
Stress** and **16A Weight Factors** say what kind of non-fixed system it is, and
**17A Rhythm Types** says which end of the word it leans on. **13A Tone** drives
the tone policy.

Weighting follows [`phoneme-prevalence.md`](phoneme-prevalence.md) exactly: L1
counts from `data/processed/l1_speakers.csv` (Wikidata P1098, 1,858 languages),
joined on ISO 639-3 with a Glottocode fallback; total-speaker counts from CLDR
(a *speaker-language pair* count, so multilinguals are overcounted — see that
study's judgment call 7); languages missing from the L1 source default to 10,000
L1 speakers.

### Two classification schemes

The study emits both, because they answer different questions.

**TIER A — `wals_rule`: "what kind of system is it?"** Faithful to WALS.

| Condition | Category |
|---|---|
| 14A = Initial / Second / Third / Antepenultimate / Penultimate / Ultimate | that fixed location |
| 14A = No fixed stress, and 15A = "Not predictable" **or** 16A = "Lexical stress" | lexically unpredictable |
| 14A = No fixed stress, any other 15A value | weight-sensitive |
| 14A = No fixed stress, 15A missing | unclassified |

**TIER B — `nearest_fixed`: "which single fixed rule is closest?"** This is the
actionable table. We cannot adopt "it depends on syllable weight" as our rule, so
every weight-sensitive system is collapsed onto the location a learner defaults
to, using the edge orientation in 15A and the foot type in 17A:

| 15A value | Tier B |
|---|---|
| Left-edge: first or second | second if 17A = Iambic, else **initial** |
| Left-oriented: one of the first three | **initial** |
| Right-edge: ultimate or penultimate | final if 17A = Iambic, else **penultimate** |
| Right-oriented: one of the last three | final if 17A = Iambic, else **penultimate** |
| Unbounded / Combined / Not predictable | no single default |

Trochaic is the fallback when 17A is missing or "Undetermined", because trochaic
outnumbers iambic 153 : 31 in WALS.

This is deliberate over-simplification — *that is the point of the study*, since
the deliverable is a one-sentence rule — but it does misfire on individual
languages. Known misfires are listed under *Judgment calls* #4.

## Ranked tables

### Tier A (WALS-faithful), tone-aware-extended policy

| Rule category | % L1-weighted | % total-weighted | % of languages | n |
|---|---|---|---|---|
| weight-sensitive | 41.7 | 52.7 | 30.7 | 173 |
| no lexical stress (tone) | 30.1 | 24.7 | 14.4 | 81 |
| lexically unpredictable | 13.2 | 8.6 | 5.9 | 33 |
| initial | 7.5 | 4.3 | 16.2 | 91 |
| final | 3.6 | 2.7 | 9.1 | 51 |
| penultimate | 3.4 | 6.7 | 18.8 | 106 |
| antepenultimate | 0.5 | 0.2 | 2.1 | 12 |
| second | 0.0 | 0.0 | 2.5 | 14 |
| third / unclassified | 0.0 | 0.0 | 0.4 | 2 |

Read straight, Tier A says: **most of humanity's native stress systems are
weight-sensitive**, i.e. "there is a rule, but it consults the shape of the
syllable". That is not a rule we can adopt — an interlang with weight-sensitive
stress would need learners to parse coda consonants and vowel length before they
can say a word — which is exactly why Tier B exists.

### Tier B (nearest single fixed rule), all three tone policies

L1-weighted %, so the columns are comparable across policies only in shape (the
denominator grows in the last column):

| Nearest fixed rule | wals_as_is | tone_aware | tone_aware_extended |
|---|---|---|---|
| penultimate | 56.0 | 56.0 | **50.4** |
| no lexical stress | — | 22.4 | 30.1 |
| initial | 9.3 | 9.3 | 8.4 |
| no single default | 29.7 | 7.3 | 6.6 |
| final | 4.5 | 4.5 | 4.1 |
| antepenultimate | 0.5 | 0.5 | 0.5 |
| second | 0.0 | 0.0 | 0.0 |
| covered L1 | 4.09B | 4.09B | 4.54B |

Penultimate leads under every policy. What the tone policy changes is *what comes
second*, and whether "unpredictable" looks like a third of humanity (it does not —
that number is almost entirely Mandarin sitting in the wrong bucket).

### Where the penultimate bloc comes from

Under `tone_aware_extended`, the 50.4% penultimate bucket decomposes as:

| Tier A origin | % of covered L1 | n languages |
|---|---|---|
| weight-sensitive, right-leaning, collapsed to penult | 39.3 | 72 |
| lexically unpredictable but right-leaning (Portuguese, Italian, Romanian, Catalan …) | 7.7 | 7 |
| genuinely fixed penultimate in WALS | 3.4 | 106 |

Largest members: Spanish 485M, English 379M, Hindi 341M, Portuguese 254M, French
77M, German 77M, Javanese 68M, Italian 65M, Egyptian Arabic 65M, Gujarati 56M,
Bhojpuri 52M, Indonesian 44M, Polish 40M, Maithili 34M, Sundanese 32M, Levantine
Arabic 25M, Romanian 24M, Tagalog 24M, Dutch 23M, Awadhi 22M.

Note the shape of that list: **the penultimate bloc is not a European artefact.**
Indo-Aryan (Hindi, Bhojpuri, Maithili, Awadhi, Gujarati), Arabic, and
Malayo-Polynesian (Indonesian, Javanese, Sundanese, Tagalog, Cebuano's relatives)
each contribute independently of Romance.

### Sensitivity: strip the arguable members

| Penultimate bucket, excluding | % L1-weighted |
|---|---|
| — (as computed) | 50.4 |
| French (really phrase-final) | 48.7 |
| English (really weight-sensitive, and famously irregular) | 42.1 |
| English + French | 40.4 |
| English + French + Hindi | 32.9 |

Still first in every row.

## Tone languages — the consequential judgment call

Mandarin has 918M L1 speakers, 20% of the covered population by itself. WALS
chapters 14/15/16 classify it as *no fixed stress / not predictable / lexical
stress* — i.e. as a **Russian-style memorise-it-per-word system**. That is not
what Mandarin is. Mandarin's word-level prominence is carried by tone plus
neutral-tone reduction; there is no lexically contrastive stress to memorise, and
a learner of Mandarin never asks "which syllable is stressed in this word".
Leaving it in "lexically unpredictable" would make an entire category out of one
misfiled language.

WALS offers no "no word stress" value at all, so this has to be an explicit
policy. Three are emitted; the CSV carries all three so the choice is auditable.

**`wals_as_is`** — nothing reassigned. Mandarin stays "lexically unpredictable",
which is why that category shows 37.1% of covered L1 under Tier A. Treat this
column as *what WALS literally says*, not as a finding.

**`tone_aware`** — a language whose 13A is "Complex tone system" **and** whose
Tier A came out "lexically unpredictable" is moved to **no lexical stress**. Only
three languages qualify (Mandarin, Grebo, Lealao Chinantec) and Mandarin is 99.99%
of their weight, so this policy is, honestly, "the Mandarin decision". It moves
22.4 percentage points. The restriction to the *unpredictable* bucket is
deliberate: tonal languages for which WALS **does** state a stress rule keep it —
Zulu is tonal *and* penultimate, and stays penultimate.

**`tone_aware_extended`** (headline) — as above, plus the languages that have
13A = "Complex tone system" and **no 14A value at all** are added to the universe
as "no lexical stress": 79 languages, **448M L1**, led by Wu 81M, Vietnamese 76M,
Cantonese 73M, Min Nan 50M, Hakka 48M, Yoruba 38M, Burmese 33M, Thai 21M. The
rationale is that WALS's stress chapters *declined to classify* these, and for a
complex-tone language that silence is evidence of absence rather than missing
data. Dropping them silently would bias the denominator toward the stress-having
half of the world — precisely the failure mode we are trying to avoid.

**Deliberately excluded from all three policies: "Simple tone system".** That
class contains **Japanese** (128M), whose pitch accent *is* a lexically
unpredictable word-prominence system — a Japanese learner does memorise which
mora carries the accent — so folding Japanese into "no lexical stress" would be
wrong. It also contains Hausa (44M), Igbo (27M) and Somali (16M), which arguably
*do* belong in "no lexical stress"; leaving them out is the conservative
direction, since it **understates** the no-stress bloc and therefore understates
the case against our conclusion. If someone later argues these in, "no lexical
stress" rises by roughly 87M (~1.9 points) and penultimate falls by about 1 point
— not enough to change the ranking.

**Bottom line, both ways.** With tone languages counted as having no lexical
stress: penultimate 50.4%, no-stress 30.1%. With WALS taken literally and no
reassignment at all: penultimate 56.0%, and Mandarin's 918M inflates a
"lexically unpredictable" bucket to 29.7%. Under neither reading does "no lexical
stress" or "unpredictable" beat penultimate. **The tone decision changes the
runner-up, not the winner.**

## Coverage

| | languages | L1 speakers | % of L1-source world total (6.86B) |
|---|---|---|---|
| WALS 14A (deduplicated) | 485 | 4.09B | **59.6%** |
| + complex-tone extension | 563 | 4.54B | **66.2%** |

So a third of the world's native speakers are attached to no stress
classification at all, and every percentage above means "share of *covered*
speakers".

**Biggest uncovered languages** (present in WALS but with no 14A value, or absent
from WALS): Japanese 128M, Eastern Panjabi 125M, Filipino 90M, Marathi 83M,
Telugu 82M, Korean 77M, Tamil 75M, Urdu 69M, Jinyu Chinese 47M, Kannada 44M,
Algerian Arabic 42M, Xiang Chinese 37M, Odia 35M, Igbo 27M, Ukrainian 27M,
Amharic 22M. (Wu, Vietnamese, Cantonese, Min Nan, Hakka, Yoruba, Burmese and Thai
are uncovered by 14A but recovered by the complex-tone extension.)

Would they change the answer? Directionally, most of the big absentees lean the
same way or are neutral: Marathi, Telugu, Tamil, Kannada, Malayalam-adjacent
Dravidian, Urdu and Panjabi are all weight-sensitive-or-initial South Asian
systems; Filipino/Tagalog is penultimate; Ukrainian is unpredictable like
Russian; Korean and Japanese are prominence systems that are not stress. The
remaining Chinese varieties would enlarge the no-stress bloc by ~120M. A rough
worst case — every uncovered language counted as *not* penultimate, and the
Chinese varieties added to no-stress — still leaves penultimate around 30% of a
world-sized denominator, ahead of everything except a maximally generous reading
of no-stress. That is a genuinely uncertain margin, and it is the main reason
this study is tagged as evidence for a **SOFT** decision rather than a FIRM one.

## Judgment calls

1. **WALS is the only source; StressTyp2 was wanted and could not be obtained.**
   StressTyp2 (~750 languages, the specialist stress database) has **no CLDF
   release** — none of `cldf-datasets/stresstyp2`, `clld/stresstyp2`,
   `lexibank/stresstyp2` or `cldf-datasets/StressTyp2` exists — and its own
   distribution host `st2.ullet.net`, which serves a SQL dump
   (`st2-v1-archive-0415.tar.gz`), is outside this environment's network
   allowlist. **Logged as an open gap, not a closed question:** ST2 would roughly
   double coverage (750 vs 502 languages) and is the natural cross-check on the
   Tier B collapse, which is the study's weakest link. Fix path: allowlist
   `st2.ullet.net`, load the SQL dump, join on ISO 639-3, and re-run with ST2 as
   a second backbone — reporting disagreements rather than preferring either
   source. Nothing in this write-up should be treated as cross-validated.
2. **16A = "Lexical stress" demotes a language to "lexically unpredictable".**
   WALS's own gloss for that code is "lexical stress, diacritic weight" — i.e.
   the "weight" that the stress rule consults is a per-word diacritic, which is
   another way of saying it is memorised. Applying this moves Russian, Turkish,
   Portuguese, Italian, Romanian, Catalan and Lithuanian out of
   "weight-sensitive". Without it, Tier A's weight-sensitive bucket would absorb
   genuinely unpredictable systems and overstate how rule-governed the world is.
3. **Tier B's trochaic default.** When 17A is missing or "Undetermined", a
   right-leaning window is collapsed to *penultimate* and a left-leaning window
   to *initial*, because WALS's own rhythm counts are 153 trochaic vs 31 iambic.
   This is the single assumption doing the most work in the headline number.
4. **Known Tier B misfires**, listed so they are not silently tolerated:
   - **French → penultimate; it is really phrase-final.** WALS puts French at
     "right-edge, prominence-based, rhythm undetermined" (its schwa-sensitive
     final stress), and the trochaic default then picks penult. 77M mis-assigned.
     Removing French moves the headline from 50.4% to 48.7%.
   - **English → penultimate.** English is genuinely weight-sensitive and full of
     lexical exceptions; "penultimate" is a crude summary even if it is the modal
     pattern for polysyllables. 379M, the largest single assumption in the table.
   - **Cebuano → final** (17A = Iambic), where penultimate is the more usual
     description. 16M, and it moves the *final* bucket, not the winner.
   - **Basque** has 11 WALS doculects spanning second / penultimate / initial /
     unpredictable; the dedup tie-break picks *penultimate*. 750K, immaterial.
   None of these changes the ranking; all of them are visible per-language in
   `data/processed/stress_by_language.csv`.
5. **Doculect deduplication.** WALS is doculect-level (11 Basque varieties, 10
   Arabic varieties, 6 German). Rows sharing a population join key are collapsed
   to one language by **modal category**, ties broken by a fixed category order,
   so no population is counted twice. Only two keys had conflicting Tier A
   categories at all (Basque, Irish), together under 1M speakers.
6. **Join key: ISO 639-3, falling back to Glottocode.** Near-misses that cost
   coverage and were left alone rather than hand-bridged: WALS *Nepali* (npi) and
   *Malay* (zsm) have no row in the L1 source; WALS *Serbo-Croatian* uses the
   macrolanguage code `hbs`, which the L1 source drops in favour of srp/hrv
   (~16M lost); WALS *Pashto* is `pst` (6.5M) while the larger `pbu` (21M) has no
   WALS entry. Hand-bridging these would recover ~20M — 0.4% — and would import a
   judgment call per language, so it was not done.
7. **Percentages are shares of covered speakers**, as in the phoneme prevalence
   study. The covered denominator (4.54B, 66% of world L1) is reported above and
   is a column in the output CSV (`l1_universe`).
8. **Total-weighted column.** Same convention as the phoneme study: CLDR
   total-speaker (L1 + L2) counts, per speaker-language pair, so multilinguals are
   overcounted. It is reported because an auxiliary language is learned as an L2
   and "what do prospective learners already have" is arguably the more relevant
   question — but note it is flattered by English (1.73B CLDR total, and English
   lands in the penultimate bucket via a Tier B assumption). Read the +11-point
   gap between L1 (50.4%) and total (61.6%) weighting as mostly *that*.

## Known problems logged elsewhere

- **ISO 639-3 code `nan` (Min Nan Chinese, 50.1M L1) is parsed as `NaN` by
  pandas' default NA handling.** In `data/processed/l1_speakers.csv` that row
  also has an empty glottocode and name, so a naive
  `dict(zip(iso639_3, l1_speakers))` gets a **NaN key holding 50.1M speakers**,
  which then silently matches *any* language whose ISO code is missing. This
  study reads the file through `interlang.populations.read_l1_speakers`, which
  passes `keep_default_na=False`. `scripts/phoneme_prevalence.py` does **not**,
  and PHOIBLE languages lacking an ISO code will have picked up Min Nan's weight
  there. Added to [`data-audit.md`](data-audit.md).
- **`cldr_totals()` now lives in `src/interlang/populations.py`**;
  `scripts/phoneme_prevalence.py` still has an older inline copy. It was left
  alone so a finished study keeps producing byte-identical output — migrate it
  the next time that script is touched.

## What this implies for our stress rule

**There is a clear winner, and it is fixed penultimate stress.** Flat / no
lexical stress is *not* forced on us as a compromise — it is the second-place
option, and it is second by 20 points.

The recommendation, stated as the rule would be written:

> **Stress falls on the second-from-last syllable of every word, always.**

Why this and not the alternatives:

- **vs. flat / no lexical stress (French-style).** Flat is the native pattern for
  30% of covered speakers, but "no stress" is not actually implementable as
  speech — a speaker has to put prominence *somewhere*, and speakers of the other
  70% will supply one from their L1 whether we specify it or not. Leaving it
  unspecified doesn't produce flatness, it produces uncontrolled variation, which
  is worse for recognizability than a rule that 50% of people already have.
  Specifying penultimate costs the tone-language bloc a small new habit; leaving
  it unspecified costs everyone intelligibility.
- **vs. final.** Only 4% native, and it collides with the fact that most of the
  big final-stress languages (Persian, Uzbek, Turkish-adjacent) are also
  languages where our vocabulary sourcing is thin.
- **vs. initial.** 8% native, and its main constituency (Bengali 300M, plus
  Finno-Ugric and Czech/Slovak) is real but a sixth the size.
- **vs. weight-sensitive.** 42% of speakers have one natively, but it fails the
  one-sentence test: a learner would have to know vowel length and coda structure
  before they could pronounce a new word. It is also the category that most
  strongly presupposes a syllable structure we haven't fixed yet.

Two things penultimate buys us beyond prevalence:

1. **It is compatible with a fixed final vowel.** If content words end in a
   vowel (Esperanto-style `-o` / `-a`), penultimate stress puts the accent on the
   last *root* syllable — Esperanto's rule, and one that survives suffixing
   without moving. Worth checking against whatever the morphology decides.
2. **It never needs to be written.** Spanish, Italian and Greek need accent marks
   precisely because their stress is *not* fully fixed; a genuinely fixed rule
   needs no diacritic, which matters for §3.7 (ASCII orthography).

Two things that could still overturn it:

1. **Coverage.** A third of the world is unclassified, and the biggest absentees
   (Japanese, Korean, the remaining Chinese varieties, Dravidian) skew toward
   "no stress" or "not penultimate". Getting StressTyp2 is the single highest-value
   follow-up, and the number to watch is whether penultimate stays above the
   no-stress bloc on a ~90%-coverage denominator.
2. **The Tier B collapse.** 39 of the 50 penultimate points come from
   weight-sensitive systems collapsed onto penult by a trochaic default, not from
   languages that are flatly penultimate. That is a defensible reading of "what
   rule is closest to what people have", but it is a reading. Anyone who rejects
   it is left with Tier A, where the honest answer is "most people have a
   weight-sensitive system, which we can't use", and then penultimate vs flat is
   a much closer call.

### Suggested edit to `principles.md` (another thread owns that file)

Add to §3, and to the glossary the terms *stress*, *penultimate*, *syllable
weight*:

> **3.x Word stress — penultimate, fixed. [SOFT]**
> Stress falls on the second-from-last syllable of every word, without exception
> and without orthographic marking. Nearest-native-rule for **50.4%** of covered
> L1 speakers (61.6% total-weighted) versus 30.1% for "no lexical stress" and
> 8.4% for initial — [`stress-prevalence.md`](stress-prevalence.md). SOFT rather
> than FIRM for two reasons recorded there: WALS covers only 66% of world L1 and
> the specialist database StressTyp2 could not be obtained, and 39 of the 50
> points come from collapsing weight-sensitive systems onto their trochaic
> default rather than from flatly-penultimate languages.

And to §7 (open questions):

> - **Obtain StressTyp2** (~750 languages) and re-run `stress_prevalence.py` with
>   it as a second backbone, reporting disagreements with WALS rather than
>   preferring either. Needed before the penultimate decision can move to FIRM.
> - **Does penultimate stress interact with the final-vowel/morphology decision?**
>   If content words end in a grammatical vowel, penultimate stress lands on the
>   last root syllable and stays put under suffixation — check once morphology is
>   on the table.

## Outputs

- `data/processed/stress_prevalence.csv` — 52 rows: 2 schemes × 3 tone policies ×
  categories, with `pct_languages`, `pct_l1_weighted`, `pct_total_weighted`, raw
  weighted sums, and the universe size for each policy.
- `data/processed/stress_by_language.csv` — 563 languages: the per-language audit
  trail (WALS 13A–17A values, both scheme assignments, populations, whether the
  L1 join hit).
