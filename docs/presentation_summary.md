# Presentation Summary

## 1. Project Focus

This project evaluates the statement:

**Positive audience reactions improve content popularity.**

The study uses descriptive, inferential, and predictive analytics on a secondary Rotten Tomatoes movie dataset.

## 2. Data and Variables

- Final dataset: `data/final/final.csv`
- Final dataset size: `4,072` movies and `28` variables
- Inferential sample: `3,747`
- Predictive sample: `3,746`
- Outcome variable: `log_box_office`

Main retained explanatory variables:

- `audienceScore`
- `initial_combined_sentiment_score`
- `log_initial_review_count`

## 3. Descriptive Analytics

Main descriptive findings:

- raw box office is strongly right-skewed, so `log_box_office` is more suitable for analysis
- `audienceScore`, early sentiment, and early review volume all vary meaningfully across movies
- the clearest simple descriptive relationship with popularity is `log_initial_review_count`

Key descriptive correlations with `log_box_office`:

- `log_initial_review_count = 0.6270`
- `audienceScore = 0.0841`
- `initial_combined_sentiment_score = -0.1381`

Descriptive conclusion:

- popularity is linked more clearly to **early attention** than to sentiment alone

## 4. Inferential Analytics

Corrected inferential model:

`log_box_office ~ audienceScore + initial_combined_sentiment_score + log_initial_review_count`

Method:

- explainable OLS regression
- HC3 robust standard errors
- VIF and residual diagnostics

Main results:

- `R^2 = 0.4318`
- adjusted `R^2 = 0.4313`
- overall `F = 888.1409`
- model `p < 0.001`

Coefficient directions:

- `audienceScore`: positive and significant
- `initial_combined_sentiment_score`: negative and significant
- `log_initial_review_count`: positive and significant

Inferential conclusion:

- the corrected regression model is statistically significant, and early review volume is the strongest signal in the model

## 5. Predictive Analytics

Predictive setup:

- `80/20` train-test split
- `random_state = 42`
- `5-fold` cross-validation

Final selected predictive model:

- `audienceScore`
- `tomatoMeter`
- `initial_top_critic_review_count`
- `initial_positive_review_ratio`
- `log_initial_review_count`

Selection method:

- compare baseline, inferential, full, best-subset, and forward-stepwise models
- select by cross-validated RMSE, with test-set metrics for final evaluation

Predictive performance:

- cross-validated RMSE = `0.7055`
- test RMSE = `0.7037`
- test MAE = `0.5308`
- test `R^2 = 0.4529`

Predictive conclusion:

- the final predictive model explains about **45%** of the variation in unseen `log_box_office`

## 6. Final Conclusion

The project supports the statement only with qualification.

- `audienceScore` is positively associated with popularity
- early review volume is the strongest and most consistent signal
- early sentiment is relevant, but not in a simple uniformly positive way

The corrected final workflow uses a simpler retained predictor set with low VIF values and clearer interpretation.
