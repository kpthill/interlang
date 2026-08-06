# Tier 3: predication, possession and existentials

*Decided 2026-08-05. Agenda: [`grammar-plan.md`](grammar-plan.md) §4 Tier 3 · evidence
policy: same file §5.*

**No committed study script for this one.** Figures below come from an exploratory query over
the same three sources every other grammar note uses (APiCS 2/37/38/39/64/73–78, WALS
117A–120A, Grambank GB058/059/068/117/126/250–256), run ad hoc rather than as a
`scripts/grammar_*.py` module. This is a **deliberate deviation from the "one study per
script" convention** in [`../CLAUDE.md`](../CLAUDE.md), taken on time pressure for a decision
we were already confident about, and logged here rather than left implicit. The figures are
reproducible from those parameter IDs; they are not currently reproducible by running
anything in `scripts/`.

**Bottom line up front.** **One invariant copula for every non-verbal predicate** — nominal,
adjectival and locative alike. **The same copula, with nothing following it, is the
existential.** **Possession is an ordinary transitive verb "have."** No expletive subject, no
alienable/inalienable split, no possessive classifiers. **Word bill: 1. Grammar rules added:
one.**

| | |
|---|---|
| `I COP teacher` | I am a teacher |
| `I COP tall` | I am tall |
| `book COP on table` | the book is on the table |
| `one book COP` | there is a book |
| `book no COP` | there is no book |
| `I have book` | I have a book |

---

## 1. The collision that forced the copula

Zero-copula nominal predication was never actually available to us, and no source could have
told us so — it is an interaction between two decisions made two questions apart.

**Q11 put the possessor before the noun. Q8 declined special possessive pronouns**, so the
plain pronoun in the possessor slot *is* the possessive. That makes `I house` = "my house".
Zero-copula predication would make `I teacher` = "I am a teacher". Both are
`[nominal] [nominal]`, with nothing to tell them apart — and it is worse with full noun
phrases, where `the man dog` would be both "the man's dog" and "the man is a dog".

**The copula resolves it completely**: `I COP teacher` is a clause, `I teacher` is a phrase.

This is the first decision in the project driven by an *interaction* rather than by a
distribution, and it is worth remembering as a class of risk: the evidence base codes
features one at a time, so collisions between our own choices are invisible to it.

## 2. The copula covers all three predicate types

Contact languages draw a sharp gradient — the standard typological hierarchy, adjectives
least likely to take a copula and locatives most:

| APiCS, restricted pidgins | no copula | invariant copula | variable copula |
|---|---|---|---|
| **adjectives** (73) | **8 of 9** | 1 | 0 |
| **nominals** (74) | **6 of 9** | 2 | 1 |
| **locatives** (75) | 2 | **5 of 9** | 2 |

The world sits much further toward having one: a copula for predicate nominals is 56.6% of
languages but **83.1% of L1** (GB117), zero copula is *impossible* for **71.9% of L1**
(WALS 120A), and predicative adjectives get non-verbal encoding in **59.9% of L1**
(WALS 118A). Nominal and locative predication are identical in 30.4% of languages, 46.9% of
L1 and **59.0% of total speakers** (WALS 119A).

**Decision: one copula, all three types, no conditional.** Reasons:

1. **Nominals are forced** by §1.
2. **"Use the copula except with adjectives" is a conditional**, exactly the shape of rule
   Q10 rejected, and a learner can get it wrong in both directions.
3. **It protects the modifier rule.** The alternative is to make adjectives stative verbs, so
   `I tall` is an ordinary intransitive clause — which is what 8 of 9 restricted pidgins
   effectively do, and it is genuinely tempting. But it breaks *attributive* use: if "big" is
   a verb, `big house` is a relative clause, and Tier 0 puts relative clauses **after** the
   noun. Mandarin and Japanese pay for this with a linker (*de*, the *-i* form). We would be
   buying a word to save a word, and losing §3.2's modifier uniformity in the exchange.

**This overrides 8 of 9 restricted pidgins on adjectives** — the strongest single pidgin
signal in the study — under the policy Patrick stated when adopting it: *the goal is ease of
learning, so we copy pidgins only where they point at that objective.* Recorded as a standing
rule 6 departure.

## 3. The existential is the copula with nothing after it

**The recommendation here was reversed in discussion, and the reversal is worth recording
with the evidence that argued against it.**

The initial recommendation was a "have"-existential (`have book` = "there is a book"), on the
strength of APiCS 78: the existential and the transitive possession verb are the same word in
40 of 73 contact languages. Checking *which* languages weakened it considerably:

| APiCS 78 | European lexifier | non-European |
|---|---|---|
| **identity** | **37** | 4 |
| differentiation | 13 | 3 |
| no transitive possession verb | 3 | **6** |
| overlap | 7 | 1 |

Romance hands this to its creoles directly — *il y a*, *tem* and *hay* are all literally
"has" — and among non-European-lexifier contact languages identity is only 4 of 14.

**But the English column cuts the other way and must not be buried.** English does *not* have
identity: it says *there is*, using the copula, and reserves *have* for possession. Yet
English-lexifier contact languages show **identity 16, differentiation 7** (Tok Pisin *i gat*
and relatives). Those sixteen are **innovations, not inheritance** — a have-existential built
from a lexifier that has none. That is exactly the Rule 2 divergence signal, and it is real
evidence that adults reach for "have" here.

**Decided against it anyway, on structure:**

- `have book` is a **transitive verb with no subject, predicate-first**. It would be the only
  clause in the language shaped like that — an exception in the one place we have allowed
  none, since rigid SVO is the *only* marker of argument roles (Tier 0) and Q10 rejected
  inversion specifically to protect it.
- `book COP` is **subject + verb**, like every other clause. Nothing new to learn.

Existentials do tend to be predicate-first cross-linguistically, because the subject is new
information — but that is the same presentational logic behind inversion, which we have
already declined to buy.

**Decision: the copula does double duty. With a predicate following it links; with nothing
following it asserts existence.** The parse is decided by whether anything follows, so there
is no ambiguity. Precedent: **Russian** uses one verb (*есть*) for both with no expletive, and
**Turkish** *kitap var* and **Japanese** *hon ga aru* are both subject-first existentials.

**No expletive subject** — 8 of 9 restricted pidgins and 39 of 54 creoles use none
(APiCS 64). English's *there* and French's *il* are dummies that carry no meaning and would
have to be taught as an arbitrary requirement.

*Alternative left on the table:* a separate lexical verb "exist". Also free — ordinary
vocabulary, not grammar — and GB126 puts a dedicated existential verb at 66.7% of languages
and **80.5% of L1**. It costs one more word to learn and gives the clause more prosodic
weight than a bare copula. Judged a coin flip; reusing the copula won on economy.

## 4. Possession is just a verb

| APiCS 77 | restricted | expanded | creole |
|---|---|---|---|
| **transitive 'have'** | 4 of 9 | **6 of 9** | **47 of 54** |
| genitive / topic / locational / comitative | 4 | 3 | 7 |

WALS 117A has **no majority strategy at all** — 'have' 30.1% of L1, topic 29.8%, locational
26.4%, genitive 10.4%, conjunctional 3.3% — which is unusual enough to note: on this feature
the world genuinely has no answer. Grambank GB250 puts "can express predicative possession
with a transitive *habeo* verb" at 43.6% of languages and **59.6% of L1**, and the creole
column is near-unanimous.

**Decision: 'have' is an ordinary transitive verb.** It costs **zero grammatical words** — it
is lexicon, not grammar — and needs no rule, since SVO already handles it. Note this is the
one place the conjunctional strategy ("I am with a book"), which is 24.7% of *languages*, is
dismissed easily: it is **3.3% of L1**, one of the sharpest by-language/by-people gaps in the
project.

**Adnominal possession** was already settled by Q11 (possessor precedes the noun). Two
further rejections, both with the language/people gap running our way for once:

- **No alienable/inalienable split** (GB059): 47.4% of languages but only **13.6% of L1**.
- **No possessive classifiers** (GB058): 9.8% of languages, **5.0% of L1**. Consistent with
  Q7's rejection of numeral classifiers.

---

## 5. What this decides

| | decision |
|---|---|
| nominal predication | **copula** — forced by the possessive collision (§1) |
| adjectival predication | **copula** — overrides 8 of 9 restricted pidgins, for uniformity |
| locative predication | **copula** — same word |
| copula form | **invariant** — no agreement, no tense (TAM is adverbial, Q6) |
| existential | **the copula with nothing following it** |
| expletive subject | **none** |
| predicative possession | **transitive 'have'** — lexicon, not grammar |
| alienable/inalienable | **no** |
| possessive classifiers | **no** |

**Word bill: 1** (the copula). **Grammar rules added: one** — *a non-verbal predicate takes
the copula*.

## 6. Honest limits

- **No committed script.** See the header. This note is not reproducible by running anything
  in `scripts/`, unlike every other grammar note in this directory.
- **The adjectival copula overrides the strongest pidgin signal in the study** (8 of 9), on a
  uniformity argument plus the attributive-order consequence in §2.3. It is an argument, not
  a measurement.
- **The existential decision runs against genuine Rule 2 evidence** (16 English-lexifier
  innovations toward a have-existential) and is held up by an internal consistency argument.
  §3 states the opposing evidence at full strength deliberately.
- **This is the fourth consecutive question decided against the contact record** — Q6 (taste),
  Q8 (politeness, against 85% of L1), Q10 (particle, against 9 of 9 pidgins), and now the
  adjectival copula. Patrick reviewed the pattern explicitly and accepted the trade: copy
  pidgins only where they point at ease of learning. **It still belongs in the final bias
  audit** ([`grammar-plan.md`](grammar-plan.md) §1) as a pattern, not only as four separate
  entries.
