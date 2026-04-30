# Movie Sentiment Analysis

> **Analytical statement:** *Positive audience reactions improve content popularity.*

This project investigates whether audience reactions and early review behaviour predict movie box-office performance. It uses a secondary Rotten Tomatoes dataset and applies **descriptive**, **inferential**, and **predictive** analytics to evaluate the statement above.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Dataset](#dataset)
- [Repository Structure](#repository-structure)
- [Pipeline](#pipeline)
- [Installation](#installation)
- [Usage](#usage)
- [Analysis Results](#analysis-results)
  - [Descriptive Analytics](#descriptive-analytics)
  - [Inferential Analytics](#inferential-analytics)
  - [Predictive Analytics](#predictive-analytics)
- [Final Conclusion](#final-conclusion)
- [Documentation](#documentation)

---

## Project Overview

The project tests whether positive audience reactions are associated with higher movie popularity, measured as log-transformed box-office revenue (`log_box_office`). The analysis pipeline:

1. Cleans and processes raw Rotten Tomatoes movie and review data.
2. Constructs an early-reaction dataset using only reviews submitted in the **first 10 days** after theatrical release.
3. Runs descriptive, inferential, and predictive analyses using explainable OLS regression.

---

## Dataset

| Item | Detail |
|---|---|
| Source | Secondary — Rotten Tomatoes movies & reviews |
| Final dataset | `data/final/final.csv` |
| Size | **4,072 movies**, 28 variables |
| Inferential sample | 3,747 observations |
| Predictive sample | 3,746 observations |
| Outcome variable | `log_box_office` (base-10 log of box-office revenue) |

### Key Variables

| Variable | Description |
|---|---|
| `audienceScore` | Rotten Tomatoes audience score (0–100) |
| `tomatoMeter` | Rotten Tomatoes critic score (0–100) |
| `initial_combined_sentiment_score` | Combined sentiment score from early reviews (−1 to 1) |
| `log_initial_review_count` | Log of the number of reviews submitted in the first 10 days |
| `initial_top_critic_review_count` | Number of top-critic reviews in the first 10 days |
| `initial_positive_review_ratio` | Share of positive reviews in the first 10 days |
| `log_box_office` | Base-10 log of box-office revenue (outcome) |

---

## Repository Structure

```
movie-sentiment/
├── data/
│   ├── rotten_tomatoes_movies.csv              # Raw movie metadata
│   ├── rotten_tomatoes_movie_reviews.csv       # Raw review data
│   ├── initial_reaction_10_days/               # 10-day reaction datasets
│   └── final/
│       └── final.csv                           # Source of truth for analysis
├── docs/
│   ├── descriptive_analysis.md                 # Descriptive analysis report
│   ├── inferential_analysis.md                 # Inferential analysis report
│   ├── predictive_analysis.md                  # Predictive analysis report
│   ├── final_report.md                         # Full project report
│   ├── presentation_summary.md                 # Presentation summary
│   └── presentation_slides/                    # Slide assets
├── images/                                     # Analysis visualisations
├── notebooks/
│   ├── descirpitve_analysys.ipynb              # Descriptive analysis notebook
│   ├── inferential_analysis.ipynb              # Inferential analysis notebook
│   └── predictive_analysis.ipynb               # Predictive analysis notebook
├── src/
│   ├── data_cleaninig.py                       # Text-cleaning script
│   ├── build_initial_reaction_dataset.py       # 10-day dataset builder
│   └── hypothesis_testing_10_day.py            # Hypothesis testing script
├── main.py                                     # Pipeline entry point
└── pyproject.toml                              # Project metadata and dependencies
```

---

## Pipeline

```
Raw reviews  ──►  data_cleaninig.py  ──►  Cleaned reviews
                                               │
                                               ▼
                              build_initial_reaction_dataset.py
                                               │
                                               ▼
                              data/final/final.csv  ──►  Analysis notebooks
```

1. **`src/data_cleaninig.py`** — Strips unsupported characters from review text fields and writes `data/rotten_tomatoes_movie_reviews_cleaned.csv`.
2. **`src/build_initial_reaction_dataset.py`** — Builds the 10-day movie-level dataset, keeping only reviews from the first 10 days after release and movies with at least 21 reviews in that window.
3. **Analysis notebooks** — Descriptive, inferential, and predictive stages each live in a dedicated Jupyter notebook.

---

## Installation

This project uses [uv](https://github.com/astral-sh/uv) for dependency management and requires **Python ≥ 3.14**.

```bash
# Clone the repository
git clone https://github.com/dinukadilshan03/movie-sentiment.git
cd movie-sentiment

# Install dependencies
pip install -e .
```

Or with uv:

```bash
uv sync
```

### Dependencies

| Package | Purpose |
|---|---|
| `pandas` | Data manipulation |
| `numpy` | Numerical operations |
| `matplotlib` / `seaborn` | Visualisation |
| `scikit-learn` | Predictive modelling and cross-validation |
| `statsmodels` | OLS regression and diagnostics |

---

## Usage

### Run the full data pipeline

```bash
python main.py
```

This runs cleaning and builds the 10-day initial-reaction dataset.

### Run hypothesis testing

```bash
python src/hypothesis_testing_10_day.py
```

### Run analysis notebooks

Open and run notebooks in order:

```bash
jupyter notebook notebooks/descirpitve_analysys.ipynb
jupyter notebook notebooks/inferential_analysis.ipynb
jupyter notebook notebooks/predictive_analysis.ipynb
```

---

## Analysis Results

### Descriptive Analytics

> Full report: [`docs/descriptive_analysis.md`](docs/descriptive_analysis.md)

**Key findings:**

- Raw box-office revenue is strongly right-skewed (skewness = 3.80), so `log_box_office` is used as the outcome.
- `audienceScore` varies substantially across movies (mean = 61.8, SD = 19.2).
- Early review sentiment is mixed: 47.96% positive, 33.10% negative, 18.93% mixed.
- Early review volume (`log_initial_review_count`) is the strongest simple predictor of box-office performance.

**Pearson correlations with `log_box_office`:**

| Variable | Correlation |
|---|---|
| `log_initial_review_count` | **0.6270** |
| `audienceScore` | 0.0841 |
| `initial_combined_sentiment_score` | −0.1381 |

**Grouped box-office by review-count quartile:**

| Quartile | Mean `log_box_office` |
|---|---|
| Q1 (lowest) | 6.18 |
| Q2 | 6.95 |
| Q3 | 7.40 |
| Q4 (highest) | 7.79 |

---

### Inferential Analytics

> Full report: [`docs/inferential_analysis.md`](docs/inferential_analysis.md)

**Research question:** Do positive audience reactions improve content popularity?

**Hypotheses:**
- **H₀**: No significant linear relationship between `log_box_office` and the explanatory variables.
- **H₁**: At least one predictor is significantly associated with `log_box_office`.

**Inferential model:**

```
log_box_office ~ audienceScore
               + initial_combined_sentiment_score
               + log_initial_review_count
```

**OLS regression results (HC3 robust standard errors, n = 3,747):**

| Metric | Value |
|---|---|
| R² | 0.4318 |
| Adjusted R² | 0.4313 |
| Overall F | 888.14 |
| Model p-value | < 0.001 |

**Coefficient summary:**

| Predictor | Coefficient | Direction | p-value |
|---|---|---|---|
| Intercept | 1.7078 | — | < 0.001 |
| `audienceScore` | 0.0107 | Positive ✅ | < 0.001 |
| `initial_combined_sentiment_score` | −0.4314 | Negative | < 0.001 |
| `log_initial_review_count` | 1.2176 | Positive ✅ | < 0.001 |

**Decision:** Reject H₀ — the model is statistically significant overall, and all three predictors are significant at α = 0.05.

**Assumption checks:**

| Assumption | Result |
|---|---|
| Multicollinearity (VIF) | All VIF < 2 — no issue |
| Homoscedasticity | Heteroskedastic (Breusch-Pagan p < 0.001) — HC3 SEs used |
| Independence | Durbin-Watson = 1.91 — acceptable |

---

### Predictive Analytics

> Full report: [`docs/predictive_analysis.md`](docs/predictive_analysis.md)

**Setup:** 80/20 train-test split, `random_state = 42`, 5-fold cross-validation.

**Model comparison:**

| Model | CV RMSE | Test RMSE | Test MAE | Test R² |
|---|---|---|---|---|
| Mean-only baseline | — | 0.9522 | 0.7515 | −0.0018 |
| Inferential (3-var) | 0.7218 | 0.7133 | 0.5436 | 0.4378 |
| Full candidate pool (7-var) | 0.7063 | 0.7039 | 0.5309 | 0.4526 |
| **Best-subset (5-var)** ✅ | **0.7055** | **0.7037** | **0.5308** | **0.4529** |
| Forward-stepwise (5-var) | 0.7055 | 0.7037 | 0.5308 | 0.4529 |

**Final predictive model — 5-variable best-subset regression:**

```
log_box_office ~ audienceScore
               + tomatoMeter
               + initial_top_critic_review_count
               + initial_positive_review_ratio
               + log_initial_review_count
```

The model explains **~45.3%** of the variation in `log_box_office` on unseen test data. Both best-subset and forward-stepwise selection converge on the same five features, confirming model stability.

---

## Final Conclusion

> Full report: [`docs/final_report.md`](docs/final_report.md)

The statement *"Positive audience reactions improve content popularity"* is **partially supported**.

- `audienceScore` is **positively** and significantly associated with box-office performance.
- `log_initial_review_count` (early review volume) is the **strongest and most consistent signal** across all three analysis stages.
- Early sentiment alone is not uniformly positive in its relationship to box office.
- The final predictive model explains about 45% of variance in unseen data — a meaningful result using only audience-reaction and review-behaviour features.

> **Final academically defensible conclusion:** Positive audience reactions and early review behaviour are meaningfully associated with content popularity, but the strongest evidence points to **early review volume** as the clearest signal of popularity.

---

## Documentation

| Document | Description |
|---|---|
| [`docs/descriptive_analysis.md`](docs/descriptive_analysis.md) | Full descriptive analysis report |
| [`docs/inferential_analysis.md`](docs/inferential_analysis.md) | Full inferential analysis report |
| [`docs/predictive_analysis.md`](docs/predictive_analysis.md) | Full predictive analysis report |
| [`docs/final_report.md`](docs/final_report.md) | Complete project report |
| [`docs/presentation_summary.md`](docs/presentation_summary.md) | Condensed presentation summary |
