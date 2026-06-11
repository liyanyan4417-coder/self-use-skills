---
name: sem-measurement-model
description: Generate structural equation modeling measurement-model, structural-path, and bootstrap mediation results from survey data. Use when the user asks for SEM measurement model analysis, CFA results, demographic summaries, latent-variable descriptive statistics, factor loadings, item reliability SMC, CR, AVE, Fornell-Larcker, HTMT, measurement-model fit tables, structural path coefficient tables with VIF and R2, or bootstrap mediation analysis with confidence intervals from Excel/CSV data.
---

# SEM Measurement Model

Use this skill to turn a survey dataset plus latent-variable item mappings into the standard SEM measurement-model workbook.

## Required Inputs

Ask for missing inputs only when they cannot be inferred:

- Data file path: `.xlsx`, `.xls`, or `.csv`.
- Construct mapping: each latent construct and its observed items.
- Optional demographic variables and valid category codes.
- Optional item valid range, usually `[1, 7]` for Likert scales.
- Optional structural paths: when supplied, fit the structural model and output 表5 变量间路径系数表.
- Optional mediation specifications: when supplied, append Bootstrap mediation results under 表5.

## Default Output

When demographics are supplied, output four tables:

- 表0：人口特征与潜变量描述统计。
- 表1：参数估计、题目信度 SMC、CR、AVE。
- 表2：Fornell-Larcker + HTMT 区分效度。
- 表3：测量模型拟合度。
- 表5：变量间路径系数表。仅当用户给出结构关系时输出。
- 表5下方：中介效应 Bootstrap 检验。仅当用户给出中介关系时输出。

When demographics are not supplied, output the original three SEM measurement tables.

## Preferred Script

Use `scripts/sem_four_tables.py` when demographics or latent descriptive statistics are requested.
Use `scripts/sem_measurement_tables.py` only for the older three-table measurement-model workflow.

Create a config like:

```json
{
  "data_file": "data.xlsx",
  "constructs": {
    "CultureAtmosphere": {"label": "文化氛围", "items": ["A1", "A2", "A3"]},
    "LifeSatisfaction": {"label": "生活满意度", "items": ["C1", "C2", "C3", "C4", "C5"]},
    "EmotionalMemory": {"label": "情感记忆", "items": ["B1", "B2", "B3", "B4"]},
    "HeritageProtection": {"label": "遗产保护", "items": ["D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8"]}
  },
  "demographics": {
    "V1": {"label": "性别", "valid": {"1": "男", "2": "女"}},
    "V2": {"label": "年龄", "valid": {"1": "编码1", "2": "编码2", "3": "编码3", "4": "编码4", "5": "编码5"}}
  },
  "structural_paths": [
    {"dependent": "EmotionalMemory", "predictors": ["CultureAtmosphere", "LifeSatisfaction"]},
    {"dependent": "HeritageProtection", "predictors": ["CultureAtmosphere", "LifeSatisfaction", "EmotionalMemory"]}
  ],
  "mediations": [
    {"x": "CultureAtmosphere", "mediator": "EmotionalMemory", "y": "HeritageProtection", "covariates": ["LifeSatisfaction"]},
    {"x": "LifeSatisfaction", "mediator": "EmotionalMemory", "y": "HeritageProtection", "covariates": ["CultureAtmosphere"]}
  ],
  "bootstrap": 5000,
  "confidence": 0.95,
  "item_valid_range": [1, 7],
  "output_file": "outputs/sem_four_tables.xlsx",
  "decimals": 3
}
```

Run:

```bash
python scripts/sem_four_tables.py --config sem_config.json
```

If dependencies are missing, install into a project-local `.venv`: `semopy pandas numpy scipy openpyxl`.

## Table 0 Standards

Demographic variables:

- Treat values outside the provided valid codes as missing.
- Mark invalid/missing codes as `-999`.
- Output frequency, percentage, and missing percentage.
- Format percentages as percentages and round numeric output to three decimals unless the user says otherwise.

Latent descriptive statistics:

- Treat measurement item values outside `item_valid_range` as missing.
- Replace missing measurement item values with the corresponding item column mean.
- Compute latent-variable scores as the row mean of that construct's cleaned/imputed items.
- Output mean, standard deviation, skewness, kurtosis, 95% confidence interval for the mean, and 5% trimmed mean.

## Tables 1-3 Standards

Table 1 must include construct, item, `Unstd.`, `S.E.`, `z-value`, `P`, `Std.`, `SMC`, `CR`, and `AVE`.

Use significance stars in the P column:

- `***` for `p < .001`
- `**` for `p < .01`
- `*` for `p < .05`
- exact p value rounded to three decimals otherwise
- `-` for marker loading fixed to 1

Table 2 must include AVE, Fornell-Larcker, and HTMT in one matrix:

- Diagonal: `sqrt(AVE)`, bold.
- Lower triangle: latent correlations.
- Upper triangle: HTMT ratio.

Table 3 must include Chi-square, df, `x²/df`, GFI, AGFI, RMSEA, SRMR, CFI, IFI, TLI, Hoelter's N, Gamma hat, and McDonald's NCI.

## Table 5 Standards

When `structural_paths` are supplied, output 表5 in a separate sheet named `SEM结构路径`.

Table 5 must include:

- 因变量
- 自变量
- 非标准化路径系数
- 标准误
- C.R.
- P
- 标准化系数
- VIF
- R²

Use SEM structural-model estimates for nonstandardized coefficients, standard errors, C.R., p values, and standardized coefficients. Compute VIF and R² from latent factor scores predicted from the fitted structural model. For a dependent variable with only one predictor, VIF is `1.000`.

For mediation analysis under Table 5:

- Use cleaned/imputed construct scores.
- Standardize construct scores before mediation estimation.
- Use bootstrap resampling, default `5000` times and confidence level `.95`.
- For each mediation relation, output total effect, indirect effect, and direct effect.
- Include point estimate, Boot SE, Z, P, Bias-Corrected 95% LLCI/ULCI, Percentile 95% LLCI/ULCI, and bootstrap count.
- Treat an indirect effect as significant when the bootstrap confidence interval does not include zero.

Round all displayed numeric results to three decimals unless the user asks otherwise.

## Interpretation Notes

Mention these issues when present:

- Loadings below `.70`, CR below `.70`, or AVE below `.50`.
- Fornell-Larcker violation when an off-diagonal latent correlation exceeds either construct's `sqrt(AVE)`.
- HTMT concern when HTMT exceeds `.85` or `.90`, depending on the user's convention.
- Measurement fit concerns when CFI/TLI/GFI are below `.90` or RMSEA/SRMR are above `.08`.
- Structural path significance, direction, and multicollinearity concerns when VIF is above `5` or `10`.
- Mediation significance based on whether Bias-Corrected and Percentile confidence intervals include zero.

Keep final responses short: provide file links, the most important fit/validity findings, and any warnings.
