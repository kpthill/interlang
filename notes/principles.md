# Interlang: principles, decisions, and findings

*Last updated 2026-08-05 (§3.2 grammar: Tier 0 SVO/prepositions/no case FIRM, modifier order and nominal categories FIRM, TAM lexical; §3.3 inventory FIRM; §3.5 stress decided; **§3.6 phonotactics now FIRM — syllable template, compounding, hiatus**; §3.7 orthography, punctuation, case and solid compounds all FIRM). Companion documents: [`data-audit.md`](data-audit.md) (dataset details, metric validation), [`cost-learning.md`](cost-learning.md) (learned substitution/epenthesis costs), [`../src/interlang/metric.py`](../src/interlang/metric.py) (recognizability metric v0).*

Each decision below is tagged:

- **FIRM** — committed; revisit only with strong new evidence.
- **SOFT** — current working position; expected to survive but pending data.
- **OPEN** — genuinely undecided; an experiment or discussion is planned.

---

## 1. Project goal

Design an easy-to-learn, globally unbiased international auxiliary language (IAL) by writing down explicit principles as optimization targets, then letting a program optimize the vocabulary — and inform the phonology choices — against databases covering approximately all of the world's languages.

The improvement over Esperanto is not "zero bias" (impossible) but bias that is **chosen, explicit, and measured** rather than unexamined. Esperanto's word stock and sound system are overwhelmingly European; we want every such tradeoff to be a deliberate, quantified decision.

**Honest expectation-setting:** the world's language families share almost nothing lexically. Absolute recognizability scores will be low for everyone. The real output of this project is a **measured tradeoff curve** — how much ease-of-learning you buy at what cost in representational fairness — not a language that magically feels familiar to all 8 billion people.

---

## 2. Guiding principles

### Two parallel objectives (FIRM)

1. **Ease of learning**, for as many people as possible. Weighted by **L2/total speaker counts** — "how many people are likely to recognize this word?" Counting second-language speakers pushes toward lingua-franca (English etc.) word stock, and that is intentional: an L2 English speaker really does know English words.
2. **Representation** — everyone should recognize *some* words as their own. Weighted by **L1 (native) speaker counts only**, so that big lingua francas don't double-dip.

### Loss shape (SOFT)

Proposed loss: an **absolute-error term** for ease (1) plus a **mean-squared-error term** for representation (2). The squared term makes the worst-represented groups dominate its gradient. Intuition: *use the most common words, but where there is no universal answer, make sure everyone is represented at least a little.*

### Representation as attribution, not similarity (OPEN)

Refinement under consideration: operationalize the representation term as **etymology attribution share** — what fraction of the lexicon traces to your language/family — rather than string similarity. Similarity-based representation saturates near zero for speakers of small languages no matter what we do, so it provides almost no gradient exactly where fairness matters most. Attribution share stays meaningful ("3% of the lexicon is sourced from your family") even when phonetic recognizability is negligible.

### Process (FIRM)

- Small, session-sized iterative milestones.
- Patrick stays in the loop in chat and reacts to intermediate results before anything is committed.
- Discoveries and decisions get documented (this file, `data-audit.md`).

---

## 3. Design decisions so far

### 3.1 Sequencing: phonology first, but vocab-aware (FIRM)

Order of work: **phonology & phonotactics → vocabulary**, with grammar hand-designed in parallel.

- *Phonology* = the language's sound system: its inventory of **phonemes** (the contrastive sound units of a language — categories that can distinguish one word from another, like English /p/ vs /b/).
- *Phonotactics* = the rules for how phonemes may combine into syllables and words (e.g., English allows "str-" at a syllable start; Japanese doesn't).

Vocabulary can't be optimized before the sound system exists, because every source word must be *projected into* our phonology. But phonology can't be chosen blind to vocabulary either: candidate phonologies are scored partly by a **projection distortion** term — how much recognizability source words retain after being squeezed into that phonology. A too-restrictive phonology (e.g., toki pona's strict consonant-vowel syllables) mangles every source word so badly that the later vocabulary optimization becomes moot.

### 3.2 Grammar: hand-designed from typology, not optimized (FIRM)

Grammar mostly can't be optimized from dictionaries — there is no database of "grammatical recognizability." Instead it will be hand-designed from typological principles, with a data citation for each decision, using cross-language majority evidence from **WALS** and **Grambank** (databases of structural features across thousands of languages) and convergence evidence from creoles (contact languages that emerge when adults must learn fast — a natural experiment in learnability). The expected shape:

- **Isolating morphology** — words don't inflect; grammatical information comes from separate particles and word order (like Mandarin), rather than from endings (like Latin).
- No grammatical gender, no case, no agreement.
- Particles for tense/aspect.
- Transparent, regular derivation of new words.

Grammar's main coupling to phonology: an isolating language needs a stock of **short, mutually distinct particles**, which argues for reserving short-word space in the phonotactics/lexicon design.

#### Tier 0 decided (**FIRM**, 2026-08-05 by Patrick)

Evidence: [`grammar-tier0.md`](grammar-tier0.md), creole convergence under the Rule 1/Rule 2
policy of [`grammar-plan.md`](grammar-plan.md) §2.

- **SVO.** Converges in creoles across lexifier families (13 of 16 non-European-lexifier), and
  three creoles *moved to* SVO from a non-SVO lexifier (Pidgin Hindustani from SOV Hindi,
  Pidgin Hawaiian from VSO Hawaiian, Chinuk Wawa from Chinookan). SOV leads the world by
  language count (40.9%) but SVO leads by people (59.2% of L1, 63.1% of total speakers), and
  §2 counts people.
- **Prepositions**, not postpositions. Creole lean 11 of 15; head-initial, consistent with SVO.
- **No case marking on core arguments.** Argument roles are carried by position alone.

**Head-directionality is not one parameter, and the agenda was wrong to assume it was.**
Creoles converge above the noun phrase — constituent order, relative-clause position, and
more weakly adpositions — and split 8:7, 8:7, 8:7 on adjective, numeral and demonstrative
order. **NP-internal order therefore has no creole answer and is deferred to Tier 2** as its
own question (§7).

#### Morphological type (**SOFT**, 2026-08-05 — recommendation on the table)

The creole record says adults **do not invent derivational affixation**: 3 gains against 35
losses over 14 creole/lexifier pairs scored on identical Grambank features. What they add
instead is **compounding and reduplication** (13 gained, 2 lost). Working position:

- **No derivational affixes**; word-formation is compounding (already FIRM, §3.6).
- **Reduplication is a candidate morphological device** — the single most-gained feature in
  the study — and costs nothing under §3.6's template.
- **Any affix ever adopted must be a suffix**: 84.4% of L1 speakers have a strongly
  suffixing native language, the largest margin in the study.

Held SOFT because the *loss* half of the finding does not survive the Rule 1 lexifier split
(European-lexifier creoles 27:8, non-European 8:11); only the *no-gain* half does. See
[`grammar-tier0.md`](grammar-tier0.md) §2.3.

#### TAM: no TAM grammar at all (**SOFT**, 2026-08-05 by Patrick — a taste-based choice)

**Tense, aspect and mood are ordinary open-class adverbs**, omitted whenever context supplies
them: *I run {continuously} {in-the-past}*. No particles, no fixed slot, no closed class, no
ordering rule, nothing to combine. **Particle bill: 0.**

**This decision overrides its own study and is recorded as taste, not evidence.** The
evidence in [`grammar-tier2-tam.md`](grammar-tier2-tam.md) supports **two aspect particles in
a fixed preverbal slot with tense and mood lexical**: an overt imperfective marker is present
in 100% of expanded pidgins and 100% of creoles, 7 of 9 expanded pidgins place markers
immediately preverbally, and of the three categories aspect and mood are the ones the world
puts on free words (31.9% and 51.1% of L1) while tense is the rarest strategy in the study
(9.3%). That design was declined because singling out **aspect** for structural treatment,
when tense and mood are handled lexically, is an asymmetry a learner cannot see the reason
for. Uniformity was preferred.

Accepted costs, all live: we are outside the contact-language sample entirely; there is no
positional cue for where the predicate begins, in a language where position already carries
all the argument-role work (§3.2 Tier 0); and **negation scope becomes an open problem** —
*I not run in-the-past* is structurally ambiguous in a way a fixed TAM slot would have
prevented. That lands on Tier 2 Q9.

What it buys: an optional *grammatical* marker makes its own omission meaningful (with a past
particle, not using it invites "not past"); **adverbs do not**, so the implicature problem
disappears. There is no TAM chapter in the grammar. And the open class gives unlimited
gradation — *briefly, repeatedly, finally, almost* — with no new machinery.

**Handoff to the lexicon stage:** ~10–14 high-frequency TAM concepts are flagged for **short
forms** (past, future, now, already, still, again, used-to, maybe, must, if, yesterday,
tomorrow, soon, long-ago). Same shape as §3.3's segment discouragement — a nudge on the
vocabulary optimizer, not a rule. Monosyllabic space is not a constraint: ~180 cluster-free
(C)V(N) forms avoiding /r h l/, so this is ~8% of it. A **recommended default usage** should
ship with the lexicon so the permissive grammar does not fragment in practice.

#### Noun phrase and modifier order (**FIRM**, 2026-08-05 by Patrick)

Evidence: [`grammar-tier2-np.md`](grammar-tier2-np.md).

**One rule: single-word modifiers precede their head, clausal modifiers follow it.**

- adjective, numeral, demonstrative and possessor all **precede the noun**;
- the relative clause **follows** it (Tier 0, unchanged) — short modifiers before, heavy
  constituents after, the standard processing pattern;
- and therefore **adverbs precede the verb**, which answers Q11a without a separate study.

A third line of evidence, directional: of 62 contact languages whose lexifier has a WALS
adjective-order value, **every one of the 14 that changed moved N-Adj → Adj-N, and none moved
the other way** — 0 of 29 Adj-N-lexifier languages ever left Adj-N. Part of that drift is
substrate transfer (the South Asian Portuguese creoles), but Palenquero, Louisiana, Reunion,
Cape Verdean and Casamancese moved with N-Adj substrates too.

Tier 0 reported these as coin flips; that was a pooling artefact. Stratified by contact type,
**restricted pidgins put the modifier first on all four**, and the harmony test settles the
uniform treatment: **67% of 1,297 languages put adjective, numeral and demonstrative on the
same side, and those languages are 91% of the L1 mass**. Of the two harmonic options,
modifier-first is a minority by language count (23.8% vs 43.1%) and **86.1% by people** — the
largest by-language/by-people divergence anywhere in the project.

*Consequence worth noting:* §3.2's TAM decision declined a preverbal particle slot, and the
modifier rule puts TAM adverbs there anyway — *I in-the-past continuously run*. It also
weakens that decision's "no cue for where the predicate begins" cost, since a run of
preverbal modifiers is itself the cue.

*Weakest link:* the possessor. Expanded pidgins and creoles prefer head-first; only
restricted pidgins and a slim world majority support possessor-first. Adopted for uniformity.

#### Nominal categories (**FIRM**, 2026-08-05 by Patrick)

**The noun carries almost nothing.**

- **No articles.** Definiteness uses the **demonstrative**, indefiniteness uses **'one'** —
  both words exist anyway, so this costs zero vocabulary. No restricted pidgin has a
  dedicated article of either kind; 5 of 9 use a demonstrative and 4 of 4 use 'one'. Rule 2
  splits informatively: definite articles are KEPT 8 / LOST 1 (retained when inherited, never
  invented), indefinite articles LOST 9 / KEPT 1 (actively shed — the strongest Rule 2 signal
  in the study).
- **Number is optional.** A bare noun is number-neutral; a plural *word* is available when
  the count matters. No restricted pidgin marks plural obligatorily. Note the strategy
  constraint: the world's dominant plural marker is a **suffix** (84.7% of L1), which Tier 0
  rules out for us; a plural word is 5.2% of L1.
- **No numeral classifiers.** 68 of 72 contact languages have none, including 9 of 9 expanded
  pidgins. **This is a deliberate vote against a large constituency** — classifiers are
  native to ~36% of the world's L1 mass — and must be surfaced in the final bias audit
  ([`grammar-plan.md`](grammar-plan.md) §1) rather than buried.

**Particle bill: still 0.** Grammar rules added by Q11 + Q7: **one.**

#### Negation (**SOFT**, 2026-08-05)

Evidence: [`grammar-tier2-negation.md`](grammar-tier2-negation.md).

**One negator, a free word, immediately before the verb, used for everything.** Verbal,
locational, existential and nominal predication, and commands. No bipartite negation, no
negative pronouns, no effect on anything else in the clause.

- **Position falls out of §3.2's modifier rule** rather than being decided separately — a
  negator modifies the verb, so it precedes it. The rule made a prediction and it held:
  preverbal in 6 of 9 restricted pidgins, 6 of 9 expanded pidgins, 46 of 54 creoles, and
  68.7% of world L1 (WALS 143A).
- **A free word is also the world's majority strategy here** (84.2% of L1, Grambank GB299;
  Rule 2 KEPT 13 / LOST 0) — unlike the plural marker, where the no-affix constraint forced
  us onto a 5.2% minority option. The isolating decision is not always a sacrifice.
- **One negator for all predication types**: 71.6% of L1 already do this (GB140). One rule
  instead of four.
- **The same negator for the prohibitive** — the weakest call. Contact languages agree (7 of
  8 restricted pidgins) but a slim population majority does not (54.7% of L1 use a special
  negator, by WALS 71A's finer coding; Grambank GB139's coarser 83.5% conflates a special
  negator with a special imperative construction).
- **Rejected:** bipartite *ne…pas* negation (0 of 18 pidgins, 2.6% of world L1) and dedicated
  negative pronouns (where they exist, 66.3% of L1 negate the predicate *as well* — we negate
  once and say "not … any").

**Scope: linear order, leftmost modifier widest.** This pays the debt the TAM decision
created — *not past run* is "it is not the case that I ran", *past not run* is "in the past I
did not run". It uses the modifier position already fixed, generalises to any stacked
modifiers, and turns an ambiguity into an expressible distinction. **A design decision, not a
finding** — no source codes the relative order of negation and TAM adverbs.

**Word bill: 1** — the first grammatical word the grammar has required; Q6 and Q7 cost zero.
**Grammar rules added: zero.**

### 3.3 Phoneme inventory (**FIRM** — decided 2026-08-05 by Patrick)

**The inventory is closed. 15 consonants + 5 vowels = 20 phonemes.**

| | |
|---|---|
| **Consonants** | **p t k b d ɡ m n f s h j w l r** |
| **Vowels** | **a e i o u** (mids are wide: E = {e, ɛ}, O = {o, ɔ}) |

Rules that come with it:

- **One stop series contrast, defined widely (fortis/lenis).** /p t k/ vs /b d ɡ/ may be
  realized as a voicing difference, an aspiration difference, or both — whichever the
  speaker's native system provides. Voiceless implies aspirated: [pʰ tʰ kʰ] and [p t k]
  are both fine for /p t k/, [b d ɡ] and unaspirated [p t k] both fine for /b d ɡ/. This
  is the §3.4 wide-phoneme mechanism doing its most important work: 93–96% of humanity
  can hear the contrast under this definition, vs 73–75% if it were strictly voicing.
- **No other consonant makes a voicing or aspiration distinction.** /f/ and /s/ have no
  voiced counterparts (so [v] and [z] are acceptable *realizations*, not separate
  phonemes); /m n l r j w/ likewise. This is what keeps the ruled-out set (v z ʒ dʒ θ)
  ruled out rather than sneaking back in as allophonic contrasts.
- **No second sibilant.** The wide CH/SH category was offered by the contrast study and
  **declined** — at 61.9% audibility against /s/ it was the weakest of the priced add-ons.
- **/r/ and /h/ are broadly defined**; exact realization sets are delegated to the build
  agent (§3.4 gives the shape: any rhotic for /r/, h~[x~χ~ħ] for /h/).
- **Two contrasts are protected by minimal-pair bans** (the §3.3 functional-load
  mechanism, now concrete):
  - **/l/ ~ /r/** — never a minimal pair. Japanese and Korean speakers hear one category
    (81.9% audible, 45 attested mergers).
  - **/h/ ~ /r/** — never a minimal pair. **New constraint (2026-08-05).** Wide /h/
    admits [x ~ χ] and wide /r/ admits uvular [ʁ ~ ʀ]; a French or German speaker's
    rhotic and a Russian or Spanish speaker's /h/ can land on nearly the same sound.
    The two wide definitions overlap at their edges, so the contrast must not carry
    lexical weight. *This is a cost of the wide-phoneme approach, not of either segment
    individually — worth noting as the first case where two wide sets collide.*
- **Segment discouragement ranking** (a preference for the lexicon optimizer where a
  choice exists, not a ban): **/r/ and /h/** strongly discouraged; **/l/** moderately;
  **/b d ɡ/** mildly. Everything else is free. Applies with extra force to particles and
  basic vocabulary. **Onset clusters join this list as a structural item** — see §3.6.
  *This needs to become a numeric penalty before the optimizer runs — currently an
  ordinal ranking (§7).*

Retained context behind the decision:

- Notation: symbols between slashes are **IPA** — the International Phonetic Alphabet, the standard one-symbol-per-sound notation; /j/ is the "y" sound of *yes*.
- **Penalize contrasts, not just rare sounds.** A sound can be common while a *distinction* is deadly: /r/ vs /l/ is a single category for Japanese and Korean speakers; Mandarin has no voicing contrast in stops (it uses aspiration — a puff of air — instead, so /b/ vs /p/ as *voicing* is hard). The inventory cost function should charge for contrasts that major populations can't hear.
- **Empirical status** (see [`phoneme-prevalence.md`](phoneme-prevalence.md) and [`contrast-study.md`](contrast-study.md)): the core **m n p t k s j w r + a i u** is native for ~89–99.9% of humanity per segment; **h** is weakest (55%) but wide-h over [x χ ħ] recovers 83.5%; mid vowels must be wide (E={e,ɛ}, O={o,ɔ}), giving vowel contrasts 80–83% audibility. Priced add-ons: a fortis/lenis second stop series (93–96% audible as voicing-OR-aspiration, vs 73–75% for strictly voiced — but only ~61% of *languages* have any second series), /l/ (r/l audible to 82–85%), /f/ (79%), one wide CH sibilant (~62% vs /s/). Ruled out as phonemes: v z ʒ dʒ θ ŋ ə ɪ ʊ y, and any e/ɛ, o/ɔ, or h/x contrast.
- **Functional-load pricing (SOFT → partly FIRM):** contrast costs feed the lexicon optimizer as per-pair penalties, not just keep/drop gates — a kept-but-expensive contrast is made cheap in practice by forbidding minimal pairs that hinge on it (*lira*/*rira* never both words). The contrast-study table is exactly this penalty matrix. Two bans are now FIRM (l/r, h/r, above); **f/p** (77.2% audible) remains a SOFT candidate for low functional load rather than a hard ban.

### 3.4 Wide phonemes (FIRM as an approach)

Each phoneme of our language is defined as a **set of acceptable realizations**, not a single target sound. Examples:

- A fortis/lenis stop contrast (i.e., the /p t k/ vs /b d ɡ/ series) may be realized as a voicing difference *or* an aspiration difference — whichever the speaker's native system provides.
- /h/ may be pronounced [x] (the *Bach* sound).
- Any rhotic (r-like sound — trilled, tapped, or the English approximant) counts as /r/ if we have one.

Recognizability is scored against the **best** realization in the set. This is essentially designing with **allophones** on purpose — an allophone is a variant pronunciation of a phoneme that speakers treat as "the same sound" (English /t/ in *top* vs *stop*). PHOIBLE's `Allophones` column provides direct empirical data on which realization sets languages actually treat as one category.

### 3.5 Suprasegmentals (FIRM)

No tone, no contrastive vowel length, no contrastive stress. Each of these is a distinction that large populations cannot produce or hear reliably, and none is needed if the segmental inventory and phonotactics leave enough word space.

**Stress placement: always the first syllable** (decided 2026-08-05). Stress carries no meaning — this rule exists only to give every word a single citation pronunciation.

Why initial rather than penultimate, given the study ([`stress-prevalence.md`](stress-prevalence.md)) headlined penultimate at 50.4% of covered L1 speakers: that headline collapses weight-sensitive systems onto penult via a trochaic default. Read faithfully, penultimate is a **3.4%** rule and **initial (7.5%) is twice as common** among languages with a genuinely fixed rule. The two also **coincide on one- and two-syllable words**, so they only differ on longer forms. Initial wins on simplicity — "stress the first syllable" is the shortest statable rule, and it never moves under compounding or affixation. Chosen deliberately over the more familiar Esperanto-style penultimate.

### 3.6 Phonotactics (**decided 2026-08-05**; only the lexicon-facing weights remain)

Notation: C = consonant, V = vowel, N = nasal consonant; parentheses mean optional. The **coda** is the consonant material at the *end* of a syllable (the /n/ in "san"); the **onset** is the consonant material at the start.

#### Syllable template (**FIRM** — decided 2026-08-05 by Patrick)

**(C)V(N) with N ∈ {n, m}, plus a closed set of Cr/Cl onset clusters.** Optional onset,
optional nasal coda, and — only in the onset — one of ten permitted two-consonant
sequences:

```
pr  tr  kr  br  dr  ɡr  fr        pl  kl  fl
```

That set is **exhaustive and not productive**: it is a list, not a rule, so no cluster
enters by analogy. An illegal word-final consonant takes a **support vowel** rather than
being deleted (*bank* → *banki*, *virus* → *firusi*), which keeps the mapping lossless at
the segment level.

**The support vowel is /u/ after a labial (p b f m w) and /i/ everywhere else**
(decided 2026-08-05 by Patrick). *club* → **klubu**, *camp* → **kampu**, but *bank* →
**banki**, *virus* → **firusi**, *hotel* → **hoteli**. Every candidate — fixed /i/, fixed
/u/, echo, and this rule — scores identically on recognizability (spread 0.0005 over 52
words), so the decision rests on articulation and precedent: [mu pu bu fu] need no lip
transition where [mi pi bi fi] do, and **Swahili splits exactly this way**, 3 of 3 labial
cases taking -u (*atomu, kilogramu, filamu*) against 19 of 19 non-labial cases taking -i
(*benki, plastiki, protoni, hoteli, sukari*) — note velars pattern with -i, so this is a
labial rule, not a backness rule. Evidence: [`international-vocab.md`](international-vocab.md) §6.7.

*Note the interaction with the clusters above: licensing Cr/Cl removed **every** labial
epenthesis site in the 52-word study set, so this rule changes none of the words priced
for the template decision. It bites on word-final /p b f/, which that word set happens
not to contain.*

Evidence: [`international-vocab.md`](international-vocab.md), 52 international words ×
6 templates × 2 final-coda policies.

- **Strict CV is ruled out.** (C)V → (C)V(n) is the single largest step in the table
  (+0.052 recognizability); the floor is the expensive part, everything after it is cheap.
- **/m/ is kept alongside /n/** — free, and without it *atom* → *aton*, *film* → *filin*,
  *system* → *sisiten*, *computer* → *konpute*.
- **Liquid codas are ruled out.** (C)V(N,l,r) scores the same as the onset clusters
  (0.828 vs 0.828 under deletion, 0.843 vs 0.846 under epenthesis) while inflating more,
  and it puts /l/ and /r/ — the segments §3.3 already discourages — in the position where
  they are hardest to hear.
- **Onset clusters are taken** because they dominate plain (C)V(N) on *both* axes at once:
  +0.017 recognizability and −0.085 syllable inflation. Permitting the cluster removes the
  very epenthetic vowel that was inflating the count, so nothing is traded away. They also
  target the worst-hit domain (chemistry/physics, 1.40 inflation), and Cr/Cl is the most
  widespread cluster type in the world's languages.
- **Scored against recipients that must repair clusters themselves** (ja, ko, sw, ta, ha,
  vi), (C)V(N)+Cr/Cl ranks **first of six**, ahead of unrestricted (C)V(C). Unrestricted
  codas only win when the scoring is dominated by European Latin-script recipients: their
  advantage swings 0.050 across that split, ours 0.011.

Known metric bias accepted in reaching this: the metric lacks a working epenthesis model and systematically **flatters permissive codas** (§4, cost-learning guardrail 4). Syllable-count inflation is arithmetic rather than metric and was read alongside every score; the ranking also survives the learned-cost arm, which is the two-arm condition §7 set.

#### Onset clusters carry a lexicon cost (**FIRM** as a principle, weight OPEN)

The clusters are licensed **for recognizability of borrowed material**, not as free word
shapes. A cluster is the least widely producible thing in the template — the whole
cluster-repairing half of the world breaks it up — so where the lexicon has a choice, it
should not choose one.

**Treat a Cr/Cl onset as a discouraged structure in the lexicon optimizer, on the same
footing as §3.3's segment discouragement of /r/, /h/, /l/ and /b d ɡ/: a small penalty,
not a ban.** Concretely: an international word that arrives with a cluster keeps it
(*proton*, *program*, *demokratia* — that is what the clusters are for); a coined root or
a grammatical particle should not acquire one where a cluster-free alternative of equal
quality exists. Applies with extra force to particles and basic vocabulary, exactly as the
segment ranking does.

The numeric weight is deferred with the rest of the discouragement weights (§7) — it must
be small enough not to override recognizability on borrowed stems, which is the only
reason the clusters exist.

#### Decided rules (**FIRM**, 2026-08-05)

- **Compounding is kept** (decided 2026-08-05 by Patrick; was OPEN). Words may be built by
  joining roots, and the seam is left alone.
- **Concatenation is the whole rule: a compound is its parts, written in order, unchanged.**
  Whatever falls out of the join is legal — **geminates** (`kan` + `nomi` → `kannomi`) and
  **hiatus** (`bao` + `ito` → `baoito`) alike. There is no repair at the seam: no
  degemination, no glide insertion, no linking vowel, nothing to memorise. This costs a
  marginal amount of pronunciation ease and buys two things worth more: compound
  transparency — the seam stays visible, so a compound can always be read back to its parts
  — and one less rule between a learner and a word they want to build.
- **Geminates do not occur within a morpheme.** They are a compound-seam phenomenon only,
  so a geminate in a word is positive evidence of a boundary.
- **Hiatus is legal** (revised 2026-08-05; supersedes the earlier glide-insertion rule).
  Vowel + vowel needs no repair anywhere: not at a compound seam, not in borrowed
  vocabulary (*radio*, *bakteria*, *geometria*, *malaria*), not inside a root. The glide
  insertion rule (`oa` → `owa`) is **retired** — see the note below.
- **No sandhi, no alternations, no deviation from "pronounce what is written."** This is a strong constraint and it has a consequence: every repair above is **orthographic**, applied when the word is formed, not a pronunciation rule layered on top. There is never a gap between spelling and speech. (Interacts with §3.7: the ASCII orthography is one letter per phoneme, so "what is written" is unambiguous.)

*Why the glide rule was retired rather than narrowed (2026-08-05).* It was FIRM earlier the
same day, so the reversal is worth stating. Three things arrived at once. (1) The
international-vocabulary study measured it: glide insertion costs **0.018** recognizability
and its damage is systematic, landing on `e_o`, `e_i` and `a_V` — precisely where Greek
compounding lives. No recipient language produces *gejometrija*. The rule already had a
loanword exemption, and loanwords are where hiatus mostly occurs. (2) Patrick's compounding
decision exempts the seam, on the principle that a rewrite rule people have to learn is
worse than the thing it repairs. (3) What remains after those two exemptions is hiatus
inside monomorphemic native roots — words *we coin*. **A rule that only ever fires inside
words we design ourselves is not a rule the learner needs; it is a preference for the
lexicon chooser.** So the rule goes and the preference stays: if root-internal hiatus turns
out to hurt, the lexicon optimizer prefers roots without it, and nothing about the language
a learner must memorise changes. This also dissolves §7's open question about which glide
follows /a/ — it no longer arises.

#### Loanword adaptation: `<v>` → /f/ (**SOFT** — decided 2026-08-05 by Patrick)

International vocabulary is projected into the inventory by the ruleset in
[`../src/interlang/translit.py`](../src/interlang/translit.py). Its one genuinely
arbitrary segment mapping — what to do with `<v>`, which §3.3's inventory does not have —
is settled: **`<v>` → /f/** (*virus* → *firusi*, *vitamin* → *fitamin*, *television* →
*telefision*). /b/ was tied with it on recognizability (0.810 vs 0.811 over 52
international words); /w/, the earlier placeholder, is 0.015 worse. The tiebreak is
inventory-internal, not metric: /f/ keeps /w/ free to render `<w>`, and §3.3 mildly
discourages /b d ɡ/. Evidence and the full ruleset:
[`international-vocab.md`](international-vocab.md) §4.1, §6.4, §7.1.

SOFT rather than FIRM for one reason only, now that the template above is settled: z→s,
th→t and v→f all pile onto the same two consonants. Over 52 words that produced no
collisions, but it is homophony pressure the vocabulary optimizer may want re-priced at
lexicon scale.

##### The merge table — carry this to the vocabulary stage

**Every many-to-one mapping in the adaptation ruleset, with its fan-in.** Written down so
the homophony question can be asked properly when the lexicon exists rather than
re-derived from the code. `n×` is how often the rule fired over the 52-word study set.

| our phoneme | international spellings that collapse into it | fan-in | fired |
|---|---|---|---|
| **/s/** | `s`, `c` before e/i/y, `z`, `sh`, `ss` | **5** | c→s 2×, z→s 1× |
| **/k/** | `k`, `c` elsewhere, `ch`, `ck`, `q`, `sch`(→sk) | **6** | c→k 12×, ch→k 2× |
| **/f/** | `f`, `ph`, **`v`** | **3** | v→f 6×, ph→f 1× |
| **/t/** | `t`, `th` | 2 | th→t 2× |
| **/e/** | `e`, `ae`, `oe` | 3 | — |
| **/i/** | `i`, `y` not before a vowel | 2 | y→i |
| **/j/** | `j`, `y` before a vowel | 2 | y→j |
| **/r/** | `r`, `rh` | 2 | — |
| **/g/** | `g`, `gh` | 2 | — |
| **/w/** | `w`, `wh` | 2 | — |
| **/d/** | `d`, `ð` | 2 | — |
| (single) | any geminate, any doubled vowel | — | 1× |
| /ks/, /kw/ | `x`, `qu` — expansions, not merges | — | x→ks |

**Status over the 52-word set:** 198 of 358 phonemes (**55.3%**) in the rendered forms
could have come from more than one international grapheme, a mean of 3.81 ambiguous
phonemes per word — and **zero collisions**: no two of the 52 words render to the same
form. Spelling information is destroyed, word identity is not.

**What to check when the vocabulary optimizer runs**, and the reason this table exists:

1. **Collision rate** among adapted internationalisms at real lexicon scale — 52 words is
   far too few to see the birthday-problem effect.
2. **/k/ and /s/ are the overloaded targets** (fan-in 6 and 5), and /k/ is fed by the
   single most frequent rule in the set (c→k, 12×). If anything breaks it will be there,
   not at /f/.
3. **v→f is the one reversible knob.** /b/ was tied with it on recognizability (§6.4), so
   if /f/ turns out overloaded, moving `v` to `b` costs nothing measurable and relieves
   fan-in on /f/ immediately. That is why this decision is held SOFT.
4. Interaction with §3.3's minimal-pair bans: those protect l~r and h~r, which no
   adaptation rule feeds. The merges land elsewhere, so the two mechanisms do not
   currently conflict — worth re-confirming rather than assuming.

#### Deferred

- **Root shape bounds** (min/max syllables) — deferred until after grammar. Patrick is leaning **analytic**, in which case there may be no root-vs-inflected-word distinction to bound separately.
- **Functional-load policy** (numeric contrast penalties) — deferred; blocks only the lexicon chooser (§7). The two hard minimal-pair bans (l/r, h/r) are already FIRM in §3.3 and are sufficient for hand-designing the grammatical particles.

### 3.7 Orthography (**resolved** by the §3.3 inventory decision, 2026-08-05)

**Decided (2026-08-05): the orthography is diacritic-free IPA restricted to ASCII.** One
character per phoneme, one phoneme per character, with **each character standing for the
phoneme's whole realization class** (§3.4 wide phonemes) rather than a single sound — `h`
means the whole h~[x~χ~ħ] set, `r` any rhotic, `p` fortis [p~pʰ]. IPA values, not English
ones: **`j` is the "y" of *yes*, never English "j".** No digraphs, no diacritics, no silent
letters, and — with §3.6's no-sandhi rule — no gap whatsoever between spelling and speech.

#### Punctuation and capitalization (**FIRM**, 2026-08-05 — Patrick: "not central to the project, let's just go with those")

Surveyed in [`punctuation-survey.md`](punctuation-survey.md), weighted by total (L1+L2)
speakers. Adopted: `.` `?` `!` `,` as in English; `"` outer and `'` nested quotation,
understood as the ASCII rendering of the world's typographic pair (no locale in CLDR
specifies straight quotes); spaces between words; `1,000.50` with 3-digit grouping.
Rejected: Spanish inverted `¿ ¡` (one language), English `I` capitalization (one language,
7.6% of L1 weight), German noun capitalization (one language), Indian 2-2-3 grouping (15%
of the world, but tied to a lakh/crore numeral vocabulary we are not adopting).

**Case is kept: sentence-initial capitals + proper nouns** (decided 2026-08-05 by Patrick,
closing the one question the survey left open — *"since we're using latin orthography"*).
Proper nouns are defined narrowly — people, places, organizations — and explicitly **not**
extended to days, months, nationalities or language names, which is an English quirk that
Spanish, French and Russian all decline. The rejected alternative, on the record: 53% of
the world's total-speaker weight (60% by L1) writes in a unicameral script, and
all-lowercase would have matched that majority and deleted the one orthographic rule that
requires a lexical judgment. It loses to the fact that a reader of a Latin orthography
arrives expecting case regardless of their L1 script, and that proper-noun capitals do
real disambiguation work in a language whose names are transliterated into 20 letters.

**Compounds are written solid** — `firetruck`, not `fire-truck` or `fire truck`
(**FIRM**, decided 2026-08-05 by Patrick). Consistent with §3.6: a compound is one word,
concatenated without seam repair, and it takes one initial stress like any other word.
This keeps the hyphen and the apostrophe unused.

Two costs come with it. Both are **accepted, and both are logged in §7 to be re-examined
once a lexicon and a grammar exist** — neither is measurable before then:

- **Segmentation ambiguity is the cost, and it is a lexicon problem, not a spelling
  problem.** With (C)V(N) syllables and no seam marker, a solid compound can in principle
  be parsed more than one way — a form like *banana* could be *ban+ana* or *ba+nana* if
  both splits happen to be real roots. Two signals already work against this: **geminates
  occur only at a seam** (§3.6), so a geminate is positive evidence of a boundary, and if
  the lexicon chooser also disfavours root-internal hiatus, **hiatus becomes weak evidence
  of one**. Neither covers the common V+C join. The right place to manage the residue is
  the lexicon chooser — avoid coining roots that make frequent compounds ambiguous — which
  is one more constraint to hand it alongside the discouragement weights (§7).
- **Solid writing plus §3.5's single initial stress makes a compound prosodically
  identical to a simple root of the same shape.** Spaced or hyphenated writing would have
  preserved two stresses and kept the seam audible. This is the real thing being traded
  away, and it is traded knowingly: the seam stays visible *in the spelling*, which is
  where a learner decomposes words, and §3.5's rule stays exception-free. Precedent is
  strong — Esperanto, German, Dutch, Swedish, Finnish and Turkish all write compounds
  solid, and the whole Sinosphere writes without word spaces at all.

**The ASCII orthography is free, with zero casualties.** The closed inventory maps
one-to-one onto 20 ASCII letters:

```
p t k b d g m n f s h j w l r   a e i o u
```

Every §3.7 problem symbol is gone: **ʃ** and **tʃ** disappeared with the declined CH
sibilant, and **ŋ** was never in the inventory (it survives as an allophone of /n/, as in
most languages). The /tʃ/ spelling question ("c" vs digraph) is **moot** — c, q, v, x, y, z
are simply unused. The wide-phonemes approach did exactly what §3.4 predicted it might:
the problem symbols never entered the inventory, so the orthography never had to
compromise. Remaining orthographic decisions are conventions only (capitalization,
punctuation, how compounds are written).

*Note /j/ is IPA-valued ("y" of yes), not English-valued — the one place where an
English-reading learner is actively misled by the ASCII choice.*

#### Prior discussion (superseded, kept for the record)

Aspiration: the writing system is simply **IPA restricted to phonemes whose IPA symbols are ASCII a–z** — nearly free given the optimal inventories, since a–z natively covers p b t d k g m n f v s z h l r w j + a e i o u. Real casualties: **ʃ** (the "sh" sound), **tʃ** ("ch"), **ŋ** ("ng"). ŋ is recoverable as an allophone of /n/ (as in most languages). Considered and not committed for /tʃ/:

- "c" — near-IPA, since IPA [c] (a palatal stop) is acoustically close to tʃ;
- "tc" / "tsh" digraphs (Patrick's suggestion, on a soft principle of not using one glyph for two sounds).

The wide-phonemes approach may make much of this moot — if /s/~[ʃ] land in one wide phoneme, the problem symbols never enter the inventory.

### 3.8 L2 data sparsity accepted (FIRM)

Reliable L2 speaker counts exist for roughly the top ~30 languages. Beyond those, falling back to L2 = L1 is fine: languages outside the top ~30 have few L2 speakers by definition, so the approximation error is small.

---

## 4. The recognizability metric

**Question the metric answers:** how likely is a listener to recognize a word of our language as a word they already know? Implemented in `src/interlang/metric.py` (v0), validated in `data-audit.md`.

### Literature basis

- **Workhorse:** PanPhon (Mortensen et al. 2016) — every IPA segment maps to a vector of **articulatory features** (binary-ish dimensions describing how a sound is physically produced: voiced?, nasal?, place of articulation, …). Word distance is then a **weighted feature edit distance**: an alignment-based edit distance where substituting /d/→/t/ (one feature apart) is cheap and /d/→/f/ is expensive.
- **Empirically calibrated alternative:** Jäger's sound-class distances, learned via pointwise mutual information from cognate alignments over ASJP.
- **Efficiency layer for scale:** PWESuite (Zouhar et al. 2024) phonetic word embeddings.
- Rejected generalization: raw formant distance (formants = the resonant frequencies that characterize vowels) only works for vowels — stops and fricatives have no steady-state formants. Articulatory features are the standard generalization.

### Key refinement: listener conditioning

Recognizability is not symmetric or universal — it depends on the hearer's **native phoneme categories**. This is the central finding of the loanword-adaptation literature (English "strike" → Japanese "sutoraiku"). v0 implements it by **projecting both words onto the listener's PHOIBLE inventory** — each segment is mapped to the nearest native category in feature space — before scoring. Contrasts the listener lacks become free (verified: /l/ ~ /ɾ/ scores 1.0 under a Japanese-like inventory).

### What v0 does

1. Tokenize IPA strings into segments (normalizing ASCII lookalike glyphs like `g` → IPA `ɡ`).
2. Optionally project both words onto a listener inventory.
3. Score weighted feature edit distance, normalized to [0, 1] similarity where the normalizer is the cost of deleting the longer word entirely (1.0 = identical; 0.0 = no more similar than an arbitrary word).

### Validation results (revised 2026-08-04)

The old headline "AUC 0.923" is **retired**: its negative controls were drawn from the *global* pool of source words, so a model could score well by detecting which donor pool a recipient borrows from rather than by modelling adaptation. Under the honest protocol — leave-one-recipient-out over all 41 WOLD recipients, controls shuffled *within* recipient — v0 scores **AUC 0.8961 ± 0.0618** (min 0.720 for Mandarin, max 0.985 for Bezhta). Costs learned from the same data score **0.9569 ± 0.0391** and beat v0 on **41 of 41** held-out recipients. Full detail: [`cost-learning.md`](cost-learning.md).

Sanity gradient vs /da/ under v0 orders as desired: ta 0.98 > ða 0.91 > ɡa 0.85 > fa 0.82 > ma 0.75 > ia 0.41 (though compressed into 0.75–0.98; the learned costs order the same way with far better separation, 0.84 down to 0.00).

### Known issues

*Updated 2026-08-04 by the cost-learning study ([`cost-learning.md`](cost-learning.md)); issues 1 and 2 move from "known" to "bounded".*

1. **Place of articulation underweighted** by panphon's default weights: projection maps /v/ → /z/ for a Japanese-like inventory where real loanword adaptation gives /v/ → /b/ (confirmed: default costs are /v/→/z/ 1.125, /v/→/b/ 1.250). **BOUNDED and fixable.** Learning the weights from WOLD raises the labial weight to 3.2× panphon's (0.803 ± 0.018 across 41 leave-one-recipient-out folds) and flips the diagnostic: /v/ → /b/ now wins over /z/ by a factor of 1.9. More precisely than expected, it is *labiality* that was underweighted, not place in general — coronal place detail (`ant`, `cor`, `distr`) goes **down** and manner (`cont`) barely moves. The learned weights are in `data/processed/learned_costs.csv` and `metric.py` accepts them via `params=`, but they are **not the default** — see issue 5.
2. **No epenthesis modeling.** **BOUNDED, partially fixed.** The cost model now has separate insertion prices for vowels and consonants (and, in the `context` variant, for cluster-repair vs other positions), fitted jointly with the substitution weights. Insertion and deletion drop from panphon's flat 7.25 to 2.2–3.9 and separate correctly (deleting a vowel is the cheapest edit at 2.18, inserting a consonant the dearest at 3.91), and cluster-repair insertion is 13–21% cheaper than gratuitous insertion. But "sutoraiku" vs "strike" goes 0.617 → **0.577** — the wrong way — where hand-setting the cluster-insertion prices gives 0.904. The reason is structural: the negative control shares the recipient word, so cheap insertion helps it as much as the true pair, and a **discriminative objective cannot learn repair costs**. Fixing it needs a generative term, not a richer insertion model. **The bias toward permissive codas is reduced, not removed**, so the syllable-template experiment (§7.4) still needs the caveat, now with a measured size rather than an assertion.
3. **Baseline inflation:** random CV-ish pairs score ~0.46, so usable dynamic range is roughly [0.45, 1.0]. Recalibrate against that floor, e.g. `score' = max(0, (s − s_random)/(1 − s_random))`. (Unchanged.)
4. **Glyph normalization:** ASCII `g`, `:`, `'` are mapped to proper IPA in `segments()`; watch for more lookalikes when ingesting new sources. (Unchanged.)
5. **NEW — the learned costs encode loanword facts, not only perceptual ones.** Fitted freely the WOLD data prices *voicing* at ~7× panphon's weight; even with the major-class prior it settles at **3.5×**, the single largest upward move in the parameter table. The contrast study says voicing is one of the **cheapest** contrasts perceptually (t/d natively audible to 75%, p/b to 73%). Loanword orthographies record voicing faithfully on both sides, so the fit is learning a transcription artifact — and this single effect is what makes the contrast-study cross-check come out null (ρ = +0.059, p = 0.79): the vowel-quality contrasts move correctly, every voicing contrast moves wrongly, and they cancel. Similarly, aspiration/breathiness (`sg`), ejectivity (`cg`) and clicks (`velaric`) learn weight ≈ 0 — which means "no evidence in WOLD's recipient set", not "does not matter". This is why v0 is still the default.

---

## 5. Data landscape

All raw data in `data/raw/` (gitignored, re-fetchable); the universal join key is the **Glottocode** (Glottolog's stable per-language identifier), usually alongside ISO 639-3. Full details in `data-audit.md`.

| Dataset | Size | Role | Caveat |
|---|---|---|---|
| **PHOIBLE** | 3,020 phoneme inventories, 2,177 languages | Phoneme/contrast prevalence; listener inventories for the metric; allophone data for wide phonemes | Multiple inventories per language (~1.4 avg) — needs a selection/union policy |
| **ASJP** (lexibank) | 568,820 word forms, 11,540 doculects, 100 concepts (core 40 well covered) | Maximal-breadth word forms for projection-distortion and cross-family similarity; the fairness denominator | Only 100 concepts — fine for phonology, too few for the real lexicon. (`Segments` is already IPA-ish/CLTS-tokenized.) |
| **WOLD** (World Loanword Database) | 41 recipient languages, 21,624 borrowing records | Validation set for the metric; attested adaptation/repair evidence | Source words are raw strings in mixed orthography; 13,779 pairs survive a conservative cleaning filter |
| **Glottolog CLDF** | 27,177 languoids | Family tree + macroareas for fairness weighting and aggregation | — |
| **CLDR language populations** | 799 languages | Total-speaker weights (the L2/ease term) | Figures are **total** speakers; BCP-47 → ISO 639-3 mapping built in `scripts/phoneme_prevalence.py` (macrolanguage choices documented) |
| **Wikidata P1098 L1 counts** | 1,858 languages | Native-speaker weights (the representation term) | Ethnologue-derived via Wikidata, CC0; selection policy + phantom-MSA override in `scripts/fetch_l1_speakers.py`; languages missing from it default to 10k L1 |

Deferred to the vocabulary stage:

- **Concepticon** — the standard cross-linguistic concept list (what meanings need words).
- **CLICS** — colexification data. *Colexification*: when one word covers multiple meanings in a language (e.g., many languages use one word for "hand" and "arm"). Cross-language colexification patterns are a de-Eurocentrizing tool for deciding sense granularity — which meaning splits are universal vs European habits.
- **Lexibank / IDS / NorthEuraLex** — deeper wordlists (up to ~1,300 concepts) for actual lexicon sourcing.

*Terminology: a **doculect** is a language as documented by one particular source; a **languoid** is Glottolog's umbrella term for any node in the family tree (family, language, or dialect).*

---

## 6. Discoveries / empirical results so far

1. **The metric works at v0 quality — but the original number was measured too generously.** Under an honest protocol (recipient-grouped CV, controls shuffled within recipient) v0 separates attested loanword pairs from controls at **AUC 0.896 ± 0.062**, not the 0.923 first recorded; the difference is that the old controls came from the global source pool, so part of that 0.923 was a donor-pool detector. 0.896 is still good separation given noisy transcriptions on both sides, and good enough to rank candidate phonologies. (2026-08-04)
2. **Listener conditioning is implementable and cheap** — segment-wise nearest-native-category projection against PHOIBLE inventories behaves correctly on the classic cases (/l/~/ɾ/ free for Japanese-like listeners).
3. **The metric's failure modes are characterized**, not just suspected: place-of-articulation underweighting (/v/→/z/ instead of /v/→/b/), no epenthesis (punishes attested heavy-epenthesis adaptations, flatters permissive codas), and a ~0.46 random-pair floor. Each has a concrete fix path (§4). **Update 2026-08-04:** the place problem is fixed by learning the weights (labial ×3.2, diagnostic flips, stable across 41 held-out recipients); the epenthesis problem is *not* — see finding 8.
4. **WOLD is usable as ground truth** for learning substitution costs: **13,595** clean attested adaptation pairs after a now-committed filter (`scripts/wold_pipeline.py`), despite the empty `Source_Form_ID` column. It is *not* usable for repair costs — see finding 8.
5. **ASJP requires no transcription conversion** — its `Segments` column is already CLTS-tokenized and panphon-compatible, removing an expected preprocessing step.
6. **CLDR alone can't serve both objectives.** Its figures are total-speaker counts: exactly right for the ease/L2 term, unusable for the representation/L1 term. The two-objective design forces sourcing a second population dataset.
7. **The ASCII orthography is nearly free** given the kind of inventory the prevalence data is expected to favor — the losses concentrate in ʃ/tʃ/ŋ, and ŋ is recoverable allophonically.
8. **A discriminative objective cannot learn repair costs (2026-08-04, new).** Fitting costs so attested loanword pairs outrank shuffled controls buys a large, stable win on substitution structure and **no** improvement on epenthesis — because the negative control shares the recipient word, so a cheap vowel insertion helps the decoy as much as the truth. This is a general lesson for the project's method, not a WOLD quirk: ranking objectives learn what *discriminates*, and repair operations do not discriminate. Anything we want the metric to *predict* (rather than rank) needs a generative term.
9. **Learning from loanwords teaches orthography as perception (2026-08-04, new).** The fit prices voicing at 3.5× panphon's weight because loanword transcriptions record voicing faithfully on both sides — while the independent contrast study prices voicing as one of the cheapest contrasts for real listeners. The two disagree so sharply that the contrast-study cross-check comes out null overall (ρ = +0.059). Calibration data has to be chosen for the *concept* being calibrated.
10. **"Every language but Chinese adapts the Latin/Greek roots" is false as stated (2026-08-05, new).** Adaptation rates over a 52-word international set run from 98% (Spanish) to 28% (Tamil) with no outlier structure. There are three groups: the adapters; a **Sinosphere calquing bloc** (Mandarin, Japanese, Korean, Vietnamese — Chinese is its flagship, not its exception, and the split inside those languages is chronological, 19th-century science calqued and 20th-century vocabulary loaned); and an independent purist tradition (Icelandic, Tamil, Hebrew, Finnish's older stratum, Arabic). **The international-vocabulary goal should be priced for roughly half of humanity, not all of it** — for the other half an internationalism is already an arbitrary string, which incidentally means §2's representation objective is in less tension with it than it looked. → [`international-vocab.md`](international-vocab.md) §1.
11. **Latin and Greek morphology fits a nasal-coda language almost perfectly (2026-08-05, new).** The endings that carry scientific vocabulary — *-on, -in, -um, -ia, -ion, -ate, -ide, -ine* — are already legal under (C)V(N) with no repair at all, because they are open syllables or nasal-final. Only *-us* (and *-s* generally) and the consonant-final adjectival endings *-ic, -al, -ol* cost anything. The damage from a restrictive template lands on **onset clusters**, not on endings, which is why the template decision came out as "add onsets, not codas" (§3.6).

---

## 7. Open questions / next steps

Experiments:

1. ~~**Phoneme/contrast prevalence study**~~ **DONE** → [`phoneme-prevalence.md`](phoneme-prevalence.md); inventory findings folded into §3.3.
2. ~~**Contrast study**~~ **DONE** → [`contrast-study.md`](contrast-study.md); contrast prices and functional-load mechanism in §3.3.
3. ~~**L1 speaker-count sourcing**~~ **DONE** → Wikidata P1098 (1,858 languages, `data/processed/l1_speakers.csv`), with the phantom-MSA override (`L1_OVERRIDES` in `scripts/fetch_l1_speakers.py`; see contrast-study Addendum).
4. ~~**Projection-distortion experiment**~~ **DONE (2026-08-05)** → [`international-vocab.md`](international-vocab.md); resolved §3.6, which is now FIRM. 52 international words projected through six templates and both final-coda policies, scored against attested adaptations in 18 languages. The two-arm condition was met: v0 and the learned costs give the same ordering (V1 < V2 < V3 < V4 ≈ V3C < V5), so the ranking is reportable despite the epenthesis gap. The deciding evidence was not the pooled ranking but the **recipient split** — permissive codas lead only when scored against European Latin-script recipients — plus syllable inflation, which is arithmetic rather than metric. Deliverable B of that study (predictability) also produced the transliteration ruleset in `src/interlang/translit.py`: 12 of 13 decision points are rule-resolvable, the 13th is lexical (which international shape to start from) and belongs to the vocabulary optimizer.
5. ~~**Metric calibration**~~ **DONE (2026-08-04)** → [`cost-learning.md`](cost-learning.md), spec in [`cost-learning-spec.md`](cost-learning-spec.md). Summary:
   - The WOLD pipeline is **committed** for the first time (`scripts/wold_pipeline.py`): 16,687 cleaned pairs, 13,595 used.
   - The recorded **AUC 0.923 is retired as a reference point.** It came from a protocol that shuffled negative controls from the *global* source pool, which lets a model win by detecting which donor pool a recipient draws from. Rebuilt under that same loose protocol we get 0.909; under an honest recipient-grouped protocol with within-recipient controls the default-weight baseline is the number to compare against (see `cost-learning.md` §4).
   - Substitution and insertion/deletion costs are learned **jointly** and cross-validated **leave-one-recipient-out over all 41 recipients**. The headline is a stability statement, not a point estimate.
   - Learned costs beat panphon's defaults on **41 of 41** held-out recipients (0.9569 vs 0.8961; paired delta +0.061 ± 0.033), with learned weights stable to 1–8% relative sd across folds. The honest default-weight baseline is **0.896**, not 0.923.
   - **The place-of-articulation fix is real and stable**; the epenthesis fix moves the wrong way; **two of five guardrails fail** (4 and 5). **v0 remains the default metric**; the learned costs ship as `data/processed/learned_costs.csv` and are opt-in via `metric.similarity(..., params=...)`.
   - A phonetically coherent metric costs ~0.009 AUC: unconstrained fits reach 0.965 but score /d/→/i/ cheaper than /d/→/f/. The three major-class features (`syl`, `son`, `cons`) had to be held near panphon's values by a targeted prior — the data as we can clean it does not inform them.
   - New standing worry: the loanword corpus teaches production/orthography facts (voicing) as if they were perceptual facts. §4 known-issue 5.

6. **Retire the loanword-only calibration (NEW, OPEN)** — the cost model is calibrated on adaptation but consumed for recognition and distinguishability. The contrast study is the only non-loanword anchor we have, and it is inventory-level, not word-level. Candidates for a second anchor: perceptual-confusion matrices from the L2 speech-perception literature; ASJP cognate alignments (Jäger-style PMI) as a *within-family* substitution signal that has no orthography in it.

Standing open questions:

- **Representation term formulation (OPEN):** string-similarity vs etymology attribution share (§2).
- **PHOIBLE multi-inventory policy (decided SOFT):** majority vote across a language's inventories (≥50%), chosen in the prevalence study; union and intersection rejected (judgment calls documented there).
- **Diphthong-mediated contrasts (OPEN, new):** binary "has the phoneme" checks under-credit listeners whose inventories carry a vowel quality only inside diphthongs/allophones (Mandarin 918M, Wu 81M — see contrast-study Addendum). The listener-conditioned metric handles this at the word level; decide whether inventory-level analyses need a correction, or whether all downstream decisions should use the word-level metric.
- ~~**Second stop series**~~ **DECIDED 2026-08-05: taken** (§3.3), on the people-weighted reading of §2. The ~61%-of-languages figure is the accepted cost.
- ~~**Glide-selection rule for hiatus**~~ **MOOT 2026-08-05** — the glide-insertion rule is retired and hiatus is legal everywhere (§3.6), so there is no glide to select. The measurement that prompted it: glide insertion cost 0.018 recognizability on international vocabulary and mangled exactly the Greek compounding cases (*geometria* → *gejometrija*).
- ~~**Onset-cluster inventory (OPEN, conditional)**~~ **CLOSED 2026-08-05** — clusters were adopted and the set is enumerated in §3.6: `pr tr kr br dr ɡr fr pl kl fl`. Exhaustive, not productive.
- **Discouragement weights (OPEN — explicitly postponed to lexicon construction by Patrick 2026-08-05):** §3.3 ranks /r/ /h/ > /l/ > /b d ɡ/ as segments to avoid where the lexicon has a choice, and §3.6 adds **Cr/Cl onset clusters** as a structural item on the same footing. All of it is currently ordinal and must become numeric **before the lexicon optimizer runs, and not before then** — the weights are meaningless without the thing they weight. Three constraints on the eventual numbers: the cluster penalty must stay small enough never to override recognizability on a borrowed stem (clusters exist for exactly that); the whole set applies with extra force to particles and basic vocabulary; and a preference against root-internal hiatus and root-internal geminates belongs here too, since both then work as compound-boundary signals (§3.7).
- ~~**Stress rule**~~ **DECIDED 2026-08-05: first syllable** (§3.5). See [`stress-prevalence.md`](stress-prevalence.md); initial was chosen over the headline penultimate on simplicity, and because the penultimate lead depends on collapsing weight-sensitive systems.
- ~~**Case or no case**~~ **DECIDED 2026-08-05: keep case** — sentence-initial + narrowly-defined proper nouns (§3.7). Punctuation, quotes and number formats went FIRM with it.
- ~~**How compounds are written**~~ **DECIDED 2026-08-05: solid** (§3.7). Leaves segmentation ambiguity as a constraint for the lexicon chooser rather than a spelling rule.
- ~~**Support vowel: fixed /i/, or /u/ after a labial?**~~ **DECIDED 2026-08-05: /u/ after a labial** (§3.6), on articulation and Swahili's 3/3-vs-19/19 precedent, the metric being indifferent. It is the `translit.py` default and changes no word under the locked template.
- **Solid compounds: check back in on the two costs (OPEN, new, deferred by Patrick 2026-08-05).** The decision is made (§3.7) and the costs are accepted, but both are worth re-examining once there is a lexicon and a grammar to look at: (a) **segmentation ambiguity** — measure the real rate at which a solid compound admits more than one parse into attested roots, and see whether the geminate and hiatus boundary signals cover enough of it, or whether the lexicon chooser needs an explicit anti-ambiguity term; (b) **the prosodic seam** — §3.5 gives a compound one initial stress, making it prosodically identical to a simple root of the same shape, which is fine on paper and may or may not be fine in speech. Neither is measurable before the lexicon exists.
- **Loan-mapping homophony (OPEN, deferred to the vocabulary stage by Patrick 2026-08-05):** the adaptation ruleset merges 5 international spellings into /s/, 6 into /k/ and 3 into /f/. Zero collisions over 52 words, but that is far too small a sample to see the birthday-problem effect. The full merge table and the four things to check are recorded with the rule in §3.6; **raise this again when the lexicon exists**. The reversible knob is v→f, which /b/ ties on the metric.
- ~~**Compounding: keep or drop**~~ **DECIDED 2026-08-05: keep** (§3.6). Compounds are plain concatenation with no seam repair — geminates and hiatus are both legal results. Consequences that are now live rather than hypothetical: **how compounds are written** (solid / hyphen / space) is still open under §3.7, and compounding is one of the two things §3.2's derivation strategy can be built from.
- **Alignment (DEFERRED INDEFINITELY, 2026-08-05 by Patrick):** nominative-accusative vs ergative vs neutral. With no case marking on core arguments and no verbal agreement, no morphology remains to carry the contrast, so the question does not arise. **Revisit only if something is adopted that makes it relevant** — a passive, an oblique that marks agents, or case forms of pronouns (an isolating language can still have *I/me*; English does). Flagged in the Tier 2 pronoun question as the live route back in.
- **Noun-phrase-internal order (OPEN, new 2026-08-05):** adjective, numeral, demonstrative and possessor order relative to the noun. Tier 0 expected these to fall out of head-directionality; they do not — creoles split 8:7 three times over, so there is no creole answer. Worse, the people-weighted world preference (Dem-N 86.1%, Num-N 89.5%, Adj-N 65.3% of L1) is the *opposite* of the by-language majority in each case, and for demonstratives it also contradicts the weak creole lean (N-Dem, 9 of 14). Decide in Tier 2 on separate grounds. → [`grammar-tier0.md`](grammar-tier0.md) §1.2.
- **Reduplication: adopt as a morphological device? (OPEN, new 2026-08-05):** the most-gained feature in the Tier 0 study (verbs 7 gained / 0 lost across creole-lexifier pairs) and free under §3.6's template. Candidate functions: plurality, intensity, iterativity. Bears on §3.2's derivation strategy and on the lexicon's word-shape budget.
- **Loss shape details (SOFT):** AE + MSE combination is a proposal, not validated.
- ~~**/tʃ/ orthography**~~ **MOOT** — the §3.3 inventory has no /tʃ/; the ASCII orthography is free (§3.7).

---

## Glossary

- **Allophone** — a variant pronunciation of a phoneme that native speakers treat as "the same sound" (English /t/ in *top* [aspirated] vs *stop* [not]).
- **Articulatory features** — dimensions describing how a sound is physically produced (voiced?, nasal?, tongue position, …); the basis for measuring how "close" two sounds are.
- **Coda** — consonant material at the end of a syllable (the /n/ in "san").
- **Cognate** — words in different languages descending from the same ancestral word.
- **Colexification** — one word covering multiple meanings in a language (e.g., "hand" = "arm"); cross-language patterns reveal which meaning distinctions are universal.
- **Doculect** — a language variety as documented by one specific source.
- **Epenthesis** — inserting sounds (usually vowels) to repair illegal clusters: "strike" → "sutoraiku".
- **Fortis/lenis** — the "strong" vs "weak" stop series (/p t k/ vs /b d ɡ/), realized as voicing in some languages and aspiration in others.
- **Glottocode** — Glottolog's stable identifier for a languoid; this project's universal join key.
- **IPA** — International Phonetic Alphabet: standard one-symbol-per-sound notation; /slashes/ mark phonemes, [brackets] mark actual pronunciations.
- **Isolating morphology** — grammar via separate particles and word order rather than word endings (Mandarin-style, not Latin-style).
- **L1 / L2** — native language / a language learned in addition to the native one.
- **Languoid** — Glottolog's umbrella term for any node in the language family tree (family, language, or dialect).
- **Phoneme** — a contrastive sound category of a language: swapping one phoneme for another can change one word into a different word.
- **Phonology / phonotactics** — a language's sound system / its rules for combining sounds into syllables and words.
- **Rhotic** — any r-like sound (trill, tap, English approximant, …).
- **Suprasegmentals** — properties layered over segments: tone, stress, length.
