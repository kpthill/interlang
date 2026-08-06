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

## 10. What is still open

**The grammar is not finished, and saying otherwise would repeat the mistake this note
exists to correct.** Remaining, ranked:

1. **Fragment answers.** *Who came? — John.* Currently ill-formed: only *yes* and *no* are
   licensed as standalone fragments. Not coded by any source.
2. **Direct vs indirect speech.** *He said "I am tired"* vs *he said he was tired* — whether
   pronouns shift under reporting. With no tense marking the tense half is moot, but the
   **pronoun** half is real and undecided.
3. **Stacked prenominal modifier order.** *big red house* — the order among multiple
   modifiers before a noun. The modifier rule fixes the side, not the sequence.
4. **Reflexive domain** — how far `self` may look for its antecedent, now that it also marks
   the passive.
5. **Valency and labile verbs** — *the window broke* vs *he broke the window*. Interacts
   directly with the `self` passive and may be redundant with it.
6. **Distributive, multiplicative and fractional numerals** — *each two*, *twice*, *half*
   (WALS 54A, APiCS 34).
7. **Non-subject ellipsis**, **evidentiality**, **ideophones and interjections**,
   **extraposed relatives** — minor or lexicon-facing.

Items 1–3 are the ones a user would hit in a first conversation.

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
