# Tier 0: head-directionality and morphological type

*Study run 2026-08-05. Script: [`../scripts/grammar_tier0.py`](../scripts/grammar_tier0.py) ·
sources audited first in [`grammar-plan.md`](grammar-plan.md) §3 ·
outputs: `data/processed/grammar_tier0_order.csv`, `data/processed/grammar_tier0_morphology.csv`.
Decides [`principles.md`](principles.md) §3.2.*

**The two questions.** (1) Is the language head-initial — and does "head-directionality"
behave as a single parameter at all? (2) How isolating? Specifically, Patrick's question:
**when creoles differ from their lexifier, do they gain derivational affixes or lose
them?**

**Bottom line up front.** Head-directionality is **not one parameter**: creoles converge
hard on clause-level order and relative-clause position, lean on adpositions, and split
evenly on every noun-phrase-internal modifier. And creoles **lose** derivational affixes
and **essentially never gain them** — 35 losses against 3 gains — while *gaining*
compounding and reduplication in their place. Word-building by compounding rather than
affixation is the creole answer.

---

## 1. Head-directionality is not one parameter

For each order, the creole distribution among **non-European-lexifier** languages (Rule 1
— the only creole evidence that is not contaminated by inheritance), with the WALS world
distribution alongside. `n` for the creole column is 14–16; it is small and every claim
below is bounded by it.

| order | non-European-lexifier creoles | verdict | WALS by language / by L1 |
|---|---|---|---|
| **subject/object/verb** | **SVO 13**, SOV 2, OSV 1 | **converges (81%)** | SOV 40.9% / 35.6% · SVO 35.8% / **59.2%** |
| **relative clause & noun** | **N-Rel 12**, Rel-N 2, correlative 1 | **converges (80%)** | N-Rel 70.4% / 50.4% |
| adposition & NP | **Prep 11**, Postp 4 | leans (73%) | Postp 48.6% / 30.1% · Prep 43.3% / 48.8% |
| demonstrative & noun | N-Dem 9, Dem-N 5 | leans (64%) | N-Dem 46.0% / 9.8% · Dem-N 44.3% / **86.1%** |
| possessor & possessum | Possessum-first 8, Possessor-first 7 | **split** | Gen-N 54.6% / 50.0% |
| adjective & noun | Adj-N 8, N-Adj 7 | **split** | N-Adj 64.6% / 33.8% · Adj-N 27.0% / **65.3%** |
| numeral & noun | N-Num 8, Num-N 7 | **split** | N-Num 52.7% / 7.1% · Num-N 41.5% / **89.5%** |

**The clause converges; the noun phrase does not.** Everything above the NP — the order of
subject, object and verb, the position of the relative clause, and (more weakly) the
adposition — has a creole answer, and it is head-initial every time. Every modifier
*inside* the NP is a coin flip: 8–7, 8–7, 8–7, three times over. That is not weak
evidence of a trend, it is clean evidence of *no* trend.

This matters because it falsifies the premise the agenda was built on. Fixing one
head-directionality parameter was supposed to make a dozen later decisions fall out as
consequences. It buys the clause skeleton and nothing else; **NP-internal order has to be
decided on separate grounds**, and it should be moved out of Tier 0 and into its own Tier 2
question.

### 1.1 Rule 2 fires on the constituent-order question, and it points the same way

Three non-European-lexifier creoles **diverge from their own lexifier's order**, all in the
same direction:

| creole | lexifier order | creole order |
|---|---|---|
| Pidgin Hindustani | Hindi **SOV** | **SVO** |
| Pidgin Hawaiian | Hawaiian **VSO** | **SVO** |
| Chinuk Wawa | Chinookan (not SVO) | **SVO** |

The order was available in the input and adults moved off it. This is Rule 2 in its
positive form and it is the strongest single piece of evidence in the study.

### 1.2 Where language-counts and people-counts disagree, and it is not close

The WALS column above carries two percentages for a reason. On **numeral & noun** the
by-language majority is N-Num (52.7%) and the by-L1 majority is Num-N (**89.5%**) — a
37-point reversal. **Demonstratives** reverse by 42 points, **adjectives** by 31.
[`principles.md`](principles.md) §2 says count people, so the people-weighted answer wins
where we have to choose; but note that for demonstratives the (weak) creole lean and the
people-weighted answer point in **opposite** directions. That conflict is logged, not
resolved, and belongs to the NP-order question in Tier 2.

---

## 2. Morphological type: creoles lose derivation and never gain it

### 2.1 The design — the cleanest Rule 2 test in the project

Rule 2 usually needs hand-supplied lexifier values, because APiCS does not contain
lexifiers. Here it does not: **14 APiCS contact languages are also in Grambank, and so are
their lexifiers.** Both sides are scored on the same feature definitions by the same
project, so no value on either side is hand-coded. Each (creole, feature) cell is:

| verdict | meaning |
|---|---|
| **LOST** | lexifier has it, creole does not — the learnability signal |
| KEPT | both have it |
| **GAINED** | creole has it, lexifier does not |
| ABSENT | neither — uninformative |

`?` on either side is dropped rather than read as 0. The 14 pairs are 8 European-lexifier
(English ×6, French, Dutch) and 6 non-European (Standard Malay ×3, Standard Arabic ×2,
Bobangi). Judgment calls in the script docstring; the two that matter are that Sudanese
Arabic is absent from Grambank so the Arabic creoles are paired with Standard Arabic, and
that Berbice Dutch's Eastern Ijo substrate is not in Grambank so only half its input is
represented.

### 2.2 The answer

| block | LOST | KEPT | GAINED | of informative cells |
|---|---|---|---|---|
| **derivation** (nominalisation, agent/object noun, diminutive, augmentative, causative, transitiviser) | **35** | 19 | **3** | LOST 61%, KEPT 33%, **GAINED 5%** |
| inflection (case, agreement, tense, aspect, plural, passive) | 46 | 29 | 7 | LOST 56%, KEPT 35%, GAINED 9% |
| **periphrasis** (verb compounding, reduplication) | 2 | 5 | **13** | LOST 10%, KEPT 25%, **GAINED 65%** |

**Derivational affixes go out and compounding and reduplication come in.** The two blocks
are near mirror images. Nothing in the study is as lopsided as *verb compounding*, which is
GAINED 3 / LOST 0, and *verb reduplication*, GAINED 7 / KEPT 3 / LOST 0.

The single most robust number here is **GAINED 3 of 57**. Whatever else is true, **adults
building a language under time pressure do not invent derivational affixation.**

### 2.3 The Rule 1 check — and it does not fully pass

Splitting the same cells by lexifier family, as [`grammar-plan.md`](grammar-plan.md) §2
requires:

| block | European-lexifier LOST:KEPT | non-European LOST:KEPT |
|---|---|---|
| derivation | **27 : 8** | **8 : 11** |
| inflection | **30 : 7** | 16 : 22 |
| periphrasis (GAINED) | 6 gained, 0 lost | 7 gained, 2 lost |

**"Creoles lose derivation" is strong for European-lexifier creoles and unproven across
lexifier families.** The non-European group goes the other way. Reporting that honestly
matters more than the conclusion, so: per creole,

| creole | lexifier | LOST | KEPT | GAINED |
|---|---|---|---|---|
| San Andres Creole English | English | 6 | 0 | 0 |
| Bislama | English | 5 | 1 | 0 |
| Berbice Creole Dutch | Dutch | 4 | 0 | 0 |
| Jamaican Creole English | English | 4 | 2 | 0 |
| Tok Pisin | English | 4 | 1 | 1 |
| Ambonese Malay | Standard Malay | 4 | 0 | 1 |
| Baba Malay | Standard Malay | 3 | 1 | 0 |
| Saramaccan | English | 3 | 3 | 0 |
| Haitian | French | 1 | 1 | 0 |
| Nubi | Standard Arabic | 1 | 2 | 0 |
| Sri Lanka Malay | Standard Malay | 0 | 3 | 1 |
| Kinshasa Lingala | Bobangi | 0 | **5** | 0 |
| South Sudanese Creole Arabic | Standard Arabic | 0 | 0 | 0 |

The non-European group's two "keep everything" cases are the two that are least
restructured: **Kinshasa Lingala** differs from Bobangi far less than a plantation creole
differs from English — it is a creolised Bantu language whose lexifier is typologically
identical to it — and **Sri Lanka Malay** is the textbook case of a contact language
converging *toward* an agglutinative substrate (Tamil and Sinhala), so it gained morphology
rather than shedding it. The Malay creoles that did restructure, Ambonese and Baba, lose 4:0
and 3:1.

That reading is defensible but it is post-hoc, so the honest summary is the two-part one:

1. **"Creoles do not gain derivational affixes" survives Rule 1** — 1 gain in the European
   group, 2 in the non-European, 3 of 57 cells overall. This is the robust finding.
2. **"Creoles lose derivational affixes" does not survive Rule 1** on this sample. It is
   strong where the lexifier is European and morphologically rich, absent where the
   lexifier is Bantu or where the substrate is agglutinative.

Since we are *designing* rather than predicting, (1) is the operative one: we have no
positive evidence that derivational affixation is something adult learners reach for, and
substantial evidence that compounding and reduplication are.

### 2.4 The world for scale (WALS, and the n is small)

| chapter | n | headline by language | by L1 |
|---|---|---|---|
| 20A fusion of inflectional formatives | **164** | exclusively concatenative 75.6% | 62.3% (exclusively isolating just 5.1%) |
| 22A inflectional synthesis of the verb | **144** | 4–5 categories per word 35.4% | 2–3 categories 28.7% (43.1% by total speakers) |
| 26A prefixing vs suffixing | 958 | strongly suffixing 41.6% | **84.4%** |

Two things worth carrying forward. **Fully isolating is rare in the world** — 5.1% of L1 —
so an isolating design is a deliberate learnability choice, not the typological default,
and should be justified as such rather than assumed. And **if we ever do adopt an affix,
it should be a suffix**: 84.4% of L1 speakers have a strongly-suffixing native language,
the largest margin anywhere in this study.

---

## 3. What this decides

**Locked by Patrick, 2026-08-05** (evidence §1): **SVO**, **prepositions**, **no case
marking on core arguments**. Head-initial where the creole evidence converges.

**Recommended, pending discussion (§2):**

- **No derivational affixes.** Build words by **compounding** — already FIRM in §3.6 — and,
  optionally, reduplication. Nothing in the creole record suggests adults reach for
  affixation; the record positively suggests the opposite substitute.
- **Reduplication is worth considering as a real morphological device**, not a curiosity:
  it is the single most-gained feature in the study (verbs 7 gained / 0 lost). It costs
  nothing phonologically — our syllable template already permits it — and it is the one
  word-formation process creoles *add*. Candidate uses: plurality, intensity, iterativity.
- **If an affix is ever adopted, it is a suffix** (84.4% of L1 speakers).

**Moved out of Tier 0:** noun-phrase-internal order (adjective, numeral, demonstrative,
possessor) has no creole signal and its people-weighted answer conflicts with the weak
creole lean on demonstratives. It becomes its own Tier 2 question.

---

## 4. Honest limits

- **n = 14 paired languages, 6 of them non-European-lexifier.** Every conclusion in §2 is
  bounded by that. The Rule 1 split has 6 languages on one side.
- **Grambank binaries flatten real distinctions.** "Is there a productive pattern for
  deriving an agent noun from a verb?" is one bit; it cannot distinguish a single fossilised
  suffix from a fully productive system, and *productive* is doing a lot of work in the
  coding.
- **The creole/lexifier pairing is a simplification.** A creole's input is a lexifier *and*
  one or more substrates; only the lexifier side is modelled here. Where the substrate is
  morphologically rich (Sri Lanka Malay, Berbice Dutch), "LOST relative to the lexifier"
  can coexist with "gained relative to the substrate".
- **Standard Arabic is the wrong comparison** for Nubi and Juba Arabic — they descend from
  Sudanese colloquial Arabic, which Grambank lacks. Arabic's templatic morphology is also
  the case Grambank's affix-shaped questions fit worst.
