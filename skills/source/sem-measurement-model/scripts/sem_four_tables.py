#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, Side
from openpyxl.utils import get_column_letter
from scipy import stats

from sem_measurement_tables import (
    fit_model,
    fit_rows,
    htmt_matrix,
    latent_correlation_matrix,
    measurement_loadings,
    model_syntax,
    p_marker,
    read_data,
    reliability_summary,
    round_value,
    style_sheet,
    write_table1,
    write_table2,
    write_table3,
)


def normalize_code(value):
    if pd.isna(value):
        return -999
    try:
        numeric = float(value)
    except (TypeError, ValueError):
        return -999
    if numeric.is_integer():
        return int(numeric)
    return -999


def clean_measurement_items(data, constructs, valid_range=None):
    items = [item for spec in constructs.values() for item in spec["items"]]
    cleaned = pd.DataFrame(index=data.index)
    missing_rows = []
    low, high = valid_range or [None, None]
    for item in items:
        values = pd.to_numeric(data[item], errors="coerce")
        if low is not None and high is not None:
            values = values.where(values.between(low, high), np.nan)
        missing_count = int(values.isna().sum())
        cleaned[item] = values.fillna(values.mean())
        missing_rows.append(
            {
                "题项": item,
                "超范围或无法识别数量": missing_count,
                "占比": missing_count / len(data),
                "处理方式": "列均值替换" if missing_count else "无需替换",
            }
        )
    return cleaned, missing_rows


def demographic_rows(data, demographics):
    rows = []
    total = len(data)
    for variable, spec in demographics.items():
        if variable not in data.columns:
            raise ValueError(f"Missing demographic column in data: {variable}")
        valid = {normalize_code(k): v for k, v in spec.get("valid", {}).items()}
        coded = data[variable].map(normalize_code)
        coded = coded.where(coded.isin(valid), -999)
        for code, label in valid.items():
            count = int((coded == code).sum())
            rows.append([variable, spec.get("label", variable), code, label, count, count / total, 0])
        missing_count = int((coded == -999).sum())
        rows.append(
            [
                variable,
                spec.get("label", variable),
                -999,
                "缺失",
                missing_count,
                missing_count / total,
                missing_count / total,
            ]
        )
    return rows


def latent_rows(data, constructs):
    rows = []
    for construct, spec in constructs.items():
        label = spec.get("label", construct)
        values = data[spec["items"]].mean(axis=1).dropna().astype(float).to_numpy()
        n = len(values)
        mean = values.mean()
        sd = values.std(ddof=1)
        se = sd / np.sqrt(n)
        t_crit = stats.t.ppf(0.975, df=n - 1)
        rows.append(
            [
                label,
                ", ".join(spec["items"]),
                n,
                mean,
                sd,
                stats.skew(values, bias=False),
                stats.kurtosis(values, fisher=True, bias=False),
                mean - t_crit * se,
                mean + t_crit * se,
                stats.trim_mean(values, 0.05),
            ]
        )
    return rows


def set_medium_bottom(ws, row, min_col, max_col):
    side = Side(style="medium", color="000000")
    for col in range(min_col, max_col + 1):
        ws.cell(row, col).border = Border(bottom=side)


def extract_std_column(estimates):
    for column in ["Est. Std", "Std. Est", "Std.Estimate"]:
        if column in estimates.columns:
            return column
    raise ValueError(f"No standardized estimate column found: {list(estimates.columns)}")


def r_squared(y, predictors):
    y = np.asarray(y, dtype=float)
    x = np.asarray(predictors, dtype=float)
    x = np.column_stack([np.ones(len(x)), x])
    beta, *_ = np.linalg.lstsq(x, y, rcond=None)
    fitted = x @ beta
    ss_total = np.sum((y - y.mean()) ** 2)
    ss_resid = np.sum((y - fitted) ** 2)
    if ss_total == 0:
        return np.nan
    return 1 - ss_resid / ss_total


def vif_values(scores, predictors):
    if len(predictors) <= 1:
        return {predictors[0]: 1.0}
    out = {}
    for predictor in predictors:
        others = [name for name in predictors if name != predictor]
        r2 = r_squared(scores[predictor], scores[others])
        out[predictor] = np.inf if r2 >= 1 else 1 / (1 - r2)
    return out


def structural_path_rows(model, estimates, data, constructs, structural_paths):
    std = extract_std_column(estimates)
    scores = model.predict_factors(data)
    rows = []
    for path in structural_paths:
        dependent = path["dependent"]
        predictors = path["predictors"]
        dep_r2 = r_squared(scores[dependent], scores[predictors])
        dep_vifs = vif_values(scores, predictors)
        for predictor in predictors:
            est = estimates.loc[
                estimates["op"].eq("~")
                & estimates["lval"].eq(dependent)
                & estimates["rval"].eq(predictor)
            ]
            if est.empty:
                continue
            est = est.iloc[0]
            rows.append(
                [
                    constructs[dependent].get("label", dependent),
                    constructs[predictor].get("label", predictor),
                    est["Estimate"],
                    est["Std. Err"],
                    est["z-value"],
                    est["p-value"],
                    est[std],
                    dep_vifs[predictor],
                    dep_r2,
                ]
            )
    return rows


def construct_score_frame(data, constructs):
    scores = pd.DataFrame(index=data.index)
    for construct, spec in constructs.items():
        scores[construct] = data[spec["items"]].mean(axis=1)
    return scores


def standardize_frame(frame):
    return (frame - frame.mean()) / frame.std(ddof=1)


def ols_coefficients(y, x):
    y = np.asarray(y, dtype=float)
    x = np.asarray(x, dtype=float)
    x = np.column_stack([np.ones(len(x)), x])
    beta, *_ = np.linalg.lstsq(x, y, rcond=None)
    return beta


def percentile_ci(values, confidence=0.95):
    alpha = 1 - confidence
    return (
        np.percentile(values, 100 * alpha / 2),
        np.percentile(values, 100 * (1 - alpha / 2)),
    )


def bias_corrected_ci(values, point, confidence=0.95):
    values = np.asarray(values, dtype=float)
    alpha = 1 - confidence
    prop_less = np.mean(values < point)
    prop_less = np.clip(prop_less, 1 / (2 * len(values)), 1 - 1 / (2 * len(values)))
    z0 = stats.norm.ppf(prop_less)
    lower_q = stats.norm.cdf(2 * z0 + stats.norm.ppf(alpha / 2))
    upper_q = stats.norm.cdf(2 * z0 + stats.norm.ppf(1 - alpha / 2))
    return (
        np.percentile(values, 100 * lower_q),
        np.percentile(values, 100 * upper_q),
    )


def mediation_rows(data, constructs, mediations, bootstrap=5000, confidence=0.95, seed=20260610):
    scores = standardize_frame(construct_score_frame(data, constructs))
    rng = np.random.default_rng(seed)
    rows = []

    for spec in mediations:
        x_name = spec["x"]
        mediator = spec["mediator"]
        y_name = spec["y"]
        covariates = spec.get("covariates", [])

        m_predictors = [x_name] + covariates
        y_predictors = [x_name, mediator] + covariates

        a = ols_coefficients(scores[mediator], scores[m_predictors])[1]
        y_beta = ols_coefficients(scores[y_name], scores[y_predictors])
        c_prime = y_beta[1]
        b = y_beta[2]
        c = ols_coefficients(scores[y_name], scores[[x_name] + covariates])[1]
        points = {
            "总效应": c,
            "间接效应": a * b,
            "直接效应": c_prime,
        }

        boot = {name: [] for name in points}
        n = len(scores)
        for _ in range(int(bootstrap)):
            sample_index = rng.integers(0, n, n)
            sample = scores.iloc[sample_index].reset_index(drop=True)
            boot_a = ols_coefficients(sample[mediator], sample[m_predictors])[1]
            boot_y = ols_coefficients(sample[y_name], sample[y_predictors])
            boot_c_prime = boot_y[1]
            boot_b = boot_y[2]
            boot_c = ols_coefficients(sample[y_name], sample[[x_name] + covariates])[1]
            boot["总效应"].append(boot_c)
            boot["间接效应"].append(boot_a * boot_b)
            boot["直接效应"].append(boot_c_prime)

        relationship = (
            f"{constructs[x_name].get('label', x_name)}"
            f"→{constructs[y_name].get('label', y_name)}"
        )
        for effect_name in ["总效应", "间接效应", "直接效应"]:
            boot_values = np.asarray(boot[effect_name], dtype=float)
            point = points[effect_name]
            se = np.std(boot_values, ddof=1)
            z_value = point / se if se else np.nan
            p_value = 2 * (1 - stats.norm.cdf(abs(z_value))) if se else np.nan
            bc_low, bc_high = bias_corrected_ci(boot_values, point, confidence)
            pct_low, pct_high = percentile_ci(boot_values, confidence)
            rows.append(
                [
                    relationship,
                    constructs[mediator].get("label", mediator),
                    effect_name,
                    point,
                    se,
                    z_value,
                    p_value,
                    bc_low,
                    bc_high,
                    pct_low,
                    pct_high,
                    bootstrap,
                ]
            )
    return rows


def write_table5(ws, rows, decimals, mediation=None):
    ws["A1"] = "表5  变量间路径系数表"
    ws["A1"].font = Font(name="Songti SC", bold=True, size=14)
    ws.merge_cells("A1:I1")
    set_medium_bottom(ws, 1, 1, 9)
    headers = [
        "因变量",
        "自变量",
        "非标准化路径系数",
        "标准误",
        "C.R.",
        "P",
        "标准化系数",
        "VIF",
        "R²",
    ]
    for col, header in enumerate(headers, start=1):
        ws.cell(2, col, header)
    for row_idx, values in enumerate(rows, start=3):
        for col_idx, value in enumerate(values, start=1):
            if col_idx == 6:
                value = p_marker(value, decimals)
            else:
                value = round_value(value, decimals)
            ws.cell(row_idx, col_idx, value)
    set_medium_bottom(ws, 2, 1, 9)
    set_medium_bottom(ws, 2 + len(rows), 1, 9)
    for col_idx, width in enumerate([16, 16, 18, 12, 12, 10, 14, 10, 10], start=1):
        ws.column_dimensions[get_column_letter(col_idx)].width = width

    if mediation:
        start = 5 + len(rows)
        ws.cell(start, 1, "中介效应 Bootstrap 检验")
        ws.cell(start, 1).font = Font(name="Songti SC", bold=True, size=14)
        ws.merge_cells(start_row=start, start_column=1, end_row=start, end_column=12)
        set_medium_bottom(ws, start, 1, 12)
        headers = [
            "关系检验",
            "中介变量",
            "效应类型",
            "点估计值",
            "Boot SE",
            "Z",
            "P",
            "Bias-Corrected 95% LLCI",
            "Bias-Corrected 95% ULCI",
            "Percentile 95% LLCI",
            "Percentile 95% ULCI",
            "Bootstrap次数",
        ]
        for col, header in enumerate(headers, start=1):
            ws.cell(start + 1, col, header)
        for row_idx, values in enumerate(mediation, start=start + 2):
            for col_idx, value in enumerate(values, start=1):
                if col_idx == 7:
                    value = p_marker(value, decimals)
                else:
                    value = round_value(value, decimals)
                ws.cell(row_idx, col_idx, value)
        set_medium_bottom(ws, start + 1, 1, 12)
        set_medium_bottom(ws, start + 1 + len(mediation), 1, 12)
        for col_idx, width in enumerate([24, 16, 12, 12, 12, 10, 10, 22, 22, 20, 20, 14], start=1):
            ws.column_dimensions[get_column_letter(col_idx)].width = width


def write_table0(ws, data, constructs, demographics, item_missing, decimals):
    ws["A1"] = "表0  人口特征与潜变量描述统计"
    ws["A1"].font = Font(name="Songti SC", bold=True, size=14)
    ws.merge_cells("A1:J1")
    set_medium_bottom(ws, 1, 1, 10)

    ws["A2"] = "人口特征汇总"
    ws["A2"].font = Font(name="Songti SC", bold=True)
    headers = ["变量", "变量含义", "编码值", "类别", "频数", "占比", "缺失占比"]
    for col, header in enumerate(headers, start=1):
        ws.cell(3, col, header)
    row = 4
    for values in demographic_rows(data, demographics):
        for col, value in enumerate(values, start=1):
            ws.cell(row, col, round_value(value, decimals))
        row += 1
    for r in range(4, row):
        ws.cell(r, 6).number_format = "0." + ("0" * decimals) + "%"
        ws.cell(r, 7).number_format = "0." + ("0" * decimals) + "%"

    row += 2
    ws.cell(row, 1, "潜变量描述性统计")
    ws.cell(row, 1).font = Font(name="Songti SC", bold=True)
    row += 1
    latent_headers = [
        "潜变量",
        "题项",
        "样本量",
        "均值",
        "标准差",
        "偏度",
        "峰度",
        "95%置信区间下限",
        "95%置信区间上限",
        "5%剪除后均值",
    ]
    for col, header in enumerate(latent_headers, start=1):
        ws.cell(row, col, header)
    row += 1
    for values in latent_rows(data, constructs):
        for col, value in enumerate(values, start=1):
            ws.cell(row, col, round_value(value, decimals))
        row += 1

    row += 2
    ws.cell(row, 1, "题项超范围缺失统计")
    ws.cell(row, 1).font = Font(name="Songti SC", bold=True)
    row += 1
    missing_headers = ["题项", "超范围或无法识别数量", "占比", "处理方式"]
    for col, header in enumerate(missing_headers, start=1):
        ws.cell(row, col, header)
    row += 1
    for item_row in item_missing:
        values = [
            item_row["题项"],
            item_row["超范围或无法识别数量"],
            item_row["占比"],
            item_row["处理方式"],
        ]
        for col, value in enumerate(values, start=1):
            ws.cell(row, col, round_value(value, decimals))
        ws.cell(row, 3).number_format = "0." + ("0" * decimals) + "%"
        row += 1

    for width_col, width in enumerate([14, 20, 12, 16, 10, 12, 12, 20, 20, 18], start=1):
        ws.column_dimensions[get_column_letter(width_col)].width = width
    return row + 2


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    args = parser.parse_args()
    config = json.loads(Path(args.config).read_text(encoding="utf-8"))

    decimals = int(config.get("decimals", 3))
    constructs = config["constructs"]
    output_file = Path(config.get("output_file", "outputs/sem_four_tables.xlsx"))
    output_file.parent.mkdir(parents=True, exist_ok=True)

    raw_data = read_data(config["data_file"])
    items = [item for spec in constructs.values() for item in spec["items"]]
    missing = [item for item in items if item not in raw_data.columns]
    if missing:
        raise ValueError(f"Missing item columns in data: {missing}")

    valid_range = config.get("item_valid_range")
    data_for_sem, item_missing = clean_measurement_items(raw_data, constructs, valid_range)

    measurement_desc = model_syntax(constructs, measurement_only=True)
    measurement_model, measurement_estimates, measurement_fit = fit_model(measurement_desc, data_for_sem)
    loadings = measurement_loadings(measurement_estimates, constructs)
    reliability = reliability_summary(data_for_sem, constructs, loadings)
    fornell = latent_correlation_matrix(measurement_estimates, constructs, reliability)
    htmt = htmt_matrix(data_for_sem, constructs)
    fits = fit_rows(measurement_model, data_for_sem, measurement_fit)
    structural_rows = []
    mediation = []
    if config.get("structural_paths"):
        structural_desc = model_syntax(constructs, config["structural_paths"], measurement_only=False)
        structural_model, structural_estimates, _ = fit_model(structural_desc, data_for_sem)
        structural_rows = structural_path_rows(
            structural_model,
            structural_estimates,
            data_for_sem,
            constructs,
            config["structural_paths"],
        )
    if config.get("mediations"):
        mediation = mediation_rows(
            data_for_sem,
            constructs,
            config["mediations"],
            bootstrap=config.get("bootstrap", 5000),
            confidence=config.get("confidence", 0.95),
            seed=config.get("seed", 20260610),
        )

    wb = Workbook()
    ws = wb.active
    ws.title = "SEM四表"
    next_row = 1
    if config.get("demographics"):
        next_row = write_table0(
            ws, raw_data, constructs, config["demographics"], item_missing, decimals
        )

    # Put the original three SEM tables below Table 0 if demographics are supplied.
    if next_row != 1:
        sub = wb.create_sheet("SEM三表")
        write_table1(sub, constructs, loadings, reliability, decimals)
        next_sub = write_table2(sub, len(items) + 6, constructs, reliability, fornell, htmt, decimals)
        write_table3(sub, next_sub, fits, decimals)
        style_sheet(sub, decimals)
    else:
        ws.title = "SEM三表"
        next_row = write_table1(ws, constructs, loadings, reliability, decimals)
        next_row = write_table2(ws, next_row, constructs, reliability, fornell, htmt, decimals)
        write_table3(ws, next_row, fits, decimals)

    if structural_rows:
        paths_sheet = wb.create_sheet("SEM结构路径")
        write_table5(paths_sheet, structural_rows, decimals, mediation)
        style_sheet(paths_sheet, decimals)

    style_sheet(ws, decimals)
    wb.save(output_file)
    print(output_file)


if __name__ == "__main__":
    main()
