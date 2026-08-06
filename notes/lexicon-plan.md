# Lexicon: the plan, the sources, and how concept space gets divided

*Written 2026-08-06, opening the vocabulary phase. No study script yet — this is the
methodology document that says what the scripts will do and why, the equivalent of
[`grammar-plan.md`](grammar-plan.md) for the lexicon. Companions:
[`principles.md`](principles.md) §2 (the two objectives), §3.3/§3.6/§3.7 (the phonological
box the lexicon must fit in), §7 (open questions this note inherits and adds to);
[`grammar-plan.md`](grammar-plan.md) §1–2 (why creoles are the north star, and the two
creole evidence rules).*

**Provenance policy for this document.** Everything numeric here is either (a) computed
during the writing of this note from data already on disk in `data/raw/`, marked
**[measured]**, (b) read from a file fetched over the network while writing, marked
**[verified]** with the URL, or (c) general linguistic knowledge with no source checked,
marked **[recall]**. This project is strict about provenance and the (c) items are the ones
to distrust. No numbers below are estimated or remembered from a source I did not open.

---

## 0. What this stage has to deliver

Three things, in this order:

1. **A concept inventory** — the list of meanings the language must be able to express, and
   the decision, per concept, of whether it gets a **root**, a **compound**, or only a
   **description** (§2).
2. **A form for each root** — which source languages a root draws on, chosen against §2's
   two objectives by the recognizability metric. That is the optimizer, and it is *not*
   what this note is about.
3. **A bias audit** of the result, as [`grammar-plan.md`](grammar-plan.md) §1 requires of
   the grammar: report where the concept divisions and the word forms landed
   genealogically and areally, as a measured statement rather than an absorbed bias.

**§7 of `grammar-plan.md` put representation here.** Grammar was optimised for learnability
alone because there is no grammatical analogue of an etymology; the lexicon is where
fairness becomes measurable and therefore where it is owed. That has a consequence this
note takes seriously: **representation is not only about whose word-forms we borrow. It is
also about whose way of carving up meaning we adopt** — and the second is invisible unless
we go looking for it. §4 is that search.

---

## 1. The box the lexicon has to fit in

Everything in this list is already FIRM or SOFT and closed. Stated here because each one
bites on a lexicon decision, and it is easier to see the shape of the problem with the
constraints collected in one place.

| Constraint | Source | Where it bites on the lexicon |
|---|---|---|
| 15 consonants + 5 vowels | §3.3 **FIRM** | Root-form space |
| (C)V(N), N ∈ {n, m}, plus ten Cr/Cl onsets | §3.6 **FIRM** | **~180 cluster-free monosyllables avoiding the discouraged segments** — the short-word budget |
| /r/, /h/ most discouraged, then /l/, then /b d ɡ/; small cost on Cr/Cl onsets | §3.3, §3.6 **FIRM as ordinal, weights OPEN** | **Must become numbers before the optimizer runs.** §2.6 below is my recommendation for how |
| l~r and h~r never a minimal pair | §3.3 **FIRM** | A hard constraint on the form assignment, not on the concept inventory |
| Compounding is free: plain concatenation, no seam repair, geminates and hiatus legal, written solid | §3.6, §3.7 **FIRM** | **The tier-2 device.** Costs nothing structurally, so the only thing rationing compounds is length and inferability |
| Geminates occur only at a seam; root-internal hiatus disfavoured | §3.6, §3.7 | Two weak boundary signals the lexicon chooser should strengthen, not waste |
| **No derivational affixes** | §3.2 **SOFT** (Tier 0: creoles 35 losses : 3 gains) | There is no third word-formation device. Compounding is it |
| Reduplication available, undecided | §3.2, §7 **OPEN** | Bears directly on §2 — see §2.7 |
| Grammar needs ~16 words total, 5 rules | Tiers 0–3, complete | **Essentially the whole lexicon is open-class.** The grammar has already taken under 9% of the short-word space |
| Stress always initial; one letter per phoneme; no sandhi | §3.5, §3.7 **FIRM** | A compound is prosodically indistinguishable from a simple root of the same shape |
| ~10–14 TAM concepts flagged for short forms | §3.2 (Q6 handoff) | A pre-existing claim on the monosyllable budget |
| Loan-mapping merge table (fan-in 6 into /k/, 5 into /s/, 3 into /f/) | §3.6 **SOFT** | Homophony must be re-checked at lexicon scale; v→f is the reversible knob |
| "they" = the plural word? | §7 **OPEN** | An economy decision explicitly deferred to here |

Two of these are worth restating because they change the character of the problem.

**There are no derivational affixes, so the tier system is genuinely three-valued.** In
Esperanto, "the thing between root and phrase" is a large graded space: *-ejo*, *-ilo*,
*-isto*, *mal-*, *-ig-* let you build a semantically predictable word of almost any
specificity. We have deleted that middle. Our middle tier is **compounding only**, which is
a blunter instrument: `X-place` is a compound, not a suffix, and it is exactly as long as
its parts. This makes the root/compound boundary matter *more* than it does in a language
with affixes, because the cost step between the tiers is bigger.

**The grammar left the lexicon almost the entire short-word budget.** 16 grammatical words
out of ~180 cluster-free monosyllables. That is unusually generous and it means the tier
decision is not being forced by phonological scarcity — we can afford a few hundred roots
of one or two syllables without strain. The constraint that bites is **learning cost**, not
form space. Say so explicitly rather than letting the ~180 figure do rhetorical work it
does not deserve.

---

## 2. The central question: root, compound, or description?

### 2.1 The economics, stated precisely

A concept can be given:

- **Tier 1 — an underived root.** *Cost:* one item of rote memory per learner, permanently;
  one form consumed from the phonological space; and a place in the homophony/minimal-pair
  budget. *Benefit:* shortest possible form, no compositional ambiguity, and it can itself
  become a compounding element for other concepts.
- **Tier 2 — a compound of existing roots.** *Cost:* length (roughly the sum of the parts,
  since there is no seam repair to shorten it), plus **inferability risk** — the learner
  must be able to get from the parts to the meaning, and from the meaning back to the parts.
  *Benefit:* zero new rote memory if the compound is transparent, and it is generative.
- **Tier 3 — a multi-word description, with no fixed form.** *Cost:* verbosity, and the fact
  that different speakers will describe the same thing differently, so it is not a
  *word* at all — it does not aid mutual comprehension the way an agreed compound does.
  *Benefit:* free. Nothing to learn, nothing to standardise.

The naive criterion is "frequency": common things get roots. That is not wrong but it is
not sufficient, because it ignores the thing that actually makes a compound cheap or
expensive, which is whether its meaning is **predictable from its parts in both
directions**.

### 2.2 The recommendation (SOFT)

> **A concept gets a root if and only if a compound would not be reliably inferable, or the
> concept is frequent enough that the compound's length cost outweighs the root's learning
> cost. Otherwise it gets a compound. It gets only a description when the world's languages
> do not treat it as a lexical item at all.**
>
> Operationally, score every candidate concept on four axes and threshold on the combination:
>
> | Axis | What it measures | Instrument | Status |
> |---|---|---|---|
> | **A. Cross-linguistic lexicalization** | Do the world's languages give this concept a simple word, or do they build it? | **WOLD `Analyzability`** (§2.3) — on disk, 41 languages, 1,814 concepts | **measured, works** |
> | **B. Frequency / communicative load** | How often is it needed? | Concept-list membership as a stacked proxy (§3.4) | proxy only, weak |
> | **C. Compositional predictability** | Would a learner derive the compound from the meaning, and the meaning from the compound? | **No corpus instrument exists** — this is a judgment call (§2.4) | **the honest gap** |
> | **D. Boundary risk** | Does our chosen carving match how languages actually divide this region of meaning? | **CLICS colexification** (§4) | **available, unverified against our use** |
>
> Axis A is the one that is both cheap and empirical, and it should be the **default
> ranking**, with C used to override it in the direction of "root" and never in the
> direction of "compound".

The asymmetry in the last sentence is the load-bearing part. **When in doubt, promote to
root.** A concept given a root that could have been a compound costs one memorised item. A
concept given a compound whose meaning is not inferable costs a memorised item *and* an
actively misleading form — the learner reads the parts, derives the wrong meaning, and is
wrong with confidence. `firetruck` is fine; *`fire-wagon`* meaning "ambulance" would be
worse than an arbitrary root. The failure modes are not symmetric, so the threshold should
not be either.

Tagged **SOFT**: the shape is right and I expect it to survive, but the thresholds are
numbers nobody has picked yet, and axis C has no instrument.

### 2.3 Axis A has a real instrument, and it is already on disk

**This is the main practical finding of this note.** WOLD's `forms.csv` carries an
`Analyzability` column, per word, per language, with five values —
`unanalyzable` / `semi-analyzable` / `analyzable derived` / `analyzable compound` /
`analyzable phrasal`. That is *precisely* the tier question, asked of 41 languages across
24 families for 1,814 concepts, and we already have it locally because WOLD was fetched for
the cost-learning study.

**[measured]** over `data/raw/wold/cldf/forms.csv`, 64,289 forms, 41 languages:

| Analyzability | forms | share |
|---|---:|---:|
| unanalyzable | 43,643 | 67.9% |
| analyzable derived | 6,920 | 10.8% |
| analyzable compound | 6,646 | 10.3% |
| analyzable phrasal | 4,174 | 6.5% |
| semi-analyzable | 2,902 | 4.5% |

Define a concept's **root rate** as the fraction of languages that give it at least one
unanalyzable word. Restricted to the 1,372 concepts attested in ≥25 of the 41 languages
(the restriction matters — see the caveat below), **[measured]**:

| quantile | 5% | 10% | 25% | 50% | 75% | 90% | 95% |
|---|---|---|---|---|---|---|---|
| root rate | 0.38 | 0.46 | 0.59 | **0.73** | 0.85 | 0.93 | 0.95 |

Mean 0.704, median 0.730, min 0.079, max 1.00.

**The extremes validate the instrument.** The 25 lowest-scoring well-covered concepts
**[measured]**:

> twice/two times 0.08 · three times 0.09 · the nostril 0.12 · the defendant 0.17 ·
> third 0.17 · the plaintiff 0.17 · fifteen 0.17 · the day before yesterday 0.18 ·
> the fisherman 0.18 · the stepdaughter 0.18 · the spider web 0.18 · the stepfather 0.19 ·
> the stepmother 0.19 · the arson 0.20 · the earlobe 0.21 · the stepson 0.21 ·
> innocent 0.21 · the eyelid 0.23 · to surrender 0.23 · the potter 0.23 · to convict 0.24 ·
> the married woman 0.24 · the native country 0.24 · the day after tomorrow 0.25 ·
> to kneel 0.26

Every one of those is something a designer would independently have made a compound:
ordinals and multiplicatives, step-kin, agent nouns, part-of-a-part body terms, legal
roles. At the other end, concepts at root rate 1.00 across 31–41 languages are *tooth,
blood, flesh, mountain-or-hill, bottle, iron, dish, rice, bear, and, at* — the things no
language builds out of other things.

Aggregated **[measured]**, same n≥25 restriction:

| by word class | root rate | | by semantic field (extremes of 24) | root rate |
|---|---:|---|---|---:|
| Verb (n=331) | 0.623 | | Law (n=25) | **0.477** |
| Adjective (n=120) | 0.687 | | Emotions and values (n=48) | 0.628 |
| Function word (n=97) | 0.689 | | Religion and belief (n=23) | 0.631 |
| Noun (n=820) | 0.741 | | … | … |
| | | | Agriculture and vegetation (n=58) | 0.782 |
| | | | Animals (n=99) | 0.786 |

Two readings worth keeping. **Verbs are the most compositional class**, which is a warning:
a language with no derivational affixes and no serial verbs has fewer ways to build a verb
than to build a noun, and verbs are where our missing middle tier will hurt most.
**Law is the most compositional field in the world's languages** (0.477) — legal vocabulary
is built, everywhere, out of ordinary words. That is a licence to give the whole domain
zero roots.

**Caveats on this instrument, logged rather than tolerated:**

1. **The n≥25 restriction is not optional.** Over all 1,814 concepts the mean root rate is
   0.731, and non-core concepts appear to score *higher* (0.853) than core ones (0.702)
   **[measured]** — which is backwards, and is a coverage artifact: a rare concept is
   recorded in WOLD mainly by the languages that happen to lexicalize it simply. **Any
   script using this must restrict to well-covered concepts and say what the cutoff was.**
2. **41 languages is small** and WOLD's recipient set is a convenience sample built for
   loanword study, not a typological sample. It is 24 families, which is respectable, but it
   is not CLICS's 200.
3. **"Analyzable" conflates compound with derived**, and 10.8% of forms are derived. We have
   no derivational affixes, so a concept that the world builds by *derivation* is one we
   must build by compounding or make a root. The instrument tells us "not a simple root";
   it does not tell us "and a compound will work."
4. **Analyzability is a fact about a source language's history, not about learnability.**
   English *understand* is analyzable and completely non-inferable. The measure counts
   morphological transparency, not semantic transparency, which is exactly axis C — and
   axis C is the one we cannot measure.

### 2.4 Axis C is a judgment call, and it should be documented as one

**There is no cross-linguistic corpus of "is this compound inferable from its parts".** I
looked; what exists (Concepticon, CLICS, IDS, WOLD) codes *meanings* and *forms*, not
*compositional predictability*. Psycholinguistics has semantic-transparency norms for
compounds, but per-language and per-experiment, not cross-linguistically **[recall — I did
not check for such a dataset]**.

Since it cannot be measured, it should be **procedural**. Recommendation, **SOFT**:

- Every proposed compound is written down with a **paraphrase and a back-derivation test**:
  given the meaning, would a learner produce these parts? Given the parts, would a learner
  produce this meaning? A compound passes only if both directions are plausible.
- **The reverse direction is the one that fails.** `water-house` → learners will not guess
  "bathroom" from the meaning even if they can read it backwards. The forward test alone is
  too permissive, and is how Esperanto's *-um-* problem happens.
- **Compounds that fail the reverse test but are wanted anyway get promoted to roots**, per
  §2.2's asymmetry. They are not "compounds with a note".
- The judgment gets logged next to the compound in the lexicon data file, not in prose, so
  the failure rate is countable later.

This is a deliberate deviation from the project's preference for measured criteria, and it
is here because the alternative is pretending. It is also the natural place for a future
experiment — a compound-inferability test on actual humans is the one study in this project
that would need participants rather than databases.

### 2.5 Where tier 3 (description only) applies

A concept gets **no fixed form at all** when the world's languages do not agree that it is a
lexical item. Concretely, three groups:

- **Compositional grammatical series** the grammar already generates. Q10 built the
  interrogatives from one root plus compounding (*what-person*, *what-time*); Q7 built
  definiteness from the demonstrative; Tier 3 built adverbial clauses from
  preposition+noun+relativizer. These are already tier 2 or 3 by prior decision and should
  not be re-litigated.
- **Numerals above the base, ordinals, multiplicatives.** *fifteen* at 0.17, *third* at
  0.17, *twice* at 0.08 **[measured]** — the world builds these, and so should we.
- **Whole domains that are culturally local.** Law (0.477), and specialised
  agriculture/food/animal vocabulary. If the concept is *the jowar* or *the manioc juice*,
  the language should not have a word; it should have a description or a loan, decided
  when someone needs it.

**Recommendation (SOFT): the shipped lexicon should be explicitly open at the bottom.** It
publishes roots and a set of *sanctioned* compounds, and says that beyond those, description
is the intended mechanism and new compounds are the users' to coin. Toki Pona demonstrates
that a very small root set plus description is communicatively viable **[recall — I have not
verified any toki pona figure and no toki pona list is in Concepticon (§3.2)]**; Ogden's
Basic English is the same bet at 850 words. We are not going as far as either, but the
bottom of the lexicon should be a policy, not a boundary.

### 2.6 What this implies for the deferred discouragement weights (§7)

§7 says the segment and cluster penalties must become numeric "before the lexicon optimizer
runs, and not before then". The tier system tells us the shape they should take:

**Recommendation (OPEN, for Patrick): make the discouragement weight a function of tier and
expected frequency, not a constant.** §3.3 already says the ranking "applies with extra
force to particles and basic vocabulary" — that is the same idea, stated ordinally. The
concrete version: penalty = base_segment_cost × frequency_weight, where frequency_weight is
highest for the 16 grammatical words, high for tier-1 roots that are frequent compounding
elements, and ~1 for everything else. A root that appears inside forty compounds pays its
/r/ forty times.

This also gives the cluster cost its natural calibration: §3.6 requires the cluster penalty
to stay small enough never to override recognizability on a borrowed stem. Under a
frequency-weighted scheme that falls out, because borrowed technical stems are by definition
low-frequency and non-compounding.

### 2.7 Reduplication (§7, OPEN) bears on this and should be decided here

Reduplication is the single most-gained feature in the Tier 0 creole study (13:2 with
compounding; verbs 7 gained / 0 lost) and is free under §3.6's template. It is the only
candidate for a *fourth* word-formation device, and it would partially restore the middle
tier that "no derivational affixes" deleted.

**Recommendation: decline it, and record the reason** — **SOFT**, and genuinely close.

- The functions it is attested for (plurality, intensity, iterativity) are all already
  handled: Q7 made number optional with a plural *word*, and Q6 made aspect and degree
  open-class adverbs. Adopting reduplication would give a *second* way to say things the
  language can already say, which is the failure mode §3.2's TAM decision was taken to
  avoid ("an asymmetry a learner cannot see the reason for").
- It collides with §3.7's segmentation problem. A reduplicated form is a compound of a root
  with itself; with solid writing, no seam repair and geminates legal, `kan` + `kan` →
  `kankan`, which is indistinguishable from a root of that shape. We would be adding
  parse ambiguity to buy a device we do not need.
- The creole evidence is Rule-1 strong but it is evidence about **what emerges**, not what
  is **learnable when taught** — `grammar-plan.md` standing rule 6. This is exactly the
  licensed-departure case, and it makes the language simpler, which is the standing policy
  recorded in §3.2's Tier 3 note.

If Patrick disagrees, the place it would earn its keep is **verbs** — the most compositional
word class (0.623) and the one with the fewest alternatives.

---

## 3. Concept inventories: what exists, verified

### 3.1 What is already on disk

| Resource | Status | Contents | Use here |
|---|---|---|---|
| **WOLD** `data/raw/wold/` | **on disk** | 41 languages, 1,814 concepts, 64,289 forms. Per-concept `Concepticon_ID` (1,459 mapped), `Core_list` (1,460 = the LWT list), `Semantic_field` (24), `Semantic_category`, `Borrowed_score`, `Age_score`, `Simplicity_score`; per-form `Analyzability` **[measured]** | **The axis-A instrument (§2.3), and a Concepticon-mapped 1,460-concept starting inventory. The most valuable thing we already own.** |
| **PHOIBLE, Glottolog, WALS, Grambank, APiCS, CLDR** | on disk | — | Unchanged roles |
| **ASJP** | **NOT on disk** — `data/raw/asjp/` does not exist, though the README lists it **[measured]** | 100 concepts, 11,540 doculects | Re-fetchable; `lexibank/asjp` master is `0127953…`, matching the README's recorded v21 commit **[verified via `git ls-remote`]**. *Correction to an earlier draft of this note: the README is **not** wrong — it lists ASJP in the raw-data **fetch table** with its clone command, and `data/raw/` is gitignored and disposable by design (CLAUDE.md: "raw data is disposable, constructed data is not"). ASJP simply has not been fetched in this container. Nothing depends on it.* |

**WOLD's `Core_list` is the LWT 1460 list = Concepticon `Haspelmath-2009-1460`
[verified].** So we already hold a curated, Concepticon-mapped, 1,460-concept meaning list
with borrowability and analyzability scores attached, without fetching anything.

### 3.2 What is available externally — all probed while writing this note

Every row below was checked by an actual request. No row is asserted from memory.

| Resource | Reachable? | What it actually is | Verdict |
|---|---|---|---|
| **Concepticon** (`concepticon/concepticon-data`) | **yes** — `git ls-remote` OK; `concepticon.tsv` fetched, **4,165 concept sets, all with definitions** **[verified]** | The catalog of concept *sets* plus **480 concept lists** mapped onto them **[verified]**. Ontological categories: Person/Thing 2,532 · Action/Process 850 · Property 365 · Other 209 · Number 163 · Classifier 46 **[verified]** | **Take it. This is the join key for the whole stage** — exactly as Glottocode is for the language-level studies. Everything else in this table speaks Concepticon |
| **CLICS³** (`clics/clics3`) | **yes** | 30 datasets, **3,156 varieties / 2,271 Glottocodes / 200 families / 2,906 concept sets** **[verified]**. Ships **prebuilt artefacts**: `clics3.sqlite.zip` (90.1 MB) and `clics3-network.gml.zip` (12.2 MB, 70.6 MB unzipped) **[verified — I downloaded and parsed the latter]** | **Take it, and take the prebuilt network, not the pipeline.** The documented build requires installing 30 lexibank packages. The GML has everything §4 needs. See §4 |
| **IDS** (`lexibank/ids`) | **yes** | **319 varieties, 1,310 concepts, 437,902 lexemes**, Concepticon 100%, Glottolog 98%, synonymy 1.28 **[verified from README]**. = Concepticon `Key-2016-1310` | **Take it** if we need form-sourcing beyond WOLD's 41 languages. Also already inside CLICS3 (dataset #13) |
| **NorthEuraLex** (`lexibank/northeuralex`) | **yes** | **107 varieties, 1,016 concepts (954 Concepticon sets), 121,611 lexemes**, IPA-normalized, BIPA 100% **[verified from README]** | **Take it only for form quality, never as evidence.** It is *Northern Eurasia* — genealogically narrow by construction. Using it to decide anything about universality would be Eurocentrism by dataset selection |
| **Leipzig-Jakarta list** | **yes**, as Concepticon `Tadmor-2009-100`, 100 items, tagged `ranked` **[verified]** | The 100 most borrowing-resistant meanings, derived from the LWT/WOLD project | **Take it.** Note it is *derived from data we already hold* — but reconstructing it from our `Borrowed_score` naively does **not** work: sorting our copy puts 25+ concepts at exactly 0.000 because they are attested in one or two languages **[measured]**. **Use Concepticon's list; do not re-derive** |
| **Swadesh lists** | **yes** — `Swadesh-1955-100`, `Swadesh-1952-200`, `Swadesh-1971-100`, `Swadesh-1955-215` and dozens of derivatives among the 480 **[verified]** | Lexicostatistic stability lists | **Use as a frequency/coreness proxy only.** They were built to detect genetic relatedness, not to be a basic vocabulary, and their well-known Eurocentrism is exactly the failure §4 exists to catch |
| **Ogden's Basic English** | **partially** — Concepticon has `Ogden-1930-100` ("operational") and `Ogden-1930-200` ("picturable") **[verified]** | **300 of the 850 words only.** The full 850 is not in Concepticon | **Use as precedent, not as data.** Its interest is the *method* — a defining vocabulary closed under paraphrase — not the list |
| **Longman Defining Vocabulary** | **not in Concepticon** — searched all 480 lists, no match **[verified]** | ~2,000 words in which LDOCE definitions are written | **Precedent only, and I could not obtain it.** It is the closest existing thing to "a vocabulary provably sufficient to define everything else", which is the exact property tier 3 depends on. If it can be obtained, it is the single most relevant non-database resource to this note |
| **NSM semantic primes** (Wierzbicka/Goddard) | **yes** — `Goddard-2011-63` (63 primes), `Goddard-2002-59`, `Goddard-2001-42` **[verified]** | Claimed universal indefinables | **Use as a cross-check on the root tier, not as the root tier.** See below |
| **Toki Pona** | **not in Concepticon** — searched, no match **[verified]** | ~120–137 roots **[recall — unverified]** | Precedent only |
| **Lexibank** | reachable but **not examined** | The umbrella of CLDF wordlists that CLICS3 aggregates | Deferred. CLICS3 already gives us the aggregate; individual datasets only matter if form-sourcing needs them |

**On NSM.** 63 claimed-universal primes is a tempting root list, and it is the wrong tool
here. The NSM claim is that these are *indefinable* — that everything else can be
paraphrased into them. That is a claim about the bottom of the definitional hierarchy, not
about what deserves a word: nobody wants a language where "red" is a phrase. Its correct
use is a **falsification check**: if a concept is an NSM prime and our procedure assigned it
tier 2 or 3, that is a flag to re-examine, because it would mean we are proposing to build
something out of parts that a serious body of work says has no parts.

### 3.3 Recommendation on the inventory

**SOFT:**

1. **Concepticon is the identifier system.** Every concept in our lexicon carries a
   Concepticon ID. This is non-negotiable in the same way Glottocode is — it is what makes
   WOLD, CLICS, IDS and the concept lists joinable at all, and it is free because WOLD's
   parameters already carry it.
2. **The starting inventory is WOLD's `Core_list` (LWT 1460)**, already on disk and already
   Concepticon-mapped, **restricted to the 1,372 concepts with ≥25 languages of coverage**
   so axis A is computable for all of them.
3. **Stack the concept lists as a coreness score, don't pick one.** For each concept, count
   membership in `Tadmor-2009-100`, `Swadesh-1955-100`, `Swadesh-1952-200`,
   `Goddard-2011-63`, `Ogden-1930-100/200`. That stacked count is axis B — a crude
   frequency proxy, but a *transparently* crude one, and better than any single list because
   the lists' biases differ. **Log it as a proxy for frequency, not frequency**; we have no
   cross-linguistic frequency data and should not pretend otherwise.
4. **IDS is the form-sourcing expansion**, fetched only when the optimizer needs word forms
   from more than WOLD's 41 languages.
5. **Do not use NorthEuraLex for anything evidential.**

---

## 4. Avoiding Eurocentrism in how concept space is divided

### 4.1 The problem, stated as a design failure rather than a virtue

The project's stated goal is bias that is "chosen, explicit, and measured". The
word-form side of that is already instrumented — the metric measures recognizability, and
§2's two objectives price whose languages we borrow from. **The concept-division side is
not instrumented at all, and it is the easier one to get wrong**, because a designer working
in English does not experience English's carvings as choices.

Concrete cases: English splits *arm* / *hand*, *blue* / *green*, *know*-a-fact /
*know*-a-person, and conflates path and manner in motion verbs. Each of those is a decision
about how many words a region of meaning gets, and each is currently made by default. If we
build a lexicon by translating an English concept list into optimized forms, we ship English
semantics in interlang phonology — which is a *worse* outcome than Esperanto's, because
Esperanto's European bias is at least visible in its word-shapes.

### 4.2 CLICS is the right instrument, and here is exactly how to use it

**Colexification**: one word covering two meanings in one language. CLICS aggregates this
across its 3,156 varieties: for every pair of Concepticon concepts, how many languages and
how many *families* use a single word for both.

The proposal, concretely:

> **For each pair of concepts our draft lexicon proposes to give two different roots,
> compute the CLICS colexification rate. Where a large majority of families that have both
> concepts use one word, our split is a minority position and must be justified, not
> assumed. Where families overwhelmingly keep them apart, the split is safe.**

Mechanically:

1. Download `clics3-network.gml.zip` (12.2 MB) — the published `-t 3 -f families` network,
   i.e. every edge is attested in **≥3 families**. Parse nodes (Concepticon ID, gloss,
   `FamilyFrequency`, `LanguageFrequency`) and edges (`FamilyWeight`, `LanguageWeight`,
   `WordWeight`). **[verified — I did exactly this: 2,919 nodes, 4,228 edges, 1,647 nodes
   with at least one edge]**
2. For a candidate pair (A, B), report
   **`FamilyWeight(A,B) / min(FamilyFrequency(A), FamilyFrequency(B))`** — the share of
   families that *could* colexify and do. **This is a lower bound**: the true denominator is
   "families attesting both", which is ≤ min of the two, so real rates are at or above the
   figures below. The exact denominator needs the SQLite database rather than the GML —
   **a known limitation, and the reason to consider taking the 90 MB SQLite too.**
3. Threshold and act. Proposal, **OPEN on the numbers**:
   - **rate ≥ 0.60** → *merge by default*. Our two-root split is a minority position
     worldwide. One root, and if the distinction is needed, a compound or modifier makes it.
   - **0.35–0.60** → *flag for decision*, and record which way we went and why. The world
     genuinely disagrees; this is where §2's representation objective has to be spent
     deliberately.
   - **rate < 0.35** → *split is safe*, no note needed.
4. **Run it in both directions.** Not only "should these two roots be one?" but also, for
   every concept in the inventory, **look at its colexification neighbourhood** and ask
   whether our single root is being asked to cover a region that most families divide. The
   CLICS network's degree distribution is the entry point: **[measured]** the
   highest-degree nodes are *GIVE* (41 partners), *SAY* (37), *KILL* (28), *GET* (28),
   *EAT* (28), *CUT* (27), *DIG* (26), *SEE* (26), *SEIZE* (26), *CARRY* (25) — i.e.
   high-frequency verbs, which is also where axis A said our missing derivational middle
   would hurt most (§2.3). **The two independent analyses point at the same place: verbs are
   the hard part of this lexicon.**

### 4.3 What it actually says — measured, not asserted

**[measured]** from the CLICS3 network I downloaded and parsed. Format: families colexifying
/ min-families-with-either = lower-bound rate, and the language count.

**Splits where English is in the global minority — our default should be one root:**

| pair | families | lower-bound rate | languages |
|---|---|---|---|
| SON-IN-LAW (of man) ~ (of woman) | 49 / 56 | **0.88** | 261 |
| DAUGHTER-IN-LAW (of man) ~ (of woman) | 47 / 54 | **0.87** | 234 |
| MALE (of person) ~ MALE (of animal) | 45 / 55 | **0.82** | 145 |
| KNIFE ~ KNIFE (for eating) | 51 / 63 | **0.81** | 268 |
| SEA ~ OCEAN | 41 / 51 | **0.80** | 101 |
| FEMALE (of person) ~ FEMALE (of animal) | 44 / 58 | **0.76** | 146 |
| **MOON ~ MONTH** | 57 / 76 | **0.75** | 324 |
| PLATE ~ DISH | 44 / 61 | 0.72 | 155 |
| SKY ~ HEAVEN | 40 / 56 | 0.71 | 117 |
| **MEAT ~ FLESH** | 47 / 67 | **0.70** | 252 |
| HEAR ~ LISTEN | 48 / 72 | 0.67 | 107 |
| **TREE ~ WOOD** | 59 / 89 | **0.66** | 348 |
| SKIN ~ LEATHER | 46 / 70 | 0.66 | 236 |
| LANGUAGE ~ WORD | 49 / 76 | 0.64 | 148 |
| FOOD ~ MEAL | 40 / 65 | 0.62 | 124 |

**And now the counterintuitive part, which is why this has to be measured rather than
reasoned about:**

| pair | families | lower-bound rate | languages |
|---|---|---|---|
| BLUE ~ GREEN | 46 / 88 | 0.52 | 195 |
| ROAD ~ PATH | 43 / 91 | 0.47 | 133 |
| LEG ~ FOOT | 52 / 123 | 0.42 | 349 |
| WOMAN ~ WIFE | 44 / 112 | 0.39 | 289 |
| **HAND ~ ARM** | 48 / 134 | **0.36** | 294 |
| FINGER ~ TOE | 29 / 81 | 0.36 | 133 |
| SEE ~ LOOK | 30 / 84 | 0.36 | 121 |
| GO ~ WALK | 39 / 113 | 0.35 | 288 |
| SKIN ~ BARK | 49 / 145 | 0.34 | 209 |
| WATER ~ RIVER | 38 / 119 | 0.32 | 197 |
| MAN ~ HUSBAND | 34 / 109 | 0.31 | 185 |
| SLEEP ~ LIE DOWN | 40 / 130 | 0.31 | 191 |
| SAY ~ SPEAK | 31 / 120 | 0.26 | 196 |
| EAT ~ DRINK | 26 / 151 | 0.17 | 125 |

**The textbook examples are the weak cases.** ARM/HAND — the canonical illustration of
"languages carve the body differently" — is a *minority* pattern at ≤0.36 even as a lower
bound, and BLUE/GREEN is near a coin flip at 0.52. Meanwhile the strongest merge signals in
the data are places nobody flags: in-law kinship terms collapsing the ego's-sex distinction
(0.87–0.88), the sex-of-a-person vs sex-of-an-animal distinction (0.76–0.82), MOON/MONTH
(0.75), MEAT/FLESH (0.70), TREE/WOOD (0.66).

**This is the finding that justifies running the instrument at all.** Intuition about which
English distinctions are parochial is *anti-correlated* with the data on the famous cases.
A designer relying on the standard examples would merge arm/hand — a split most families
make — and keep moon/month — a split most families don't.

Reading these against §2's tier system: MOON/MONTH, TREE/WOOD and MEAT/FLESH should be one
root each, with the secondary sense reached by compounding if it is ever ambiguous
(*moon-count* for "month"). The in-law and animal-sex distinctions should simply not exist,
which is consistent with Q8's rejection of pronominal gender.

**One case we were asked about and cannot answer.** The **KNOW-a-fact / KNOW-a-person**
split (Romance *savoir/connaître*, German *wissen/kennen*) is **not testable in CLICS3**:
`KNOW (SOMEBODY)` is attested in only **5 families** **[measured]**, and there is no edge
between the two, which reflects absence of data rather than absence of colexification. Same
for THINK~BELIEVE (no edge) and SMELL~NOSE (no edge, and SMELL is in 16 families).
**Concepts thin in CLICS get no verdict, and "no edge" must never be read as "the world
splits these."** That is the single most likely way to misuse this dataset.

### 4.4 CLICS's limitations, quantified

**These are serious and the note should not soft-pedal them.**

1. **The sample is dominated by New Guinea, and family-counting makes it worse, not
   better.** **[verified from the CLICS3 dataset table]** the `transnewguineaorg` dataset
   alone contributes **1,004 of 3,156 varieties (31.8%)** and **106 of the 200 families**.
   Adding `zgraggenmadang` (98 varieties) puts Papuan sources near 35% of varieties. The
   `-f families` weighting is designed to control *genealogical* bias and it does — but it
   has no defence against *areal* bias, and by upweighting small families it actively
   amplifies the region with the most of them. **A "56 of 76 families" figure may be
   substantially a New Guinea figure.** Any threshold decision taken on family counts should
   be re-checked with New Guinea sources excluded; that is a concrete, runnable robustness
   test and it should be part of the script, not an afterthought.
2. **Areal concentration elsewhere too.** Sino-Tibetan and mainland-SE-Asian sources total
   ~248 varieties across 13 datasets; Australian (`bowernpny`) 175; island SE Asia
   (`lexirumah`) 357; Solomons 111 **[verified]**. The genuinely broad-coverage members —
   IDS (60 families), DiACL (25), WOLD (24), NorthEuraLex (21) — are a minority of the
   varieties.
3. **Coverage is unequal across concepts**, badly. `FamilyFrequency` runs from 0 (e.g.
   BELIEF (RELIGIOUS), EVENING STAR) through 5 (KNOW-somebody) to a maximum of 200 (WATER;
   then HEAD 196, TOOTH 195) **[measured]**. Rates computed on thin concepts are
   noise. **Impose a minimum, e.g. both concepts in ≥25 families, and report the n every
   time** — `grammar-plan.md` standing rule 1, which applies here unchanged.
4. **The denominator in §4.2 step 2 is a lower bound**, as noted. Fixable with the SQLite
   database.
5. **Colexification is not synonymy.** An edge can mean genuine polysemy, historical
   accident, or a transcription/elicitation artifact where one gloss was reused. CLICS's own
   ≥3-family threshold filters the worst of it. It does not distinguish "these are one
   concept" from "these are two concepts that share a word."
6. **Colexification measures where boundaries *can* fall, not where they *should*.** A high
   rate is evidence a merge is *learnable and natural*, not that it is *communicatively
   sufficient*. TREE~WOOD at 0.66 does not mean a language is better without a way to say
   "wood"; it means one root plus compounding will not feel alien. **The tier system is what
   converts a colexification finding into a design decision** — merge the roots, keep the
   distinction expressible as a compound. That is the whole point of having tiers.
7. **CLICS cannot see the distinctions no language in it makes**, nor tell us about concepts
   outside its 2,906 sets. It is a filter on our proposals, not a generator of them.

### 4.5 The one thing colexification cannot fix

Colexification is pairwise. Some of the sharpest Eurocentrism in concept division is
**structural rather than pairwise** — the motion-verb case the task raises is the clean
example: whether a language packages *path* into the verb (Romance *entrer*, *monter*) or
*manner* (Germanic *run in*, *climb up*) is a fact about the whole verb system, not about
any concept pair. **[recall — this is Talmy's verb-framed/satellite-framed typology; I did
not verify it against any source in this session, and I did not find a database coding it.]**
WALS and Grambank were built for morphosyntax and I did not check whether either codes it.

Our grammar has already made a partial choice without noticing: with no derivational
affixes, no serial verbs, and modifiers preceding their head, a manner verb plus a
directional modifier is the only available construction — which is satellite-framing, the
Germanic pattern. **This is an unexamined Eurocentric commitment sitting in the grammar
already, and it should go in the final bias audit alongside the classifier and politeness
rejections.** It is also a reason to look hard at the motion domain when the verb roots are
chosen: WOLD's Motion field holds 89 concepts, 77 of them well-covered, at a mean root rate
of 0.679 — below the 0.704 average **[measured]**.

---

## 5. Known problems, collected

Per CLAUDE.md, logged rather than tolerated:

1. **Axis C (compositional predictability) has no instrument** (§2.4). Mitigated
   procedurally, not measured. The largest methodological gap in this plan.
2. **ASJP has not been fetched in this container** (§3.1) — not a README defect, since `data/raw/` is gitignored and re-fetchable by design. Nothing currently depends on it. The
   README needs a fix or the data needs fetching.
3. **The frequency axis is a proxy** — concept-list membership stacked, not corpus
   frequency (§3.3). There is no cross-linguistic frequency corpus in this project and I did
   not look for one.
4. **WOLD analyzability conflates compounding with derivation** (§2.3 caveat 3), and we have
   no derivation, so the instrument systematically *over*-estimates how many concepts a
   compound will serve.
5. **WOLD's coverage bias requires an n≥25 filter** or the root-rate ranking inverts
   (§2.3 caveat 1).
6. **CLICS's family weighting amplifies areal bias toward New Guinea** (§4.4.1) — 106 of 200
   families from one dataset.
7. **The CLICS denominator available from the GML is a lower bound** (§4.4.4).
8. **Thin CLICS concepts give false "the world splits these" readings** (§4.3, KNOW).
9. **The recognizability metric is calibrated on loanword adaptation** (§4 known-issue 5 in
   principles.md) and will be consumed here for recognition. That worry is inherited, not
   new, but the lexicon stage is where it does the most damage — it is the stage where the
   metric actually picks the words.
10. **§3.6's loan-mapping merge table needs re-running at lexicon scale** (fan-in 6 into
    /k/, 5 into /s/, 3 into /f/; zero collisions over 52 words, which proves nothing).
    §3.6 says raise this when the lexicon exists — it now does, in plan form. The reversible
    knob is v→f.
11. **§3.7's segmentation-ambiguity cost is now measurable and should be measured** once a
    root set exists: the real rate at which a solid compound admits more than one parse.
12. **Satellite-framing is already baked into the grammar without having been chosen**
    (§4.5).

---

## 6. Proposed sequence

Session-sized, per CLAUDE.md. Each is one script writing one CSV to `data/processed/`.

| # | Step | Output | Depends on |
|---|---|---|---|
| 1 | **Fetch and stage Concepticon + CLICS3 network**; add both to the README data table | `data/raw/concepticon/`, `data/raw/clics3/` | network |
| 2 | **Analyzability study** — per-concept root rate from WOLD, with the n≥25 policy and field/class aggregates | `lexicon_analyzability.csv` | on-disk only |
| 3 | **Concept inventory v0** — LWT 1460 ∩ (n≥25), Concepticon-keyed, with stacked concept-list membership and WOLD borrowability | `lexicon_inventory.csv` | 1, 2 |
| 4 | **Colexification audit** — every concept pair in the inventory with a CLICS edge, family/language counts, lower-bound rate, plus the **New Guinea-excluded robustness column** | `lexicon_colexification.csv` | 1, 3 |
| 5 | **Tier assignment v0** — apply §2.2, show Patrick the borderline cases rather than the confident ones | `lexicon_tiers.csv` | 2, 3, 4 |
| 6 | **Discouragement weights** — turn §3.3/§3.6's ordinal rankings into numbers, frequency-weighted per §2.6 | in `principles.md` §3.3 | 5 |
| 7 | *Then* the form optimizer | — | 6 |

Steps 2 and 4 are the two that produce data worth reacting to, and neither needs a decision
first. **Recommend starting with step 2** — it uses only data already on disk, and its
output is the table that makes the tier conversation concrete.

---

## 6a. Answers to §7's three questions (Patrick, 2026-08-06)

The three open questions below were put to Patrick and all three are answered. Recorded here
because they change the plan rather than merely confirming it; §7 is kept as written so the
questions and answers can be read together.

**1. How many roots? — WRONG QUESTION, and the reframing matters (SOFT).**
There is no target count. **The target is a *complete* lexicon: the negaverse of toki pona —
as simple as possible subject to being as expressive as any natural language.** A
proliferation of roots is acceptable where the concepts genuinely resist compounding.
Spitball scale: **1–2k roots that participate in compounds, plus thousands of one-off loans**
for country names, and for foods, plants and animals local to one part of the globe.

This kills the framing in §1 that treated the ~180 monosyllables as the binding constraint.
At 1–2k roots **most roots are polysyllabic by necessity**, the short-word budget is a
*ranking* problem (which concepts earn the short forms) rather than a *feasibility* one, and
§2.6's discouragement weights matter more, not less, because they will be applied thousands
of times. **The frequency axis (B) is therefore more load-bearing than §2.2 assumed** — it is
what allocates the short forms — and its "proxy only, weak" status is now the plan's second
methodological gap alongside axis C.

**Loanwords are a third regime the plan did not model.** One-off loans for endonyms and local
biota are neither roots-to-be-compounded nor descriptions: they are borrowed whole, adapted
by §3.6's mapping, and never enter the compounding system. They should be scoped out of the
axis A/B/C/D scoring entirely and handled by the transliteration pipeline
(`src/interlang/translit.py`) plus the deferred homophony check. **Endonyms are preferred**
(Patrick) — *Deutschland*, not *Germany* — which is also a representation decision under §2
of [`principles.md`](principles.md) and should be reported in the bias audit as one.

**2. Does CLICS override intuition, given New Guinea? — YES, but population-weight it (SOFT).**
**The project weights by *people*, not by families** ([`principles.md`](principles.md) §2),
and §4.4's problem is precisely that family-weighting cannot see population. Patrick's
instruction: **if New Guinean languages cannot be weighted properly by population, partially
exclude them.** So the merge rate should be computed **population-weighted where speaker
counts exist**, with the New-Guinea-excluded column promoted from a robustness check to a
**primary output** rather than a footnote.

This is consistent with every other decision in the project — the by-language/by-people
reversal has decided most of the grammar — and it is worth stating that colexification is the
first place where the two weightings were about to diverge silently.

**3. Reduplication — ADOPTED as optional and emphatic (SOFT).** Not declined, contrary to
§2.7's recommendation. The data supports Patrick's reading: **APiCS 26 puts "only iconic
functions" at 4 of 9 restricted pidgins, 5 of 9 expanded and 31 of 54 creoles — 40 of 73**,
cross-lexifier (32 European : 10 non-European, so Rule 1 is satisfied), and Tier 0 found
reduplication **gained 13:2** (verbs 7:0). *Iconic* means plurality, intensity, repetition and
distribution — i.e. emphasis.

- **Nothing depends on it.** Plurality is already handled by the optional plural word and by
  numerals (`three item`), and aspect by Q6's adverbs. Reduplication is **documented as
  available for emphasis and never required** — the same shape as optional number.
- **It is documented because speakers would reinvent it otherwise** (Patrick's reasoning, and
  the 13:2 gain rate is the evidence for it). Documenting an optional device is cheaper than
  having it re-emerge unstandardised.
- **In a compound, the final element reduplicates.** *Not codable* — no source codes partial
  reduplication inside compounds — but it follows from the modifier rule: modifiers precede
  heads, so **the final element of a compound is its head**, and reduplicating the head is
  both semantically apt and keeps initial stress (§3.5) on the original first syllable.
  `firetruck` → `firetrucktruck`.
- **Cost to watch:** reduplication interacts with §3.7's solid compounds and with the geminate
  boundary signal. A reduplicated final element creates a seam that looks like a compound
  seam. Logged in §5.

---

## 7. Open questions for Patrick

Ordered by how much depends on the answer.

1. **Is the "when in doubt, promote to root" asymmetry (§2.2) the right default?** It is the
   single most consequential parameter in the plan — it sets the size of the lexicon. The
   argument for it is that a misleading compound is worse than an arbitrary root. The
   argument against is that it inflates rote-learning cost, which is objective 1. There is a
   *number* behind this and I have not proposed one: **how many roots is interlang aiming
   at?** Ogden 850, toki pona ~120, Esperanto's core several thousand. Everything downstream
   changes with the answer, including whether ~180 monosyllables is comfortable or tight.
2. **Do we accept CLICS as authoritative enough to override our intuitions, given §4.4's
   New Guinea problem?** §4.3 shows the instrument disagreeing with the standard examples.
   That is either its main value or a reason to distrust it. My recommendation is to use it
   as a **flagging** tool at the 0.35–0.60 band and an **overriding** tool only above 0.60
   *and* only when the New Guinea-excluded robustness column agrees — but that is a judgment
   about how much to trust a biased sample, and it is Patrick's to make.
3. **Reduplication: confirm the rejection (§2.7)?** It is the last OPEN item from §3.2's
   morphology decision and it is the only thing that could restore a middle tier between
   root and compound. I recommend declining it and I have given three reasons, but the
   creole evidence is Rule-1 strong (13:2, verbs 7:0) and this would be the fifth
   consecutive departure from the contact record — a pattern §3.2 already says belongs in
   the bias audit.

*Smaller, and answerable later:* whether to take the 90 MB CLICS SQLite for exact
denominators (§4.2); whether "they" and the plural word are one form (§7, inherited);
whether the Longman Defining Vocabulary is worth chasing (§3.2) — it is the only resource I
could not obtain that would materially improve tier 3.

---

## Glossary additions

For [`principles.md`](principles.md)'s glossary, per CLAUDE.md's jargon rule. *Colexification*
is already there.

- **Analyzability** — whether a word can be broken into meaningful parts. WOLD codes it per
  word as unanalyzable (*dog*), derived (*singer*), compound (*doghouse*) or phrasal
  (*day after tomorrow*).
- **Concept set / Concepticon ID** — a stable identifier for a *meaning*, so that
  "the tooth" in WOLD and "TOOTH" in a Swadesh list are known to be the same thing.
  The lexicon stage's join key, as Glottocode is for languages.
- **Defining vocabulary** — a word list large enough that every other word in the language
  can be defined using only it (Ogden's Basic English, the Longman Defining Vocabulary).
- **Lexicalization** — whether a language has a single word for a concept at all, as
  opposed to expressing it with a phrase.
- **Semantic prime** — in Natural Semantic Metalanguage, a meaning claimed to be universal
  and indefinable, so that all other meanings can be paraphrased into primes.
- **Verb-framed / satellite-framed** — whether the direction of motion is carried by the
  verb itself (*enter*) or by a separate element (*go in*). A whole-system property, not a
  per-word one.
