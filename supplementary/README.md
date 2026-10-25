# Supplementary material and manuscript-facing single-cell outputs

This directory contains the repository-readable supplementary document and donor-level GSE221156 beta-cell files supporting the current manuscript revision.

Files:

- `Supplementary_Material.md` — current supplement, including Tables S1-S7, in GitHub-readable form.
- `GSE221156_donor_singlecell_scores_and_metadata.csv` — donor-level scores and clinical metadata.
- `GSE221156_primary_singlecell_comparisons.csv` — unadjusted donor-level ND vs T2D comparisons used to construct the primary manuscript validation.

The exact Microsoft Word supplement used for journal resubmission is kept in the submission package and may be attached separately to a GitHub release or archival deposit.

The manuscript applies Benjamini-Hochberg correction jointly across seven reported single-cell score tests. The primary single-cell score is `IsletDysfunctionScore_sc = z(ImmuneStress) - z(BetaIdentitySecretion)`; the exploratory `DiseaseAxis` is a different composite and is defined in `data/metadata/core_modules.yaml`.
