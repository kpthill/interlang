# interlang

Designing an international auxiliary language by optimizing explicit, written-down
principles against databases covering approximately all of the world's languages.

The improvement over Esperanto is not "zero bias" (impossible) but bias that is
**chosen, explicit, and measured**. The expected output is a measured tradeoff curve —
how much ease-of-learning you buy at what cost in representational fairness — not a
language that magically feels familiar to everyone.

Start with **[`notes/principles.md`](notes/principles.md)**: the goal, the two-objective
loss, and every design decision so far, each tagged FIRM / SOFT / OPEN, with open
questions and next steps in §7.

## Status

- **Recognizability metric v0** (`src/interlang/metric.py`) — panphon weighted feature
  edit distance with listener conditioning (project both words onto the listener's
  PHOIBLE inventory first). Still the default. Known issues are characterized in
  [`notes/data-audit.md`](notes/data-audit.md); issues 1 and 2 are now *bounded* by
  the cost-learning study rather than merely logged.
  (The older "AUC 0.923" figure is **retired** — its negative controls were shuffled
  globally, which makes the task easier than the one we care about. See
  [`notes/cost-learning.md`](notes/cost-learning.md) §2.)
- **Phoneme prevalence study** — done, [`notes/phoneme-prevalence.md`](notes/phoneme-prevalence.md).
- **Contrast study** — done, [`notes/contrast-study.md`](notes/contrast-study.md).
- **Word-stress prevalence study** — done,
  [`notes/stress-prevalence.md`](notes/stress-prevalence.md). WALS 14A–17A weighted by
  L1 population: fixed **penultimate** stress is the nearest-native rule for 50.4% of
  covered speakers, against 30.1% for "no lexical stress". Coverage is 66% of world
  L1 and StressTyp2 could not be obtained, so the decision is SOFT.
- **Cost learning from WOLD** — done, [`notes/cost-learning.md`](notes/cost-learning.md).
  Substitution + epenthesis costs fitted jointly to 13,595 attested loanword
  adaptations, cross-validated leave-one-recipient-out over all 41 recipients.
  Learned costs are opt-in (`metric.similarity(..., params=...)`), not the default.
- **Punctuation and capitalization survey** — done,
  [`notes/punctuation-survey.md`](notes/punctuation-survey.md). What the world's
  writing systems do with sentence-final marks, `? !`, commas, quotes, case, word
  spacing and number separators, weighted by total (L1+L2) speakers, with each option
  marked available/unavailable to an ASCII Latin orthography. Quotes and number
  formats come from CLDR per-locale data; the rest is knowledge-assembled over the
  top 50 languages and flagged as such. Headline: English-style holds everywhere
  except quotation marks (no locale on earth specifies straight `"`) and case —
  53% of the world's total-speaker weight writes in a script with no capitals.
- **International vocabulary vs syllable templates** — done,
  [`notes/international-vocab.md`](notes/international-vocab.md). 52 Latin/Greek and
  Wanderwort items rendered under six phonotactic variants by an explicit
  transliteration ruleset (`src/interlang/translit.py`), scored against attested
  adaptations in 18 languages. Run as the two-arm sensitivity analysis §7.4 asked for
  (v0 costs and learned costs agree on the ranking), with syllable inflation reported
  alongside as the non-metric counterweight.
  **Resolved §3.6:** the syllable template is FIRM as (C)V(N) plus the ten Cr/Cl onset
  clusters, with a support vowel for illegal word-final consonants (/u/ after a
  labial, /i/ elsewhere).
- **Grammar sources audited** — done, [`notes/grammar-plan.md`](notes/grammar-plan.md).
  WALS, Grambank and APiCS checked for coverage and bias before any of them is
  quoted. Grambank is 4.7x denser than WALS and covers the big languages WALS
  misses; APiCS is 80% Western-European-lexifier, leaving 14 independent
  non-European-lexifier languages as the real sample behind any creole universal.
  Carries the grammar agenda and the two creole evidence rules.
- **Grammar Tier 0** — done, [`notes/grammar-tier0.md`](notes/grammar-tier0.md).
  Head-directionality and morphological type, from creole convergence (Rule 1) and
  creole-vs-lexifier divergence (Rule 2). **SVO, prepositions, no case marking** are
  FIRM. Two findings worth the click: head-directionality is *not* one parameter —
  creoles converge above the noun phrase and split 8:7 inside it — and creoles lose
  derivational affixes 35:3 while *gaining* compounding and reduplication 13:2.
- **Grammar Tier 2 Q6 (TAM)** — done, [`notes/grammar-tier2-tam.md`](notes/grammar-tier2-tam.md).
  **Decision: there is no TAM grammar** — tense, aspect and mood are open-class adverbs, and
  this is flagged as a **taste-based choice that overrides the study's own finding** (the
  evidence supports two aspect particles in a preverbal slot). The study itself is the more
  reusable part: contact evidence is now stratified **restricted pidgin / expanded pidgin /
  creole**, because *pidgins*, not creoles, are the closest analogue to an auxiliary language
  — adults, no shared language, no native speakers. TAM elaboration grows monotonically along
  that gradient, which ranks the categories by necessity: imperfective, then past, then
  nothing else.
- **Grammar Tier 2 Q11 + Q7 (noun phrase)** — done,
  [`notes/grammar-tier2-np.md`](notes/grammar-tier2-np.md). **One rule: single-word
  modifiers precede their head, clausal modifiers follow** — which also settles adverb
  placement, since modifiers behave the same way whatever they modify. Tier 0's three
  "coin flips" were a pooling artefact: stratified, restricted pidgins put the modifier
  first on all four, and the new harmony test finds 67% of 1,297 languages put adjective,
  numeral and demonstrative on the same side — **91% of the L1 mass**. The noun itself
  carries almost nothing: no articles (demonstrative and 'one' do the work), optional
  number, no classifiers.
- **Next:** the rest of Tier 2 of the grammar agenda. Phonology and phonotactics are closed (`notes/principles.md`
  §3.3–§3.7). The one piece of unfinished phonology business is lexicon-facing rather
  than sound-facing: §3.3's segment discouragement and §3.6's onset-cluster cost are
  ordinal rankings that must become numeric penalties before the lexicon optimizer runs.

## Layout

```
notes/          decisions, study write-ups, data audit   <- read these first
src/interlang/  library code (metric.py = recognizability v0)
scripts/        one study or fetch per file; docstring documents its policies
data/raw/       third-party datasets (gitignored, re-fetchable — see below)
data/processed/ everything we constructed (committed)
```

## Setup

Requires [uv](https://docs.astral.sh/uv/) and Python 3.13.

```bash
uv sync
```

## Data

`data/raw/` is **gitignored and not preserved** — all of it is public and re-fetchable,
and routine upstream updates are fine (numbers may drift slightly on re-run; the
studies were run 2026-07-14 against the versions noted below). Everything joins on
**Glottocode**, usually alongside ISO 639-3.

| Path under `data/raw/` | Source | Version used | How to get it |
|---|---|---|---|
| `phoible/` | [cldf-datasets/phoible](https://github.com/cldf-datasets/phoible) | commit `5c477f1` | `git clone --depth 1 https://github.com/cldf-datasets/phoible` |
| `asjp/` | [lexibank/asjp](https://github.com/lexibank/asjp) | v21 (`0127953`) | `git clone --depth 1 https://github.com/lexibank/asjp` |
| `wold/` | [lexibank/wold](https://github.com/lexibank/wold) | commit `0df955a` | `git clone --depth 1 https://github.com/lexibank/wold` |
| `glottolog-cldf/` | [glottolog/glottolog-cldf](https://github.com/glottolog/glottolog-cldf) | 5.3 (`072ca0d`) | `git clone --depth 1 https://github.com/glottolog/glottolog-cldf` |
| `wals/` | [cldf-datasets/wals](https://github.com/cldf-datasets/wals) | 2020.3 (`f97440d`), fetched 2026-08-05 | `git clone --depth 1 https://github.com/cldf-datasets/wals` |
| `cldr_supplementalData.xml` | [unicode-org/cldr](https://github.com/unicode-org/cldr) | `main`, fetched 2026-07-14 | `curl -sSL -o data/raw/cldr_supplementalData.xml https://raw.githubusercontent.com/unicode-org/cldr/main/common/supplemental/supplementalData.xml` |
| `cldr/` | [unicode-org/cldr](https://github.com/unicode-org/cldr) | `main` (`9fcd511`), fetched 2026-08-05 | `git clone --depth 1 --filter=blob:none --sparse https://github.com/unicode-org/cldr data/raw/cldr && git -C data/raw/cldr sparse-checkout set common/main` |
| `wikidata_l1/p1098_raw.json`, `iso639/iso-639-3.tab` | Wikidata SPARQL (P1098), SIL | fetched 2026-07-14 | `uv run python scripts/fetch_l1_speakers.py` (downloads both) |
| `wikipedia_langlinks/*.json` | [en.wikipedia.org langlinks API](https://en.wikipedia.org/w/api.php) — one file per concept, giving that article's title in every language | fetched 2026-08-05 | `uv run python scripts/international_vocab.py` (fetches on first run; `--offline` reuses the cache) |
| `grambank/` | [grambank/grambank](https://github.com/grambank/grambank) | `main`, fetched 2026-08-05 | `git clone --depth 1 https://github.com/grambank/grambank data/raw/grambank` |
| `apics/` | [cldf-datasets/apics](https://github.com/cldf-datasets/apics) | `main`, fetched 2026-08-05 | `git clone --depth 1 https://github.com/cldf-datasets/apics data/raw/apics` |
| `iso639/language-codes-full.csv` | [datasets/language-codes](https://github.com/datasets/language-codes) | `main`, fetched 2026-08-05 | `curl -sSL --create-dirs -o data/raw/iso639/language-codes-full.csv https://raw.githubusercontent.com/datasets/language-codes/main/data/language-codes-full.csv` |

`language-codes-full.csv` is only a **fallback** for the ISO 639-1 ↔ 639-3 map that
`iso-639-3.tab` normally provides: `iso639-3.sil.org` is not always reachable, and
`src/interlang/populations.py` accepts either table. Prefer the SIL one when you can
get it (it also carries the macrolanguage `Scope` column).

Clone the five CLDF repos into `data/raw/` under the directory names in the first
column. Only their `cldf/*.csv` files are read, so shallow clones suffice (~300 MB
total). The `cldr/` clone is separate and only `common/main/*.xml` is read
(per-locale quotation marks and number formats), hence the sparse checkout. What each
dataset is for, its row counts, and its caveats:
[`notes/data-audit.md`](notes/data-audit.md).

### What we constructed (committed, in `data/processed/`)

| File | Built by | Contents |
|---|---|---|
| `l1_speakers.csv` | `scripts/fetch_l1_speakers.py` | 1,858 languages × L1 speaker counts from Wikidata P1098, with the documented statement-selection policy and the phantom-MSA override (`L1_OVERRIDES`) applied |
| `phoneme_prevalence.csv` | `scripts/phoneme_prevalence.py` | every PHOIBLE segment × prevalence by languages / L1 speakers / total speakers, at `strict` and `lumped` symbol granularity, with top allophones |
| `contrast_costs.csv` | `scripts/contrast_study.py` | candidate contrasts × share of languages and people whose native phonology distinguishes them, plus attested merger counts — the functional-load penalty matrix |
| `stress_prevalence.csv`, `stress_by_language.csv` | `scripts/stress_prevalence.py` | broad word-stress rule categories × share of languages / L1 speakers / total speakers, under two classification schemes and three tone-language policies, plus the per-language audit trail |
| `international_vocab.csv`, `international_vocab_forms.csv` | `scripts/international_vocab.py` | 52 international words × 6 syllable-template variants × 2 final-coda policies — rendered form, syllable counts before/after, length inflation, recognizability against attested adaptations; plus the 828 attested renderings in 18 languages with their loan/calque classification and provenance |
| `punctuation_survey.csv` | `scripts/punctuation_survey.py` | punctuation / capitalization / spacing / number-format conventions × total-speaker prevalence, each row marked ASCII-available or not and CLDR-derived (`source=cldr`) or knowledge-assembled (`source=knowledge`) |

## Reproducing

Fetch the raw data as above, then run, in order:

```bash
uv run python scripts/fetch_l1_speakers.py     # -> data/processed/l1_speakers.csv
                                               #    (--offline rebuilds from cached raw)
uv run python scripts/phoneme_prevalence.py    # -> data/processed/phoneme_prevalence.csv
uv run python scripts/contrast_study.py        # -> data/processed/contrast_costs.csv
uv run python scripts/stress_prevalence.py     # -> data/processed/stress_prevalence.csv
                                               #    + stress_by_language.csv
uv run python scripts/punctuation_survey.py    # -> data/processed/punctuation_survey.csv
uv run python scripts/international_vocab.py   # -> data/processed/international_vocab.csv
                                               #    + international_vocab_forms.csv
                                               #    (fetches Wikipedia langlinks on first
                                               #    run; --offline reuses the cache)
uv run python scripts/grammar_sources.py       # -> data/processed/grammar_source_coverage.csv
                                               #    + apics_lexifiers.csv
uv run python scripts/grammar_tier0.py         # -> data/processed/grammar_tier0_order.csv
                                               #    + grammar_tier0_morphology.csv
uv run python scripts/grammar_tier2_tam.py     # -> data/processed/grammar_tier2_tam.csv
```

Each script's module docstring documents its inputs, outputs, and the judgment calls
baked into it; the matching write-up in `notes/` interprets the results.
