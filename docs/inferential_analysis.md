# Inferential Analysis

## Overview

This report presents the inferential analysis of the final movie-level dataset used for the box-office study. The purpose of this stage is to move beyond description and test whether audience reaction and early review behavior are significantly associated with movie popularity.

The analysis is based on secondary Rotten Tomatoes movie and review data processed into the final assignment dataset.

The response variable is `log_box_office`, and the main inferential model is:

`log_box_office ~ audienceScore + initial_combined_sentiment_score + log_initial_review_count + initial_sentiment_x_log_review_count`

Following the lecture framework, this stage uses:

- correlation-based relationship checks
- group comparison tests
- multiple linear regression estimated by Ordinary Least Squares (OLS)
- ANOVA / overall F-test interpretation
- coefficient-level significance testing
- regression-assumption diagnostics

The analysis is based on the final curated dataset and uses lecture-aligned terminology for hypotheses, significance testing, and regression interpretation.

## Research Question and Hypotheses

The central research question is:

**Do positive audience reactions improve content popularity?**

At the model level, the inferential analysis tests:

- **Null hypothesis (`H0`)**: There is no significant linear relationship between `log_box_office` and the explanatory variables `audienceScore`, `initial_combined_sentiment_score`, `log_initial_review_count`, and `initial_sentiment_x_log_review_count`.
- **Alternative hypothesis (`H1`)**: At least one of the regression coefficients differs from zero, meaning the predictors jointly have a significant linear relationship with `log_box_office`.

At the coefficient level, each predictor is tested using:

- `H0: beta_i = 0`
- `H1: beta_i != 0`

The level of significance used in the analysis is:

- `alpha = 0.05`

## Data Used for Inference

The raw final dataset contains 4,072 movies and 29 variables. For inferential analysis, the model requires `log_box_office` and the four selected predictors. After removing rows with missing values in these variables, the final inferential sample contains **3,747 observations**.

The inferential dataset is strong in terms of completeness:

- `initial_combined_sentiment_score`, `log_initial_review_count`, and `initial_sentiment_x_log_review_count` are fully populated in the retained sample
- `audienceScore` has only a small amount of missingness in the raw file
- `log_box_office` is already stored in the final dataset and matches the logged numeric box-office column exactly

Overall, the dataset is sufficiently large and complete for multiple regression and supporting hypothesis tests.

## Correlation and Group Comparison Results

Before fitting the full regression model, the notebook examines simpler inferential relationships.

### Correlation Results

Pearson correlation shows the following relationships with `log_box_office`:

- `log_initial_review_count`: `r = 0.6267`
- `audienceScore`: `r = 0.0841`
- `initial_combined_sentiment_score`: `r = -0.1387`
- `initial_sentiment_x_log_review_count`: `r = -0.0994`

These results indicate that early review volume is the strongest simple linear correlate of logged box office, while audience score has only a weak positive pairwise association. The sentiment variables show weak negative pairwise correlations with the response.

This is important because it shows that the full regression model must be interpreted jointly rather than by simple pairwise relationships alone.

### Group Comparison Results

The notebook compares `log_box_office` across `initial_combined_sentiment_label` groups using both ANOVA and Kruskal-Wallis tests.

The sentiment-group means are:

- negative: `7.2142`
- mixed: `7.1975`
- positive: `6.9494`

The inferential tests are both statistically significant:

- One-way ANOVA: `F = 34.8873`, `p < 0.001`
- Kruskal-Wallis: `statistic = 30.9764`, `p < 0.001`

This means that the average or distribution of `log_box_office` differs across sentiment groups. However, the direction of the group means shows that the relationship is not a simple "more positive sentiment means higher popularity" pattern.

The notebook also includes a supporting two-group comparison based on high versus low `audienceScore`. Those tests show significantly different central tendency between the two groups, but the full multivariable regression remains the main inferential test.

## Multiple Linear Regression Results

The core inferential model is a **multiple linear regression estimated by OLS** with HC3 robust standard errors.

### Overall Model Significance

The fitted model produces:

- Number of observations: `3,747`
- `R^2 = 0.4382`
- Adjusted `R^2 = 0.4376`
- Overall `F = 681.3789`
- Model `p < 0.001`

This means the model explains about **43.8%** of the variation in `log_box_office`, and the overall regression is statistically significant.

Using the model-level hypothesis test:

- **Decision**: Reject `H0`
- **Conclusion**: The full set of predictors jointly explains a statistically significant share of variation in `log_box_office`.

### Coefficient-Level Results

The fitted coefficients are:

- Intercept: `1.9628`, `p < 0.001`
- `audienceScore`: `0.0103`, `p < 0.001`
- `initial_combined_sentiment_score`: `-1.5620`, `p < 0.001`
- `log_initial_review_count`: `1.1579`, `p < 0.001`
- `initial_sentiment_x_log_review_count`: `0.2954`, `p < 0.001`

All four predictors are statistically significant at the 5% level.

The coefficient interpretation is not uniform in direction:

- `audienceScore` is a positive and significant predictor
- `log_initial_review_count` is also positive and strongly significant
- `initial_combined_sentiment_score` is negative and significant
- the interaction term is positive and significant

This means that the inferential result is more nuanced than a simple statement that "positive sentiment increases popularity." The interaction term indicates that the effect of early sentiment depends on review volume, so the predictors must be interpreted together rather than independently.

## ANOVA Interpretation

The lecture-aligned ANOVA view of the regression provides the following sums of squares and test values:

- `audienceScore`: `F = 47.1428`, `p < 0.001`
- `initial_combined_sentiment_score`: `F = 438.0429`, `p < 0.001`
- `log_initial_review_count`: `F = 2390.6635`, `p < 0.001`
- `initial_sentiment_x_log_review_count`: `F = 42.7628`, `p < 0.001`

This confirms that each term contributes significantly within the fitted model. Among the included predictors, `log_initial_review_count` contributes the strongest inferential signal in the ANOVA table.

## Regression Assumption Checks

The inferential notebook evaluates the five regression assumptions emphasized in the lecture notes.

### Linearity

Linearity is checked using:

- scatterplots with fitted regression lines
- residuals versus fitted values

The relationship is treated as **reasonably acceptable visually**. There is no strong evidence of a purely non-linear pattern, although this remains a visual judgment rather than a strict formal test.

### Multicollinearity

Multicollinearity is checked using VIF.

The raw fitted model shows:

- `audienceScore`: `VIF = 1.7831`
- `initial_combined_sentiment_score`: `VIF = 72.1515`
- `log_initial_review_count`: `VIF = 1.1522`
- `initial_sentiment_x_log_review_count`: `VIF = 72.2320`

This indicates a serious multicollinearity problem between the sentiment term and the interaction term in the raw specification.

The notebook therefore includes a centered robustness check. After centering the sentiment and review-count variables before forming the interaction, the VIF values drop to about:

- `sentiment_c`: `1.8037`
- `review_count_c`: `1.0572`
- `interaction_c`: `1.0671`

This shows that the interaction structure itself is not necessarily the problem, but the raw uncentered parameterization creates unstable collinearity.

### Homoscedasticity

Homoscedasticity is checked using:

- residuals versus fitted plot
- Breusch-Pagan test

The results are:

- Breusch-Pagan LM = `135.2182`, `p < 0.001`
- Breusch-Pagan F = `35.0233`, `p < 0.001`

This indicates heteroskedasticity. Because of this, the regression is reported with **HC3 robust standard errors**.

### Independence

Independence is checked through:

- study-design reasoning
- Durbin-Watson statistic

The Durbin-Watson statistic is:

- `1.9188`

For this movie-level cross-sectional dataset, independence is mainly a design assumption rather than something that can be completely established with a single test. The reported value does not indicate a strong serial-correlation problem, but the assumption is still treated as mostly justified by the study design.

### Normality

Normality is checked using:

- residual histogram
- Q-Q plot

The residuals are **not perfectly normal**, and the regression summary also shows non-normality through the omnibus and Jarque-Bera results. However, because the sample size is large, this is treated as less critical than the multicollinearity and heteroskedasticity issues.

## Robustness Interpretation

The assumption checks do not invalidate the analysis, but they do affect how confidently the regression coefficients should be interpreted.

The most important issues are:

- heteroskedasticity in the raw model
- strong multicollinearity between the sentiment term and the interaction term

The notebook addresses the first issue by using HC3 robust standard errors and addresses the second by adding a centered interaction robustness check.

The centered robustness model preserves the main qualitative conclusions:

- `audienceScore` remains positive and significant
- review-count intensity remains strongly important
- the interaction remains significant

This strengthens confidence that the interaction effect is real, even though the raw parameterization is difficult to interpret coefficient by coefficient.

## Summary of Main Findings

The inferential analysis leads to several clear conclusions.

First, the full multiple linear regression model is statistically significant overall, and the null hypothesis that the predictors jointly have no relationship with `log_box_office` is rejected.

Second, all four predictors in the planned inferential specification are statistically significant:

- `audienceScore`
- `initial_combined_sentiment_score`
- `log_initial_review_count`
- `initial_sentiment_x_log_review_count`

Third, the strongest inferential signal in the model comes from `log_initial_review_count`, which suggests that early review attention is a major factor associated with box-office popularity.

Fourth, the relationship between early sentiment and popularity is not simple. The sentiment main effect is negative, while the interaction with review volume is positive and significant. This indicates that sentiment should be interpreted together with review volume rather than on its own.

Fifth, the model assumptions are only partly satisfied. Linearity is acceptable, but heteroskedasticity is present, residual normality is imperfect, and multicollinearity is severe in the raw interaction model. The notebook responds to these issues with robust standard errors and a centered robustness analysis.

Overall, the inferential analysis supports the conclusion that audience reaction and early review behavior are significantly associated with movie popularity, but the strongest and clearest signal comes from early review volume, and the sentiment effect is conditional rather than uniformly positive.
