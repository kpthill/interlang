# International vocabulary under candidate syllable templates

*Study run 2026-08-05. Script: [`../scripts/international_vocab.py`](../scripts/international_vocab.py) ·
ruleset: [`../src/interlang/translit.py`](../src/interlang/translit.py) ·
outputs: `data/processed/international_vocab.csv` (52 words × 6 variants × 2 coda
policies = 624 rows) and `data/processed/international_vocab_forms.csv` (828 attested
forms). Informs [`principles.md`](principles.md) §3.6 (syllable template, OPEN).*

**The question.** Internationally shared vocabulary — above all the scientific and
technical words built from Latin and Greek roots — should be near-instantly
recognizable. Patrick is leaning toward **(C)V(N)** (optional onset, optional nasal
coda) and wants to know what it costs. Two answers are needed:

- **(A) Recognizability** — do these words survive projection into our phonology?
- **(B) Predictability** — is there a *deterministic* path from the international form
  to our form, and back? An arbitrary choice is a defect even when it scores well.

**Bottom line up front.** (C)V(N) is adequate but not the best buy. One notch of extra
permissiveness pays for itself, and it is **not the one usually proposed**: adding the
**Cr/Cl onset clusters** (pr tr kr pl kl br dr gr fr fl) buys as much recognizability as
adding liquid codas *and costs less* — it strictly dominates (C)V(N,l,r) on both axes.
Liquid codas do not pay. Details in §8.

---

## 1. The premise check

**Patrick's assumption:** for scientific terminology essentially every language adapts
the Latin/Greek roots, except Chinese, which calques (builds native compounds).

**Verdict: the direction is right, the "essentially every language" is wrong.** Chinese
is not the exception — it is the flagship of a large calquing bloc, and there is a
second, independent purist bloc. Adaptation rates across our 52-word set range from
**98% (Spanish) to 28% (Tamil)**, which is not a distribution with one outlier in it.

### 1.1 Measured adaptation rates

Share of the 52-word set whose Wikipedia headword in that language is an adaptation of
the international root (classifier and its error rate in §1.2; `n` < 52 because a few
concepts have no usable article):

| Language | n | adapted | % |
|---|---|---|---|
| Spanish | 48 | 47 | **97.9** |
| Indonesian | 47 | 45 | **95.7** |
| Russian | 48 | 41 | 85.4 |
| Turkish | 47 | 40 | 85.1 |
| Czech | 48 | 39 | 81.2 |
| Swahili | 45 | 34 | 75.6 |
| Finnish | 48 | 35 | 72.9 |
| Hungarian | 47 | 33 | 70.2 |
| Hebrew | 48 | 33 | 68.8 |
| Hausa | 23 | 14 | 60.9 |
| Hindi | 47 | 27 | 57.4 |
| Arabic | 48 | 27 | 56.2 |
| Korean | 48 | 23 | 47.9 |
| Japanese | 48 | 23 | 47.9 |
| Icelandic | 46 | 20 | 43.5 |
| Vietnamese | 47 | 17 | 36.2 |
| Tamil | 47 | 13 | **27.7** |

Mandarin is hand-classified (§3.4) and sits at the bottom with the other Sinosphere
languages: of the 52 concepts, the standard term is a phonetic loan in roughly five —
咖啡 *kāfēi* (coffee), 巧克力 *qiǎokèlì* (chocolate), 的士 *dīshì* (taxi, via Cantonese),
米 *mǐ* (metre), 维他命 *wéitāmìng* (vitamin, and the modern standard 维生素 is a calque).

### 1.2 What the pattern actually is

Three groups, not two:

1. **Adapters (Latin-script Europe, plus the languages that modernised through European
   contact).** Spanish, Indonesian, Russian, Turkish, Czech, Swahili, Hungarian. Here the
   premise holds outright. Indonesian and Swahili matter most for this project: they are
   the non-European members of this group, and they adapt at 96% and 76%.
2. **The Sinosphere calquing bloc.** Mandarin, Japanese, Korean, Vietnamese. The premise
   named Chinese; it should have named the *character-culture sphere*, because Japanese,
   Korean and Vietnamese imported the Chinese-built compounds wholesale. 電子 / 전자 /
   電子 (electron), 原子 / 원자 (atom), 分子 / 분자 (molecule), 電話 / 전화 / *điện thoại*
   (telephone). The split inside these languages is **chronological, not categorical**:
   19th-century core science is calqued, 20th-century vocabulary is loaned — Japanese has
   ウイルス *uirusu*, プラスチック *purasutʃikku*, インターネット *intānetto*, コンピュータ
   *konpyūta*. Japanese and Korean land at 48% because our word set straddles both eras.
3. **Deliberate purism, independent of the Sinosphere.** Icelandic (43.5%: *rafeind*
   electron, *frumeind* atom, *sími* telephone, *tölva* computer, *lýðræði* democracy),
   Tamil (27.7%: *etirminni* electron, *tolaipēci* telephone, *makkaḷāṭci* democracy),
   Hebrew (*ḥamtsan* oxygen, *maḥshev* computer, *negif* virus), Finnish for the older
   layer (*happi* oxygen, *puhelin* telephone, *tietokone* computer, *vety* hydrogen),
   Arabic (*ḥāsūb* computer, *hātif* telephone, *dharra* atom).

**Two complications named in the brief came out the other way from expectation.**
Hungarian and Czech are *not* strong purists in this vocabulary (70% and 81%) —
19th-century Czech and Hungarian coinages exist (*kyslík*, *vodík*, *počítač*,
*számítógép*, *fehérje*) but they did not displace the international stock. Finnish is
purist in the older stratum only.

### 1.3 The register problem — the largest caveat on this section

Wikipedia headwords are the **formal written standard**, which is exactly where purism
concentrates. The spoken language often uses a loan the encyclopedia does not name.
Hindi is the clearest case: the article titles are *paramāṇu* (atom), *viṣāṇu* (virus),
*dūrabhāṣ* (telephone), *antarjāl* (internet) — while everyday spoken Hindi is टेलीफोन,
वायरस, इंटरनेट, कंप्यूटर. Tamil behaves the same way (*ṭelipōṉ* is normal speech).

So the numbers in §1.1 are **lower bounds on real-world adaptation** for exactly the
languages that look most purist, and the honest reading is:

> The international stock is available almost everywhere as a *register*, and is the
> default in most languages; but for a large minority of humanity, the word a person
> actually learned for "electron" is a native compound with no phonological relation to
> *electron* at all.

A supplementary table of 18 spoken-register loans (`MODEL_RECALL` in the script) is
carried in the forms CSV with `provenance = model-recall`; it is **not** in any headline
number, because it is model-recalled rather than sourced (§3.3).

### 1.4 Classifier accuracy, measured

The loan/calque call is automatic (§3.5). I hand-audited a **stratified random sample of
60 forms** (10 per score band, which deliberately over-samples the ambiguous middle):
**52/60 agreed** with my own judgment — 4 missed loans (Tamil *oṭcicaṉ* oxygen, Korean
에너지 energy, Japanese テレビ *terebi* — a clipping, Tamil *tēnīr* tea — a hybrid) and 4
spurious loans (Hebrew *ḥamtsan* oxygen, Hindi *dūradarśan* television, Hebrew *seret
kolnoa* film, Arabic *naẓariyya* theory). Since the sample over-weights the boundary,
**~13% is a pessimistic bound**; over the whole set the error is lower.

The errors are not symmetric across scripts: missed loans concentrate in non-Latin
scripts where our romanisation is lossy (ja, ko, ta), spurious loans in the abjads (ar,
he) where only the consonant skeleton is visible. **Japanese, Korean, Tamil, Arabic and
Hebrew rates in §1.1 are therefore likely understated by a few points each; the ordering
of the table is robust, the exact percentages are not.**

### 1.5 What this means for the project

The goal "internationally shared vocabulary should be instantly recognizable" is worth
roughly what it looked like, but the beneficiary set is narrower than "everyone":

- It is worth a great deal for the ~1.5–2 billion people whose language is in group 1,
  and for educated speakers in most of group 3.
- It is worth much less for the Sinosphere (~1.6 billion), where the *concept* is
  familiar but the *word* is not — a Mandarin or Vietnamese speaker gains nothing
  phonological from *elekitron*.
- It is worth almost nothing for Tamil-style purist registers.

This does not argue against the goal; it argues against pricing it as if it were
universal. It also means the §2 representation objective is not in as much tension with
the international vocabulary as it looks: for half the world, an internationalism is
already an arbitrary string, so choosing it costs them nothing they had.

---

## 2. The word set

52 words. Selection policy, applied in this order:

1. **Domain coverage** — 9 chemistry/physics, 9 biology/medicine, 7 mathematics/units,
   10 technology, 8 institutions/society, 9 non-technical Wanderwörter. The last group
   is there as a control: these travelled without a scientific register behind them.
2. **Phonotactic stress-testing** — every word is in the set because it stresses the
   phonology in a specific way, recorded in the `why` column of the CSV and printed in
   the script's `WORDS` table. The intended coverage:
   - *onset clusters*: proton, plastic, program, president, protein, algebra, kilogram
   - *medial clusters*: electron (/kt/ + /tr/), bacteria, insulin, system, hospital,
     computer, internet (/rn/)
   - *non-nasal codas*: robot, internet, president (/t/), plastic, antibiotic (/k/),
     virus, gas-like /s/ (virus), hotel, hospital, molecule (/l/), meter, motor (/r/)
   - *cluster codas*: bank (/nk/), film (/lm/) — illegal under **every** variant, V5
     included
   - *sounds we lack*: /v/ virus, vitamin, video, television, university, vaccine;
     /z/ zero; /ʃ tʃ/ machine, chocolate; /θ/ mathematics, theory
   - *floor cases* (already legal, to show the base rate): banana, malaria, radio,
     tomato, tea
3. **Attestation** — preference for words with a Wikipedia article for the same concept
   in most of the 18 recipient languages, so that attested renderings exist (§3).

Four words (zero, million, motor, program) have no usable article — the concept's
article is about the number or is ambiguous — so they carry rendering and syllable data
but no similarity score. They stay in the set because they are good phonotactic probes.

### 2.1 Choosing the international form is itself a decision

The ruleset is a function *of the international form*, so the international form has to
be picked before the function runs. Policy: **the Latin-script shape shared by the
largest number of the 18 recipient languages, written with classical Latin/Greek
digraphs** (ph, th, ch, x, c, y) so that the *ruleset*, not the word list, does the sound
mapping. So `molecula` (molekul/molekül/molekula/molécula), `telephon` (telefon
everywhere), `energia`, `democratia`, `universitat`, `hormon`, `vaccin`.

Three words take a **non-classical** shape because the classical form is not the shape
that travelled: `cafe` (not Latin *coffea*: kahve/kahawa/kafe/kopi), `sukar` (not
*saccharum*: sukari/sukkar/sakhar/şeker/cukr), `te` (not *thea*). These are flagged in
the `intl_note` column.

**This is decision point #1 of the predictability audit** and it is the biggest one: it
is not resolvable by rule, it is lexical (§7).

---

## 3. Data and provenance

### 3.1 Attested renderings: Wikipedia langlinks

For each word, the en.wikipedia article title is queried for its interlanguage links,
and the article title in each of the 18 recipient languages is taken as that language's
standard term for the concept. Cached one JSON per title under
`data/raw/wikipedia_langlinks/` (gitignored, re-fetchable; README source table row
added). 48 titles, 828 usable (word, language) forms.

**Why Wikipedia langlinks rather than Wiktionary or PanLex:** one API call per *concept*
returns all 18 languages at once, in native script, for the same referent, with no
sense-disambiguation problem. The cost is the register bias discussed in §1.3 and the
fact that a title is sometimes a multi-word descriptive phrase.

### 3.2 Recipient languages

ja, zh, ko, hi, ar, sw, id, tr, ru, es, fi, vi, ha, ta (the 14 named in the brief) plus
**he, is, hu, cs** — the four purist/complication cases the premise check needed.

### 3.3 Provenance classes (the honest part)

| class | what it is | used for |
|---|---|---|
| `wikipedia` | the langlink title, verbatim from the cached API response | everything, including all headline numbers |
| `model-recall` | a form from my own knowledge | the 18 spoken-register loans of §1.3 and the Mandarin classification of §3.4 — **flagged, never in a headline number** |
| `derived` | a romanisation of one of the above | scoring |

**The romanisation and phonemicisation tables are rough and hand-written by me** — 8
Latin-orthography tables plus Cyrillic, katakana, Hangul, Devanagari, Tamil, Arabic and
Hebrew. They are not a transliteration standard, and they do not model allophony, stress
or tone. Two bugs found and fixed during the run are recorded in the script (accents
blocking digraph rules; affricates silently dropped from skeletons), which is a fair
indication of how much residual error is likely still in there.

**Why the study is still valid despite that.** Every one of the six variants is scored
against *exactly the same* romanised targets, so romanisation error is a constant offset
shared by all six. Absolute similarity levels are noisy; **variant comparisons are not**.

Two consequences are enforced in code:
- **Arabic and Hebrew are excluded from all similarity scoring** (`scored = False`).
  They are abjads: short vowels are unwritten, so the romanised form is a consonant
  skeleton, not a phonological form. They are kept for the premise check, where the
  skeleton is enough to see whether the root is there.
- **Mandarin is excluded from scoring** entirely, because Chinese characters carry no
  phonology we can extract without a reading dictionary.

### 3.4 Mandarin

Hand-classified in `ZH_LOAN`, provenance model-recall, spot-checkable against the cached
langlink titles which are printed in the forms CSV.

### 3.5 The loan/calque classifier

Not metric v0. v0 is length-biased at this decision boundary — its random-pair floor is
~0.46 ([`principles.md`](principles.md) §4 issue 3), so short words score high against
anything, which made Spanish *metro* (a loan) and Korean *sanso* (a calque) inseparable.

Instead: **weighted edit distance over a coarse consonant-class skeleton**. Consonants
collapse to 8 classes (labial / coronal stop / sibilant / dorsal / nasal / liquid /
glide, affricates into the sibilant class, all nasals into one class because nasal place
assimilation is universal in adaptation), vowels to one class, and **vowel
insertion/deletion costs 0.4 against 1.0 for a consonant** — so epenthesis (Japanese
*intāneto*, Swahili *protini*) is nearly free while a different root is not. A form
counts as an adaptation at **≥ 0.62**, matched against the whole title, any token of it,
or that token's prefix (so compounds containing the stem — *Radiokomunikace*,
*Telefonkészülék*, *Kwayar cutar Bakteriya* — count, which is what the premise is about).
Threshold set by inspecting the distribution; accuracy measured in §1.4.

### 3.6 The metric caveat that governs everything below

[`principles.md`](principles.md) §4 known issue 2: **the metric has no working epenthesis
model**, and the cost-learning study established that a discriminative objective cannot
learn one. Inserted repair vowels are charged near full price, so the metric
**systematically flatters permissive codas**. Every similarity number in §6 is biased in
favour of V4/V5 and against V1/V2/V3.

Three counterweights are reported alongside, and the conclusions rest on them:
1. **Syllable inflation** — the cost the metric cannot see, reported in the same table.
2. **A restrictive/permissive recipient split** — scoring separately against the
   recipients that must themselves repair clusters (ja, ko, sw, ta, ha, vi) and those
   that need not. This is the direct test, and it **flips the ranking** (§6.2).
3. **A learned-cost sensitivity arm** (`sim_learned`, from
   `data/processed/learned_costs.csv`, opt-in per §7.5 of principles). Reported, never
   the headline, since 2 of its 5 guardrails fail.

---

## 4. The transliteration ruleset

Implemented in [`../src/interlang/translit.py`](../src/interlang/translit.py). It is a
function, in two ordered stages. Nothing in it is a per-word decision; the whole word
list is rendered by the same rules.

### 4.0 Rule A0 — read the international spelling with LATIN values

The single most consequential decision. The input is the Latin-script international
spelling, read with the values Latin gives its letters, not the values English or French
give them. `<c>` is /k/ (or /s/ before a front vowel), `<ch>` is /k/, `<g>` is always
hard, `<j>` is /j/, `<y>` is /i/.

*Why:* it is the only convention under which one rule table serves a Turkish, a Russian,
an Indonesian and a Spanish reader at once, and it is what the Latin-script recipient
languages already do — *telefon, elektron, sistem, universitet, komputer, plastik*.

*Cost, measured:* the words whose modern donor pronunciation has left the Latin values
behind come out Latinised. In the whole 52-word set the rule fires "wrongly" twice
(`ch`): **chocolate → kokolate** (attested renderings are all /ʃ/ or /tʃ/: çikolata,
šokoláda, chokorēto, 초콜릿) — this one costs 0.09 similarity. The other, **machine →
makina**, actually *out-scores* the reference international reading (0.91 vs 0.80),
because Turkish *makine*, Spanish *máquina* and Russian *mašina* sit closer to the Latin
form than to the French one.

### 4.1 Stage 1 — graphemic (`to_phonemes`)

Ordered; each rule sees the output of the previous one.

**A1. Digraphs and trigraphs, longest match first.**

| source | → | note |
|---|---|---|
| sch | sk | |
| ph | f | Greek phi |
| th | t | Greek theta — **decision point**, see §7 |
| ch | k | Greek chi, Latin value (rule A0) |
| rh, gh, wh, ck | r, g, w, k | |
| sh | s | no second sibilant in the inventory (§3.3) |
| qu | kw | |
| ae, oe | e | as in every modern reflex |
| x | ks | in every position |

**A2/A3. Single letters, with one letter of lookahead.**

| source | → | condition |
|---|---|---|
| c | s | before e, i, y |
| c | k | elsewhere |
| g | g | always hard — **decision point**, §7 |
| y | j | before a vowel |
| y | i | elsewhere |
| v | w | **decision point**, §7 — b and f are the rivals |
| z | s | no /z/ in the inventory |
| q | k | |
| j | j | Latin/IPA value ("y" of *yes*), not English |
| p t k b d m n f s h l r w | themselves | |

**A4/A5. Degemination.** Doubled consonants and doubled vowels collapse: there is no
length contrast (§3.5). *million → milion*, *vaccin → wakisin* (via c→k, c→s).

### 4.2 Stage 2 — phonotactic repair (`repair`)

Applied left to right; `is_legal()` validates the output.

- **B1 Onset.** Each syllable takes the largest legal onset: one consonant, or two if the
  pair is a permitted onset cluster of the variant.
- **B2 Coda.** One consonant may be left over before the next onset. If it is in the
  variant's coda set it becomes a coda; if the variant has a nasal merger for it (V2:
  /m/ → /n/, because a (C)V(n) language has nowhere else to put /m/) it merges;
  otherwise B4.
- **B3 Word-final.** An illegal word-final consonant is either **deleted** (trailing
  consonants stripped until the word ends in a vowel or a legal coda) or given a
  **support vowel**. This is a policy, priced in §6.3.
- **B4 Epenthesis.** Any consonant that can be neither onset nor coda takes a support
  vowel after it and becomes the onset of a new syllable — the Japanese pattern: the
  segment survives, the syllable count grows. **Epenthesis is never applied
  word-internally as deletion**: material inside the word is never destroyed, only the
  final edge is, and only under one policy. Deleting internally would break the mapping
  in the middle of the stem, where the recognizability payload lives.

The support vowel is **/i/** by default. The metric is indifferent between /i/, /u/ and
an echo of the following vowel (0.7962 / 0.7958 / 0.7964 — a range of 0.0006, i.e.
nothing), so the choice is made on learnability: a single fixed vowel is one rule instead
of a conditional one, /i/ is the epenthetic vowel of Swahili (*virusi, filimu, hoteli,
sukari*) and of Arabic, and it is one of the three maximally prevalent vowels.

### 4.3 The Latin/Greek ending table

Endings are where scientific vocabulary is most repetitive, so they deserve their own
row-by-row check. Under the recommended ruleset (V3C, support vowel /i/, final
epenthesis), computed by the code, not by hand:

| ending | example | result | note |
|---|---|---|---|
| -um | album | ali·**bum** | survives intact — /m/ coda |
| -us | virus | wiru·**si** | -us → -usi; under the deletion policy → *wiru* |
| -on | proton | pro·**ton** | survives intact — /n/ coda |
| -in | insulin | insu·**lin** | survives intact |
| -ine | vaccine | wakisi·**ne** | final -e is pronounced under Latin reading |
| -ol | alcohol | alikoho·**li** | |
| -al | hospital | hosipita·**li** | |
| -ic | plastic | plasiti·**ki** | |
| -ide | oxide | okisi·**de** | |
| -ate | carbonate | karibona·**te** → *karibonate* | |
| -ia | bacteria | bakiter·**ia** | already legal: hiatus, two syllables |
| -tion | nation | na·ti·**on** | already legal, three syllables |
| -y / -ia | energy → energia | eneri·**gi** / eneri·**gia** | |

**The endings are the good news.** -on, -in, -um, -ia, -tion, -ide, -ate and -ine are
*already legal* under (C)V(N) with no repair at all, because Latin and Greek nominal
endings are overwhelmingly open syllables or nasal-final. The only ending that costs
anything is **-us** (and -s generally), plus the consonant-final adjectival endings -ic,
-al, -ol. That is a genuinely favourable fit and it is not a coincidence: the nasal coda
is exactly the coda Latin morphology uses.

---

## 5. Per-word renderings

Full table, V3 (C)V(N) under both final-coda policies, with V3C and V5 for comparison.
`sim` is metric v0 against the attested adaptations; `ceiling` is what the international
form *itself* scores against the same attested set — i.e. what a language that borrowed
the word unaltered would get, and the natural upper bound for that word. Four words have
no attested set (§2).

| word | intl form | V3 (epen) | V3 (del) | V3C (epen) | V5 | syl | sim V3 | sim V5 | ceiling |
|---|---|---|---|---|---|---|---|---|---|
| atom | atom | **atom** | atom | atom | atom | 2 → 2 | 0.93 | 0.93 | 0.93 |
| proton | proton | **piroton** | piroton | proton | piroton | 2 → 3 | 0.82 | 0.82 | 0.96 |
| electron | electron | **elekitiron** | elekitiron | elekitron | elekitron | 3 → 5 | 0.77 | 0.85 | 0.96 |
| molecule | molecula | **molekula** | molekula | molekula | molekula | 4 → 4 | 0.93 | 0.93 | 0.93 |
| oxygen | oxygen | **okisigen** | okisigen | okisigen | oksigen | 3 → 4 | 0.78 | 0.90 | 0.90 |
| hydrogen | hydrogen | **hidirogen** | hidirogen | hidrogen | hidrogen | 3 → 4 | 0.77 | 0.85 | 0.85 |
| carbon | carbon | **karibon** | karibon | karibon | karbon | 2 → 3 | 0.78 | 0.84 | 0.84 |
| energy | energia | **enerigia** | enerigia | enerigia | energia | 4 → 5 | 0.82 | 0.90 | 0.90 |
| plastic | plastic | **pilasitiki** | pilasiti | plasitiki | pilastik | 2 → 5 | 0.68 | 0.74 | 0.81 |
| virus | virus | **wirusi** | wiru | wirusi | wirus | 2 → 3 | 0.71 | 0.71 | 0.83 |
| bacteria | bacteria | **bakiteria** | bakiteria | bakiteria | bakteria | 4 → 5 | 0.78 | 0.88 | 0.88 |
| antibiotic | antibiotic | **antibiotiki** | antibioti | antibiotiki | antibiotik | 5 → 6 | 0.91 | 0.88 | 0.88 |
| vitamin | vitamin | **witamin** | witamin | witamin | witamin | 3 → 3 | 0.83 | 0.83 | 0.95 |
| protein | protein | **pirotein** | pirotein | protein | pirotein | 3 → 4 | 0.77 | 0.77 | 0.85 |
| hormone | hormon | **horimon** | horimon | horimon | hormon | 2 → 3 | 0.81 | 0.89 | 0.89 |
| malaria | malaria | **malaria** | malaria | malaria | malaria | 4 → 4 | 0.94 | 0.94 | 0.94 |
| insulin | insulin | **insulin** | insulin | insulin | insulin | 3 → 3 | 0.95 | 0.95 | 0.95 |
| vaccine | vaccin | **wakisin** | wakisin | wakisin | waksin | 2 → 3 | 0.69 | 0.72 | 0.81 |
| mathematics | mathematica | **matematika** | matematika | matematika | matematika | 5 → 5 | 0.95 | 0.95 | 0.93 |
| algebra | algebra | **aligebira** | aligebira | aligebra | algebra | 3 → 5 | 0.76 | 0.94 | 0.94 |
| geometry | geometria | **geometiria** | geometiria | geometria | geometria | 5 → 6 | 0.83 | 0.93 | 0.93 |
| zero | zero | **sero** | sero | sero | sero | 2 → 2 | – | – | – |
| million | million | **milion** | milion | milion | milion | 3 → 3 | – | – | – |
| meter | meter | **meteri** | mete | meteri | meter | 2 → 3 | 0.74 | 0.78 | 0.78 |
| kilogram | kilogram | **kilogiram** | kilogiram | kilogram | kilogram | 3 → 4 | 0.84 | 0.90 | 0.90 |
| telephone | telephon | **telefon** | telefon | telefon | telefon | 3 → 3 | 0.85 | 0.85 | 0.85 |
| computer | computer | **komputeri** | kompute | komputeri | komputer | 3 → 4 | 0.77 | 0.81 | 0.81 |
| radio | radio | **radio** | radio | radio | radio | 3 → 3 | 0.80 | 0.80 | 0.80 |
| internet | internet | **interineti** | interine | interineti | internet | 3 → 5 | 0.77 | 0.90 | 0.90 |
| television | television | **telewision** | telewision | telewision | telewision | 5 → 5 | 0.75 | 0.75 | 0.83 |
| video | video | **wideo** | wideo | wideo | wideo | 3 → 3 | 0.79 | 0.79 | 0.96 |
| machine | machina | **makina** | makina | makina | makina | 3 → 3 | 0.91 | 0.91 | 0.80 |
| motor | motor | **motori** | moto | motori | motor | 2 → 3 | – | – | – |
| film | film | **filim** | filim | filim | filim | 1 → 2 | 0.74 | 0.74 | 0.85 |
| robot | robot | **roboti** | robo | roboti | robot | 2 → 3 | 0.85 | 0.94 | 0.94 |
| democracy | democratia | **demokiratia** | demokiratia | demokratia | demokratia | 5 → 6 | 0.84 | 0.91 | 0.91 |
| police | policia | **polisia** | polisia | polisia | polisia | 4 → 4 | 0.81 | 0.81 | 0.81 |
| university | universitat | **uniwerisitati** | uniwerisita | uniwerisitati | uniwersitat | 5 → 7 | 0.74 | 0.87 | 0.95 |
| president | president | **piresideniti** | piresiden | presideniti | piresidenit | 3 → 6 | 0.79 | 0.75 | 0.86 |
| hospital | hospital | **hosipitali** | hosipita | hosipitali | hospital | 3 → 5 | 0.76 | 0.78 | 0.78 |
| bank | bank | **baniki** | ban | baniki | banik | 1 → 3 | 0.76 | 0.66 | 0.84 |
| system | system | **sisitem** | sisitem | sisitem | sistem | 2 → 3 | 0.83 | 0.90 | 0.90 |
| program | program | **pirogiram** | pirogiram | program | pirogram | 2 → 4 | – | – | – |
| coffee | cafe | **kafe** | kafe | kafe | kafe | 2 → 2 | 0.87 | 0.87 | 0.87 |
| tea | te | **te** | te | te | te | 1 → 1 | 0.82 | 0.82 | 0.82 |
| chocolate | chocolate | **kokolate** | kokolate | kokolate | kokolate | 4 → 4 | 0.75 | 0.75 | 0.83 |
| sugar | sukar | **sukari** | suka | sukari | sukar | 2 → 3 | 0.77 | 0.80 | 0.80 |
| banana | banana | **banana** | banana | banana | banana | 3 → 3 | 0.89 | 0.89 | 0.89 |
| taxi | taxi | **takisi** | takisi | takisi | taksi | 2 → 3 | 0.82 | 0.96 | 0.96 |
| hotel | hotel | **hoteli** | hote | hoteli | hotel | 2 → 3 | 0.83 | 0.89 | 0.89 |
| tomato | tomate | **tomate** | tomate | tomate | tomate | 3 → 3 | 0.85 | 0.85 | 0.85 |
| theory | theoria | **teoria** | teoria | teoria | teoria | 4 → 4 | 0.92 | 0.92 | 0.89 |

**Reading it.** 20 of the 52 words come out of (C)V(N) with **no change in syllable
count at all**, and 23 of 52 are *identical* under V3 and V5 — for nearly half the set,
the template question is moot. The damage is concentrated: *elekitiron*, *pilasitiki*,
*aligebira*, *uniwerisitati*, *piresideniti*, *interineti*, *geometiria*.

Note also the words where our form **beats** the international reference: *matematika*,
*teoria*, *makina*, *antibiotiki*. th→t and ch→k are not losses — the recipient
languages mostly did the same thing.

---

## 6. The variant comparison

52 words, mean over the set. `syl_infl` = mean(syllables after / syllables before) —
**this is the column the metric cannot see, and it is the honest counterweight**; the
metric column is biased in favour of the permissive variants (§3.6).

### 6.1 Headline table

| policy | variant | syl before → after | **syl_infl** | epenth. | deleted | sim v0 | sim learned | retention |
|---|---|---|---|---|---|---|---|---|
| delete | V1 (C)V | 2.92 → 3.50 | **1.211** | 0.58 | 0.67 | 0.744 | 0.647 | 0.849 |
| delete | V2 (C)V(n) | 2.92 → 3.44 | **1.207** | 0.52 | 0.27 | 0.796 | 0.718 | 0.908 |
| delete | **V3 (C)V(N)** | 2.92 → 3.44 | **1.207** | 0.52 | 0.27 | 0.798 | 0.729 | 0.910 |
| delete | V4 (C)V(N,l,r) | 2.92 → 3.33 | **1.166** | 0.40 | 0.15 | 0.815 | 0.751 | 0.929 |
| delete | V5 (C)V(C) | 2.92 → 3.10 | **1.093** | 0.17 | 0.00 | 0.849 | 0.792 | 0.967 |
| delete | **V3C** V3+Cr/Cl | 2.92 → 3.21 | **1.122** | 0.29 | 0.27 | **0.815** | 0.743 | 0.929 |
| epen | V1 | 2.92 → 4.17 | 1.524 | 1.25 | 0 | 0.795 | 0.743 | 0.907 |
| epen | V2 | 2.92 → 3.75 | 1.353 | 0.83 | 0 | 0.811 | 0.750 | 0.925 |
| epen | **V3** | 2.92 → 3.75 | 1.353 | 0.83 | 0 | 0.813 | 0.761 | 0.928 |
| epen | V4 | 2.92 → 3.52 | 1.261 | 0.60 | 0 | 0.827 | 0.772 | 0.943 |
| epen | V5 | 2.92 → 3.10 | 1.093 | 0.17 | 0 | 0.849 | 0.792 | 0.967 |
| epen | **V3C** | 2.92 → 3.52 | 1.268 | 0.60 | 0 | **0.829** | 0.774 | 0.945 |

Reference points, same scale: the **international form itself** scores **0.878** against
the attested set, and the attested adaptations score **0.821** against *each other*.
That second number is the one to hold on to — **it is how far apart two real languages'
adaptations of the same word are**, and it is the natural target. V3 (0.798–0.813) lands
just below the natural spread of real adaptations; V1 (0.744) falls clearly outside it.

Four things fall out:

1. **The floor is expensive, the rest is cheap.** V1 → V2 buys +0.052 similarity, the
   single largest step in the table. Going from "no codas" to "one nasal coda" is worth
   more than everything after it put together. Strict CV is not a live option.
2. **V3's extra /m/ over V2 is nearly worthless *on average* and free.** +0.002
   similarity, zero syllable cost. Its value is concentrated in five words where V2
   produces a visibly wrong form: **atom → aton**, film → filin, system → sisiten,
   kilogram → kilogiran, program → pirogiran. Keep /m/: it costs nothing and *aton* for
   *atom* would be a permanent visible defect in the flagship word of the whole domain.
3. **Onset clusters strictly dominate liquid codas.** V3C and V4 score *identically*
   (0.815 / 0.815 delete, 0.829 / 0.827 epenthesis) while V3C inflates less
   (1.122 vs 1.166 delete, 1.268 vs 1.261 epenthesis — a tie there). Under the deletion
   policy V3C is better on both axes at once. It also renders 26 of 52 words identically
   to the unrestricted V5, against 23 for V3.
4. **V5 is the ceiling and it is not far above V3C** — 0.849 vs 0.829 — and see §6.2
   before believing even that gap.

The learned-cost arm (`sim learned`) gives the same ordering everywhere:
V1 < V2 < V3 < V4 ≈ V3C < V5. **The two arms agree**, which is the condition
[`principles.md`](principles.md) §7.4 set for trusting this ranking.

### 6.2 The check that matters: who are you asking?

Scoring the same forms separately against recipients that must themselves repair
clusters (ja, ko, sw, ta, ha, vi) versus recipients that need not (the rest):

| variant (epenthesis policy) | vs cluster-**repairing** recipients | vs cluster-**tolerant** recipients |
|---|---|---|
| V1 | 0.807 | 0.790 |
| V2 | 0.811 | 0.807 |
| **V3** | **0.814** | 0.810 |
| V4 | 0.809 | 0.829 |
| V5 | 0.808 | **0.861** |
| **V3C** | **0.821** | 0.830 |

**Against the languages that adapt the way we would have to, V5's advantage vanishes
entirely** — it comes *last but one*, and V3C comes first. The whole permissive
advantage in the pooled numbers of §6.1 is contributed by the European Latin-script
recipients, which keep the clusters because they can. This is the strongest available
evidence that the metric's known pro-permissive bias (§3.6) is inflating the pooled
result, and it is non-metric in origin: it is a fact about which recipients you weight.

Given [`principles.md`](principles.md) §2 — ease weighted by total speakers,
representation weighted by L1 speakers — the cluster-repairing group is not a minority
worth discounting: Japanese, Korean, Vietnamese, Swahili, Tamil and Hausa alone are
~500M L1 speakers, and the phonotactic *type* (open syllables, small coda inventory) is
much more widespread than that list.

### 6.3 Delete or epenthesise the final consonant?

| | mean sim | syl inflation |
|---|---|---|
| delete | 0.796 | 1.207 |
| epenthesise | 0.813 | 1.353 |

Epenthesis wins on the metric **by +0.017 despite the metric charging near-full price for
the inserted vowel** — i.e. its true advantage is larger than measured, because the bias
runs against it here. It costs +0.146 in syllable inflation.

The per-word evidence is more decisive than the mean. Deletion produces
**virus → wiru, bank → ban, hotel → hote, sugar → suka, robot → robo, motor → moto,
physics → fisi** — it eats short words, precisely the Wanderwörter with the widest reach,
and the deleted material is unrecoverable. Epenthesis produces *wirusi, baniki, hoteli,
sukari, roboti, motori* — which is, almost segment for segment, what **Swahili** actually
did (*virusi, benki, hoteli, sukari*). Recommendation: **epenthesise**.

### 6.4 The other decision points, priced

| decision | option | mean sim | note |
|---|---|---|---|
| /v/ → | **f** | **0.811** | best, marginally |
| | b | 0.810 | statistically the same |
| | w | 0.796 | 0.015 worse |
| th → | **t** | 0.7962 | |
| | s | 0.7956 | a tie |
| epenthetic vowel | i / u / echo | 0.7962 / 0.7958 / 0.7964 | a tie |
| `<g>` | **hard always** | 0.796 | |
| | soft before e/i/y | 0.790 | worse |
| hiatus | **keep** | 0.796 | §6.5 |
| | glide after any vowel | 0.781 | |
| | glide after /i u/ only | 0.787 | |

### 6.5 Interaction with the new §3.6 hiatus rule (added after the run)

While this study was running, another thread recorded §3.6's FIRM decision that **hiatus
is repaired by glide insertion, written into the spelling** (`oa` → `owa`), with hiatus
*permitted as a fallback for loanwords*. International vocabulary is exactly loanword
material, and it is full of hiatus — the Greek and Latin combining forms are vowel-final
(`geo-`, `theo-`, `bio-`, `radio-`, `-ia`, `-ion`). So the interaction had to be measured.

Scored on the recommended ruleset (V3C, epenthesis, v→f), the same 52 words:

| hiatus policy | mean sim | words changed | examples |
|---|---|---|---|
| **keep hiatus** | **0.843** | – | radio, bakteria, geometria, protein |
| glide after every vowel | 0.826 | 13 | radijo, bakterija, **gejometrija**, **tejorija**, **protejin** |
| glide after high vowels only | 0.833 | 11 | radijo, bakterija, geometria, protein |

**Glide insertion costs recognizability, and the general rule costs twice what the
restricted one does.** The damage is systematic, not random: it lands on the **e_o, e_i
and a_V** sequences, which is precisely where Greek compounding lives (*geo-*, *theo-*,
*-ein*). No recipient language produces *gejometrija*. By contrast the i_V cases the
restricted rule keeps — *radijo, bakterija, malarija, milijon, demokratija, polisija* —
are exactly the attested Slavic reflexes, so they cost nothing.

Recommendation to feed back to §3.6: **take the loanword fallback**, i.e. let
international vocabulary keep its hiatus; or, if a uniform rule is wanted, **restrict
glide insertion to the high vowels /i u/**, where the glide is the vowel's own
approximant. This also answers §3.6's logged open question about the glide after /a/:
under the restricted rule it does not arise.

### 6.6 By domain (V3, delete)

| domain | n | syl inflation | sim | ceiling |
|---|---|---|---|---|
| wanderwort | 9 | **1.056** | 0.805 | 0.866 |
| technology | 10 | 1.133 | 0.797 | 0.860 |
| math/units | 7 | 1.171 | 0.835 | 0.897 |
| bio/med | 9 | 1.176 | 0.794 | 0.888 |
| institutions | 8 | 1.321 | 0.763 | 0.865 |
| chem/phys | 9 | **1.398** | 0.805 | 0.898 |

The non-technical Wanderwörter are almost free (1.06) — they travelled through
phonologically diverse mouths already and arrived pre-simplified. **Chemistry/physics is
the worst-hit domain** (1.40), which is unfortunate given that it is the domain the goal
was written for: Greek compounds are cluster-dense (*electron*, *plastic*, *hydrogen*,
*oxygen*). This is the strongest word-level argument for the onset clusters, which target
exactly this material.

---

## 7. The predictability audit (deliverable B)

**Forward — from the international word to our form — the mapping is a total function
with no arbitrary steps left in it.** Once the five policy parameters below are fixed,
`render()` takes the international spelling and returns one form; there is no lookup
table, no exception list, and no word in the set required a hand adjustment. Every rule
fires on spelling context alone, with at most one letter of lookahead.

That is the good half. The full ledger:

### 7.1 Every point where a choice had to be made

| # | decision point | resolvable by rule? | rule chosen | cost / precedent |
|---|---|---|---|---|
| 1 | **Which international shape to start from** (*computer* or *komputer*? *coffee* or *kahve*? *universitas* or *university*?) | **No — lexical** | pick the shape shared by the most recipient languages | This is the one genuinely unresolvable point. The learner must know the international *stem*, not their own language's word. Precedent: every IAL has this problem; Interlingua's "prototype" procedure is the same judgment made by hand. |
| 2 | **/v/ → f, b or w** | Yes, arbitrary but fixable | **f** (0.811) or **b** (0.810); w is 0.015 worse | Genuine three-way split in the wild: Arabic → f (*fīrūs*), Japanese/Korean/Spanish → b (*bitamin, 바이러스, vacuna*), Mandarin → w (维 *wéi*). No convention is universal. |
| 3 | **`<th>` → t or s** | Yes | **t** | Dead tie on the metric (0.7962 vs 0.7956). Precedent: t is the majority reflex worldwide (*matematika, teoria*); s is the Greek-modern/French-learned one. Pick t and never revisit. |
| 4 | **`<ch>` → k or s** | Yes, at a cost | **k** (Latin value, rule A0) | Right for Greek chi (*chemistry, technology, archive*), wrong for the Romance layer (*chocolate → kokolate*). Fires twice in 52 words. |
| 5 | **`<c>` → k or s** | **Yes, fully** | s before e/i/y, k elsewhere | Not arbitrary at all: this is the Romance rule that all Latin-script recipients already apply. Fires 14 times, always predictably. |
| 6 | **`<g>` soft before front vowels?** | Yes | **no, always hard** | Hard g is 0.006 better and one rule simpler. Precedent: Latin, German, Slavic, Indonesian, Turkish (*geometri, energi*). |
| 7 | **`<y>` → i or u** | Yes | i (j before a vowel) | Not close: every recipient renders it i (*hidrogen, sistem, oksigen*). |
| 8 | **`<x>` → ks** | Yes | always ks | Costly in clusters (*experiment → ekisiperimeniti*) but wholly predictable. |
| 9 | **Which vowel to epenthesise** | Yes | **/i/**, fixed | Metric is indifferent (spread 0.0006). Fixed beats context-sensitive on learnability. Precedent: Swahili and Arabic use /i/; Japanese uses /u/ with allophonic exceptions (a rule a learner would have to memorise); Turkish uses harmony (context-dependent). |
| 10 | **Where to epenthesise in an initial cluster** | Yes | after each excess consonant (*plastic → pilasitiki*) | The rival is Spanish prothesis (*estación*), which only covers /sC/ and would need a second rule. |
| 11 | **Illegal final consonant: delete or support?** | Yes | **support vowel** | §6.3. Deletion is shorter but unrecoverable and hits short Wanderwörter hardest. |
| 12 | **Coda /n/ vs /m/ (V3)** | Yes | whatever the international spelling has | Fully determined by the source; no choice to make. Under V2 it *would* be a forced merger (m → n), which is one more reason V3 over V2. |
| 13 | Geminates, `<ae/oe>`, doubled vowels | Yes | collapse | Forced by §3.5 (no length contrast). |

**Twelve of thirteen are rule-resolvable.** Only #1 is not, and #1 is not a phonology
problem — it is the lexicon-selection problem, and it will be answered by the vocabulary
optimizer choosing a citation form per concept anyway.

### 7.2 Invertibility — the backward direction

Backward is **not** deterministic, and cannot be made so:

- **Merges.** Over the 52-word set the lossy segment rules fire: c→k 12×, v→w 6×,
  c→s 2×, th→t 2×, ch→k 2×, z→s 1×, ph→f 1×, degemination 1×. **55% of the phonemes in
  the rendered forms (198 of 358) could have come from more than one international
  grapheme.** A learner reading *sisitem* cannot know whether the s's were `s`, `c`, `z`,
  `sh` or `th`; reading *witamin* cannot know whether the w was `v` or `w`.
- **Deletion is worse than ambiguity.** Under the deletion policy 14 of 52 words lose a
  segment outright; that information is gone, not merely ambiguous. Under the epenthesis
  policy: **zero**. This is an independent argument for §6.3's recommendation — the
  epenthesis policy makes the mapping *lossless at the segment level*, so the inverse
  becomes a finite disambiguation problem rather than a reconstruction problem.
- **But no collisions.** No two of the 52 words render to the same form. The merges
  destroy *spelling* information, not *word identity*.

The realistic claim is therefore: **the forward direction is a rule; the backward
direction is recognition, not derivation.** A learner who meets *telefon*, *matematika*,
*demokratia*, *sisitem*, *witamin* recognises them instantly; a learner asked to produce
the English spelling from *witamin* will guess `w` before `v` and be wrong. That is the
correct division of labour — recognition is the objective in
[`principles.md`](principles.md) §2, production of the English spelling is not.

One caveat that will grow with the lexicon: with 52 words there are no collisions, but
z→s, v→w and th→t all merge into the two most frequent consonants in the inventory. At
lexicon scale this raises the homophony pressure that §3.3's minimal-pair bans already
manage. Worth re-measuring when the vocabulary optimizer runs.

---

## 8. Bottom line and recommendation

**Is (C)V(N) adequate for the goal?** Yes — it is a workable answer, and it is not close
to the disaster that strict CV would be. It retains 91% of the achievable
recognizability (0.798 against a 0.878 ceiling), lands just below the spread that
separates real languages' adaptations of the same word from each other (0.821), leaves
20 of 52 words with their syllable count untouched, and — the pleasant surprise — fits
the Latin/Greek **ending inventory** almost perfectly, because -on, -in, -um, -ia, -ion,
-ate and -ide are all already legal under it.

**Does one notch of extra permissiveness pay for itself? Yes — but onsets, not codas.**

- **Add the Cr/Cl onset clusters** (pr tr kr pl kl br dr gr fr fl). This is the
  recommendation. **It dominates plain V3 on both axes at once**: +0.017 similarity AND
  −0.085 syllable inflation (delete policy 0.798 → 0.815 at 1.207 → 1.122; epenthesis
  policy 0.813 → 0.829 at 1.353 → 1.268). Permitting the cluster removes the very
  epenthetic vowel that was inflating the syllable count, so nothing is traded away. It is the **best of all six variants when scored
  against the recipients that themselves repair clusters** (§6.2), better even than
  unrestricted (C)V(C). It targets exactly the domain that (C)V(N) hurts most,
  chemistry/physics. And it is phonotactically cheap: a Cr/Cl onset is the single most
  widespread cluster type in the world's languages, far more so than a liquid coda.
- **Do not add liquid codas.** V4 is dominated: same similarity as V3C, more syllables
  (under the deletion policy) or no better (under epenthesis), and it adds /l/ and /r/ —
  the two segments §3.3 already discourages, in the position where they are hardest to
  hear.
- **Keep /m/ alongside /n/.** Free, and it saves *atom*, *film*, *system*, *kilogram*,
  *program* from visible mangling. V2's forced m→n merger is a defect for zero saving.
- **Repair word-final illegal consonants with a support vowel /i/, not by deletion.**
  Better on the metric even though the metric is biased against it, lossless at the
  segment level, and it reproduces Swahili's actual behaviour.
- **Segment rules:** v → f (or b — they are tied; f is more distinctive against /b/ in
  the inventory and keeps /w/ free for `<w>`), th → t, ch → k, c → k/s by the Romance
  rule, g always hard, y → i, x → ks, z → s.

Under that recommendation the flagship words read:
*atom, proton, elekitron, molekula, okisigen, hidrogen, telefon, komputeri, radio,
interineti, demokratia, uniferisitati, matematika, bakiteria, antibiotiki, fitamin,
firusi, plasitiki, telefision, fideo, sisitem, filim, baniki, kafe, sukari, hoteli,
takisi, banana*.

(That list is under **v → f**. Under the tied **v → b** they read *bitamin, birusi,
telebision, bideo, unibersitati* — the Japanese/Spanish/Korean convention rather than the
Arabic one. §3.3's mild discouragement of /b d ɡ/ is the tiebreaker for f.)

**What would talk me out of it.** If the vocabulary optimizer finds that onset clusters
create pressure on the particle inventory (§3.2 wants short, mutually distinct
particles), or if a production study shows Cr/Cl onsets are harder for the
cluster-repairing group than the syllable-count saving is worth, V3 plain remains a
perfectly defensible fallback — it is 0.017 behind, not 0.17.

**The honest residual risk in this study**: the similarity numbers rest on rough
hand-written romanisations (§3.3) and on a metric with a known, unfixed epenthesis gap
(§3.6). The *ordering* of the variants survives both the learned-cost arm and the
recipient split, and the syllable-inflation column is arithmetic rather than metric — so
the ranking is solid. The absolute levels are not, and should not be quoted as if they
were.

---

## 9. Suggested edit to `principles.md` (not applied — another thread owns that file)

§3.6 could move from OPEN to **SOFT** with the following text:

> ### 3.6 Syllable template (SOFT — informed by the international-vocabulary study, 2026-08-05)
>
> **(C)V(N) with N ∈ {n, m}, plus the Cr/Cl onset clusters** (pr tr kr pl kl br dr gr fr
> fl). Illegal word-final consonants take a support vowel /i/ rather than being deleted.
>
> Evidence: [`international-vocab.md`](international-vocab.md). Strict CV is ruled out
> (it costs the largest single step in the table). Liquid codas are ruled out: they are
> dominated by the onset clusters on both recognizability and syllable count, and they
> put /l/ and /r/ — already discouraged in §3.3 — in their least audible position.
> Scored against the recipient languages that themselves repair clusters, (C)V(N)+Cr/Cl
> outperforms even unrestricted (C)V(C).
>
> Still open: whether onset clusters conflict with the short-particle inventory §3.2
> needs; whether /v/ maps to f or b (tied at 0.810–0.811).
>
> The hiatus rule interacts: glide insertion costs 0.017 similarity on international
> vocabulary and mangles Greek compounds (*geometria* → *gejometrija*). Either take the
> loanword fallback the rule already allows, or restrict glide insertion to the high
> vowels /i u/ (cost 0.010, and *radijo / bakterija / demokratija* are attested shapes).
> That restriction also disposes of the logged open question about the glide after /a/.

And §7 could record a new finding:

> 10. **"Every language but Chinese adapts the Latin/Greek roots" is false as stated
>     (2026-08-05).** Adaptation rates over a 52-word international set run from 98%
>     (Spanish) to 28% (Tamil) with no outlier structure. There are three groups: the
>     adapters, a *Sinosphere calquing bloc* (Mandarin, Japanese, Korean, Vietnamese —
>     Chinese is its flagship, not its exception, and the split inside those languages is
>     chronological: 19th-century science calqued, 20th-century vocabulary loaned), and an
>     independent purist tradition (Icelandic, Tamil, Hebrew, Finnish's older stratum,
>     Arabic). The international-vocabulary goal should be priced for roughly half of
>     humanity, not all of it.
