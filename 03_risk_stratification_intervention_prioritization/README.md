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
