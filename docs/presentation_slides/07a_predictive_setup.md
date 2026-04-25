# Predictive Analysis Setup

## Slide Purpose

Explain how the predictive workflow is different from inferential analysis.

## Main Points

- Goal: predict `log_box_office` for unseen movies.
- Target variable: `log_box_office`.
- Candidate predictors: 7 explainable movie, audience, critic, and early-review variables.
- Modelling sample: 3,746 complete rows.
- Validation: 80/20 train-test split and 5-fold cross-validation on the training set.
- Selection rule: choose the model with the lowest cross-validated RMSE.

## Figure

Use:

`images/predictive_workflow_slide.png`

## Speaker Note

Inferential analysis asked whether the selected predictors are statistically significant. Predictive analysis asks whether an explainable model can accurately predict box-office popularity on movies not used to train the model.
