# Tier 2 Q6: tense, aspect and mood

*Study run 2026-08-05. Script: [`../scripts/grammar_tier2_tam.py`](../scripts/grammar_tier2_tam.py) ·
output: `data/processed/grammar_tier2_tam.csv` · agenda:
[`grammar-plan.md`](grammar-plan.md) §4 Q6 · evidence policy: same file §2 and §5.*

**Bottom line up front.** TAM goes on **free preverbal particles**, the system is
**aspect-first with optional tense**, **one imperfective particle covers progressive and
habitual**, and **negation does not disturb any of it**. Recommended inventory: **three
particles**. Purely tense-based systems are essentially unattested in creoles (0 of 8, 1 of
76 including pidgins and European-lexifier cases).

**And a bias in our own instrument turned up, which matters beyond this study:** the
non-European-lexifier group that Rule 1 rests on is **37% pidgins** against 11% for the
European group. A pidgin has less grammar by definition, so any Rule 1 finding of the form
"creoles converge on *not* having X" is partly counting that skew. Every creole number
below is therefore reported twice — raw, and with pidgins excluded — and in this study the
exclusion **strengthens** three findings and weakens none.

---

## 0. The pidgin skew in the Rule 1 sample

| lexifier group | creoles | pidgins | % pidgin |
|---|---|---|---|
| European | 74 | 9 | 11% |
| **non-European** | **12** | **7** | **37%** |
| mixed | 2 | 0 | — |

Classification is rough — name contains "Pidgin", plus Fanakalo, Chinuk Wawa and Singapore
Bazaar Malay, which are pidgins whose names do not say so. It does not need to be precise
to make the point: the group we use as the bias control against European inheritance carries
a bias of its own, in the direction of *less grammar*. **This applies to every Rule 1 claim
in the project**, including Tier 0's, and should be run as a matter of course from now on.
It is now logged in [`grammar-plan.md`](grammar-plan.md) §5 as a standing rule.

---

## 1. What creoles do

Non-European-lexifier column only (Rule 1); the European column is the inheritance control.
"ex-pidgin" repeats the same count over creoles alone.

### 1.1 Position: preverbal

| | non-European | ex-pidgin | European |
|---|---|---|---|
| **immediately preceding the verb** | 6 | **5** | 38 |
| in a leftward position | 2 | 1 | 11 |
| immediately following the verb | 3 | 2 | 8 |
| in a rightward position | 1 | 0 | 2 |
| no TAM markers at all | 3 | 0 | 0 |

Raw, preverbal is only 40%; **excluding pidgins it is 6 of 8 (75%)**, against 2 postverbal.
Among European-lexifier creoles it is 49 of 59 (83%). Preverbal it is — which is also what
head-initial SVO predicts, so nothing is being traded here.

### 1.2 The famous creole TMA stack is rarer than its reputation

| internal order of T, A and M | non-European | ex-pidgin | European |
|---|---|---|---|
| **the feature does not apply** (they do not co-occur) | 14 | **7** | 40 |
| Tense-Mood-Aspect | 0 | 0 | 12 |
| Mood-Tense-Aspect | 0 | 0 | 3 |
| Tense-Aspect-Mood | 1 | 1 | 1 |

The Bickerton-style anterior/irrealis/non-punctual *sequence* shows up in **16 of 56**
European-lexifier creoles and **1 of 8** non-European creoles. The received wisdom overstates
it: what creoles converge on is a small preverbal **inventory**, not a three-slot template.
Where the stack does occur, **Tense-Mood-Aspect** is the attested order (12 of 16).

### 1.3 Aspect is compulsory, tense is not

| tense-aspect system | non-European | ex-pidgin | European |
|---|---|---|---|
| mixed aspectual-temporal | 6 | **5** | 48 |
| no or only one marker | 6 | 2 | 3 |
| purely aspectual | 3 | 1 | 7 |
| **purely temporal** | **0** | **0** | 1 |

**Not one non-European-lexifier creole has a purely temporal system**, and only one language
in the whole of APiCS does. Aspect is in every system that has anything; tense is the part
that comes and goes. Among true creoles the mixed system is the norm (5 of 8), so this is
not an argument for dropping tense — it is an argument for **aspect being the backbone and
tense the optional layer**.

### 1.4 One imperfective marker, not a progressive and a habitual

| what the habitual marker also covers | non-European | ex-pidgin | European |
|---|---|---|---|
| **no overt habitual marker** | 10 | **3** | 8 |
| habitual and progressive (same marker) | 3 | **3** | 4 |
| **only habitual** (a dedicated marker) | **0** | **0** | 21 |

**"Only habitual" is 0 of 9 outside the European group and 21 of 59 inside it** — one of the
cleanest Rule 2 contrasts in the study. Either there is no habitual marker, or it is the
progressive doing double duty. The progressive table agrees from the other side: among true
creoles, "progressive and habitual" ties "only progressive" at 3 each.

**Design consequence: one imperfective particle covering progressive *and* habitual.** Two
separate markers is a European-lexifier pattern.

### 1.5 Negation leaves TAM alone

| TAM marking in negated clauses | non-European | ex-pidgin | European |
|---|---|---|---|
| **same** | 8 | **5** | 38 |
| reduced | 2 | 2 | 8 |
| **different** | **0** | **0** | 9 |

Zero non-European-lexifier languages change their TAM marking under negation; nine
European-lexifier creoles do, inheriting French and English negation quirks. This settles
the dependency that Tier 2 Q9 (negation) was waiting on: **negation is a particle that
changes nothing else.**

---

## 2. What the world does — and the morphology/particle split matters

Grambank codes each category twice, as bound morphology and as a free particle, which lets
us ask the question that actually bears on our design: not "does the world mark tense?" but
"does the world mark tense *the way we would have to*?"

| | n | % languages | **% of world L1** | % total speakers |
|---|---|---|---|---|
| morphology: past tense | 2199 | 52.4 | 63.9 | 70.4 |
| morphology: perfective/imperfective | 2064 | 66.8 | **77.9** | 65.4 |
| morphology: mood | 1865 | 69.6 | 57.4 | 50.9 |
| **particle: mood** | 1553 | 40.0 | **51.1** | **58.1** |
| **particle: aspect** | 1615 | 38.1 | 31.9 | 26.5 |
| **particle: tense** | 1649 | 24.4 | **9.3** | **6.8** |
| *context:* multiple pasts/futures (remoteness) | 1867 | 31.8 | 32.2 | 32.4 |

**Mood is the category the world is most willing to put on a particle** (51–58% of people);
tense is the least (7–9%). That is a real asymmetry and it cuts against a tense-heavy
design for an isolating language.

**Does "no tense morphology" mean "no tense" or "tense elsewhere"?** The binaries cannot say
on their own, so crossing them:

| | particle = no | particle = yes |
|---|---|---|
| past-tense morphology = no | **506** | 301 |
| past-tense morphology = yes | 704 | 90 |

**506 of 1601 languages mark past tense neither way — 28.2% of the L1 mass in that subset.**
The same crossing for perfective/imperfective gives only 192 of 1518, **18.2%**. So roughly
**four times as much of humanity lives without dedicated past marking as without aspect
marking.** Tense really is the optional one, and this is measured rather than asserted.

*Recorded as considered and rejected:* graded/remoteness tense (multiple pasts or futures)
is present in 31.8% of languages and about a third of the L1 mass. It is a real option; it
is also an obvious complexity cost with no learnability argument behind it, and no creole
uses it.

---

## 3. Rule 2: creoles swap morphology for particles

The same 14 creole/lexifier pairs as Tier 0, scored on identical Grambank features on both
sides.

| | KEPT | LOST | **GAINED** | ABSENT |
|---|---|---|---|---|
| TAM by **morphology** | 7 | **17** | 6 | 35 |
| TAM by **particle** | 3 | 2 | **9** | 3 |

Per feature, particles only: **aspect particle gained 4, lost 0. Tense particle gained 4,
lost 0.** Mood particle is the one that was mostly already there (kept 3, gained 1, lost 2).

Split by lexifier family, the morphology→particle swap is carried by the European group
(morphology lost 13, kept 0; particles gained 8, lost 0) — unsurprising, since their
lexifiers had the morphology to lose. The non-European group is quieter (morphology lost 4,
kept 7; particles gained 1, kept 1, lost 2), which is the same Rule 1 limitation as Tier 0's
derivation finding: the swap is *demonstrated* where there was something to swap.

---

## 4. Recommendation

**Three preverbal particles, all optional, fixed order, invariant under negation.**

| particle | covers | evidence |
|---|---|---|
| **imperfective** | progressive *and* habitual, in one marker | §1.4 — "only habitual" is 0 of 9 outside Europe, 21 of 59 inside |
| **past / anterior** | past reference where context does not supply it | §1.3 — mixed aspectual-temporal is the creole norm (5 of 8); Rule 2 gains tense particles 4:0 |
| **irrealis** | future and conditional in one marker | §2 — mood is the category the world most readily puts on a particle (51–58% of people) |

Supporting decisions:

- **Preverbal**, immediately before the verb (§1.1: 6 of 8 creoles, 83% of European-lexifier
  creoles, and it is what head-initial SVO predicts).
- **Optional, not obligatory.** A bare verb is unmarked for both tense and aspect and takes
  its reading from context. This is the aspect-first design of §1.3, and it is what lets the
  particle count stay at three.
- **Order when they combine: Tense-Mood-Aspect** (§1.2 — 12 of the 16 languages that stack
  them). Stacking will be rare; the order exists so it is defined, not because it is common.
- **Negation changes nothing** (§1.5). One rule, not two.
- **No perfect, no remoteness distinctions, no separate habitual.** Each is attested
  somewhere and none is supported by the creole record.

**Particle bill so far: 3.** (Tier 2 running total, per the standing rule in
[`grammar-plan.md`](grammar-plan.md) §4 — every Tier 2 answer that costs a particle is
counted, because Tier 4 has to find phonological room for all of them under §3.3's segment
discouragement and §3.6's cluster cost.)

---

## 5. Honest limits

- **8 non-European-lexifier creoles** after excluding pidgins. That is the real n behind
  every Rule 1 number above, and it is small enough that a single re-coding could move a
  ratio.
- **The pidgin classification is by name**, plus three hand-added cases. It is good enough
  to demonstrate the skew, not good enough to be a variable in a model.
- **APiCS's "the feature does not apply"** for marker ordering conflates "has fewer than
  three marker types" with "has them but does not order them" — §1.2's conclusion is about
  the inventory, not the syntax, and should not be read as "creoles cannot stack markers".
- **Rule 2 on TAM is largely a European-lexifier result**, exactly as in Tier 0: the swap
  from morphology to particles can only be observed where the lexifier had morphology.
- **Grambank's particle features** ("can aspect be marked by a non-inflecting word?") are
  permissive — they say a strategy is *available*, not that it is the normal or obligatory
  one. The world percentages in §2 are therefore upper bounds on "this is how the language
  does it".
