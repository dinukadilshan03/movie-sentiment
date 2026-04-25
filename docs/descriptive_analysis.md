# Descriptive Analysis

## Overview

This report presents the descriptive analysis of the final movie-level dataset used for the box-office study. The purpose of this stage is to describe the structure, completeness, and major patterns in the data before formal inferential and predictive modelling.

The analysis is based on secondary Rotten Tomatoes movie and review data processed into the final assignment dataset stored in `data/final/final.csv`.

The descriptive stage is aligned with the corrected inferential specification:

`log_box_office ~ audienceScore + initial_combined_sentiment_score + log_initial_review_count`

The notebook first checks that the curated final dataset exists, the corrected schema is present, the selected variables are numeric, and missingness is documented before any summaries or figures are interpreted.

## Dataset Structure and Completeness

The final dataset contains **4,072 movies and 28 variables**. These variables include:

- movie identifiers
- audience and critic scores
- release information
- box-office variables
- early-review sentiment features
- early-review volume features

The dataset is structurally clean for descriptive analysis:

- duplicate movie IDs: `0`
- finite `log_box_office` values: `3,748`
- complete selected model rows: `3,747`
- no missingness in `initial_combined_sentiment_score`
- no missingness in `log_initial_review_count`

`audienceScore` has a small amount of missingness in the raw file, but the core descriptive and modelling variables remain highly complete.

## Key Variables

The main variables used in the descriptive stage are:

- `box_office_num`: numeric box-office revenue
- `log_box_office`: base-10 logarithm of box-office revenue
- `audienceScore`: Rotten Tomatoes audience score
- `initial_combined_sentiment_score`: combined early-review sentiment score
- `log_initial_review_count`: logged early review count

These variables provide the descriptive foundation for the later inferential and predictive stages.

## Univariate Analysis

### Box Office and Logged Box Office

Raw `box_office_num` is strongly right-skewed, so `log_box_office` is the more suitable outcome for later analysis.

For `log_box_office`:

- mean = `7.0869`
- median = `7.3324`
- standard deviation = `0.9565`
- IQR = `1.1814`
- skewness = `-1.0381`
- range = `0.3010` to `8.9337`

The log transformation reduces the influence of extreme blockbuster values and produces a more stable scale for analysis.

For comparison, raw `box_office_num` has skewness of `3.8015`, confirming a heavy right tail.

### Audience Score

`audienceScore` is broadly distributed and centered in the moderate-to-positive range:

- mean = `61.7549`
- median = `63.0000`
- standard deviation = `19.1535`
- IQR = `30.0000`
- skewness = `-0.1956`
- range = `10` to `100`

This indicates substantial variation in audience reception across movies.

### Early Sentiment

`initial_combined_sentiment_score` ranges from `-1` to `1`:

- mean = `0.1102`
- median = `0.1507`
- standard deviation = `0.5690`
- IQR = `0.9980`
- skewness = `-0.1790`

The sentiment-label composition remains meaningfully mixed:

- positive = `47.96%`
- negative = `33.10%`
- mixed = `18.93%`

### Early Review Volume

`log_initial_review_count` is more compact than the raw review count and works better for modelling:

- mean = `3.8999`
- median = `3.9120`
- standard deviation = `0.4762`
- IQR = `0.7662`
- skewness = `0.1498`
- range = `3.0910` to `5.2627`

This shows that early review attention varies substantially across films.

## Bivariate Analysis

### Relationships with `log_box_office`

Pearson correlations with `log_box_office` are:

- `log_initial_review_count = 0.6270`
- `audienceScore = 0.0841`
- `initial_combined_sentiment_score = -0.1381`

These results show that early review volume is the strongest simple descriptive signal of popularity.

### Relationships Among Predictors

The main pairwise relationships among the retained predictors are:

- `audienceScore` and `initial_combined_sentiment_score = 0.6500`
- `audienceScore` and `log_initial_review_count = 0.0741`
- `initial_combined_sentiment_score` and `log_initial_review_count = -0.0338`

This means that early review volume captures a relatively distinct attention dimension, while audience score and sentiment are moderately aligned but not redundant.

## Grouped Descriptive Analysis

Grouped summaries by `initial_combined_sentiment_label` show a clear audience-response pattern:

- positive films have mean `audienceScore = 72.89`
- mixed films have mean `audienceScore = 58.34`
- negative films have mean `audienceScore = 47.58`

However, average `log_box_office` is not highest for the positive sentiment group:

- negative mean `log_box_office = 7.2127`
- mixed mean `log_box_office = 7.1975`
- positive mean `log_box_office = 6.9494`

This shows that positive early sentiment does not translate into a simple descriptive increase in box office.

Grouped summaries by review-count quartile show a much clearer commercial gradient:

- Q1 lowest: mean `log_box_office = 6.1842`
- Q2: mean `log_box_office = 6.9493`
- Q3: mean `log_box_office = 7.4003`
- Q4 highest: mean `log_box_office = 7.7927`

This is strong descriptive evidence that movies receiving more early review attention tend to perform better commercially.

The descriptive notebook also visualizes:

- raw versus logged box-office distributions
- histograms and boxplots for the retained variables
- a retained-variable correlation heatmap
- predictor-versus-`log_box_office` scatterplots
- grouped boxplots by sentiment label and review-count quartile

## Summary of Main Findings

The descriptive analysis leads to several clear conclusions.

First, the final dataset is large, clean, and usable for later modelling stages.

Second, raw box office is strongly right-skewed, so `log_box_office` is the more appropriate outcome for analysis.

Third, `audienceScore`, `initial_combined_sentiment_score`, and `log_initial_review_count` all vary meaningfully across films.

Fourth, the strongest descriptive signal of popularity is early review volume rather than sentiment polarity alone.

Finally, the descriptive correlation structure is clean enough to support the corrected inferential and predictive workflows.
