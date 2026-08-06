# Tier 3: coordination, comparatives and subordination

*Decided 2026-08-06. Agenda: [`grammar-plan.md`](grammar-plan.md) §4 Tier 3 Q13–17 ·
evidence policy: same file §5.*

**No committed study script.** Like [`grammar-tier3-predication.md`](grammar-tier3-predication.md),
the figures come from an ad-hoc query over the usual three sources (APiCS 20/41/42/71/72/92/93/
95/96, WALS 63A/64A/94A/121A/122A/128A, Grambank GB027/134/265/266/270/273/275/276/327/421/422)
rather than a `scripts/` module — a **logged deviation from the one-study-per-script
convention**, taken deliberately on time pressure for the least consequential tier. Figures are
reproducible from those parameter IDs; they are not reproducible by running anything in
`scripts/`.

**Bottom line up front.** **Five words** — *and*, *or*, *than*, *if*, and one invariant
**relativizer** that also serves as the optional complementizer. Comparatives leave the
adjective unmarked. Adverbial clauses of time, place, reason and manner reuse the Q10
interrogative compounds and cost nothing. **Tier 3 closes at 6 words and 3 rules.**

*§5 was revised after first publication:* it originally claimed adverbial clauses cost zero
words because subordinators are "ordinary vocabulary". That was under-argued — a dedicated
subordinator set would have been 8–10 words — and the zero is now earned by deriving them
from the interrogative compounds instead, at the cost of one rule and one irreducible word
(*if*). The word bill in §6 and the running totals were corrected with it.

| English | interlang shape |
|---|---|
| salt **and** pepper · he came **and** he sat | `salt and pepper` · `he come and he sit` |
| tea **or** coffee | `tea or coffee` |
| I am tall**er than** you | `I COP tall than you` |
| the tall**est** of all | `I COP tall than all` |
| the man **who** saw me | `man REL COP see me` |
| the book **that** I read | `book REL I read` |
| I know (**that**) he came | `I know (REL) he come` |
| **when** he arrived, we ate | `what-time he arrive, we eat` |
| **if** you go, I go | `if you go, I go` |

---

## 1. Coordination (Q13)

Three sub-questions, and English happens to answer all three the same way, which is worth
flagging so the English reader does not mistake familiarity for universality.

**(a) Is "and" the same word as "with"?** English distinguishes them (*John and Mary* vs
*I went with Mary*); many languages do not, using one word for both.

| | %lang | **%L1** |
|---|---|---|
| GB027 — nominal conjunction and comitative are **different** | 59.5 | **81.5** |
| WALS 63A — 'and' different from 'with' | 56.0 | 62.7 |

Contact languages split (APiCS 71: differentiation 3 of 9 restricted, identity 1, overlap 3).
**Decision: different words.** 81.5% of L1 keeps them apart, and conflating them makes
*I and you went* and *I went with you* the same string — we have spent our ambiguity budget
already (see the copula collision in the predication note).

**(b) Is noun-"and" the same as clause-"and"?** English uses *and* for both (*salt and
pepper*; *he came and he sat*); many languages use different words.

| | %lang | **%L1** | %total |
|---|---|---|---|
| WALS 64A — **identity** | 53.8 | **60.7** | 69.7 |
| WALS 64A — differentiation | 41.1 | 39.3 | 30.3 |

APiCS 72 is split by stratum — restricted pidgins prefer differentiation 4 to 2, expanded
pidgins prefer identity 5 to 2, creoles 28 to 19. **Decision: one word for both.** The
majority by people, the expanded-pidgin lean, and one fewer word.

**(c) Pronoun conjunction.** Some languages use an *inclusory* construction where "we"
already includes the named person — literally *we with John* meaning "John and I". APiCS 20:
**plain conjunction in 5 of 9 restricted pidgins and 47 of 54 creoles**, inclusory in 2 of 9
restricted. **Decision: plain conjunction** — `I and you`, not `we with you`. Rejecting the
inclusory pattern costs nothing and removes a construction that is genuinely confusing to
anyone whose language lacks it.

**"but" costs nothing** — it is *and* plus a contrast adverb from ordinary vocabulary.

**Word bill: 2** (*and*, *or*). "Or" has no useful typological feature in these sources; it is
taken as necessary without evidence, which is worth stating rather than implying it was
measured.

## 2. Comparatives (Q14)

English: *I am tall**er** than you* — a **degree marker** on the adjective (*-er*) plus a
**standard marker** (*than*) on the thing compared against. Languages vary independently on
both halves, and there are four broad strategies for the standard:

- **particle** — a dedicated word meaning roughly "than" (English)
- **locational** — the standard is marked with a spatial adposition, literally *tall from you*
- **exceed** — a verb meaning "surpass": *I tall exceed you* (widespread in West Africa and
  its creoles — Tok Pisin *winim*)
- **conjoined** — two clauses: *I am tall, you are short*

| WALS 121A | %lang | **%L1** | %total |
|---|---|---|---|
| locational | 47.0 | 29.9 | 26.5 |
| conjoined | 20.7 | **0.0** | 0.0 |
| exceed | 19.5 | 35.1 | 28.3 |
| particle | 12.8 | 35.0 | **45.2** |

| Grambank | %lang | **%L1** |
|---|---|---|
| GB273 — standard marker **neither** locational nor 'surpass' (i.e. a dedicated particle) | 41.7 | **73.5** |
| GB265 — comparative uses a 'surpass/exceed' form | 32.1 | 41.5 |
| GB276 — **non-bound** degree marker ("more") | 33.2 | 56.7 |
| GB275 — **bound** degree marker ("-er") | 20.5 | 22.3 |

**Decision: a dedicated particle "than", and the adjective is left unmarked.**
`I COP tall than you`. Superlative is `than all` — `I COP tall than all` — costing nothing.

- The **bound** degree marker is foreclosed by Tier 0 (no affixes), so *-er* was never
  available. The non-bound version ("more") is 56.7% of L1, and we are declining it: **6 of 9
  restricted pidgins leave the adjective unmarked** (APiCS 41), and the *than*-phrase already
  signals that a comparison is happening. One word saved.
- The particle strategy is only 12.8% of languages but **45.2% of total speakers**, and
  GB273's broader question puts a dedicated standard marker at **73.5% of L1**.
- **Rejecting "exceed" is a departure with a specific internal cause, and it is downstream of
  the copula.** Expanded pidgins prefer it strongly (7 of 9, APiCS 42) and it is 41.5% of L1.
  But we made adjectives take the copula, so *I COP tall exceed you* puts **two predicates in
  one clause** — serial-verb machinery we have not adopted and do not want. The uniform copula
  bought regularity in predication and charged us here. **Worth recording as a chain of
  consequences**, not just a local preference.
- **Conjoined comparatives are the cheapest rejection in the tier**: 20.7% of languages and
  **0.0% of L1** — the only feature in the entire project to hit a clean zero by population.

**Word bill: 1** (*than*), and it is an ordinary preposition using prepositional syntax we
already have, so it adds no rule.

## 3. Relative clauses (Q15)

Position was fixed in Tier 0 (relative clauses **follow** the noun). What was open is **how
the clause is introduced**, and the strategies differ in what English speakers would recognise:

- **gap** — nothing marks the clause; the shared element is simply missing: *the man [__ saw me]*
- **relative particle + gap** — an **invariant** marker: *the man **that** [__ saw me]*
- **relative pronoun** — a marker that **inflects** for the role of the shared element:
  *the man **who** [__ saw me]* vs *the man **whom** I saw*, or German *der/den/dem*
- **resumptive pronoun** — the marker plus a pronoun holding the slot: *the man that [**he**
  saw me]*
- **non-reduction** — the head noun is repeated inside the clause in full

| WALS 122A (subjects) | %lang | **%L1** | %total |
|---|---|---|---|
| gap | **75.2** | **65.4** | 49.4 |
| non-reduction | 14.5 | 10.1 | 9.5 |
| **relative pronoun** | 7.3 | 23.4 | **40.6** |
| pronoun-retention | 3.0 | 1.1 | 0.5 |

| APiCS 92 (subject relatives) | restricted | expanded | creole |
|---|---|---|---|
| **relative particle + gap** | 2 of 9 | **4 of 9** | **37 of 54** |
| zero + gap | 2 | 1 | 5 |
| relative particle + resumptive | 1 | 4 | 2 |
| **relative pronoun** | **0** | **0** | 9 |

**Decision: one invariant relativizer plus a gap.** `man REL COP see me` = "the man who saw
me"; `book REL I read` = "the book that I read".

- **The relative pronoun is rejected outright.** It is 40.6% of *total speakers* — a large
  number driven by English *who/which*, German *der*, Russian *который* — but **0 of 9
  restricted pidgins and 0 of 9 expanded pidgins have one**, and it is structurally impossible
  for us anyway: an inflecting relative pronoun needs case, and Q8 gave pronouns none.
- **Zero (bare gap) is cheaper and we are not taking it.** It is the world's majority strategy
  at 65.4% of L1, but those languages have case, agreement or verb morphology to signal where
  a clause begins. We have none of that, the clause *follows* the noun, and an unmarked
  postnominal clause gives a listener no cue that a new clause has started. The word buys a
  boundary marker.
- The particle-plus-gap combination is the modal contact strategy — 37 of 54 creoles on
  subjects, 29 of 54 on objects, 4 of 9 expanded pidgins.

**Word bill: 1. Rule added: 1** — *the relative clause follows its noun, begins with the
relativizer, and omits the shared element.*

## 4. Complement clauses (Q16)

English: *I know **that** he came*; *she said **that** it rained*. The complement clause is an
argument of the verb — it fills the object slot. English allows the *that* to be dropped
(*I know he came*), which is exactly the choice at issue.

| APiCS | restricted | expanded | creole |
|---|---|---|---|
| 95, verbs of **speaking**: no complementizer | **7 of 9** | 0 of 9 | 25 of 54 |
| 95: complementizer identical to 'say' | 0 | **6 of 9** | 11 |
| 96, verbs of **knowing**: no complementizer | **8 of 9** | 2 of 9 | 24 of 54 |

| the world | %lang | **%L1** |
|---|---|---|
| GB421 — **preposed** complementizer | 40.2 | **56.6** |
| GB422 — postposed complementizer | 12.2 | 12.1 |
| WALS 128A — utterance complements are **balanced** (ordinary finite clauses) | 79.6 | **75.3** |

**Decision: the complementizer is the same word as the relativizer, and it is optional.**
`I know he come` and `I know REL he come` are both well-formed.

- Restricted pidgins overwhelmingly use none (7 of 9, 8 of 9); 56.6% of L1 has one. Making it
  optional takes both, and English shows the pattern is stable for a real language.
- **Reusing the relativizer costs zero words.** English *that* already does both jobs, and
  nothing else in our grammar distinguishes the two contexts.
- **Optionality is safe here in a way it was not for TAM** (Q6 flagged that an optional
  *grammatical* marker makes its own omission meaningful). Omitting this one implicates
  nothing — the clause is a complement either way.
- **WALS 128A matters more than it looks**: "balanced" means the complement is an ordinary
  finite clause rather than a special non-finite form (English *I want **him to go*** is
  deranked). At 75.3% of L1, the majority strategy is the one requiring no machinery, which
  is fortunate since Tier 0 leaves us no way to build a non-finite verb form.

**Word bill: 0.**

## 5. Adverbial clauses (Q17)

English: ***when** he arrived*, we ate · *we left **because** it rained* · ***if** you go*, I
go. An adverbial clause is a whole clause acting as a **modifier of another clause** — it
fills the slot a single adverb would fill (*we ate **yesterday*** → *we ate **when he
arrived***). The **subordinator** marks the clause as subordinate and names the relation it
bears to the main clause. Without one, `he arrive, we eat` is two clauses in sequence with
the relation left to guess.

| | %lang | **%L1** | %total |
|---|---|---|---|
| WALS 94A — **initial** subordinator word | 60.3 | **78.4** | **86.4** |
| WALS 94A — final subordinator word | 14.8 | 6.8 | 4.0 |
| WALS 94A — subordinating **suffix** | 9.5 | 5.4 | 3.4 |
| GB134 — **same constituent order** in main and subordinate clauses | 94.0 | **96.4** | 89.6 |

**A correction to this note's first version, which claimed adverbial clauses cost zero words
because subordinators are "ordinary vocabulary".** That was under-argued. A subordinator is a
closed-class function word, not lexicon like *dog*, and **a dedicated set — when, while,
until, after, before, because, if, although — would have been 8–10 grammatical words, the
single most expensive decision in the grammar.** The zero is real, but it has to be earned by
deriving the subordinators from something, and there are two ways to do that.

**Route A — a noun plus the relativizer:** `time REL you arrive, we eat`, "the time that you
arrive, we eat". Attractive because it adds *no rule* — it is a relative clause on a noun,
using §3 machinery already bought. **But it silently requires the hard case:**

| WALS 123A, relativization on **obliques** | %lang | **%L1** |
|---|---|---|
| gap | 48.6 | 42.7 |
| pronoun-retention | 18.0 | 6.1 |
| relative pronoun | 11.7 | 39.3 |
| **not possible at all** | 9.0 | 1.3 |

Against subject relativization at 75.2% / 65.4% (§3), the oblique gap is markedly weaker —
and `time REL you arrive` is exactly an oblique, since "time" inside the clause is an adjunct
(*you arrive [at __]*), not subject or object. Contact languages agree it is hard: on
instrument relatives (APiCS 94) the modal strategy is **relative particle + resumptive
pronoun** (7 of 9 expanded pidgins), not a bare gap, and 5 languages cannot do it at all.
§3's rule licensed subject and object gaps only.

**Route B — reuse the interrogative compounds:** `what-time you arrive, we eat`. **Adopted.**
No gap, no relativization — the clause is complete and the compound names the relation. It is
what English does (*when*, *where*, *why*, *how* are each interrogative and subordinator at
once) and what many languages do, and it reuses words Q10 already coined.

**Q10 pays for itself here.** Putting the question particle on *every* question — argued in
that note on late-signal grounds — is what keeps the two readings apart:

| | |
|---|---|
| `Q what-time you arrive?` | when did you arrive? |
| `what-time you arrive, we eat` | when you arrived, we ate |

**The wrinkle is Q10's tolerated-dropping concession.** If speakers drop the particle in
casual content questions the two converge. The parse stays recoverable — a subordinate clause
is followed by a main clause, a bare question is not, and in writing the `?` settles it — but
this is a **residual ambiguity that is a direct cost of that concession**, and it belongs in
the record rather than in a footnote to Q10.

**Decision:**

| | |
|---|---|
| time, place, reason, manner | **0 words** — `what-time`, `what-place`, `what-reason`, `what-manner` |
| **conditional "if"** | **1 word, irreducible** — conditionals are irrealis, they do not decompose into noun-plus-clause, and with mood adverbial (Q6) there is nothing else to build them from |
| concessive "although" | **0** — contrastive coordination: `it rain, but we go` |
| position | **clause-initial** — 78.4% of L1, 86.4% of total speakers, and it follows §3.2's modifier rule |
| constituent order | **unchanged** — GB134 at **96.4% of L1** is the most one-sided figure in this note; the German-style verb-final subordinate clause is the exception, not something to consider |

**Word bill: 1** (*if*). **Rule added: 1** — *an interrogative compound with no question
particle, followed by a main clause, is an adverbial clause.*

---

## 6. What this decides

| | decision | words |
|---|---|---|
| "and" vs "with" | **different words** | — |
| noun-"and" vs clause-"and" | **same word** | 1 |
| "or" | one word | 1 |
| "but" | *and* + a contrast adverb | 0 |
| pronoun conjunction | plain (`I and you`), **no inclusory** | 0 |
| comparative standard | **particle "than"**, ordinary preposition | 1 |
| comparative degree | **adjective unmarked** — no "more", no *-er* | 0 |
| superlative | `than all` | 0 |
| relative clauses | **invariant relativizer + gap**, following the noun | 1 |
| relative pronoun | **rejected** — needs case, which Q8 refused | — |
| complement clauses | **the relativizer, optional** | 0 |
| adverbial clauses (time/place/reason/manner) | **the interrogative compounds**, clause-initial | 0 |
| conditional | **"if"** — irreducible | 1 |
| concessive | contrastive coordination (`it rain, but we go`) | 0 |

**Word bill: 5.** **Tier 3 total: 6** (copula 1, here 5). **Running grammar total: 16**
(Tier 2 ten, Tier 3 six) — still under 9% of the ~180 cluster-free monosyllables that avoid
the discouraged onsets.

**Grammar rules added: 2** (the relative-clause rule; the adverbial-clause rule). **Tier 3
total: 3**, with the copula rule. **Running grammar total: 5 rules.**

## 7. Honest limits

- **No committed script**, as with the predication note. See the header.
- **"Or" is asserted, not measured.** None of the three sources codes disjunction usefully.
- **The comparative rejects "exceed" against 7 of 9 expanded pidgins**, and the reason is a
  consequence of our own copula decision rather than anything about comparatives. If the
  copula were ever revisited, this should be revisited with it.
- **Leaving the adjective unmarked goes against 56.7% of L1** (GB276) on the strength of 6 of
  9 restricted pidgins and an economy argument.
- **The relativizer goes against the world's majority strategy** (bare gap, 65.4% of L1) on a
  boundary-cue argument that is about *our* grammar's lack of case and agreement, not about
  frequency. This is the right kind of reason, but it is an argument, not a measurement.
- **APiCS's restricted-pidgin cells are thin here** — several of the relative-clause and
  complementizer rows rest on one or two languages, thinner than the nine-language columns
  used in Tier 2.
- **§5's first version was wrong about the cost of subordinators** and is corrected in place
  with a note at the head of this file. The failure mode is worth naming: *"it's ordinary
  vocabulary" is the easiest way to make a word bill come out to zero, and it needs an
  argument every time it is used.* Nothing else in the grammar currently rests on that move,
  but Tier 4 will be full of opportunities to make it again.
- **Reusing the interrogative compounds as subordinators inherits Q10's residual ambiguity.**
  It is resolvable from the following main clause and from the `?` in writing, but it exists,
  and it is a downstream cost of a concession made two questions earlier.
