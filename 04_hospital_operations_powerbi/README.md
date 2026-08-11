# Hospital Operations and Cost Efficiency Analytics

A healthcare analytics project using New York State SPARCS inpatient discharge data to design transparent hospital-utilization benchmarks, governed operational metrics, and a Power BI-ready star schema.

Although this project uses hospital data, the core workflow is transferable to other settings where organizations need to compare operational performance across entities with different case or customer mixes.

## Project Objective

The goal is to identify hospitals and service lines with unusually high utilization, length of stay, estimated cost, or unfavorable outcomes relative to comparable inpatient cases.

The project combines:

* Python for data auditing, metric design, feature engineering, and later model development
* Transparent peer benchmarking for operational comparison
* Machine learning for later retrospective case-mix-adjusted length-of-stay estimation
* Power BI for semantic modeling and executive reporting
* Microsoft Fabric as a planned scalable ingestion, transformation, scoring, and deployment architecture

The project supports investigation and prioritization. It does not establish why a hospital performs differently, prove that excess utilization is preventable, or prescribe clinical interventions.

## Dataset

This project uses the 2023 New York State Hospital Inpatient Discharges dataset released through the Statewide Planning and Research Cooperative System (SPARCS).

The audited file contains:

* 2,125,754 released inpatient discharge records
* 33 source fields
* Hospital and geographic attributes
* Demographic and admission context
* APR-DRG, severity, and mortality-risk classifications
* Diagnosis and procedure classifications
* Length of stay
* Total charges and estimated costs
* Discharge disposition

The analytical unit is one released inpatient discharge record.

The dataset does not contain a unique patient identifier or durable public discharge identifier. Discharge counts must not be interpreted as unique-patient counts, and the data cannot support readmission or longitudinal patient analysis.

## Raw Data Access

Raw data files are not committed to this repository because `data/raw/` is gitignored.

Download the 2023 SPARCS de-identified inpatient discharge dataset from the New York State open-data portal:

```text
https://health.data.ny.gov/Health/Hospital-Inpatient-Discharges-SPARCS-De-Identified/46xm-urtu
```

Export the dataset as CSV, rename it if necessary, and place it at:

```text
data/raw/sparcs_inpatient_2023.csv
```

The audit notebook expects that exact filename and path.

## Business Question

Which hospitals and service lines demonstrate unusually high inpatient utilization, length of stay, estimated cost, or unfavorable outcomes relative to comparable cases?

Supporting questions include:

* Where are inpatient stays longer than expected?
* Which facilities or service lines contribute the most excess inpatient days?
* Which facilities have high estimated costs, and how are those patterns associated with volume, LOS, and case mix?
* Which operational differences are sufficiently large and reliable to prioritize for further investigation?

## Analytical Scope

The current design supports:

* Inpatient discharge volume
* Total and distributional LOS analysis
* Emergency and elective admission mix
* APR-DRG and service-line composition
* Severity-of-illness and mortality-risk distributions
* Payer, demographic, disposition, and geographic context
* Charges and released estimated costs
* Leave-one-facility-out peer benchmarks
* Future retrospective case-mix-adjusted expected LOS
* Power BI semantic-model design
* Conservative small-cell reporting controls

The project does not support:

* Unique-patient counts
* Patient-level longitudinal analysis
* Readmission measurement
* Monthly trends or seasonality
* True bed-capacity utilization without staffed-bed data
* Real-time or admission-time clinical prediction
* Audited profitability or reimbursement analysis
* Causal claims about hospital performance

## Environment & Setup

The current notebooks are designed for a standard Python virtual environment.

Recommended setup:

```bash
python -m venv .venv
```

Activate the environment:

```bash
# Windows
.venv\Scripts\activate
```

```bash
# macOS / Linux
source .venv/bin/activate
```

Install the packages required by the current notebooks:

```bash
pip install pandas duckdb jupyter
```

Later modeling and visualization work may add packages such as `numpy`, `scikit-learn`, gradient-boosting libraries, and plotting libraries.

## Project Workflow

The completed design-stage workflow covers:

* Source-file and schema auditing
* Missingness and cardinality profiling
* Numeric parsing and distribution review
* LOS top-coding assessment
* Financial-field interpretation
* Apparent duplicate-pattern assessment
* Facility-key consistency review
* Metric catalog and denominator design
* Category-mapping specifications
* Peer-benchmark design
* Small-cell suppression rules
* Logical star-schema and relationship design
* Source-to-model lineage
* Machine-readable validation and documentation exports

Planned later stages include:

* Reproducible data cleaning and dimensional-table construction
* Peer-benchmark calculation
* DAX measure implementation
* Power BI report development
* Retrospective expected-LOS model development and validation
* Versioned model scoring outputs
* Model-performance and stability monitoring
* Microsoft Fabric architecture and deployment design

## Notebook 01: SPARCS Data and Schema Audit

Notebook 01 audits the structure, quality, and analytical usability of the 2023 SPARCS inpatient discharge file.

The notebook is descriptive. It does not clean records, engineer features, remove apparent duplicates, or train predictive models.

### Main Work Completed

* Validated the raw source file and its schema
* Recorded file metadata and a SHA-256 reproducibility hash
* Confirmed 2,125,754 discharge records and 33 fields
* Measured missingness and cardinality across every field
* Reviewed released categorical values and de-identification patterns
* Validated parsing for LOS, charges, estimated costs, and related numeric fields
* Examined LOS and financial distributions
* Identified LOS top-coding
* Assessed fully repeated value patterns without deleting rows
* Evaluated facility-name and permanent-facility-ID consistency
* Exported reusable audit tables for downstream notebooks

### Length-of-Stay Findings

Length of stay is strongly right-skewed:

* Lower-bound mean LOS: approximately 5.78 days
* Median LOS: 3 days
* Approximately 2,290 records are released as `120 +`
* Top-coded records represent approximately 0.108% of the dataset

When a numeric value is needed, `120 +` is represented as an observable lower bound of 120 days. It must not be interpreted as an exact 120-day stay.

### Financial Findings

Charges and estimated costs are also strongly right-skewed:

* Mean total charges: approximately $83,340
* Median total charges: approximately $43,901
* Mean estimated costs: approximately $25,155
* Median estimated costs: approximately $13,234

`Total Charges` represents billed charges, not reimbursement or revenue.

`Total Costs` is a released analytical estimate and should not be described as audited hospital expense.

### Duplicate-Pattern Review

The audit found fully repeated released-value patterns, but no records were removed.

Because the public-use dataset has no unique discharge identifier, identical released rows may represent separate real discharges whose distinguishing information was removed during de-identification. Repeated rows therefore cannot automatically be classified as erroneous duplicates.

### Modeling Implications

The primary modeling objective is retrospective case-mix-adjusted LOS estimation rather than admission-time clinical prediction.

The primary model will exclude:

* LOS-derived variables
* Charges and estimated costs
* Patient disposition
* Other downstream resource-use or post-outcome information

Hospital identity will be evaluated only in documented sensitivity analysis because including it in the primary model could absorb the facility differences the project is intended to measure.

Because the audited source currently contains only 2023 records, future-year stability cannot yet be demonstrated.

### Outputs Created

Notebook 01 exports audit artifacts to:

```text
outputs/data_audit/
```

Key outputs include:

```text
file_metadata.csv
schema.csv
required_field_availability.csv
column_profile.csv
categorical_counts.csv
numeric_audit.csv
los_distribution.csv
financial_distribution.csv
duplicate_summary.csv
facility_key_audit.csv
facility_name_audit.csv
```

### What This Notebook Does Not Do

Notebook 01 does not perform:

* Data cleaning or recoding
* Missing-value imputation
* Duplicate removal
* Feature engineering
* Predictive modeling
* Multi-year integration
* Power BI ingestion

## Notebook 02: Metric Catalog and Benchmark Design

Notebook 02 converts the audit findings into formal specifications for operational metrics, denominator rules, category mappings, peer benchmarks, and reporting suppression.

It defines how metrics should be calculated but does not yet calculate hospital performance from the raw discharge file.

### Main Work Completed

* Loaded and validated Notebook 01 outputs
* Confirmed availability of metric- and benchmark-critical fields
* Defined source grain and aggregation standards
* Created a machine-readable metric catalog
* Defined valid-record, denominator, exclusion, and display rules
* Added robust LOS statistics, including median, IQR, and P95
* Defined financial, admission-context, case-mix, disposition, and outcome metrics
* Created approved category-mapping specifications
* Defined leave-one-facility-out LOS and estimated-cost peer benchmarks
* Separated descriptive peer expectations from later model predictions
* Defined conservative small-cell suppression controls
* Exported validated specifications and business-readable documentation

### Metric Framework

The metric catalog currently contains 32 governed metrics across:

* Volume
* Length of stay
* Financial indicators
* Admission context
* Case mix
* Outcomes
* Descriptive benchmarking

Examples include:

* Discharges
* Total LOS Days — Lower Bound
* Average LOS — Lower Bound
* Median LOS
* LOS Interquartile Range
* P95 LOS
* Extended-Stay Rate
* Total Charges
* Median Charge per Discharge
* Total Estimated Costs
* Estimated Cost per Inpatient Day
* Emergency Admission Rate
* Major or Extreme Severity Rate
* Home Discharge Rate
* In-Hospital Mortality Rate
* Disposition Share
* Peer-Expected LOS Days
* LOS Actual-to-Peer-Expected Ratio
* Excess LOS Days — Lower Bound
* Estimated Cost Actual-to-Peer-Expected Ratio

Extended-Stay Rate remains pending until an operational LOS threshold is approved.

### Peer-Benchmark Design

The primary descriptive peer definition uses:

```text
APR-DRG Code × APR Severity of Illness Code
```

If that peer group contains fewer than 30 eligible comparison discharges after excluding the benchmarked facility, the design falls back to:

```text
APR-DRG Code
```

If the fallback group also contains fewer than 30 comparison discharges, the peer expectation remains missing.

Each facility is excluded from its own comparison benchmark. This prevents the focal facility from materially influencing the expected value used to evaluate it.

The initial peer expectation is a descriptive baseline. It is not a machine-learning prediction, clinical expectation, formal risk-adjusted quality measure, or causal estimate.

Peer-median benchmarks are retained as deferred contextual measures. Their aggregation across multiple peer groups must be defined before implementation.

### Small-Cell Suppression

The project uses a conservative reporting standard:

* Displayed discharge counts from 1 through 10 are suppressed
* Continuous summaries and aggregate amounts are suppressed when fewer than 11 discharges contribute
* Rates are suppressed when the denominator is below 11 or when the numerator or complement would expose a count from 1 through 10
* Zero may be displayed when the true value is zero

Complementary suppression and cross-filter inference still require review during Power BI implementation.

### Outputs Created

Notebook 02 exports specification artifacts to:

```text
outputs/metric_catalog/
```

Key outputs include:

```text
metric_catalog.csv
category_mapping.csv
benchmark_specification.csv
suppression_policy.csv
design_standards.csv
benchmark_field_validation.csv
metric_field_validation.csv
validation_results.csv
```

It also generates:

```text
docs/metric_catalog.md
```

### What This Notebook Does Not Do

Notebook 02 does not perform:

* Raw-data cleaning
* Final KPI calculation
* Feature engineering
* Model training
* Risk-adjusted cost modeling
* DAX implementation
* Causal performance attribution

## Notebook 03: Star Schema Design and Relationship Specification

Notebook 03 converts the audited fields and approved analytical specifications into a documented logical star schema for Power BI.

It designs the semantic model but does not physically construct Power Query tables, create DAX measures, or build report pages.

### Main Work Completed

* Loaded and validated Notebook 01 and Notebook 02 outputs
* Defined the one-discharge-per-row `FactDischarge` grain
* Defined dimension-table grains and business roles
* Classified all 33 audited source fields as included or staging-only
* Defined source-to-model lineage
* Specified whole-number surrogate keys
* Reserved key `0` for Unknown or Not Available members
* Defined active one-to-many, single-direction relationships
* Confirmed model support for all 32 catalog metrics
* Defined deferred storage requirements for peer benchmarks
* Documented a later versioned model-prediction extension
* Exported machine-readable schema and validation artifacts

### Logical Model

The initial semantic model contains:

```text
FactDischarge
├── DimHospital
├── DimDate
├── DimService
├── DimCaseMix
├── DimDiagnosis
├── DimProcedure
├── DimPatientSegment
├── DimGeography
├── DimPayer
└── DimAdmissionContext
```

A disconnected `Measures` table provides a governed location for explicit DAX measures.

All descriptive dimensions filter `FactDischarge` through active, one-to-many, single-direction relationships.

### Fact Grain and Key Policy

`FactDischarge` contains one row per released inpatient discharge.

The model does not invent a durable patient or longitudinal discharge identifier. Missing, suppressed, or unresolved dimension values map to surrogate key `0` so fact rows are preserved.

Released natural identifiers remain available as descriptive attributes, while technical surrogate and foreign keys are intended to be hidden from report users.

### Deferred Prediction Extension

Validated machine-learning predictions will remain separate from descriptive peer-benchmark values.

The later modeling phase must define versioned prediction outputs containing:

* A technical source-record key scoped to the source snapshot
* Source snapshot or file identifier
* Model version
* Scoring timestamp
* Model-predicted LOS
* Prediction status or coverage flag
* Missing-prediction reason
* Optional validated P50 or P90 estimates

The technical source-record key must not be described as a patient identifier or durable longitudinal discharge identifier.

`peer_expected_los_days` and `model_predicted_los_days` must remain distinct fields with distinct interpretations.

### Outputs Created

Notebook 03 exports schema artifacts to:

```text
outputs/star_schema/
```

Key outputs include:

```text
table_specification.csv
column_specification.csv
source_to_model_mapping.csv
relationship_specification.csv
key_policy.csv
metric_support_matrix.csv
schema_validation_results.csv
design_standards.csv
```

It also generates:

```text
docs/star_schema.md
```

### Remaining Physical Validations

The following checks are deferred until the dimensional tables are constructed:

* Dimension-key uniqueness
* Natural-key-to-description consistency
* Orphan foreign keys
* Fact-row reconciliation
* Unknown-member assignment
* Data-type conversion
* Financial and LOS validity flags
* Actual Power BI relationship cardinality
* Semantic-model memory usage

### What This Notebook Does Not Do

Notebook 03 does not build:

* Power Query transformations
* Physical fact or dimension tables
* DAX measures
* Power BI report pages
* Hospital rankings
* Predictive models
* Fabric pipelines

## Project Structure

```text
04_hospital_operations_powerbi/
├── data/
│   └── raw/
│       └── sparcs_inpatient_2023.csv
├── docs/
│   ├── project_charter.md
│   ├── metric_catalog.md
│   └── star_schema.md
├── notebooks/
│   ├── 01_data_audit.ipynb
│   ├── 02_metric_catalog_and_benchmark_design.ipynb
│   └── 03_star_schema_design.ipynb
├── outputs/
│   ├── data_audit/
│   ├── metric_catalog/
│   └── star_schema/
├── .gitignore
└── README.md
```

## Execution Order

For a complete clean run, execute the notebooks in numerical order:

```text
01_data_audit.ipynb
02_metric_catalog_and_benchmark_design.ipynb
03_star_schema_design.ipynb
```

Notebook 02 depends on exported audit outputs from Notebook 01.

Notebook 03 depends on the audited schema and validated metric-catalog outputs from Notebooks 01 and 02.

The notebooks use dynamic project-root detection based on `docs/project_charter.md`, so paths resolve relative to the repository rather than through hard-coded user-specific locations.

## Privacy and Reporting Standards

The source is publicly released and de-identified, but the project applies conservative reporting controls.

Planned dashboard controls include:

* Suppressing or masking displayed groups with fewer than 11 discharges
* Reducing reconstruction risk from totals where practical
* Flagging statistically unstable low-volume comparisons
* Avoiding patient-level dashboard views
* Avoiding unnecessarily granular public exports

The threshold of 11 is a conservative project reporting standard. It is not presented as a universal SPARCS publication rule.

## Interpretation Limitations

Important limitations include:

* The data represent released discharge records rather than unique patients
* No readmission or longitudinal patient analysis is possible
* Monthly analysis is unavailable because only discharge year is present
* LOS values released as `120 +` are right-censored
* Charges are not reimbursement, revenue, or profit
* Estimated costs are not audited hospital expenses
* APR-DRG and severity do not capture every case-mix difference
* Hospital structural characteristics are not yet incorporated
* Peer benchmarks are descriptive rather than formal clinical risk adjustment
* Peer differences do not prove inefficiency, preventability, or causality
* Multi-year schema compatibility and future-year stability have not yet been established
* The current project phase does not include a completed Power BI report or validated predictive model

## Planned Next Steps

Planned work includes:

* Constructing the physical fact and dimension tables
* Calculating leave-one-facility-out peer benchmarks
* Defining and implementing explicit DAX measures
* Building Power BI executive and operational report pages
* Developing baseline and candidate expected-LOS models
* Comparing models using identical validation data
* Evaluating calibration and subgroup performance
* Producing versioned prediction outputs
* Reconciling Power BI measures to independent Python calculations
* Evaluating multi-year data compatibility
* Designing the Desktop-to-Fabric deployment path

## Final Project Statement

This project builds an end-to-end hospital operations analytics solution that combines Python, transparent benchmarking, semantic modeling, machine learning, Microsoft Fabric, and Power BI to identify excess inpatient resource utilization after accounting for observable case complexity.
