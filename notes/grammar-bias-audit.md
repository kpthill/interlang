# The final grammar bias audit: where this grammar actually landed

*Run 2026-08-06, on the finished grammar (19 words, 7 rules —
[`principles.md`](principles.md) §3.2). Script:
[`../scripts/grammar_bias_audit.py`](../scripts/grammar_bias_audit.py) · outputs:
`data/processed/grammar_bias_audit.csv` (one row per language),
`grammar_bias_audit_features.csv` (the encoded feature vector with its rationale and
per-feature population cost), `grammar_bias_audit_apics_features.csv`.
This is the deliverable [`grammar-plan.md`](grammar-plan.md) §1 promised:*

> "This grammar is 90% Standard Average European with a Mandarin TAM system" should be a
> measured statement we publish, not a bias we absorb.

**It is now measured, and the guess was wrong in both halves.** The grammar is not Standard
Average European — SAE sits at the **41st percentile** of the world's languages by similarity
to interlang, *below* the world average. And it does not have a Mandarin TAM system; it has
**no TAM system at all**, which is the single feature that separates it most sharply from
every contact language ever recorded. What it *is*, measurably, is a **Mainland-Southeast-Asian-shaped
isolating language that sits inside the restricted-pidgin cloud** — which is, for once,
exactly where the project aimed.

---

## 0. How to read this, and the words in it

**Jargon, once.**

- **Grambank** — a database of 195 yes/no (and a few three-way) grammatical questions asked
  of 2,393 languages. "Are there prepositions?" "Is there a gender system?"
- **APiCS** — the *Atlas of Pidgin and Creole Language Structures*: 336 features across 104
  contact-language varieties. The project's north star, because contact languages are the
  natural experiment in what adults converge on under time pressure.
- **L1** — first-language (native) speakers. This project counts **people, not languages**
  ([`principles.md`](principles.md) §2), and the two answers disagree constantly.
- **Agreement** — for a given language, the fraction of features that *both* it and interlang
  have a value for, on which the values are the same. So 0.84 for Mandarin means: of the 187
  Grambank features we encoded and Mandarin is coded for, we give the same answer on 84%.
- **Standard Average European (SAE)** — Haspelmath's term for the bundle of features shared
  across western/central European languages regardless of family (definite and indefinite
  articles, *have*-perfects, relative pronouns, participial passives, and so on). Its
  *nucleus* is French, German, Dutch, northern Italian and Romansh.
- **Restricted / expanded pidgin / creole** — the three-way contact stratification this
  project adopted in [`grammar-tier2-tam.md`](grammar-tier2-tam.md) §0. A **restricted
  pidgin** is the closest analogue to an auxiliary language: adults, no shared language, no
  native speakers. An **expanded pidgin** carries a full communicative load but is still
  adult-built. A **creole** has been nativised by children.

**Provenance marks.** **[measured]** = computed by the script from a dataset in this repo.
**[recall]** = general knowledge, not verified against a source we hold.

**The main judgment call is the encoding, and it is a big one.** Everything in Part 1 rests
on `INTERLANG_GB` and `INTERLANG_APICS` in the script: 187 Grambank features and 65 APiCS
parameters, each carrying a one-line rationale naming the decision it comes from. Every one
is a claim that one of our decisions is *the same thing* a database coder would have coded.
A different analyst would code some of them differently. §1.7 measures how much that
matters.

---

## 1. PART 1 — where does this grammar actually land?

### 1.1 The encoding, and what was left out

**[measured]** 187 of Grambank's 195 features carry an interlang value: **33 positive, 154
negative.** The imbalance is the grammar — it was designed almost entirely by *removing*
distinctions, and Grambank mostly asks "is there an X?".

The eight left blank, and why:

| feature | why not coded |
|---|---|
| GB035 three-or-more distance contrasts in demonstratives | undecided, and a lexicon question |
| GB129 fewer than ~100 verb roots | lexicon stage |
| GB160 reduplication of non-verbs/non-nouns | too specific to call from what we decided |
| GB177 verbal animacy marking | a marker we could not have; not forced |
| GB296 ideophones | lexicon stage, undecided |
| **GB306 independent reciprocal pronoun** | **reciprocals were never decided** — §3 |
| **GB331 non-adjacent (extraposed) relative clauses** | **never decided** — §3 |
| GB108 directional/locative marking on the verb | see §3.1: this is *not* the satellite-framing feature and reading it that way would be a category error |

**Where a decision maps onto no coded feature, it is left out rather than forced onto an
adjacent one.** That rule exists because this project has already made the opposite mistake
twice: [`grammar-tier3-combination.md`](grammar-tier3-combination.md) §7 records WALS 123A
applied to a construction with no gap in it, and WALS 94A read as answering a question about
a different constituent. *A feature name is not a feature definition.*

**Grambank, not WALS, for the similarity computation.** [`grammar-plan.md`](grammar-plan.md)
§3.1: Grambank is 4.7× denser (0.75 vs 0.16) and codes the big languages WALS misses.
Density is decisive for a *per-language* score in a way it is not for a marginal percentage.
WALS is used only in Part 2, where a specific write-up quoted a specific WALS chapter.

### 1.2 The calibration that has to come first

Grambank is 68% zeros and interlang's vector is 82% negative. A raw agreement of 0.7
therefore means nothing until it is compared to something. Three baselines, all computed on
the identical feature set **[measured]**:

| vector | by language | **by L1** | by total speakers |
|---|---|---|---|
| **INTERLANG** | **0.693** | **0.718** | 0.714 |
| all-zero — a language with *none* of these features | 0.665 | 0.643 | 0.638 |
| all-mode — the majority value of every feature, by language | **0.742** | 0.719 | 0.716 |
| all-mode **by L1** — the population-optimal fixed vector (**the ceiling**) | 0.702 | **0.761** | 0.760 |
| two randomly drawn real languages | 0.657 | — | — |

Random language pairs: median 0.656, 90th percentile 0.750, 99th 0.836, max 0.962.
**Interlang sits at the 70th percentile of the real-language-pair distribution** — i.e. it is
a more typical-looking language than two random languages are typical of each other, but not
extraordinarily so.

Three things fall out of this table and they are the honest frame for everything below.

1. **Scoring above the all-zero floor is not automatic and we clear it, but not by much on
   the by-language column** (+0.028). By population the gap is nearly three times larger
   (+0.075). That is the project's objective working: we bought population fit, not language
   fit.
2. **By language count, interlang is *worse* than the trivial "all-mode" strawman**
   (0.693 vs 0.742). It is not trying to be the average language and it is not.
3. **By population it reaches 63% of the way from the floor to the ceiling** — 0.718 against
   a maximum of 0.761 that *no real language achieves either*. **[measured]** Interlang
   differs from the population-optimal vector on **32 of 187 features**, and those 32 *are*
   the entire population cost of the grammar. They are enumerated in §1.6 and Part 2.

### 1.3 Nearest and furthest — and the answer is Mainland Southeast Asia

**[measured]** 2,299 Grambank languages share ≥60 features with our vector (median 155).

**The 12 most similar:**

| language | family / group | macroarea | shared | agreement |
|---|---|---|---|---|
| Haroi | Austronesian (Chamic) | Eurasia | 91 | **0.912** |
| U | Austroasiatic | Eurasia | 135 | 0.911 |
| **San Andres Creole English** | **contact language** | North America | 161 | 0.907 |
| She | Hmong-Mien | Eurasia | 156 | 0.904 |
| **Belize Kriol English** | **contact language** | North America | 124 | 0.903 |
| Central Gelao-Qau | Tai-Kadai | Eurasia | 95 | 0.895 |
| Bih | Austronesian (Chamic) | Eurasia | 174 | 0.891 |
| Hu | Austroasiatic | Eurasia | 169 | 0.888 |
| Western Cham | Austronesian (Chamic) | Eurasia | 148 | 0.885 |
| Chong of Chanthaburi | Austroasiatic | Eurasia | 185 | 0.881 |
| **Nicaragua Creole English** | **contact language** | North America | 150 | 0.880 |
| Mak (China) | Tai-Kadai | Eurasia | 166 | 0.880 |

**Two clusters, and they are the only two.** Mainland Southeast Asian isolating languages —
Austroasiatic, Tai-Kadai, Hmong-Mien, and the Chamic Austronesian languages that have
converged on the MSEA type — and **Caribbean/Pacific English-lexifier creoles**. Nothing else
appears in the top 25 except one Australian outlier (Iwaidja, on 62 shared features).

**The 10 least similar:** Masai 0.352, Tira 0.365, Otoro 0.381, Krongo 0.384, Turkana 0.400,
Moro 0.405 (all Nilotic, Heibanic or Kadugli-Krongo — the Sudanic belt), Tariana 0.425
(Arawakan), Konso 0.440, Sandawe 0.446, Beja 0.466. **The furthest languages from interlang
are almost all African and South American languages with rich case, gender-class and verbal
agreement systems** — which is what "we removed every distinction" predicts, and it should be
said plainly rather than left implicit.

Among the 60 largest languages by L1, the nearest are **Hakka 0.854, Mandarin 0.840, Wu
0.837, Vietnamese 0.822, Thai 0.814, Haitian 0.814, Khmer 0.811, Igbo 0.801**; the furthest
are **Somali 0.479, Polish 0.529, Amharic 0.530, Hausa 0.563, Fulfulde 0.573, Telugu 0.577.**

### 1.4 By family and by macroarea, by languages and by people

**[measured]** Families with ≥8 Grambank languages. Grambank (via Glottolog) classifies a
creole inside its *lexifier's* family — Haitian is Indo-European, Tok Pisin is Indo-European —
so the 19 contact languages Grambank codes are pulled out into their own group, or they
would inflate whichever family lent them their words.

| family / group | n | **by language** | **by L1** | L1 in group (M) |
|---|---|---|---|---|
| Hmong-Mien | 10 | **0.855** | 0.849 | 0.8 |
| Tai-Kadai | 16 | 0.846 | 0.830 | 32 |
| **contact language** | **19** | **0.821** | 0.684 | 33 |
| Austroasiatic | 78 | 0.796 | 0.804 | 108 |
| Austronesian | 501 | 0.732 | 0.720 | 359 |
| Uralic | 25 | 0.732 | 0.684 | 20 |
| Sino-Tibetan | 184 | 0.726 | **0.825** | 1,172 |
| Mande | 16 | 0.707 | 0.737 | 12 |
| Otomanguean | 32 | 0.700 | 0.747 | 0.04 |
| **Indo-European** | **64** | **0.675** | **0.683** | **1,893** |
| Atlantic-Congo | 296 | 0.675 | 0.673 | 176 |
| Turkic | 14 | 0.670 | 0.670 | 141 |
| Dravidian | 30 | 0.667 | 0.644 | 243 |
| Afro-Asiatic | 112 | 0.665 | **0.595** | 219 |
| … | | | | |
| Nilotic | 14 | 0.612 | 0.689 | 9 |
| Arawakan | 32 | 0.587 | 0.552 | 0.6 |
| Tucanoan | 10 | 0.560 | 0.578 | 0.02 |

**Sino-Tibetan is the by-language/by-people reversal in miniature**: 0.726 across its 184
languages but **0.825 weighted by speakers**, because Mandarin and the other Sinitic
languages are the isolating ones and the Tibeto-Burman majority is not. Afro-Asiatic reverses
the other way (0.665 → 0.595): Arabic and Amharic are further from us than the family
average.

By macroarea:

| macroarea | n | by language | by L1 | L1 (M) |
|---|---|---|---|---|
| Eurasia | 523 | 0.725 | 0.726 | 3,873 |
| Papunesia | 690 | 0.711 | 0.719 | 358 |
| Africa | 530 | 0.672 | **0.635** | 414 |
| North America | 237 | 0.668 | **0.787** | 18 |
| Australia | 120 | 0.666 | 0.668 | 0.02 |
| South America | 199 | 0.645 | 0.649 | 4 |

**North America's by-L1 figure is an artefact and must not be quoted alone.** Glottolog
assigns English and Spanish to Eurasia, so Grambank's entire North American L1 mass is 18M —
and 9.6M of it is Haitian, with the other Caribbean creoles behind it. The 0.787 is measuring
creoles, not North America.

**Africa is the region this grammar fits worst, on both counts**, and by population the gap
is 9 points below Eurasia. That is a finding, not a rounding error, and it is the single most
uncomfortable number in this document.

### 1.5 The languages a reader will ask about

**[measured]** `percentile` = where that language sits among all 2,299.

| language | agreement | percentile | L1 (M) |
|---|---|---|---|
| **Mandarin** | **0.840** | **97** | 918 |
| Vietnamese | 0.822 | 95 | 76 |
| Thai | 0.814 | 93 | 21 |
| **Igbo** | 0.801 | 91 | 27 |
| **English** | 0.743 | 76 | 379 |
| **Indonesian** | 0.739 | 74 | 44 |
| Javanese | 0.713 | 62 | 68 |
| Tamil | 0.701 | 56 | 75 |
| Ewe | 0.686 | 47 | 3 |
| **Hindi** | 0.685 | 47 | 341 |
| **Swahili** | 0.667 | 34 | 16 |
| **Japanese** | 0.665 | 34 | 128 |
| **Turkish** | 0.663 | 33 | 82 |
| Korean | 0.661 | 31 | 77 |
| French | 0.658 | 30 | 77 |
| Tagalog | 0.649 | 26 | 24 |
| Marathi | 0.648 | 26 | 83 |
| Egyptian Arabic | 0.638 | 21 | 65 |
| Burmese | 0.632 | 18 | 33 |
| Russian | 0.624 | 16 | 154 |
| Hausa | 0.563 | 5 | 44 |
| **Standard Arabic** | **0.556** | **4** | — |

**Not in Grambank at all: German, Spanish, Yoruba, Bengali, Persian.** That is a real
limitation of this audit and not a small one — two of the five are among the world's ten
largest languages, and *German is the nucleus of Standard Average European*. The Yoruba
figure the task asked for cannot be produced from Grambank; **Igbo (0.801) and Ewe (0.686)
are the nearest West African substitutes and they disagree by 11 points**, so no single
number would have been trustworthy anyway.

**Standard Average European.** Haspelmath's nucleus is French, German, Dutch, northern
Italian and Romansh; German is absent, so the nucleus here is four languages and that is
stated rather than papered over.

| set | n | mean agreement | percentile | L1-weighted |
|---|---|---|---|---|
| SAE nucleus (French, Dutch, Italian, Romansh) | 4 | **0.674** | **40** | 0.661 |
| SAE wide (+ English, Iberian Romance, Nordic, West/South/East Slavic, Greek, Baltic, Hungarian, Albanian, Frisian) | 23 | **0.675** | **41** | 0.683 |

Per language: French 0.658, Dutch 0.694, Italian 0.652, Romansh 0.690, English 0.743,
Portuguese 0.670, Catalan 0.672, Occitan 0.687, Galician 0.665, Danish 0.701, Swedish 0.710,
Icelandic 0.701, Greek 0.636, Czech 0.668, **Polish 0.529**, Russian 0.624, Ukrainian 0.693,
Serbian-Croatian-Bosnian 0.692, Lithuanian 0.658, Latvian 0.665, Hungarian 0.654, Albanian
0.704, Frisian 0.756.

> **This is the headline finding and it is worth stating without hedging.
> `grammar-plan.md` §1 feared this grammar would be 90% Standard Average European. It is
> not. The average SAE language is at the 41st percentile of similarity to interlang —
> 59% of the world's languages are closer to it than the average European language is.
> English is the SAE outlier at the 76th percentile, and English is an outlier *within*
> SAE precisely on the features we adopted: little case, no gender agreement, fixed SVO,
> free-word negation.** (**FIRM** — measured, and it survives the §1.7 sensitivity run.)

### 1.6 The features that cost population

**[measured]** The 32 features where interlang's value differs from the value the *most
people* have. This is the complete, systematic version of Part 2's harvested override list.

| feature | ours | popular | % of L1 with ours | what it is |
|---|---|---|---|---|
| GB318 | 1 | 0 | **10.8** | plural marked by a dedicated free word |
| GB139 | 0 | 1 | 16.5 | prohibitive not distinct from declarative negation |
| GB187 | 0 | 1 | 19.3 | no productive diminutive |
| GB086 | 0 | 1 | 22.1 | no perfective/imperfective morphology |
| GB262 | 1 | 0 | 27.8 | clause-**initial** polar question particle |
| GB123 | 0 | 1 | 28.6 | no light-verb constructions *(never decided — §3)* |
| GB047 | 0 | 1 | 28.8 | no morphological action-noun derivation |
| GB080 | 0 | 1 | 30.8 | no verbal suffixes |
| GB049 | 0 | 1 | 33.0 | no morphological object-noun derivation |
| GB522 | 0 | 1 | 33.1 | no pro-drop |
| GB408 | 0 | 1 | 33.6 | no accusative flagging |
| GB203 | 1 | 2 | 34.7 | 'all' precedes the noun |
| GB083 | 0 | 1 | 36.1 | no past-tense morphology |
| GB415 | 0 | 1 | 37.3 | no politeness distinction |
| GB048 | 0 | 1 | 37.5 | no morphological agent-noun derivation |
| GB071 | 0 | 1 | 38.9 | no case on pronouns |
| GB044 | 0 | 1 | 38.9 | no plural morphology |
| GB159 | 1 | 0 | 39.3 | nouns reduplicate |
| GB188 | 0 | 1 | 40.1 | no productive augmentative |
| GB105 | 0 | 1 | 40.1 | recipient not marked like a monotransitive patient |
| GB325 | 0 | 1 | 40.9 | no count/mass split in interrogative quantifiers |
| GB328 | 0 | 1 | 41.6 | relative clause cannot precede the noun |
| GB312 | 0 | 1 | 42.6 | no mood morphology |
| GB185 | 0 | 1 | 42.8 | no demonstrative–noun number agreement |
| GB113 | 0 | 1 | 42.8 | no transitivising affix |
| GB150 | 0 | 1 | 43.2 | no clause chaining *(never decided — §3)* |
| GB276 | 0 | 1 | 43.3 | no free comparative degree marker |
| GB136 | 1 | 0 | 46.2 | core-argument order is **fixed** *(the topicalization proxy — §3)* |
| GB119 | 0 | 1 | 47.3 | mood cannot be marked by an inflecting auxiliary |
| GB122 | 1 | 0 | 48.5 | verb compounding is regular |
| GB519 | 0 | 1 | 48.9 | mood not marked by a non-inflecting particle |
| GB120 | 0 | 1 | 49.1 | aspect cannot be marked by an inflecting auxiliary |

**The single largest per-feature population gap is not a decision anybody debated.**
GB318 — a dedicated free plural word — is what **10.8% of world L1** has, because the world
marks plural with a *suffix* and Tier 0 forbade affixes. [`grammar-tier2-np.md`](grammar-tier2-np.md)
§4.2 already flagged this (plural suffix 84.7% of L1 against plural word 5.2% in WALS 33A);
what the audit adds is that **it is the worst single feature in the grammar by population
fit**, worse than politeness. It is a *consequence* of the isolating decision rather than an
independent choice, which is exactly why it never got a paragraph of its own.

The rest of the list is dominated by **the no-affix decision** (GB080, GB047/048/049, GB044,
GB113, GB187, GB188, GB083, GB086, GB312) and **the no-TAM decision** (GB086, GB083, GB312,
GB119, GB120, GB519). Those two, not the individually-argued overrides in Part 2, are where
the population cost actually is.

Averaged over all 187 encoded features **[measured]**: our value is shared by **69.8% of
languages and 72.1% of world L1.**

### 1.7 Sensitivity: does any of this rest on our coding taste?

18 of the 187 encodings are flagged `contested` in the script — places where a defensible
coder could pick the other value. The two that matter most: whether our open-class TAM
adverbs count as Grambank's "non-inflecting word" for tense/aspect/mood (GB519/520/521), and
whether compounding counts as a "productive morphological pattern" for derivation
(GB047/048/049). **Flipping all 18 at once [measured]:**

| | baseline | all contested flipped |
|---|---|---|
| by-language mean | 0.693 | 0.678 |
| by-L1 mean | 0.718 | 0.708 |
| SAE (wide) | 0.675 | 0.684 |
| contact languages | **0.821** | **0.785** |
| Mandarin | 0.840 | 0.818 |
| Hindi | 0.685 | 0.674 |
| English | 0.743 | 0.754 |

**Every ordering that this document draws a conclusion from survives**: contact ≫ Mandarin >
English > SAE ≈ Hindi, before and after. The top-10 nearest languages overlap 5/10 and both
lists are the same two clusters (MSEA isolating + English creoles). **The conclusions are not
artefacts of the encoding; the third decimal place is.** (**FIRM** for the orderings,
**SOFT** for any absolute figure.)

### 1.8 The sharpest test: did we land near the contact languages we designed from?

This is the one that matters, because [`grammar-plan.md`](grammar-plan.md) §1 made contact
languages the north star and everything else the tiebreaker.

**Two independent runs, because neither alone is enough.**

**(a) The Grambank half — same feature vector, 19 contact languages [measured].**

| | agreement |
|---|---|
| San Andres Creole English | 0.907 |
| Belize Kriol English | 0.903 |
| Nicaragua Creole English | 0.880 |
| Pijin | 0.872 |
| Jamaican Creole English | 0.867 |
| Baba Malay | 0.858 |
| Limonese Creole | 0.855 |
| Ambonese Malay | 0.854 |
| Berbice Creole Dutch | 0.853 |
| Bahamas Creole English | 0.832 |
| Haitian | 0.814 |
| Tok Pisin | 0.814 |
| Bislama | 0.809 |
| South Sudanese Creole Arabic | 0.804 |
| Torres Strait–Lockhart River Creole | 0.803 |
| Saramaccan | 0.784 |
| Nubi | 0.775 |
| Sri Lanka Malay | 0.730 |
| **Kinshasa Lingala** | **0.589** |

**Mean 0.821 against a world mean of 0.693 — contact languages sit at the 95th percentile of
similarity to interlang.** The one outlier, Kinshasa Lingala at 0.589, is the case
[`grammar-tier0.md`](grammar-tier0.md) §2.3 already identified as barely restructured: a
creolised Bantu language whose lexifier is typologically identical to it, so it keeps
concord, noun classes and verbal morphology. It is the exception that confirms the reading.

**(b) The APiCS half — 65 parameters mapped independently, 73 rankable lects.** This is the
larger and less contaminated test, and it needs a null, because APiCS parameters are
multi-way alternatives rather than presence/absence and 0.5 might be a high score or a low
one. The null is **how similar contact languages are to each other on the same 65
parameters.**

| | n | interlang's mean agreement | **within-stratum null** |
|---|---|---|---|
| **restricted pidgin** | 9 | **0.531** | **0.517** |
| expanded pidgin | 9 | 0.482 | 0.496 |
| creole | 55 | 0.457 | 0.526 |
| *all contact lects pooled* | 73 | 0.469 | 0.492 |

> **Read the top row.** Interlang agrees with a restricted pidgin on 53.1% of these
> parameters. **Two restricted pidgins agree with each other on 51.7%.** By this measure
> interlang is *as much a restricted pidgin as a restricted pidgin is* — it sits inside
> that cloud rather than beside it. It sits slightly outside the expanded-pidgin cloud
> (0.482 vs 0.496) and **clearly outside the creole cloud** (0.457 vs 0.526).

That gradient is the right shape. [`grammar-plan.md`](grammar-plan.md) §5 standing rule 4
says read the restricted-pidgin columns first and treat creoles as one generation removed
from the process we care about; the finished grammar reproduces exactly that ordering
without having been fitted to it.

**The nearest contact languages are the pidgins, and they are the non-European ones
[measured]:**

| lect | stratum | lexifier | agreement |
|---|---|---|---|
| **Chinuk Wawa** | restricted pidgin | Chinookan | **0.714** |
| **Pidgin Hindustani** | restricted pidgin | Hindi | 0.629 |
| Tayo | creole | French | 0.625 |
| **Eskimo Pidgin** | restricted pidgin | Eskimo-Aleut | 0.617 |
| Diu Indo-Portuguese | creole | Portuguese | 0.594 |
| Kikongo-Kituba | expanded pidgin | Bantu | 0.571 |
| Tok Pisin | expanded pidgin | English | 0.554 |
| Chinese Pidgin Russian | restricted pidgin | Russian | 0.550 |
| Juba Arabic | expanded pidgin | Arabic | 0.547 |

By lexifier group, the ordering is **Other (non-European) 0.544 > Bantu 0.495 > Dutch 0.492
> Arabic 0.489 > Spanish 0.474 > English 0.470 > Malay 0.459 > Portuguese 0.443 > French
0.435.** **The non-European-lexifier group is the one we most resemble, and the Romance
group is the one we least resemble.** For a project whose stated fear was European bias, that
is the reassuring direction — with the caveat in §4 that "Other" is 7 lects.

The furthest contact languages are the Gulf of Guinea Portuguese creoles (Fa d'Ambô 0.323,
Angolar 0.338, Santome 0.369) and the French Caribbean creoles (Haitian Creole 0.385,
Guadeloupean 0.385, Guyanais 0.400) — the most elaborated, most nativised end of the sample.

**Where we disagree with contact languages, and it is almost entirely one decision
[measured]** — the APiCS parameters where the fewest contact lects share our value:

| APiCS | our value | share of contact lects |
|---|---|---|
| **43 position of TAM markers** | **no TAM markers** | **4.2%** |
| 106 focus particle 'also' | precedes the host | 4.2% |
| **50 negation and TAM** | **no TAM marker** | 4.3% |
| **103 polar questions** | **initial question particle** | 5.5% |
| 87 reflexive constructions | dedicated reflexive pronoun | 5.8% |
| **51 unmarked-verb reference** | **no or only one TAM marker** | 8.6% |
| 35 ordinals | all derived from cardinals | 10.4% |
| 28 / 29 / 10 / 31 articles | none of any kind | 10.7–22.7% |
| 19 interrogatives | four-plus compound expressions | 11.1% |
| **49 tense–aspect system** | **no or only one marker** | 12.3% |
| 74 predicative adjectives | invariant copula | 17.6% |
| 78 existential vs 'have' | differentiated | 20.8% |

**Four of the twelve worst rows are the same decision.** The Q6 taste-based choice — no TAM
grammar at all — is quantitatively the largest single departure this grammar makes from the
contact record, and it is *the one decision the project explicitly recorded as taste rather
than evidence* ([`grammar-tier2-tam.md`](grammar-tier2-tam.md) §4.1). The audit confirms the
self-assessment at full strength: **fewer than 5% of contact languages have no TAM markers.**

And where we agree, we agree strongly: no numeral classifiers 94.4%, no clusivity 90.3%,
relative clause after the noun 90.3%, no person syncretism 88.9%, no dual 88.9%, numeral
before noun 88.9%, prepositions 87.7%, plain pronoun conjunction 86.8%, negative particle
86.1%, SVO 83.8%.

**Verdict (SOFT — n=9 in the deciding stratum, 65 parameters, and the mapping is a judgment
call): yes, we landed there.** Interlang is a statistically ordinary member of the
restricted-pidgin population on these parameters, an outlier from the creole population, and
its single biggest deviation is the one departure the project had already flagged as taste.

---

## 2. PART 2 — the population overrides, collected and re-measured

Every decision taken against a majority (or large plurality) of world L1. **`quoted` is the
figure the deciding write-up gave; `measured` is recomputed by this script from the same
feature and dataset.** They are not copied — the point of re-measuring is that a write-up's
number should be checkable, and if it is not, the write-up's number is the one to distrust.

**[measured] All twelve check out to within 0.1 points.** That is a small but real result
about the project's own reliability.

| rank | decision | source (n) | quoted | **measured % of L1 overridden** | by languages |
|---|---|---|---|---|---|
| 1 | **No politeness distinction in pronouns** | WALS 45A (205) | 85.0 | **85.1** | 34.6 |
| 2 | **No gender in pronouns** | WALS 44A (375) | 77.9 | **77.8** | 32.8 |
| 3 | **No pro-drop — the subject is obligatory** | GB522 (1,492) | 66.9 | **66.9** | 73.6 |
| 4 | **A relativizer, not the bare gap** | WALS 122A (165) | 65.4 | **65.4** | 75.2 |
| 5 | **No comparative degree marker** ('more', *-er*) | GB276 (1,258) | 56.7 | **56.7** | 33.2 |
| 6 | **The prohibitive uses the ordinary negator** | WALS 71A (492) | 54.7 | **54.7** | 66.3 |
| 7 | **No serial verb constructions** | GB118 (1,543) | 48.4 | **48.4** | 53.0 |
| 8 | **Adjectives take the copula, not verb syntax** | GB068 (1,892) | 43.7 | **43.7** | 48.6 |
| 9 | **No 'exceed' comparative** | GB265 (1,241) | 41.5 | **41.5** | 32.1 |
| 10 | **No clusivity** | GB028 (2,289) | 37.3 | **37.3** | 52.6 |
| 11 | **No numeral classifiers** | GB057 (2,110) | 36.4 | **36.4** | 23.6 |
| 12 | **No dual** | GB031 (2,264) | 1.4 | **1.4** | 26.3 |

**Notes that the ranking hides.**

- **Rows 10 and 12 are in the table to show the bottom of it.** Clusivity is a *majority by
  language count* (52.6%) and a minority by people (37.3%); the dual is 26.3% of languages
  and **1.4% of L1**. Neither is really an override — they are the by-language/by-people
  reversal working in our favour. They are listed so the ranking is complete rather than
  curated.
- **Rows 6 and 8 override the contact record too**, not just the population. The prohibitive
  decision is [`grammar-tier2-negation.md`](grammar-tier2-negation.md)'s own "weakest call";
  the adjectival copula overrides **8 of 9 restricted pidgins**, the strongest single pidgin
  signal in the project.
- **Row 4 is the odd one out**: adopting a relativizer overrides a majority by *adding*
  machinery rather than removing it, which is the opposite of every other row. The reason
  ([`grammar-tier3-combination.md`](grammar-tier3-combination.md) §3) is that gap-strategy
  languages have case, agreement or verb morphology to mark the clause edge and we have none
  — i.e. it is an override *caused by* the other overrides.
- **The reasons are in the script's `OVERRIDES` table**, one per row, so the ranking and the
  justifications travel together.

### 2.1 The one that was rejected on a false premise, and reversed

**The passive.** [`grammar-tier3-cleanup.md`](grammar-tier3-cleanup.md) §2 first rejected it
on the argument *"a passive needs verb morphology or a participle and we have neither"*, then
reversed §2a when that turned out to be false.

**[measured]** WALS 107A, n=370: passive **present** in 43.0% of languages but **95.2% of
world L1** (97.5% of total speakers); absent in 57.0% of languages and **4.8% of L1**.
Grambank GB302 — a phonologically **free** passive marker, needing no morphology at all — is
10.5% of languages but **64.6% of L1**, with Mandarin 被 *bèi* as the model.

> **Had the rejection stood it would have been a 95%-of-L1 override — comfortably the largest
> in the project, ten points larger than the politeness decision — and it would have rested
> on a claim about our own grammar that one Grambank feature refutes.**

This belongs in the audit for two reasons. First, a reader deserves to know the process
caught it. Second, the *failure mode* is nameable and generalises: **reasoning from our own
constraints straight to "therefore impossible" without checking whether the world has a
strategy that fits inside them.** It is the same shape as the "it's ordinary vocabulary"
error in [`grammar-tier3-combination.md`](grammar-tier3-combination.md) §5. Both were caught
by Patrick pushing back, not by the process — which is the honest version of the story.

**The residual concern is sourcing, not strategy.** APiCS 90's "passive without verbal
coding" type — the one nearest our preverbal `self` — is **30 European-lexifier to 1
non-European** in APiCS, and the reflexive→passive grammaticalisation path is Europe-heavy
**[recall, unverified — no source we hold codes it]**. The *strategy* we adopted (a free
preverbal marker) is a 64.6%-of-L1 strategy whose flagship is Mandarin; the *word* we chose
to fill the slot sits near a European pattern. Reusing `self` costs nothing and a dedicated
particle would cost one word and buy no structural difference, so the choice stands — but the
appearance is logged rather than argued away.

### 2.2 The pattern behind the list

[`grammar-tier3-predication.md`](grammar-tier3-predication.md) §6 asked for this to be
reported as a pattern and not only as entries. Four consecutive Tier 2/3 questions were
decided **against the contact record**: Q6 (TAM, taste), Q8 (politeness, against 85% of L1),
Q10 (question particle, against 9 of 9 restricted pidgins), and the adjectival copula
(against 8 of 9). The stated policy that licenses this is
[`grammar-plan.md`](grammar-plan.md) §5 standing rule 6 — *the contact record is evidence
about what emerges, not about what is learnable when taught* — plus Patrick's addition that
*we copy pidgins only where they point at ease of learning.*

**§1.8 is the check on whether that licence was overused, and the answer is no.** Four
departures did not move interlang out of the restricted-pidgin cloud. But the departures are
not evenly distributed: **the TAM decision alone accounts for four of the twelve
worst-agreeing APiCS parameters**, and it is the one to revisit first if the grammar is ever
reopened.

---

## 3. PART 3 — commitments made without ever being chosen

The Tier 3 cleanup found four features being silently assumed, which is reason enough to
treat "what else did we never decide?" as a search rather than a formality. Two methods were
used: the **unmapped-feature scan** (Grambank features with no interlang value are either
genuinely uncodable or things nobody decided) and a **rationale scan** over the encoding
itself, pulling out every feature whose justification is entailment rather than a decision.

**The general shape of the risk, restated:** *a write-up that justifies a decision by appeal
to a feature we have not decided has smuggled that feature in.* Everything below is an
**OPEN** item.

### 3.1 The two that were already known

**(a) Satellite-framing in motion events.** With no derivational affixes, no serial verbs,
and modifiers preceding their head, *manner verb + directional modifier* (`run in`, `climb
up`) is the only construction available. That is Talmy's **satellite-framed** pattern — the
Germanic one — as against the **verb-framed** pattern of Romance, Turkish, Japanese, Korean
and most of the world's larger families, where the path goes into the verb (*entrer*,
*monter*). Flagged in [`lexicon-plan.md`](lexicon-plan.md) §4.5.

**It is not measurable here and the reason is worth stating precisely.** Neither WALS nor
Grambank nor APiCS codes framing typology; Grambank's nearest-looking feature, GB108
("directional or locative morphological marking on verbs"), asks about *bound morphology on
the verb*, which is a different question, and coding our satellite-framing into it would be
exactly the "a feature name is not a feature definition" error this project has already made
twice. **So it is left uncoded and reported as unmeasured** rather than given a spurious
number. **[recall]** for the typology itself; the commitment is a deduction from our own
rules, which is solid.

The practical consequence is a lexicon one: the motion domain needs deliberate attention when
verb roots are chosen. WOLD's Motion field holds 89 concepts at a mean root rate of 0.679,
below the 0.704 average **[measured, `lexicon-plan.md` §4.5]**.

**(b) No topicalization.** Rigid SVO, no fronting, no clefts (rejected in Tier 5 §9), no
focus particle, and content questions in situ. **Information structure has no dedicated
syntactic device.**

**This one *is* partly measurable, and nobody checked.** Grambank GB136 asks whether core
argument order is fixed: **[measured]** fixed in 61.9% of languages but only **46.2% of world
L1** — so **53.8% of the world's people speak a language with flexible core-argument order**,
which is the standard way to topicalise without machinery. That makes "no topicalization" a
~54%-of-L1 commitment that appears in no write-up and was never argued.

**Two mitigations, both real.** The **passive** is an information-structure device — Tier 3
cleanup §2a explicitly says it "recovers the information-structure loss… the patient is now
the grammatical subject and sits in topic position" — and Tier 5 §9's focus adverb
(*specifically*) is a lexical one. So the correct statement is not "no information structure"
but **"exactly one syntactic IS device (the passive) and one lexical one, where most
languages have word order as well."**

### 3.2 The new ones

**(c) Reciprocals — never decided, and there is a collision waiting.** ***OPEN, and the
sharpest of the new findings.***

Q8 gave us one invariant reflexive (`self`) and the Tier 3 cleanup gave `self` a second job
as the preverbal passive marker. **Nothing anywhere says how to express "they see each
other."**

**[measured]** Grambank GB306 (an independent, non-bipartite reciprocal pronoun): 24.2% of
languages but **65.1% of world L1**. APiCS 89, of the 66 contact lects carrying a value:
**only 3 have no reciprocal construction at all**; 26 build one on 'other', 12 use some other
special construction, 9 use the same form as the reflexive, 9 have both, 7 build it on
'companion'. Only 4 of the 9 restricted pidgins carry a value and they split 1/1/1/1 across
'other', other-special, reflexive-identical and none.

**And the obvious cheap answer is not available.** Reusing `self` — what 9 contact languages
do, and what French *se* and Spanish *se* do — makes `they see self` mean both "they see
themselves" and "they see each other". That may be tolerable (the same ambiguity is live in
French). What is *not* tolerable is that `self` is already the passive marker, so the
reflexive/reciprocal/passive triple all hang on one word disambiguated only by position.
**This is the same class of risk as the copula collision in
[`grammar-tier3-predication.md`](grammar-tier3-predication.md) §1: an interaction between our
own decisions that no source can flag, because the evidence base codes features one at a
time.**

*Recommendation for whoever reopens this:* build the reciprocal from `each`+`other` or from
the generic-noun set (Tier 4 §2's fourth reuse pattern), not from `self`. Cost: 0–1 words.

**(d) Intensifiers — never decided.** *I did it **myself***, as against *I saw myself*. APiCS
88, of the 68 lects with a value: intensifier and reflexive are **identical in 26**,
differentiated in 22, overlapping in 13, and 6 have no special reflexive pronoun at all.
English identifies them; many languages do not. We have neither decided nor noticed. Cheap
either way, but it is one more job for `self`.

**(e) Causatives — never decided, and there is no obvious construction.** Tier 0 removed
causative affixes (**[measured]** GB155: causative affixes exist in 72.5% of languages,
48.2% of L1), the Tier 3 cleanup removed serial verbs, and we have no light verbs. **So
"I made him leave" must be periphrastic — a matrix verb plus a clause — and the grammar never
says whether that is well-formed.** With exactly one verb per clause (Tier 4 §1's premise for
the semi-rigid word-class decision) and no non-finite forms (Tier 0), it is not obvious what
`I make he go` even parses as. Compare GB113 (a transitivising affix): 69.8% of languages,
**57.2% of L1**. This is a real gap in the grammar, not a stylistic one.

**(f) Valency alternation / labile verbs — never decided.** **[measured]** GB401 (a class of
patient-labile verbs, *the window broke* / *he broke the window* with no marking): 28.0% of
languages, **41.2% of L1**. We have no anticausative, no transitiviser and no
detransitiviser; the passive covers agent demotion but not the inchoative reading. Whether
every root's transitivity is fixed in the lexicon, or whether roots are labile, is a decision
the lexicon stage will be forced to make and the grammar never made. It is coded 0 in this
audit purely because the passive was adopted to do that job.

**(g) Evidentiality — entailed, never stated.** No grammatical marking of direct or indirect
evidence. Cheap: **[measured]** absent for **95.4%** (GB322) and **79.4%** (GB323) of world
L1. But Q6's "no TAM grammar" never mentioned it and a reader would reasonably ask.

**(h) Light-verb constructions — never decided, and possibly a missed cheap win.**
**[measured]** GB123: verb-adjunct/light-verb constructions (*do a jump*, *take a look*,
Persian and Hindi's dominant verb-formation strategy) exist in 34.7% of languages but
**71.4% of world L1** — the largest by-language/by-people reversal in the unchosen set. It is
coded 0 here only because Tier 4 §1 analyses `water-do` as a *compound*. **If that same
construction were analysed as a light-verb construction instead, the grammar would agree
with 71.4% of humanity on a feature it currently disagrees with, at zero cost.** That is a
labelling question with a real population consequence and it deserves five minutes.

**(i) Clause chaining — never decided.** **[measured]** GB150: 29.0% of languages, **56.8% of
L1**. Coded 0 (we have coordination and subordination). Never argued.

**(j) Extraposed relative clauses — never decided.** **[measured]** GB331: 9.7% of languages,
25.5% of L1. Our rigid order forbids them by implication.

**(k) Demonstrative distance contrasts — never decided.** **[measured]** GB035: three or more
contrasts (*this / that / yon*) in 49.1% of languages but only **26.2% of L1**, so a binary
*this/that* fits 73.8% of the world's people. Cheap, and the default is fine — but Q7 made
the demonstrative do article duty and never said how many demonstratives there are.

**(l) Ideophones — never decided.** **[measured]** GB296: 31.1% of languages, 14.6% of L1.
Lexicon-stage, cheap, but currently unwritten.

### 3.3 A claimed non-measurability that turns out to be false

[`grammar-tier2-np.md`](grammar-tier2-np.md) §6 says: *"no source codes 'adverb position' the
way it codes adjective position, so the parallel is an argument rather than a finding."*

**APiCS 11 codes exactly that** — the order of frequency adverb, verb and object — and it was
not consulted. **[measured]**:

| APiCS 11 | restricted pidgin | expanded pidgin | creole |
|---|---|---|---|
| **Adverb – verb – object** (ours) | **4 of 9** | 2 of 9 | **25 of 54** |
| Verb – object – adverb | 1 | **7 of 9** | 18 |
| Verb – adverb – object | 0 | 0 | 5 |
| other | 2 | 0 | 3 |

The same pattern shows in APiCS 8 (degree word and adjective): **restricted pidgins put the
degree word first 6 to 2, expanded pidgins put it last 1 to 8.**

**So the modifier rule's extension to adverbs is supported by restricted pidgins and by
creoles, and contradicted by the expanded-pidgin stratum** — which
[`grammar-tier2-tam.md`](grammar-tier2-tam.md) §1 calls "usually the right target" for an
auxiliary language. **The decision does not change** (restricted pidgins are the closest
analogue, creoles agree, and consistency with the single modifier rule is worth more than a
7:2 count in the middle stratum) **but the claim that it could not be checked was wrong, and
that is a process finding worth as much as the result.** Same failure mode as §2.1: asserting
that no evidence exists without looking.

**(SOFT — this changes no decision, but the write-up's honest-limits line should be corrected
if these notes are ever revised.)**

### 3.4 What genuinely cannot be measured with the sources we hold

Recorded so that "not measured" is distinguishable from "not checked":

- **satellite- vs verb-framing** of motion events — no database in this repo codes it (§3.1)
- **whether the polar question particle also appears in content questions** — every Grambank
  interrogative feature is scoped to *polar* interrogation
  ([`grammar-tier2-questions.md`](grammar-tier2-questions.md) §5)
- **yes/no answering the fact vs the question's polarity** (Tier 5 §7)
- **proper-name classification** (Tier 5 §14) — APiCS 79/80 code motion to and from named
  places, not classification
- **ellipsis under coordination** (Tier 5 §11)
- **the relative order of stacked preverbal modifiers** — Q9's leftmost-widest scope rule is
  a design decision, and no source codes the relative order of negation and TAM adverbs
- **APiCS 104 (focusing of the noun phrase)** offers no "no dedicated focus construction"
  value, so Tier 5 §9's decision cannot be scored against contact languages at all

---

## 4. Honest limits

Every one of these was known before the run and none is fixed by it.

1. **The encoding is the study, and it is a judgment call.** 187 Grambank features and 65
   APiCS parameters, each mapped by hand. §1.7 measures the sensitivity of the *conclusions*
   to the 18 codings I could see as contestable — but the encodings I did **not** flag are
   invisible to that test, and a different analyst would flag a different 18. Read the
   `rationale` column of `grammar_bias_audit_features.csv` before quoting any single number.

2. **Grambank's coverage is uneven and population-correlated**, which is the failure mode
   that already flipped one conclusion in this project ([`stress-prevalence.md`](stress-prevalence.md)).
   Here it bites concretely: **German, Spanish, Yoruba, Bengali and Persian are not in
   Grambank at all.** Two of those are top-ten languages and one is the nucleus of Standard
   Average European. The SAE nucleus figure rests on four languages.

3. **The by-L1 columns are dominated by a handful of giants.** Sino-Tibetan's 0.825 is
   substantially Mandarin's 918M. Indo-European's 1,893M L1 is spread over 64 Grambank
   languages, most of them small. Any population-weighted mean in this document is really a
   statement about twenty languages.

4. **APiCS is 80% Western-European-lexifier**, leaving **14 independent
   non-European-lexifier languages** as the real sample behind any claim of a contact-language
   universal ([`grammar-plan.md`](grammar-plan.md) §3.3). The "non-European lexifiers score
   highest" finding in §1.8 rests on **7 lects**. It points the right way; it is not strong.

5. **The restricted-pidgin stratum is 9 languages**, as everywhere in this project, and the
   §1.8 verdict — the most quotable result in this document — rests on those 9 plus a
   within-stratum null computed from at most 36 pairs.

6. **The contact-type stratification is hand-assembled** from standard creolistics
   (`model-recall` provenance), and the expanded/creole boundary is genuinely contested — Tok
   Pisin, Bislama and Nigerian Pidgin could be typed either way. The monotonic gradient in
   §1.8 would survive a few reclassifications; the exact numbers would move.

7. **Agreement over a feature vector is a crude similarity measure.** It treats all features
   as independent and equally important, which they are not: the ~15 Grambank features that
   are all consequences of "no affixes" effectively vote fifteen times. That inflates
   similarity to other isolating languages and deflates it to synthetic ones. **A
   feature-clustered or PCA-based measure would be the right fix and was not attempted.** The
   direction of the bias is known and it runs *toward* the conclusion drawn in §1.3, so the
   MSEA finding should be read as "at most this strong".

8. **The all-zero baseline is close** (0.665 vs 0.693 by language). A sceptic can reasonably
   say that much of interlang's Grambank agreement is bought by having nothing rather than by
   having the right things. The by-L1 column (0.643 vs 0.718) is the better answer to that,
   and the APiCS run — where there is no "all-zero" to hide behind, because every parameter is
   a choice among constructions — is the best one.

9. **North America's by-L1 agreement (0.787) is a creole artefact**, as §1.4 says. It is left
   in the table because deleting it would be worse, but it should never be quoted alone.

10. **Reduplication (GB158/GB159) is encoded as present**, following
    [`lexicon-plan.md`](lexicon-plan.md) §6, which **adopted it after the grammar closed** and
    tagged it SOFT. If it were dropped, two encodings change. Both are in the contested set.

11. **This audit does not measure learnability**, which is the actual objective. It measures
    *typological position*. "Close to Mandarin" is not the same claim as "easy for Mandarin
    speakers", and nothing here licenses the second.

---

## 5. What this decides, and what it opens

**FIRM (measured, survives the sensitivity run):**

- **This grammar is not Standard Average European.** SAE sits at the 41st percentile of
  similarity to interlang; 59% of the world's languages are closer to it than the average
  European language is. The `grammar-plan.md` §1 worry was not realised.
- **It is a Mainland-Southeast-Asian-shaped isolating language.** Its nearest relatives are
  Austroasiatic, Tai-Kadai, Hmong-Mien and Chamic; its nearest large language is **Mandarin
  (0.840, 97th percentile)**; its furthest are the Sudanic and Amazonian families with rich
  case and agreement.
- **It fits Africa worst** — the lowest macroarea on both the by-language and the by-people
  column, and 9 points below Eurasia by population.

**SOFT (measured, but on thin samples or contestable coding):**

- **It landed where it was aimed.** On APiCS's 65 parameters interlang agrees with restricted
  pidgins at 0.531 against a restricted-pidgin-to-restricted-pidgin null of 0.517 — an
  ordinary member of that population — while sitting clearly outside the creole cloud (0.457
  vs 0.526). n=9 in the deciding stratum.
- **The largest single departure from the contact record is the TAM decision**, which
  accounts for four of the twelve worst-agreeing APiCS parameters, and which the project had
  already recorded as taste rather than evidence. If the grammar is reopened, reopen that
  first.
- **The population cost is 32 of 187 features**, concentrated in the no-affix and no-TAM
  decisions rather than in the individually-argued overrides. The worst single feature is the
  **free plural word (10.8% of L1)**, a consequence nobody debated.

> **Framing note (Patrick, 2026-08-06).** The free plural word should be
> **de-emphasised** in how this result is presented. We were never going to add a grammar
> rule purely for plurals, so some cost here was unavoidable — and the language already
> expresses number perfectly well with `one cat`, `two cat`, `many cat`. The gap is therefore
> **something missing rather than something unfamiliar imposed**, which is a materially easier
> thing for a learner to absorb than an alien obligatory category. Report it, but not as the
> headline cost.


**OPEN (§3 — decisions the grammar needs and has never taken):**

1. **Reciprocals**, and the `self` overload they collide with — the sharpest of these.
2. **Causatives**: no affix, no serial verb, no light verb, and no stated periphrastic
   construction.
3. **Valency / labile verbs**: is transitivity fixed per root?
4. **Intensifiers** (*I did it myself*).
5. **Light-verb constructions** — currently coded absent by a labelling choice, at a cost of
   71.4% of world L1, possibly recoverable for free.
6. **Clause chaining**, **extraposed relatives**, **demonstrative distance contrasts**,
   **ideophones**, **evidentiality** — all entailed rather than decided, all cheap, all
   currently unwritten.
7. **No topicalization** stands as a ~54%-of-L1 commitment nobody argued, mitigated by the
   passive and the focus adverb but not eliminated.

**And one correction to the record (§3.3):** [`grammar-tier2-np.md`](grammar-tier2-np.md) §6
says adverb position is not coded by any source. **APiCS 11 codes it**, and it supports the
decision in restricted pidgins and creoles while contradicting it in expanded pidgins. The
decision stands; the claim of non-measurability does not.
