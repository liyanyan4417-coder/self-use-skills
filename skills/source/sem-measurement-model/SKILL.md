---
name: sem-measurement-model
description: Generate structural equation modeling measurement-model results from survey data. Use when the user asks for SEM measurement model analysis, CFA measurement model results, factor loadings, item reliability SMC, CR, AVE, Fornell-Larcker discriminant validity, HTMT, or formatted measurement-model fit tables from Excel/CSV data.
---

# SEM Measurement Model

Use this skill to turn a survey dataset plus latent-variable item mappings into the three measurement-model tables commonly reported in SEM papers.

## Required Inputs

Ask for missing inputs only when they cannot be inferred:

- Data file path: `.xlsx`, `.xls`, or `.csv`.
- Construct mapping: each latent construct and its observed items.
- Optional structural paths: use them for structural-path appendices if supplied, but compute the three requested measurement-model tables from the CFA measurement model.
- Optional output language labels: preserve the user's construct names when possible.

Example input:

```text
数据文件是 TAM.xlsx。
态度 = Att1, Att2, Att3
易用性 = EOU1, EOU2, EOU3
有用性 = UF1, UF2, UF3
行为意图 = BI1, BI2, BI3
结构关系：行为意图 ~ 态度 + 有用性；态度 ~ 易用性 + 有用性
请看结构方程模型分析的测量模型结果。
```

## Workflow

1. Verify the file exists and inspect columns, sample size, and missing values.
2. Fit a CFA measurement model where each construct loads on its observed items and all latent constructs correlate.
3. If structural paths are supplied, also fit the structural model and keep path estimates as an appendix sheet.
4. Compute and output exactly three main formatted tables:
   - Table 1: parameter estimates and construct reliability/validity.
   - Table 2: discriminant validity.
   - Table 3: measurement-model fit.
5. Save a formatted Excel workbook and concise Chinese summary in the working directory or an `outputs/` folder.

## Preferred Script

Use `scripts/sem_measurement_tables.py` whenever possible. It accepts a JSON config and writes a formatted Excel workbook.

Create a config like:

```json
{
  "data_file": "TAM.xlsx",
  "constructs": {
    "Attitude": {"label": "态度", "items": ["Att1", "Att2", "Att3"]},
    "EaseOfUse": {"label": "易用性", "items": ["EOU1", "EOU2", "EOU3"]},
    "Usefulness": {"label": "有用性", "items": ["UF1", "UF2", "UF3"]},
    "BehavioralIntention": {"label": "行为意图", "items": ["BI1", "BI2", "BI3"]}
  },
  "structural_paths": [
    {"dependent": "BehavioralIntention", "predictors": ["Attitude", "Usefulness"]},
    {"dependent": "Attitude", "predictors": ["EaseOfUse", "Usefulness"]}
  ],
  "output_file": "outputs/sem_measurement_model_tables.xlsx",
  "decimals": 3
}
```

Run:

```bash
python scripts/sem_measurement_tables.py --config sem_config.json
```

If the project has a virtual environment, use its Python. If dependencies are missing, install into a project-local `.venv`: `semopy pandas numpy scipy openpyxl`.

## Table Standards

Table 1 must include:

- Construct name.
- Item name.
- Parameter significance estimates: `Unstd.`, `S.E.`, `z-value`, `P`.
- Item reliability: standardized loading `Std.` and `SMC`.
- Construct-level `CR` and `AVE`.

Use significance stars in the P column:

- `***` for `p < .001`
- `**` for `p < .01`
- `*` for `p < .05`
- exact p value rounded to three decimals otherwise
- `-` for marker loading fixed to 1

Table 2 must include:

- AVE column.
- Fornell-Larcker matrix: diagonal is `sqrt(AVE)` in bold; lower triangle is latent correlations.
- HTMT matrix values in the upper triangle.
- Footnote: diagonal bold values are square roots of AVE, lower triangle is construct Pearson/latent correlation, upper triangle is HTMT ratio.

Table 3 must include:

- Chi-square, df, `x²/df`, GFI, AGFI, RMSEA, SRMR, CFI, IFI, TLI, Hoelter's N, Gamma hat, McDonald's NCI.
- Criteria column matching the common thresholds:
  - chi-square: 越小越好
  - df: 越大越好
  - `1 < x²/df < 3.0`
  - GFI/AGFI/CFI/IFI/TLI/Gamma hat: `> 0.90`
  - RMSEA/SRMR: `< 0.08`
  - Hoelter's N: `>200`
  - McDonald's NCI: `>0.9`

Round all displayed numeric results to three decimals unless the user asks otherwise.

## Interpretation Notes

Mention these issues when present:

- CR below `.70`, AVE below `.50`, or loadings below `.70`.
- Fornell-Larcker violation when an off-diagonal latent correlation exceeds either construct's `sqrt(AVE)`.
- HTMT concern when HTMT exceeds `.85` or `.90`, depending on the user's convention.
- Good measurement fit when CFI/TLI/GFI are above `.90` and RMSEA/SRMR are below `.08`.

Keep final responses short: provide file links, the most important fit/validity findings, and any warnings.
