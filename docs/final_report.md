# Final Report

## 1. Assignment Context

This project was completed as the group assignment for the module. It follows the required structure:

- selection of one analytical statement
- collection and preparation of relevant data
- justification of the statement using descriptive, inferential, and predictive analytics
- analysis grounded in statistical modelling principles taught in the module

The work is based on **secondary data**.

## 2. Selected Analytical Statement

The selected analytical statement is:

**Positive audience reactions improve content popularity.**

For this project:

- **audience reactions** are represented mainly by `audienceScore` and early review-based reaction variables
- **content popularity** is represented by movie box-office performance, modelled as `log_box_office`

## 3. Data Source and Preparation

The analysis uses a final movie-level dataset stored in `data/final/final.csv`.

The dataset combines movie-level metadata with early review features derived from reviews collected in the first 10 days after theatrical release.

### 3.1 Cleaning and Feature Construction

The data-preparation pipeline includes:

- review-text cleaning
- movie and review deduplication
- filtering reviews to the first 10 days after release
- construction of early-review sentiment and review-volume features
- final movie-level dataset creation

The corrected final workflow uses only retained, explainable variables and excludes direct revenue leakage from predictive modelling.

The key variables used in the final analysis are:

- `audienceScore`
- `initial_combined_sentiment_score`
- `log_initial_review_count`
- `log_box_office`

### 3.2 Final Dataset Suitability

The final dataset contains **4,072 movies and 28 variables**.

- descriptive analysis uses the final movie-level dataset
- inferential analysis uses **3,747** observations
- predictive analysis uses **3,746** observations

This supports stable descriptive summaries, formal hypothesis testing, and train/test predictive evaluation.

## 4. Descriptive Analytics

### 4.1 Purpose

The descriptive stage was used to understand the structure, quality, and major patterns in the dataset before formal modelling.

### 4.2 Main Descriptive Findings

The descriptive analysis showed that:

- the dataset is generally clean and highly complete for the selected model variables
- raw box office is strongly right-skewed, so a logged outcome is more appropriate
- `audienceScore` is broadly distributed and shows meaningful variation across movies
- `initial_combined_sentiment_score` also varies substantially across films
- `log_initial_review_count` is one of the clearest descriptive signals of popularity

Key pairwise correlations with `log_box_office` are:

- `log_initial_review_count = 0.6270`
- `audienceScore = 0.0841`
- `initial_combined_sentiment_score = -0.1381`

### 4.3 Descriptive Interpretation

The descriptive stage suggests that popularity is more clearly associated with **early attention / review volume** than with sentiment polarity alone.

It also shows that the retained predictors are straightforward to interpret in the corrected workflow.

## 5. Inferential Analytics

### 5.1 Purpose

The inferential stage tested whether the selected explanatory variables are significantly associated with `log_box_office`.

### 5.2 Main Inferential Model

The corrected inferential model is:

`log_box_office ~ audienceScore + initial_combined_sentiment_score + log_initial_review_count`

The model is deliberately explainable: OLS provides transparent coefficients, model-level testing, ANOVA-style contribution checks, and assumption diagnostics.

### 5.3 Main Inferential Findings

The inferential analysis found that:

- the overall regression model is statistically significant
- the null hypothesis that the predictors jointly have no relationship with `log_box_office` is rejected
- all three retained predictors are statistically significant in the fitted model

Key model results:

- `R^2 = 0.4318`
- adjusted `R^2 = 0.4313`
- overall `F = 888.1409`
- model `p < 0.001`

Coefficient directions:

- `audienceScore`: positive and significant
- `initial_combined_sentiment_score`: negative and significant
- `log_initial_review_count`: positive and significant

### 5.4 Inferential Interpretation

The inferential stage supports the conclusion that audience reaction and early review behavior are significantly related to popularity.

The strongest inferential signal comes from `log_initial_review_count`, which suggests that early review attention is a major factor associated with box-office performance.

### 5.5 Inferential Limitations

The corrected final model has low VIF values for the retained predictors. The main remaining modelling limitation is heteroskedasticity, which is handled by reporting **HC3 robust standard errors**.

Residual normality is imperfect, but this is less critical given the sample size.

## 6. Predictive Analytics

### 6.1 Purpose

The predictive stage evaluated how well movie popularity can be predicted on unseen data using an explainable regression workflow.

### 6.2 Predictive Setup

The predictive target is:

- `log_box_office`

The analysis uses:

- `80%` training data
- `20%` test data
- `random_state = 42`
- `5-fold` cross-validation

The notebook compares a mean-only baseline, the corrected inferential model, the full candidate-pool model, best-subset selection, and forward-stepwise selection. Model selection is based primarily on training cross-validated RMSE, with test metrics reserved for final evaluation.

### 6.3 Main Predictive Findings

The final predictive model is a **5-variable best-subset selected regression** using:

- `audienceScore`
- `tomatoMeter`
- `initial_top_critic_review_count`
- `initial_positive_review_ratio`
- `log_initial_review_count`

Its performance is:

- cross-validated RMSE = `0.7055`
- test RMSE = `0.7037`
- test MAE = `0.5308`
- test `R^2 = 0.4529`

This means the final predictive model explains about **45% of the variation** in `log_box_office` on unseen test data.

Forward-stepwise selection reaches the same five-feature result, which supports the stability of the selected model.

### 6.4 Predictive Interpretation

The predictive stage shows that:

- the selected reaction and review variables contain real predictive information
- the predictive model performs much better than a mean-only baseline
- the corrected inferential three-variable model is useful, but not the strongest predictive model
- best-subset and forward-stepwise selection both identify the same final five-feature combination

The strongest predictive signals come from:

- early review volume
- audience and critic scores
- early top-critic attention
- early positive-review share

## 7. Overall Justification of the Statement

Taken together, the descriptive, inferential, and predictive stages support the following conclusion.

### 7.1 What the Project Supports

The project supports that:

- audience reaction is related to popularity
- early review behavior is strongly related to popularity
- popularity can be predicted to a meaningful extent using audience and early-review features

### 7.2 Final Verdict

The selected statement is best judged as:

**Partially supported / supported with qualification**

This is the most statistically accurate conclusion because:

- `audienceScore` is positively associated with popularity
- early review volume is a strong positive factor
- predictive performance improves meaningfully when reaction-related variables are used
- the strongest consistent signal across the analysis is early attention rather than sentiment alone

## 8. Final Conclusion

This assignment completes the required descriptive, inferential, and predictive workflow using lecture-aligned statistical modelling techniques.

The corrected final workflow uses a simpler retained predictor set with low VIF values and a clearer interpretation.

The final academically defensible conclusion is:

**Positive audience reactions and early review behavior are meaningfully associated with content popularity, but the strongest evidence points to early review volume as the clearest signal of popularity.**
