# Tier 2 Q6: tense, aspect and mood

*Study run 2026-08-05, **revised the same day** after Patrick corrected the framing (§0).
Script: [`../scripts/grammar_tier2_tam.py`](../scripts/grammar_tier2_tam.py) · output:
`data/processed/grammar_tier2_tam.csv` · agenda: [`grammar-plan.md`](grammar-plan.md) §4 Q6.*

**Bottom line up front.** TAM goes on **free preverbal particles**, marking is **optional**,
and the categories arrive in a strict order of necessity: **imperfective first, past second,
everything else optional or rejected**. Contact languages **never stack three markers** —
0 of 18 pidgins of either kind. Recommended: **two particles, with a third (irrealis) as a
judgment call rather than a finding.**

---

## 0. The framing was wrong the first time

The first version of this study treated pidgins as a contaminant in the creole sample and
reported every number with them excluded. **That was backwards** (Patrick, 2026-08-05):

> We are designing an **auxiliary** language — nobody's first language, built by adults who
> share no language. **That is what a pidgin is.** A creole is what happens once children
> nativise a pidgin: a different process, with a different learner. So pidgins are not noise
> in the creole evidence, they are the closest analogue to the use case, and where the two
> disagree the **pidgin** evidence should win.

Everything below is therefore stratified three ways, hand-classified from standard
creolistics (`model-recall` provenance — it is not in the APiCS data, and the boundary calls
are listed in the script):

| | European lexifier | non-European | total |
|---|---|---|---|
| **restricted pidgin** — no native speakers, limited domains | 4 | 7 | **11** |
| **expanded pidgin** — a community's main language, often nativising | 7 | 7 | **14** |
| creole — nativised | 70 | 4 | 74 |
| *mixed language (excluded — arises in bilingual communities, not from a no-shared-language situation)* | 2 | 1 | 5 |

Note what this does to the Rule 1 problem as a side effect: the pidgin strata are **~50/50**
European and non-European lexifier, against 95/5 for the creoles. The stratum we now care
about most is the one least contaminated by European inheritance.

**Standing rule, updated in [`grammar-plan.md`](grammar-plan.md) §5:** stratify every contact
claim by restricted pidgin / expanded pidgin / creole, and read the pidgin columns first.

---

## 1. The gradient: TAM elaboration grows with nativisation

This is the shape of the whole result. Every feature tells the same story.

| | restricted pidgin | expanded pidgin | creole |
|---|---|---|---|
| **at most one tense/aspect marker** | **6 of 9** | 1 of 9 | 2 of 55 |
| mixed aspectual-temporal system | 1 of 9 | 6 of 9 | 46 of 55 |
| **TAM markers immediately preverbal** | 1 of 9 | **7 of 9** | 36 of 54 (+10 leftward) |
| no TAM markers at all | 3 of 9 | 0 | 0 |
| **three markers stacked and ordered** | **0 of 9** | **0 of 9** | 17 of 51 |

**Restricted pidgins are minimal — 6 of 9 have at most one tense/aspect marker at all, and
3 of 9 have none.** Expanded pidgins have a small preverbal set. Creoles develop the full
mixed system, and only creoles ever stack three markers.

That gradient is the useful thing, because it ranks the categories by *necessity*: what
appears in a restricted pidgin is indispensable, what appears by the expanded-pidgin stage
is what an adult-built language needs to do a full communicative job, and what only appears
in creoles is what nativisation adds.

**Which stratum should we copy?** Restricted pidgins are the purest analogue but they are
*communicatively limited* — not a system anyone would write a technical document in.
**Expanded pidgins are the right target**: still adult-built, but carrying a full
communicative load, which is what an auxiliary language has to do.

---

## 2. The categories, one by one

Patrick's question: which tenses/aspects/moods were considered, and how common is each?

### 2.1 In contact languages — does the category have an overt marker at all?

| category | restricted pidgin | expanded pidgin | creole |
|---|---|---|---|
| **progressive / imperfective** | 4 of 9 (44%) | **9 of 9 (100%)** | 53 of 53 (100%) |
| **past** | 2 of 8 (25%) | 6 of 9 (67%) | 48 of 55 (87%) |
| **habitual** (as a separate marker) | **0 of 9 (0%)** | 9 of 9* | 46 of 55 (84%) |

\* the expanded-pidgin habitual is almost always **the progressive doing double duty** — of
the 9, four are coded "habitual and progressive" (one marker, both functions) and only the
European-lexifier creoles have a dedicated habitual: **"only habitual" is 21 of 59
European-lexifier lects and 0 of 9 outside that group.** A separate habitual particle is an
inherited European trait, not a contact-language one.

**The order of necessity is: imperfective → past → (habitual, only as an extension of the
imperfective).** Nothing else reaches an expanded pidgin at all.

### 2.2 In the world — per category, deduplicated and population-weighted

WALS's 200-language sample (n=220 after dedup) for the four classic categories, Grambank
(n≈1,900–2,200) for the rest:

| category | source | % languages | **% world L1** | % total speakers |
|---|---|---|---|---|
| **perfective/imperfective** | WALS 65A | 45.0 | **65.3** | 54.6 |
| perfective/imperfective | Grambank GB086 | 66.8 | **77.9** | 65.4 |
| **past** | WALS 66A (any) | 60.5 | **67.6** | 71.3 |
| past | Grambank GB083 | 52.4 | 63.9 | 70.4 |
| present | Grambank GB082 | 34.2 | 48.2 | 42.8 |
| **future** | WALS 67A (inflectional) | 49.5 | **39.5** | 33.9 |
| future | Grambank GB084 | 45.5 | 48.9 | 44.0 |
| **the perfect** | WALS 68A (any) | 48.6 | 56.2 | 67.2 |
| mood | Grambank GB312 | 69.6 | 57.4 | 50.9 |
| *remoteness grades on past/future* | WALS 66A / GB309 | 18.2 / 31.8 | 0.9 / 32.2 | 0.7 / 32.4 |

**Aspect is the most-marked category by people in both sources** (65.3% and 77.9% of L1).
Past is close behind. **Future is the weakest of the three** — half the world's languages
have no inflectional future and 60.5% of L1 speakers' languages do not.

The perfect deserves its own line because it is the **trap**: 48.6% of languages have one,
but the possessive-derived kind (English *have eaten*, Romance) is only **3.2% of languages
while being 36.6% of total speakers**. That is the single most Eurocentric-looking number in
the study — a category that looks common because the languages we happen to speak have it.

### 2.3 What an unmarked verb means (APiCS 51) — this is what makes "optional" work

| | restricted pidgin | expanded pidgin | creole |
|---|---|---|---|
| stative → present *and* dynamic → past/perfective, **both unmarked** | 0 of 8 | **7 of 8** | 32 of 53 |
| marked differently | 3 of 8 | 1 of 8 | 19 of 53 |
| has no or only one TAM marker | 5 of 8 | 0 | 1 of 53 |

**7 of 8 expanded pidgins get both readings from a bare verb.** The contact-language default
is that an unmarked verb means *present* for a stative and *past/perfective* for a dynamic —
which is precisely why the marker inventory can stay tiny: the commonest readings are free.

---

## 3. Where the markers go, and what disturbs them

**Preverbal.** 7 of 9 expanded pidgins, 46 of 54 creoles (85%). Restricted pidgins are
silent rather than contradictory — most have nothing to position. Consistent with
head-initial SVO, so nothing is traded.

**Never stack three.** **0 of 9 restricted pidgins and 0 of 9 expanded pidgins** have T, A
and M markers that co-occur and need ordering; 17 of 51 creoles do. The Bickerton
anterior/irrealis/non-punctual *sequence* is a creole development, not an adult-built one —
and it appears in 16 of 56 European-lexifier creoles against 1 of 8 non-European. **We do not
need an ordering rule**, which is one fewer thing to specify and to learn.

**Negation leaves TAM alone.** Zero non-European-lexifier languages change TAM marking under
negation. By stratum: restricted pidgins 4 same / 2 reduced / 0 different; expanded pidgins 6
same / 3 different (all three European-lexifier); creoles 35 same / 8 reduced / 6 different.
Settles the dependency Tier 2 Q9 was waiting on: **negation changes nothing else.**

**Rule 2, morphology vs particles.** Over the 14 creole/lexifier Grambank pairs: TAM
morphology **lost 17, gained 6**; TAM particles **gained 9, lost 2**, with aspect and tense
particles both 4:0. The swap from bound to free marking is confirmed, with the same
limitation as Tier 0 — it is demonstrated where the lexifier had morphology to lose.

---

## 4. Recommendation (revised)

**Two particles, with a third as an open judgment call.**

| | particle | status |
|---|---|---|
| 1 | **imperfective** — progressive *and* habitual in one marker | **strongly supported.** 100% of expanded pidgins and creoles; the one category no contact language does without. The habitual conflation is the non-European pattern (dedicated habitual: 0 of 9 outside Europe, 21 of 59 inside) |
| 2 | **past / anterior** | **supported.** 6 of 9 expanded pidgins, 87% of creoles, 63.9–67.6% of world L1 |
| 3 | *irrealis (future + conditional)* | **judgment call, not a finding.** Mood-by-particle is the world's most common particle strategy (51.1% of L1, 58.1% of total speakers) — but future is the weakest of the three tense categories (39.5% of L1 have an inflectional future), and contact languages commonly express it lexically with a 'go' or 'want' verb rather than a particle |

Supporting decisions, all evidenced above:

- **Preverbal**, immediately before the verb.
- **Optional**, not obligatory. A bare verb is stative-present / dynamic-past-perfective by
  default (§2.3), which is what keeps the inventory this small.
- **No ordering rule** — stacking all three is unattested in pidgins of either kind (§3).
- **Negation changes nothing.**
- **Rejected, each with its number:** a **perfect** (the possessive-derived kind is 3.2% of
  languages and 36.6% of total speakers — the most Eurocentric number in the study); a
  **separate habitual** (0 of 9 outside Europe); **remoteness grades** (0.9% of L1 in WALS's
  past-tense chapter); a dedicated **present** marker (48.2% of L1, and redundant given the
  unmarked default).

**Particle bill: 2, or 3 if irrealis is adopted.** (Tier 2 running total — Tier 4 has to fit
all of them into the phonology under §3.3's segment discouragement and §3.6's cluster cost.)

**What changed from the first version of this study, and why.** The first pass recommended
three particles including a fixed T-M-A ordering rule, on the strength of the creole record
with pidgins removed. Reading the pidgin strata first: the ordering rule is unsupported (0 of
18 pidgins stack three markers), the third particle drops from "recommended" to "judgment
call", and the case for optionality gets much stronger. The direction of the correction is
consistent — **weighting pidgins up makes the system smaller.**

---

## 5. Honest limits

- **9 restricted and 9 expanded pidgins** carry the load in §1–§2. That is the real n.
- **The contact-type classification is hand-assembled** and the expanded/creole boundary is
  genuinely contested — Tok Pisin, Bislama and Nigerian Pidgin have growing L1 populations
  and could be typed either way. The gradient in §1 is monotonic enough that a few
  re-classifications would not reverse it, but a ratio could move.
- **WALS 65A–68A rest on 220 languages.** They are a designed sample rather than a
  convenience one, but they are not a census, and the by-L1 columns are dominated by a
  handful of large languages.
- **APiCS codes category presence indirectly**, via a "no overt X marker" option on the
  feature that otherwise describes X. That is reliable for absence, less so for how central
  the marker is when present.
- **Grambank's particle features are permissive** — "*can* aspect be marked by a
  non-inflecting word" says a strategy is available, not that it is normal. The world
  percentages are upper bounds on "this is how the language does it".
