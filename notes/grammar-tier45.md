# Tiers 4 and 5: word formation, and the discourse residue

*Decided 2026-08-06. Agenda: [`grammar-plan.md`](grammar-plan.md) §4 · evidence policy:
same file §5. **No committed study script** — the third and last of the light-analysis notes,
same logged deviation from one-study-per-script as the two Tier 3 notes.*

**Bottom line up front.** **Three more words** — the ordinal marker, *yes* and *no* — and
**two more rules**. The grammar closes at **19 words and 8 rules**.

The two decisions worth reading are §1 (word classes are **semi-rigid**, not fluid, and the
reason is that our own earlier choices removed every cue that makes fluidity safe) and §9
(focus is **vocabulary**, which dissolves a conflict with the modifier rule rather than
resolving it).

---

# Tier 4 — word classes and word formation

## 1. Word classes: semi-rigid, with conversion by compounding

> **What the question is.** English lets you say *I **googled** it* or *a good **run*** — a
> noun used as a verb, a verb used as a noun, no change to the word. Other languages require
> a derivational suffix. **Fluid** means any root fills any slot; **rigid** means each root
> has a class and conversion costs something.

**The initial lean was fluid, and it does not survive contact with our other decisions.**

With fluid classes **nothing in a word tells you which word is the verb**, and every other cue
has already been spent: no articles (Q7), no case (Tier 0), no agreement (Tier 0), no
derivational affixes (Tier 0), and — as of the Tier 3 cleanup — exactly one verb per clause.

> `I water plant`
> `[I] [water = V] [plant = O]` → "I water the plant"
> `[I] [water = modifier] [plant = V]` → "I plant, water-ly"

Both parse. The obligatory-subject rule fixes the first slot; **which of the next two is the
verb is undetermined.** A subject followed by two class-ambiguous roots is not a rare
configuration in an isolating language with bare noun phrases — it is an ordinary one.

**Toki pona is the proof by example, and it argues the other way.** It is radically fluid, and
it pays for that with **`li`** (predicate marker) and **`e`** (direct object marker): *mi moku
**e** kili*. Those are exactly the disambiguators we lack. **Fluidity is not free; toki pona
buys it for two words.**

**We have also already chosen rigid once.** GB068 — do core adjectives act like verbs in
predicative position — is **48.6% of languages and 43.7% of L1**, and
[`grammar-tier3-predication.md`](grammar-tier3-predication.md) said no: adjectives take the
copula. The adjective/verb boundary is already rigid, so full noun/verb fluidity would be
inconsistent with a decision made one day earlier.

**Decision: semi-rigid. Each root carries a default class in the lexicon; conversion uses the
§2 compounding elements.** `water-do` verbs a noun, `run-thing` nominalises a verb. This is
**not new machinery** — it is §2's machinery applied one step further, so it costs **zero
words and zero rules**.

The language stays *fluid in spirit* — any concept can reach any slot — but the **form**
changes, which is what keeps the parse recoverable.

*The alternative, recorded because it is real:* buy an object marker on the toki pona model
(**+1 word**), which would restore full fluidity and incidentally allow word order to relax.
Declined — a word plus a rule, to loosen a word order that is currently doing all the
argument-role work perfectly well.

## 2. Derivation: a semi-open class of compounding elements

> **What the question is.** English builds *teach → teacher*, *bake → bakery*, *good →
> goodness*. Esperanto uses suffixes (*-isto*, *-ejo*, *-eco*). **We have no suffixes**, so
> these must be compounds: `teach-person`, `bake-place`, `good-quality`.

**GB048 — a productive way to derive an agent noun from a verb — is 65.4% of languages,
62.5% of L1 and 72.3% of total speakers.** Most languages have a way to say "teacher" from
"teach", and we need one. Ours is compounding, because Tier 0 left nothing else.

**Decision: bless a standard set of ~6–8 generic nouns as compounding elements —
person, thing, place, quality, action, tool — and treat the class as *semi-open*.** The
blessed set ships with the language as the recommended pattern; speakers imitate the pattern
to coin their own. **Not a rule, a published default** — the same shape as the Q6 handoff of
TAM concepts to the lexicon stage.

Explicitly modelled on toki pona's *jan*, *ma*, *toki* (Patrick, 2026-08-06).

**This is the single biggest lever on lexicon size**, and it is now the backbone of four
separate constructions:

| construction | source | example |
|---|---|---|
| interrogatives | Q10 | `what-person`, `what-place`, `what-time` |
| adverbial clauses | Tier 3 | `at time REL he arrive` |
| indefinites | §6 below | `some person`, `some thing` |
| **derivation** | **here** | `teach-person`, `bake-place` |

**The same handful of generic nouns does all four jobs.** That is a real architectural
economy and it is worth stating as a design principle rather than leaving as a coincidence:
*where a construction needs a semantic category, use the generic noun for it rather than
coining grammar.*

## 3. Compound headedness — forced, recorded anyway

> **What the question is.** Is a *firetruck* a truck or a fire? English puts the head last.

**Forced by Q11's modifier rule: compounds are head-final.** A `fire-truck` is a truck. No
decision required — recorded explicitly because the Tier 3 cleanup showed this project is
capable of assuming a feature into existence without deciding it.

## 4. Numerals: decimal, transparent, fully regular

> **What the question is.** Is counting base-10? Is 23 *twenty-three* or *two-ten-three*? And
> does *third* get a special form, or is it regular from *three*?

| | %lang | **%L1** | %total |
|---|---|---|---|
| GB333 — decimal system | 70.7 | **91.1** | 91.8 |
| WALS 131A — decimal base | 64.1 | **97.7** | 98.7 |
| GB335 — vigesimal element | 16.3 | 7.0 | 8.6 |
| GB334 — quinary element | 22.1 | **1.0** | 0.3 |

**Decimal is as close to a population universal as anything in this project.**

**Ordinals show the pidgin/creole gradient cleanly:**

| APiCS 35 | restricted | expanded | creole |
|---|---|---|---|
| **all ordinals derived from cardinals** | **2 of 9** | **3 of 9** | **2 of 54** |
| 'first' suppletive, rest derived | 1 | 1 | 19 |
| 'first', 'second' or more suppletive | 0 | 2 | 13 |
| all suppletive | 0 | 0 | 6 |

**Suppletive "first" is inherited, never invented** — 2 of 54 creoles are fully regular
against 2 of 9 restricted pidgins. WALS 53A's by-population columns are split several ways
with no majority, so the pidgin column decides it.

**Decision: decimal; 23 is `two-ten-three` (transparent, not *twenty-three*); ordinals fully
regular from cardinals with one marker, no suppletion.** `one-th, two-th, three-th`.

**Handoff to the lexicon stage: numerals should be monosyllabic** (Patrick, 2026-08-06) — a
nudge on the optimizer of the same kind as §3.3's segment discouragement and Q6's TAM
shortlist, not a rule. With transparent formation, 23 is three morphemes, so their length
compounds fast.

**Word bill: 1** (the ordinal marker) — or 0 if it is folded into §2's element set.

## 5. Quantifiers: both 'all' and 'every'

> **What the question is.** *All the students passed* (as a group) vs *every student passed*
> (one by one). English has two words; many languages have one.

**GB204 — 'all' and 'every' differ in form or position — is 55.7% of languages but 83.3% of
L1** (79.1% of total speakers).

**Decision: take both, meeting the population majority.** They are **ordinary vocabulary in a
semi-open quantifier class**, not grammar (Patrick, 2026-08-06), so the word bill is
unaffected. Recorded as a deliberate exception to this project's usual instinct to collapse a
distinction: an 83%-of-L1 majority is expensive to override, and here it costs nothing to
honour because the quantifiers are lexicon.

## 6. Indefinite pronouns: generic-noun-based

> **What the question is.** *someone*, *something*, *anything*. Q9 already committed us —
> "nobody came" is `not came any-person` — so these have to exist.

| APiCS 21 | restricted | expanded | creole |
|---|---|---|---|
| **generic-noun-based** | **4 of 9** | **5 of 9** | 30 of 54 |
| old generic-noun-based (*somebody/something*) | 1 | 4 | 14 |
| interrogative-based | 2 | 0 | 3 |
| special forms | 1 | 0 | 5 |

WALS 46A: interrogative-based is **59.3% of languages but only 22.2% of L1**; generic-noun-based
is 26.2% of languages, 21.8% of L1 and **40.4% of total speakers**. Another by-language /
by-people split, running our way.

**Decision: generic-noun-based** — `some person`, `some thing`, `any place`. 39 of 73 contact
languages, and it reuses §2's elements for the fourth time. **Word bill: 0** — "some" and
"any" are ordinary vocabulary.

---

# Tier 5 — discourse and the residue

## 7. Yes and no — and the trap

> **What the question is.** *Did you eat?* → yes/no is easy. **"Didn't you eat?" → "yes"** is
> ambiguous in English: *yes I did*, or *yes I didn't*? Japanese and Chinese answer the
> **polarity of the question**; English answers **the fact**, inconsistently.

**No source we hold codes this.** Decided by design argument.

**Decision: two words, answering the FACT and never the question's polarity** — and this is
stated explicitly in the grammar rather than left to convention, because it is a known
collision that bites exactly the L2 speakers the language exists for. `Q you no eat?` → `yes`
means *I ate*.

**Word bill: 2.** (Reusing the negator for "no" would save one; declined, because a bare
negator as a full answer is the construction most likely to be misheard.)

## 8. The imperative and the hortative

> **What the question is.** *Eat!* — is there a special form? And *let's eat* — a separate
> construction?

Settled by decisions already made rather than freshly: Q9 gave commands the ordinary negator
and no special construction, and the Tier 3 cleanup made **a subjectless verb phrase an
imperative**, which is what forced the obligatory-subject rule.

**WALS 72A: "neither an imperative nor a hortative system" — 53.9% of languages but 86.6% of
L1**, 87.5% of total speakers. A maximal system is 35.3% of languages and 9.7% of L1.

**Decision: no hortative construction** — *let's eat* is `we eat` plus a mood adverb, from
Q6's open-class TAM. Word bill 0.

**The imperative particle was considered and rejected** (Patrick asked for the check, on the
toki pona *o* model). **APiCS 56: a special imperative construction appears in 0 of 9
restricted pidgins, 1 of 9 expanded, 8 of 54 creoles.** Rare in exactly the stratum we weight
most, so by the rule Patrick set — *if it is rare, no particle and no pro-drop* — the
obligatory-subject decision stands. *Caveat: APiCS has no dedicated imperative feature; 56 is
the prohibitive feature and this reads its imperative half. "How often gained" is not
measurable here.*

## 9. Focus: vocabulary, not grammar

> **What the question is.** *It was **JOHN** who broke it* — English uses a cleft to spotlight
> one element. Many languages use a particle instead.

**The contact record is unusually consistent, and it conflicts with our modifier rule:**

| APiCS 106, focus particle 'also' | restricted | expanded | creole |
|---|---|---|---|
| **after the focused element** | **6 of 9** | **7 of 9** | 38 of 54 |
| before the focused element | 1 | 2 | 0 |

APiCS 104 (focusing the noun phrase) shows clefts are a creole strategy — cleft with copula
21 of 54 creoles, but **0 of 9 restricted pidgins**.

**Decision (Patrick, 2026-08-06): no dedicated focus construction. Focus is an ordinary
adjective or adverb** — *specifically*, *definitely* — drawn from the open lexicon.
`specifically John break window`.

**This dissolves the conflict rather than resolving it.** A focus *particle* would have had to
either follow its host (contradicting Q11's modifier rule) or precede it (contradicting 6 of 9
restricted pidgins). An ordinary modifier precedes its head like every other modifier, and
Q9's leftmost-widest scope rule already gives it the right scope. **We are not contradicting
the contact record's position — we are declining to have the construction**, which is a
cleaner kind of departure and worth distinguishing in the bias audit.

Clefts are rejected separately: they need a copula-fronting rule, and 0 of 9 restricted
pidgins use one. **Word bill: 0.**

## 10. Vocatives: none

> **What the question is.** ***John**, come here!* — some languages mark the addressee with a
> particle.

| APiCS 107 | restricted | expanded | creole |
|---|---|---|---|
| optional marker preceding the noun | 3 of 9 | 0 of 9 | 24 of 54 |
| **no vocative marker** | **3 of 9** | **4 of 9** | 9 of 54 |
| optional marker following the noun | 1 | 4 | 14 |

**Restricted pidgins split three ways evenly**, so nothing forces the decision.

**Decision: no vocative marker.** A bare name, with a comma in writing (§3.7). Word bill 0.

## 11. Ellipsis under coordination

> **What the question is.** *I ate and left* — English drops the second *I*. With subjects
> obligatory, must we say `I eat and I leave`?

Not codable in any source we hold. This is a **direct consequence of the no-pro-drop rule**
and would not exist without it.

**Decision: the shared subject may be omitted in the second and later conjuncts, and only
there.** `I eat and leave` is well-formed.

It **cannot collide with the imperative**, which is the collision that motivated banning
pro-drop in the first place: an imperative is clause-initial, and this position is
post-conjunction. Without this exception the no-pro-drop rule makes ordinary sentences
noticeably clunky for no gain.

**Word bill: 0. Rule added: 1.**

## 12. Comparison of equality

*as tall as you* — the Tier 3 comparative bought *than* for **inequality** and never covered
equality. **Decision: ordinary vocabulary** — `I COP tall same you`. Word bill 0.

## 13. Politeness and register, system-wide

Q8 rejected politeness distinctions in pronouns. **Confirmed system-wide: there is no
grammatical politeness anywhere.** Register is lexical — titles and honorific vocabulary,
which is what 8 creoles in the Q8 sample do.

**Patrick's expectation, recorded because it is a prediction the project can be judged on:
users will resurrect politeness via titles, and that is a success rather than a failure.** The
design goal was never to prevent politeness — it was to keep it out of the obligatory
grammar, so a learner who cannot yet read the social register can still form a sentence.

**This belongs in the bias audit as a system-level choice**, not only as the pronoun decision
it was first recorded as.

## 14. Proper names

> **What the question is.** Do names take a generic-noun classifier — toki pona *ma Tosi*,
> English *Lake Titicaca*, *Mount Everest*?

**Not codable.** APiCS 79 and 80 cover motion *to* and *from* named places (which preposition
is used), not classification. WALS and Grambank code nothing relevant. **The "do many L1
speakers do this" test cannot be run with the sources this project holds**, and no proxy is
substituted.

**Decision: no obligatory classifier.** Q7 rejected numeral classifiers and obligatory
classification generally; reintroducing it for names alone would be inconsistent.
**Optional use is free and expected** — `lake Titicaca`, `country Deutschland` — because §2's
generic nouns exist and compounding is free. Same shape as Q7's optional number: **not
required, freely available.**

**Endonyms are preferred** for names of places and peoples (Patrick, 2026-08-06) — a
lexicon-stage policy, recorded here and inherited by
[`lexicon-plan.md`](lexicon-plan.md). The §3.6 loan-mapping merge table applies, and the
deferred homophony recheck covers proper names too.

---

## 15. Totals

| | words | rules |
|---|---|---|
| Tier 4 | 1 (ordinal marker) | 0 |
| Tier 5 | 2 (*yes*, *no*) | 1 (coordination ellipsis) |
| **added here** | **3** | **1** |
| Tiers 0–3 | 16 | 6 |
| **grammar total** | **19** | **7** |

Plus the semi-rigid word-class decision, which adds a **lexicon convention** (every root
carries a default class) rather than a grammar rule.

**19 grammatical words against ~180 cluster-free monosyllables avoiding the discouraged
onsets — under 11% of the short-word space.** The lexicon inherits the rest.

## 16. Honest limits

- **No committed script**, the third such note. Figures come from an ad-hoc query over
  APiCS 21/26/35/56/104/106/107, WALS 46A/53A/72A/131A, Grambank GB048/GB068/GB204/GB333–335.
- **Four of these decisions rest on no contact evidence at all** — yes/no (§7), ellipsis
  (§11), equality (§12) and proper names (§14) are not coded by any source we hold. They are
  design arguments, and §14 in particular is the one Patrick explicitly wanted data for.
- **The word-class decision reverses the working lean** (fluid → semi-rigid) on an argument
  about *our* grammar rather than a distribution. If the object-marker option is ever
  revisited, this reverses with it.
- **§5 takes both 'all' and 'every' against this project's usual instinct to collapse**, and
  is only affordable because quantifiers were classed as lexicon. If that classification is
  wrong, the word bill is wrong by one.
- **APiCS's restricted-pidgin columns are 9 languages, and several rows here rest on 1–3.**
  §10's three-way even split is 3/3/1.
