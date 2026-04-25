# Predictive Analysis

## Overview

This report presents the predictive analysis of the final movie-level dataset used for the box-office study. The goal is to evaluate how well movie popularity can be predicted on unseen data using an explainable regression workflow.

The predictive target is `log_box_office`. The analysis is predictive rather than causal: the goal is to minimize prediction error while retaining an interpretable model.

Only explainable linear regression models are used. Direct revenue leakage columns such as `boxOffice` and `box_office_num` are excluded from the predictor set.

## Data and Predictor Pool

The raw final dataset contains 4,072 movies and 28 variables. For predictive modelling, the response variable is `log_box_office`, and the candidate predictor pool contains seven variables:

- `audienceScore`
- `tomatoMeter`
- `runtimeMinutes`
- `initial_top_critic_review_count`
- `initial_positive_review_ratio`
- `initial_combined_sentiment_score`
- `log_initial_review_count`

The candidate pool combines audience reaction, critic reaction, movie context, early sentiment, and early review attention.

After removing rows with missing values in the target or candidate predictors, **3,746 movies** remain for predictive analysis.

## Predictive Setup

The predictive workflow uses a fixed split so that results are reproducible:

- training set: `80%`
- test set: `20%`
- `random_state = 42`
- `5-fold` cross-validation on the training set

Model selection is performed using cross-validated RMSE on the training set only. The held-out test set is reserved for final generalization evaluation.

The comparison includes:

- a mean-only baseline
- the corrected inferential three-variable regression
- a full candidate-pool regression
- a best-subset selected regression
- a forward-stepwise selected regression

## Baseline Predictive Models

The mean-only benchmark performs poorly:

- test RMSE = `0.9522`
- test MAE = `0.7515`
- test `R^2 = -0.0018`

The corrected inferential three-variable regression performs much better:

- predictors: `audienceScore`, `initial_combined_sentiment_score`, `log_initial_review_count`
- cross-validated RMSE = `0.7218`
- test RMSE = `0.7133`
- test MAE = `0.5436`
- test `R^2 = 0.4378`

The full seven-variable candidate-pool regression improves slightly further:

- cross-validated RMSE = `0.7063`
- test RMSE = `0.7039`
- test MAE = `0.5309`
- test `R^2 = 0.4526`

## Feature Selection Results

The notebook applies two lecture-aligned model-selection methods: best-subset selection and forward-stepwise selection.

The selection rule is:

- primary criterion: lowest cross-validated RMSE
- tie-breakers: BIC and number of predictors
- if best-subset and forward-stepwise tie, report the best-subset model because it comes from exhaustive search

### Best-Subset Selection

The best-subset winner uses five predictors:

- `audienceScore`
- `tomatoMeter`
- `initial_top_critic_review_count`
- `initial_positive_review_ratio`
- `log_initial_review_count`

Its performance is:

- adjusted `R^2 = 0.4542`
- cross-validated RMSE = `0.7055`
- test RMSE = `0.7037`
- test MAE = `0.5308`
- test `R^2 = 0.4529`

### Forward-Stepwise Selection

Forward stepwise selection reaches the same five-feature model, just in a different order. It therefore produces the same predictive performance:

- adjusted `R^2 = 0.4542`
- cross-validated RMSE = `0.7055`
- test RMSE = `0.7037`
- test MAE = `0.5308`
- test `R^2 = 0.4529`

## Final Predictive Model

The selected final model is the **5-variable best-subset regression**. The forward-stepwise result is statistically equivalent, but the notebook reports the best-subset version as the final model for consistency.

The final predictive model uses:

- `audienceScore`
- `tomatoMeter`
- `initial_top_critic_review_count`
- `initial_positive_review_ratio`
- `log_initial_review_count`

This means the final predictive model explains about **45.3%** of the variation in `log_box_office` on unseen test data.

## Interpretation

The predictive analysis leads to several clear conclusions.

First, the mean-only benchmark performs poorly, which confirms that the selected movie-reaction and movie-context variables contain real predictive information.

Second, the corrected inferential three-variable model is a meaningful predictor, but it is slightly outperformed by the larger predictive models.

Third, both best-subset and forward-stepwise selection identify the same five-feature regression as the strongest interpretable predictive model in this dataset.

Fourth, the strongest predictive signals come from:

- early review volume
- audience and critic scores
- early top-critic attention
- early positive-review share

Finally, the selected model shows very similar cross-validation and held-out test performance, so strong overfitting is not indicated.
