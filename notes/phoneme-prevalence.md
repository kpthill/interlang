# Phoneme prevalence study (2026-07-14)

> **Rev 2 (same day):** numbers regenerated after zeroing the phantom
> "Standard Arabic" L1 figure (335M was the macro-Arabic total; MSA has ~no
> native speakers — see `contrast-study.md` Addendum and `L1_OVERRIDES` in
> `scripts/fetch_l1_speakers.py`). Biggest movers: /p/ 91.8→96.8, /e/
> 69.6→73.4, /o/ 67.1→70.8, /tʃ/ 53.2→56.1 L1-weighted; pharyngeals and θ
> dropped. MSA keeps its CLDR *total*-speaker weight (ease term), which is
> why /p/ now shows L1 96.8 > total 94.5.

*Which sounds do the world's speakers actually have?* Resolves inputs for
[`principles.md`](principles.md) §3.3 (inventory), §3.4 (wide phonemes), §3.7
(orthography). Reproduce with:

```
uv run python scripts/fetch_l1_speakers.py    # Wikidata L1 counts + ISO 639-3 table
uv run python scripts/phoneme_prevalence.py   # -> data/processed/phoneme_prevalence.csv
```

## Method (brief)

Universe: the 2,177 PHOIBLE languages. For every segment, three prevalence
measures:

- **% L1-weighted** — share of native speakers whose native language has the
  segment. L1 counts: Wikidata P1098 ("number of speakers"), which is
  overwhelmingly Ethnologue-derived; 1,858 individual languages
  (`data/processed/l1_speakers.csv`, fetched by `scripts/fetch_l1_speakers.py`).
- **% total-weighted** — share of *speaker-language pairs* weighted by CLDR
  total-speaker counts (L1+L2), approximating "share of people who have the
  sound in ANY language they speak". A person counts once per language they
  speak, so multilinguals are overcounted (see Judgment calls).
- **% of languages** — unweighted; each PHOIBLE language counts once.

Denominators are the PHOIBLE-covered totals: 860 of 2,177 PHOIBLE languages
joined to an L1 figure, but those carry **6.15B L1 speakers = 89.7%** of the
L1 source's world total (the unjoined 1,317 are small languages, defaulted to
10,000 L1 each; 415 languages joined to a CLDR total, the rest fall back to
total := L1 per principles §3.8). So read the percentages as "share of speakers
of PHOIBLE-covered languages", which is ≈ share of the world.

Symbols are counted at two granularities, both in the output CSV:
**strict** (PHOIBLE symbol as-is, /t̪/ ≠ /t/) and **lumped** (perceptually
negligible diacritic variation collapsed — exact rules under Judgment calls).
The tables below use the lumped level. A third level, **class**, reports
"wide phoneme" unions (§3.4).

## Top 50 sounds (lumped, ranked by L1-weighted share)

Allophones column: most frequent realizations listed for the segment across
PHOIBLE's `Allophones` field (number of languages in parentheses); notation-only
variants of the segment itself are folded away.

| # | Phoneme | Common allophones (n languages) | % L1-weighted | % total-weighted | % of languages |
|---|---------|--------------------------------|---------------|------------------|----------------|
| 1 | m | mʷ (30) m̥ (27) mʲ (25) ɱ (25) ŋ (21) | 99.9 | 99.9 | 97.0 |
| 2 | k | kʰ (266) ɡ (109) kʲ (56) kʷ (55) ɣ (30) | 99.8 | 99.9 | 95.6 |
| 3 | i | ɪ (138) ĩ (81) i̥ (41) e (32) ɨ (30) | 99.2 | 99.3 | 97.2 |
| 4 | t | tʰ (280) d (88) tʲ (42) tʷ (19) ts (16) | 99.1 | 99.4 | 93.9 |
| 5 | n | ŋ (131) ɲ (64) m (36) nʲ (34) n̥ (29) | 99.0 | 99.4 | 94.6 |
| 6 | a | ɑ (147) ã (82) ə (55) ɐ (55) æ (45) | 98.9 | 99.2 | 99.0 |
| 7 | s | ʃ (98) z (42) sʲ (26) sʷ (18) ts (11) | 98.5 | 99.1 | 73.5 |
| 8 | p | pʰ (247) b (87) ɸ (31) pʷ (28) pʲ (28) | 96.8 | 94.5 | 89.9 |
| 9 | u | ʊ (88) ũ (72) u̥ (32) o (31) w (25) | 96.4 | 97.3 | 93.0 |
| 10 | l | r (37) lʲ (30) l̥ (27) ɾ (24) d (24) | 91.5 | 93.8 | 78.8 |
| 11 | j | j̃ (26) j̥ (24) ʝ (18) ɲ (14) i (8) | 89.8 | 93.5 | 91.1 |
| 12 | r | ɾ (319) ɽ (59) ɹ (55) r̥ (36) ɻ (29) | 89.4 | 89.5 | 78.7 |
| 13 | f | v (24) fʷ (23) fʲ (21) ɸ (19) p (6) | 79.4 | 86.3 | 43.8 |
| 14 | b | β (59) p (52) bʷ (38) mb (36) bʲ (31) | 75.7 | 80.0 | 62.9 |
| 15 | d | nd (35) t (31) r (28) dʲ (26) ɾ (26) | 75.1 | 79.8 | 59.9 |
| 16 | w | w̃ (28) β (27) ɥ (23) v (19) ʍ (15) | 74.8 | 80.1 | 86.1 |
| 17 | ɡ | ɣ (71) ɡʷ (37) ɡʲ (34) ŋɡ (31) k (28) | 73.7 | 74.7 | 57.0 |
| 18 | e | ɛ (115) ẽ (68) ɪ (22) ə (19) e̥ (17) | 73.4 | 75.0 | 75.6 |
| 19 | o | ɔ (93) õ (76) u (29) ʊ (20) o̥ (18) | 70.8 | 61.2 | 74.4 |
| 20 | ʃ | ʒ (14) ʃʲ (11) s (8) tʃ (5) ʃʷ (5) | 59.1 | 72.1 | 35.0 |
| 21 | ŋ | ŋʷ (23) ɲ (19) ŋʲ (14) m (13) n (13) | 58.8 | 65.3 | 64.9 |
| 22 | tʃ | tʃʰ (101) dʒ (28) ts (11) tʃʷ (9) ʰtʃ (7) | 56.1 | 63.4 | 42.3 |
| 23 | h | x (32) ɦ (27) hʷ (10) h̃ (8) ç (7) | 55.0 | 62.3 | 57.1 |
| 24 | ɛ | ɛ̃ (48) e (42) æ (20) ɛ̥ (12) ə (9) | 49.7 | 59.4 | 39.5 |
| 25 | z | ʒ (38) dz (14) zʲ (11) dʒ (10) s (10) | 49.2 | 62.6 | 32.8 |
| 26 | ɔ | ɔ̃ (50) o (20) ɔ̥ (9) ɒ (4) ø (3) | 49.1 | 56.7 | 37.7 |
| 27 | ə | ə̃ (17) a (12) ɐ (8) ɨ (8) ə̥ (6) | 48.5 | 58.7 | 24.0 |
| 28 | x | h (16) xʷ (11) ɣ (11) xʲ (10) ç (9) | 39.3 | 36.4 | 18.1 |
| 29 | ts | tsʰ (70) tʃ (44) dz (16) tsʲ (7) s (7) | 34.9 | 28.0 | 26.4 |
| 30 | v | w (16) vʲ (13) vʷ (10) β (10) f (9) | 34.6 | 43.7 | 27.7 |
| 31 | æ | ɛ (8) æ̃ (5) a (3) e (1) æə (1) | 33.3 | 40.0 | 7.4 |
| 32 | ɲ | ŋ (16) n (11) m (8) ɲ̥ (7) j̃ (6) | 32.6 | 28.6 | 44.2 |
| 33 | dʒ | ʒ (14) ndʒ (13) tʃ (10) dʒʷ (9) dʒʲ (6) | 31.9 | 45.7 | 28.1 |
| 34 | ɪ | i (20) ɪ̃ (15) ɪ̥ (7) e (6) ɛ (4) | 27.4 | 38.8 | 15.2 |
| 35 | ʊ | ʊ̃ (14) o (12) u (10) ʊ̥ (8) ɔ (5) | 27.2 | 39.0 | 14.1 |
| 36 | õ | ɔ̃ (5) ũ (2) ʌ̃ (1) ɤ̃ (1) õ̰ (1) | 26.1 | 24.1 | 14.7 |
| 37 | ɖ | ɽ (8) ɖʱ (6) ɖʲ (2) dˀ (1) ɖˀ (1) | 25.7 | 22.9 | 7.6 |
| 38 | ʈ | ʈʰ (32) ɖ (11) ʈʲʰ (2) ɽ (2) ʈˀ (1) | 25.6 | 22.9 | 16.4 |
| 39 | y | yə (2) ʏ (2) y̥ (1) ɔ (1) ø (1) | 25.5 | 24.6 | 5.9 |
| 40 | ẽ | ɛ̃ (4) e (1) ẽi (1) | 23.4 | 20.2 | 13.6 |
| 41 | ʂ | ʂɻ (1) ʐ (1) s (1) ʃ (1) | 22.7 | 20.5 | 6.1 |
| 42 | ʒ | dʒ (11) ʃ (6) ʃ͉ (5) ʒ̥ (5) j (3) | 22.3 | 31.1 | 14.4 |
| 43 | ç | x (2) çʰ (1) s (1) ch (1) h (1) | 21.9 | 20.2 | 4.5 |
| 44 | cç | cçʰ (5) c (4) ɟʝ (3) ʃ (3) ç (1) | 21.7 | 19.7 | 4.4 |
| 45 | ai | ɑi (5) ɐi (3) aɪ (1) ʌi (1) ãĩ (1) | 21.3 | 22.5 | 4.8 |
| 46 | ĩ | ɪ̃ (7) ḭ̃ (1) ĩˤ (1) i (1) ỹ (1) | 21.2 | 19.1 | 19.8 |
| 47 | au | ɑu (4) ɐu (2) ʌʊ (1) oʊ (1) aʊ (1) | 20.9 | 22.0 | 3.9 |
| 48 | ʔ | ʔʲ (4) ʔʰ (3) ʔʷ (2) h (2) ɦ (2) | 20.7 | 20.3 | 37.8 |
| 49 | ũ | ʊ̃ (3) m (1) õ (1) ỹ (1) ũˤ (1) | 20.2 | 18.5 | 18.5 |
| 50 | χ | x (3) χʲ (3) h (2) ʁ (2) q (2) | 19.1 | 16.0 | 6.6 |

Ranks 36-50 are dominated by segments of large South-Asian languages (Indic
breathy/retroflex series, the /ai au/ diphthong analyses) and by nasal vowels
(Indic + Portuguese + French + West Africa) — high population share, low
cross-linguistic share.

### Wide-phoneme classes (unions of lumped segments, §3.4)

| Wide class | Members | % L1-weighted | % total-weighted | % of languages |
|---|---|---|---|---|
| R-class | r ʀ ʁ (r already includes ɾ ɹ ɻ ɽ) | 92.0 | 94.2 | 79.8 |
| L-class | l ɭ ʎ | 91.5 | 93.8 | 79.5 |
| H-class | h x ħ χ | 83.5 | 84.5 | 66.0 |
| W-class | w ʋ | 81.9 | 87.0 | 87.2 |
| F-class | f ɸ | 80.5 | 87.0 | 48.0 |
| CH-class | c tɕ tʂ tʃ | 64.8 | 69.4 | 56.3 |
| SH-class | ɕ ʂ ʃ | 62.3 | 74.2 | 39.6 |

## Judgment calls

1. **L1 source: Wikidata P1098 via SPARQL** (property "number of speakers,
   writers, or signers" on items with an ISO 639-3 code). Chosen over the
   Wikipedia native-speaker tables because it covers **1,858 individual
   languages** (vs ~100-200 in the tables) while having the same ultimate
   provenance (the bulk is the 2019 Ethnologue-22 import), is CC0, and is
   queryable reproducibly. Statement selection: deprecated-rank dropped;
   statements qualified "applies to part = first language" (Q36870) preferred —
   every major lingua franca has one, which is exactly where L1-vs-total
   confusion would distort weights (English 379M L1 vs 1.5B total); otherwise
   *unqualified* statements are used and **assumed L1** (Ethnologue-style
   population figures; for non-lingua-francas L1 ≈ total anyway, cf. §3.8);
   "second language"/"whole"/territory-qualified statements are never used.
   Ties: PreferredRank, then latest point-in-time, then larger value.
   **ISO macrolanguage codes dropped** (zho, ara, msa...) since their members
   (cmn, arb...) are counted individually — keeping both would double-count.
   Sanity check against Ethnologue/Wikipedia top-30 passes (cmn 918M, spa 485M,
   eng 379M, hin 341M, arb 335M...).
2. **Languages missing an L1 figure get a default of 10,000 L1 speakers.**
   1,317 of 2,177 PHOIBLE languages are absent from the L1 source; they are
   overwhelmingly small. The default keeps them in every denominator at a total
   cost of ~13M ≈ 0.2% of the weight mass, so it cannot move any headline
   number, while excluding them would silently change the unweighted universe.
3. **PHOIBLE multi-inventory policy: majority vote.** A segment counts as
   present in a language if it appears in ≥ 50% of that language's inventories
   (75% of languages have just one; English has 9). Union was rejected because
   single aberrant analyses would inflate inventories (one English source lists
   /kx/); intersection was rejected as too fragile to transcription-convention
   disagreements. With ≥ 50%, a 1-of-2 split still counts (union-leaning tie
   break).
4. **Lumping rules (strict vs lumped).** Both levels are in the CSV. The lumped
   level (a) strips diacritics judged perceptually negligible for *recognizing*
   a category: length (ː ˑ ̆), coronal sub-place (dental ̪, apical ̺, laminal ̻),
   fine tongue position (̟ ̠ ̈ ̽ ̝ ̞ — this merges ä→a, e̞→e), syllabicity (̩ ̯),
   release detail (̚), tie bars; (b) strips **aspiration** (ʰ ʱ) — this is a
   *presence* decision, not a claim that the contrast is negligible: 6 of 9
   English inventories and Standard Arabic's only inventory analyze their
   voiceless stops as /kʰ tʰ pʰ/, and without the strip PHOIBLE literally says
   English has no /k/ or /t/ (k drops from 99.8% to 85% L1). The aspiration
   *contrast* remains visible at the strict level (kʰ alone: 61% L1, 17.5% of
   languages); (c) merges coronal rhotics ɾ ɹ ɻ ɽ → r (§3.4 "any rhotic";
   uvular ʀ ʁ deliberately NOT merged because ʁ doubles as a plain fricative,
   e.g. Arabic ghayn — the R-class row adds them back), and low vowels ɑ ɐ → a.
   Kept distinct on purpose: voicing, ejectives, phonation (breathy b̤, creaky),
   nasalization, palatalization/labialization/velarization, retroflexion, and
   vowel quality (ɪ ʊ ɛ ɔ æ ə). Considered and rejected: ɯ → u (would erase
   Turkish ı/u and be wrong for Korean/Vietnamese, which contrast both).
5. **Marginal phonemes:** policy is to exclude them, but this PHOIBLE CLDF
   export contains **no `Marginal = True` rows at all** (84,581 False + 20,878
   blank), so the filter is a documented no-op. If a future re-fetch restores
   the flags, the script already applies the exclusion.
6. **CLDR BCP-47 → ISO 639-3.** Two-letter codes mapped via the SIL
   `iso-639-3.tab` Part1 column (fetched by `fetch_l1_speakers.py`). Script and
   region subtags are stripped and summed (`zh_Hant`+`zh` → zh; **lossy:**
   `pa_Arab` — really Western Punjabi — folds into `pa`/pan). Macrolanguage
   codes are mapped to their dominant individual language (zh→cmn, ar→arb,
   ms→zsm, fa→pes, sw→swh, ku→kmr, az→azj, uz→uzn, lah→pnb, qu→quz, ...
   full list in `scripts/phoneme_prevalence.py: MACRO_MAP`), which attributes
   all of the macro population to one member — acceptable for phoneme presence,
   wrong if members' inventories diverge. Remaining unmapped macros carry < 13M
   speakers combined (raj, luy, kln). PHOIBLE languages missing from CLDR
   (most of them) use total := L1 (principles §3.8).
7. **Population double counting.** (a) The total-weighted column counts a
   person once per language they speak (an Indian speaking Hindi + English +
   Marathi contributes 3 person-language pairs); it therefore *overcounts
   multilinguals* and is a weighting convention, not a person count — the
   denominator (10.3B pairs) absorbs most of the distortion. (b) L1 figures
   sum to 7.2B, slightly above plausibility: mixed census vintages (1999-2024),
   Ethnologue's generous Hindi-vs-regional-language attributions, and a few
   totals hiding in "unqualified" Wikidata statements (e.g. Filipino 90M is
   probably an all-users figure; its PHOIBLE join is nil so the phoneme table
   is unaffected). (c) Hindi/Urdu and Punjabi variants are counted per ISO code
   as distinct, following the source.

## Notable observations

1. **The §3.3 candidate core is confirmed, with two soft spots.** /m k i t n
   a s p u/ are all ≥ 96.4% L1-weighted (/p/ joined the top tier at 96.8%
   after the Arabic fix); /l j r/ are ~89-92%. The soft spots in
   /m n p t k s l w j h + a e i o u/: **/h/ is the weakest consonant (55% L1)**
   — but the wide H-class h~[x~χ~ħ] recovers 83.5%, directly supporting the §3.4
   plan of /h/ with [x] latitude; and **mid vowels /e o/ (~71-73%) are far
   behind /a i u/ (~96-99%)** — Arabic's three-vowel system plus the
   English/Mandarin/Japanese mid-vowel analyses. A 5-vowel system is still
   defensible (75% of *languages* have e and o), but /e o/ carry real cost for
   ~30% of humanity, worth an explicit wide definition ([e]~[ɛ], [o]~[ɔ] —
   which the allophone data supports: ɛ is /e/'s top allophone, ɔ is /o/'s).
2. **L1 vs L2 weighting reorders the middle of the table in English's favor.**
   Sounds English has gain up to +14 points under total weighting: ʃ 59→72,
   v 35→44, z 49→63, dʒ 32→46, ɪ 27→39, ʊ 27→39, ɛ 50→59, ə 49→59, θ 17→29.
   Sounds carried by big non-lingua-francas drop: o 71→61, ʔ 21→20, ts 35→28,
   ɲ 33→29, x 39→36. The ease/L2 objective will therefore pull the inventory
   toward an English/European fricative-rich profile — this is the explicit,
   measured bias the project accepts (§2), but now it has numbers.
3. **Population weighting and language counting disagree spectacularly for
   /s/ and /f/.** /s/ is native for 98.5% of people but present in only 73.5%
   of languages (the sibilant-less languages — much of Australia, parts of
   Papunesia — are numerous but tiny). /f/ is even starker: 43.8% of languages,
   79.4% of people. Conversely /w/ is in 86% of languages but only 75% of
   people (Spanish, Hindi, Russian, Turkish, German lack it; W-class w~ʋ
   recovers 82%). Fairness-by-languages and fairness-by-people are different
   objectives; the loss function should know which it is using.
4. **ʃ / tʃ / ŋ (the §3.7 ASCII casualties) are the best sounds we'd be giving
   up, and the allophone data softens each loss.** They rank 20, 22, 21 —
   clearly above the cut for nothing else in ASCII's reach is better. But:
   [ʃ] is the #1 allophone of /s/ (98 languages) → a wide /s/~[ʃ] is
   empirically normal; ŋ's top-30 gaps (Spanish, Hindi, Arabic, Portuguese,
   Russian...) coincide with languages where [ŋ] exists as an allophone of /n/
   (ŋ is /n/'s #1 allophone, 131 languages) → ŋ-as-allophone (§3.7) is
   confirmed; tʃ at 56% L1 (CH-class 64.8%) is the real casualty, and its top
   allophone is [tʃʰ] — any /tʃ/ should be aspiration-indifferent.
5. **The voiced stop series is a quarter of humanity more expensive than the
   voiceless one.** p/t/k = 97/99/100% L1 vs b/d/ɡ = 76/75/74%. And the
   voiceless numbers are only that high because aspirated-only analyses were
   lumped in — i.e., "voiceless stop" is near-universal only as a *fortis*
   category realized as [k] or [kʰ]. Both facts argue for §3.4's fortis/lenis
   wide contrast (voicing OR aspiration), and put a measured price on having a
   second stop series at all: it costs nothing for ~70-77% of people and is
   unavailable natively to the rest (Mandarin, Wu, Yue, Korean, Tamil...).
6. **Rhotic latitude is huge and quantified.** The lumped /r/ (tap, trill,
   approximant, retroflex) reaches 89% L1 / 79% of languages, and PHOIBLE lists
   [ɾ] as an allophonic realization of it in 319 languages — the single most
   allophone-rich segment in the database. Adding uvular rhotics (French/German
   ʁ ʀ) lifts it to 92.0%. "Any rhotic counts as /r/" (§3.4) is about as safe
   as a design decision gets. Bonus: /l/ at 92% pairs with it, but note the
   r/l *contrast* is exactly what Japanese/Korean lack — prevalence of the
   segments says nothing about the contrast's cost (that's the planned
   contrast study).

## Outputs

- `data/processed/l1_speakers.csv` — 1,858 languages: iso639_3, glottocode,
  name, l1_speakers, year, source_note.
- `data/processed/phoneme_prevalence.csv` — 4,127 rows: 2,604 strict + 1,516
  lumped segments + 7 wide classes; columns include all three percentages,
  raw weighted sums, top allophones, and which strict variants each lumped
  symbol absorbed.
- Raw caches: `data/raw/wikidata_l1/p1098_raw.json`, `data/raw/iso639/iso-639-3.tab`.
