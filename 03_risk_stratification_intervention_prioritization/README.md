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

## Notebook 06: Fairness and Subgroup Review

Notebook 06 evaluates subgroup selection and predictive-performance patterns for the Risk Stratification and Intervention Prioritization project.

The goal is to determine whether model scores, outreach selection, and threshold-based performance differ across key demographic groups before final intervention recommendations are made.

This notebook does **not** certify that the model is fair. It identifies patterns that require monitoring, validation, and further review before any real-world use.

### Key Findings

* The Top 10% threshold selected **2,016 of 20,153 encounters**. This group had a **25.79% observed readmission rate**, compared with approximately **10.67% across the full test set**, and captured about **24.17% of all observed readmissions**.
* Among age groups with at least 100 encounters, the `[30-40)` group had the highest Top 10% selection rate at **16.67%** and the highest recall at **35.35%**.
* African American encounters had an **11.33% selection rate** and **28.00% recall**, compared with a **9.88% selection rate** and **23.43% recall** for Caucasian encounters.
* Encounters with unknown race had a substantially lower **4.63% selection rate** and **4.76% recall**. This may indicate a missing-demographic or data-quality issue requiring further review.
* Female and male encounters had similar results. Selection rates were **10.25% for females** and **9.71% for males**, while recall was **23.60%** and **24.85%**, respectively.
* Very small groups, including `[0-10)` with 38 encounters and `Unknown/Invalid` gender with 2 encounters, produced unstable metrics and should not be treated as reliable subgroup evidence.
* These results are descriptive. The notebook does not calculate confidence intervals or formal significance tests, so observed differences cannot be labeled statistically significant or used as proof that the model is fair or unfair.

### Main Work Completed

**Data preparation**

* Loaded the test-set risk ranking created in Notebook 05
* Loaded the model-ready dataset created in Notebook 03
* Joined demographic fields to ranked test encounters using `encounter_id`
* Confirmed that the join preserved the original test-set row count
* Created rank-based selection indicators for the Top 5%, Top 10%, and Top 20% highest-risk encounters

**Subgroup evaluation**

* Reviewed performance across `age`, `race`, and `gender`
* Used the Top 10% risk group as the primary subgroup-monitoring threshold
* Calculated subgroup outcome, selection, and classification metrics
* Compared subgroup selection rates and recall with overall values
* Flagged subgroups with fewer than 100 encounters

**Visualization and export**

* Visualized selection-rate and recall differences across demographic groups
* Compared subgroup selection rates with observed readmission rates
* Exported subgroup tables, monitoring flags, threshold summaries, and figures

### Requirements

Notebook 06 uses:

* Python
* `pandas`
* `numpy`
* `matplotlib`

It does not use a specialized fairness library such as Fairlearn.

Install project dependencies from the project root:

```bash
pip install -r requirements.txt
```

### Execution Requirements

Notebook 06 depends on outputs created by earlier notebooks. It is not fully standalone unless the following files already exist:

```text
data/processed/diabetes_readmission_model_ready.csv
outputs/outreach_lists/test_set_risk_ranking.csv
outputs/model_results/selected_candidate_model.csv
```

For a complete clean run, execute the notebooks in numerical order:

```text
00_project_setup_and_data_access_check.ipynb
01_data_cleaning_and_dictionary.ipynb
02_eda_and_outcome_analysis.ipynb
03_feature_engineering_and_leakage_review.ipynb
04_baseline_risk_modeling.ipynb
05_model_comparison_and_threshold_strategy.ipynb
06_fairness_and_subgroup_review.ipynb
```

Notebook 06 can be rerun independently after the required Notebook 03 and Notebook 05 outputs have been generated.

Dynamic project-root detection is used so inputs and outputs are resolved relative to the repository rather than through hard-coded local paths.

### Outreach Selection Threshold

The primary operational threshold is the Top 10% highest-risk encounters.

Selection indicators use rank-based cutoffs so the evaluated populations remain consistent with the threshold and outreach-list logic established in Notebook 05.

```python
top_10_cutoff = int(np.ceil(total_test_encounters * 0.10))

top_10_selected = 1 if risk_rank <= top_10_cutoff else 0
```

Additional indicators are created for:

* Top 5% highest-risk encounters
* Top 10% highest-risk encounters
* Top 20% highest-risk encounters

Selection into the Top 10% does not mean that readmission is certain. It means the encounter received one of the highest model scores under limited outreach capacity.

### Subgroups Reviewed

Subgroup performance is reviewed across:

* `age`
* `race`
* `gender`

Race and gender are excluded from the primary predictive feature set and retained for subgroup monitoring.

Age may be included as a clinically relevant predictive feature, but age-based selection and performance differences still require review.

### Subgroup Metrics

The notebook calculates the following fields for each subgroup:

* `encounter_count`
* `readmission_count`
* `readmission_rate`
* `avg_predicted_risk`
* `selected_count`
* `selection_rate`
* `true_positive`
* `false_positive`
* `false_negative`
* `true_negative`
* `precision`
* `recall`
* `false_positive_rate`
* `false_negative_rate`

The exported field `avg_predicted_risk` represents the subgroup’s average model score.

Probability calibration has not yet been completed. This field is therefore used for relative ranking and subgroup comparison rather than interpreted as a calibrated absolute readmission probability.

#### Selection Rate

The percentage of subgroup encounters selected into the Top 10% highest-risk group.

```text
selected encounters / total subgroup encounters
```

#### Precision

Among selected subgroup encounters, the percentage that experienced a 30-day readmission.

```text
true positives / selected encounters
```

#### Recall

Among subgroup encounters that experienced a 30-day readmission, the percentage selected into the Top 10% group.

```text
true positives / total subgroup readmissions
```

#### False Positive Rate

Among subgroup encounters that were not readmitted, the percentage selected into the Top 10%.

```text
false positives / total subgroup non-readmissions
```

#### False Negative Rate

Among subgroup encounters that were readmitted, the percentage not selected into the Top 10%.

```text
false negatives / total subgroup readmissions
```

These metrics describe model behavior at the selected outreach threshold. They do not prove that the model is fair or unfair.

### Age Group Review

Age-group analysis compares:

* Encounter volume
* Observed readmission rate
* `avg_predicted_risk`
* Top 10% selection rate
* Precision and recall
* False positive and false negative rates

Age bands are displayed in their natural ordinal order:

```text
[0-10)
[10-20)
[20-30)
...
[90-100)
```

Differences across age groups may reflect clinical risk, utilization patterns, historical data patterns, feature availability, or model behavior.

### Race Group Review

Race-group analysis compares selection and predictive-performance metrics across available race categories.

Race is used only for subgroup monitoring in the primary workflow.

Observed differences may reflect:

* Unequal subgroup sample sizes
* Missing demographic information
* Documentation patterns
* Clinical complexity
* Historical utilization
* Structural inequities
* Model behavior

Race-group differences should not be interpreted as causal effects or automatic evidence of discrimination.

### Gender Group Review

Gender-group analysis compares:

* Observed readmission rates
* `avg_predicted_risk`
* Top 10% selection rates
* Precision and recall
* False positive and false negative rates

Very small groups may produce unstable metrics and should be interpreted cautiously.

Results from a single retrospective test set should be treated as monitoring signals rather than final conclusions.

### Small-Sample Monitoring

Subgroups with fewer than 100 encounters are flagged using:

```python
small_sample_flag = 1 if encounter_count < 100 else 0
```

Small-sample metrics can change substantially because of only a few outcomes or selections.

The notebook does not currently calculate confidence intervals or formal significance tests for subgroup differences.

### Overall Comparison

Each subgroup’s selection rate is compared with the overall Top 10% selection rate.

Each subgroup’s recall is also compared with overall recall.

The notebook calculates:

```text
selection_rate_diff_vs_overall
recall_diff_vs_overall
```

These differences identify groups that may require further review.

A difference from the overall result is not automatically evidence of bias. Observed readmission rates, sample sizes, data quality, and clinical profiles must also be considered.

### Selection Rate and Observed Outcome

The notebook reviews subgroup Top 10% selection rates alongside observed subgroup readmission rates.

A subgroup with a higher observed readmission rate may reasonably receive a higher selection rate. However, observed outcome differences do not automatically justify every selection difference.

Differences may also result from:

* Data quality
* Feature availability
* Probability calibration
* Documentation practices
* Historical care patterns
* Structural inequities
* Model behavior

Selection rates and observed outcomes should therefore be reviewed together.

### Outputs Created

Subgroup review tables are exported to:

```text
outputs/model_results/subgroup_review_age.csv
outputs/model_results/subgroup_review_race.csv
outputs/model_results/subgroup_review_gender.csv
outputs/model_results/subgroup_review_combined.csv
outputs/model_results/subgroup_monitoring_flags.csv
outputs/model_results/test_ranking_with_subgroups.csv
outputs/model_results/subgroup_threshold_selection_summary.csv
```

Subgroup figures are exported to:

```text
outputs/figures/top_10_selection_rate_by_age.png
outputs/figures/recall_at_top_10_by_age.png
outputs/figures/top_10_selection_rate_by_race.png
outputs/figures/recall_at_top_10_by_race.png
outputs/figures/top_10_selection_rate_by_gender.png
outputs/figures/recall_at_top_10_by_gender.png
outputs/figures/selection_rate_vs_readmission_rate_by_subgroup.png
```

### Interpretation Limitations

This notebook does not provide final fairness approval.

Important limitations include:

* Retrospective test-set evaluation
* Unequal subgroup sample sizes
* No confidence intervals
* No formal significance testing
* No intersectional subgroup analysis
* No calibration analysis by subgroup
* No post-deployment monitoring
* No outreach completion data
* No intervention outcome data
* No causal evidence that outreach reduces readmissions

Differences in subgroup performance may reflect model behavior, underlying outcome differences, data quality, documentation practices, historical care patterns, or structural inequities.

### What This Notebook Does Not Do

This notebook does not perform:

* Model retraining or hyperparameter tuning
* Final model selection
* Final outreach-list creation
* Intervention ROI estimation
* Causal impact evaluation
* Production deployment approval
* Formal legal or regulatory fairness validation
* Claims that the model is fair

Those steps require additional analysis, operational validation, and ongoing monitoring.

### Monitoring Recommendations

Any real-world implementation should continue monitoring:

* Selection rates by subgroup
* Outreach completion rates by subgroup
* Observed readmission rates by subgroup
* Precision and recall by subgroup
* False negative rates by subgroup
* Probability calibration
* Data and population drift
* Missingness patterns
* Manual overrides
* Model recalibration frequency

The next notebook converts the risk rankings and subgroup-review findings into final intervention-prioritization outputs and a business recommendation.

## Notebook 07: Intervention Prioritization and Business Recommendation

This project uses the public **UCI Diabetes 130-US Hospitals for Years 1999–2008 dataset**, containing de-identified hospital encounter records for patients diagnosed with diabetes.

Notebook 07 converts the final readmission-risk rankings into an operational intervention-prioritization strategy for the Risk Stratification and Intervention Prioritization project.

The goal is to translate encounter-level model rankings into practical patient-level outreach decisions when care management capacity is limited.

This notebook does **not** retrain the model, calibrate predicted probabilities, or estimate the causal effect of outreach. It focuses on outreach capacity, patient-level prioritization, subgroup-monitoring requirements, and business recommendations.

### Key Findings

* The Top 5% threshold selected **1,008 of 20,153 encounters** and had an observed 30-day readmission rate of approximately **30.06%**.
* The Top 10% threshold selected **2,016 encounters** and had a **25.79% observed readmission rate**, compared with approximately **10.67% across the full test set**.
* The Top 10% group captured approximately **24.17% of all observed test-set readmissions** while targeting about one-tenth of encounters.
* The Top 20% threshold selected **4,031 encounters** and had an observed readmission rate of approximately **20.39%**.
* The risk-tier results showed a clear risk gradient, with higher-ranked tiers having higher observed readmission rates than lower-ranked tiers.
* The Top 10% threshold was retained as the provisional pilot strategy because it balances risk concentration, readmission capture, and operational workload.
* The encounter-level Top 10% list contained repeated patients, confirming that model evaluation and operational outreach require different units of analysis.
* The selected encounter list was deduplicated into a prototype roster containing one priority row per patient.
* Actual future readmission outcomes were excluded from the prototype outreach list because they would not be available at prediction time.
* Gradient Boosting remains a **provisional candidate model**. The model scores are used for relative ranking and should not be interpreted as calibrated absolute probabilities.
* These results support a controlled outreach pilot. They do not prove that outreach will reduce readmissions.
* Deduplicating the 2,016 selected encounters produced a prototype outreach roster of **1,240 unique patients**, representing approximately **8.67% of the 14,304 unique patients** in the test set.
* The threshold is therefore Top 10% at the encounter level, not at the patient level.

### Main Work Completed

**Input validation**

* Loaded the provisional candidate-model output from Notebook 05
* Loaded ranked test encounters and subgroup-review outputs from Notebook 06
* Confirmed that required ranking, outcome, subgroup, and threshold columns were available
* Confirmed that `encounter_id` remained unique in the encounter-level ranking
* Validated model-score and risk-percentile ranges
* Confirmed that Top 5%, Top 10%, and Top 20% selection flags matched exact risk-rank cutoffs

**Threshold and risk-tier evaluation**

* Recalculated encounter-level threshold performance
* Validated threshold results against Notebook 06 outputs
* Calculated selected encounter counts and unique-patient counts
* Calculated observed readmission rates within each threshold
* Calculated lift over the test-set baseline
* Calculated the percentage of total readmissions captured
* Summarized observed outcomes across final risk tiers
* Visualized lift, readmission capture, and risk-tier gradients

**Operational prioritization**

* Distinguished encounter-level retrospective evaluation from patient-level outreach operations
* Identified patients with multiple selected encounters
* Deduplicated the Top 10% encounter list using `patient_nbr`
* Retained the highest-ranked qualifying encounter for each patient
* Created a retrospective patient-level list for evaluation
* Created a separate operational outreach roster without future outcomes
* Assigned proposed operational actions by risk tier

**Business recommendation and monitoring**

* Incorporated subgroup-monitoring findings from Notebook 06
* Defined subgroup-monitoring requirements for a prospective pilot
* Defined capacity, outreach, outcome, model, and data-quality monitoring metrics
* Recommended a controlled Top 10% outreach pilot
* Documented model, operational, fairness, and causal limitations
* Exported final prioritization, monitoring, recommendation, and outreach outputs

### Requirements

Notebook 07 uses:

* Python
* `pandas`
* `numpy`
* `matplotlib`

Install project dependencies from the project root:

```bash
pip install -r requirements.txt
```

### Execution Requirements

Notebook 07 depends on outputs created by earlier notebooks. It is not fully standalone unless the following files already exist:

```text
outputs/model_results/selected_candidate_model.csv
outputs/model_results/candidate_model_cv_summary.csv
outputs/model_results/test_ranking_with_subgroups.csv
outputs/model_results/subgroup_monitoring_flags.csv
outputs/model_results/subgroup_threshold_selection_summary.csv
```

For a complete clean run, execute the notebooks in numerical order:

```text
00_project_setup_and_data_access_check.ipynb
01_data_cleaning_and_dictionary.ipynb
02_eda_and_outcome_analysis.ipynb
03_feature_engineering_and_leakage_review.ipynb
04_baseline_risk_modeling.ipynb
05_model_comparison_and_threshold_strategy.ipynb
06_fairness_and_subgroup_review.ipynb
07_intervention_prioritization_and_business_recommendation.ipynb
```

Notebook 07 can be rerun independently after the required Notebook 05 and Notebook 06 outputs have been generated.

Dynamic project-root detection is used so inputs and outputs are resolved relative to the repository rather than through hard-coded local paths.

### Candidate Model Status

The provisional candidate model is **Gradient Boosting**.

The model was selected during the fixed-parameter comparison performed in Notebook 05.

The model should remain provisional because:

* Final hyperparameter tuning has not been completed
* Probability calibration has not been completed
* External validation has not been completed
* Prospective operational validation has not been completed

The exported field `predicted_readmission_risk` represents the model score used for relative ranking.

It should not be interpreted as a calibrated absolute probability of readmission.

### Unit of Analysis and Operational Unit

The predictive model remains **encounter-level**.

Each row represents one hospital encounter and receives one predicted readmission-risk score.

However, care management outreach is generally **patient-level**.

The same patient may have multiple encounters within the selected Top 10% group. Sending the encounter-level ranking directly to an outreach team could therefore create duplicate assignments.

Notebook 07 preserves two distinct outputs:

1. **Encounter-level retrospective evaluation**
2. **Patient-level prototype prioritization**

This distinction keeps performance evaluation aligned with the model’s prediction unit while making the outreach output operationally usable.

### Rank-Based Outreach Thresholds

Notebook 07 reuses the rank-based threshold indicators established in Notebooks 05 and 06.

```python
top_10_cutoff = int(np.ceil(total_test_encounters * 0.10))

top_10_selected = 1 if risk_rank <= top_10_cutoff else 0
```

The reviewed thresholds are:

* Top 5% highest-risk encounters
* Top 10% highest-risk encounters
* Top 20% highest-risk encounters

Rank-based thresholds are used instead of fixed score thresholds because probability calibration has not been completed.

This also keeps the selected population aligned with explicit outreach-capacity assumptions.

### Outreach Capacity Metrics

For each threshold, the notebook calculates:

* `selected_encounters`
* `selected_unique_patients`
* `selected_readmissions`
* `selected_readmission_rate`
* `baseline_readmission_rate`
* `lift_vs_baseline`
* `percent_of_readmissions_captured`

#### Lift Over Baseline

Lift measures how concentrated observed readmissions are within the selected outreach group compared with the full test set.

```text
selected-group readmission rate / baseline readmission rate
```

A lift greater than `1.0` means the selected group has a higher observed readmission rate than the overall test population.

#### Readmission Capture

Readmission capture measures the percentage of all observed test-set readmissions included in the selected group.

```text
selected readmissions / total test-set readmissions
```

This metric reflects the tradeoff between outreach volume and missed readmissions.

### Outreach Capacity Tradeoff

A smaller selected population generally provides:

* Higher observed readmission concentration
* Higher lift
* Fewer selected encounters
* Fewer selected patients
* Lower total readmission capture

A larger selected population generally provides:

* More selected encounters
* More selected patients
* Higher total readmission capture
* Lower readmission concentration
* Lower lift

The outreach threshold is therefore an operational capacity decision rather than a universal model cutoff.

### Provisional Pilot Threshold

The recommended pilot threshold is the **Top 10% highest-risk encounters**.

The Top 10% threshold provides a practical balance between:

* Risk concentration
* Readmission capture
* Outreach volume
* Patient volume
* Staffing requirements
* Pilot feasibility

The Top 5% threshold may be used when outreach capacity is extremely limited.

The Top 20% threshold may be considered if the organization has sufficient capacity and prioritizes broader readmission capture.

The final operational threshold should be selected using actual staffing, outreach cost, eligibility rules, and workflow data.

### Final Risk Tiers

Notebook 07 summarizes four capacity-based risk tiers:

* **Very High Risk:** Top 5%
* **High Risk:** 5% to 10%
* **Moderate Risk:** 10% to 25%
* **Lower Risk:** Bottom 75%

For each risk tier, the notebook calculates:

* Encounter count
* Unique-patient count
* Observed readmission count
* Average model score
* Observed readmission rate
* Lift over baseline

The average model score is used for relative comparison only.

It should not be interpreted as the tier’s true absolute readmission probability.

### Encounter-Level Retrospective Ranking

The encounter-level retrospective ranking contains:

* `encounter_id`
* `patient_nbr`
* predicted model score
* risk rank
* risk percentile
* risk tier
* actual 30-day readmission outcome
* subgroup-monitoring fields
* Top 5%, Top 10%, and Top 20% selection indicators

This output is used for historical model and threshold evaluation.

The actual outcome is included because the analysis is retrospective.

### Patient-Level Deduplication

The Top 10% encounter list is deduplicated using `patient_nbr`.

For patients with multiple selected encounters, the highest-ranked qualifying encounter is retained as the priority encounter.

The patient-level retrospective list includes:

* `patient_nbr`
* priority `encounter_id`
* highest model score
* best risk rank
* best risk percentile
* risk tier
* qualifying encounter count
* actual retrospective outcome
* subgroup-monitoring fields

The qualifying encounter count identifies patients who appeared multiple times within the selected encounter group.

### Patient-Level Prototype Outreach Roster

The prototype outreach list is separate from the retrospective evaluation list.

It includes fields such as:

* `patient_nbr`
* priority `encounter_id`
* highest model score
* best risk rank
* best risk percentile
* risk tier
* qualifying encounter count
* age group
* proposed operational action

The operational list excludes:

* `actual_readmitted_30d`
* retrospective true-positive or false-positive indicators
* Top 5%, Top 10%, and Top 20% selection indicators
* race
* gender

The future readmission outcome would not be available at prediction time.

Race and gender remain available in separate subgroup-monitoring outputs rather than the core outreach roster.

### Proposed Operational Actions

The notebook assigns proposed actions by risk tier.

#### Very High Risk

```text
Priority review and first outreach attempt
```

#### High Risk

```text
Standard pilot outreach after the Very High Risk group
```

#### Moderate Risk

```text
Monitor or include if additional outreach capacity is available
```

#### Lower Risk

```text
Usual workflow without model-prioritized outreach
```

These actions are portfolio-level recommendations rather than clinical orders.

A real operational workflow would still require:

* Program eligibility review
* Discharge-status review
* Existing care-management enrollment checks
* Contact-preference review
* Clinical and operational overrides
* Privacy and access controls

### Subgroup Monitoring Integration

Notebook 07 incorporates the subgroup-monitoring findings from Notebook 06.

Monitoring fields include:

* Subgroup encounter count
* Observed readmission rate
* Selection rate
* Recall
* False negative rate
* Small-sample flag
* Selection-rate difference from overall
* Recall difference from overall

Notebook 06 identified meaningful subgroup variation and several very small groups.

These findings do not prove that the model is fair or unfair. They identify areas requiring monitoring during any prospective pilot.

### Subgroup Monitoring Requirements

The recommended pilot should monitor:

* Selection rate by subgroup
* Outreach-attempt rate by subgroup
* Outreach-completion rate by subgroup
* Recall by subgroup
* False negative rate by subgroup
* Observed readmission rate by subgroup
* Missingness patterns
* Subgroup sample sizes
* Calibration by subgroup after calibration work is completed

Subgroup selection, intervention delivery, missed outcomes, and observed outcomes should be reviewed together.

### Pilot Monitoring Plan

The pilot-monitoring framework includes:

**Capacity metrics**

* Selected encounter count
* Unique selected patient count
* Duplicate selected encounters
* Care-manager caseload

**Operational metrics**

* Outreach-attempt rate
* Successful-contact rate
* Outreach-completion rate
* Time from discharge to outreach
* Unable-to-reach rate
* Patient-refusal rate

**Outcome metrics**

* 30-day readmission rate
* Emergency department utilization
* Inpatient utilization
* Time to readmission
* Readmission rate by risk tier

**Model metrics**

* Top 10% lift
* Top 10% readmission capture
* PR AUC
* ROC AUC
* Risk-tier stability
* Population drift
* Feature drift

**Subgroup metrics**

* Selection rate by subgroup
* Outreach-completion rate by subgroup
* Recall by subgroup
* False negative rate by subgroup
* Readmission outcome by subgroup

### Controlled Pilot Recommendation

The preferred next step is a randomized or controlled outreach pilot.

Possible evaluation designs include:

* Randomized outreach versus usual care within the Top 10% group
* Holdout group receiving the current care-management process
* Phased rollout across facilities or care-management teams
* Matched comparison when randomization is not feasible

A controlled evaluation is necessary because retrospective model performance does not establish intervention effectiveness.

### Business Recommendation

The recommended strategy is:

> Use the provisional Gradient Boosting ranking to identify a high-risk candidate pool from the Top 10% encounter-level threshold. Deduplicate the selected encounters to one priority record per patient, then apply clinical and operational review to assess eligibility, modifiable barriers, and likely outreach actionability before assignment.

The Top 10% group should not be treated as a final ordered list of patients expected to benefit most. The current model predicts readmission risk, not intervention responsiveness.

A controlled pilot should randomize eligible patients to outreach or usual care. The resulting treatment and outcome data could later support uplift modeling or heterogeneous treatment-effect estimation to prioritize patients by expected intervention benefit rather than risk alone.

The pilot should:

* Retain a comparison group
* Track outreach attempts and completion
* Measure 30-day readmission outcomes
* Monitor subgroup selection and missed readmissions
* Review operational workload
* Reassess the threshold after initial results
* Revisit model tuning and calibration before broader implementation

### Outputs Created

Final model and intervention summaries are exported to:

```text
outputs/model_results/final_threshold_summary.csv
outputs/model_results/final_risk_tier_summary.csv
outputs/model_results/intervention_executive_summary.csv
outputs/model_results/intervention_recommendation_summary.csv
outputs/model_results/pilot_monitoring_plan.csv
outputs/model_results/subgroup_monitoring_requirements.csv
outputs/model_results/encounter_patient_deduplication_summary.csv
```

Final outreach outputs are exported to:

```text
outputs/outreach_lists/final_ranked_encounter_list_retrospective.csv
outputs/outreach_lists/top_10_percent_encounter_list_retrospective.csv
outputs/outreach_lists/top_10_encounter_threshold_patient_list_retrospective.csv
outputs/outreach_lists/top_10_encounter_threshold_patient_outreach_list_prototype.csv
```

Final figures are exported to:

```text
outputs/figures/final_lift_by_outreach_threshold.png
outputs/figures/final_outreach_volume_vs_readmission_capture.png
outputs/figures/final_readmission_rate_by_risk_tier.png
```

### Interpretation Limitations

Important limitations include:

* Historical data from 1999–2008
* Retrospective test-set evaluation
* Fixed model parameters
* No final hyperparameter tuning
* No probability calibration
* No external validation
* No prospective operational validation
* Encounter-level predictions requiring patient-level deduplication
* No outreach staffing or cost data
* No intervention completion data
* No randomized intervention results
* No causal evidence that outreach reduces readmissions
* Retrospective subgroup review that does not prove fairness
* Potentially unstable metrics for small subgroups

Model scores should be interpreted as relative ranking values rather than calibrated probabilities.

### Risk Versus Intervention Benefit

This project predicts the risk of 30-day readmission.

It does not predict which patient will benefit most from outreach.

A very high-risk patient may remain high risk even after intervention.

A moderately high-risk patient may be more responsive to outreach than the highest-risk patient.

Future work could estimate intervention benefit using:

* Randomized pilot data
* Uplift modeling
* Treatment-effect estimation
* Heterogeneous treatment-effect models
* Causal machine learning

The current workflow should therefore be interpreted as risk prioritization rather than treatment-effect optimization.

### What This Notebook Does Not Do

This notebook does not perform:

* Model retraining
* Hyperparameter tuning
* Probability calibration
* SHAP analysis
* External validation
* Financial ROI estimation
* Causal inference
* Treatment-effect estimation
* Clinical deployment
* Automated care-management assignment
* Final fairness approval
* Claims that outreach reduces readmission
* Claims that the model is production-ready

Those steps require additional data, prospective validation, controlled intervention testing, and organizational governance.

### Final Project Conclusion

Notebook 07 completes the planned Risk Stratification and Intervention Prioritization workflow.

The project created a patient-aware and leakage-aware process that:

* Cleans and documents the public UCI Diabetes 130-US Hospitals dataset
* Engineers prediction-timing-aware features
* Separates patients across model-validation folds
* Compares baseline and nonlinear models
* Evaluates capacity-based Top 5%, Top 10%, and Top 20% thresholds
* Reviews subgroup selection and performance
* Converts encounter-level rankings into a deduplicated patient-level prototype outreach roster
* Defines a controlled pilot and monitoring strategy

The final recommendation is:

> Pilot outreach for patients represented in the Top 10% highest-risk encounters. Deduplicate selected encounters to one priority record per patient, apply operational eligibility review, retain a comparison group, and monitor operational, outcome, model, and subgroup results.

The project supports intervention prioritization.

It does not establish that the intervention itself is effective.



