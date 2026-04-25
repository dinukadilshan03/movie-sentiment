# Inferential Analysis

## Overview

This report presents the inferential analysis of the final movie-level dataset used for the box-office study. The goal is to test whether audience reaction and early review behavior are significantly associated with movie popularity.

The response variable is `log_box_office`, and the corrected inferential model is:

`log_box_office ~ audienceScore + initial_combined_sentiment_score + log_initial_review_count`

The analysis uses:

- prerequisite checks for required columns and numeric types
- correlation-based relationship checks
- group comparison tests
- multiple linear regression estimated by OLS
- ANOVA / overall F-test interpretation
- coefficient-level significance testing
- regression-assumption diagnostics

## Research Question and Hypotheses

The central research question is:

**Do positive audience reactions improve content popularity?**

At the model level, the inferential analysis tests:

- **Null hypothesis (`H0`)**: There is no significant linear relationship between `log_box_office` and the explanatory variables `audienceScore`, `initial_combined_sentiment_score`, and `log_initial_review_count`.
- **Alternative hypothesis (`H1`)**: At least one regression coefficient differs from zero, meaning the predictors jointly have a significant linear relationship with `log_box_office`.

The level of significance is:

- `alpha = 0.05`

## Data Used for Inference

The raw final dataset contains 4,072 movies and 28 variables. After removing rows with missing values in the outcome and the three selected predictors, the final inferential sample contains **3,747 observations**.

The inferential dataset is strong in terms of completeness:

- `initial_combined_sentiment_score` and `log_initial_review_count` are fully populated in the retained sample
- `audienceScore` has only a small amount of missingness
- `log_box_office` is already stored in the final dataset and matches the logged numeric box-office column

The notebook also confirms that the final curated dataset contains **28 variables**, matching the corrected workflow.

## Correlation and Group Comparison Results

### Correlation Results

Pearson correlations with `log_box_office` are:

- `log_initial_review_count`: `r = 0.6267`
- `audienceScore`: `r = 0.0841`
- `initial_combined_sentiment_score`: `r = -0.1387`

These results indicate that early review volume is the strongest simple linear correlate of logged box office, while audience score has only a weak positive pairwise association.

### Group Comparison Results

The notebook compares `log_box_office` across `initial_combined_sentiment_label` groups using both ANOVA and Kruskal-Wallis tests.

The sentiment-group means are:

- negative: `7.2142`
- mixed: `7.1975`
- positive: `6.9494`

The inferential tests are both statistically significant:

- One-way ANOVA: `F = 34.8873`, `p < 0.001`
- Kruskal-Wallis: `statistic = 30.9764`, `p < 0.001`

The notebook also includes a supporting two-group comparison based on high versus low `audienceScore`:

- Welch t-test: `statistic = 3.6838`, `p < 0.001`
- Mann-Whitney U: `statistic = 1915164.5`, `p < 0.001`

## Multiple Linear Regression Results

The core inferential model is a **multiple linear regression estimated by OLS** with HC3 robust standard errors.

This model is explainable because each coefficient has a direct interpretation after controlling for the other retained predictors.

### Overall Model Significance

The fitted model produces:

- Number of observations: `3,747`
- `R^2 = 0.4318`
- Adjusted `R^2 = 0.4313`
- Overall `F = 888.1409`
- Model `p < 0.001`

This means the model explains about **43.2%** of the variation in `log_box_office`, and the overall regression is statistically significant.

Using the model-level hypothesis test:

- **Decision**: Reject `H0`
- **Conclusion**: The full set of predictors jointly explains a statistically significant share of variation in `log_box_office`.

### Coefficient-Level Results

The fitted coefficients are:

- Intercept: `1.7078`, `p < 0.001`
- `audienceScore`: `0.0107`, `p < 0.001`
- `initial_combined_sentiment_score`: `-0.4314`, `p < 0.001`
- `log_initial_review_count`: `1.2176`, `p < 0.001`

All three predictors are statistically significant at the 5% level.

Coefficient directions:

- `audienceScore` is positive and significant
- `initial_combined_sentiment_score` is negative and significant
- `log_initial_review_count` is positive and strongly significant

### ANOVA Interpretation

The lecture-aligned ANOVA view of the regression provides the following results:

- `audienceScore`: `F = 46.6226`, `p < 0.001`
- `initial_combined_sentiment_score`: `F = 433.2093`, `p < 0.001`
- `log_initial_review_count`: `F = 2364.2838`, `p < 0.001`

Among the included predictors, `log_initial_review_count` contributes the strongest inferential signal.

## Regression Assumption Checks

### Linearity

Linearity is checked using scatterplots with fitted lines and residuals versus fitted values. The relationship is treated as reasonably acceptable visually.

### Multicollinearity

Multicollinearity is checked using VIF.

The fitted model shows:

- `audienceScore`: `VIF = 1.7761`
- `initial_combined_sentiment_score`: `VIF = 1.7704`
- `log_initial_review_count`: `VIF = 1.0154`

These values do **not** indicate a serious multicollinearity problem in the accepted final model.

### Homoscedasticity

Homoscedasticity is checked using the Breusch-Pagan test:

- Breusch-Pagan LM = `125.7813`, `p < 0.001`
- Breusch-Pagan F = `43.3371`, `p < 0.001`

This indicates heteroskedasticity, so HC3 robust standard errors are reported.

### Independence

Independence is checked through study-design reasoning and the Durbin-Watson statistic:

- Durbin-Watson = `1.9080`

For this movie-level cross-sectional dataset, independence is treated mainly as a design assumption.

### Normality

Normality is checked using a residual histogram and a Q-Q plot. Residual normality is imperfect, but the large sample size reduces the severity of this issue for overall inference.

## Summary of Main Findings

The inferential analysis leads to several clear conclusions.

First, the corrected multiple linear regression model is statistically significant overall, and the null hypothesis that the predictors jointly have no relationship with `log_box_office` is rejected.

Second, all three predictors in the corrected inferential specification are statistically significant:

- `audienceScore`
- `initial_combined_sentiment_score`
- `log_initial_review_count`

Third, the strongest inferential signal in the model comes from `log_initial_review_count`, which suggests that early review attention is a major factor associated with box-office popularity.

Fourth, audience score has a positive association with popularity, while the simple early-sentiment measure remains negative in the multivariable model.

Finally, the corrected final model has low VIF values for the retained predictors, although heteroskedasticity still requires robust standard errors.
