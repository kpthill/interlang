# Grammar: the plan, the sources, and what each source may be asked

*Written 2026-08-05, opening the grammar phase. Source audit:
[`../scripts/grammar_sources.py`](../scripts/grammar_sources.py) →
`data/processed/grammar_source_coverage.csv`, `data/processed/apics_lexifiers.csv`.
Companion: [`principles.md`](principles.md) §3.2 (grammar is hand-designed from
typology), §2 (the two objectives).*

Phonology and phonotactics closed on 2026-08-05 ([`principles.md`](principles.md)
§3.3–§3.7). This document is the equivalent of §3's structure for grammar: what we are
deciding, in what order, against what evidence, and — first — what the evidence can
actually support.

---

## 1. The objective is different here, and that changes the method

For vocabulary, §2's two objectives both work: *ease* is "how many people recognise this
word" and *representation* is "whose languages did the lexicon draw on". **For grammar
only the first survives.** You cannot source 3% of your syntax from Bantu the way you can
source 3% of your lexicon; there is no grammatical analogue of an etymology.

Position taken (Patrick, 2026-08-05): **representation is a vocabulary-stage objective.
Grammar is optimised for learnability alone**, and the fairness question is handled by
*auditing the result* — at the end, report how the chosen feature bundle clusters
genealogically and areally, the same way [`international-vocab.md`](international-vocab.md)
§6.2 reports the recipient split. "This grammar is 90% Standard Average European with a
Mandarin TAM system" should be a measured statement we publish, not a bias we absorb.

That makes **creoles the north star**, not typological frequency. Typological frequency
measures what languages *are*; creoles measure what adults *converge on under time
pressure*, which is the actual objective. Grambank and WALS are the check that we have not
mistaken a European default for a universal — a tiebreaker and a bias control, not a
source of answers.

---

## 2. The two creole rules (**FIRM**, agreed 2026-08-05)

Creole evidence is not free of confounds. 80% of APiCS has a Western-European lexifier, so
"creoles agree" can just mean "European languages agree, and their creoles inherited it".
Two rules make the evidence usable, and they are complementary — one licenses a claim, the
other licenses it differently:

**RULE 1 — cross-lexifier convergence.** A creole feature counts as evidence of
learnability where creoles converge **across lexifier families**. Agreement confined to
English/French/Spanish/Portuguese/Dutch creoles is indistinguishable from inheritance and
proves nothing.

**RULE 2 — divergence from the lexifier.** Where creoles **differ from their own
lexifier**, that is strong evidence *even within one lexifier family*, because inheritance
is exactly what it rules out: the feature was available in the input and adults dropped it
anyway (Patrick's addition, 2026-08-05). Grammatical gender is the model case.

Rule 2 also has a **contrapositive that is the more useful tool in practice**: it is the
sanity check on any Euro-coded feature we are minded to *keep*. If we are about to adopt
something European, ask whether European-lexifier creoles kept it. If even they dropped
it, we should not be adopting it.

*In practice Rule 2's positive form will rarely add a decision Rule 1 did not already
make — the two agree on every case tested so far. It earns its place as the check on
retention, not as an independent generator of answers.*

---

## 3. What the audit found — the constraint on all of it

`scripts/grammar_sources.py`, run 2026-08-05. Everything is deduplicated on Glottocode
first (WALS is doculect-level: 11 Basque varieties, 10 Arabic), Grambank dialects and
family-level entries are dropped, and `?` never counts as coverage.

| source | languages | features | density | median feature covers |
|---|---|---|---|---|
| WALS | 2,502 | 192 | 0.16 | 52.0% of world L1 |
| Grambank | 2,393 | 195 | **0.75** | **62.4%** of world L1 |
| APiCS | 104 lects / 69 languages | 336 | 0.90 | 0.8% of world L1 |

### 3.1 Grambank is dramatically better where they overlap

The density difference is the whole story: **0.75 vs 0.16**. Grambank was built to be
filled in; WALS was built chapter by chapter by different authors with different samples.

The consequence shows up exactly where it hurts. Taking the 20 largest languages by L1 and
the features Tier 0/1 rests on:

- **Grambank: 16 of 20 have every spotlight feature, 0 of 20 have none.**
- **WALS: 6 of 20 have all of them, and 3 of 20 have none at all** — including
  **Mandarin (918M), Wu (81M) and German**, which are simply absent from the
  word-order and morphology chapters we would most want them in.

This is the same population-correlated sparsity that flipped the stress conclusion
([`stress-prevalence.md`](stress-prevalence.md)); it has not gone away, and it is worse in
the morphology chapters than the word-order ones. **Revised division of labour:** use
**Grambank as the default source**, and treat WALS as the supplement for features Grambank
does not code — the reverse of what §3.2 originally assumed.

### 3.2 WALS's morphology chapters are too thin to carry a decision alone

| WALS chapter | languages | % of world L1 |
|---|---|---|
| 81A order of S, O, V | 1,346 | 78.9 |
| 87A adjective and noun | 1,336 | 73.7 |
| 85A adposition and NP | 1,162 | 72.1 |
| 26A prefixing vs suffixing | 958 | 70.0 |
| 30A number of genders | 257 | **52.8** |
| 49A number of cases | 259 | **52.7** |
| 98A alignment of case marking | 189 | **49.9** |
| 22A inflectional synthesis of the verb | 144 | **47.8** |
| 20A fusion of inflectional formatives | 164 | **47.6** |

The word-order chapters are usable. **The morphological-typology chapters — the ones that
would answer "how isolating should we be?" — cover under half of humanity and 144–164
languages.** Any claim from 20A/22A must be quoted with its n.

### 3.3 APiCS: the confound, measured

| lexifier group | lects | independent languages |
|---|---|---|
| Western European (English 33, Portuguese 21, French 17, Spanish 7, Dutch 3, Russian 2) | 83 (80%) | 53 |
| non-European (Arabic 4, Bantu 3, Malay 3, + 9 others: Ngbandi, Chinookan, Hawaiian, Hindi, Lower Sepik, Eskimo-Aleut, Bantu/Cushitic) | 19 | **14** |
| mixed (Michif, Gurindji Kriol) | 2 | 2 |

**14 independent non-European-lexifier languages is the real sample size behind any claim
of a creole universal under Rule 1.** That is small, and every claim in the grammar
write-ups must quote it rather than the headline 104. Rule 2 is limited differently: only
48 of 336 APiCS parameters carry a WALS_ID, and the lexifier's own value has to be
supplied from outside APiCS — so Rule 2 comparisons are hand-assembled per feature and
must be flagged as such (the `model-recall` provenance convention from
[`international-vocab.md`](international-vocab.md) §3.3 applies).

**Population weighting is meaningless for APiCS** (0.8% of world L1) and it is not a
defect: creoles are evidence about *learning*, not about *how many people we please*. Do
not weight them by speakers.

### 3.4 One bug worth recording

Grambank carries **no ISO 639-3 codes at all** — it is Glottocode-only. The CLDR
total-speaker table is keyed by ISO, so the naive join silently produces zero
total-speaker coverage for every Grambank feature. `grammar_sources.py` builds a
Glottocode→ISO map from `l1_speakers.csv` first. Any future script touching Grambank needs
the same bridge.

---

## 4. The agenda

Ordered by **how much would have to be redone if this decision flipped**, not by the order
a descriptive grammar presents things in. The coverage checklist is the **Lingua
Descriptive Studies Questionnaire** (Comrie & Smith 1977, *Lingua* 42:1–72, open via
[TulQuest](https://tulquest.huma-num.fr/en/node/47)) — chosen because it is the template
behind the Routledge *Descriptive Grammars* series, so its section numbers are a citation
scheme shared with dozens of published reference grammars. But it is a *documentation*
instrument, ordered for completeness, so we work it in the order below and use it only to
check that nothing was left undecided.

**Tier 0 — decided together, first. Everything downstream inherits these.**
1. **How much morphology at all.** §3.2's "isolating" is a package: unwrap it into
   morphemes-per-word, presence of inflection, and presence of agreement, and decide each.
   Compounding is already FIRM (§3.6), so we are not strictly isolating.
2. **Head-directionality.** Fix it and adposition type, genitive order, relative-clause
   position, comparative and auxiliary order stop being separate decisions. Consistency is
   itself a learnability asset.

**Tier 1 — the clause skeleton.** 3. basic constituent order · 4. alignment ·
5. whether core arguments are marked at all.

**Tier 2 — what every clause must carry.** 6. TAM (including whether tense exists at
all) · 7. nominal categories: number, definiteness, classifiers · 8. the pronoun system ·
9. negation · 10. question formation.

**Tier 3 — combination.** relative clauses · complement clauses · adverbial clauses ·
coordination · comparatives · copula, possession and existentials.

**Tier 4 — the lexicon interface, deliberately last.** word classes and how rigid they
are · derivational machinery · **the particle inventory**, which is the coupling back to
phonology (§3.2) and what finally closes the deferred root-shape bounds (§3.6): short-word
space cannot be reserved until we know how many short words the grammar demands.

---

## 5. Standing rules for every grammar decision

1. **Quote the n and the coverage**, never a bare percentage. Both sources are sparse in
   population-correlated ways.
2. **Report by-language *and* by-speaker counts** where they differ, and say which one the
   decision used. They disagree on the very first Tier 1 question.
3. **Creole claims cite the non-European-lexifier count** (max 14), not the APiCS total.
4. **Any Euro-coded feature we keep gets the Rule 2 contrapositive run on it** before it
   is tagged FIRM.
5. **Hand-supplied lexifier values are flagged**, like `model-recall` in the vocabulary
   study, and never enter a headline number unflagged.
