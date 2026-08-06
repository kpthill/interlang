# Tier 3 cleanup: four decisions that were being assumed

*Decided 2026-08-06. Agenda: [`grammar-plan.md`](grammar-plan.md) · evidence policy: same
file §5. **No committed study script** — same logged deviation as the other two Tier 3 notes.*

These four were never on the agenda, and three of them are only visible because earlier
write-ups **invoked them as premises**. The exceed-comparative in
[`grammar-tier3-combination.md`](grammar-tier3-combination.md) §2 was rejected because it
"puts two predicates in one clause — serial-verb machinery we have not adopted", which was
true only in the sense that nobody had adopted it *or rejected it*. That is a bad way for a
grammar to acquire a feature, so they are settled here explicitly.

**All four cost zero words. One adds a rule.**

| | decision |
|---|---|
| serial verb constructions | **none** |
| passive | **yes** — preverbal `self` (§2 reversed a wrong rejection) |
| pro-drop | **none** — the subject is obligatory |
| ditransitives | **indirect-object construction** — the recipient takes a preposition |

---

## 1. No serial verb constructions

A **serial verb construction** puts two or more verbs in one clause sharing arguments, with
no conjunction and no subordination: *I take knife cut bread* for "I cut the bread with a
knife", *he run go market* for "he ran to the market".

| APiCS | restricted | expanded | creole |
|---|---|---|---|
| 86 — **no 'give' serials** | **7 of 9** | **7 of 9** | 25 of 54 |
| 85 — **no 'take' serials** | **5 of 9** | 4 of 9 | 30 of 54 |
| 84 — directional 'come'/'go' serials **exist** | 4 of 9 | 5 of 9 | 30 of 54 |

Grambank GB118 puts serial verbs at 53.0% of languages, **48.4% of L1** and 58.8% of total
speakers — a plurality of humanity but not a majority of languages, and **not a pidgin
feature**: restricted pidgins lack 'give' serials 7 to 2 and 'take' serials 5 to 4.

**Decision: no serial verbs.** Everything they do is available to us by other means already
bought — coordination (*I take knife and I cut bread*), prepositions (*I cut bread with
knife*), and the indirect-object construction in §4. The cost of having them is that a
learner must work out how two adjacent verbs share arguments with nothing marking the
relation, in a language where **word order is the only marker of argument role** (Tier 0).

**This is not a Euro-default.** Serial verbs are a West African and South-East Asian feature
and rejecting them could look like exactly the bias this project is trying to avoid — but the
pidgin columns are what decide it, and they point the same way. Recorded so the final bias
audit can weigh it rather than have it pass unnoticed.

**Consequence:** the exceed-comparative rejection in
[`grammar-tier3-combination.md`](grammar-tier3-combination.md) §2 now rests on a stated
premise instead of an assumed one.

## 2. The passive — REVERSED 2026-08-06, on a false premise

> **The decision recorded in this section was wrong and has been reversed.** The original
> text is preserved below the rule, because the error is instructive. §2a is what replaced it.

**Original decision: no passive**, on the grounds that *a passive needs either verb morphology
(Tier 0 forbids affixes) or a participle (we have no non-finite verb form), so it would cost a
word, a rule and a verb form the grammar otherwise lacks.* Use an indefinite subject instead —
`someone steal the book`. Quoted GB086 at 66.8% of languages / 77.9% of L1, and accepted the
loss of patient-topicalization as "the sharpest cost in this note".

**The premise is false.** Grambank codes the third option the argument never considered:

| | %lang | **%L1** | %total |
|---|---|---|---|
| **GB302 — phonologically FREE passive marker (particle or auxiliary)** | 10.5 | **64.6** | 67.3 |
| GB147 — morphological passive on the lexical verb | 42.6 | 36.5 | 35.3 |
| GB304 — the agent can be expressed overtly in a passive clause | 40.5 | **91.8** | 89.8 |

**A free passive particle needs no morphology at all** — Mandarin 被 *bèi* is the model — and
it is what **64.6% of world L1** has. The passive was never structurally foreclosed.

**The population cost was also understated.** WALS 107A is worse than the GB086 figure quoted:

| WALS 107A | %lang | **%L1** | %total |
|---|---|---|---|
| passive **present** | 43.0 | **95.2** | 97.5 |
| passive **absent** | 57.0 | **4.8** | 2.5 |

Rejecting the passive would have been a **95%-of-L1 override**, comfortably the largest in the
project — larger than Q8's politeness distinction at 85% — resting on a claim about our own
grammar that one Grambank feature refutes.

**Failure mode, named:** the argument reasoned from *our* constraints straight to "therefore
impossible", without checking whether the world had a strategy that fits inside them. Same
shape as the `"it's ordinary vocabulary"` error in
[`grammar-tier3-combination.md`](grammar-tier3-combination.md) §5 — a conclusion reached by
introspecting about the design instead of looking.

## 2a. The passive, as adopted: a preverbal `self`

**Decision (Patrick, 2026-08-06): the reflexive pronoun in the preverbal modifier slot marks
the passive.** `window self break` = "the window was broken".

- **Zero words** — it reuses the Q8 reflexive. **Zero rules** — it uses the preverbal modifier
  zone that already holds negation (Q9) and TAM adverbs (Q6).
- **Disambiguation is positional and free.** Q8 put the reflexive in *object* position
  (`I see self` = "I see myself"), so preverbal `self` is an unused combination:
  `I self see` = "I am seen".
- **The agent can still be expressed** — `window self break by man` — which matters, since
  GB304 puts agent expression at **91.8% of L1**. "By" is ordinary vocabulary.
- **It recovers the information-structure loss** the original decision accepted: the patient
  is now the grammatical subject and sits in topic position.

**A correction to the proposal as first framed.** Putting `self` in *subject* position —
`self break window` — yields an **impersonal**, not a passive: the patient stays an object, so
the agent is defocused but not demoted, and it buys nothing over `someone break window`. The
Spanish model actually points the other way: in *se dejaron caer las llaves*, `se` is a
**preverbal clitic** and *las llaves* is the **subject** — the verb agrees with it, plural
*dejaron*. The preverbal slot is what makes it a passive rather than an impersonal.

**Eurocentrism check, as requested — mixed, and the parts have to be separated.**

| APiCS 90, by lexifier group | European | non-European |
|---|---|---|
| typical passive construction | 30 | 7 |
| **passive without verbal coding** | **30** | **1** |
| absence of passive | 17 | 6 |
| other atypical passive | 3 | 3 |

- **The passive itself is not a European import**: non-European-lexifier creoles have some
  passive **11 to 6**.
- **The unmarked type specifically is Euro-concentrated, 30 to 1** — and that is the type
  nearest a bare reflexive construction, so the concern was well placed.
- **Pidgins do lack passives**: absent in **5 of 9 restricted** and 6 of 9 expanded. That half
  of the original argument survives, and adopting one is a standing rule 6 departure.
- **No source we hold codes the reflexive→passive path.** **[recall, unverified]** it is well
  attested in Romance, Slavic and Scandinavian and is Europe-heavy. **But that is about where
  the *word* comes from, not about the *strategy*.** We are adopting a free preverbal marker —
  a 64.6%-of-L1 strategy whose flagship is Mandarin, not Romance — and which existing word
  fills the slot is a costless lexical choice. Reusing `self` costs nothing; a dedicated
  particle would cost one word and buy no structural difference.

**Consequence: the alignment deferral is reopened and immediately re-closed.**
[`principles.md`](principles.md) §7 named a passive as one of the two routes back to alignment.
We now have one — but it carries no case, no agreement and no argument marking of any kind, so
there is still no morphology anywhere that could express an alignment contrast. **The deferral
holds, now for a stated reason rather than by absence of the construction.**

## 3. No pro-drop — the subject is obligatory

**Pro-drop** (or *null anaphora*) is omitting a subject or object recoverable from context:
Spanish *hablo* "I speak", Japanese with no pronoun at all.

| | %lang | **%L1** | %total |
|---|---|---|---|
| GB522 — S or A can be omitted when inferrable | 73.6 | **66.9** | 52.5 |

**This rejects a two-thirds majority**, and there are two reasons, the second decisive:

1. **There is nothing to recover the subject from.** Languages that drop subjects almost
   always have verb agreement encoding person and number. Tier 0 gave us none, so a dropped
   subject is recoverable only from discourse context — the least reliable channel, and the
   one least shared between strangers.
2. **It would collide with the imperative.** Q9 settled that commands use the ordinary
   negator and no special construction, which makes the imperative a **bare verb phrase with
   no subject**. If subjects were droppable, `eat food` would be both "eat the food!" and
   "(he) eats food" — a high-frequency ambiguity in the one construction where being
   misunderstood matters most.

**Decision: the subject is obligatory.** This is the second decision in Tier 3 forced by an
**interaction between our own choices** rather than by a distribution — the first was the
copula and the possessive collision. Both were invisible to the sources, which code features
one at a time.

**Rule added: 1** — *every clause has an overt subject; a subjectless verb phrase is an
imperative.*

## 4. Ditransitives: the recipient takes a preposition

*I gave him the book* has two objects, and **SVO does not say what order they go in** — a gap
in Tier 0 that has been sitting open unnoticed. Three strategies:

- **indirect-object construction** — recipient marked by an adposition: *I gave the book **to
  him***
- **double-object construction** — both bare, order fixed by rule: *I gave **him** **the
  book***
- **secondary-object construction** — recipient bare, theme marked

| WALS 105A | %lang | **%L1** | %total |
|---|---|---|---|
| **indirect-object** | **49.9** | **51.3** | 40.3 |
| double-object | 22.3 | 29.7 | 26.1 |
| secondary-object | 17.4 | 2.6 | 1.4 |
| mixed | 10.5 | 16.3 | 32.1 |

**Decision: the indirect-object construction.** `I give book to he`.

- Plurality on both counts, and **it costs nothing** — we already have prepositions (Tier 0)
  and "to" is ordinary vocabulary.
- **It removes the need for any rule at all about two objects.** The double-object
  construction would require memorising which bare object comes first, in a language where
  position is the only role marker and there would be no cue to recover from an error. The
  preposition makes the roles explicit.
- Note this is the same move as §1: where a construction could be handled by *position* or by
  *an overt marker*, and position is already carrying the entire argument-role load, take the
  overt marker.

---

## 5. Totals

**Word bill: 0** — the passive reuses `self`, the ditransitive reuses a preposition.
**Rules added: 1** (obligatory subject).

**Running grammar total: 16 words, 6 rules.**

## 6. Honest limits

- **No committed script**, as with the other two Tier 3 notes.
- **§2 was wrong and is reversed in place.** The rejection rested on "we have no morphology
  to build a passive from", which GB302 refutes: a free passive particle is 64.6% of L1. Had
  it stood, it would have been a 95%-of-L1 override (WALS 107A) — the largest in the project —
  on a false premise. The failure mode is named in §2 and it is the same one as the
  "ordinary vocabulary" error in the combination note: **reasoning from our constraints to
  "impossible" without checking what strategies fit inside them.** Both errors were caught by
  Patrick pushing back, not by the process.
- **Adopting a passive is still a rule 6 departure** — 5 of 9 restricted pidgins have none —
  and reusing `self` for it sits near a Euro-concentrated pattern (APiCS 90's unmarked
  passive is 30 European to 1 non-European). The *strategy* is not Euro; the sourcing might
  look it. Belongs in the bias audit.
- **The pro-drop rejection overrides 66.9% of world L1.** The imperative-collision argument
  is decisive given our other choices, but it is an argument about our design, not a finding.
- **Three of these four were being silently assumed**, which is the actual finding here. The
  process risk is worth naming: *a write-up that justifies a decision by appeal to a feature
  we have not decided has smuggled that feature in.* Worth a grep of the notes for similar
  appeals before the grammar is called finished.
- ~~**APiCS does not code the passive, pro-drop or ditransitive order.**~~ **FALSE, corrected
  2026-08-06 by the coverage sweep** ([`grammar-coverage-sweep.md`](grammar-coverage-sweep.md)).
  **APiCS 90 codes the passive** — and §2a of this very note uses it, so the claim contradicts
  the document it appears in. **APiCS 61 codes the order of recipient and theme in
  ditransitives**, and §4 decided that question on WALS 105A alone while declaring contact
  evidence absent. **Only pro-drop is genuinely uncoded.** §4 should be re-run against
  APiCS 61 before the ditransitive decision is called settled.
- **The failure mode this reveals is worse than a typo:** an honest-limits section asserted an
  absence of evidence without checking the parameter list, and the assertion was false in two
  of three cases. *"No source codes this"* is a claim like any other and needs the same
  verification as a percentage — the sweep found the same pattern in four other places where
  features sitting on disk (APiCS 11, 94, 97, 98; WALS 124A) were never consulted.
