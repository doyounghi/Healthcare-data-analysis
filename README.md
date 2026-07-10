# Healthcare Analytics and Data Science Portfolio

This repository contains healthcare analytics, machine learning, experimentation, and risk stratification portfolio projects focused on Medicaid/Medicare-style member analytics, outreach evaluation, quality improvement, cost modeling, and readmission-risk prioritization.

The projects use a mix of **synthetic healthcare-style datasets** and **public de-identified healthcare dataset**. Results are intended for portfolio, learning, and demonstration purposes. They should not be interpreted as real-world clinical, operational, or financial evidence.

## Recommended Review Path

For a fast review, start here:

| Review Goal | Recommended File |
| :--- | :--- |
| **Best Machine Learning Workflow** | `03_risk_stratification_intervention_prioritization/notebooks/05_model_comparison_and_threshold_strategy.ipynb` |
| **Best Risk Modeling Setup** | `03_risk_stratification_intervention_prioritization/notebooks/04_baseline_risk_modeling.ipynb` |
| **Best Statistical Analysis** | `02_diabetes_peer_support_ab_testing/notebooks/02_ab_test_primary_outcome.ipynb` |
| **Best Business Recommendation** | `02_diabetes_peer_support_ab_testing/notebooks/06_Business_Recommendation_Summary.ipynb` |

This path highlights the strongest recruiter-facing work: patient-aware readmission modeling, threshold-based outreach prioritization, randomized experiment analysis, and business recommendation development.

## Projects

### 01 — Synthetic Medicaid & Medicare Member Analytics

End-to-end healthcare analytics and machine learning project using synthetic Medicaid/Medicare-style member-level data.

This project demonstrates member-level healthcare analytics, Annual Wellness Visit completion modeling, monthly cost regression, model interpretation, and final project synthesis.

Main topics:

* Synthetic healthcare member data generation
* Medicaid/Medicare-style member analytics
* Annual Wellness Visit completion classification
* Monthly healthcare cost regression
* Feature engineering
* Model comparison
* Residual diagnostics
* Tree-based models
* Random Forest and Gradient Boosting
* Hyperparameter tuning
* Portfolio-ready project summary

Key files:

* `01_medicare_and_medicaid_member_analysis/README.md`
* `01_medicare_and_medicaid_member_analysis/notebooks/15_final_regression_model_comparison.ipynb`
* `01_medicare_and_medicaid_member_analysis/notebooks/16_project_summary.ipynb`

---

### 02 — Diabetes Peer Support A/B Testing and Outreach Evaluation

Healthcare experimentation project evaluating whether a Diabetes Peer Support outreach program improves diabetes testing compliance compared with Standard Outreach.

This project uses a synthetic randomized experiment design and follows an **intent-to-treat** framework. Members are analyzed based on randomized assignment rather than later enrollment or attendance behavior.

The primary outcome notebook focuses on treatment-effect estimation. The funnel notebook is operational: it evaluates outreach execution, drop-off, and participation flow after assignment.

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

Key notebooks:

* `02_diabetes_peer_support_ab_testing/notebooks/01_EDA_And_Randomization_Balance_Check.ipynb`
* `02_diabetes_peer_support_ab_testing/notebooks/02_ab_test_primary_outcome.ipynb`
* `02_diabetes_peer_support_ab_testing/notebooks/03_Peer_Support_Funnel_Analysis.ipynb`
* `02_diabetes_peer_support_ab_testing/notebooks/04_SDOH_Segment_Analysis.ipynb`
* `02_diabetes_peer_support_ab_testing/notebooks/05_adjusted_sensitivity_analysis.ipynb`
* `02_diabetes_peer_support_ab_testing/notebooks/06_Business_Recommendation_Summary.ipynb`

---

### 03 — Readmission Risk Stratification and Outreach Prioritization

Healthcare risk modeling project using the public UCI Diabetes 130-US Hospitals dataset to predict 30-day hospital readmission risk and translate predicted risk scores into a capacity-constrained outreach prioritization strategy.

This project is framed around a practical care-management question:

> How can a care management team identify high-risk encounters, rank them by predicted readmission risk, and prioritize limited outreach capacity?

The project uses encounter-level hospital data and includes leakage-aware feature engineering, patient-aware validation, baseline modeling, model comparison, and threshold strategy.

Main topics:

* Public de-identified healthcare dataset analysis
* 30-day readmission target creation
* Real-world missing-value handling
* Encounter-level vs patient-level unit-of-analysis review
* Patient-aware train/test splitting
* Leakage-aware feature selection
* Near-discharge prediction framing
* Feature engineering for utilization, diagnosis, medication, and missingness patterns
* Baseline Logistic Regression and Decision Tree modeling
* Candidate model comparison with Logistic Regression, Random Forest, and Gradient Boosting
* ROC AUC and PR AUC evaluation
* Grouped cross-validation
* Top 5%, Top 10%, and Top 20% risk-group analysis
* Lift over baseline
* Precision at k and recall at k
* Outreach capacity simulation
* Risk tier creation
* Threshold strategy for care management prioritization
* Calibration and causal interpretation caution

Key notebooks:

* `03_risk_stratification_intervention_prioritization/notebooks/00_project_setup_and_data_access_check.ipynb`
* `03_risk_stratification_intervention_prioritization/notebooks/01_data_cleaning_and_dictionary.ipynb`
* `03_risk_stratification_intervention_prioritization/notebooks/02_eda_and_outcome_analysis.ipynb`
* `03_risk_stratification_intervention_prioritization/notebooks/03_feature_engineering_and_leakage_review.ipynb`
* `03_risk_stratification_intervention_prioritization/notebooks/04_baseline_risk_modeling.ipynb`
* `03_risk_stratification_intervention_prioritization/notebooks/05_model_comparison_and_threshold_strategy.ipynb`

## Skills Demonstrated

**Languages and libraries:** Python, pandas, NumPy, matplotlib, scipy, statsmodels, scikit-learn

**Healthcare analytics:** Medicaid/Medicare-style member analytics, Annual Wellness Visit analytics, diabetes testing compliance, readmission risk, outreach prioritization, SDOH segment analysis

**Machine learning:** Feature engineering, classification modeling, regression modeling, model comparison, tree-based models, grouped train/test splitting, grouped cross-validation, ROC AUC, PR AUC, precision, recall, lift analysis, threshold strategy

**Experimentation and statistics:** Intent-to-treat A/B testing, baseline balance checks, standardized mean differences, two-proportion z-test, Welch's t-test, confidence intervals, p-values, logistic regression, odds ratio interpretation

**Business analytics:** Funnel analysis, subgroup analysis, risk tiering, outreach capacity simulation, business recommendation development, data storytelling, Git/GitHub project organization

## Repository Structure

```text
healthcare-analytics-portfolio/
|
|-- 01_medicare_and_medicaid_member_analysis/
|   |-- notebooks/
|   |-- data/
|   |-- src/
|   |-- requirements.txt
|   `-- README.md
|
|-- 02_diabetes_peer_support_ab_testing/
|   |-- notebooks/
|   |-- data/
|   |-- src/
|   |-- requirements.txt
|   `-- README.md
|
|-- 03_risk_stratification_intervention_prioritization/
|   |-- notebooks/
|   |-- data/
|   |-- outputs/
|   |-- requirements.txt
|   `-- README.md
|
`-- README.md
```

## About the Author

I am a healthcare data analyst focused on Medicaid/Medicare analytics, population health reporting, quality improvement, and risk stratification workflows.

My professional work includes SQL, Power BI, DAX, Excel, and healthcare dashboard development. This repository focuses on Python-based analytics and machine learning workflows that complement that business intelligence background.

I am also pursuing graduate-level analytics training through Georgia Tech OMSA.

LinkedIn: [Doyoung Kim](https://www.linkedin.com/in/doyoung-kim-hello/)

## Notes on Interpretation

These projects are portfolio demonstrations, not clinical decision tools.

Model predictions, experiment results, and business recommendations are intended to demonstrate analytical workflow design, statistical reasoning, machine learning implementation, and healthcare business interpretation. They should not be used for real clinical, financial, or operational decisions without external validation, governance review, and appropriate deployment controls.
