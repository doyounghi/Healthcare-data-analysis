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

### Notebook 4: Model Interpretation and Threshold Tuning

- Rebuilt the baseline Logistic Regression model for AWV completion prediction using the cleaned predictor set from Notebook 3.
- Excluded cost-related outcome variables, full-dataset quartile features, and redundant engineered grouping variables to keep coefficient interpretation cleaner.
- Split the data into training, validation, and test sets so threshold tuning could be performed on validation data while preserving a final untouched test set.
- Applied one-hot encoding to categorical variables and standard scaling to numeric variables using a scikit-learn pipeline.
- Evaluated the model using accuracy, precision, recall, F1 score, ROC AUC, confusion matrix, and classification report.
- Extracted Logistic Regression coefficients and converted them into odds ratios for interpretation.
- Interpreted numeric coefficients as one-standard-deviation changes because numeric predictors were standardized.
- Interpreted categorical coefficients relative to omitted reference categories because one-hot encoding used `drop="first"`.
- Tested classification thresholds from 0.30 to 0.70 and selected 0.40 based on validation F1 score.
- Applied the selected 0.40 threshold once to the final test set, producing test recall of 0.84 and test F1 score of 0.73.
- Results are based on synthetic data and should be interpreted as baseline model behavior, not causal effects or final production performance.