# Tier 2 Q11 + Q7: noun-phrase order, and what the noun carries

*Study run 2026-08-05. Script: [`../scripts/grammar_tier2_np.py`](../scripts/grammar_tier2_np.py) ·
output: `data/processed/grammar_tier2_np.csv` · agenda:
[`grammar-plan.md`](grammar-plan.md) §4 Q11, Q7 · evidence policy: same file §5.*

**Bottom line up front.** **Every single-word modifier precedes its head; clausal modifiers
follow.** Three independent lines agree: restricted pidgins put the modifier first on all
four relations (§1), **every attested change in adjective order runs N-Adj → Adj-N, 14 to 0**
(§1.1), and modifier-first is the harmonic pattern that 86% of the world's L1 mass already
speaks (§2). One rule, and by Patrick's parallel-modifier principle it settles **adverb
placement (Q11a) at the same time** — adverbs precede the verb. Tier 0's three coin flips
were an artefact of pooling: stratified by contact type, **modifier-first wins in every
stratum**, and it is what **86% of the world's L1 mass** already has. On Q7 the noun carries
almost nothing: **no articles, no classifiers, optional number.**

---

## 1. Tier 0's coin flips were a pooling artefact

Tier 0 reported adjective, numeral and possessor order as 8:7, 8:7, 8:7 among
non-European-lexifier creoles and concluded there was no creole signal. Re-cut by contact
type — the stratification we only adopted afterwards — the signal is clear:

| | restricted pidgin | expanded pidgin | creole | WALS by language / **by L1** |
|---|---|---|---|---|
| **adjective** | **8 : 1** Adj-N | 6 : 3 Adj-N | 36 : 18 Adj-N | N-Adj 64.6% / Adj-N **65.3%** |
| **numeral** | **7 : 2** Num-N | 6 : 3 Num-N | 51 : 3 Num-N | N-Num 52.7% / Num-N **89.5%** |
| **demonstrative** | **6 : 2** Dem-N | 5 : 5 tie | 34 : 19 Dem-N | N-Dem 46.0% / Dem-N **86.1%** |
| **possessor** | **7 : 2** Possessor-first | 3 : 6 head-first | 23 : 32 head-first | Gen-N 54.6% / Gen-N **50.0%** |

**Restricted pidgins — the closest analogue to our use case — put the modifier first on all
four.** Expanded pidgins and creoles agree on the first three and flip on the possessor,
which is the weakest of the four and the only one where the strata disagree.

The by-language/by-people reversal Tier 0 flagged is confirmed and is large: N-Num leads by
language count (52.7%) while Num-N leads by people (**89.5%**), a 37-point flip;
demonstratives flip by 42 points. §2 of [`principles.md`](principles.md) says count people.

### 1.1 Rule 2, directional: when adjective order changes, it changes one way

Asked as a spot-check and it turned out to be the strongest single result in the study.
Taking every contact language whose lexifier has a WALS 87A value (62 languages; Bantu and
the "Other" lexifiers have no clean WALS entry and are dropped rather than guessed):

| the lexifier's own order | CHANGED | SAME |
|---|---|---|
| **Adj-N** (English, Dutch) | **0** | 29 |
| **N-Adj** (French, Portuguese, Spanish, Malay, Arabic) | **14** | 19 |

**All 14 changes are N-Adj → Adj-N. Not one goes the other way.** No contact language with an
Adj-N lexifier has ever moved off it; 42% of those with an N-Adj lexifier moved to Adj-N.
The movers: Palenquero, Louisiana Creole, Reunion Creole, Tayo, Cape Verdean (Santiago),
Casamancese, Korlai, Diu Indo-Portuguese, Sri Lanka Portuguese, Sri Lankan Malay, Singapore
Bazaar Malay, and all three Chabacano varieties.

**Caveats, and they matter.** Several of these have **Adj-N substrates** — the South Asian
Portuguese creoles (Tamil, Sinhala, Gujarati, Marathi) and Sri Lankan/Bazaar Malay — so
substrate transfer explains part of the drift rather than any general adult preference. But
not all of it: **Palenquero, Louisiana Creole, Reunion Creole, Cape Verdean and Casamancese
moved to Adj-N with substrates that are themselves N-Adj** (Kikongo, West African, Malagasy).
Those are the cases where the change cannot be inheritance from either side. Also note French
has a prenominal adjective subclass, so French-lexifier creoles may be generalising a pattern
that was already partly there.

Even discounted for substrate, a 14:0 directional asymmetry is a real signal, and it is
independent evidence for the same conclusion the harmony test reaches below.

---

## 2. The harmony test — is "one modifier rule" natural or invented?

This is the analysis that decides whether Patrick's parallel-treatment principle copies the
world or imposes on it. Within a single language, do adjective, numeral and demonstrative sit
on the **same side** of the noun? Grambank codes all three on one scale, so it is a
like-for-like comparison inside each language. 1,297 languages are committed on all three
(a definite value, not "both orders").

**867 of 1,297 (67%) put all three on the same side — and those languages are 91% of the L1
mass in the sample.** Harmony is the norm, not a designed tidiness.

| pattern (adjective / numeral / demonstrative) | languages | % languages | **% of L1** |
|---|---|---|---|
| N-Mod / N-Mod / N-Mod | 559 | 43.1 | 4.5 |
| **Mod-N / Mod-N / Mod-N** | 309 | 23.8 | **86.1** |
| the six disharmonic patterns | 429 | 33.1 | 9.4 |

Pairwise agreement is 77–79% for every pair, so no one modifier is the odd one out.

**Two things fall out.** One rule for modifier position is what two-thirds of languages
already have, so adopting it is not an invented regularity. And of the two harmonic options,
**modifier-first is the one 86% of humanity already speaks** — despite being the *minority*
by language count (23.8% against 43.1%). This is the single largest by-language/by-people
divergence anywhere in the project.

## 3. Q11 decision: modifiers precede, clauses follow

**All single-word modifiers precede their head.** Adjective, numeral, demonstrative and
possessor all come before the noun.

**Clausal modifiers follow.** The relative clause was already settled in Tier 0 (N-Rel, 12 of
15) and is unchanged. The combination is principled rather than inconsistent: short
modifiers before, heavy constituents after, is the standard processing-efficiency pattern
and is what both English and the creole record do.

**Caveat on the possessor.** It is the weakest of the four — expanded pidgins and creoles
prefer head-first, and only restricted pidgins and a slim world majority (54.6% by language,
50.0% by L1) support possessor-first. It is adopted for **uniformity**, not because the
evidence demands it. If any part of §3 gets revisited, this is the part.

### 3.1 Q11a falls out: adverbs precede the verb

By the parallel-modifier principle — *modifiers behave the same way whatever they modify* —
**adverbs precede the verb**, and the whole of Q11a is answered without a separate study.
One rule covers both: *big house*, *three house*, *this house*, and *quickly run*,
*already run*, *in-the-past run*.

**The pleasing consequence: TAM lands preverbally after all.** Q6 declined a preverbal TAM
particle slot on grounds of uniformity — and uniformity applied to modifiers now puts the
TAM adverbs in exactly that position. *I in-the-past continuously run*, not Patrick's
original *I run continuously in-the-past*. The taste-based choice and the evidence
reconverge: 7 of 9 expanded pidgins put their TAM markers immediately preverbally, and so do
we, by a different route and without a closed class.

This is worth stating plainly because it also **retires one of Q6's accepted costs**: the
"no positional cue for where the predicate begins" objection is much weaker if modifiers
reliably precede their head, since a run of preverbal modifiers is itself the cue.

---

## 4. Q7: what the noun carries — almost nothing

### 4.1 No articles

| | restricted pidgin | expanded pidgin | creole |
|---|---|---|---|
| **definite article distinct from demonstratives** | **0 of 9** | 4 of 9 | 33 of 57 |
| definite article *identical to a demonstrative* | **5 of 9** | 0 | 16 of 57 |
| neither definite nor indefinite article | 4 of 9 | 3 of 9 | 1 of 57 |
| **indefinite article identical to numeral 'one'** | **4 of 9** | 4 of 10 | 36 of 54 |
| indefinite article distinct from 'one' | **0 of 9** | 2 of 10 | 17 of 54 |

**No restricted pidgin has a dedicated article of either kind.** Where they mark definiteness
at all they use the **demonstrative** (5 of 9); where they mark indefiniteness they use the
numeral **'one'** (4 of 4 that have anything). World: 38.0% of languages have a definite
article (36.1% of L1) and only 13.8% an indefinite one (24.0% of L1); WALS 37A puts "no
article at all" at 32.1% of languages.

**Rule 2 is split and the split is informative.** Definite articles are **KEPT 8, LOST 1** —
European-lexifier creoles hold on to them. Indefinite articles are **LOST 9, KEPT 1,
GAINED 1** — the strongest Rule 2 signal in this study. Read together: a definite article is
*retained when inherited but never invented*, and an indefinite article is actively shed.

**Decision: no articles.** Definiteness is carried by the demonstrative when it matters,
indefiniteness by 'one'. Both words exist regardless, so this costs **zero vocabulary** and
removes an obligatory choice from every noun phrase.

### 4.2 Number is optional

| | restricted pidgin | expanded pidgin | creole |
|---|---|---|---|
| no plural marking | **4 of 9** | 0 | 1 of 57 |
| variable (optional) plural marking | **5 of 9** | 5 of 9 | 46 of 57 |
| invariant (obligatory) plural marking | **0 of 9** | 4 of 9 | 10 of 57 |

**No restricted pidgin marks plural obligatorily.** Optional marking is the contact-language
norm at every level. In the world, 55.9% of languages have productive plural morphology
(61.1% of L1), but the *strategy* matters for us: WALS 33A gives plural **suffix** 48.1% of
languages and **84.7% of L1**, against a plural **word** at 16.0% / 5.2%. We have no
suffixes (Tier 0), so the majority strategy is unavailable and the minority one is what is
left.

**Decision: number is optional.** A bare noun is number-neutral; a separate plural word is
available when the count matters and is omitted otherwise. Rule 2 is neutral here (KEPT 6,
LOST 5, GAINED 0), which is consistent with "not something adults reach for, not something
they fight to keep".

### 4.3 No numeral classifiers

| | restricted pidgin | expanded pidgin | creole |
|---|---|---|---|
| no numeral classifiers | **8 of 9** | **9 of 9** | 51 of 54 |

**This is the one place we vote against a large population deliberately.** Numeral
classifiers are native to **36.4% of the world's L1 mass** (Grambank; WALS 55A puts
obligatory classifiers at 46.8% of L1 in its smaller sample) — the Sinosphere plus much of
South and Southeast Asia. And contact languages reject them almost totally: **68 of 72**
have none, including 9 of 9 expanded pidgins, and Rule 2 shows ABSENT 10, KEPT 2, LOST 1.

A feature that a third of humanity has natively and that adults building a shared language
essentially never adopt is exactly the case our two objectives pull apart on. The contact
evidence wins because grammar is optimised for learnability alone
([`grammar-plan.md`](grammar-plan.md) §1), but **this is the clearest instance so far of a
decision that a very large group will find unfamiliar**, and it should be reported as such
in the final bias audit rather than buried.

---

## 5. What this decides, and the running bill

| | decision |
|---|---|
| adjective, numeral, demonstrative, possessor | **precede the noun** |
| relative clause | follows the noun (Tier 0, unchanged) |
| **adverbs** | **precede the verb** — Q11a, by the parallel-modifier principle |
| definite article | **none** — use the demonstrative |
| indefinite article | **none** — use 'one' |
| number | **optional**; bare noun is number-neutral, separate plural word available |
| numeral classifiers | **none** |

**Particle bill: still 0.** Q7 adds no grammatical words at all — the demonstrative, 'one'
and the plural word are ordinary vocabulary, and the first two exist regardless.

**Grammar rules added: one.** "Modifiers precede their head; clauses follow it." It replaces
what would have been four NP-order facts plus a separate adverb-placement rule.

---

## 6. Honest limits

- **9 restricted pidgins** carry the stratum that most of §1 and §4 leans on. Every claim
  about them is a claim about nine languages.
- **The harmony test uses Grambank's three-way scale**, and dropping the "both orders" value
  removes languages with genuinely free order — 1,297 of ~2,100 remain. Free-order languages
  are neither harmonic nor disharmonic, and excluding them may make harmony look slightly
  more dominant than it is.
- **The possessor decision is uniformity, not evidence** (§3), and is the weakest link.
- **Adjective order is the least population-lopsided of the three** (Adj-N 65.3% of L1
  against Num-N 89.5% and Dem-N 86.1%), so the harmonic rule is carrying it more than its own
  numbers are.
- **"Modifier" is doing work that needs defining.** Q11a extends the rule from noun modifiers
  to verb modifiers on a principle, not a measurement — no source codes "adverb position" the
  way it codes adjective position, so the parallel is an argument rather than a finding.
