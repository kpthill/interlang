# Closing the gaps the coverage sweep found

*Decided 2026-08-06. Source of the gap list:
[`grammar-coverage-sweep.md`](grammar-coverage-sweep.md) and
[`grammar-bias-audit.md`](grammar-bias-audit.md) §3. Evidence policy:
[`grammar-plan.md`](grammar-plan.md) §5. **No committed study script** — same logged
deviation as the other light-analysis notes.*

**Bottom line up front.** Eight gaps closed for **one word** — a second demonstrative — and
**no new rules**. Two existing rules are amended rather than added to. **Grammar total:
20 words, 7 rules.**

The sweep and the audit between them found that the grammar was **not** complete when it was
declared so. That is the second time a "done" claim in this project did not survive checking,
and it is recorded here rather than quietly fixed.

| gap | closure | cost |
|---|---|---|
| demonstrative distance contrast | **two-way, `this`/`that`** | **+1 word** |
| reciprocals | **`one-other`**, a compound | 0 |
| control complements (*I want to go*) | **subject omitted when it matches the matrix subject** | 0 |
| oblique relativization | **resumptive pronoun** (the ordinary 3sg/3pl) | 0 |
| causatives | **periphrastic**, identical in shape to control complements | 0 |
| intensifiers (*I did it myself*) | **the focus adverb** — and it is forced, not chosen | 0 |
| light verbs | **already present as `X-do`**; relabelled, not added | 0 |
| comitative vs instrumental | **two distinct prepositions** | 0 |

---

## 1. Demonstratives: a two-way contrast after all

Patrick's initial lean was a single demonstrative meaning "the contextually relevant one"
(toki pona *ni*), with a stated test: **adopt a distance contrast only if ≥50% of creoles and
pidgins make one.**

| APiCS 33 | restricted | expanded | creole |
|---|---|---|---|
| **two-way contrast** | **6 of 8** | **6 of 9** | 36 of 54 |
| no distance contrast | 2 | 3 | 9 |
| three-way | 0 | 0 | 8 |
| four-way | 0 | 0 | 1 |

**75% of restricted pidgins, 67% of expanded, 83% of creoles.** The test is met in every
stratum. WALS 41A agrees emphatically: *no distance contrast* is 3.0% of languages and
**4.4% of L1**, so roughly 95% of humanity distinguishes.

**Decision: a two-way contrast, `this` / `that`. Not three-way** — three-way is 37.8% of
languages but only 21.9% of L1 and **0 of 9 restricted pidgins**.

**+1 word.** This is the only gap in this note that costs anything, and it is the one where
the owner's stated test overrode the owner's lean — worth recording as a case where writing
the test down first did work.

## 2. Reciprocals: a compound, because a bare word is ambiguous

*They saw each other.* The first proposal was to reuse `self`, and the second was a bare
`other`. **Both fail.**

**Reusing `self` is what 1.2% of humanity does.** WALS 106A puts *reciprocal identical to
reflexive* at 24.7% of languages but **1.2% of L1**, against *distinct from reflexive* at
56.9% / **72.8%**. It is also a third job for `self`, which already carries the reflexive and
the passive.

**A bare `other` is genuinely ambiguous** (Patrick's objection, and it is correct):
`they see other` would mean both "they see the other one" and "they see each other".

**Every 'other'-based reciprocal in the world is a compound**, which is the answer: English
*each other* / *one another*, Spanish *el uno al otro*, German *einander*, Dutch *elkaar*.

**Decision: `one-other`**, a solid compound (§3.7) of two words we already have.

| | |
|---|---|
| `I see one, they see other` | "I see one, they see **the other**" |
| `they see one-other` | "they see **each other**" |

**Zero words.** It also matches the most common contact strategy: *special reciprocal
construction based on 'other'* is **25 of 54 creoles** (APiCS 89), the single largest cell.

## 3. Control complements: omit the subject when it matches

| APiCS 97 | restricted | expanded | creole |
|---|---|---|---|
| **complement subject left implicit** | **7 of 8** | **7 of 8** | **52 of 54** |
| expressed overtly | 1 | 1 | 1 |

**66 of 70 contact languages**, and WALS 124A puts *subject left implicit* at 51.3% of
languages and **89.4% of L1** (93.7% of total speakers). APiCS 98 adds that **8 of 9
restricted pidgins use no complementizer** at all.

**Decision: the complement subject is omitted when identical to the matrix subject.**

| | |
|---|---|
| `I want go` | I want to go |
| `I try eat` | I try to eat |
| `I like swim` | I like to swim |
| `I want REL you go` | I want **you** to go |

**This does not add a rule — it extends the one Tier 5 already added for coordination.**
Subject omission is now licensed in exactly two places: **the second conjunct of a
coordination, and the complement of a control verb.** Neither is clause-initial, so neither
can be misread as an imperative, which was the collision that forced the obligatory-subject
rule in the first place.

**Usage note, not a rule:** where the complement subject *differs*, the optional
complementizer stops being optional in practice. `I want you go` is ambiguous between
*[I want you] [go]* and *[I want [you go]]*; `I want REL you go` is not. **`REL` earns its
keep exactly where the subjects differ.**

## 4. Oblique relativization: a resumptive pronoun

*The knife I cut the bread with* was **unsayable** — Q15 chose relativizer-plus-gap on
WALS 122A, which codes relativization on **subjects** only.

The two candidate repairs, by lexifier group (APiCS 94):

| | European | non-European |
|---|---|---|
| particle + gap, **preposition stranding** | **18** | **1** |
| zero + gap, **preposition stranding** | **9** | **0** |
| particle + **resumptive pronoun** | 15 | 5 |
| zero + **resumptive pronoun** | 11 | 3 |

**Preposition stranding is 27 European to 1 non-European** — it fails Rule 1 about as badly
as a feature can, and it is a Germanic quirk that the sweep flagged as such. Resumptive is
26:8, and leads the pidgin columns (7 of 9 expanded pidgins use particle + resumptive).

Stranding also carries a real ambiguity: a preposition with no object followed by a noun can
capture that noun. `man REL I give book to leave` reads *to leave* as a prepositional phrase.
§1 of [`grammar-tier45.md`](grammar-tier45.md)'s semi-rigid word classes mitigate this but do
not remove it.

**Decision: a resumptive pronoun — the ordinary 3sg (or 3pl) pronoun, in the position the
gap would have occupied.**

> `knife REL I cut bread with it COP not sharp`
> "the knife I cut the bread with is not sharp"

**Zero words.** A resumptive pronoun *is* an ordinary pronoun; nothing new is coined, and Q8's
gender-free 3sg covers he/she/it.

**This amends rule 4 rather than adding one:** *the relative clause omits the shared element
where it is subject or object; where it is oblique, a resumptive pronoun holds the position.*

## 5. Causatives: periphrastic, and the same shape as §3

**No contact evidence exists.** APiCS has no causative parameter — checked against
`data/raw/apics/cldf/parameters.csv`, genuinely absent, unlike two earlier claims of this
kind in these notes (see [`grammar-tier3-cleanup.md`](grammar-tier3-cleanup.md) §6).

The world, and it does not offer us much: **GB155 puts affixal causatives at 72.5% of
languages but 48.2% of L1** — and affixes are foreclosed by Tier 0 anyway. WALS 111A shows
*morphological but no compound* at 81.9% of languages, with the interesting minority being
*compound but no morphological* at 2.9% of languages and **25.2% of L1**.

With no affixes and no serial verbs, **periphrastic is the only route**, and Patrick's
preferred shape — *the dependent clause looks exactly like a standalone clause* — is WALS
128A's **balanced** strategy, which is 75.3% of L1.

| | |
|---|---|
| `I want REL John go` | I want John to go |
| `I make REL John go` | I make John go |
| `I let REL John go` | I let John go |

**Same structure, swap the verb.** *Make*, *let* and *want* are ordinary lexical verbs.
**Zero grammatical words, zero rules** — it is a complement clause and nothing more. The
compound causative (`go-make`) remains available to the lexicon for free if it ever wants it.

## 6. Intensifiers: forced, not chosen

*I did it myself.* WALS 47A puts *intensifiers identical to reflexives* at 56.0% of languages
and **70.5% of L1**, so reusing `self` is the world's normal pattern, and APiCS 88 splits
(identical 3 of 9 restricted, differentiated 1 of 9).

**We cannot have it.** The preverbal slot where an intensifying `self` would sit **is already
the passive** (§2a of the cleanup note): `I self do it` means *"I am done"*. The slot is
occupied.

**Decision: the focus adverb** — `specifically I do it`. **Zero words**, since focus was made
lexical in [`grammar-tier45.md`](grammar-tier45.md) §9.

**We lose the form 70.5% of L1 uses, not the meaning.** Worth recording precisely because it
is the first decision in the project that was *forced by a prior decision leaving no
alternative*, rather than chosen among live options.

## 7. Light verbs: already present, mislabelled

A **light verb** is a semantically bleached verb that carries the syntax while a noun carries
the meaning: *take a walk*, *have a look*; Hindi *karnā*, Japanese *suru*, Persian *kardan*,
Turkish *etmek*. Their most important job for us is **verbalising borrowings without
morphology** — Japanese *benkyō-suru*, Hindi *start karnā*.

The bias audit coded this absent, at a cost of **71.4% of world L1**. **That is a labelling
artefact.** §2 of [`grammar-tier45.md`](grammar-tier45.md) already blesses `X-do` as a
derivational compounding element, and `telefon-do` "to telephone" *is* a light-verb
construction — it is simply written solid.

**Decision: relabel, do not add.** `X-do` is the light-verb construction, and it is the
designated mechanism for verbalising international borrowings. **Zero words, zero rules.**
**No source codes light verbs** — all three parameter lists checked.

**One consequence handed to the lexicon stage:** §3.7's solid compounding makes this
`telefondo`, and for long technical borrowings the results get unwieldy. Flagged rather than
solved.

## 8. Comitative vs instrumental: distinguish them

*I went **with** my friend* (comitative) versus *I cut it **with** a knife* (instrumental).

| APiCS 70 | restricted | expanded | creole |
|---|---|---|---|
| **identity** | 3 of 8 | **7 of 7** | **41 of 45** |
| **differentiation** | **5 of 8** | 0 | 4 |

**The creole identity is almost certainly inheritance, not convergence.** English *with*,
French *avec*, Spanish *con* and Portuguese *com* all conflate the two — so 41 of 45 creoles
agreeing is exactly the confound **Rule 1** exists to catch. The stratum least exposed to
lexifier syntax, restricted pidgins, goes the other way **5 to 3**.

WALS 52A: **differentiation 66.0% of languages and 59.3% of L1**; identity 23.6% / 34.1%.

**Decision: two distinct prepositions.** World majority by people, restricted-pidgin lean, and
consistent with our own `and` ≠ `with` decision (GB027, **81.5% of L1**). **Zero grammatical
words** — they are prepositions, which are ordinary vocabulary.

APiCS 69 confirms the strategy independently: the instrumental is expressed by an
**adposition** in 5 of 8 restricted pidgins and 49 of 54 creoles — which is what we would do
regardless, having no serial verbs and no case.

---

## 9. Totals

**Word bill: 1** (the second demonstrative). **Rules added: 0** — two existing rules amended:

- *relative clauses* now read: omit the shared element where it is subject or object; where
  it is oblique, a resumptive pronoun holds the position.
- *subject omission* now reads: licensed in the second conjunct of a coordination, and in the
  complement of a control verb.

**GRAMMAR TOTAL: 20 words, 7 rules.**

## 10. Three more, closed 2026-08-06

**None of these is coded by any source we hold** — parameter lists checked for all three,
stated plainly given that this project has twice asserted an absence of evidence and been
wrong. All three cost **zero words and zero new rules**.

### 10.1 Fragment answers

*Who came? — John.* Currently ill-formed: only *yes* and *no* were licensed as standalone
fragments, so an answer had to be a full clause.

| option | |
|---|---|
| ban fragments, require `John come` | safest, most verbose |
| **allow a bare constituent as the answer to a content question** | **adopted** |
| allow fragments generally in conversation | loosest, least recoverable |

**Decision: a bare constituent may answer a content question.** The question supplies the
frame, so the answer is recoverable — the same licensing logic as coordination ellipsis and
control complements, and the third member of that family. Arguably a discourse convention
rather than a grammar rule. **No contact data.**

### 10.2 Direct vs indirect speech

*He said "I am tired"* versus *he said he was tired.* With no tense marking the tense half is
moot; **the pronoun half is real** — in `he say REL I COP tired`, is *I* the original speaker
or the reporter?

**Decision: direct speech only. Reported speech is always a quotation and pronouns never
shift.** `he say "I COP tired"`.

- §3.7 already supplies quotation marks, so writing is covered.
- Indirect speech would require an **obligatory pronoun-shifting computation** on every
  report — exactly the class of thing rejected in Q8 (politeness) and Q6 (TAM): a calculation
  the speaker must perform correctly before opening their mouth.
- **Indirect contact evidence, the closest available:** APiCS 95 shows **6 of 9 expanded
  pidgins use a complementizer identical to bare 'say'** — grammaticalising the verb *say*
  into a quotative, which is the classic direct-speech pattern. Suggestive, not decisive, and
  labelled as such.

### 10.3 Stacked modifier order

*big red house*, *three big houses*. §3.2's modifier rule fixes which **side** modifiers go
on, not their **sequence** among themselves.

| option | |
|---|---|
| free order, no constraint | ambiguous, wastes a distinction |
| English-style fixed semantic sequence (opinion > size > age > colour > origin) | a memorised list with no principle behind it — the worst kind of rule for a learner |
| **scope-based: leftmost modifier is widest** | **adopted** |

**Decision: reuse Q9's scope rule.** *Leftmost is widest* was established for negation and TAM
adverbs; applying it to stacked noun modifiers costs **zero new rules** and converts free
order into an expressible distinction:

| | |
|---|---|
| `three big house` | three [big houses] |
| `big three house` | a big [group of three houses] |

This is the third construction that rule now covers (negation scope, TAM scope, modifier
stacking), which is a good sign it was the right rule to buy.

**No contact data.** WALS 87A and APiCS 3 code adjective-versus-noun order, not the ordering
among multiple adjectives.

## 11. What is still open

**The grammar is now complete except where explicitly deferred**, which is the strongest
version of that claim this project should make. Remaining, all minor:

1. **Reflexive domain** — how far `self` may look for its antecedent, now that it also marks
   the passive.
2. **Valency and labile verbs** — *the window broke* vs *he broke the window*. Interacts with
   the `self` passive and may be redundant with it.
3. **Distributive, multiplicative and fractional numerals** — *each two*, *twice*, *half*
   (WALS 54A, APiCS 34 both code this — it is measurable when we want it).
4. **Non-subject ellipsis**, **evidentiality**, **ideophones and interjections**,
   **extraposed relatives** — minor or lexicon-facing.

## 11. Honest limits

- **No committed study script**, the fourth such note.
- **Causatives and light verbs rest on no contact evidence** — APiCS codes neither, verified
  against the parameter list.
- **Fragment answers, reciprocal ambiguity and the control-complement usage note are design
  arguments**, not measurements.
- **§1 is the only decision here that the owner's prior lean opposed**, and it was reversed by
  a test the owner set in advance. That is the process working; it is also a reminder that the
  other seven decisions here had no such pre-registered test.
- **The claim "the grammar is complete" has now been wrong twice** — once at the end of
  Tier 3, once at the end of Tier 5. §10 is written to keep the third claim honest.
