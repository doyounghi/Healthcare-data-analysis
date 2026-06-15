# Synthetic Healthcare Data Analysis Portfolio

This repository contains healthcare analytics, machine learning, and experimentation portfolio projects focused on Medicaid/Medicare-style member data, cost prediction, outreach analysis, quality improvement, and healthcare program evaluation.

#### This repository uses synthetic healthcare-style data created for portfolio and learning purposes. Results should not be interpreted as real-world clinical, operational, or financial evidence.

## Recommended Review Path

For a quick technical review, start with the strongest recruiter-facing materials:

1. `02_diabetes_peer_support_ab_testing/README.md`
2. `02_diabetes_peer_support_ab_testing/notebooks/02_ab_test_primary_outcome.ipynb`
3. `02_diabetes_peer_support_ab_testing/notebooks/06_Business_Recommendation_Summary.ipynb`
4. `01_mock_member_health_analysis/Readme.md`
5. `01_mock_member_health_analysis/notebooks/15_final_regression_model_comparison.ipynb`
6. `01_mock_member_health_analysis/notebooks/16_project_summary.ipynb`

This path highlights the strongest project narratives first: randomized experiment analysis, business recommendation, model comparison, and project-level synthesis.

## Projects

### 01_mock_member_health_analysis

End-to-end healthcare analytics and machine learning project using synthetic member-level data.

Main topics:

* Synthetic healthcare data generation
* Exploratory data analysis
* Feature engineering
* AWV completion classification
* Monthly cost regression
* Model interpretation
* Residual diagnostics
* Tree-based models
* Random Forest and Gradient Boosting
* Hyperparameter tuning
* Final regression model comparison
* Portfolio-ready project summary

---

### 02_diabetes_peer_support_ab_testing

Healthcare A/B testing project evaluating whether a Diabetes Peer Support outreach program improves diabetes testing compliance compared with Standard Outreach.

This project uses a synthetic randomized experiment design and follows an intent-to-treat framework. Members are analyzed based on randomized assignment rather than later enrollment or attendance behavior.

Main topics:

* Synthetic healthcare outreach data generation
* Randomized treatment/control assignment
* Intent-to-treat A/B testing
* Baseline balance validation
* Standardized mean differences
* Two-proportion z-test
* Welch's t-test
* Absolute lift and relative lift
* Confidence intervals and p-values
* Peer-support funnel analysis
* SDOH segment analysis
* Adjusted regression sensitivity analysis
* Logistic regression and odds ratios
* Business recommendation summary
* Healthcare outreach interpretation

Key notebooks:

* `01_EDA_And_Randomization_Balance_Check.ipynb`
* `02_ab_test_primary_outcome.ipynb`
* `03_Peer_Support_Funnel_Analysis.ipynb`
* `04_SDOH_Segment_Analysis.ipynb`
* `05_adjusted_sensitivity_analysis.ipynb`
* `06_Business_Recommendation_Summary.ipynb`

## Skills Demonstrated

* Python
* pandas
* NumPy
* matplotlib
* scipy
* statsmodels
* scikit-learn
* healthcare analytics
* Medicaid/Medicare-style member analytics
* exploratory data analysis
* synthetic data generation
* feature engineering
* classification modeling
* regression modeling
* model comparison
* residual diagnostics
* A/B testing
* randomized experiment analysis
* intent-to-treat interpretation
* baseline balance checks
* standardized mean differences
* statistical hypothesis testing
* confidence interval interpretation
* logistic regression
* odds ratio interpretation
* subgroup and segment analysis
* funnel analysis
* business recommendation development
* data storytelling
* Git/GitHub project organization

## Repository Structure

```text
synthetic-data-analysis/
|
|-- 01_mock_member_health_analysis/
|   |-- notebooks/
|   |-- data/
|   |-- src/
|   |-- requirements.txt
|   `-- Readme.md
|
|-- 02_diabetes_peer_support_ab_testing/
|   |-- notebooks/
|   |-- data/
|   |-- src/
|   |-- requirements.txt
|   `-- README.md
|
`-- README.md
```
