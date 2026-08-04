"""How much of phonological space do WOLD's 41 recipient languages actually cover?

The cost-learning study (notes/cost-learning-spec.md) accepts an assumption:
"wide family coverage => wide phonological-type coverage", i.e. that 24 families
across 6 macroareas is enough of the world's phonological space that costs
learned there transfer to unseen languages. The spec asks for that assumption to
be given a HARD NUMBER rather than left as an assertion. This script produces it.

QUESTION
  For each PHOIBLE segment, does it appear in at least one WOLD recipient
  language's inventory? Aggregated three ways:
    - by segment, weighted by how prevalent the segment is (share of languages,
      and share of L1 speakers, from data/processed/phoneme_prevalence.csv);
    - by macroarea and by family, comparing WOLD's recipient set against
      PHOIBLE's full language set;
    - by inventory SIZE and TYPE, since "has the segment somewhere" can hide a
      missing structural type (e.g. click languages, large-tone systems).

POLICIES (same as the prevalence study, deliberately, so the numbers compose)
  - Inventory membership: majority vote across a language's PHOIBLE inventories
    (a segment counts as present if it is in >= 50% of them).
  - Symbol granularity: the `lumped` level from scripts/phoneme_prevalence.py
    (sub-place and length diacritics collapsed); the strict level would report
    spuriously poor coverage because it treats /t/ and /t̪/ as different sounds.
  - Tone "segments" are excluded from the segment coverage number and reported
    separately, because the metric has no tone dimension anyway (principles
    §3.5 rules tone out of our own inventory).
  - A WOLD recipient with no PHOIBLE inventory is reported, not silently
    dropped: it means the coverage number is computed on fewer than 41.

INPUTS   data/processed/wold_pairs.csv, data/processed/phoneme_prevalence.csv,
         data/raw/phoible/cldf/{values,languages}.csv
OUTPUT   data/processed/wold_coverage.csv  (per lumped segment: prevalence,
         whether a WOLD recipient has it, how many recipients do)

Usage: uv run python scripts/wold_coverage.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import phoneme_prevalence as pp  # noqa: E402  (reuse lump() and the inventory policy)
import wold_pipeline as wp  # noqa: E402

PHOIBLE = ROOT / "data" / "raw" / "phoible" / "cldf"
PREV_CSV = ROOT / "data" / "processed" / "phoneme_prevalence.csv"
OUT_CSV = ROOT / "data" / "processed" / "wold_coverage.csv"


def inventories() -> pd.DataFrame:
    """Language x lumped-segment presence under the majority-vote policy."""
    vals = pd.read_csv(PHOIBLE / "values.csv", low_memory=False)
    langs = pd.read_csv(PHOIBLE / "languages.csv")
    # PHOIBLE CLDF: values.Language_ID IS the Glottocode; Inventory_ID indexes
    # the (possibly several) source inventories per language.
    vals = vals.merge(langs[["Glottocode", "Macroarea", "Family_Name"]].drop_duplicates(),
                      left_on="Language_ID", right_on="Glottocode", how="left")
    vals = vals[vals["Glottocode"].notna()].copy()
    vals["seg"] = vals["Value"].map(pp.lump)
    n_inv = vals.groupby("Glottocode")["Inventory_ID"].nunique().rename("n_inv")
    present = (vals.groupby(["Glottocode", "seg"])["Inventory_ID"].nunique()
               .rename("n_with").reset_index().merge(n_inv, on="Glottocode"))
    present = present[present["n_with"] >= present["n_inv"] / 2.0]
    meta = (vals.groupby("Glottocode")[["Macroarea", "Family_Name"]].first())
    return present, meta


def main() -> None:
    pairs = wp.load_pairs()
    recips = pairs[["recipient", "recipient_glottocode", "family", "macroarea"]].drop_duplicates()
    present, meta = inventories()

    have = set(present["Glottocode"])
    covered = recips[recips["recipient_glottocode"].isin(have)]
    missing = recips[~recips["recipient_glottocode"].isin(have)]
    print(f"WOLD recipients: {len(recips)}; with a PHOIBLE inventory: {len(covered)}")
    if len(missing):
        print("  no PHOIBLE inventory (excluded from the segment number): "
              + ", ".join(missing["recipient"]))

    rset = set(covered["recipient_glottocode"])
    in_wold = present[present["Glottocode"].isin(rset)]
    wold_segs = in_wold.groupby("seg")["Glottocode"].nunique()

    prev = pd.read_csv(PREV_CSV)
    prev = prev[prev["level"] == "lumped"] if "level" in prev.columns else prev
    prev = prev.rename(columns={"symbol": "seg"})
    prev = prev[prev["segment_class"] != "tone"]
    prev = prev.drop_duplicates("seg")

    prev["n_wold_recipients"] = prev["seg"].map(wold_segs).fillna(0).astype(int)
    prev["in_wold"] = prev["n_wold_recipients"] > 0
    langcol, l1col = "pct_languages", "pct_l1_weighted"
    prev.to_csv(OUT_CSV, index=False)

    print(f"\nPHOIBLE lumped segment types (non-tone): {len(prev)}")
    print(f"  present in >=1 WOLD recipient: {prev['in_wold'].sum()} "
          f"({prev['in_wold'].mean():.1%} of types)")
    for label, thresh in [("in >=1% of world languages", 0.01),
                          ("in >=5% of world languages", 0.05),
                          ("in >=20% of world languages", 0.20)]:
        sub = prev[prev[langcol] >= thresh]
        print(f"  of segments {label} (n={len(sub)}): {sub['in_wold'].mean():.1%} covered")
    if l1col:
        w = prev[l1col].fillna(0)
        print(f"  L1-prevalence-weighted coverage: "
              f"{(w * prev['in_wold']).sum() / w.sum():.2%}")
        worst = prev[~prev["in_wold"]].nlargest(10, l1col)[["seg", langcol, l1col]]
        print("\n  most prevalent segments NOT in any WOLD recipient:")
        print(worst.to_string(index=False))

    print("\nmacroarea coverage (WOLD recipients vs PHOIBLE languages):")
    ph_area = meta.loc[list(have)].groupby("Macroarea").size()
    wo_area = meta.loc[list(rset)].groupby("Macroarea").size()
    t = pd.DataFrame({"phoible_langs": ph_area, "wold_recipients": wo_area}).fillna(0).astype(int)
    print(t.to_string())

    ph_fam = set(meta.loc[list(have), "Family_Name"].dropna())
    wo_fam = set(meta.loc[list(rset), "Family_Name"].dropna())
    print(f"\nfamilies: WOLD recipients span {len(wo_fam)} of PHOIBLE's {len(ph_fam)} "
          f"({len(wo_fam) / len(ph_fam):.1%})")

    sizes = present[present["Glottocode"].isin(have)].groupby("Glottocode").size()
    print("\ninventory size (number of lumped segments):")
    print(f"  PHOIBLE all languages: median {sizes.median():.0f}  "
          f"5th pct {sizes.quantile(0.05):.0f}  95th pct {sizes.quantile(0.95):.0f}")
    ws = sizes.loc[[g for g in rset if g in sizes.index]]
    print(f"  WOLD recipients:       median {ws.median():.0f}  "
          f"min {ws.min():.0f}  max {ws.max():.0f}")
    print(f"\nwrote {OUT_CSV}")


if __name__ == "__main__":
    main()
