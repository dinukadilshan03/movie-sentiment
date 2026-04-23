from __future__ import annotations

import re
import unicodedata
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
INPUT_PATH = BASE_DIR / "data" / "rotten_tomatoes_movie_reviews.csv"
OUTPUT_PATH = BASE_DIR / "data" / "rotten_tomatoes_movie_reviews_cleaned.csv"

# Clean only human-readable text fields. Keep ids, URLs, scores, and empty values as-is.
TEXT_COLUMNS = ("criticName", "publicatioName", "reviewText")
ALLOWED_PUNCTUATION = r".,!?;:'\"()\-/&%"
DISALLOWED_CHARS = re.compile(rf"[^\w\s{re.escape(ALLOWED_PUNCTUATION)}]", re.UNICODE)
MULTISPACE = re.compile(r"\s+")


def sanitize_text(value: str) -> str:
    if value == "":
        return value

    normalized = unicodedata.normalize("NFKC", value)
    filtered = "".join(
        char
        for char in normalized
        if unicodedata.category(char)[0] != "C" and unicodedata.category(char) != "So"
    )
    cleaned = DISALLOWED_CHARS.sub(" ", filtered)
    return MULTISPACE.sub(" ", cleaned).strip()


def main() -> None:
    reviews_df = pd.read_csv(INPUT_PATH, dtype=str, keep_default_na=False)

    for column in TEXT_COLUMNS:
        if column in reviews_df.columns:
            reviews_df[column] = reviews_df[column].map(sanitize_text)

    reviews_df.to_csv(OUTPUT_PATH, index=False)
    print(f"Cleaned reviews saved to {OUTPUT_PATH}")
    print(f"Rows preserved: {len(reviews_df)}")


if __name__ == "__main__":
    main()
