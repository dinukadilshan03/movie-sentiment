# Final Report

## 1. Assignment Context

This project was completed as the group assignment for the module and follows the required assignment structure:

- selection of one analytical statement
- collection and preparation of relevant data
- justification of the statement using:
  - descriptive analytics
  - inferential analytics
  - predictive analytics
- analysis grounded in statistical modelling principles taught in the module

The work presented in this report is based on **secondary data**, not primary data.

## 2. Selected Analytical Statement

The selected analytical statement for this study is:

**Positive audience reactions improve content popularity.**

For this project:

- **audience reactions** are represented mainly by `audienceScore` and early review-based reaction features
- **content popularity** is represented by movie box-office performance, modeled as `log_box_office`

This report evaluates whether the statement is supported by the data using descriptive, inferential, and predictive analytics.

## 3. Data Source and Preparation

### 3.1 Data Source

The analysis uses secondary Rotten Tomatoes movie and review data processed into a final movie-level dataset stored in:

- `data/final/final.csv`

The dataset combines movie-level metadata with early review reaction features derived from reviews collected in the first 10 days after theatrical release.

### 3.2 Data Cleaning and Feature Construction

The project includes a structured cleaning and preparation pipeline:

- review text cleaning
- movie and review deduplication
- filtering of reviews to the first 10 days after release
- construction of early-review sentiment and review-volume features
- final movie-level dataset creation

The key constructed variables used in later stages are:

- `audienceScore`
- `initial_combined_sentiment_score`
- `log_initial_review_count`
- `initial_sentiment_x_log_review_count`
- `log_box_office`

### 3.3 Data Suitability

The final dataset is sufficiently large and complete for the assignment:

- descriptive stage used the final movie-level dataset
- inferential stage used 3,747 valid observations for regression
- predictive stage used 3,746 valid observations for prediction

This supports stable descriptive summaries, formal hypothesis testing, and train/test predictive evaluation.

## 4. Descriptive Analytics

### 4.1 Purpose

The descriptive stage was used to understand the structure, quality, and major patterns in the dataset before formal modelling.

### 4.2 Main Descriptive Findings

The descriptive analysis showed that:

- the dataset is generally clean and highly complete for the selected model variables
- raw box office is strongly right-skewed, so a logged outcome is more appropriate
- `audienceScore` is broadly distributed and shows meaningful variation across movies
- early review volume varies strongly across films and is one of the clearest descriptive signals of popularity
- early sentiment varies substantially, but its descriptive relationship with popularity is weaker and less straightforward

### 4.3 Descriptive Interpretation

The descriptive stage suggested that:

- popularity is more clearly associated with **early attention / review volume** than with sentiment polarity alone
- audience score is related to popularity, but only weakly at the simple pairwise level
- the sentiment variables overlap considerably with each other, especially the raw sentiment score and the interaction term

This stage provided the foundation for the inferential and predictive analyses.

## 5. Inferential Analytics

### 5.1 Purpose

The inferential stage tested whether the selected explanatory variables are significantly associated with `log_box_office`.

### 5.2 Methods Used

The inferential analysis used statistical modelling principles taught in the module, including:

- Pearson and Spearman correlation
- one-way ANOVA
- Kruskal-Wallis test
- Welch t-test
- Mann-Whitney U test
- multiple linear regression estimated by Ordinary Least Squares (OLS)
- ANOVA / overall F-test for regression
- coefficient significance tests
- regression assumption checks

### 5.3 Main Inferential Model

The main inferential model was:

`log_box_office ~ audienceScore + initial_combined_sentiment_score + log_initial_review_count + initial_sentiment_x_log_review_count`

### 5.4 Main Inferential Findings

The inferential analysis found that:

- the overall regression model is statistically significant
- the null hypothesis that the predictors jointly have no relationship with `log_box_office` is rejected
- all four predictors are statistically significant in the fitted model

Key model results:

- `R^2 = 0.4382`
- adjusted `R^2 = 0.4376`
- overall `F = 681.3789`
- model `p < 0.001`

Coefficient directions:

- `audienceScore`: positive and significant
- `initial_combined_sentiment_score`: negative and significant
- `log_initial_review_count`: positive and significant
- `initial_sentiment_x_log_review_count`: positive and significant

### 5.5 Inferential Interpretation

The inferential stage supports the conclusion that audience reaction and early review behavior are significantly related to popularity.

However, the result is **not a simple one-direction sentiment story**:

- audience score has a positive relationship with popularity
- early review volume is a very strong positive signal
- the main sentiment coefficient is negative
- the interaction term is positive, which means the effect of sentiment depends on review volume

Therefore, the statement is not validated in a simplistic form such as “more positive sentiment always directly increases popularity.” The relationship is more conditional and must be interpreted through the full model.

### 5.6 Inferential Gaps and Limitations

The inferential analysis also found several modelling limitations:

- heteroskedasticity is present
- residual normality is imperfect
- multicollinearity is severe in the raw interaction specification
- independence is mostly justified by study design rather than fully testable statistically

These issues were handled or documented by:

- using HC3 robust standard errors
- reporting regression diagnostics
- adding a centered interaction robustness check

So the inferential analysis is valid and defensible, but the coefficient interpretation requires caution.

## 6. Predictive Analytics

### 6.1 Purpose

The predictive stage evaluated how well movie popularity can be predicted on unseen data using an explainable regression workflow.

### 6.2 Methods Used

The predictive analysis followed the model-selection ideas from the lectures and used:

- fixed train/test split
- 5-fold cross-validation
- multiple linear regression
- best-subset selection
- forward-stepwise selection
- adjusted `R^2`
- AIC
- BIC
- RMSE
- MAE
- test-set `R^2`

### 6.3 Predictive Setup

The predictive target was:

- `log_box_office`

The analysis used:

- 80% training set
- 20% test set
- `random_state = 42`

Leakage variables were excluded from the predictor set:

- `boxOffice`
- `box_office_num`

### 6.4 Main Predictive Findings

The final predictive model was a **6-variable best-subset selected regression** using:

- `audienceScore`
- `tomatoMeter`
- `initial_top_critic_review_count`
- `initial_combined_sentiment_score`
- `log_initial_review_count`
- `initial_sentiment_x_log_review_count`

Its performance was:

- cross-validated RMSE = `0.7021`
- test RMSE = `0.6990`
- test MAE = `0.5236`
- test `R^2 = 0.4603`

This means the final predictive model explains about **46% of the variation** in `log_box_office` on unseen test data.

### 6.5 Predictive Interpretation

The predictive stage showed that:

- the selected reaction and review variables contain real predictive information
- the predictive model performs much better than a mean-only baseline
- the inferential four-variable model is useful, but not the strongest predictive model
- the best-subset and forward-stepwise procedures both point to the same six-feature solution
- overfitting is not strongly indicated, because cross-validation error and test error are very close

The strongest predictive signals come from:

- early review volume
- the sentiment × review-volume interaction
- critic score
- then audience score and related reaction variables

### 6.6 Predictive Gaps and Limitations

The predictive model is meaningful but not perfect.

The notebook shows that:

- some movies are predicted very accurately
- some movies have very large absolute prediction errors

This is expected because box office may also be influenced by factors not captured in the dataset, such as:

- marketing intensity
- franchise power
- release timing
- platform strategy
- distribution scale
- broader audience behavior

So the predictive model is useful, but it does not explain all variation in popularity.

## 7. Overall Justification of the Selected Statement

The assignment required the selected statement to be justified using descriptive, inferential, and predictive analytics. Taken together, the three stages provide the following conclusion.

### 7.1 What the Project Supports

The project supports that:

- audience reaction is related to popularity
- early review behavior is strongly related to popularity
- popularity can be predicted to a meaningful extent using audience and early-review features

### 7.2 What the Project Does Not Support in a Simple Form

The project does **not** support an oversimplified claim that:

- “positive sentiment alone directly and uniformly increases popularity”

That is not what the inferential model found.

### 7.3 Final Verdict on the Statement

The selected statement is best judged as:

**Partially supported / supported with qualification**

This is the most statistically accurate conclusion because:

- `audienceScore` is positively associated with popularity
- early review volume is a strong positive factor
- prediction improves meaningfully when reaction-related variables are used
- but the sentiment effects are mixed and interaction-dependent rather than uniformly positive

So the overall assignment conclusion should be:

**Positive audience reactions and early review behavior are meaningfully associated with content popularity, but the evidence suggests a conditional and multi-factor relationship rather than a simple direct positive effect of sentiment alone.**

## 8. Alignment with Assignment Requirements

### 8.1 Required Components

The assignment asked for:

- one analytical statement
- relevant data collection
- descriptive analytics
- inferential analytics
- predictive analytics
- justification based strictly on module-taught statistical modelling principles

This project satisfies those requirements as follows:

- **Analytical statement selected**: yes
- **Relevant data collected and prepared**: yes, using secondary Rotten Tomatoes data
- **Descriptive analytics completed**: yes
- **Inferential analytics completed**: yes
- **Predictive analytics completed**: yes
- **Use of taught statistical modelling methods**: yes

### 8.2 Learning Outcomes Alignment

The project also aligns well with the learning outcomes listed in the assignment brief:

- **LO1 / LO4**: data collection, cleaning, and preparation
- **LO2 / LO3 / LO4**: descriptive and inferential statistical analysis
- **LO3 / LO5**: predictive modelling and model comparison
- **LO2 / LO6**: interpretation and justification of findings
- **LO1–LO6**: viva defense of methods, assumptions, findings, and limitations

### 8.3 Bloom’s Taxonomy Alignment

The assignment emphasized Apply, Analyze, and Evaluate. This project demonstrates those levels clearly:

- **Apply**: data cleaning, feature creation, and use of taught models
- **Analyze**: descriptive, inferential, and predictive comparisons
- **Evaluate**: model diagnostics, feature selection, limitations, and final judgment on the statement

## 9. Gaps and Final Improvements Needed for Presentation/Viva

The technical work is complete, but for presentation and viva the following points should be stated clearly:

- this study uses **secondary data**
- the selected analytical statement should be shown explicitly on the slides
- the final conclusion should be presented as **qualified support**, not absolute proof
- the difference between descriptive, inferential, and predictive results should be explained clearly
- the limitations should be acknowledged openly:
  - multicollinearity
  - heteroskedasticity
  - omitted commercial factors
  - imperfect prediction for unusual films

These are not failures of the assignment. They strengthen the defense because they show critical statistical evaluation rather than overclaiming.

## 10. Final Conclusion

This assignment successfully completes the required descriptive, inferential, and predictive analytics workflow using statistical modelling techniques taught in the module.

The project shows that movie popularity can be meaningfully studied and predicted using audience reaction, critic reaction, and early review behavior. The strongest consistent signal across the analysis is early review volume, while audience score also contributes positively. However, the effect of sentiment is more complex than a simple direct positive relationship.

Therefore, the final academically defensible conclusion is:

**The selected statement is supported with qualification rather than fully proven in a simple form.**

This conclusion is well aligned with the assignment requirements and is grounded in the statistical evidence generated throughout the project.
