"""International form -> interlang: a deterministic, ordered transliteration ruleset.

This is a FUNCTION, not a bag of one-off decisions.  Given the international
(Latin-script) spelling of a word and a phonotactic variant, it returns the
interlang form, a trace of every rule that fired, and every point at which the
rule had to make a lossy or arbitrary choice.

Target phonology (principles.md 3.3, FIRM):
    consonants  p t k b d g m n f s h j w l r
    vowels      a e i o u
    orthography ASCII, one letter per phoneme (3.7); /j/ is IPA-valued ("y" of yes)

Two stages, run in order:

  STAGE 1  GRAPHEMIC (`to_phonemes`)  international spelling -> interlang
           phonemes, ignoring phonotactics.  Reads the international spelling
           with LATIN values, not English or French ones (rule A0): this is the
           only convention under which one rule table serves a Turkish, a
           Russian, an Indonesian and a Spanish reader at once, and it is what
           the Latin-script recipient languages themselves overwhelmingly do
           (telefon, elektron, sistem, universitet, komputer).  Cost: words
           whose modern donor pronunciation left the Latin values behind
           (machine, chocolate, energy) come out Latinised.  Priced in
           notes/international-vocab.md 6.

  STAGE 2  PHONOTACTIC (`repair`)  interlang phonemes -> a legal word under the
           chosen syllable-template variant, by epenthesis and (word-finally,
           under one policy) deletion.

Variants (all are (C)V(X): the onset is always optional, so V1..V5 differ ONLY
in what may close a syllable, and V3C differs from V3 only in onsets):

  V1   (C)V            no codas at all - the floor
  V2   (C)V(n)         /n/ only
  V3   (C)V(N)         N in {n, m}                       <- the candidate
  V4   (C)V(N,l,r)     nasals plus liquids
  V5   (C)V(C)         any single consonant - the ceiling
  V3C  V3 + permitted onset clusters {pr tr kr pl kl br dr gr fr fl}

Policies that are genuinely open (each is a decision point in the
predictability audit, notes/international-vocab.md 6) are parameters, so the
study can price each arm instead of asserting one:

  v_target      'w' | 'b' | 'f'          what /v/ becomes
  th_target     't' | 's'                what <th> becomes
  epen          'i' | 'u' | 'echo'       the epenthetic (repair) vowel
  final_policy  'delete' | 'epenthesize' what happens to an illegal word-final
                                         consonant
  g_soft        False | True             whether <g> before e/i/y softens

Defaults are the recommended ruleset; see the write-up for why.
"""

from __future__ import annotations

import unicodedata
from dataclasses import dataclass, field

CONSONANTS = set("ptkbdgmnfshjwlr")
VOWELS = set("aeiou")
LETTERS = CONSONANTS | VOWELS

ONSET_CLUSTERS = {"pr", "tr", "kr", "pl", "kl", "br", "dr", "gr", "fr", "fl"}


@dataclass(frozen=True)
class Variant:
    name: str
    codas: frozenset[str]
    onset_clusters: frozenset[str] = frozenset()
    # nasal->nasal coda mergers forced by the coda set (V2: /m/ has nowhere to
    # go but /n/; a real (C)V(n) language neutralises there rather than
    # epenthesising).  Only within the nasal class - merging /t/ to /n/ would
    # destroy far more than it saves.
    coda_merge: dict = field(default_factory=dict)
    label: str = ""


VARIANTS = {
    "V1": Variant("V1", frozenset(), label="(C)V - strict open syllables"),
    "V2": Variant("V2", frozenset("n"), coda_merge={"m": "n"}, label="(C)V(n)"),
    "V3": Variant("V3", frozenset("nm"), label="(C)V(N), N in {n,m}"),
    "V4": Variant("V4", frozenset("nmlr"), label="(C)V(N,l,r)"),
    "V5": Variant("V5", frozenset(CONSONANTS), label="(C)V(C)"),
    "V3C": Variant("V3C", frozenset("nm"), frozenset(ONSET_CLUSTERS),
                   label="(C)V(N) + Cr/Cl onsets"),
}

# ---------------------------------------------------------------------------
# STAGE 1: graphemic rules
# ---------------------------------------------------------------------------

# A1. Digraphs and trigraphs, longest match first.  Applied left to right in a
#     single pass so that later single-letter rules never re-see them.
#     '@' is a placeholder for the <th> decision, resolved in A3.
DIGRAPHS = [
    ("sch", "sk"),   # Greek/German schema, schola
    ("ph", "f"),     # Greek phi: telephone, philosophy, phase
    ("th", "@"),     # Greek theta: t or s (decision point)
    ("ch", "k"),     # Greek chi read with its Latin value (rule A0)
    ("rh", "r"),     # Greek rho with rough breathing
    ("gh", "g"),
    ("wh", "w"),
    ("ck", "k"),
    ("sh", "s"),     # no second sibilant in the inventory (3.3)
    ("qu", "kw"),
    ("ae", "e"),     # Latin ae/oe monophthongised, as in every modern reflex
    ("oe", "e"),
    ("x", "ks"),     # always, in every position
]

# A2. Single letters that are not themselves interlang phonemes.
#     c, g, y and v are context- or policy-dependent and handled in A3.
SIMPLE = {
    "q": "k", "z": "s",           # no /z/ in the inventory: z -> s
    "ð": "d", "þ": "t",  # eth/thorn, in case an Icelandic form is fed in
}

FRONT = set("eiy")


def _strip(s: str) -> str:
    """Lowercase, strip diacritics, keep letters only."""
    s = unicodedata.normalize("NFD", s.lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return "".join(c for c in s if c.isalpha())


def to_phonemes(intl: str, *, v_target: str = "w", th_target: str = "t",
                g_soft: bool = False) -> tuple[str, list[str]]:
    """STAGE 1.  International spelling -> interlang phoneme string.

    Returns (phonemes, trace) where trace names every rule that fired and, for
    the lossy ones, is prefixed 'LOSSY:' (these are what the predictability
    audit counts).
    """
    trace: list[str] = []
    s = _strip(intl)

    # A1: digraphs, longest match first
    out = []
    i = 0
    while i < len(s):
        for src, dst in DIGRAPHS:
            if s.startswith(src, i):
                out.append(dst)
                if src in ("ph", "ch", "sh", "sch"):   # <th> is logged by A3
                    trace.append(f"LOSSY:A1 {src}->{dst}")
                else:
                    trace.append(f"A1 {src}->{dst}")
                i += len(src)
                break
        else:
            out.append(s[i])
            i += 1
    s = "".join(out)

    # A3: single letters, with lookahead for c/g/y
    res = []
    for i, ch in enumerate(s):
        nxt = s[i + 1] if i + 1 < len(s) else ""
        if ch == "@":                       # <th>
            res.append(th_target)
            trace.append(f"LOSSY:A3 th->{th_target}")
        elif ch == "c":
            if nxt in FRONT:
                res.append("s")
                trace.append("LOSSY:A3 c->s / _front")
            else:
                res.append("k")
                trace.append("LOSSY:A3 c->k")
        elif ch == "g":
            if g_soft and nxt in FRONT:
                res.append("j")
                trace.append("LOSSY:A3 g->j / _front")
            else:
                res.append("g")
        elif ch == "y":
            if nxt and nxt in VOWELS:
                res.append("j")
                trace.append("A3 y->j / _V")
            else:
                res.append("i")
                trace.append("A3 y->i")
        elif ch == "v":
            res.append(v_target)
            trace.append(f"LOSSY:A3 v->{v_target}")
        elif ch == "j":
            res.append("j")                 # Latin/IPA value, not English
        elif ch in SIMPLE:
            res.append(SIMPLE[ch])
            trace.append(f"LOSSY:A3 {ch}->{SIMPLE[ch]}")
        elif ch in LETTERS:
            res.append(ch)
        else:
            trace.append(f"DROP unmapped <{ch}>")
    s = "".join(res)

    # A4: degeminate (no long consonants in the inventory; 3.5 bans length)
    dedup = []
    for ch in s:
        if dedup and dedup[-1] == ch and ch in CONSONANTS:
            trace.append(f"LOSSY:A4 degeminate {ch}{ch}->{ch}")
            continue
        dedup.append(ch)
    s = "".join(dedup)

    # A5: no vowel may repeat adjacently either (no contrastive length, 3.5)
    dedup = []
    for ch in s:
        if dedup and dedup[-1] == ch and ch in VOWELS:
            trace.append(f"LOSSY:A5 shorten {ch}{ch}->{ch}")
            continue
        dedup.append(ch)
    s = "".join(dedup)

    assert all(c in LETTERS for c in s), f"stage 1 leaked non-phonemes: {s}"
    return s, trace


# ---------------------------------------------------------------------------
# STAGE 2: phonotactic repair
# ---------------------------------------------------------------------------

def _split(ph: str) -> tuple[str, list[tuple[str, str]], str]:
    """ph -> (C0, [(Ci, Vi), ...], Cn) with C0 the onset run before the first vowel."""
    runs: list[tuple[str, str]] = []
    i = 0
    while i < len(ph) and ph[i] in CONSONANTS:
        i += 1
    c0, i0 = ph[:i], i
    i = i0
    cur_c = ""
    while i < len(ph):
        if ph[i] in VOWELS:
            runs.append((cur_c, ph[i]))
            cur_c = ""
            i += 1
        else:
            j = i
            while j < len(ph) and ph[j] in CONSONANTS:
                j += 1
            cur_c = ph[i:j]
            i = j
    return c0, runs, cur_c


def _epen_vowel(policy: str, prev_v: str, next_v: str) -> str:
    if policy == "echo":
        return next_v or prev_v or "i"
    return policy


def repair(ph: str, variant: Variant, *, epen: str = "i",
           final_policy: str = "delete") -> tuple[str, list[str]]:
    """STAGE 2.  Make a phoneme string legal under `variant`.

    Rules, applied left to right:

      B1 ONSET.  Each syllable takes the largest legal onset: 1 consonant, or 2
         if the pair is a permitted onset cluster of the variant.
      B2 CODA.   One consonant may be left over before an onset; if it is in the
         variant's coda set it becomes a coda, if the variant has a nasal
         merger for it (V2: m->n) it merges, otherwise B4 applies.
      B3 WORD-FINAL.  The final consonant, if not a legal coda, is either
         DELETED (final_policy='delete', trailing consonants are stripped until
         the word ends in a vowel or a legal coda) or given a support vowel
         (final_policy='epenthesize').
      B4 EPENTHESIS.  Any consonant that can be neither onset nor coda gets a
         support vowel after it, becoming the onset of a new syllable
         (Japanese-style: the segment survives, the syllable count grows).
         The support vowel is chosen by `epen`.

    B4 before B3 in priority: material inside the word is never deleted, only
    the word-final edge is, and only under one policy.  Deleting internally
    would make the mapping non-invertible in the middle of the stem, where the
    recognizability payload lives.
    """
    trace: list[str] = []
    c0, runs, cn = _split(ph)
    out: list[str] = []

    def legal_onset(cs: str) -> int:
        """How many trailing consonants of `cs` can serve as one onset."""
        if len(cs) >= 2 and cs[-2:] in variant.onset_clusters:
            return 2
        return 1 if cs else 0

    # --- word-initial cluster ------------------------------------------------
    if runs:
        first_v = runs[0][1]
        k = legal_onset(c0)
        excess, onset = c0[:len(c0) - k], c0[len(c0) - k:]
        for c in excess:
            # echo policy has no preceding vowel word-initially, so it copies
            # the first vowel of the word (Japanese sutoraiku-style spreading)
            nv = _epen_vowel(epen, "", first_v)
            out.append(c + nv)
            trace.append(f"B4 epenthesis (initial cluster) {c}->{c}{nv}")
        out.append(onset)
    else:
        out.append(c0)

    # --- syllables -----------------------------------------------------------
    for idx, (cs, v) in enumerate(runs):
        if idx == 0:
            out.append(v)
            continue
        prev_v = runs[idx - 1][1]
        k = legal_onset(cs)
        pre, onset = cs[:len(cs) - k], cs[len(cs) - k:]
        # everything in `pre` except possibly the last is epenthesised
        for j, c in enumerate(pre):
            last = (j == len(pre) - 1)
            if last and c in variant.codas:
                out.append(c)                      # B2 coda
            elif last and c in variant.coda_merge:
                out.append(variant.coda_merge[c])  # B2 nasal merger
                trace.append(f"LOSSY:B2 coda merge {c}->{variant.coda_merge[c]}")
            else:
                nv = _epen_vowel(epen, prev_v, v)
                out.append(c + nv)
                trace.append(f"B4 epenthesis (medial cluster) {c}->{c}{nv}")
        out.append(onset)
        out.append(v)

    # --- word-final cluster --------------------------------------------------
    if cn:
        last_v = runs[-1][1] if runs else "a"
        cs = cn
        if final_policy == "delete":
            while cs and cs[-1] not in variant.codas and cs[-1] not in variant.coda_merge:
                trace.append(f"LOSSY:B3 final deletion -{cs[-1]}")
                cs = cs[:-1]
            if cs:
                tail = cs[-1]
                head = cs[:-1]
                for c in head:
                    nv = _epen_vowel(epen, last_v, last_v)
                    out.append(c + nv)
                    trace.append(f"B4 epenthesis (final cluster) {c}->{c}{nv}")
                if tail in variant.codas:
                    out.append(tail)
                else:
                    out.append(variant.coda_merge[tail])
                    trace.append(f"LOSSY:B2 coda merge {tail}->{variant.coda_merge[tail]}")
        else:  # epenthesize
            for j, c in enumerate(cs):
                last = (j == len(cs) - 1)
                if last and c in variant.codas:
                    out.append(c)
                elif last and c in variant.coda_merge:
                    out.append(variant.coda_merge[c])
                    trace.append(f"LOSSY:B2 coda merge {c}->{variant.coda_merge[c]}")
                else:
                    nv = _epen_vowel(epen, last_v, last_v)
                    out.append(c + nv)
                    trace.append(f"B4 epenthesis (final) {c}->{c}{nv}")

    form = "".join(out)
    assert is_legal(form, variant), f"repair produced an illegal form: {ph} -> {form}"
    return form, trace


def is_legal(form: str, variant: Variant) -> bool:
    """Validator: is `form` a legal word under `variant`?"""
    c0, runs, cn = _split(form)
    if len(c0) > 2 or (len(c0) == 2 and c0 not in variant.onset_clusters):
        return False
    for cs, _v in runs[1:] if runs else []:
        if not cs:
            continue
        k = 2 if (len(cs) >= 2 and cs[-2:] in variant.onset_clusters) else 1
        pre = cs[:len(cs) - k]
        if len(pre) > 1:
            return False
        if pre and pre not in variant.codas:
            return False
    if len(cn) > 1:
        return False
    if cn and cn not in variant.codas:
        return False
    return True


def glide_hiatus(form: str, policy: str = "glide") -> tuple[str, list[str]]:
    """Repair vowel-vowel sequences by inserting a glide (principles.md 3.6).

    3.6 (FIRM, 2026-08-05) says hiatus is avoided by glide insertion written
    into the spelling (oa -> owa), with hiatus PERMITTED as a loanword
    fallback.  International vocabulary is loanword material, so this is off by
    default in `render`; the study measures both arms.

    `policy='glide'`: the glide is chosen by the FIRST vowel - /j/ after the
    front vowels i, e; /w/ after the round vowels u, o.  After /a/ (3.6's
    logged open question) the SECOND vowel decides: /j/ before i, e and /w/
    before u, o.

    `policy='glide_high'`: insert only after the HIGH vowels i and u, where the
    glide is the vowel's own approximant and the result is attested
    (radio -> radijo, bacteria -> bakterija, exactly the Slavic reflexes).
    Leaves e_o, e_i and a_V alone, which is where the general rule mangles
    Greek compounds (geo-, theo-, -ein).  Measured in
    notes/international-vocab.md 6.6.
    """
    out, trace = [], []
    for i, ch in enumerate(form):
        out.append(ch)
        nxt = form[i + 1] if i + 1 < len(form) else ""
        if ch in VOWELS and nxt in VOWELS:
            if policy == "glide_high" and ch not in "iu":
                continue
            if ch in "ie":
                g = "j"
            elif ch in "uo":
                g = "w"
            else:                       # after /a/: decided by what follows
                g = "j" if nxt in "ie" else "w"
            out.append(g)
            trace.append(f"B5 glide insertion {ch}_{nxt} -> {ch}{g}{nxt}")
    return "".join(out), trace


def syllables(form: str) -> int:
    """Syllable count = number of vowels (no diphthongs in the inventory, 3.3)."""
    return sum(1 for c in form if c in VOWELS)


def render(intl: str, variant: str | Variant, *, v_target: str = "w",
           th_target: str = "t", epen: str = "i", final_policy: str = "delete",
           g_soft: bool = False, hiatus: str = "keep") -> dict:
    """Full pipeline: international spelling -> interlang word under a variant.

    Returns a dict with the form, both stage outputs, the syllable counts
    before and after repair, and the rule trace.
    """
    var = VARIANTS[variant] if isinstance(variant, str) else variant
    ph, t1 = to_phonemes(intl, v_target=v_target, th_target=th_target, g_soft=g_soft)
    form, t2 = repair(ph, var, epen=epen, final_policy=final_policy)
    t3: list[str] = []
    if hiatus in ("glide", "glide_high"):
        form, t3 = glide_hiatus(form, hiatus)
    trace = t1 + t2 + t3
    return {
        "variant": var.name,
        "intl": intl,
        "phonemes": ph,
        "form": form,
        "syl_before": syllables(ph),
        "syl_after": syllables(form),
        "len_before": len(ph),
        "len_after": len(form),
        "trace": trace,
        "n_lossy": sum(1 for x in trace if x.startswith("LOSSY:")),
        "n_epenthesis": sum(1 for x in trace if x.startswith("B4")),
        "n_deleted": sum(1 for x in trace if x.startswith("LOSSY:B3")),
    }


def to_ipa(form: str) -> str:
    """Interlang orthography -> IPA (the only difference is <g> = /g/)."""
    return form.replace("g", "ɡ")
