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
| passive | **none** — use an indefinite subject |
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

## 2. No passive

| | %lang | **%L1** | %total |
|---|---|---|---|
| GB086 — passive construction | 66.8 | **77.9** | 65.4 |
| GB110 — antipassive | 10.5 | 24.2 | 35.0 |

**77.9% of world L1 has a passive**, and this rejects it. The reason is structural rather
than preferential: a passive needs either **verb morphology** (Tier 0 forbids affixes) or a
**participle** in a periphrastic construction (we have no non-finite verb form — see
[`grammar-tier3-combination.md`](grammar-tier3-combination.md) §5 on balanced clauses). So a
passive would cost a new word *and* a new rule *and* a verb form the grammar otherwise lacks.

**Decision: no passive. Use an indefinite subject** — `someone steal the book` for "the book
was stolen". The passive's real work is demoting an unknown or unimportant agent, and an
indefinite subject does that with vocabulary we need anyway.

**What is genuinely lost:** the passive's *other* job is information structure — putting the
patient in topic position — and with rigid SVO and no topicalization we cannot do that. A
speaker who wants "the book" as the topic has no way to get it there. **This is an accepted
cost and it is the sharpest one in this note.**

**Consequence: the alignment deferral is now closed on both routes.**
[`principles.md`](principles.md) §7 named two things that would reopen alignment — pronoun
case (closed by Q8) and *a passive*. Both are now shut.

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

**Word bill: 0.** **Rules added: 1** (obligatory subject).

**Running grammar total: 16 words, 6 rules.**

## 6. Honest limits

- **No committed script**, as with the other two Tier 3 notes.
- **The passive rejection overrides 77.9% of world L1**, the second-largest population
  override in the project after Q8's politeness distinction (85%). The structural argument is
  strong — we genuinely have no morphology to build one from — but the *information-structure*
  loss in §2 is real and unmitigated, and belongs in the final bias audit.
- **The pro-drop rejection overrides 66.9% of world L1.** The imperative-collision argument
  is decisive given our other choices, but it is an argument about our design, not a finding.
- **Three of these four were being silently assumed**, which is the actual finding here. The
  process risk is worth naming: *a write-up that justifies a decision by appeal to a feature
  we have not decided has smuggled that feature in.* Worth a grep of the notes for similar
  appeals before the grammar is called finished.
- **APiCS does not code the passive, pro-drop or ditransitive order**, so those three have no
  contact-language column at all — only the serial-verb decision has pidgin evidence behind
  it. That is a thinner basis than any Tier 2 decision had.
