# Risk Stratification and Intervention Prioritization

A healthcare data science project using public diabetes hospital readmission data to predict 30-day readmission risk and translate model scores into a capacity-constrained outreach prioritization strategy.

Although this project uses healthcare data, the core workflow is transferable to many industries where teams must rank high-risk cases and prioritize limited intervention capacity.

## Project Objective

The goal is to identify diabetic inpatient encounters with higher predicted 30-day readmission risk and prioritize post-discharge outreach when care management capacity is limited.

## Dataset

This project uses the UCI Diabetes 130-US Hospitals for Years 1999–2008 dataset.

The dataset contains 101,766 hospital encounter records for patients diagnosed with diabetes and supports a classification task related to early readmission within 30 days after discharge.

## Raw Data Access

The raw dataset files are not committed to this repository because the `data/` directory is gitignored.

To reproduce the project, download the UCI Diabetes 130-US Hospitals for Years 1999–2008 dataset from the UCI Machine Learning Repository:

```text
https://archive.ics.uci.edu/ml/datasets/diabetes+130-us+hospitals+for+years+1999-2008
```

After downloading and extracting the dataset, place the required raw files in:

```text
data/raw/
```

Expected raw files:

```text
data/raw/diabetic_data.csv
data/raw/IDS_mapping.csv
```

The project notebooks expect these exact filenames and paths. Notebook 00 checks whether both files exist before the cleaning and modeling workflow begins.

## Business Question

Can historical hospital encounter data be used to identify higher-risk diabetic patients and prioritize post-discharge outreach under limited care management capacity?

## Primary Target

The primary binary target identifies readmissions occurring within a 30-day window:

```python
readmitted_30d = 1 if readmitted == "<30" else 0
```

## Environment & Setup

This project is designed for execution within a standard Python virtual environment.

Recommended setup:

```bash
python -m venv .venv
```

Activate the virtual environment:

```bash
# Windows
.venv\Scripts\activate
```

```bash
# macOS / Linux
source .venv/bin/activate
```

Core dependency for Notebook 00:

```text
pandas
```

Later notebooks will add additional modeling, statistical, and visualization dependencies such as `numpy`, `scikit-learn`, `statsmodels`, and plotting libraries.

## Project Workflow

Across the full project, the workflow will cover:

* Project setup and raw data validation
* Data cleaning and missing-value handling
* Feature engineering
* Leakage-aware feature selection
* Classification modeling
* Model evaluation using healthcare-relevant metrics
* Risk ranking and threshold selection
* Outreach capacity simulation
* Subgroup review and business recommendation

## Notebook 00: Project Setup and Validation

Notebook 00 validates the local project structure and confirms that the raw dataset can be loaded successfully before the analytical pipeline begins.

Validations performed:

* Directory instantiation for project data and output folders
* Raw UCI dataset and ID mapping file validation
* Required-column validation
* Readmission outcome distribution review
* Planned `readmitted_30d` target feasibility check
* Raw missing-value code identification, including high-missingness fields such as `weight`, `medical_specialty`, and `payer_code`

Data cleaning, exploratory data analysis, feature engineering, and modeling are deferred to Notebook 01 and beyond.


## Notebook 01: Data Cleaning and Data Dictionary

Notebook 01 performs the initial cleaning and documentation step for the Risk Stratification and Intervention Prioritization project.

The goal of this notebook is to convert the raw UCI diabetes readmission dataset into a cleaned starter dataset for later exploratory analysis, feature engineering, and modeling.

This notebook keeps the encounter as the unit of analysis. Each row represents one hospital encounter.

### Main Work Completed

* Loaded the raw diabetes encounter dataset
* Confirmed the dataset contains 101,766 rows
* Verified that each `encounter_id` is unique
* Identified 71,518 unique patients
* Documented 30,248 repeated-patient rows
* Replaced raw `?` missing-value codes with `NaN`
* Reviewed high-missingness fields such as `weight`, `medical_specialty`, and `payer_code`
* Created the binary 30-day readmission target, `readmitted_30d`
* Confirmed the baseline 30-day readmission rate is approximately 11.16%
* Flagged ID columns that should not be used as predictive features
* Flagged `race`, `gender`, and `age` as sensitive demographic fields for later subgroup review
* Created a data dictionary with column roles, missingness severity flags, and preliminary modeling decisions
* Exported cleaned data and reference documentation for later notebooks

### Target Definition

The primary binary target is:

```python
readmitted_30d = 1 if readmitted == "<30" else 0
```

Rows with `readmitted == ">30"` or `readmitted == "NO"` are treated as `0`.

This target supports a classification workflow focused on identifying encounters at higher risk of 30-day readmission.

### Unit of Analysis

This project uses **encounter-level modeling**.

That means each row represents one hospital encounter, not one unique patient.

Because some patients appear in multiple encounters, later modeling notebooks must use patient-aware splitting. A simple random row-level train/test split could place encounters from the same patient in both training and test sets, causing train/test contamination and inflated evaluation metrics.

Later modeling should use `patient_nbr` as the grouping variable with approaches such as:

* `GroupShuffleSplit`
* `GroupKFold`
* `StratifiedGroupKFold`

The model should not use `encounter_id` or `patient_nbr` as predictive features.

### Missingness Review

The raw dataset uses `?` as a missing-value code. Notebook 01 replaces these values with `NaN` so later notebooks can handle missingness using standard pandas and scikit-learn workflows.

High-missingness fields are documented rather than immediately removed. Extremely incomplete fields are flagged for likely exclusion or special handling during feature engineering.

Examples include:

* `weight`
* `max_glu_serum`
* `A1Cresult`
* `medical_specialty`
* `payer_code`

### Data Dictionary

Notebook 01 creates a data dictionary that documents:

* Column name
* Data type
* Column role
* Missing-value count
* Missing-value percentage
* Number of unique values
* Missingness severity flag
* Preliminary modeling decision

This dictionary supports later leakage review, feature selection, and business interpretation.

### Outputs Created

Notebook 01 exports:

```text
data/processed/diabetes_readmission_cleaned.csv
outputs/model_results/data_dictionary.csv
outputs/model_results/missingness_summary.csv
```

These files are used as reference inputs for later notebooks.

### What This Notebook Does Not Do

This notebook does not perform:

* Exploratory data analysis
* Feature engineering
* Train/test splitting
* Imputation pipelines
* One-hot encoding
* Model training
* Model evaluation
* Threshold selection
* Outreach prioritization
* Fairness or subgroup performance analysis

Those steps are handled in later notebooks.

## Notebook 02: EDA and Outcome Analysis

Notebook 02 performs descriptive exploratory data analysis for the Risk Stratification and Intervention Prioritization project.

The goal is to understand population structure, missingness patterns, feature distributions, and observed 30-day readmission rates across key variables before modeling begins.

This notebook is descriptive only. It does not estimate causal effects, train models, or make intervention recommendations.

### Main Work Completed

* Loaded the cleaned starter dataset created in Notebook 01
* Confirmed the dataset contains 101,766 encounter-level records
* Reviewed the distribution of the binary target, `readmitted_30d`
* Confirmed the baseline 30-day readmission rate is approximately 11.16%
* Examined class imbalance for the readmission outcome
* Analyzed missingness patterns across columns
* Visualized high-missingness fields such as `weight`, `max_glu_serum`, and `A1Cresult`
* Compared observed readmission rates across demographic fields including `age`, `race`, and `gender`
* Flagged sensitive demographic fields for later fairness and subgroup monitoring
* Analyzed encounter context fields such as `admission_type_id`, `discharge_disposition_id`, and `admission_source_id`
* Added caution that admission and discharge ID fields require mapping labels before business presentation
* Evaluated prior utilization variables such as outpatient, emergency, and inpatient visit counts
* Created grouped utilization summaries using natural ordinal ordering
* Reviewed clinical complexity variables such as `number_diagnoses` and `num_medications`
* Analyzed diabetes medication indicators and medication change patterns
* Added patient-aware train/test split reminders for later modeling notebooks
* Exported EDA summary tables and figures for later reference

### Target Review

The primary binary target is:

```python
readmitted_30d = 1 if readmitted == "<30" else 0
```

Rows with `readmitted == ">30"` or `readmitted == "NO"` are treated as `0`.

The positive class is relatively uncommon, with a baseline 30-day readmission rate of approximately 11.16%.

This class imbalance means later modeling notebooks should not rely on accuracy alone. More useful evaluation metrics will include ROC AUC, PR AUC, precision, recall, lift, calibration, and event capture rates at different outreach thresholds.

### Unit of Analysis

This project remains **encounter-level**.

Each row represents one hospital encounter, not one unique patient.

Because some patients appear in multiple encounters, later modeling notebooks must use patient-aware train/test splitting with `patient_nbr` as the grouping variable. A simple random row-level split could place encounters from the same patient in both training and test sets, causing train/test contamination and inflated model performance.

Recommended later splitting approaches include:

* `GroupShuffleSplit`
* `GroupKFold`
* `StratifiedGroupKFold`

This notebook does not perform model validation. All tables and charts are descriptive EDA outputs.

### Missingness Review

Missingness is reviewed after Notebook 01 converted raw `?` missing-value codes into `NaN`.

Missingness is shown as a percentage of rows. High-missingness fields are visualized and documented for later feature engineering decisions.

Examples of high-missingness fields include:

* `weight`
* `max_glu_serum`
* `A1Cresult`
* `medical_specialty`
* `payer_code`

These fields are not automatically removed in this notebook. Final feature inclusion decisions are deferred to later feature engineering and modeling notebooks.

### Demographic and Subgroup Review

Observed readmission rates are compared across demographic fields such as:

* `age`
* `race`
* `gender`

These summaries are used for descriptive subgroup review only.

Observed differences across demographic groups should not be interpreted as causal effects. Sensitive demographic fields may be useful for fairness monitoring and subgroup performance review, but they require caution before being used as predictive features.

### Encounter Context Review

Encounter-level context analysis includes:

* `admission_type_id`
* `discharge_disposition_id`
* `admission_source_id`
* `time_in_hospital`

Admission and discharge fields are shown using source-system ID values in this notebook. Human-readable mapping labels should be added before final business presentation.

Some encounter context fields may also be prediction-timing sensitive. Later feature selection must decide whether the model is intended for admission-time prediction or near-discharge prioritization.

### Utilization and Clinical Complexity Review

Utilization and clinical complexity analysis includes:

* `number_outpatient`
* `number_emergency`
* `number_inpatient`
* Total prior utilization
* `number_diagnoses`
* `num_medications`
* Medication change indicators

Ordinal grouped variables are summarized using natural order rather than sorting only by observed readmission rate. This preserves logical trend interpretation across ordered groups such as age, prior visits, diagnosis count, and medication count.

### Outputs Created

EDA summary tables are exported to:

```text
outputs/model_results/
```

EDA figures are exported to:

```text
outputs/figures/
```

The notebook uses dynamic project path resolution, so output paths are generated relative to the project root instead of relying on hard-coded local machine paths. This improves reproducibility across different environments.

These files provide reference outputs for later feature engineering, modeling, and business interpretation notebooks.

### What This Notebook Does Not Do

This notebook does not perform:

* Feature engineering, including imputation, encoding, or scaling
* Predictive modeling, validation, or threshold selection
* Outreach prioritization or intervention simulation
* Causal inference or final fairness evaluation

Those steps are handled in later notebooks.

## Notebook 03: Feature Engineering and Leakage Review

Notebook 03 creates a leakage-reviewed modeling input dataset for the Risk Stratification and Intervention Prioritization project.

The goal of this notebook is to transform the cleaned encounter-level dataset into a structured modeling input while documenting feature availability, prediction timing, missingness assumptions, and leakage risks before model training begins.

This notebook does not train models. It prepares the candidate feature set that later notebooks will use for patient-aware model development.

### Main Work Completed

* Loaded the cleaned starter dataset created in Notebook 01
* Used robust project-root detection to avoid hard-coded local paths
* Verified that pseudo-null values such as `?`, `"None"`, `"NULL"`, and `"nan"` were not present after cleaning
* Preserved encounter-level modeling as the unit of analysis
* Preserved `patient_nbr` for later patient-aware train/test splitting
* Created age midpoint and age-order features from the original age bands
* Created prior utilization features from outpatient, emergency, and inpatient visit counts
* Created encounter complexity features using length of stay, diagnosis count, medication count, procedures, and lab activity
* Grouped diagnosis codes into broad simplified ICD-9 categories
* Created medication change indicators and medication-change count features
* Created tested/not-tested flags for highly missing lab-result fields
* Excluded raw sparse lab-result fields such as `A1Cresult` and `max_glu_serum` from the first modeling input dataset
* Created missingness indicator features for high-missingness fields
* Grouped rare categorical levels to reduce sparse categories
* Converted operational ID fields to categorical representations
* Normalized feature data types before export
* Created leakage review, excluded-column review, feature-list, and missingness-summary outputs
* Exported a modeling-input dataset for later preprocessing and model development

### Prediction Timing

This notebook uses a **near-discharge prediction framing**.

That means the model input may include information that would be available by the end of the hospital encounter, before post-discharge outreach prioritization.

This framing is different from admission-time prediction. Some fields that may be acceptable for near-discharge prioritization could be unavailable or leakage-prone for admission-time triage.

Later notebooks should keep this timing assumption consistent when building and evaluating models.

### Unit of Analysis and Splitting Requirement

This project remains **encounter-level**.

Each row represents one hospital encounter, not one unique patient.

Because some patients appear in multiple encounters, later modeling notebooks must use patient-aware train/test splitting with `patient_nbr` as the grouping variable. A simple random row-level split could place encounters from the same patient in both training and test sets, causing train/test contamination and inflated model performance.

Recommended later splitting approaches include:

* `GroupShuffleSplit`
* `GroupKFold`
* `StratifiedGroupKFold`

Identifier fields such as `encounter_id` and `patient_nbr` are not used as predictive features. The original target field, `readmitted`, is also excluded from the feature list.

### Feature Engineering Summary

Notebook 03 creates several groups of engineered features:

* **Age features**

  * Age midpoint
  * Age order

* **Prior utilization features**

  * Total prior visits
  * Any prior utilization flag
  * Prior inpatient flag
  * Prior emergency flag
  * High prior utilization flag

* **Encounter complexity features**

  * Long-stay flag
  * Time-in-hospital group
  * Diagnosis count group
  * Medication count group
  * Raw encounter-volume fields such as `time_in_hospital`, `num_lab_procedures`, `num_procedures`, `num_medications`, and `number_diagnoses`

* **Diagnosis grouping features**

  * Primary diagnosis group
  * Secondary diagnosis group
  * Tertiary diagnosis group

* **Medication features**

  * Insulin flag
  * Diabetes medication flag
  * Diabetes medication changed flag
  * Medication change count
  * Any medication change flag

* **Missingness and testing features**

  * Missingness flags for high-missingness fields
  * `A1Cresult_tested_flag`
  * `max_glu_serum_tested_flag`

These features are designed for predictive modeling and operational prioritization, not causal interpretation.

### Leakage Review

Notebook 03 creates a leakage review table documenting excluded, retained, and caution-required fields.

The review covers:

* Identifier fields
* Original and engineered target fields
* Prediction-timing-sensitive encounter fields
* Highly sparse lab-result fields
* Sensitive demographic fields
* Patient grouping fields needed for later split logic

This notebook prepares a defensible candidate feature set, but final feature inclusion decisions should still be reviewed during modeling.

### Missingness Handling

Notebook 03 does not perform imputation.

Instead, it:

* Validates that pseudo-null values were already cleaned
* Creates missingness indicators for selected high-missingness fields
* Creates tested/not-tested flags for sparse lab-result fields
* Excludes extremely sparse raw lab-result categories from the first modeling input dataset

Actual imputation strategy is deferred to later modeling pipelines.

### Data Type Handling

Before export, selected features are normalized into clearer modeling-input types:

* Numeric features are converted to numeric types
* Binary and missingness flags are converted to compact integer flags
* Categorical and subgroup-review fields are converted to string representation

This improves consistency for later preprocessing, but the dataset is not yet fully scikit-learn-ready.

### Outputs Created

Notebook 03 exports:

```text
data/processed/diabetes_readmission_model_ready.csv
outputs/model_results/feature_list.csv
outputs/model_results/leakage_review.csv
outputs/model_results/excluded_columns_review.csv
outputs/model_results/model_ready_missingness_summary.csv
```

The exported modeling-input dataset includes selected candidate features, the binary target column, and `patient_nbr` for later patient-aware splitting.

### What This Notebook Does Not Do

This notebook does not perform:

* Train/test splitting or grouped cross-validation
* Imputation, encoding, or scaling pipelines
* Model training or model evaluation
* Threshold selection or outreach prioritization
* Causal inference or final fairness evaluation

Those steps are handled in later notebooks.

## Notebook 04: Baseline Risk Modeling

Notebook 04 builds baseline predictive models for **30-day hospital readmission risk** using the leakage-reviewed modeling input dataset created in Notebook 03.

The goal is to establish an initial modeling benchmark before moving into advanced model comparison, calibration, threshold selection, and outreach prioritization.

This notebook focuses on **patient-aware validation**, **baseline model performance**, and **class-imbalance-aware evaluation**. It does not create final intervention thresholds or outreach lists.

### Main Work Completed

**Data and target setup**

* Loaded the modeling input dataset and feature list from Notebook 03
* Confirmed the binary target, `readmitted_30d`
* Preserved `patient_nbr` for patient-aware splitting
* Excluded patient and encounter identifiers from predictive features

**Patient-aware validation**

* Created a holdout split using `GroupShuffleSplit`
* Verified that train and test sets have **zero overlapping patients**
* Compared train and test 30-day readmission rates
* Added grouped cross-validation using `StratifiedGroupKFold`

**Modeling pipeline**

* Built preprocessing pipelines for numeric and categorical features
* Applied imputation, scaling, and one-hot encoding inside the modeling pipeline
* Trained a **Dummy Classifier**, **Logistic Regression**, and **Decision Tree** baseline

**Model selection and export**

* Compared baseline model performance
* Selected **Logistic Regression** as the provisional baseline model
* Exported model metrics, classification reports, split summary, cross-validation results, and selected baseline metadata

### Target Definition

The primary binary target is:

```python
readmitted_30d = 1 if readmitted == "<30" else 0
```

Rows with `readmitted == ">30"` or `readmitted == "NO"` are treated as `0`.

The positive class represents hospital encounters followed by readmission within 30 days.

### Unit of Analysis and Split Strategy

This project remains **encounter-level**.

Each row represents one hospital encounter, but patients can appear in multiple encounters.

Because of repeated patients, this notebook does **not** use a simple random row-level train/test split. A random split could place encounters from the same patient in both training and test sets, causing train/test contamination and inflated model performance.

Instead, this notebook uses `patient_nbr` as the grouping variable.

Validation methods used:

* **Holdout split:** `GroupShuffleSplit`
* **Grouped cross-validation:** `StratifiedGroupKFold`

This protects the evaluation from same-patient leakage while preserving the encounter-level prediction problem.

### Baseline Models

Notebook 04 compares three baseline models:

* **Dummy Classifier**

  * Serves as a no-skill reference model
  * Confirms whether trained models improve over a naive baseline

* **Logistic Regression**

  * Provides an interpretable linear baseline
  * Uses `class_weight="balanced"` to account for the low positive-class rate
  * Selected as the provisional baseline model

* **Decision Tree**

  * Provides a simple nonlinear baseline
  * Uses class weighting
  * Useful for comparison, but not selected as the strongest baseline

### Evaluation Approach

Because 30-day readmission is an imbalanced outcome, **accuracy is not the main metric**.

Notebook 04 evaluates models using:

* **ROC AUC** for overall ranking ability
* **PR AUC** for performance on the uncommon positive class
* **Precision and recall** for care-management relevance
* **F1 score** as a balance between precision and recall
* **Confusion matrices and classification reports** for threshold-based interpretation
* **Grouped cross-validation metrics** for patient-aware validation stability

The default `0.50` classification threshold is treated as provisional. Later notebooks should evaluate thresholds based on care management capacity, such as **top 5%**, **top 10%**, or **top 20%** risk groups.

### Baseline Result Summary

**Logistic Regression** is selected as the provisional baseline model.

It performs better than the Dummy Classifier and Decision Tree on the main ranking metrics used in this notebook. Precision remains low because the positive class is uncommon, which is expected in a 30-day readmission-risk problem.

This model should be interpreted as a **baseline risk-ranking model**, not a deployment-ready outreach engine.

### Interpretation Caution

This notebook evaluates **predictive association**, not causal effect.

A higher predicted risk score means the model estimates a higher probability of 30-day readmission based on observed encounter-level features. It does not prove that any individual feature causes readmission.

This notebook also does not prove that outreach will reduce readmissions. Outreach impact would require an experiment, quasi-experimental design, or separate program evaluation.

### Outputs Created

Notebook 04 exports model results to:

```text
outputs/model_results/baseline_model_metrics.csv
outputs/model_results/baseline_classification_reports.csv
outputs/model_results/baseline_split_summary.csv
outputs/model_results/baseline_cv_results.csv
outputs/model_results/selected_baseline_model.csv
```

Baseline figures are exported to:

```text
outputs/figures/
```

These outputs provide benchmark results for later notebooks covering model comparison, threshold strategy, and outreach prioritization.

### What This Notebook Does Not Do

This notebook does not perform:

* Advanced model tuning or final model selection
* Probability calibration
* Threshold selection, risk tiering, or outreach simulation
* Fairness or subgroup performance evaluation
* Causal inference or intervention-effect estimation

Those steps are handled in later notebooks.

## Notebook 05: Model Comparison and Threshold Strategy

Notebook 05 compares candidate readmission-risk models and translates predicted risk scores into an outreach prioritization strategy.

The goal is not only to evaluate model performance, but to answer a practical operational question:

> If care management capacity is limited, which encounters should be prioritized first?

This notebook focuses on **model comparison**, **patient-aware validation**, **top-risk group evaluation**, and **capacity-constrained threshold strategy**. It does not prove that outreach reduces readmissions.

### Main Work Completed

**Model comparison**

* Loaded the modeling input dataset and feature list created in Notebook 03
* Recreated a patient-aware train/test split using `patient_nbr`
* Trained three fixed-parameter candidate models:

  * Logistic Regression
  * Random Forest
  * Gradient Boosting
* Compared candidate models using holdout test performance
* Added patient-aware cross-validation to estimate metric stability

**Threshold and prioritization strategy**

* Ranked test-set encounters by predicted readmission risk
* Evaluated top-risk groups at **Top 5%**, **Top 10%**, and **Top 20%**
* Calculated observed readmission rate, lift multiplier over baseline, precision at k, and recall at k
* Created rank-based risk tiers to keep tier counts consistent with top-risk evaluation
* Simulated outreach capacity under different intervention thresholds
* Exported a Top 10% outreach list for downstream review

**Governance and interpretation**

* Selected a provisional candidate model using patient-aware cross-validation
* Added caveats for fixed-parameter model comparison, calibration, and causal interpretation
* Documented that predicted scores are used for ranking, not yet as calibrated absolute probabilities
* Stated that outreach impact requires a separate experiment or program evaluation

### Unit of Analysis and Split Strategy

This project remains **encounter-level**.

Each row represents one hospital encounter, but patients can appear in multiple encounters.

Because of repeated patients, this notebook does **not** use a simple random row-level train/test split. A random split could place encounters from the same patient in both training and test sets, causing train/test contamination and inflated model performance.

The notebook uses `patient_nbr` as the grouping variable for patient-aware validation.

Validation methods include:

* **Holdout split:** patient-aware train/test split
* **Cross-validation:** patient-aware grouped CV on the training set

This keeps the evaluation aligned with the encounter-level prediction problem while reducing same-patient leakage.

### Candidate Models

Notebook 05 compares three fixed-parameter candidate models:

* **Logistic Regression**

  * Interpretable linear benchmark
  * Useful as a stable risk-ranking baseline

* **Random Forest**

  * Nonlinear tree-based ensemble
  * Captures interactions and nonlinear relationships

* **Gradient Boosting**

  * Sequential tree-based ensemble
  * Selected as the provisional candidate model in this fixed-parameter comparison

The models use fixed, conservative hyperparameters in this notebook. This is a **provisional model comparison**, not a final hyperparameter-tuned architecture selection.

Because different model families respond differently to tuning, the selected model should not be interpreted as the final best algorithm. Later notebooks should revisit model selection after hyperparameter tuning, calibration review, and subgroup performance analysis.

### Model Selection Logic

The provisional candidate model is selected using **patient-aware cross-validation on the training set**, not by directly choosing the best result from the holdout test set.

Selection prioritizes:

1. **Top 10% lift multiplier mean**
2. **PR AUC mean**
3. **ROC AUC mean**

The **Top 10% lift multiplier** compares the observed readmission rate within the highest-risk 10% of encounters against the overall baseline readmission rate.

For example, a lift multiplier of `2.4x` means the Top 10% risk group has approximately 2.4 times the baseline readmission rate.

This selection rule aligns with the project goal: prioritizing a limited outreach population rather than maximizing generic classification accuracy.

In the current fixed-parameter comparison, **Gradient Boosting** is selected as the provisional candidate model.

### Threshold Strategy

The notebook evaluates outreach thresholds based on ranked predicted risk.

In this notebook, **k** refers to the size of the outreach group selected from the ranked risk list.

Thresholds reviewed:

* **Top 5%**: k equals the highest-risk 5% of encounters
* **Top 10%**: k equals the highest-risk 10% of encounters
* **Top 20%**: k equals the highest-risk 20% of encounters

For each threshold, the notebook calculates:

* Number of encounters targeted
* Observed 30-day readmission count
* Observed readmission rate
* Lift multiplier over baseline
* Precision at k
* Recall at k

Here, **recall at k** represents the share of all observed 30-day readmissions captured within the selected top-risk group.

The recommended pilot threshold is:

> Start with the Top 10% highest-risk encounters.

This threshold is operationally realistic for an initial outreach pilot. It can be narrowed to the Top 5% if staffing is highly constrained or expanded to the Top 20% if care management capacity allows.

### Risk Tiers

Notebook 05 assigns rank-based risk tiers:

* **Very High Risk:** Top 5%
* **High Risk:** 5% to 10%
* **Moderate Risk:** 10% to 25%
* **Lower Risk:** Bottom 75%

Risk tiers are assigned using rank cutoffs rather than probability cutoffs. This keeps tier sizes consistent with the capacity-based threshold strategy.

### Calibration and Interpretation Caution

Predicted scores are used for **ranking**.

They should not yet be interpreted as calibrated absolute probabilities. Calibration should be reviewed before using fixed probability thresholds such as `risk >= 0.30`.

This notebook evaluates predictive association, not causal effect.

A higher risk score means the model ranks an encounter as more likely to be followed by 30-day readmission. It does not prove that any feature causes readmission, and it does not prove that outreach will reduce readmissions.

Estimating outreach impact would require a randomized pilot, A/B test, quasi-experimental design, or separate program evaluation.

### Outputs Created

Notebook 05 exports model comparison outputs to:

```text
outputs/model_results/candidate_model_comparison_metrics.csv
outputs/model_results/candidate_model_cv_results.csv
outputs/model_results/candidate_model_cv_summary.csv
outputs/model_results/top_risk_segment_evaluation.csv
outputs/model_results/selected_candidate_model.csv
outputs/model_results/risk_tier_summary.csv
outputs/model_results/outreach_capacity_summary.csv
```

Notebook 05 exports outreach-prioritization files to:

```text
outputs/outreach_lists/test_set_risk_ranking.csv
outputs/outreach_lists/top_10_percent_outreach_list.csv
```

Notebook 05 exports model comparison and risk-tier figures to:

```text
outputs/figures/
```

These outputs support later subgroup review, calibration review, hyperparameter tuning, and business recommendation development.

### What This Notebook Does Not Do

This notebook does not perform:

* Final hyperparameter tuning
* Final algorithm selection
* Probability calibration
* Fairness or subgroup performance evaluation
* SHAP or feature-importance interpretation
* Causal inference or intervention-effect estimation
* Production deployment logic

Those steps are handled in later notebooks.




