# Predictive Model

## Present These Points

- Goal: predict **`log_box_office`** for unseen movies using an interpretable model
- Setup: **80/20 train-test split**, `random_state = 42`, **5-fold cross-validation**
- Compared models: mean-only baseline, inferential 3-variable model, full model, best-subset, forward-stepwise
- Final selected model: **5-variable best-subset regression**
- Selection rule: lowest cross-validated RMSE, with test metrics used for final evaluation

## Final Predictors

- `audienceScore`
- `tomatoMeter`
- `initial_top_critic_review_count`
- `initial_positive_review_ratio`
- `log_initial_review_count`

## Key Message

- A compact explainable regression model predicts popularity better than the simpler baseline models
- Best-subset and forward-stepwise selection identify the same final feature set
