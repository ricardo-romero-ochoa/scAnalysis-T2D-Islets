#!/usr/bin/env python3
"""Reproduce manuscript-facing donor-level GSE221156 beta-cell validation."""
from __future__ import annotations
import argparse
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import mannwhitneyu, ttest_ind

SCORES = [
    "IsletDysfunctionScore_sc",
    "BetaIdentitySecretion",
    "ImmuneStress",
    "DedifferentiationStress",
    "DiseaseAxis",
    "OxidativePhosphorylation",
    "ERStress_UPR",
]
PRIMARY = ["IsletDysfunctionScore_sc", "BetaIdentitySecretion", "ImmuneStress"]
LABELS = {
    "IsletDysfunctionScore_sc": "IsletDysfunctionScore analog",
    "BetaIdentitySecretion": "BetaIdentitySecretion",
    "ImmuneStress": "ImmuneStress",
}

def bh_adjust(pvals):
    p = np.asarray(pvals, dtype=float)
    order = np.argsort(p); ranked = p[order]
    q = ranked * len(p) / np.arange(1, len(p) + 1)
    q = np.minimum.accumulate(q[::-1])[::-1]
    out = np.empty_like(q); out[order] = np.minimum(q, 1.0)
    return out

def zscore(x):
    x = np.asarray(x, dtype=float)
    return (x - np.nanmean(x)) / np.nanstd(x, ddof=0)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", type=Path, required=True)
    ap.add_argument("--outdir", type=Path, default=Path("results/manuscript_validation"))
    args = ap.parse_args(); args.outdir.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(args.input)
    if "IsletDysfunctionScore_sc" not in df:
        df["IsletDysfunctionScore_sc"] = zscore(df["ImmuneStress"]) - zscore(df["BetaIdentitySecretion"])
    rows = []
    for score in SCORES:
        nd = df.loc[df.condition.eq("ND"), score].dropna().to_numpy()
        td = df.loc[df.condition.eq("T2D"), score].dropna().to_numpy()
        rows.append({
            "metric": score, "n_ND": len(nd), "n_T2D": len(td),
            "ND_mean": nd.mean(), "T2D_mean": td.mean(),
            "delta_T2D_minus_ND": td.mean() - nd.mean(),
            "MW_p": mannwhitneyu(nd, td, alternative="two-sided").pvalue,
            "Welch_p": ttest_ind(nd, td, equal_var=False).pvalue,
        })
    res = pd.DataFrame(rows); res["BH_q"] = bh_adjust(res["MW_p"].to_numpy())
    res.to_csv(args.outdir / "GSE221156_singlecell_comparisons_with_FDR.csv", index=False)
    qmap = dict(zip(res.metric, res.BH_q))
    fig, axes = plt.subplots(1, 3, figsize=(10.8, 3.7), constrained_layout=True)
    rng = np.random.default_rng(17)
    for i, (ax, score) in enumerate(zip(axes, PRIMARY)):
        vals = [df.loc[df.condition.eq("ND"), score].dropna().to_numpy(), df.loc[df.condition.eq("T2D"), score].dropna().to_numpy()]
        ax.boxplot(vals, tick_labels=["ND", "T2D"], widths=0.55, patch_artist=False, showfliers=False, medianprops={"linewidth": 1.5})
        for j, arr in enumerate(vals, start=1):
            ax.scatter(np.full(len(arr), j) + rng.normal(0, 0.045, size=len(arr)), arr, s=18, alpha=0.75)
        ax.set_ylabel(LABELS[score]); ax.set_xlabel("")
        ax.text(0.02, 0.98, chr(65 + i), transform=ax.transAxes, va="top", ha="left", fontweight="bold", fontsize=12)
        ax.text(0.5, 1.03, f"BH q = {qmap[score]:.3g}", transform=ax.transAxes, ha="center", va="bottom", fontsize=9)
    fig.savefig(args.outdir / "Figure10_singlecell_validation.png", dpi=600, bbox_inches="tight")
    fig.savefig(args.outdir / "Figure10_singlecell_validation.pdf", bbox_inches="tight")

if __name__ == "__main__":
    main()
