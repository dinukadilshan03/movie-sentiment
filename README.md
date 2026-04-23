# Movie Sentiment Pipeline

This project now keeps only the 10-day workflow and the curated final dataset built from it.

## Source data

- `data/rotten_tomatoes_movies.csv`
- `data/rotten_tomatoes_movie_reviews.csv`

## Pipeline steps

1. `src/data_cleaninig.py`  
   Cleans unsupported characters from text fields in `data/rotten_tomatoes_movie_reviews.csv` and writes `data/rotten_tomatoes_movie_reviews_cleaned.csv`.
2. `src/build_initial_reaction_dataset.py`  
   Builds the 10-day movie-level dataset using only reviews from the first 10 days after theatrical release and keeps movies with at least 21 reviews in that window.

## Active datasets

- `data/initial_reaction_10_days/movie_initial_reaction_sentiment_by_movie.csv`
- `data/initial_reaction_10_days/final_initial_reaction_movie_dataset.csv`
- `data/final/final.csv`  
  This is the current source of truth for analysis and hypothesis testing.

## Active analysis artifacts

- `notebooks/eda_final_dataset.ipynb`
- `src/hypothesis_testing_10_day.py`

## Model-ready columns

- `audienceScore`
- `initial_combined_sentiment_score`
- `log_initial_review_count`
- `initial_sentiment_x_log_review_count`

## Modeling choice

Hypothesis testing uses an explainable ordinary least squares model with:

```text
log(boxOffice) ~ audienceScore
               + initial_combined_sentiment_score
               + log_initial_review_count
               + initial_sentiment_x_log_review_count
```

No black-box models are used in the current workflow.

## Run commands

Run the cleaning and 10-day dataset pipeline:

```bash
python main.py
```

Run the hypothesis test:

```bash
python src/hypothesis_testing_10_day.py
```
