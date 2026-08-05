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

**Tier 0 — DONE 2026-08-05** → [`grammar-tier0.md`](grammar-tier0.md). SVO, prepositions and
no case marking are FIRM; morphological type is SOFT (no derivational affixes, compounding
and possibly reduplication instead). One structural surprise: **head-directionality is not a
single parameter** — creoles converge above the noun phrase and split evenly inside it — so
NP-internal order moves to Tier 2 rather than falling out here.
1. **How much morphology at all.** §3.2's "isolating" is a package: unwrap it into
   morphemes-per-word, presence of inflection, and presence of agreement, and decide each.
   Compounding is already FIRM (§3.6), so we are not strictly isolating.
2. **Head-directionality.** Fix it and adposition type, genitive order, relative-clause
   position, comparative and auxiliary order stop being separate decisions. Consistency is
   itself a learnability asset.

**Tier 1 — the clause skeleton.** 3. ~~basic constituent order~~ **done, SVO** ·
4. ~~alignment~~ **deferred indefinitely** (Patrick, 2026-08-05): with no case marking and
no verbal agreement there is no morphology left to carry an alignment contrast, so the
question is moot until something is adopted that makes it relevant — a passive, an
agent-marking oblique, or case forms of pronouns (Tier 2 Q9e is the live route back in) ·
5. ~~whether core arguments are marked at all~~ **done, no case marking**.

**Tier 2 — what every clause must carry.** Expanded 2026-08-05; suggested working order
is 6 → 7 → 8+11 together → 9 → 10, because negation needs the TAM slot, and the article,
demonstrative and numeral questions compete for the same real estate as NP order.

| # | question | sub-questions | evidence to hand |
|---|---|---|---|
| **6** | ~~**TAM**~~ **DONE** → [`grammar-tier2-tam.md`](grammar-tier2-tam.md): **no TAM grammar** — tense, aspect and mood are open-class adverbs. A taste-based choice that overrides the study; particle bill 0 | tense at all? which distinctions? aspect set? mood/irrealis? obligatory or optional? pre- or postverbal? fixed order among multiple markers? | APiCS 43 (position rel. to verb), 44 (internal order), 49 (TA systems), 50 (interaction with negation); Grambank GB082–086, GB312 |
| 7 | ~~**nominal categories**~~ **DONE** → [`grammar-tier2-np.md`](grammar-tier2-np.md): no articles, no classifiers, optional number | obligatory plural? articles — definite, indefinite, both, neither? classifiers/measure words? what a bare noun means by default | APiCS 28, 29, 9, 10, 31; Grambank GB020–023, GB042, GB044. Articles are Euro-coded → run the Rule 2 contrapositive |
| 8 | **pronoun system** | person/number; clusivity; gender; politeness; **case forms of pronouns**; total form count | APiCS 13, 15, 18; Grambank GB071, GB090–094. Gender and clusivity already answered in the Tier 0 side-evidence; politeness is genuinely split |
| 9 | **negation** | one negator or several? position rel. to verb and to TAM? double negation? negative concord? same negator for verbal, locational, existential and nominal predication? | APiCS 50; Grambank GB107, GB140 |
| 10 | **question formation** | polar: particle, intonation, word order or tag? particle position? content: in-situ or fronted? | APiCS 12; Grambank GB260, GB262, GB285, GB286; WALS 92A, 93A |
| **11a** | ~~**adverb placement**~~ **DONE** — answered by Q11's modifier rule: adverbs precede the verb | where adverbs sit relative to verb and object; whether TAM adverbs have a preferred position; scope when two or more stack | now load-bearing: with TAM fully lexical, adverb placement *is* the TAM syntax |
| **11** | ~~**NP-internal order**~~ **DONE** → [`grammar-tier2-np.md`](grammar-tier2-np.md): modifiers precede, clauses follow | adjective, numeral, demonstrative, possessor — each relative to the noun | moved down from Tier 0: creoles split 8:7 three times, and the people-weighted world answer conflicts with the creole lean on demonstratives ([`grammar-tier0.md`](grammar-tier0.md) §1.2) |

**Tier 2 is where the particle inventory gets sized, even though it is chosen in Tier 4.**
Every answer of the form "mark it with a particle" adds a short, high-frequency word that
Tier 4 has to find phonological room for, under §3.3's segment discouragement and §3.6's
cluster cost. Each Tier 2 write-up should therefore end with a running count: *how many
particles does this decision cost?*

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
4. **Stratify by contact type, and read the pidgin columns first** (added 2026-08-05,
   corrected the same day). We are designing an **auxiliary** language — nobody's first
   language, built by adults with no language in common. **That is what a pidgin is**; a
   creole is what happens once children nativise one. So pidgins are not a contaminant in
   the creole sample, they are the closest analogue to the use case, and **where pidgins and
   creoles disagree the pidgin evidence wins**. Report restricted pidgin / expanded pidgin /
   creole separately. *Expanded pidgins are usually the right target*: still adult-built, but
   carrying a full communicative load, which is what an auxiliary language must do —
   restricted pidgins tell us what is indispensable, not what is sufficient. A useful side
   effect: the pidgin strata are ~50/50 European and non-European lexifier against 95/5 for
   the creoles, so the stratum we care about most is also the least contaminated by
   inheritance. → [`grammar-tier2-tam.md`](grammar-tier2-tam.md) §0.
4. **Any Euro-coded feature we keep gets the Rule 2 contrapositive run on it** before it
   is tagged FIRM.
5. **Hand-supplied lexifier values are flagged**, like `model-recall` in the vocabulary
   study, and never enter a headline number unflagged.
6. **The contact record is evidence about what EMERGES, not about what is LEARNABLE when
   taught** (added 2026-08-05, when the Q6 decision first leaned on the distinction). Those
   coincide for most features and come apart for *optional* ones: an obligatory category has
   to justify itself against "would adults build this?", but an optional, explicitly taught
   one need not — Esperanto carries categories no creole ever built and is demonstrably
   learnable. **This is a licence to depart from the creole/pidgin record, not to ignore it:
   any departure gets recorded as a taste-based choice with its costs listed**, as Q6 is.
