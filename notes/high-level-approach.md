# High-level approach: current state & open discussion

*Written 2026-08-03 to carry context across a conversation restart. This is a
working discussion doc, not a decisions record — the authoritative decisions
live in [`principles.md`](principles.md) with FIRM/SOFT/OPEN tags. When
something here hardens, move it there.*

## Where the project is (one paragraph)

Phonology-before-vocabulary, vocab-aware. The recognizability metric exists at
v0 (panphon weighted feature edit distance + listener conditioning, AUC 0.923 on
WOLD). Two data studies are done (phoneme prevalence, contrast costs) and have
settled a soft inventory: core **m n p t k s j w r h** + **f** + priced add-ons
(fortis/lenis second stop series, l, one wide CH sibilant), vowels **a i u +
wide E + wide O**. The immediate work is **metric calibration** — learning
substitution + epenthesis costs from WOLD (spec:
[`cost-learning-spec.md`](cost-learning-spec.md)) — which is a prerequisite for
the next experiment (projection distortion across syllable templates, §3.6/§7.4)
because the metric's missing epenthesis model flatters permissive codas.

## The high-level discussion in progress (goals framework)

We were re-examining the project's goals from first principles. The framing that
emerged and that I'd propose adding to `principles.md`:

**Three learner-facing abilities the language should be easy for:**

1. **Production** — can a speaker physically make the sounds?
2. **Distinction** — can a listener hear and tell the sounds/words apart?
3. **Recognition** — can a listener recognize a word as one they already know
   from another language?

**How the project's instruments currently map onto these:**

- **Recognition** → the recognizability metric measures this directly (and is
  validated for it via WOLD).
- **Distinction** → handled in *two* places: (a) inside the metric, by the
  listener-conditioning step (distinctions you lack natively cost nothing —
  /l/~/ɾ/ free for Japanese-like listeners); (b) *between our own words*, priced
  by the contrast study as functional-load penalties on minimal pairs
  (`contrast_costs.csv`). Note the same projection machinery in `metric.py`
  *could* compute intra-lexicon confusability per listener — we haven't used it
  that way yet.
- **Production** → **no direct metric.** Served only by proxy: the prevalence
  study ("share of humanity who natively *have* the segment" as a stand-in for
  "can produce it"), the wide-phonemes principle (§3.4 — any realization in the
  set is acceptable, so speakers use what their native system provides), and the
  syllable-template question (permissive codas export unproducible clusters).

**Honest weakness in that mapping:** our data (PHOIBLE "has it natively") is used
as a proxy for *both* "can produce" and "can hear," and can't fully separate the
three goals. Perception often outruns production; production failures surface as
*repairs* (epenthesis) rather than silence — which is why the metric's
epenthesis gap is simultaneously a recognition bug and the place where
production constraints leak into scoring.

## Candidate additional goals raised (not yet decided — OPEN)

1. **Lexicon distinctiveness / word-space capacity.** A small inventory + tight
   phonotactics shrinks the possible-word space, forcing long words or dense
   near-homophones. Currently only implicit (the "word-length blowup" worry, the
   reserved short-particle space for grammar). It trades *directly against*
   production/distinction ease — every phoneme or template restriction bought
   for safety costs word space. Argument for making it an explicit loss term so
   the tradeoff is measured, not felt. Will bind hard at the vocabulary stage.
2. **Memorability of unrecognized words.** Expectation-setting says absolute
   recognizability is low for most people, so most learners are *memorizing*,
   not recognizing, most words. For them ease = short words, regular derivation,
   transparent compounding. Derivation regularity is parked under grammar
   (§3.2), but "easy to memorize even when unfamiliar" is a distinct goal that
   recognition scores don't capture at all.
3. *Already covered, noted for completeness:* **fairness/representation** (not a
   fourth ability — a distribution requirement over recognition; the second term
   of the two-objective loss) and **orthography ease** (§3.7).

## Suggested next move on the high-level thread

Decide whether to adopt the production/distinction/recognition triad as the
organizing frame for `principles.md` §3 (each existing decision and each
instrument slots under one or two goals), and whether to promote goals (1) and
(2) above to explicit, eventually-measured objectives. Then return to the
standing OPEN decisions in `principles.md` §7 — in particular the **second stop
series** (93–96% of people vs ~61% of languages; a decision-ready call under the
declared weighting) and the **representation-term formulation** (string
similarity vs etymology-attribution share).

## Restart note

The prior conversation had some incidental content that tripped an unrelated
safeguard; this doc deliberately carries only the substantive project state so
the discussion can resume clean. Nothing above depends on that content.
