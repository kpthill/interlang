# Tier 2 Q9: negation

*Study run 2026-08-05. Script: [`../scripts/grammar_tier2_negation.py`](../scripts/grammar_tier2_negation.py) ·
output: `data/processed/grammar_tier2_negation.csv` · agenda:
[`grammar-plan.md`](grammar-plan.md) §4 Q9 · evidence policy: same file §5.*

**Bottom line up front.** **One negator, a free word, immediately before the verb, used for
everything** — verbal, locational, existential and nominal predication, and the prohibitive
too. No bipartite negation, no dedicated negative pronouns, no change to TAM marking. And
**the Q6 scope debt is paid**: scope is linear order, leftmost is widest.

This is the first question where the answer costs a grammatical word. **Word bill: 1.**

---

## 1. The modifier rule made a prediction, and it held

Q11 says modifiers precede their head, and a negator modifies the verb — so the modifier
rule *predicts* preverbal negation. A prediction that failed here would have been evidence
against the modifier rule itself, so this is a real test rather than a formality.

| position of standard negation | restricted pidgin | expanded pidgin | creole |
|---|---|---|---|
| **before the verb** | **6 of 9** | **6 of 9** | **46 of 54** |
| after the verb (immediately, or after the object) | 3 | 3 | 5 |
| bipartite | 0 | 0 | 4 |

World, WALS 143A (n=1,298): **NegV 39.4% of languages but 68.7% of L1** and 74.3% of total
speakers. The by-language/by-people gap runs the same way as everywhere else in this project.

**Prediction confirmed.** Negation is preverbal in every stratum and for two-thirds of
humanity. The modifier rule survives its first test outside the noun phrase.

## 2. A free word — and here the majority strategy is the one we can use

| | % languages | **% of world L1** |
|---|---|---|
| **negation by a non-inflecting word (particle)** — Grambank GB299 | 65.4 | **84.2** |
| negative particle — WALS 112A | 43.2 | **76.4** |
| negation by an affix/clitic — GB107 | 46.9 | 36.8 |
| negative affix — WALS 112A | 34.2 | 15.8 |
| negation by an inflecting auxiliary — GB298 | 11.4 | 9.0 |

Contact languages are near-unanimous: a **negative particle** in **8 of 9** restricted
pidgins, **9 of 9** expanded pidgins, 48 of 54 creoles. **Rule 2 is as clean as it gets —
the negative particle is KEPT 13, LOST 0** across the creole/lexifier pairs, while the
affixal strategy is LOST 6 / GAINED 1.

**This is worth contrasting with Q7's plural marker.** There, the world's dominant strategy
was a *suffix* (84.7% of L1), Tier 0 forbids affixes, and we had to take the 5.2% minority
option. Here the dominant strategy **is** a free word (84.2% of L1), so our no-affix
constraint costs nothing at all. Not every consequence of the isolating decision is a
sacrifice.

## 3. One negator for everything

**GB140 asks the learnability question directly**: is verbal predication negated by the same
negator as locational, existential *and* nominal predication? **50.0% of languages, 71.6% of
world L1.** One rule instead of four, and it is what most people already have. Rule 2 is
mildly positive (GAINED 4, KEPT 4, LOST 3).

**The prohibitive is the one place the contact record and the world frequency pull apart,
and the coding matters.** Grambank GB139 says the prohibitive differs from declarative
negation in 74.4% of languages and **83.5% of L1** — which looks decisive against us. But
GB139 counts *any* difference, including a special imperative construction with an ordinary
negator. WALS 71A separates the two dimensions:

| | % languages | **% of L1** |
|---|---|---|
| normal imperative + **special** negative | 36.8 | 46.2 |
| special imperative + **special** negative | 29.5 | 8.5 |
| normal imperative + **normal** negative | 22.8 | 23.3 |
| special imperative + **normal** negative | 11.0 | 22.1 |

Read on the dimension that concerns us — *is the negator itself special?* — it is
**54.7% of L1 special against 45.4% normal**, not the 5:1 GB139 implies. And contact
languages use the ordinary negator: **7 of 8 restricted pidgins** and 6 of 9 expanded
pidgins are "normal imperative construction and normal negator".

**Decision: the same negator negates commands.** Close to an even split by population, the
pidgin evidence points one way, and it saves a word and a rule. Flagged because it is the
weakest call in this study.

## 4. Rejected, with numbers

**Bipartite negation** (French *ne…pas*): **0 of 9 restricted pidgins, 0 of 9 expanded
pidgins**, 3–4 of 54 creoles. World: WALS double negation 10.2% of languages but **2.6% of
L1**; obligatory double negation 8.6% / 2.5%. A European speciality that adults building a
language never reproduce.

**Dedicated negative pronouns** (*nobody*, *nothing*). WALS 115A says that where they exist,
82.4% of languages (66.3% of L1) *also* negate the predicate — "nobody didn't come" — and
APiCS agrees (7 of 7 restricted pidgins co-occur). So the common pattern is to mark negation
twice for one semantic negation. **We negate once**: there are no negative pronouns, and
"nobody came" is *not came any-person*. This dissolves the concord question rather than
answering it, removes a closed class, and keeps one negator doing one job.

## 5. Negation does not disturb TAM

| TAM marking in negated clauses | restricted pidgin | expanded pidgin | creole |
|---|---|---|---|
| **same** | 4 of 9 | **6 of 9** | 35 of 51 |
| reduced | 2 | 0 | 8 |
| different | **0** | 3 | 6 |

Unchanged from the Q6 run: no restricted pidgin uses different TAM marking under negation,
and "same" is the plurality in every stratum. With TAM lexical (Q6) this is close to
tautological for us — adverbs do not inflect — but it confirms that nothing about negation
should perturb the rest of the clause.

## 6. The Q6 scope debt, paid

Q6 made TAM lexical, which created an ambiguity a fixed particle slot would have prevented:
*I not run in-the-past* could be **not(ran in the past)** or **(not ran) in the past**. That
was logged as the sharpest accepted cost of the decision.

**Resolution: scope is linear order, and the leftmost modifier is the widest.** The negator
sits in the same preverbal modifier zone as everything else, and each modifier scopes over
what follows it:

| | |
|---|---|
| *mi **no** **paste** kuru* | "it is not the case that I ran in the past" |
| *mi **paste** **no** kuru* | "in the past, I did not run" |

No new machinery: it uses the modifier position Q11 already fixed, and it generalises to any
two stacked modifiers rather than being a special rule about negation. The ambiguity is not
merely resolved — it becomes an **expressive distinction** the language can make and English
cannot without restructuring.

*(The forms above are placeholders for illustration; the lexicon stage will choose actual
words.)*

---

## 7. What this decides

| | decision |
|---|---|
| form | a **free word**, not an affix |
| position | **immediately before the verb** (the Q11 modifier zone) |
| coverage | **one negator** for verbal, locational, existential and nominal predication |
| prohibitive | **the same negator** — weakest call in the study |
| bipartite negation | **no** |
| negative pronouns | **none** — negate once, use "any" |
| TAM interaction | **none** |
| scope | **linear: leftmost modifier is widest** |

**Word bill: 1** (the negator) — the first grammatical word the grammar has required. Q6
and Q7 each cost zero.

**Grammar rules added: zero.** Position comes from Q11's modifier rule, scope comes from
linear order, and "one negator for everything" is the absence of a rule rather than the
presence of one.

---

## 8. Honest limits

- **9 restricted pidgins**, again, and on the prohibitive only 8 have a value.
- **The prohibitive decision goes against a slim population majority** (54.7% of L1 have a
  special negator) on the strength of 7 pidgins and a simplicity argument. It is the item in
  this study most likely to be revisited.
- **GB139 and WALS 71A genuinely disagree** because they code different things; this
  write-up uses WALS's finer split and says so, but a reader taking GB139 at face value
  would reach a different conclusion.
- **Scope-by-linear-order is a design decision, not a finding.** No source codes the relative
  order of negation and TAM adverbs, so §6 is an argument that fits the evidence rather than
  a result drawn from it.
- **WALS 115A rests on 204 languages**, the smallest sample used here.
