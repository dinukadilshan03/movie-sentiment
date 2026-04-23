# Predictive Model

## Present These Points

- Goal: predict **`log_box_office`** for unseen movies using an interpretable model
- Setup: **80/20 train-test split**, `random_state = 42`, **5-fold cross-validation**
- Compared models: mean-only baseline, inferential 4-variable model, full model, best-subset, forward-stepwise
- Final selected model: **6-variable best-subset regression**

## Final Predictors

- `audienceScore`
- `tomatoMeter`
- `initial_top_critic_review_count`
- `initial_combined_sentiment_score`
- `log_initial_review_count`
- `initial_sentiment_x_log_review_count`

## Key Message

- A compact explainable regression model predicts popularity better than the simpler baseline models
