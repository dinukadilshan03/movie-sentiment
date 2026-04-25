# Descriptive Analysis

## Present These Points

- Raw box office is **strongly right-skewed**, so `log_box_office` is used for analysis
- `audienceScore`, early sentiment, and review volume all show meaningful variation across movies
- **Early review volume** is the strongest simple descriptive signal of popularity
- Positive sentiment aligns with higher audience scores, but not with a simple increase in box office
- Descriptive checks include summary statistics, skewness, IQR, histograms, boxplots, grouped summaries, and correlations

## Strong Numbers To Mention

- Dataset size: **4,072 movies**
- Complete selected model rows: **3,747**
- Raw box-office skewness: **3.8015**
- `log_box_office` skewness: **-1.0381**
- Correlation with `log_box_office`:
  - `log_initial_review_count = 0.6270`
  - `audienceScore = 0.0841`

## Key Message

- Descriptively, popularity is linked more clearly to **early attention** than to sentiment alone
