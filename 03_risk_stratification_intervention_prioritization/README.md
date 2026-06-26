# Risk Stratification and Intervention Prioritization

A healthcare data science project using public diabetes hospital readmission data to predict 30-day readmission risk and translate model scores into a capacity-constrained outreach prioritization strategy.

Although this project uses healthcare data, the core workflow is transferable to many industries where teams must rank high-risk cases and prioritize limited intervention capacity.

## Project Objective

The goal is to identify diabetic inpatient encounters with higher predicted 30-day readmission risk and prioritize post-discharge outreach when care management capacity is limited.

## Dataset

This project uses the UCI Diabetes 130-US Hospitals for Years 1999–2008 dataset.

The dataset contains 101,766 hospital encounter records for patients diagnosed with diabetes and supports a classification task related to early readmission within 30 days after discharge.

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
outputs/model_results/model_feature_list.csv
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


