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
- **Cost learning from WOLD** — done, [`notes/cost-learning.md`](notes/cost-learning.md).
  Substitution + epenthesis costs fitted jointly to 13,595 attested loanword
  adaptations, cross-validated leave-one-recipient-out over all 41 recipients.
  Learned costs are opt-in (`metric.similarity(..., params=...)`), not the default.
- **Next:** projection-distortion experiment across syllable templates, run as a
  two-arm sensitivity analysis (v0 costs vs learned costs) because the
  permissive-coda bias is reduced but not eliminated.

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
| `cldr_supplementalData.xml` | [unicode-org/cldr](https://github.com/unicode-org/cldr) | `main`, fetched 2026-07-14 | `curl -sSL -o data/raw/cldr_supplementalData.xml https://raw.githubusercontent.com/unicode-org/cldr/main/common/supplemental/supplementalData.xml` |
| `wikidata_l1/p1098_raw.json`, `iso639/iso-639-3.tab` | Wikidata SPARQL (P1098), SIL | fetched 2026-07-14 | `uv run python scripts/fetch_l1_speakers.py` (downloads both) |

Clone the four CLDF repos into `data/raw/` under the directory names in the first
column. Only their `cldf/*.csv` files are read, so shallow clones suffice (~300 MB
total). What each dataset is for, its row counts, and its caveats:
[`notes/data-audit.md`](notes/data-audit.md).

### What we constructed (committed, in `data/processed/`)

| File | Built by | Contents |
|---|---|---|
| `l1_speakers.csv` | `scripts/fetch_l1_speakers.py` | 1,858 languages × L1 speaker counts from Wikidata P1098, with the documented statement-selection policy and the phantom-MSA override (`L1_OVERRIDES`) applied |
| `phoneme_prevalence.csv` | `scripts/phoneme_prevalence.py` | every PHOIBLE segment × prevalence by languages / L1 speakers / total speakers, at `strict` and `lumped` symbol granularity, with top allophones |
| `contrast_costs.csv` | `scripts/contrast_study.py` | candidate contrasts × share of languages and people whose native phonology distinguishes them, plus attested merger counts — the functional-load penalty matrix |

## Reproducing

Fetch the raw data as above, then run, in order:

```bash
uv run python scripts/fetch_l1_speakers.py     # -> data/processed/l1_speakers.csv
                                               #    (--offline rebuilds from cached raw)
uv run python scripts/phoneme_prevalence.py    # -> data/processed/phoneme_prevalence.csv
uv run python scripts/contrast_study.py        # -> data/processed/contrast_costs.csv
```

Each script's module docstring documents its inputs, outputs, and the judgment calls
baked into it; the matching write-up in `notes/` interprets the results.
