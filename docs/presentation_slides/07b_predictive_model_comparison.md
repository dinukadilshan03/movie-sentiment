# Predictive Model Comparison

## Slide Purpose

Show that multiple explainable regression models were compared before choosing the final model.

## Models Compared

- Mean-only baseline
- Inferential 3-variable regression
- Full 7-variable candidate model
- Best-subset regression
- Forward-stepwise regression

## Key Results

- Mean-only baseline test RMSE: `0.9522`
- Inferential 3-variable model test RMSE: `0.7133`
- Full candidate model test RMSE: `0.7039`
- Best-subset 5-variable model test RMSE: `0.7037`
- Forward-stepwise selected the same 5-variable model.

## Figure

Use:

`images/predictive_model_comparison.png`

## Speaker Note

The baseline model performs worst, which means the predictors contain useful signal. The best-subset and forward-stepwise methods both selected the same final feature set, so the final model choice is stable.
