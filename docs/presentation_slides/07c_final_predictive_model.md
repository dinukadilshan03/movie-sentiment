# Final Predictive Model

## Slide Purpose

Present the selected model, its predictors, and final held-out test performance.

## Final Selected Model

5-variable best-subset regression using:

- `audienceScore`
- `tomatoMeter`
- `initial_top_critic_review_count`
- `initial_positive_review_ratio`
- `log_initial_review_count`

## Performance

- CV RMSE: `0.7055`
- Test RMSE: `0.7037`
- Test MAE: `0.5308`
- Test R-squared: `0.4529`

## Figure

Use:

`images/predictive_final_model_slide.png`

## Speaker Note

The final model explains about 45.3% of unseen variation in logged box office. The strongest message is that early review volume and audience or critic reaction variables improve prediction compared with simple baselines.
