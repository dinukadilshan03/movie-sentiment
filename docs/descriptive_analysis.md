# Descriptive Analysis

## Overview

This report presents the descriptive analysis of the final movie-level dataset used for the box-office study. The purpose of this stage is to describe the structure, completeness, and major empirical patterns in the data before formal inferential and predictive modelling.

The analysis is based on secondary Rotten Tomatoes movie and review data processed into the final assignment dataset.

The descriptive stage supports the selected analytical statement:

**Positive audience reactions improve content popularity.**

In this project:

- audience reaction is represented mainly by `audienceScore` and early review-based reaction features
- content popularity is represented by box-office performance, especially `log_box_office`

The descriptive analysis is aligned with the final inferential specification:

`log_box_office ~ audienceScore + initial_combined_sentiment_score + log_initial_review_count + initial_sentiment_x_log_review_count`

## Dataset Structure and Completeness

The final dataset contains **4,072 movies and 29 variables**. These variables include:

- movie identifiers
- audience and critic scores
- movie characteristics
- release information
- box-office variables
- early-review sentiment and review-volume features

The dataset is structurally clean for descriptive analysis:

- duplicate movie IDs: `0`
- finite `log_box_office` values: `3,748`
- no missingness in the constructed early-review variables

Completeness is strong for the core variables used in later modelling. `initial_combined_sentiment_score`, `log_initial_review_count`, and `initial_sentiment_x_log_review_count` are fully populated. `audienceScore` has a small amount of missingness in the raw dataset, but the descriptive coverage remains strong. The only large non-core missingness appears in `soundMix`, which is missing in about **39.86%** of rows and does not affect the selected modelling variables.

Overall, the final dataset is large, usable, and well suited for the descriptive, inferential, and predictive stages required by the assignment.

## Description of Key Variables

The main variables relevant to the final assignment stages are:

- `box_office_num`: numeric box-office revenue
- `log_box_office`: base-10 logarithm of numeric box-office revenue
- `audienceScore`: Rotten Tomatoes audience score
- `tomatoMeter`: Rotten Tomatoes critic score
- `initial_review_count`: number of reviews in the early review window
- `initial_positive_review_ratio`: share of positive early reviews
- `initial_combined_sentiment_score`: combined early-review sentiment score
- `log_initial_review_count`: logged early review count
- `initial_sentiment_x_log_review_count`: interaction between early sentiment and logged review count

These variables provide the descriptive foundation for later hypothesis testing and predictive modelling.

## Univariate Analysis

### Box Office and Logged Box Office

Raw `box_office_num` is strongly right-skewed. Its mean is approximately **47.79 million**, while the median is **21.50 million**, showing that a relatively small number of very high-grossing films pull the average upward. The standard deviation is about **76.61 million**, the 95th percentile is **183.52 million**, and the maximum is **858.40 million**. The skewness is about **3.80**, confirming a heavy upper tail.

Because of this skewness, `log_box_office` is a more useful version of the outcome for later analysis. The logged outcome has:

- mean = `7.0869`
- median = `7.3324`
- standard deviation = `0.9565`

The transformation reduces the influence of extreme blockbusters and gives a more balanced scale for descriptive comparison and later modelling.

### Audience Score

`audienceScore` is broadly distributed and centered in the moderate-to-positive range:

- mean = `61.75`
- median = `63`
- standard deviation = `19.15`
- range = `10` to `100`

This indicates substantial variation in audience reception across movies and suggests that the variable is informative enough to support later inferential and predictive stages.

### Critic Score

`tomatoMeter` also shows broad variation:

- mean = `56.77`
- median = `60`
- standard deviation = `27.56`
- range = `0` to `100`

This gives the dataset a useful critic-evaluation dimension in addition to audience reaction.

### Early Sentiment

`initial_combined_sentiment_score` ranges from `-1` to `1` and is centered only slightly above zero:

- mean = `0.1102`
- median = `0.1507`
- standard deviation = `0.5690`

This shows that the sample contains a wide spread of early sentiment, from strongly negative to strongly positive.

The categorical version of this variable is also meaningfully distributed:

- positive = `47.96%`
- negative = `33.10%`
- mixed = `18.93%`

So the sample contains a broad mix of early critical reactions rather than being concentrated in only one category.

### Early Review Volume

`initial_review_count` shows strong variation across films:

- mean = `54.38`
- median = `49`
- standard deviation = `27.60`
- range = `21` to `192`

The logged version, `log_initial_review_count`, is more compact:

- mean = `3.8999`
- median = `3.9120`
- standard deviation = `0.4762`

This supports the later use of the logged version in modelling.

### Interaction Term

`initial_sentiment_x_log_review_count` ranges widely:

- mean = `0.4206`
- median = `0.5881`
- standard deviation = `2.2018`
- range = about `-4.1744` to `4.8481`

This term captures whether sentiment becomes stronger or weaker when combined with early review volume.

## Categorical Composition of the Sample

The dataset is dominated by mainstream English-language releases.

Original language composition is led by:

- English = `94.43%`
- English (United Kingdom) = `1.30%`
- French (France) = `0.79%`

The most common content ratings are:

- `R` = `46.58%`
- `PG-13` = `39.12%`
- `PG` = `14.19%`

The most common primary genres are:

- Comedy
- Drama
- Action
- Kids & family
- Mystery & thriller
- Horror

The most common distributors include:

- Universal Pictures
- Warner Bros. Pictures
- 20th Century Fox
- Paramount Pictures
- Sony Pictures Entertainment

These patterns show that the sample is mostly composed of commercially released mainstream films rather than a heavily niche set of titles.

## Bivariate Analysis

### Relationships with `log_box_office`

The clearest descriptive relationship with `log_box_office` is early review volume.

Correlations with `log_box_office` are:

- `log_initial_review_count` = `0.6270`
- `initial_review_count` = `0.5707`
- `runtimeMinutes` = `0.2052`
- `audienceScore` = `0.0841`
- `tomatoMeter` = `-0.1497`
- `initial_combined_sentiment_score` = `-0.1381`
- `initial_sentiment_x_log_review_count` = `-0.0989`

These results show that early review volume is much more strongly connected to commercial success than the sentiment variables at the simple pairwise level.

`audienceScore` has a weak positive descriptive relationship with logged popularity, while the sentiment variables show weak negative simple correlations. This already suggests that the final conclusion will need to be more nuanced than a simple "more positive sentiment means more popularity" statement.

### Relationships Among Predictors

Several of the predictors overlap strongly:

- `audienceScore` and `initial_combined_sentiment_score` = `0.6500`
- `audienceScore` and `initial_sentiment_x_log_review_count` = `0.6544`
- `initial_combined_sentiment_score` and `initial_sentiment_x_log_review_count` = `0.9919`

By contrast:

- `log_initial_review_count` and `audienceScore` = `0.0741`
- `log_initial_review_count` and `initial_combined_sentiment_score` = `-0.0338`

This means that early review volume appears to capture a more distinct commercial-attention dimension, while the sentiment score and interaction term are highly overlapping descriptively.

## Grouped Descriptive Analysis

### Differences by Sentiment Label

Grouped summaries by `initial_combined_sentiment_label` show a very clear audience-response pattern:

- positive films have mean `audienceScore = 72.89`
- mixed films have mean `audienceScore = 58.34`
- negative films have mean `audienceScore = 47.58`

So the sentiment classification aligns strongly with how audiences later score the films.

However, the box-office pattern is less straightforward:

- negative mean `log_box_office = 7.2127`
- mixed mean `log_box_office = 7.1975`
- positive mean `log_box_office = 6.9494`

This suggests that positive early sentiment is not automatically associated with the highest central tendency in logged commercial performance.

### Differences by Review-Count Quartile

Grouped summaries by review-count quartile show a much clearer commercial gradient:

- Q1 lowest: mean `log_box_office = 6.1842`
- Q2: mean `log_box_office = 6.9493`
- Q3: mean `log_box_office = 7.4003`
- Q4 highest: mean `log_box_office = 7.7927`

Mean raw box office also increases sharply across these quartiles:

- Q1 lowest: about `10.53 million`
- Q4 highest: about `103.93 million`

This is strong descriptive evidence that movies receiving more early review attention tend to perform better commercially.

Audience scores vary less dramatically across quartiles, but the highest review-count quartile still has the highest mean audience score at `65.53`.

## Interpretation of the Final Model Variables

Taken together, the descriptive analysis suggests that the later inferential and predictive models are likely capturing several different dimensions of movie performance.

- `log_initial_review_count` appears to be the strongest descriptive correlate of popularity and likely reflects visibility, attention, or early market interest.
- `audienceScore` captures audience approval and shows a weak but positive descriptive relationship with popularity.
- `initial_combined_sentiment_score` captures evaluative tone, but descriptively it is not strongly positive with the logged outcome.
- `initial_sentiment_x_log_review_count` overlaps heavily with the sentiment score and may be difficult to interpret as a distinct descriptive feature without formal modelling.

So the descriptive evidence suggests that popularity is related most clearly to **early attention**, while the role of **sentiment polarity** is more complicated.

## Summary of Main Findings

The descriptive analysis leads to several broad conclusions.

First, the final dataset is large, clean, and highly usable for later modelling stages.

Second, raw box office is strongly right-skewed, so `log_box_office` is a more appropriate outcome for analysis.

Third, `audienceScore`, critic score, early sentiment, and early review volume all vary meaningfully across films, providing a strong base for later inferential and predictive work.

Fourth, the strongest descriptive signal of popularity is early review volume rather than sentiment polarity alone.

Fifth, positive early sentiment aligns strongly with audience approval, but not with a simple higher mean logged box office.

Finally, the descriptive correlation structure shows substantial overlap between the sentiment score and the interaction term, while logged review count appears to capture a more distinct commercial-attention dimension.

These findings provide the descriptive foundation for the inferential and predictive stages of the assignment.
