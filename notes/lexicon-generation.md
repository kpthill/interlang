# Full lexicon generation: the pipeline

*Written 2026-08-06. The methodology is in [`lexicon-plan.md`](lexicon-plan.md); this is the
**execution plan** — what runs, in what order, against what objective, and what has to be
true before each stage can start. Milestone 1 ([`lexicon-milestone1.md`](lexicon-milestone1.md))
was the 137-word sanity check that produced most of the corrections below.*

**The target, in Patrick's words (2026-08-06):** *the negaverse of toki pona — as simple as we
can make it subject to being as expressive as any natural language.* There is **no target root
count**. Expect ~1–2k roots that participate in compounding, plus thousands of one-off loans
(country names, local biota, technical terms) that never do.

---

## 1. What milestone 1 changed about the plan

Four things the 137-word run taught us, all of which alter the pipeline below:

1. **The ~180 monosyllables are not the binding constraint.** At 1–2k roots most roots are
   polysyllabic by necessity. The short-word budget is a **ranking problem** — which concepts
   earn the short forms — not a feasibility one. `lexicon-plan.md` §1 over-weighted it.
2. **Loanwords are a third regime the plan never modelled.** They are borrowed whole, adapted
   by §3.6, never enter the compounding system, and — because transliteration makes them
   polysyllabic — **they do not compete for the monosyllable budget at all.** They should be
   scored on recognition alone and scoped out of the root/compound/description logic.
3. **The objective was missing a false-friend term.** Five collisions appeared in the first
   137 words, three of them against concepts *we also have* (`bu` "this" vs Mandarin *bù*
   "not"; `si` "they" vs Spanish *sí* "yes"; `da` "hit" vs Russian *da* "yes").
4. **The donor pool was the instrument, not a choice.** WOLD's 41 languages exclude Spanish,
   Hindi, Arabic, Russian, Bengali, Portuguese, Korean and Turkish — so those could not donate
   and the false-friend term would have been blind to exactly the languages that matter. Hence
   the wider donor pool in §3 below.

---

## 2. The stages

### Stage 0 — Concept inventory

**Tier A — the core, ~1,460 concepts.** WOLD's `Core_list` (the LWT 1460), already on disk and
already carrying `Concepticon_ID`. This is the only tier with **cross-linguistic
lexicalization data attached** (WOLD `Analyzability`), so it is where the tier logic in
Stage 1 can actually be measured rather than argued.

**Tier B — the extension.** Concepticon's wider concept sets (4,165) and IDS (1,310 concepts,
319 varieties) fill out everyday vocabulary the LWT list omits. No `Analyzability`, so Stage 1
runs on weaker evidence here — say so per concept rather than pretending uniform support.

**Tier C — open-ended.** Proper names, biota, technical and modern vocabulary. **Not scored by
the tier logic at all**; routed straight to the loanword regime (Stage 3b). Endonyms preferred
(Patrick, 2026-08-06).

### Stage 1 — Root, compound, or description

The criterion from `lexicon-plan.md` §2.2, unchanged, including its asymmetry: **when in
doubt, promote to root**, because a needless root costs one memorised item while a
non-inferable compound costs a memorised item *plus* an actively misleading form.

| axis | what it measures | instrument | status |
|---|---|---|---|
| **A. cross-linguistic lexicalization** | do languages give this a simple word, or build it? | **WOLD `Analyzability`** — 64,289 forms, 41 languages, 1,814 concepts | **works** |
| **B. frequency** | how often is it needed? | concept-list membership across Concepticon's 480 lists, stacked | **weak — see §4** |
| **C. compositional predictability** | would a learner derive the compound, and recover the meaning? | none | **procedural only** |
| **D. boundary risk** | does our carving match how languages divide this meaning? | **CLICS** colexification | works, with caveats |

**Axis B matters more than `lexicon-plan.md` assumed**, because with polysyllabic roots
acceptable, frequency is what allocates the *short* forms rather than what decides root-vs-
compound. It is currently the weakest instrument in the pipeline.

### Stage 2 — Where the word boundaries fall (CLICS)

**Population-weighted, not family-weighted** (Patrick, 2026-08-06) — this project weights by
people everywhere else, and family-weighting was about to diverge silently. The
**New-Guinea-excluded column is promoted from robustness check to primary output**, because
one dataset supplies 106 of CLICS's 200 families and would otherwise dominate.

The instructive result from `lexicon-plan.md` §4.3, worth restating because it is the case for
measuring this at all: **intuition is anti-correlated with the data on the famous examples.**
ARM~HAND is only 0.36 and BLUE~GREEN 0.52 — both minority merges — while MOON~MONTH 0.75,
MEAT~FLESH 0.70 and TREE~WOOD 0.66 are the strong ones nobody flags.

### Stage 3a — Form assignment for roots (the optimizer)

**Hard constraints** (violations are rejected, not penalised):

- phonotactics: (C)V(N) with N ∈ {n, m}, plus the ten Cr/Cl onsets (§3.6 FIRM)
- no two words differing only by `l~r` or only by `h~r` (§3.3 FIRM)
- **monosyllable budget**: leave one-third to one-half of the ~174 usable monosyllables
  unassigned (Patrick, 2026-08-06), for the parseability reason in Stage 5

**Objective terms**, in descending weight:

| term | what it does | state |
|---|---|---|
| **recognizability** | population-weighted similarity to attested forms, over the widened donor panel | instrument being rebuilt (§3) |
| **representation** | donor spread — **per root, not per word**, and realistically **by family**, not by language | works |
| **phonotactic cost** | discouraged segments /r h/ > /l/ > /b d ɡ/, plus a cluster penalty | **ordinal — must become numeric before this runs** (§7 OPEN) |
| **distinguishability** | maximise minimum *perceptual* distance (feature metric), not Hamming | revised spec, §4 |
| **parseability** | do not assign a polysyllabic form that already parses as a compound of existing roots | new, §5 |
| **false friends** | penalise forms that strongly evoke a *different* meaning in a high-population language | new — **deliberately weak weight**, "some of this is inevitable" (Patrick) |
| **consistency** | once a root has a donor, its compounds inherit it | trivial to implement, see §6 |

**Ordering matters and is not arbitrary:**

1. **Internationalisms first.** They are forced by the recognition thresholds and cannot take
   monosyllables anyway, so they constrain nothing downstream.
2. **Then the high-frequency block** — grammatical words, numerals, pronouns, the generic
   nouns, early Swadesh — which competes for the monosyllables.
3. **Then everything else**, into the polysyllabic space.

### Stage 3b — The loanword regime

A concept enters here if its international form clears the recognition thresholds:
**>50% of humanity ⇒ MUST adopt; >30% ⇒ SHOULD adopt** (Patrick). Adoption is by §3.6's
transliteration rules, with no tier scoring and no compounding role.

**With one correction milestone 1 forced:** transliterate **unless the result is so mangled it
is no longer recognisable**, in which case fall back to a compound of native roots. The rule
is *not* "compound the technical vocabulary" — `gramatika`, `fonema`, `silaba`, `data`,
`metodo` do exactly the job of letting technical communities pick the language up with little
learning, which is a stated dual objective. But `kiwesitione` scored **0.065** and
`sitatisitika` **0.313**: at that point the borrowing has stopped buying recognition and is
only buying length.

**Rejected option, recorded so it is not re-proposed:** extending the onset inventory to allow
`sC` clusters for loanwords. Measured — it improved only **5 of 18** problem words and saved
**6.8%** of syllables, because the real damage is word-*internal* clusters (/kt/ in
*dictionario*, *adjectivo*, *traductione*; /ks/ from *x* in *syntaxis*) that no onset rule can
reach. And WALS 12A puts **57.4% of world L1** in languages with simple or only
moderately-complex syllable structure, so `st-` is genuinely hard for a majority. It would
also be a *conditional* rule — "borrowed words may begin `st`, native words may not" — and
this grammar has rejected conditionals everywhere else.

### Stage 4 — Compound construction

For every tier-2 concept, choose the decomposition.

**Patrick's criterion (2026-08-06), and it overrides representativeness:** *make sure the
compounds make sense in a culture-agnostic way.* **`eye-water` for "tear" is excellent;
`thor-day` for Thursday is terrible** — it is tied to one culture's understanding, and should
be `four-day` or the like. Where languages agree on a decomposition, copy it; where every
family does its own thing, we are free, and **guessability wins over spreading the choices**.

**The instrument gap, named:** WOLD's `Analyzability` tells us *whether* a concept is
decomposed, not *into what*. If morpheme glosses are unavailable, the approved fallback is to
**examine ten large languages per concept and pick a popular or logical breakdown** — not
exhaustive, and flagged as such.

### Stage 5 — Validation

- **Segmentation ambiguity rate.** The measurable version of "don't fill the monosyllable
  space": for the candidate lexicon, what fraction of compounds admit more than one parse?
  This is the deferred question from §7's solid-compound entry, and it is what actually sets
  the budget. **Note syllabification itself is unambiguous** — `banti` can only be `ban.ti`
  since `nt` is not a legal onset — so the problem is purely morpheme boundaries.
- **Homophony after loan-mapping.** §3.6's merge table folds 6 spellings into /k/, 5 into /s/,
  3 into /f/. Zero collisions over 52 words proves nothing at lexicon scale; this is the
  §7 item explicitly deferred to here.
- **A negative control on the recognition metric.** There is none yet. Score random unrelated
  pairs and confirm the distribution separates from true cognates.
- **Round-trip test on compounds** — can a naive reader recover the meaning from the parts,
  and the parts from the meaning? This is axis C, and it is procedural by necessity.

### Stage 6 — The lexicon bias audit

Same shape as [`grammar-bias-audit.md`](grammar-bias-audit.md), which is the model: report
**root-share and word-share separately**, by family and macroarea, and state the skew plainly.
Root-share is the honest number for §2's fairness objective; word-share will be dominated by
whichever roots turn out to be productive.

**Known in advance:** the technical vocabulary is ~100% Latin-derived and **this is accepted**
(Patrick) — it serves the dual objective of letting technical communities transfer directly.
But it means a whole-list donor share is a very different number from the core-root share, and
both must be published.

---

## 3. Widening the donor pool — CLDF datasets, not a scrape

**A Wiktionary scrape was proposed, started and abandoned within minutes** (Patrick,
2026-08-06: *"please don't do a full scrape of wiktionary or anywhere else"*). Nothing was
fetched. The proposal rested on a **false premise worth recording**: HTTPS browsing returns
403 through the agent proxy, from which it was inferred that the CLDF research datasets were
unreachable. **They are not — `git clone` works**, which is exactly how `data/raw/` was
already populated with WALS, Grambank, APiCS, PHOIBLE and WOLD. Checking `git ls-remote`
before proposing a scrape would have avoided the whole detour. *Third instance in this
project of concluding "unavailable" without checking the specific access path — see
[`grammar-tier3-cleanup.md`](grammar-tier3-cleanup.md) §6.*

**The CLDF route is better on every axis**, which is what makes the error costly rather than
merely embarrassing:

| | Wiktionary scrape | CLDF datasets |
|---|---|---|
| sense disambiguation | the `{{trans-top}}` sense-mixing trap (below) | **curated: one form per concept** |
| concept identity | string matching on page titles | **Concepticon IDs** |
| transcription | orthography, mixed scripts | **phonetic** — what the metric consumes |
| provenance | crowd-sourced, uneven | **published, citable, versioned** |
| fetch | thousands of API calls | **one `git clone`** |

**Proposed sources**, all fetched the same way as the existing five:

| source | size | what it adds |
|---|---|---|
| **ASJP** (`lexibank/asjp`) | small | 100 core concepts × ~11,540 doculects — essentially every language, phonetically transcribed. **Already in the README fetch table, simply not fetched in this container.** |
| **IDS** (`intercontinental-dictionary-series/ids`) | 72 MB | **319 varieties, 1,310 concepts, 437,902 forms**, Concepticon-linked **[measured — test-clone]**. Adds Spanish, Russian, Portuguese, French, German, Persian, Vietnamese as donors |
| **Concepticon** | small | the catalogue that joins all of the above |
| **CLICS³** | ~12 MB | colexification, for Stage 2 |

**Coverage after WOLD + IDS**, measured on the test clone: the seven languages above become
available; **Hindi, Arabic, Bengali, Korean and Turkish remain missing** and are what ASJP is
for. That matters most for the false-friend term, which can only see languages we hold forms
for.

**The Wiktionary trap, recorded because it is a real hazard for anyone who tries this later:**
translations are grouped by sense inside `{{trans-top|gloss}}` blocks, so a naive regex mixes
senses and silently returns the wrong word. Verified **[measured]**: `water` yields Spanish
*regar* and Russian *поливать* ("to irrigate"), and `fire` yields Spanish *cocer* and Korean
*해고하다* ("to dismiss from a job"). `three` and `tooth` look correct only because they have
one dominant sense.

---

## 4. Instruments that are still too weak, honestly

1. **The recognition metric is calibrated on loanword *adaptation*, not *recognition*.**
   This is §7's open question 6 and it is the deepest problem in the pipeline: every
   "X% of humanity would recognise this" number rests on it. Patrick's working approximation —
   *a word recently borrowed into language A from source S, re-adopted by us from S under our
   rules, will be recognisable to speakers of A* — is explicitly acknowledged as false in
   general and adopted as tractable. **The thresholds should be read as a ranking with a cut
   point, not a measurement**, until there is a negative control.
2. **The discouragement weights are still ordinal.** They must become numbers before Stage 3a,
   and they will now be applied thousands of times rather than dozens.
3. **Frequency (axis B) has only a proxy**, and Stage 3a's ordering depends on it.
4. **Compound decomposition has no corpus instrument** (§Stage 4).
5. **The false-friend term can only see languages we hold forms for** — which is precisely why
   Wiktionary comes before full generation, not after.

## 5. Sequencing

| | milestone | blocks on |
|---|---|---|
| ✅ | **M1** — 137-word sanity check | done; regenerating with the four fixes |
| ▶ | **M2** — Wiktionary corpus | running |
| | **M3** — shape-budget study: segmentation ambiguity vs monosyllable utilisation, **including two-syllable roots** | nothing — can run now |
| | **M4** — numeric discouragement weights | M3 |
| | **M5** — tier assignment over LWT 1460, ranked output shown for reaction before building on it | M2 |
| | **M6** — form assignment for the root inventory | M2, M3, M4 |
| | **M7** — compound construction | M5, M6 |
| | **M8** — validation and lexicon bias audit | M7 |

**M3 is the one that can start immediately and gates the most**: it converts "leave a third to
a half of the monosyllables free" from an instinct Patrick flagged as unjustified into a curve
with a defensible point on it.
