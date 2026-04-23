# Presentation Summary

## Project Title

**Do positive audience reactions improve content popularity?**

This project evaluates that statement using descriptive, inferential, and predictive analytics on a secondary Rotten Tomatoes movie dataset.

## 1. Assignment Alignment

- Analytical statement selected: yes
- Relevant data collected: yes, using secondary data
- Descriptive analytics completed: yes
- Inferential analytics completed: yes
- Predictive analytics completed: yes
- Methods based on module statistical modelling lectures: yes

## 2. Data Used

- Source: secondary Rotten Tomatoes movie and review data
- Final dataset: `data/final/final.csv`
- Raw dataset size: `4,072` movies and `29` variables
- Inferential sample: `3,747`
- Predictive sample: `3,746`

## 3. Descriptive Analytics

Main descriptive findings:

- raw box office is strongly right-skewed
- `log_box_office` is more suitable for modelling
- `audienceScore` varies meaningfully across films
- early review volume is the strongest simple descriptive signal of popularity
- early sentiment is important, but its descriptive relationship with popularity is mixed

Descriptive conclusion:

- popularity appears to be related more clearly to early attention and review volume than to sentiment polarity alone

## 4. Inferential Analytics

Main inferential model:

`log_box_office ~ audienceScore + initial_combined_sentiment_score + log_initial_review_count + initial_sentiment_x_log_review_count`

Main inferential results:

- overall model significant
- `R^2 = 0.4382`
- adjusted `R^2 = 0.4376`
- `F = 681.3789`
- `p < 0.001`

Coefficient directions:

- `audienceScore`: positive and significant
- `initial_combined_sentiment_score`: negative and significant
- `log_initial_review_count`: positive and significant
- `initial_sentiment_x_log_review_count`: positive and significant

Inferential conclusion:

- audience reaction and early review behavior are significantly associated with popularity
- the effect of sentiment is conditional, not uniformly positive

## 5. Predictive Analytics

Predictive goal:

- predict `log_box_office` on unseen data using explainable regression

Predictive setup:

- 80/20 train-test split
- `random_state = 42`
- 5-fold cross-validation
- best-subset and forward-stepwise model selection

Final selected model:

- 6-variable best-subset regression

Predictors:

- `audienceScore`
- `tomatoMeter`
- `initial_top_critic_review_count`
- `initial_combined_sentiment_score`
- `log_initial_review_count`
- `initial_sentiment_x_log_review_count`

Predictive performance:

- cross-validated RMSE = `0.7021`
- test RMSE = `0.6990`
- test MAE = `0.5236`
- test `R^2 = 0.4603`

Predictive conclusion:

- movie popularity can be predicted to a meaningful extent using a compact, interpretable regression model

## 6. Final Verdict on the Statement

The statement:

**Positive audience reactions improve content popularity**

is best judged as:

**Supported with qualification**

Reason:

- audience score is positively associated with popularity
- early review volume is a strong positive signal
- predictive models improve clearly when reaction-related variables are included
- but sentiment alone does not show a simple uniform positive effect

Final conclusion:

**Audience reactions and early review behavior are meaningfully associated with content popularity, but the relationship is conditional and multi-factor rather than a simple direct positive effect of sentiment alone.**

## 7. Key Gaps and Limitations

- heteroskedasticity in the inferential model
- multicollinearity in the raw interaction specification
- residual normality is imperfect
- independence is mainly justified by study design
- predictive errors remain large for some unusual films
- box office is also influenced by omitted factors such as marketing, franchise strength, and release strategy

## 8. Viva Defense Points

- This is a **secondary data** study.
- The assignment required descriptive, inferential, and predictive analytics, and all three were completed.
- The analysis used statistical modelling methods taught in the module:
  - correlation
  - ANOVA
  - hypothesis testing
  - multiple linear regression / OLS
  - feature selection
  - predictive model evaluation
- The final conclusion is intentionally qualified because the evidence is statistically mixed across sentiment-related variables.
- Not overclaiming is a strength, not a weakness, because it reflects correct statistical interpretation.
