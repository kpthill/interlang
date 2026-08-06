# Grammar coverage sweep against the Lingua questionnaire

*Run 2026-08-06, against the "grammar is complete" state (19 words, 7 rules) recorded in
[`grammar-plan.md`](grammar-plan.md) §4 and [`principles.md`](principles.md) §3.2. This is
deliverable 2 of the three that §4 says remain. **No committed study script** — the parameter-ID
checks below were run ad hoc over `data/raw/{wals,grambank,apics}/cldf/parameters.csv`; same
logged deviation as the three light-analysis grammar notes.*

**Bottom line up front. The grammar is not complete. Fourteen genuine gaps, four of them
consequential enough to change sentences people will say every day**, plus **five smuggled
premises** of the exact kind the Tier 3 cleanup named. The two biggest are not exotic: **nowhere
does any rule say where a prepositional phrase goes**, and **there is no way to relativize
anything but a subject or a direct object** — so *the knife I cut the bread with* is currently
unsayable.

None of this reopens phonology (§3.3–§3.7), which comes through the sweep clean.

---

## 0. Provenance: I could not obtain the questionnaire

**I could not get the document.** All four routes returned **HTTP 403 from the agent proxy**:
`tulquest.huma-num.fr/en/node/47`, `imp.lss.wisc.edu` (a course page listing the outline),
`llacan.cnrs.fr` (Lahaussois' questionnaire survey), and `hal.science` (the TULQuest archive
paper). The proxy is working as configured; TLS verification was not touched. This is the same
block the project has hit before.

So the checklist below is **reconstructed**, with two different provenances:

- **The syntax section numbering (1.1–1.16) is corroborated `[measured, weak]`** — a web search
  returned the standard Routledge *Descriptive Grammars* syntax outline (1.1 general questions,
  1.2 structural questions, 1.3 coordination, 1.4 negation, 1.5 anaphora, 1.6 reflexives,
  1.7 reciprocals, 1.8 comparison, 1.9 equatives, 1.10 possession, 1.11 emphasis, 1.12 topic,
  1.13 heavy shift, 1.14 other movement processes, 1.15 minor sentence types, 1.16 operational
  definitions), exemplified from Hinds' *Japanese* in that series. That is a search snippet, not
  the primary document.
- **Everything below the top level of §1, and all of §2–§5, is `[recall]`** — my own knowledge of
  the questionnaire and of grammars written to it. Subsection numbers I give for §2–§5 are
  *approximate* and should not be cited as a numbering scheme.

**Consequence for how much this sweep is worth:** it is reliable as a *checklist of topics a
descriptive grammar must cover*, and unreliable as a *citation scheme*. If the actual document is
ever obtained, the gaps found here will still be gaps; what may change is whether anything the
questionnaire asks was missed entirely by my reconstruction. Treat "no gaps found in section X"
as weaker evidence than "gap found in section X".

Every database claim below **is** `[measured]` — parameter IDs and names were read out of the
CLDF files in this repo, not recalled.

---

## 1. The sweep

Four verdicts: **DECIDED** (with pointer), **FORCED** (falls out of an existing rule — the rule is
named), **OUT OF SCOPE** (deliberate, with reason), **GAP** (nobody decided it). Only GAPs and
non-obvious FORCEDs are commented; the long tail of DECIDED items is compressed, since the task
is finding what is missing.

### 1. Syntax

| § | topic | verdict |
|---|---|---|
| 1.1.1.1 | direct vs indirect speech | **GAP-7** |
| 1.1.1.2 | interrogatives — polar, content, echo | **DECIDED** — [`grammar-tier2-questions.md`](grammar-tier2-questions.md): clause-initial particle, content words in situ |
| 1.1.1.2 | **answers to content questions** | **GAP-5** (only *yes*/*no* are licensed as fragments) |
| 1.1.1.3 | imperative, prohibitive, hortative | **DECIDED** — bare VP ([`grammar-tier3-cleanup.md`](grammar-tier3-cleanup.md) §3); same negator ([`grammar-tier2-negation.md`](grammar-tier2-negation.md) §3); no hortative ([`grammar-tier45.md`](grammar-tier45.md) §8) |
| 1.1.1.4 | exclamatives ("How tall he is!") | **GAP-9** (low) |
| 1.1.2.1 | markers of subordination | **DECIDED** — one relativizer, doubling as optional complementizer |
| 1.1.2.2 | complement clauses | **DECIDED** for *say/know*; **GAP-2b** for *want/try/begin* (control) |
| 1.1.2.3 | relative clauses — subject, object | **DECIDED** — relativizer + gap, postnominal |
| 1.1.2.3 | relative clauses — **oblique, possessor** | **GAP-2** |
| 1.1.2.4 | adverbial clauses | **DECIDED** — preposition + noun + REL + clause, postposed ([`grammar-tier3-combination.md`](grammar-tier3-combination.md) §5) |
| 1.1.2.5 | sequence of tenses | **FORCED** — no tense grammar at all (Q6), so nothing can agree |
| 1.2.1.1 | copular sentences | **DECIDED** — [`grammar-tier3-predication.md`](grammar-tier3-predication.md) |
| 1.2.1.2 | valence: intransitive, transitive, ditransitive | **DECIDED** — SVO; indirect-object construction |
| 1.2.1.2 | **placement of obliques / PPs / adverbial phrases** | **GAP-1** |
| 1.2.1.2 | passive | **DECIDED** — preverbal `self` (cleanup §2a) |
| 1.2.1.2 | reflexive | **DECIDED** — one invariant `self` in object position |
| 1.2.1.2 | **reciprocal** | **GAP-3** |
| 1.2.1.2 | **causative** | **GAP-6** |
| 1.2.1.2 | applicative, antipassive, valence morphology | **FORCED** — no affixes (Tier 0) |
| 1.2.1.2 | impersonal | **DECIDED** — `someone break window` (cleanup §2) |
| 1.2.2 | adjective phrase, degree words ("very tall") | **FORCED** — modifier rule (Q11). WALS 91A / APiCS 8 code it; the rule gives the attested order without a separate decision |
| 1.2.3 | adverbial phrase | **FORCED** — modifier rule, for *single-word* adverbs only; multi-word is GAP-1 |
| 1.2.4 | adpositional phrase | **DECIDED** (prepositions, Tier 0) / **GAP-1** (where the phrase goes) |
| 1.2.5 | noun phrase — articles, number, classifiers, modifier order | **DECIDED** — [`grammar-tier2-np.md`](grammar-tier2-np.md) |
| 1.2.5 | **order among stacked prenominal modifiers** | **GAP-8** |
| 1.2.5 | demonstratives — **how many** | **GAP-4** |
| 1.3 | coordination — *and*/*or*/*but*, comitative split, inclusory | **DECIDED** — [`grammar-tier3-combination.md`](grammar-tier3-combination.md) §1 |
| 1.3 | ellipsis under coordination | **DECIDED** — subject only ([`grammar-tier45.md`](grammar-tier45.md) §11); object gapping is **GAP-12** (low) |
| 1.4 | negation — standard, prohibitive, scope, concord | **DECIDED** — [`grammar-tier2-negation.md`](grammar-tier2-negation.md) |
| 1.4 | constituent negation ("not John, but Mary") | **FORCED** — leftmost-widest scope (Q9) puts the negator before whatever it scopes over; worth stating explicitly in the published grammar |
| 1.5 | anaphora, pro-drop, zero anaphora | **DECIDED** — none; subject obligatory (cleanup §3) |
| 1.6 | reflexives — domain, scope | **DECIDED** in the simple case; long-distance and reflexive-possessive ("he loves his own wife") unaddressed, **GAP-11** (low) |
| 1.7 | reciprocals | **GAP-3** |
| 1.8 | comparison — comparative, superlative | **DECIDED** — *than*, *than all* |
| 1.8 | correlative comparison ("the more…the more") | **FORCED**-ish / lexical; not stated. Folded into GAP-12 |
| 1.9 | equatives | **DECIDED** — lexical `same` ([`grammar-tier45.md`](grammar-tier45.md) §12) |
| 1.10 | possession — adnominal, predicative | **DECIDED** — possessor precedes; *have* |
| 1.11 | emphasis / focus | **DECIDED** — vocabulary, not grammar ([`grammar-tier45.md`](grammar-tier45.md) §9) |
| 1.12 | topic | **OUT OF SCOPE**, already flagged — no topicalization; belongs in the bias audit |
| 1.13 | heavy shift | **FORCED** — word order is the sole marker of argument role (Tier 0), so no constituent may move. **Never stated anywhere**; see smuggled premise E |
| 1.14 | other movement processes | **FORCED** — the grammar contains no movement rule of any kind (questions in situ, no inversion, no clefts, no topicalization). This is a genuinely clean result and worth publishing as one |
| 1.15 | minor sentence types — fragments, greetings, formulae | **GAP-5**, **GAP-10** |
| 1.16 | operational definitions of word classes | **DECIDED** — semi-rigid, default class in the lexicon ([`grammar-tier45.md`](grammar-tier45.md) §1). The *diagnostic tests* still have to be written, but that is documentation, not a decision |

### 2. Morphology

| § | topic | verdict |
|---|---|---|
| 2.1.1 | noun inflection — case, number, gender, definiteness | **FORCED / DECIDED** — no case (Tier 0), optional number word, no gender, no articles |
| 2.1.1 | the questionnaire's **semantic-role list** (agent, instrument, comitative, benefactive, source, goal, path, purpose, cause, manner, price, …) | **HANDOFF, not a gap** — with no case these are all prepositions, and *which prepositions exist and whether the set is closed* is a lexicon question. **It is not currently on [`lexicon-plan.md`](lexicon-plan.md)'s agenda and should be**, because this list is the closest thing the project has to a specification for the preposition inventory. Comitative-vs-instrumental ("with John" / "with a knife") is **GAP-13** (low) |
| 2.1.2 | pronouns — personal, reflexive, possessive, interrogative, relative, indefinite | **DECIDED** — Q8, Q10, [`grammar-tier45.md`](grammar-tier45.md) §6 |
| 2.1.2 | **reciprocal pronoun** | **GAP-3** |
| 2.1.2 | **demonstratives — distance contrasts** | **GAP-4** |
| 2.1.3 | verb morphology — voice, TAM, agreement, finiteness | **FORCED / DECIDED** — none; TAM is adverbial (Q6) |
| 2.1.3 | **evidentiality** | **FORCED** — no verb morphology; hearsay/inference are mood, and Q6 made mood an open-class adverb. Grambank **GB323** codes it `[measured]` and no note has ever cited it. Recording the verdict here rather than leaving it silent |
| 2.1.4 | adjectives — agreement, comparison, degree | **DECIDED** — invariant; unmarked in comparatives |
| 2.1.5 | adpositions — person marking (WALS 48A) | **FORCED** — no agreement anywhere |
| 2.1.6 | numerals — cardinal, ordinal, base | **DECIDED** — [`grammar-tier45.md`](grammar-tier45.md) §4 |
| 2.1.6 | **distributive, multiplicative, fractional numerals** | **GAP-10** |
| 2.1.7 | adverbs | **FORCED** — modifier rule |
| 2.1.8 | clitics | **FORCED** — nothing is bound; every grammatical element is a free word |
| 2.2 | derivation | **DECIDED** — generic-noun compounding ([`grammar-tier45.md`](grammar-tier45.md) §2) |
| 2.2 | compounding, headedness | **DECIDED** — head-final, forced by the modifier rule |
| 2.2 | reduplication | **DECIDED** — optional/emphatic, [`lexicon-plan.md`](lexicon-plan.md) §6a.3. Already flagged, not new |

### 3. Phonology — clean

Checked for completeness only; **no decision reopened**, and **no gap found**.

| § | topic | verdict |
|---|---|---|
| 3.1 | segment inventory | **DECIDED** — §3.3, 15C + 5V |
| 3.2 | phonotactics — syllable, clusters, vowel sequences | **DECIDED** — §3.6, (C)V(N) + Cr/Cl, hiatus legal |
| 3.3 | length, stress, tone | **DECIDED** — §3.5, no tone, no length, initial stress |
| 3.3 | **intonation** | **OUT OF SCOPE**, deliberately — Q10 keeps intonation "available, never required" for questions and specifies nothing else. That is the right call for a language whose learners' L1 prosodies differ wildly, but the published grammar should *say* it is unspecified rather than be silent |
| 3.4 | segmental morphophonology — sandhi at seams | **DECIDED** — §3.6, no repair at a compound seam; geminates and hiatus both legal |
| 3.5 | suprasegmental morphophonology — stress under compounding | **DECIDED** — §3.5, one initial stress per word including compounds; the prosodic-seam cost is already an OPEN item in §7 |

**Note the questionnaire's phonology section is where an auxlang is *most* likely to look
complete and be complete**, because it is the one part of the design that was optimized rather
than hand-picked. It is.

### 4. Ideophones and interjections — **GAP-9**

Neither is decided, mentioned, or excluded anywhere in the project.

### 5. Lexicon

**OUT OF SCOPE for a grammar sweep**, and correctly so — [`lexicon-plan.md`](lexicon-plan.md) is
the whole of it. The one thing worth carrying across is the semantic-role list under 2.1.1 above.

---

## 2. The gaps, ranked by consequence

Coding column is `[measured]` — read from `data/raw/*/cldf/parameters.csv` in this repo.

### GAP-1 — Where does a prepositional phrase go? **(most consequential)**

**What is missing.** The only placement rule the grammar has is Q11's: *single-word modifiers
precede their head; clausal modifiers follow it.* **A prepositional phrase is neither.** Nothing
in the grammar says whether *I run to the market* is `I run to market` or `I to market run`, or
where a time or place adjunct sits, or what happens when there are two of them.

**Why this is the worst one.** Every worked example in the notes silently assumes **postverbal**:
`book COP on table`, `I give book to he`, `window self break by man`, `I cut bread with knife`,
`we eat at time REL he arrive`. Five write-ups rely on a placement that no rule states. This is
*precisely* the Tier 3 cleanup's failure mode, and it is higher-frequency than any of the four
features that cleanup caught — PPs appear in a large fraction of all sentences.

It also interacts with a decision already made: Q11a put **adverbs before the verb**
(`quickly run`), so the language would have manner adverbs preverbal and manner PPs postverbal.
That may well be right — it is the heavy-constituent-last logic the modifier rule already uses —
but it is a *third* case in a rule that currently states two, and it has never been argued.

**Coded?** Yes. **WALS 84A** *Order of Object, Oblique, and Verb*; **WALS 85A** *Order of
Adposition and Noun Phrase* (already used for the prepositions decision); **APiCS 4**; and
**APiCS 11** *Order of frequency adverb, verb, and object* — which bears directly on the
adverb-vs-PP asymmetry and **has never been consulted by any note**.

**Recommendation (SOFT):** extend Q11's rule to three cases —
*single-word modifiers precede their head; **phrasal and clausal modifiers follow it***. That
makes PPs postverbal, keeps every existing example legal, preserves the heavy-last principle,
and costs zero words. Then check it against WALS 84A and APiCS 11 before tagging FIRM. **Word
bill 0; it revises rule 1 rather than adding rule 8.**

### GAP-2 — Relativization on obliques and possessors

**What is missing.** *The knife I cut the bread with.* *The man whose house burned.*
[`grammar-tier3-combination.md`](grammar-tier3-combination.md) §3 chose **relativizer + gap** on
WALS 122A, which codes **subjects**, and mentions objects in passing (29 of 54 creoles). It never
decided obliques. Under the adopted strategy `knife REL I cut bread with __` **strands the
preposition** — and preposition stranding is a rare Germanic quirk, exactly the kind of Euro-coded
feature this project's Rule 2 contrapositive exists to catch. `man REL house burn` gives no way to
show the possessive link at all.

**Why it matters.** These are ordinary sentences, not edge cases, and there is currently **no
construction at all** for them — not a suboptimal one, none. The three standard repairs each cost
something the grammar has ruled out or not discussed: a **relative pronoun** (rejected — needs
case), a **resumptive pronoun** (never discussed; APiCS shows relativizer + resumptive in 4 of 9
expanded pidgins, so it is a live contact strategy), or **pied-piping** (`knife with REL I cut
bread` — but the grammar has no fronting rule anywhere).

**Coded?** Yes, and well. **WALS 123A** *Relativization on Obliques* — the note explicitly
*set this feature aside* as inapplicable (correctly, for the *gapless adverbial* construction)
and then never came back to it for the case where it does apply. **APiCS 94** *Instrument
relative clauses* `[measured]` codes exactly this in contact languages and **has never been
consulted**.

**Recommendation (OPEN — this one needs the data, not a taste call):** run WALS 123A and APiCS 94
before choosing. My prior is **resumptive pronoun** (`knife REL I cut bread with he`) — it costs
zero words, reuses the invariant pronouns, needs no movement rule, and is attested in the expanded
pidgins we weight most. The alternative worth pricing is accepting preposition stranding, which is
free but Euro-shaped and would want the Rule 2 contrapositive run on it.

### GAP-2b — Same-subject complements (control): *I want to go*

Split out from GAP-2 because the fix is different. With **no non-finite verb form** (stated in
[`grammar-tier3-combination.md`](grammar-tier3-combination.md) §4) and an **obligatory subject**
(cleanup §3), *I want to go* has to be `I want I go` or `I want REL I go` — a repeated subject in
one of the highest-frequency constructions in any language. **Nobody has said which, or that this
is the answer.**

**Coded?** Yes, and this is the sharpest source finding in the sweep: **WALS 124A *'Want'
Complement Subjects***, **APiCS 97 *'Want' complement subjects***, and **APiCS 98 *Complements of
'think' and 'want'*** all exist in this repo `[measured]`. The combination note used APiCS 95 and
96 (speaking, knowing) and **did not use 97 or 98**, which are the ones that code the hard case.

**Recommendation (OPEN):** run 124A / 97 / 98. This is cheap — the data is on disk — and it is the
single best return on effort in this sweep.

### GAP-3 — Reciprocals

**What is missing.** *They saw each other.* Q8 bought **one invariant reflexive** and said nothing
about reciprocals. Many languages use one form for both, which would be the obvious economy —
except that `self` is now **double-booked**: object-position `self` is the reflexive, preverbal
`self` is the passive (cleanup §2a). Making it the reciprocal too puts three jobs on one word, and
Q8 rejected merging the 3rd-person pronoun with the demonstrative for exactly that reason
("three jobs on one form costs more ambiguity than the one word it saves").

`they see self` would then be both "they see themselves" and "they see each other" — a real and
frequent ambiguity, and one English speakers will not notice they are creating.

**Coded?** Yes: **WALS 106A** *Reciprocal Constructions*, **APiCS 89** *Reciprocal constructions*,
**GB306** *phonologically independent non-bipartite reciprocal pronoun*, **GB115** *bound
reciprocal marker* (inapplicable — no affixes).

**Recommendation (SOFT):** one more word, a dedicated reciprocal, taking the word bill to 20.
The alternative that costs nothing is `they see each other` built from ordinary vocabulary
(`other`) — which is what English does and what the generic-noun principle from
[`grammar-tier45.md`](grammar-tier45.md) §2 would predict. **I lean to the free option**: it fits
the stated design principle (*where a construction needs a semantic category, use the generic noun
for it rather than coining grammar*) and keeps the count at 19. But it should be *decided*, and
WALS 106A / APiCS 89 should be read first.

### GAP-4 — How many demonstratives?

**What is missing.** Every note says "**the** demonstrative", singular. Q7 gave it **article
duty** (definiteness) and Q8 declined to merge it with the 3rd-person pronoun. Nowhere does
anything say whether there is a **proximal/distal contrast** (*this* vs *that*) or a single
distance-neutral form.

**Why it matters more than it looks.** The demonstrative is load-bearing — it is the whole of the
definiteness system. If there is one form, `that house` cannot mean "that house over there"; if
there are two, the "no articles" decision quietly costs two words instead of one, and the running
19 is wrong.

**Coded?** Yes: **WALS 41A** *Distance Contrasts in Demonstratives*, **APiCS 33** *Distance
contrasts in demonstratives*, **GB035** *three or more distance contrasts*.

**Recommendation (SOFT): two — proximal and distal.** A two-way contrast is the world's
overwhelming default and is what nearly every learner already has; a one-way system is the marked
option. But run WALS 41A and APiCS 33 first; both are on disk. Also worth noting **GB036**
(elevation) and **GB037** (visible/non-visible) exist and are obvious rejections — record them as
rejected rather than unconsidered.

### GAP-5 — Fragments: answering a content question

**What is missing.** *Who came?* — *John.* Under the current rules that is not a well-formed
utterance: **every clause has an overt subject**, a **subjectless verb phrase is an imperative**,
and **ellipsis is allowed under coordination only**. The only fragments the grammar licenses are
*yes* and *no* ([`grammar-tier45.md`](grammar-tier45.md) §7).

So `Q what-person come?` must be answered `John come`, and `Q you eat what?` must be answered
`I eat rice`. That may be an acceptable design — full-sentence answers are unambiguous and some
languages strongly prefer them — but **it is a consequence nobody has noticed, in one of the
highest-frequency exchanges in conversation.**

**Coded?** **No.** No source we hold codes answer fragments. Design argument only, like §7 and
§11 of the Tier 4/5 note.

**Recommendation (SOFT): license the fragment answer explicitly** — *a constituent alone may
answer a content question* — as a second named exception alongside coordination ellipsis. It
cannot collide with the imperative (an imperative is a verb phrase; a fragment answer is not) and
it cannot collide with anything else, because it only occurs immediately after a question.
**Word bill 0, +1 rule** — taking the grammar to 8 rules.

### GAP-6 — Causatives

**What is missing.** *I made him go.* Not decided, not excluded, not mentioned. Affixal causatives
are FORCED out (no affixes), so the options are a periphrastic verb (`I make he go`) or a
complement clause (`I make REL he go`).

**Why it is only mid-rank.** It probably *is* resolved by the optional complementizer — `I make he
go` is a well-formed complement clause. But that is an inference nobody has stated, and it sits on
top of a premise that turns out to be false (see smuggled premise A: "exactly one verb per
clause"). It should be written down, not inferred.

**Coded?** Yes: **WALS 110A** *Periphrastic Causative Constructions*, **WALS 111A**
*Nonperiphrastic Causative Constructions*, **GB155** (affixal — inapplicable), **GB156**
(grammaticalized from a verb).

**Recommendation (SOFT): periphrastic, via the ordinary complement-clause construction.
Word bill 0, rules 0** — but state it, and state it as the same construction as GAP-2b so a
learner sees one pattern rather than two.

### GAP-7 — Direct vs indirect speech

**What is missing.** *He said he was coming.* With one relativizer serving as complementizer, the
form is `he say (REL) he come` — and **nothing says whether the embedded `he` is the speaker or
someone else.** English resolves this by indexical shift plus context; languages with quotative
complementizers (including many creoles, where the complementizer is literally 'say') often keep
speech **direct**, so the embedded pronoun is always the original speaker's.

Tense shift is moot — Q6 removed tense entirely — which is the one part of this the grammar has
already answered by accident, and correctly.

**Coded?** **No.** Nothing in WALS, Grambank or APiCS codes direct-vs-indirect speech or indexical
shift. APiCS 95 codes the *form* of the complementizer, not this.

**Recommendation (SOFT): direct speech is the default and pronouns never shift** — `he say "I
come"` — which is the simplest rule statable and matches the say-complementizer pattern that 6 of
9 expanded pidgins use (APiCS 95). Word bill 0. Worth a line in the published grammar because it
is a silent ambiguity, the same class as the *yes/no* trap in
[`grammar-tier45.md`](grammar-tier45.md) §7.

### GAP-8 — Order among stacked prenominal modifiers

*This three big house* or *three this big house*? The modifier rule says modifiers **precede**
their head; it does not order them relative to each other. Q9's leftmost-widest scope rule is
about *scope*, not about NP-internal sequencing, and it does not obviously apply to a
demonstrative and a numeral.

**Coded?** Only piecewise — **GB024/GB025/GB193** and **WALS 87A/88A/89A** code each modifier
against the noun, not against each other. So this cannot be settled from the sources we hold.

**Recommendation (SOFT):** either state a fixed template (**demonstrative – numeral – adjective –
noun**, which is the near-universal order in modifier-first languages `[recall]`) or state
explicitly that the order is free. **Free is the cheaper and more defensible answer** — nothing
disambiguates on it, and a fixed template is one more thing to memorise for no gain. But saying
nothing is the one option that should not survive. Word bill 0.

### GAP-9 — Interjections, ideophones, exclamatives

Questionnaire §4 in full, plus 1.1.1.4 and part of 1.15. **Nothing anywhere in the project
mentions any of them.** For an auxiliary language, *greetings and thanks* are among the first
fifty things anyone learns.

**Coded?** Partly: **GB296** codes whether a language has a definable ideophone class. Nothing
codes interjections or exclamatives.

**Recommendation (SOFT):** **no grammatical ideophone class** (it would conflict with §3.6's
phonotactics, which ideophones characteristically violate — and violating the template is the
whole point of an ideophone), and **interjections and greetings are ordinary lexicon**, handed to
[`lexicon-plan.md`](lexicon-plan.md), which does not currently list them. Exclamatives are an
ordinary degree adverb (`he COP very tall`) plus punctuation, which §3.7 already has. Word bill 0.

### GAP-10 — Distributive, multiplicative and fractional numerals

*Two each*, *twice*, *one third*. [`grammar-tier45.md`](grammar-tier45.md) §4 decided cardinals and
ordinals and stopped.

**Coded?** **WALS 54A** *Distributive Numerals* and **APiCS 34** *Adnominal distributive numerals*
`[measured]`. Nothing codes fractions or multiplicatives.

**Recommendation (SOFT):** all three by the §2 generic-noun compounding pattern — `two-part` for
fractions, `two-time` for multiplicatives, reduplication or `each two` for distributives. This is
the fifth reuse of the same element set and costs zero words. Lexicon-facing; hand to
[`lexicon-plan.md`](lexicon-plan.md).

### GAP-11 — Reflexive domain

Long-distance reflexives (*he said that Mary saw himself/him*) and reflexive possessives (*he loves
his own wife* vs *his wife*) are not addressed. With one invariant `self` and no logophorics
(explicitly rejected, Q8 §5), the default is presumably clause-bounded. **Low consequence, but one
line settles it.** Recommendation (SOFT): `self` is clause-bounded; anything else uses an ordinary
pronoun.

### GAP-12 — Non-subject ellipsis under coordination

`I buy and eat bread` (shared object), `I eat rice and he tea` (gapped verb). Only **subject**
ellipsis is licensed. Low consequence — the workaround is always available — but the rule as
written forbids two patterns that will feel natural to most learners. Recommendation (SOFT): leave
it as is and say so, rather than leave it unstated.

### GAP-13 — Comitative vs instrumental

Is "with John" the same preposition as "with a knife"? **WALS 52A**, **APiCS 69**, **APiCS 70**
code it `[measured]`. GB027 was consulted for *and*-vs-*with*, but not this. Lexicon-facing; hand
to [`lexicon-plan.md`](lexicon-plan.md) with the semantic-role list.

---

## 3. Smuggled premises found

The Tier 3 cleanup named the failure mode: *a write-up that justifies a decision by appeal to a
feature we have not decided has smuggled that feature in.* Five instances, plus one factual error.

### A. "Exactly one verb per clause" — a premise stronger than what was decided

[`grammar-tier45.md`](grammar-tier45.md) §1 argues for **semi-rigid word classes** on the grounds
that every disambiguating cue has been spent, listing: *"no articles (Q7), no case (Tier 0), no
agreement (Tier 0), no derivational affixes (Tier 0), and — **as of the Tier 3 cleanup — exactly
one verb per clause**."*

**The cleanup decided no *serial verbs*, which is not the same claim.** With an **optional**
complementizer, `I know he come` and `I want I go` and `I make he go` all put two verbs in one
string with nothing between them. The surface configuration a serial verb construction produces is
therefore **still generated by the grammar** — the ban is unenforceable at the string level, and
"exactly one verb per clause" is not a property the grammar has.

This does not overturn the word-class decision — the parsing argument survives on the other four
cues, and arguably gets *stronger*, since two adjacent verbs are now more ambiguous rather than
less. But the premise as stated is false, and it is load-bearing in the sentence that reverses the
project's working lean from fluid to rigid. **It should be restated as "no serial verbs" and the
argument re-checked.**

### B. Postverbal PPs, assumed across five write-ups

See GAP-1. `book COP on table`, `I give book to he`, `window self break by man`, `I cut bread with
knife`, `we eat at time REL he arrive` all assume a placement rule the grammar does not contain.
This is the same shape as the four features the Tier 3 cleanup caught, and it is more frequent
than any of them.

### C. "The demonstrative", assumed singular

See GAP-4. Q7 (§4.1) and Q8 (§5) both reason about "the demonstrative" as a single form — Q8's
rejection of the 3rd-person merge is explicitly *"one form carrying three jobs"*, a count that
presupposes there is one demonstrative. If there are two, that argument changes and so does the
word bill.

### D. WALS 123A dismissed for one construction, then never applied to the other

[`grammar-tier3-combination.md`](grammar-tier3-combination.md) §5 correctly shows that WALS 123A
(oblique relativization) does not apply to the *gapless adverbial* construction, calls that a
corrected mis-analysis, and moves on. The note then reads as though 123A has been dealt with. **It
has not** — ordinary oblique relativization was never decided (GAP-2). A feature can be correctly
dismissed for one use and still be owed for another.

### E. "Word order is the only marker of argument role" — true, and never cashed out as a rule

The claim appears in [`grammar-tier3-cleanup.md`](grammar-tier3-cleanup.md) §1 and §4 and in
[`grammar-tier3-combination.md`](grammar-tier3-combination.md) §5, each time as a *premise* used to
reject something. It is correct, and it has a consequence nobody has drawn: **no constituent may
move, ever** — no heavy shift (questionnaire 1.13), no scrambling, no topicalization. That is a
real, publishable property of the grammar and currently exists only as an unstated inference
scattered across three arguments. **Recommendation: state it once as a named property** ("the
grammar contains no movement rule"), which converts 1.12, 1.13 and 1.14 from three silences into
one deliberate decision.

### F. A factual error, not a smuggled premise

[`grammar-tier3-cleanup.md`](grammar-tier3-cleanup.md) §6 states: *"APiCS does not code the
passive, pro-drop or ditransitive order, so those three have no contact-language column at all."*

**Two-thirds of that is wrong, and checkable against files in this repo `[measured]`:**

- **APiCS 90** *Passive constructions* exists — and §2a of the *same note* uses it, in a table
  broken down by lexifier group. The note contradicts itself.
- **APiCS 61** *Order of recipient and theme in ditransitive constructions* exists. The
  ditransitive decision was made on WALS 105A alone, with the contact evidence declared absent
  when it was on disk.

Only **pro-drop** is genuinely uncoded in APiCS. The ditransitive decision may well survive
consulting APiCS 61 — but it was taken while believing no such evidence existed, and standing rule
1 (*quote the n and the coverage*) is not satisfied by a coverage claim that is false. **This
should be re-run; it is a five-minute check.**

---

## 4. What this means for "the grammar is complete"

It isn't, but it is close, and the shape of what is missing is informative.

- **Nothing found here overturns a decision.** No gap requires reopening a FIRM item, and phonology
  is untouched.
- **The word bill moves by at most one or two.** GAP-3 (reciprocal) and GAP-4 (a second
  demonstrative) are the only two that could add words; both have zero-cost options.
- **The rule count moves by one or two.** GAP-1 revises rule 1 rather than adding one; GAP-5 adds a
  rule. Realistic landing point: **19–21 words, 8 rules.**
- **The gaps cluster in one place.** Nine of the fourteen are about **phrases and clauses larger
  than a word but smaller than a sentence** — PP placement, oblique relatives, control complements,
  stacked modifiers, fragments, reciprocals. The tiers were organised by *how much would have to be
  redone if this flipped*, which front-loaded the big parameters and left the mid-level combinatorics
  to fall out of the modifier rule. Mostly they did. **Where they didn't, nobody was looking**, and
  that is the structural reason the Tier 3 cleanup and this sweep found the same kind of thing.
- **Four features had evidence on disk that was never consulted**: APiCS 11 (adverb/object order),
  APiCS 94 (instrument relatives), APiCS 97/98 and WALS 124A (want-complements), APiCS 61
  (ditransitive order). None required new data. **That is the cheapest possible next session.**

**Suggested order of work:** GAP-2b and GAP-2 first (data is on disk, and they are the two the
language currently *cannot express*), then GAP-1 (highest frequency, and it is a rule revision),
then GAP-3 and GAP-4 (both cheap, both coded), then the rest as a batch of one-liners.

---

## 5. Honest limits

- **I could not obtain the questionnaire.** §0 says exactly what was tried and what was blocked.
  The checklist is `[recall]` below the top level of §1. **A gap in my reconstruction is invisible
  to this sweep** — the most likely places for that are the fine detail of §1.2 (structural
  questions) and the semantic-role list in §2.1.1, both of which are long in the original and
  compressed here.
- **No committed study script.** The database checks were ad hoc reads of `parameters.csv`. They
  establish that a parameter *exists*, not what it *says* — **I have not run a single distribution
  in this note**, and every recommendation tagged SOFT or OPEN is a prior awaiting the data, not a
  result. That distinction matters more than usual here, because the project's two recorded errors
  (the passive, and "it's ordinary vocabulary") were both *reasoning without looking*.
- **Consequence rankings are my judgment**, informed by construction frequency rather than measured
  from a corpus. The project has no corpus of its own language, so it cannot be otherwise yet.
- **The FORCED verdicts are arguments, not proofs.** Where I have written FORCED, I have named the
  rule it follows from, so each can be checked. Two of them (1.13 heavy shift, 2.1.3 evidentiality)
  are FORCED only in the sense that no machinery exists to do otherwise — which is exactly the
  reasoning that produced the false passive rejection. They are the two most worth a second look.
- **Smuggled premise A is a judgment call about wording.** One could read "exactly one verb per
  clause" as loose shorthand for "no serial verbs". I have reported it because the sentence is
  load-bearing in a decision reversal and because the two claims come apart precisely where the
  optional complementizer sits — but a reader who disagrees loses nothing else in this note.
