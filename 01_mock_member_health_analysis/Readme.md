# Mock Member Health Analysis

Practice project for Python, data analysis, and introductory machine learning.

## Notebook 1 : Explornatory Data Analysis

This notebook performs initial exploratory analysis on a synthetic healthcare member dataset. Each row represents one health plan member with demographic, plan, SDOH, utilization, cost, PCP attribution, and AWV completion fields.

The analysis checks data structure, missing values, duplicate member IDs, categorical distributions, numeric ranges, and basic visualizations. It also compares cost, utilization, and AWV completion patterns across plan type, region, PCP attribution, chronic condition burden, engagement quartiles, and age groups.

Key findings:
- DSNP members showed higher average SDOH risk, ED visits, and monthly cost.
- Rural members showed higher average SDOH risk, lower engagement, and higher ED utilization.
- PCP-attributed members had higher AWV completion and lower average utilization.
- AWV completion increased strongly across engagement score quartiles.
- Non-AWV-compliant members had higher average monthly cost in this synthetic dataset.

These findings are descriptive and should not be interpreted causally.

### Notebook 2 : Feature Engineering

- Loaded the EDA-ready synthetic healthcare member dataset from the prior notebook.
- Created stakeholder-friendly analytical features including age group, engagement quartile, chronic burden group, SDOH risk quartile, prior AWV group, PCP attribution status, acute utilization flag, and high-cost member flag.
- Defined high-cost members as the top 25% of monthly cost, creating a potential future classification target.
- Validated engineered features by checking distributions and grouped summaries.
- Found that higher chronic burden, higher acute utilization, older age, and higher SDOH risk were associated with higher average monthly cost.
- Found that AWV completion was higher among members with stronger engagement and prior AWV history.
- Exported the analysis-ready dataset to `data/processed/member_analysis_ready.csv`.

These findings are descriptive and based on synthetic data. They should not be interpreted causally.

### Notebook 3 : Modeling Baseline

- Built baseline classification models to predict current-year Annual Wellness Visit (AWV) completion.
- Used `awv_completed` as the binary target variable.
- Reviewed the synthetic data-generation logic to confirm which predictors were created before the AWV outcome.
- Excluded identifier fields, cost-related outcome variables, full-dataset quartile features, and redundant engineered grouping variables from the predictor set.
- Specifically excluded `member_id`, `monthly_cost`, `high_cost_member`, `engagement_group`, `sdoh_risk_group`, `age_group`, `chronic_burden_group`, `pcp_status`, `total_acute_visits`, `acute_utilization_group`, `has_acute_utilization`, `prior_awv_count`, and `prior_awv_group`.
- Split the data into training and test sets using an 80/20 stratified split.
- Applied one-hot encoding to categorical variables and standard scaling to numeric variables using a scikit-learn preprocessing pipeline.
- Compared Logistic Regression and Decision Tree Classifier baseline models.
- Evaluated performance using accuracy, precision, recall, F1 score, ROC AUC, confusion matrix, and classification report.
- Logistic Regression performed better than the Decision Tree, with ROC AUC of 0.76 and F1 score of 0.71.
- Treated Logistic Regression as the stronger baseline model for future threshold tuning, coefficient interpretation, and model comparison.
- Results should be interpreted as baseline model performance only, not as a final production model.
