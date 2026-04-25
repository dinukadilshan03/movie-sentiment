# Final Decision

## Research Question

**Do positive audience reactions improve content popularity?**

## Statistical Decision

**Reject `H0`.**

The corrected inferential model is statistically significant:

- `F = 888.1409`
- model `p < 0.001`
- `R^2 = 0.4318`
- adjusted `R^2 = 0.4313`

This means the retained audience-reaction and early-review predictors jointly explain a statistically significant share of variation in `log_box_office`.

## Evidence Across the Three Analyses

Descriptive analysis:

- `log_initial_review_count` has the strongest simple relationship with popularity: `r = 0.6270`
- `audienceScore` is positive but weak at the pairwise level: `r = 0.0841`
- early sentiment does not show a simple positive box-office pattern by itself

Inferential analysis:

- `audienceScore`: positive and significant, coefficient `0.0107`, `p < 0.001`
- `log_initial_review_count`: positive and significant, coefficient `1.2176`, `p < 0.001`
- `initial_combined_sentiment_score`: negative after controls, coefficient `-0.4314`, `p < 0.001`
- VIF values are low, so the corrected model does not have serious multicollinearity
- HC3 robust standard errors are used because heteroskedasticity was detected

Predictive analysis:

- final model: 5-variable best-subset regression
- test RMSE: `0.7037`
- test MAE: `0.5308`
- test `R^2 = 0.4529`
- CV RMSE `0.7055` is close to test RMSE `0.7037`, so strong overfitting is not indicated

## Final Verdict

**Supported with qualification.**

The data support that positive audience reaction is significantly associated with popularity, especially through `audienceScore`, and that early review attention is a strong and consistent popularity signal.

However, the statement should not be presented as fully proven causally because:

- the data are observational secondary data
- the strongest evidence is for early review volume / attention, not sentiment positivity alone
- early sentiment is negative after controlling for audience score and review volume

## Slide Figure

Use:

`images/final_decision_slide.png`

## Speaker Note

Based on the inferential model, we reject the null hypothesis at the 5% level because the model is highly significant with `p < 0.001`. The evidence supports the idea that audience reaction and early review behavior are related to popularity. But the best final wording is “supported with qualification,” because the strongest signal is early review attention and the analysis shows association and prediction, not proven causation.
