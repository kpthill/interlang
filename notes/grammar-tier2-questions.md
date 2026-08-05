# Tier 2 Q10: question formation

*Study run 2026-08-05. Script: [`../scripts/grammar_tier2_questions.py`](../scripts/grammar_tier2_questions.py) ·
output: `data/processed/grammar_tier2_questions.csv` · agenda:
[`grammar-plan.md`](grammar-plan.md) §4 Q10 · evidence policy: same file §5.*

**Bottom line up front.** **One clause-initial question particle — "is it the case that…?" —
on every question, polar and content alike. Content question words stay in place. One
interrogative root, "what", with the rest built by compounding.** Inversion is rejected on
the cleanest Rule 2 result in the project. **Word bill: 2**, closing Tier 2 at **10**.

Two things in this study are departures rather than findings, and both are flagged where
they occur: putting the particle **first** goes against a modest world and contact preference
for clause-final, and putting it on **content questions too** is not codable from any source
we have.

---

## 1. Polar questions: four of the seven strategies were already dead

WALS 116A is the only source here that partitions — it asks which strategy is *dominant*:

| strategy | %lang | **%L1** | %total | available to us? |
|---|---|---|---|---|
| **question particle** | **61.0** | **66.4** | 63.6 | **yes** |
| interrogative intonation only | 18.2 | 6.2 | 3.4 | yes |
| interrogative verb morphology | 17.3 | 6.5 | 4.1 | **no** — Tier 0 forbids affixes |
| interrogative word order | 1.4 | **20.1** | 28.3 | yes, but see §2 |
| mixture of intonation + morphology | 1.6 | 0.8 | 0.6 | no |
| absence of declarative morphemes | 0.4 | 0.0 | 0.0 | no |
| no interrogative/declarative distinction | 0.1 | 0.0 | 0.0 | — |

Add Grambank's two extra strategies, neither of which we can use: **tone** (4.8% of languages)
is ruled out by §3.3's non-tonal inventory, and **verbal morphology only** (17.6%) by Tier 0.
**V-not-V** — *you like not like?* — is 6.9% of languages but **39.9% of L1**, almost all of it
Sinitic; it is compatible with an isolating grammar and we are not taking it, because it is a
single areal pattern and it doubles the verb on every yes/no question.

So the real choice was three-way: **intonation, a particle, or inversion.**

## 2. Inversion: the cleanest Rule 2 result in the project

**Rule 2 on GB260 (polar interrogation by special word order): LOST 8, KEPT 0.** Every creole
in the like-for-like set whose lexifier inverts has dropped inversion. Not one kept it. The
only comparable result anywhere in this project is Q9's negative particle at KEPT 13 / LOST 0
— and this is its mirror image, a feature universally shed rather than universally retained.

The by-people figure is the reason this needed checking at all. Inversion is **20.1% of world
L1 on 1.4% of languages**, which looks like a serious constituency until you see who:

| | L1 |
|---|---|
| Spanish | 485M |
| English | 379M |
| German | 76.5M |
| Dutch | 23.1M |
| Czech | 10.7M |
| Swedish, Danish, Frisian | 15.7M |
| Manggarai, Palauan | 0.9M |

**Every speaker of it but a million is European.** This is the exact shape the Rule 2
contrapositive was written to catch: a Euro-coded feature with a big population number,
which the European-lexifier creoles themselves refuse to reproduce. Contact languages agree
directly too — **0 of 9 restricted pidgins, 0 of 9 expanded pidgins**, 2 of 54 creoles.

**Rejected.** It would also have been the worst structural fit available: word order is the
only thing marking argument roles in this grammar (Tier 0), and inversion is a rule whose
sole job is to disturb it.

## 3. Particle over intonation — and the two sources that look contradictory

**This needs care, because WALS and Grambank appear to disagree by a factor of twelve and do
not actually disagree at all.**

| | %lang | **%L1** |
|---|---|---|
| WALS 116A — intonation-only is the **dominant** strategy | 18.2 | **6.2** |
| Grambank GB257 — intonation alone **can** mark a polar question | 51.0 | **77.4** |

Both are true. **Rising intonation is available almost everywhere and is the primary marker
almost nowhere.** Any write-up quoting one figure without the other misleads, and the script
docstring says so.

The contact record is as unanimous as anything we have seen:

| | restricted pidgin | expanded pidgin | creole |
|---|---|---|---|
| **only interrogative intonation** | **9 of 9** | 7 of 9 | 41 of 54 |
| final question particle | 0 | 1 | 4 |
| initial question particle | 0 | 1 | 4 |
| particle in another position | 0 | 0 | 4 |
| interrogative word order | 0 | 0 | 2 |

**Decision: a particle, against 9 of 9 restricted pidgins.** This is a **standing rule 6
departure** ([`grammar-plan.md`](grammar-plan.md) §5) — the contact record is evidence about
what *emerges* among speakers, not what is *learnable when taught* — and the reason is
specific rather than general:

1. **Pidgins are not written.** Intonation is free when you have a voice and worth nothing on
   a page. We have `?` from §3.7, so writing is covered, but a language whose *spoken* yes/no
   marking has no segmental content asks every learner to produce a prosodic contrast.
2. **Prosody is the least transferable thing across L1s.** A speaker whose language marks
   polar questions with a final particle has no reason to produce a rising contour, and no
   way to hear that one was expected. Every other decision in this grammar has been made to
   avoid exactly this kind of invisible requirement.
3. **A particle is the world's dominant strategy anyway** — 66.4% of L1, the majority option
   for once.
4. **Intonation remains available**, as it is in the 77.4% of L1 that can use it alongside a
   particle. We are not banning it; we are declining to make it load-bearing.

Rule 2 is consistent with keeping intonation available: **intonation-only is KEPT 9, GAINED 3,
LOST 1** across the creole/lexifier pairs.

## 4. Position: the modifier rule makes a prediction, and this time the data mildly disagrees

**Q9 was a test the modifier rule passed.** Negation was predicted preverbal and the contact
record and the world both confirmed it. **Q10 is a test where the rule and the data pull
apart, and we followed the rule.** That is worth stating plainly rather than smoothing over.

The rule says a single-word modifier precedes what it modifies (§3.2), and Q9 added that
scope is linear with the leftmost modifier widest. A polar question particle modifies the
whole clause and has the widest scope of anything in it, so **both rules predict
clause-initial.**

The data leans the other way:

| | %lang | **%L1** | share of *particle-having* L1 |
|---|---|---|---|
| final | 35.3 | 33.7 | **51.1%** |
| initial | 14.4 | 26.4 | 40.0% |
| second position | 6.0 | 4.1 | 6.2% |
| either of two positions | 3.0 | 1.4 | 2.1% |
| (no question particle) | 40.5 | 34.0 | — |

And **Rule 2 leans final too: a clause-final particle is GAINED 5 / LOST 0, while a
clause-initial particle is GAINED 2 / LOST 2.** Creoles that acquire a question particle
tend to acquire a final one. APiCS is split evenly (creoles: 4 initial, 4 final, 4 other).

**Decision: clause-initial. This is the weakest call in the study**, and it is a consistency
choice over a modest population margin (51:40 among particle-having L1), not a reading of the
evidence. Three things hold it up:

- Following the scope rule costs nothing to state; breaking it costs an exception a learner
  must memorise, in the one part of the grammar (§3.2 Q9) where scope is otherwise perfectly
  regular.
- **Early signalling**, which matters more here than in most languages because of §5: with
  the particle on content questions too and question words in situ, a final particle would
  put the only clause-typing signal *after* everything it was supposed to prepare the
  listener for.
- The margin is 11 points of L1, the smallest gap this project has overridden.

## 5. Content questions: in situ, and the particle stays

| | restricted pidgin | expanded pidgin | creole |
|---|---|---|---|
| interrogative phrase **initial** (fronted) | 5 of 9 | 3 of 9 | **46 of 54** |
| interrogative phrase **not initial** (in situ) | 4 of 9 | **6 of 9** | 8 of 54 |

| the world | %lang | **%L1** |
|---|---|---|
| WALS 93A — **not** initial | **68.0** | **66.5** |
| WALS 93A — initial | 29.4 | 31.5 |
| GB326 — content interrogatives normally/frequently in situ | 53.3 | **62.4** |

**Decision: in situ.** *You like what?* The question word sits where the noun would have sat.

- It is the world majority on both counts and the expanded-pidgin lean.
- **It costs zero rules.** Fronting is a movement rule, and movement is the last thing to buy
  in a language where linear position is the only marker of who did what to whom. English can
  front only because it has inversion to disambiguate *who did you see* from *who saw you* —
  and §2 just rejected inversion.
- **Rule 2 never loses it: GAINED 4, KEPT 3, LOST 0.**

**The creole column and the Rule 2 column look contradictory and are not.** APiCS 12 says
46 of 54 creoles front; GB326 says no creole lost in-situ and four gained it. The two code
different things — APiCS asks the *normal* position, GB326 asks whether in-situ is *normal or
frequent*. A creole can front by default and still permit in-situ freely, and evidently many
do. The honest summary is that creoles front because their lexifiers front, while pidgins and
the world at large do not, and the nativisation gradient is the same one Q8 found in pronoun
case.

### The particle goes on content questions too

**No source in this project codes this.** All twelve Grambank features are scoped to *polar*
interrogation explicitly and GB326 covers only position, so whether a language with a polar
particle also uses it in content questions cannot be measured here. From examples, the
majority pattern is **polar-only** (Mandarin *ma*, Turkish *mI*, Russian *ли*, Polish *czy*,
Thai, Vietnamese), and the "both" pattern clusters in **in-situ languages with a sentence-final
marker** — Japanese *ka*, Korean's interrogative endings, Malay/Indonesian *-kah*, optionally
Tagalog *ba*.

**Decision: the particle appears on every question.** One rule — *a question begins with the
question particle* — instead of two mechanisms with a conditional between them:

- **In-situ has a late-signal problem and the initial particle fixes it.** *You like what?* is
  indistinguishable from a statement until the final word.
- **It is not really double-marking.** Q9's "negate once" precedent looks like it argues the
  other way, but negative concord is two words that both mean *not*. Here the particle means
  "this is a question" and the interrogative word means "this is the gap" — one job each,
  which is *more* compositional, not less.
- **It removes a conditional.** "Use the particle, except when there is a question word" is a
  rule a learner can get wrong; "questions start with the particle" is not.

**With a descriptive note, not a prescription:** many speakers will drop the particle when an
in-situ question word is present. That is **tolerated, not an error worth correcting.** It
loses nothing — the question word already disambiguates, which is exactly why polar-only is
the world's majority pattern — so the standard form marks twice and casual speech marks once.
This is the first *descriptive* statement in the grammar rather than a prescriptive one.

## 6. The interrogative words: build them, don't list them

APiCS 19 asks whether a language lists its interrogatives or composes them:

| | restricted pidgin | expanded pidgin | creole |
|---|---|---|---|
| all simple words | 1 of 9 | 2 of 9 | 17 of 54 |
| one compound expression | **5 of 9** | 0 | 13 |
| two compound expressions | 0 | 3 | 14 |
| three compound expressions | 0 | **4 of 9** | 5 |
| four compound expressions | 2 | 0 | 6 |

**Only 1 of 9 restricted pidgins has an all-simple set.** Adults building a language derive
*where* from *what-place* and *when* from *what-time* rather than memorising a closed class.
§3.6 makes compounding FIRM and free, so this is available to us in a way it is not to every
language in the sample.

**Decision: one interrogative root — "what" — general on its own**, exactly as English uses
*what* for an unspecified thing, with *what-person*, *what-place*, *what-time*, *what-reason*,
*what-manner* built by compounding from ordinary nouns.

**Count/mass in interrogative quantifiers** (*how many* vs *how much*, GB325) is 18.3% of
languages but **59.1% of L1** — one of the sharper by-language/by-people reversals in the
project, and it dissolves under the compositional scheme: *what-number* and *what-amount* are
available without being obligatory. **Rule 2 is one-directional here too: LOST 5, KEPT 0** —
every creole whose lexifier had the distinction dropped it.

**Interrogative verbs** (GB324, "to do-what") are 11.3% of languages, 6.7% of L1, and 0 of 12
contact pairs. Not considered further.

---

## 7. What this decides

| | decision |
|---|---|
| polar questions | **one clause-initial particle**, "is it the case that…?" |
| intonation | permitted, never required |
| inversion | **rejected** — Rule 2 LOST 8 / KEPT 0, and 99% of its speakers are European |
| content questions | **question word in situ** |
| particle in content questions | **yes** — one rule, no conditional |
| dropping it before a question word | **tolerated**, non-standard, not an error |
| interrogative words | **one root, "what"**; the rest by compounding |
| count/mass | not grammaticalised — *what-number* / *what-amount* available, never required |

**Word bill: 2** (the particle and the interrogative root). **Tier 2 closes at 10** — Q6 zero,
Q7 zero, Q8 seven, Q9 one, Q10 two. Against ~180 cluster-free monosyllables avoiding the
discouraged onsets, the whole of Tier 2 is under 6% of the short-word space.

**Grammar rules added: one** — *a question begins with the question particle*. Position falls
out of §3.2's modifier rule and Q9's scope rule; in-situ is the absence of a movement rule
rather than the presence of anything.

---

## 8. Honest limits

- **9 restricted pidgins**, as everywhere in this project.
- **The particle itself overrides a 9-of-9 pidgin result.** The argument in §3 is about
  writing and prosodic transfer and it is an argument, not a measurement. It is a rule 6
  departure and is recorded as one.
- **Clause-initial position goes against the evidence**, mildly: 51:40 among particle-having
  L1, and Rule 2 GAINED 5 final vs 2 initial. We followed the internal scope rule instead.
  This is the item in Q10 most likely to be revisited, and unlike §3 there is no strong
  external argument on our side — only consistency.
- **Whether the particle appears in content questions is not codable from any source we have.**
  §5 is settled by design argument plus a handful of language examples, and the examples are
  from general knowledge rather than from a dataset in this repo.
- **The Grambank polar features are non-exclusive** ("can the language do X?"), so they do not
  sum to 100 and cannot be read as a partition. Only WALS 116A partitions, on n=941.
- **APiCS 12 and GB326 disagree in appearance** for the reason given in §5; a reader taking
  either at face value alone would draw a different conclusion about creole fronting.
