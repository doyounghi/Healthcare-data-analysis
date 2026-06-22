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

