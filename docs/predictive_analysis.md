# Predictive Analysis

## Overview

This report presents the predictive analysis of the final movie-level dataset used for the box-office study. The purpose of this stage is to evaluate how well movie popularity can be predicted on unseen data using an explainable regression workflow that is aligned with the course lectures on linear regression and feature selection.

The analysis is based on secondary Rotten Tomatoes movie and review data processed into the final assignment dataset.

The predictive target is `log_box_office`. The analysis is predictive rather than causal: the goal is to minimize prediction error while retaining an interpretable model.

The notebook compares several regression models using a fixed training and test split, 5-fold cross-validation, and the model-selection criteria discussed in the lectures:

- adjusted `R^2`
- AIC
- BIC
- cross-validated RMSE

The final predictive workflow compares the following models:

- Baseline mean-only predictor
- The four-variable regression carried forward from the inferential stage
- A full candidate-pool multiple linear regression
- A best-subset selected regression
- A forward-stepwise selected regression

## Dataset Preparation for Prediction

The raw final dataset contains 4,072 movies and 29 variables. For predictive modeling, the response variable is `log_box_office`, and the candidate predictor pool contains eight variables:

- `audienceScore`
- `tomatoMeter`
- `runtimeMinutes`
- `initial_top_critic_review_count`
- `initial_positive_review_ratio`
- `initial_combined_sentiment_score`
- `log_initial_review_count`
- `initial_sentiment_x_log_review_count`

To avoid target leakage, `boxOffice` and `box_office_num` are not used as predictors. They are kept only for interpretation and error review after prediction.

The raw review-count variables `initial_review_count`, `initial_positive_review_count`, and `initial_negative_review_count` are also excluded from the main candidate pool. They are highly redundant with the logged review-count and derived sentiment features and would add collinearity without improving the interpretability of the predictive story.

After removing rows with missing values in the target or the selected predictors, 3,746 movies remain for predictive analysis. This provides a large and stable modeling sample for train/test evaluation and subset selection.

## Train/Test Setup

The predictive workflow uses a fixed split so that results are reproducible:

- 80% training data
- 20% test data
- `random_state = 42`

This produces:

- 2,996 training observations
- 750 test observations

All model selection is performed using 5-fold cross-validation on the training set only. The held-out test set is reserved for final predictive evaluation.

This separation is important because it allows the analysis to distinguish between models that fit the training data well and models that actually generalize well to unseen observations.

## Baseline Predictive Models

The first comparison evaluates the benchmark models before feature selection.

### Baseline 0: Mean-only Predictor

The simplest benchmark predicts the same average `log_box_office` value for every movie. As expected, this performs poorly:

- Test RMSE = 0.9522
- Test MAE = 0.7515
- Test `R^2` = -0.0018

This model provides the minimum standard that all useful predictive models should improve upon.

### Model 1: Inferential Four-Variable Regression

The four-variable regression from the inferential stage uses:

- `audienceScore`
- `initial_combined_sentiment_score`
- `log_initial_review_count`
- `initial_sentiment_x_log_review_count`

Its predictive performance is:

- Cross-validated RMSE = 0.7178
- Test RMSE = 0.7094
- Test MAE = 0.5362
- Test `R^2` = 0.4440

This model is clearly much better than the mean-only benchmark and remains a strong interpretable predictor, but it is not the best-performing model in the final comparison.

### Model 2: Full Candidate-Pool Regression

The full eight-predictor regression includes all selected candidate features. Its predictive performance is:

- Cross-validated RMSE = 0.7028
- Test RMSE = 0.7003
- Test MAE = 0.5240
- Test `R^2` = 0.4582

This model improves on the inferential four-variable model and gives the best training fit among the compared models, but the improvement is small relative to the more compact selected models.

## Feature Selection Results

The predictive notebook applies two model-selection methods from the lecture material: best-subset selection and forward-stepwise selection.

### Best-Subset Selection

All non-empty subsets of the eight predictors are evaluated on the training set. This means 255 subsets are compared in total.

The best-subset search shows a steady improvement as variables are added, but the gains become very small once the model reaches about five or six predictors. The best subset according to the declared ranking rule uses six predictors:

- `audienceScore`
- `tomatoMeter`
- `initial_top_critic_review_count`
- `initial_combined_sentiment_score`
- `log_initial_review_count`
- `initial_sentiment_x_log_review_count`

Its selection statistics are:

- adjusted `R^2` = 0.4593
- AIC = 6405.11
- BIC = 6447.15
- cross-validated RMSE = 0.7021

### Forward-Stepwise Selection

Forward stepwise selection starts from the intercept-only model and adds one variable at a time. The forward-stepwise winner also reaches a six-predictor model, and in this dataset it arrives at the same final feature set as the best-subset winner, just in a different order.

Its final statistics are identical:

- adjusted `R^2` = 0.4593
- AIC = 6405.11
- BIC = 6447.15
- cross-validated RMSE = 0.7021

This agreement between best-subset and forward-stepwise selection strengthens confidence that the chosen six-variable model is not an unstable or arbitrary result.

## Final Model Comparison

The final model is selected using the stated decision rule:

1. Lowest cross-validated RMSE
2. Lower test RMSE if needed
3. Lower BIC if still tied
4. Fewer predictors if still tied

The compared models produce the following main results:

- Baseline 0: mean-only predictor
  - Test RMSE = 0.9522
  - Test `R^2` = -0.0018
- Model 1: inferential four-variable regression
  - Test RMSE = 0.7094
  - Test `R^2` = 0.4440
- Model 2: full candidate-pool regression
  - Test RMSE = 0.7003
  - Test `R^2` = 0.4582
- Model 3: best-subset selected regression
  - Test RMSE = 0.6990
  - Test MAE = 0.5236
  - Test `R^2` = 0.4603
- Model 4: forward-stepwise selected regression
  - Test RMSE = 0.6990
  - Test MAE = 0.5236
  - Test `R^2` = 0.4603

The selected final model is **Model 3: Best-subset selected regression**. Model 4 is statistically equivalent in this dataset, but the notebook selects Model 3 under the stated rule.

## Interpretation of the Final Predictive Model

The selected model uses six predictors:

- `audienceScore`
- `tomatoMeter`
- `initial_top_critic_review_count`
- `initial_combined_sentiment_score`
- `log_initial_review_count`
- `initial_sentiment_x_log_review_count`

This result suggests that the strongest predictive signal comes from a combination of:

- audience reaction
- critic reaction
- early review attention
- early sentiment intensity and its interaction with review volume

The standardized coefficient view shows that the most influential predictors in the final linear model are:

1. `log_initial_review_count`
2. `initial_sentiment_x_log_review_count`
3. `tomatoMeter`
4. `initial_combined_sentiment_score`
5. `audienceScore`
6. `initial_top_critic_review_count`

This indicates that early review attention and the interaction between sentiment and review volume are the most powerful components of the final predictive model, while audience score still contributes useful predictive information but is not the single dominant feature.

## Overfitting Check

The selected model has:

- Cross-validated RMSE = 0.7021
- Test RMSE = 0.6990

The difference between test RMSE and cross-validated RMSE is approximately -0.0031, which is very small. This indicates that the selected model generalizes consistently from the training set to the held-out test set.

There is no strong evidence of overfitting in the final selected model.

By contrast, the full eight-variable regression achieves the best training fit, but it does not improve held-out prediction enough to justify the extra complexity.

## Prediction Diagnostics and Error Behavior

The final notebook includes several diagnostic views for the selected model:

- actual vs predicted `log_box_office`
- residuals vs predicted values
- distribution of prediction errors
- a table of the largest absolute prediction errors

These diagnostics show that the model performs reasonably well for many films, but it still struggles with a small number of unusual cases. Some movies are predicted far too high or far too low relative to their true box office. This is expected in movie-performance data because commercial success can sometimes be driven by factors not included in the model, such as franchise effects, release strategy, marketing intensity, seasonal timing, or unusual audience behavior.

Examples of the largest prediction errors include movies such as:

- *A Glitch in the Matrix*
- *The Wicker Man*
- *The Apparition*
- *Summerland*
- *Paranormal Activity*
- *Black Swan*

These large residual cases show that even the best selected linear model cannot fully capture every type of box-office outcome.

At the same time, the back-transformed example table shows that some films are predicted very closely, with very small log-scale errors. This confirms that the model is genuinely useful on many typical observations even though it misses some exceptional ones.

## Summary of Main Findings

The predictive analysis leads to several clear conclusions.

First, the final dataset is large enough for a reliable predictive regression workflow, and after filtering there are 3,746 usable observations for modeling.

Second, the mean-only benchmark performs poorly, which confirms that the selected movie-reaction and movie-context variables contain real predictive information.

Third, the inferential four-variable model is a strong predictor, but it is slightly outperformed by the larger predictive models.

Fourth, both best-subset selection and forward-stepwise selection identify the same six-variable regression as the strongest interpretable predictive model in this dataset.

Fifth, the final selected model achieves:

- Cross-validated RMSE = 0.7021
- Test RMSE = 0.6990
- Test MAE = 0.5236
- Test `R^2` = 0.4603

This means the model explains about 46% of the variation in `log_box_office` on unseen test data.

Finally, the predictive results show that early review volume and sentiment-volume interaction are especially important for prediction, while audience score and critic score also add useful signal. The chosen model improves predictive accuracy without becoming unnecessarily complex.

Overall, the predictive analysis supports the conclusion that movie popularity can be predicted to a meaningful extent using a compact, interpretable regression model built from audience reaction, critic reaction, and early review behavior.
