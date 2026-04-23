from __future__ import annotations

import argparse
import math
import re
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
MOVIES_PATH = BASE_DIR / "data" / "rotten_tomatoes_movies.csv"
REVIEWS_PATH = BASE_DIR / "data" / "rotten_tomatoes_movie_reviews_cleaned.csv"
OUTPUT_DIR = BASE_DIR / "data" / "initial_reaction_10_days"
FINAL_DIR = BASE_DIR / "data" / "final"
AGGREGATED_OUTPUT_PATH = OUTPUT_DIR / "movie_initial_reaction_sentiment_by_movie.csv"
FINAL_OUTPUT_PATH = OUTPUT_DIR / "final_initial_reaction_movie_dataset.csv"
CURATED_FINAL_OUTPUT_PATH = FINAL_DIR / "final.csv"

POSITIVE_LABEL = "POSITIVE"
NEGATIVE_LABEL = "NEGATIVE"
TOP_CRITIC_WEIGHT = 1.5
REGULAR_CRITIC_WEIGHT = 1.0
BOX_OFFICE_PATTERN = re.compile(r"^\$?([0-9]*\.?[0-9]+)\s*([KMB])?$", re.IGNORECASE)
BOX_OFFICE_MULTIPLIERS = {"": 1.0, "K": 1e3, "M": 1e6, "B": 1e9}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build a separate movie dataset using only the first N days of review reactions."
    )
    parser.add_argument(
        "--window-days",
        type=int,
        default=10,
        help="Number of calendar days to include starting from theatrical release day.",
    )
    parser.add_argument(
        "--min-reviews",
        type=int,
        default=21,
        help="Minimum number of early reviews required for a movie to remain in the final dataset.",
    )
    return parser.parse_args()


def load_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, dtype=str, keep_default_na=False)


def row_completeness(frame: pd.DataFrame) -> pd.Series:
    return frame.ne("").sum(axis=1)


def deduplicate_movies(movies_df: pd.DataFrame) -> pd.DataFrame:
    ranked = movies_df.assign(_completeness=row_completeness(movies_df))
    ranked = ranked.sort_values(["id", "_completeness"], ascending=[True, False], kind="stable")
    return ranked.drop_duplicates(subset=["id"], keep="first").drop(columns="_completeness")


def deduplicate_reviews(reviews_df: pd.DataFrame) -> pd.DataFrame:
    ranked = reviews_df.assign(_completeness=row_completeness(reviews_df))
    ranked = ranked.sort_values(
        ["id", "reviewId", "_completeness"],
        ascending=[True, True, False],
        kind="stable",
    )
    return ranked.drop_duplicates(subset=["id", "reviewId"], keep="first").drop(
        columns="_completeness"
    )


def label_from_score(score: float) -> str:
    if score >= 0.2:
        return "positive"
    if score <= -0.2:
        return "negative"
    return "mixed"


def parse_box_office(value: object) -> float:
    if pd.isna(value):
        return math.nan

    text = str(value).strip().replace(",", "")
    if not text:
        return math.nan

    match = BOX_OFFICE_PATTERN.match(text)
    if not match:
        return math.nan

    number = float(match.group(1))
    suffix = (match.group(2) or "").upper()
    return number * BOX_OFFICE_MULTIPLIERS[suffix]


def add_box_office_features(frame: pd.DataFrame) -> pd.DataFrame:
    enriched = frame.copy()
    enriched["box_office_num"] = enriched["boxOffice"].map(parse_box_office)
    enriched["log_box_office"] = enriched["box_office_num"].map(
        lambda value: math.log10(value) if pd.notna(value) and value > 0 else math.nan
    )
    return enriched


def write_csv(path: Path, frame: pd.DataFrame, *, required: bool) -> None:
    try:
        frame.to_csv(path, index=False)
    except PermissionError:
        if required:
            raise
        print(f"Warning: could not overwrite locked file: {path}")


def filter_initial_reactions(
    movies_df: pd.DataFrame, reviews_df: pd.DataFrame, window_days: int
) -> pd.DataFrame:
    merged = reviews_df.merge(
        movies_df[["id", "releaseDateTheaters"]],
        on="id",
        how="inner",
    )
    merged["creationDate"] = pd.to_datetime(merged["creationDate"], errors="coerce")
    merged["releaseDateTheaters"] = pd.to_datetime(
        merged["releaseDateTheaters"], errors="coerce"
    )
    merged = merged[
        merged["creationDate"].notna() & merged["releaseDateTheaters"].notna()
    ].copy()
    merged["days_since_release"] = (
        merged["creationDate"] - merged["releaseDateTheaters"]
    ).dt.days
    return merged[
        merged["days_since_release"].between(0, window_days - 1, inclusive="both")
    ].copy()


def build_sentiment_features(reviews_df: pd.DataFrame) -> pd.DataFrame:
    prepared = reviews_df.copy()
    prepared["scoreSentiment"] = prepared["scoreSentiment"].str.upper().str.strip()
    prepared["sentiment_value"] = prepared["scoreSentiment"].map(
        {POSITIVE_LABEL: 1, NEGATIVE_LABEL: -1}
    )
    prepared = prepared[prepared["sentiment_value"].notna()].copy()

    prepared["isTopCritic"] = prepared["isTopCritic"].str.lower().eq("true")
    prepared["review_weight"] = prepared["isTopCritic"].map(
        {True: TOP_CRITIC_WEIGHT, False: REGULAR_CRITIC_WEIGHT}
    )
    prepared["weighted_sentiment"] = prepared["sentiment_value"] * prepared["review_weight"]

    aggregated = (
        prepared.groupby("id", as_index=False)
        .agg(
            initial_review_count=("reviewId", "size"),
            initial_positive_review_count=(
                "scoreSentiment",
                lambda values: (values == POSITIVE_LABEL).sum(),
            ),
            initial_negative_review_count=(
                "scoreSentiment",
                lambda values: (values == NEGATIVE_LABEL).sum(),
            ),
            initial_top_critic_review_count=("isTopCritic", "sum"),
            initial_weighted_sentiment_total=("weighted_sentiment", "sum"),
            initial_total_review_weight=("review_weight", "sum"),
            first_review_date=("creationDate", "min"),
            last_review_date_in_window=("creationDate", "max"),
        )
    )

    aggregated["initial_positive_review_ratio"] = (
        aggregated["initial_positive_review_count"] / aggregated["initial_review_count"]
    )
    aggregated["initial_combined_sentiment_score"] = (
        aggregated["initial_weighted_sentiment_total"] / aggregated["initial_total_review_weight"]
    )
    aggregated["initial_combined_sentiment_label"] = aggregated[
        "initial_combined_sentiment_score"
    ].map(label_from_score)
    aggregated["log_initial_review_count"] = aggregated["initial_review_count"].map(
        lambda value: math.log1p(value)
    )
    aggregated["initial_sentiment_x_log_review_count"] = (
        aggregated["initial_combined_sentiment_score"] * aggregated["log_initial_review_count"]
    )

    return aggregated[
        [
            "id",
            "initial_review_count",
            "initial_positive_review_count",
            "initial_negative_review_count",
            "initial_top_critic_review_count",
            "initial_positive_review_ratio",
            "initial_combined_sentiment_score",
            "initial_combined_sentiment_label",
            "log_initial_review_count",
            "initial_sentiment_x_log_review_count",
            "first_review_date",
            "last_review_date_in_window",
        ]
    ]


def main() -> None:
    args = parse_args()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    FINAL_DIR.mkdir(parents=True, exist_ok=True)

    if not REVIEWS_PATH.exists():
        raise FileNotFoundError(
            f"Missing cleaned reviews file: {REVIEWS_PATH}. Run src/data_cleaninig.py first."
        )

    movies_raw = load_csv(MOVIES_PATH)
    reviews_raw = load_csv(REVIEWS_PATH)

    movies_df = deduplicate_movies(movies_raw)
    reviews_df = deduplicate_reviews(reviews_raw)
    initial_reviews_df = filter_initial_reactions(movies_df, reviews_df, args.window_days)
    initial_sentiment_df = build_sentiment_features(initial_reviews_df)

    final_df = movies_df.merge(initial_sentiment_df, on="id", how="inner")
    final_df = final_df[final_df["initial_review_count"] >= args.min_reviews].copy()
    final_df = add_box_office_features(final_df)
    final_df = final_df.sort_values(
        ["initial_review_count", "initial_combined_sentiment_score", "title"],
        ascending=[False, False, True],
        kind="stable",
    )

    write_csv(FINAL_OUTPUT_PATH, final_df, required=False)
    write_csv(CURATED_FINAL_OUTPUT_PATH, final_df, required=True)
    write_csv(AGGREGATED_OUTPUT_PATH, initial_sentiment_df, required=False)

    print(f"Movie rows loaded: {len(movies_raw)}")
    print(f"Movie rows after deduplication: {len(movies_df)}")
    print(f"Review rows loaded: {len(reviews_raw)}")
    print(f"Review rows after deduplication: {len(reviews_df)}")
    print(f"Initial-window review rows kept: {len(initial_reviews_df)}")
    print(f"Movies with at least 1 review in first {args.window_days} days: {len(initial_sentiment_df)}")
    print(f"Movies kept with min_reviews >= {args.min_reviews}: {len(final_df)}")
    print(f"Saved aggregated initial reaction sentiment to: {AGGREGATED_OUTPUT_PATH}")
    print(f"Saved final initial reaction dataset to: {FINAL_OUTPUT_PATH}")
    print(f"Saved curated final analysis dataset to: {CURATED_FINAL_OUTPUT_PATH}")


if __name__ == "__main__":
    main()
