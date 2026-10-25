# scAnalysis-T2D-Islets

Reproducible single-cell beta-cell validation repository for the manuscript:

> **Human Islet Transcriptomics in Type 2 Diabetes Reveals Conserved Dysfunction Axes and a Candidate Gene Panel**

This repository contains the GSE221156 beta-cell analysis used as an independent, cell-type-resolved validation layer for the bulk-islet framework. The manuscript-facing analysis is donor-level and cross-sectional; it is intended to test whether the stress/identity pattern identified in bulk islets is detectable within beta cells themselves.

## Manuscript-facing primary analyses

The primary single-cell validation uses 34 donors from GSE221156 (17 ND, 17 T2D) and focuses on three scores:

1. **BetaIdentitySecretion** — expanded 21-gene beta-cell identity/secretion module.
2. **ImmuneStress** — the 14-gene immune/stress module used in the bulk framework.
3. **IsletDysfunctionScore analog** — donor-level `z(ImmuneStress) - z(BetaIdentitySecretion)`.

The main manuscript reports the IsletDysfunctionScore analog and BetaIdentitySecretion as the principal single-cell validation results. ImmuneStress is nominally increased in T2D but does not survive Benjamini-Hochberg correction across the seven reported single-cell score tests.

Exploratory single-cell scores are reported separately:

- **DedifferentiationStress**
- **ERStress_UPR**
- **OxidativePhosphorylation**
- **DiseaseAxis**, defined exactly as
  `z(ImmuneStress) + z(ERStress_UPR) + z(DedifferentiationStress) - z(BetaIdentitySecretion)`.

`DiseaseAxis` is not interchangeable with the bulk IsletDysfunctionScore.

## Key manuscript-facing results

For GSE221156 beta cells:

| Score | T2D - ND delta | Mann-Whitney p | BH q |
|---|---:|---:|---:|
| IsletDysfunctionScore analog | +0.713 | 9.44e-4 | 0.00249 |
| BetaIdentitySecretion | -0.123 | 5.72e-4 | 0.00249 |
| ImmuneStress | +0.00214 | 0.0388 | 0.0543 |
| DedifferentiationStress | +0.0706 | 0.00107 | 0.00249 |
| DiseaseAxis | +0.917 | 0.00979 | 0.0171 |

The repository also includes donor-level age, BMI, HbA1c, sex, assay version, and medication annotation where available. Medication metadata are incomplete and do not define an untreated T2D comparator; no causal drug-specific effect is inferred.

## Supplementary material

The current manuscript supplement is deposited in:

```text
supplementary/Supplementary_Material.docx
```

Supporting donor-level files are in the same directory. The supplement contains the primary and exploratory GSE221156 score definitions, donor metadata, multiple-testing-adjusted results, and the cross-fitted/nested-validation supporting tables from the companion bulk and ML repositories.

## Reproduce the manuscript-facing single-cell comparison

```bash
python scripts/08_manuscript_singlecell_validation.py \
  --input supplementary/GSE221156_donor_singlecell_scores_and_metadata.csv \
  --outdir results/manuscript_validation
```

This regenerates the donor-level comparison table and the three-panel single-cell validation figure.

## Repository organization

```text
scAnalysis-T2D-Islets/
├── config/
├── data/metadata/
├── docs/
├── results/
│   └── manuscript_validation/
├── scripts/
├── src/
└── supplementary/
```

Older landscape/transition scripts remain in the repository as exploratory legacy analyses. They are **not required for the manuscript's primary conclusions** and should not be interpreted as direct evidence of temporal progression or causal state transitions.

## Data source

Primary single-cell dataset: **GSE221156**, human pancreatic islet single-cell RNA-seq. The manuscript analysis uses the reintegrated beta-cell data and donor-level summaries for ND and T2D donors.

## Related repositories

- Bulk cross-cohort transcriptomic integration: `ricardo-romero-ochoa/T2D-islet-integrative`
- Machine learning and GSE50244 external validation: `ricardo-romero-ochoa/T2D-islet-ML-panel`

## License

MIT License. See `LICENSE`.
