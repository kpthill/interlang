# Working on interlang

Read [`README.md`](README.md) for what the project is and how to run things, and
[`notes/principles.md`](notes/principles.md) for the goal, the two-objective loss, and
every decision made so far. `notes/` is the source of truth for decisions; this file is
about *how* to work here.

## How Patrick wants to collaborate

- **Drive investigation phases in chat**, in prose — not through question menus.
  Part of the process is Patrick working out what he's actually looking for, so
  discuss design decisions openly, give a recommendation, and ask questions inline.
- **Small, session-sized milestones**, not big ones. Propose the next step, get
  agreement, do it, show the result.
- **Show intermediate data and results for reaction** before building on top of them.
  Don't run ahead of the agreed scope.

## Conventions

- **Every decision gets tagged** in `notes/principles.md`: **FIRM** (committed, revisit
  only with strong new evidence), **SOFT** (working position, expected to survive,
  pending data), **OPEN** (genuinely undecided, experiment or discussion planned).
  Moving a decision between tags is itself worth writing down.
- **Judgment calls get documented where they're made.** Each script's module docstring
  states its inputs, outputs, and the policies baked into it (inventory selection,
  fallbacks, exclusions); the matching write-up in `notes/` interprets the results.
  If you make a new judgment call, write it in both places, not just in code.
- **Known problems get logged, not silently tolerated.** The metric's characterized
  failure modes (place-of-articulation weights, no epenthesis, ~0.46 random floor)
  live in `notes/data-audit.md` with concrete fix paths, and callers are warned where
  a failure mode biases a conclusion (e.g. epenthesis flatters permissive codas).
- **Jargon gets defined for a non-linguist reader.** `notes/principles.md` carries a
  glossary and explains terms at first use; keep that up.
- **Raw data is disposable, constructed data is not.** `data/raw/` is gitignored and
  re-fetchable (sources in the README); anything a script builds goes in
  `data/processed/` and is committed.
- **One study per script**, reading from `data/raw` + `data/processed` and writing a
  CSV back to `data/processed`. Reusable logic goes in `src/interlang/`.

## Where things stand

Phonology is being decided before vocabulary, but vocabulary-aware. **Phonology and
phonotactics are now closed** (`notes/principles.md` §3.3–§3.7): inventory, stress,
orthography, syllable template ((C)V(N) + Cr/Cl onsets), compounding and hiatus are all
FIRM. What remains before grammar is lexicon-facing, not phonology-facing — the
discouragement weights have to become numbers, and root-shape bounds wait on grammar.
Open questions are listed in `notes/principles.md` §7.
