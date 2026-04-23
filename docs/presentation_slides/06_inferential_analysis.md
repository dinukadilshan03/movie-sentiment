# Inferential Analysis

## Present These Points

- Main model: `log_box_office ~ audienceScore + initial_combined_sentiment_score + log_initial_review_count + initial_sentiment_x_log_review_count`
- Method used: **OLS multiple regression** with **HC3 robust standard errors**
- Overall model is statistically significant
- All four predictors are significant in the fitted model

## Main Results

- `R^2 = 0.4382`
- Adjusted `R^2 = 0.4376`
- `F = 681.3789`
- `p < 0.001`

## Coefficient Directions

- `audienceScore`: positive
- `initial_combined_sentiment_score`: negative
- `log_initial_review_count`: positive
- `initial_sentiment_x_log_review_count`: positive

## Key Message

- Audience reaction matters, but the sentiment effect is **conditional**, not simply positive on its own
