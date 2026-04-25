# Inferential Analysis

## Present These Points

- Main model: `log_box_office ~ audienceScore + initial_combined_sentiment_score + log_initial_review_count`
- Method used: **OLS multiple regression** with **HC3 robust standard errors**
- Diagnostics checked: **VIF**, residual plots, Breusch-Pagan, Durbin-Watson
- Overall model is statistically significant
- All three predictors are significant in the fitted model

## Main Results

- `R^2 = 0.4318`
- Adjusted `R^2 = 0.4313`
- `F = 888.1409`
- `p < 0.001`

## Coefficient Directions

- `audienceScore`: positive
- `initial_combined_sentiment_score`: negative
- `log_initial_review_count`: positive

## Key Message

- Audience reaction matters, but the strongest inferential signal is **early review volume**
- The corrected model is explainable and has low VIF values for the retained predictors
