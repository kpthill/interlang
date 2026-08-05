# Punctuation and capitalization survey

*Run 2026-08-05. Script: [`../scripts/punctuation_survey.py`](../scripts/punctuation_survey.py).
Data: [`../data/processed/punctuation_survey.csv`](../data/processed/punctuation_survey.csv).*

The letters are decided (principles.md §3.7: ASCII IPA, one letter per phoneme,
`p t k b d g m n f s h j w l r a e i o u`). This is the survey for everything layered
on top of the letters — sentence-final marks, question and exclamation marks, commas,
quotation marks, capitalization, word spacing, number separators, apostrophe and
hyphen. It exists so the conventions can be picked from a table rather than argued
about. **The recommendation is in §10.**

Everything is weighted by **total (L1+L2) speakers** — the ease-of-learning objective's
weighting (principles.md §2). L1 shares are given alongside where they are available,
because the two sometimes point different ways.

---

## 0. How to read this, in three lines

1. Our orthography is **ASCII Latin, left-to-right**. A convention used by 20% of the
   world but needing a non-ASCII character is *context*, not a candidate. Each table
   marks which options are actually available to us.
2. Rows are marked **[CLDR]** (real database) or **[recalled]** (written from the
   author's knowledge, not measured). Do not read a [recalled] percentage as dataset
   output. See §1.
3. Percentages are shares of a **covered set**, not of humanity. The set is stated per
   table.

---

## 1. Where the numbers come from — and where they do not

### [CLDR] — genuinely measured

CLDR (`common/main/*.xml`, commit `9fcd511`) carries per-locale `<delimiters>`
(quotation marks) and `<numbers>` (decimal separator, grouping separator, grouping
pattern) for 1,149 locales. The script extracts those with CLDR's inheritance chain
resolved (the "same as parent" marker, plus `parentLocales` overrides such as
`es_MX → es_419` and `en_GB → en_001`), then weights each locale by its speaker
population from `cldr_supplementalData.xml`.

Weighting is at the **(language, territory)** grain — finer than the project's usual
per-ISO-639-3 total, because `es_MX` (`1,000.50`) and `es_AR` (`1.000,50`) genuinely
differ. The per-language sums are asserted in the script to reproduce
`populations.cldr_totals()` exactly (max drift 0.0000 speakers), so this weighting and
the rest of the project's remain reconcilable. Denominator: **10.868B** total-speaker
weight, i.e. the whole world — CLDR's population table covers every territory.

One caveat, carried as its own column. CLDR's `↑↑↑` marker means "checked, same as the
parent" — a positive statement, so it counts. But **12.7%** of the quotation weight and
**13.4%** of the number weight belongs to locales whose whole chain is silent below
`root`; those silently inherit root's curly quotes and `.`/`,`, which inflates exactly
the options we are minded to pick. Every [CLDR] table therefore gives both the full
share and `stated only` (the share within the surveyed subset). They differ by about
three points and change no ranking.

### [recalled] — NOT measured, and this is a real limitation

**There is no machine-readable database of sentence-final punctuation, capitalization
rules, or word spacing.** Those tables were written out by hand for the top 50
languages by CLDR total-speaker count. The population weights attached to them are
real; the convention labels are recalled and could contain errors. Given the stakes —
a one-session survey to settle a convention nobody wants to spend a week on — that was
judged acceptable. It would not be acceptable for a phonology decision.

Known softness in the recalled labels:

- **One convention per language**, but real usage is mixed. Hindi and Marathi are
  recorded as danda-final (`।`); educated modern Hindi writes `.` a large fraction of
  the time, especially online. Amharic is recorded with the Ethiopic question mark
  `፧`; the ASCII `?` is common in practice. Both of these move weight *toward* the
  ASCII options, so the ASCII column is if anything understated.
- **Script assignment is the dominant modern script.** Punjabi is correctly split
  (`pan` = Gurmukhi in India, `pnb` = Shahmukhi/Arabic in Pakistan); Uzbek is counted
  as Latin, Hausa as Boko (Latin), Javanese as Latin.
- **Coverage.** The top 50 languages are 8.987B of 10.868B total-speaker weight =
  **82.7% of the world**. Percentages in [recalled] tables are shares of that 82.7%.

Six languages outside the top 50 carry the conventions that are the whole reason
someone asks the question (Greek `;`, Armenian `։ ՞ ՜`, Khmer `។`, Lao, Hebrew,
Georgian). They are reported as **context** and are deliberately **excluded from the
percentages** — hand-picking languages because they have an unusual convention would
inflate that convention's prevalence.

---

## 2. Sentence-final punctuation [recalled]

*Share of the top-50 set (82.7% of world total-speaker weight).*

| Mark | ASCII? | Languages | % total-weighted | % L1-weighted | Who |
|---|---|---:|---:|---:|---|
| `.` | **yes** | 31 | **59.3%** | 51.4% | all Latin/Cyrillic, Korean, Arabic and Persian proper, Dravidian, Gujarati, Odia |
| `。` ideographic | no | 7 | 20.0% | 26.7% | Mandarin, Yue, Wu, Xiang, Min Nan, Hakka, Japanese |
| `।` danda | no | 5 | 13.5% | 18.0% | Hindi, Marathi, Bhojpuri, Bengali, Punjabi (Gurmukhi) |
| `۔` Arabic full stop | no | 4 | 5.7% | 2.3% | Urdu, Western Punjabi, Pashto, Sindhi |
| *(space, no mark)* | **yes** | 1 | 0.6% | 0.4% | Thai |
| `።` Ethiopic | no | 1 | 0.4% | 0.4% | Amharic |
| `။` | no | 1 | 0.4% | 0.7% | Burmese |

Context (excluded): Khmer `។` (0.14% of world), Armenian `։` (0.05%), Lao writes a
space (0.05%).

**Available to us:** `.` or nothing. `.` is the only ASCII option with meaningful
prevalence, and it is also the plurality option outright. Note the size of the
non-Latin block: **40% of the covered world does not end sentences with a period**,
which is worth knowing but changes nothing, because none of their marks are ASCII.

## 3. Question and exclamation marks [recalled]

| Question mark | ASCII? | Languages | % total | % L1 |
|---|---|---:|---:|---:|
| `?` | **yes** | 31 | **60.6%** | 56.7% |
| `？` fullwidth | no | 7 | 20.0% | 26.7% |
| `؟` Arabic (mirrored) | no | 9 | 12.7% | 6.0% |
| `¿ … ?` paired | no | 1 | 5.7% | 9.7% |
| *(none — Thai)* | yes | 1 | 0.6% | 0.4% |
| `፧` Ethiopic | no | 1 | 0.4% | 0.4% |

| Exclamation mark | ASCII? | Languages | % total | % L1 |
|---|---|---:|---:|---:|
| `!` | **yes** | 42 | **74.3%** | 63.6% |
| `！` fullwidth | no | 7 | 20.0% | 26.7% |
| `¡ … !` paired | no | 1 | 5.7% | 9.7% |

Two specifically-asked-about options:

- **Spanish inverted `¿ ¡`.** Exactly one language, 5.7% of the covered set — and it is
  the *only* system in the survey that marks the *start* of the sentence, which is its
  genuine functional advantage (you know it is a question before you read it). Both
  characters are non-ASCII. It could be imitated in ASCII, but no other language does
  this and it doubles the typing cost. Not recommended.
- **Greek `;` for question.** Modern Greek only, ~13M speakers, 0.11% of world
  total-speaker weight — outside the top 50 and reported as context. It is ASCII, and
  it is a trap: `;` reads as a semicolon to every non-Greek Latin-script reader. Not
  recommended.

**Available to us:** `?` and `!`, uncontested.

## 4. Comma [recalled]

| Mark | ASCII? | Languages | % total | % L1 |
|---|---|---:|---:|---:|
| `,` | **yes** | 31 | **65.8%** | 65.8% |
| `、` ideographic | no | 7 | 20.0% | 26.7% |
| `،` Arabic | no | 9 | 12.7% | 6.0% |
| *(space)* | yes | 1 | 0.6% | 0.4% |
| `፣` Ethiopic | no | 1 | 0.4% | 0.4% |
| `၊` Burmese | no | 1 | 0.4% | 0.7% |

The CJK figure lumps two marks: `、` (list separator) and `，` (fullwidth clause comma).
Both are non-ASCII, so the distinction does not reach a decision.

**Available to us:** `,`.

## 5. Quotation marks [CLDR] — *the one place the English default breaks*

*Share of the full 10.868B world total-speaker weight, 1,583 language×territory locales.
(The locale counts below total 1,565, because the count column deduplicates by display
label — `zh` and `zh_Hant` in Taiwan are one label. Weights are unaffected.)*

Primary (outer) quotes:

| Pair | ASCII? | Locales | % total | % stated only | Who |
|---|---|---:|---:|---:|---|
| `“ ”` | **no** | 1085 | **78.5%** | 75.4% | English, and almost every locale with no override |
| `« »` | no | 240 | 9.6% | 11.1% | French, Russian, Spanish(some), Armenian, Greek, Portuguese(PT) |
| `” “` | no | 49 | 6.4% | 7.3% | Arabic and other RTL locales (same glyphs, reversed) |
| `„ “` | no | 75 | 2.0% | 2.2% | German, Bulgarian, Czech, Serbian, Bosnian |
| `「 」` | no | 23 | 1.5% | 1.7% | Japanese, Traditional-Chinese locales |
| `„ ”` | no | 42 | 0.9% | 1.1% | Polish, Romanian, Hungarian |
| `” ”` | no | 19 | 0.5% | 0.6% | Finnish, Swedish, Hebrew |
| `‘ ’` | no | 22 | 0.4% | 0.5% | Dutch |
| **`" "` straight ASCII** | **yes** | **0** | **0.0%** | — | **nobody** |

Nested (inner) quotes, same source: `‘ ’` 78.6%, `’ ‘` 6.7% (RTL), `« »` 3.7%,
`“ ”` 2.6%, `„ “` 2.3%, `‚ ‘` 1.8%, `‹ ›` 1.6%, `『 』` 1.5%.

**Not one of CLDR's 1,149 locales uses the straight ASCII `"`.** Every quotation
convention in the world is typographic, i.e. outside our character budget. This is the
single area where "just do what English does" does not resolve to an ASCII answer:
English style *is* `“ ”`, and `" "` is not English typographic style — it is the
typewriter approximation of it — what plain-text English has used since the typewriter
put one key where two glyphs belonged, and what every keyboard still emits by default.

So the decision here is a re-specification, not a copy: **use `"` for outer quotes and
`'` for nested**, understood as the ASCII rendering of the world's dominant pair. The
only real alternative with independent backing is `« »` (9.6%, and it is the
*explicitly stated* runner-up at 11.1%), which is non-ASCII and therefore out.

Both `"` and `'` are free — the alphabet is 20 letters and uses no apostrophe (§9).

## 6. Capitalization [recalled] — the one area that is a real question

This is not a table row. **A majority of humanity writes in a script that has no
capital letters at all.**

| Case system | Languages | % total-weighted | % L1-weighted |
|---|---:|---:|---:|
| **unicameral** (no case whatsoever) | 31 | **53.0%** | **60.4%** |
| bicameral (has capitals) | 19 | 47.0% | 39.6% |

Unicameral here means Han, Japanese, Hangul, Arabic, Devanagari, Bengali, Gurmukhi,
Telugu, Tamil, Gujarati, Kannada, Malayalam, Odia, Thai, Myanmar, Ethiopic — and,
outside the top 50, Hebrew and (in modern practice) Georgian. Bicameral is Latin and
Cyrillic, plus Greek and Armenian in the context set.

Among the bicameral 47%, what gets capitalized:

| Rule | Languages | % total | % L1 | Note |
|---|---:|---:|---:|---|
| sentence-initial + proper nouns | 17 | 26.1% | 30.5% | the ordinary case |
| … **+ first-person `I`** | 1 | 19.3% | 7.6% | **English only** |
| … **+ ALL nouns** | 1 | 1.6% | 1.5% | **German only** |

Note the shape of that table: capitalizing `I` looks like a big number (19.3%) purely
because English is one-fifth of the total-speaker weight. It is a one-language
orthographic accident, and its L1 share (7.6%) shows what it really is. German noun
capitalization is likewise one language.

**The tradeoff, stated honestly.**

*For having no case at all:* it matches 53% of the weighted world and 60% by L1; it
halves the glyph inventory a learner has to acquire (20 shapes, not 40); it removes a
rule that has genuine judgment in it, since "is this a proper noun?" is a category
whose boundaries differ across languages (English capitalizes days, months,
nationalities and language names; Spanish and French do not; German capitalizes every
noun). It is also consistent with the spirit of §3.6's "no deviation from pronounce
what is written" — case is a purely visual distinction with no phonological content.

*For keeping sentence-initial capitals:* every reader of a Latin-script language
expects them, and our orthography is Latin, so 100% of our readers arrive with that
expectation regardless of what their L1 script does. They mark sentence boundaries
redundantly with the period, which is exactly the kind of redundancy that helps under
noise. And the rule is *mechanical*: first letter of a sentence, no judgment, no
exceptions — unlike the proper-noun rule.

*For keeping proper-noun capitals specifically:* in an IAL, names are borrowed and
transliterated into a 20-letter alphabet, so collisions between a transliterated name
and an ordinary word are likely. A capital is a cheap disambiguator that says "this is
a name, do not look it up." That is a real function, not just convention. The cost is
that "what is a proper noun" has to be specified, and the specification is where every
natural language's rule differs.

## 7. Word spacing [recalled]

| Convention | Languages | % total | % L1 | Who |
|---|---:|---:|---:|---|
| spaces between words | 40 | **77.9%** | 70.7% | everything alphabetic or abugida, incl. Korean |
| none (scriptio continua) | 9 | 21.1% | 27.8% | Mandarin, Yue, Wu, Xiang, Min Nan, Hakka, Japanese, Thai, Burmese |
| spaces between *syllables* | 1 | 1.0% | 1.5% | Vietnamese |

Context (excluded): Khmer and Lao also write without word spaces (0.19% of world
combined).

Scriptio continua works for Chinese and Japanese because the writing system marks word
boundaries another way — a shift between logographic and syllabic characters. Thai
manages without that and is genuinely hard to segment. Neither is available to an
alphabetic script. This is the least interesting question in the survey: spaces, 77.9%,
and no realistic alternative.

Vietnamese is the interesting outlier — it writes each syllable as a separate token
(`Việt Nam`, not `Việtnam`), a habit inherited from its former Han-character
orthography. If the interlang ends up highly analytic with short roots, this is a live
option for how compounds are written, and it is a compound-writing question rather than
a punctuation one. Left to §3.6's deferred compound decision.

## 8. Decimal and thousands separators [CLDR]

*Share of the full 10.868B world total-speaker weight. Latin-digit separators, i.e.
what the locale does when it writes with 0-9.*

| Format | ASCII? | Locales | % total | % stated only | Who |
|---|---|---:|---:|---:|---|
| `1,000.50` | **yes** | 1006 | **74.4%** | 70.4% | English, Chinese, Japanese, Korean, most of Asia and Africa, Mexico |
| `1.000,50` | **yes** | 242 | 16.2% | 18.7% | German, Spanish (Spain, most of S. America), Italian, Dutch, Indonesian, Portuguese |
| `1 000,50` (NBSP U+00A0) | no | 210 | 5.9% | 6.8% | Russian, Polish, Czech, Swedish, Afrikaans, Ukrainian |
| `1 000,50` (NNBSP U+202F) | no | 69 | 3.1% | 3.5% | French |
| `1 000.50` (NBSP) | no | 13 | 0.2% | 0.2% | Kazakh |
| `1'000.50` | **yes** | 8 | 0.15% | 0.15% | Swiss German |
| `1'000,50` | **yes** | 5 | 0.07% | 0.08% | Swiss French, Lombard |
| `1٬000٫50` Arabic-Indic | no | 3 | 0.02% | 0.02% | some Arabic locales |

Collapsed to the decimal mark alone: **`.` 74.8%, `,` 25.2%.** That is a real 3:1
majority but not the walkover the top row suggests — a quarter of the world reads
`1.000,50` as one thousand.

Grouping *pattern*, separately:

| Pattern | Locales | % total | % stated only |
|---|---:|---:|---:|
| 3-digit, `1,000,000` | 1505 | **84.6%** | 82.3% |
| Indian 2-2-3, `10,00,000` (lakh/crore) | 53 | 15.4% | 17.7% |

The Indian grouping is not a rounding error — 15% of the world writes ten lakh as
`10,00,000`. It is ASCII-expressible, so unlike the other minority conventions it is a
genuine candidate. It is also tied to a numeral *vocabulary* (lakh, crore) that we are
not adopting, and mixing 2-2-3 grouping with a 3-digit number-word system would be
worse than either.

A third of the "space" group (9.2% combined, France + Russia + Poland + Nordics) is
following the SI/BIPM recommendation, which is the only *deliberately international*
convention on this list. It is attractive on neutrality grounds and unavailable on
technical ones: the SI separator is a non-breaking thin space, and using an ASCII space
instead would make `1 000` two tokens for every parser in existence.

## 9. Apostrophe and hyphen [recalled, notes only]

Nothing to count here; there is no database and no prevalence question, only usage
patterns worth naming.

| Mark | Use | Where |
|---|---|---|
| `'` | elision / possessive (`don't`, `l'eau`, `John's`) | English, French, Italian, Catalan, Dutch |
| `'` | **a letter of the alphabet** — glottal stop or ejective | Hawaiian ʻokina, Guarani, many Latin-script African orthographies |
| `'` | not used at all | Han, Japanese, Korean, Thai, Devanagari, Arabic |
| `-` | compound joiner, end-of-line break | most Latin-script and Cyrillic orthographies |
| `-` | reduplication and affix marker | Indonesian/Malay `orang-orang`, Swahili, Tagalog |
| `-` | not used at all | Han, Japanese, Thai |

The one thing here that matters to us: **the apostrophe is a letter in a lot of
Latin-script orthographies**, and using it as punctuation is a live source of
confusion for exactly the learners we are optimizing for. §3.6 already rules out
elision (no sandhi, no alternations, pronounce what is written), and §3.7's alphabet
has no glottal stop — so the apostrophe has no work to do in the language and stays
free for nested quotation (§5).

The hyphen's fate depends on the compound-writing decision, which §3.6 defers. If
compounds are written solid, the hyphen has no job either.

---

## 10. Recommended default set

Patrick's stated fallback was "English-style unless something beats it". Nothing beats
it on marks, punctuation or numbers. Two things need re-specifying rather than copying,
and one is a genuine open choice.

| Area | Recommendation | Backing | Status |
|---|---|---|---|
| Sentence-final | `.` | 59.3%, only viable ASCII option | matches English |
| Question | `?` | 60.6% | matches English |
| Exclamation | `!` | 74.3% | matches English |
| No inverted `¿ ¡` | — | Spanish only, 5.7%, non-ASCII | — |
| Comma | `,` | 65.8% | matches English |
| Quotation, outer | `"` | **0% of locales — see below** | **re-specified** |
| Quotation, nested | `'` | ASCII rendering of `‘ ’` (78.6%) | **re-specified** |
| Word spacing | spaces between words | 77.9%, no alternative for an alphabet | matches English |
| Decimal mark | `.` | 74.8% | matches English |
| Thousands separator | `,`, 3-digit groups | 74.4% / 84.6% | matches English |
| Capitalization | sentence-initial + proper nouns, **no** `I`, **no** German noun rule | 26.1% + see §6 | **English minus its two quirks** |
| Apostrophe | not used | §3.6 rules out elision; keeps `'` free | — |
| Hyphen | deferred with compounds | — | open |

**Where the data disagrees with "English-style":**

1. **Quotation marks.** English style is `“ ”` / `‘ ’`, which is not ASCII, and *no
   locale on earth* specifies the straight `" "`. So `"` and `'` are not "what English
   does" — they are the typewriter approximation. Adopt them explicitly on that basis,
   not by assuming English gave us an ASCII answer.
2. **Capitalizing `I`.** 19.3% of the total-speaker weight, all of it one language, and
   only 7.6% by L1. Do not inherit it.
3. **Capitalizing all nouns.** German only, 1.6%. Do not inherit it. (Nobody was going
   to, but it is the third option in the space and it should be on the record as
   rejected rather than unconsidered.)
4. **Having capital letters at all.** 53% of the weighted world — 60% by L1 — writes in
   a script with no case. This is the only area where the majority of humanity does
   something structurally different from English, and it is the one item in this
   document that deserves a minute of actual thought.

   *Recommendation: keep case, with sentence-initial and proper-noun capitals.* Our
   orthography is Latin, so every reader of it arrives with the expectation regardless
   of their L1 script; sentence-initial is mechanical and exception-free; and
   proper-noun capitals do real disambiguation work in a language whose names are
   transliterated into 20 letters. The honest alternative is **all-lowercase, no case
   distinction**, which matches the 53% majority, halves the glyph inventory, and
   deletes the one orthographic rule that requires a lexical judgment. If the project's
   instinct is "simpler is better and the majority of the world agrees", that is a
   defensible choice and this survey does not refute it.

   If case is kept, a smaller sub-choice follows: whether proper-noun capitalization is
   a *rule* (with a definition of proper noun) or merely *permitted*. Recommend it be a
   rule stated in one sentence — names of people, places and organizations — and
   explicitly **not** extended to days, months, nationalities or language names, since
   that extension is an English quirk that Spanish, French and Russian all decline.

5. **Decimal `.` vs `,`.** `.` wins 74.8% to 25.2%, so the English default holds, but
   the margin is 3:1 rather than overwhelming — a quarter of the world reads
   `1.000,50` as one thousand. Worth knowing before anyone claims the choice is obvious.

**Where the data supports the default with no asterisk:** `. ? ! ,`, word spaces,
3-digit grouping. Those six are plurality winners *and* the only ASCII options
available, so there is nothing to trade off.

---

## 11. Suggested change to `principles.md` — **APPLIED 2026-08-05**

Both edits below are now in `principles.md`: the subsection under §3.7, and the narrowed
§7 entry ("Case or no case"). Text kept here for the record.


§3.7 currently says punctuation and capitalization are "pending a survey (§7): the
policy is *whatever is most common among the world's languages weighted by total
speakers, with English-style as the default*", and §7 carries the matching OPEN entry.
The survey is now run. Suggest replacing that paragraph with a short subsection, and
closing the §7 entry:

> #### Punctuation and capitalization (**SOFT**, 2026-08-05)
>
> Surveyed in [`punctuation-survey.md`](punctuation-survey.md), weighted by total
> (L1+L2) speakers. Adopted: `.` `?` `!` `,` as in English; `"` outer and `'` nested
> quotation, understood as the ASCII rendering of the world's typographic pair (no
> locale in CLDR specifies straight quotes); spaces between words; `1,000.50` with
> 3-digit grouping. Rejected: Spanish inverted `¿ ¡` (one language), English `I`
> capitalization (one language, 7.6% of L1 weight), German noun capitalization (one
> language), Indian 2-2-3 grouping (15% of the world, but tied to a lakh/crore numeral
> vocabulary we are not adopting).
>
> **Capitalization is SOFT and worth revisiting**: 53% of the world's total-speaker
> weight (60% of L1) writes in a unicameral script with no capitals at all. Working
> position is sentence-initial + proper nouns; the live alternative is no case at all.
> Compound writing (and with it the hyphen) stays deferred.

The §7 entry ("Punctuation & capitalization (OPEN, survey running)") can then be
narrowed rather than deleted — everything except one question is answered, and the
remaining one is worth keeping visible:

> **Case or no case (OPEN).** The survey settled every other punctuation convention;
> this one it only framed. 53% of total-speaker weight (60% L1) writes caselessly.
> Working position: sentence-initial + proper nouns. See
> [`punctuation-survey.md`](punctuation-survey.md) §6.
