from __future__ import annotations

import math
import re
from pathlib import Path

import numpy as np
import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "data" / "final" / "final.csv"
ALPHA = 0.05

BOX_OFFICE_PATTERN = re.compile(r"^\$?([0-9]*\.?[0-9]+)\s*([KMB])?$", re.IGNORECASE)
BOX_OFFICE_MULTIPLIERS = {"": 1.0, "K": 1e3, "M": 1e6, "B": 1e9}

MODEL_TERMS = [
    "audienceScore",
    "initial_combined_sentiment_score",
    "log_initial_review_count",
]


def parse_box_office(value: object) -> float:
    if pd.isna(value):
        return math.nan
    if isinstance(value, (int, float, np.integer, np.floating)):
        return float(value)

    text = str(value).strip().replace(",", "")
    if not text:
        return math.nan

    match = BOX_OFFICE_PATTERN.match(text)
    if not match:
        return math.nan

    number = float(match.group(1))
    suffix = (match.group(2) or "").upper()
    return number * BOX_OFFICE_MULTIPLIERS[suffix]


def normal_p_value(t_stat: float) -> float:
    return math.erfc(abs(float(t_stat)) / math.sqrt(2))


def load_model_frame() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH)

    if "box_office_num" not in df.columns:
        df["box_office_num"] = df["boxOffice"].map(parse_box_office)
    else:
        df["box_office_num"] = pd.to_numeric(df["box_office_num"], errors="coerce")

    if "log_box_office" not in df.columns:
        df["log_box_office"] = np.log10(df["box_office_num"])
    else:
        df["log_box_office"] = pd.to_numeric(df["log_box_office"], errors="coerce")

    for column in MODEL_TERMS:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    df = df[df["box_office_num"].notna() & (df["box_office_num"] > 0)].copy()
    return df[["id", "title", "log_box_office", *MODEL_TERMS]].dropna().copy()


def fit_ols(model_df: pd.DataFrame) -> tuple[pd.DataFrame, float]:
    y = model_df["log_box_office"].to_numpy(dtype=float)
    X = np.column_stack(
        [
            np.ones(len(model_df)),
            model_df["audienceScore"].to_numpy(dtype=float),
            model_df["initial_combined_sentiment_score"].to_numpy(dtype=float),
            model_df["log_initial_review_count"].to_numpy(dtype=float),
        ]
    )
    labels = ["intercept", *MODEL_TERMS]

    xtx_inv = np.linalg.inv(X.T @ X)
    beta = xtx_inv @ X.T @ y
    residuals = y - X @ beta

    n = len(y)
    p = X.shape[1]
    sigma2 = (residuals @ residuals) / (n - p)
    covariance = sigma2 * xtx_inv
    std_err = np.sqrt(np.diag(covariance))
    t_stat = beta / std_err
    p_values = np.array([normal_p_value(value) for value in t_stat])

    ss_total = ((y - y.mean()) ** 2).sum()
    r_squared = 1 - (residuals @ residuals) / ss_total

    results = pd.DataFrame(
        {
            "term": labels,
            "coef": beta,
            "std_err": std_err,
            "t_approx": t_stat,
            "p_approx": p_values,
        }
    )
    return results, float(r_squared)


def print_hypothesis_summary(results: pd.DataFrame, r_squared: float, n_obs: int) -> None:
    audience_row = results.loc[results["term"] == "audienceScore"].iloc[0]
    reject_null = audience_row["coef"] > 0 and audience_row["p_approx"] < ALPHA

    print("10-day hypothesis test using explainable OLS")
    print(f"Dataset: {DATA_PATH}")
    print(f"Observations used: {n_obs}")
    print(f"Model R^2: {r_squared:.4f}")
    print()
    print("Null hypothesis (H0):")
    print("There is no significant relationship between positive audience reaction and movie popularity,")
    print("after accounting for review sentiment and review volume.")
    print()
    print("Alternative hypothesis (H1):")
    print("Higher positive audience reaction is significantly associated with greater movie popularity,")
    print("after accounting for review sentiment and review volume.")
    print()
    print(results.to_string(index=False))
    print()
    if reject_null:
        print(
            "Decision: Reject H0. Audience score is a positive and statistically significant "
            "predictor of log(boxOffice) in the 10-day OLS model."
        )
    else:
        print(
            "Decision: Fail to reject H0. Audience score is not a positive and statistically significant "
            "predictor of log(boxOffice) in the 10-day OLS model."
        )


def main() -> None:
    model_df = load_model_frame()
    results, r_squared = fit_ols(model_df)
    print_hypothesis_summary(results, r_squared, len(model_df))


if __name__ == "__main__":
    main()
