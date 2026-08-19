# Hospital Operations and Cost Efficiency Analytics

A healthcare analytics project using New York State SPARCS inpatient discharge data to design, build, and validate transparent hospital-utilization benchmarks, governed operational metrics, and a Power BI-ready star schema.

Although this project uses hospital data, the core workflow is transferable to other settings where organizations need to compare operational performance across entities with different case or customer mixes.

## Project Objective

The goal is to identify hospitals and service lines with unusually high utilization, length of stay, estimated cost, or unfavorable outcomes relative to comparable inpatient cases.

The project combines:

* Python and DuckDB for data auditing, metric design, transformation, validation, and later model development
* Transparent leave-one-facility-out peer benchmarking for operational comparison
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

The audit and physical-model notebooks expect that exact filename and path.

## Business Question

Which hospitals and service lines demonstrate unusually high inpatient utilization, length of stay, estimated cost, or unfavorable outcomes relative to comparable cases?

Supporting questions include:

* Where are inpatient stays longer than expected?
* Which facilities or service lines contribute the most excess inpatient days?
* Which facilities have high estimated costs, and how are those patterns associated with volume, LOS, and case mix?
* Which operational differences are sufficiently large and reliable to prioritize for further investigation?

## Analytical Scope

The current implementation supports:

* Inpatient discharge volume
* Total and distributional LOS analysis
* Emergency and elective admission mix
* APR-DRG and service-line composition
* Severity-of-illness and mortality-risk distributions
* Payer, demographic, disposition, and geographic context
* Charges and released estimated costs
* Leave-one-facility-out LOS and estimated-cost peer benchmarks
* Primary APR-DRG × severity benchmarks with APR-DRG fallback
* Power BI-ready dimensional tables and benchmarked fact-table exports
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

The completed workflow currently covers:

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
* Physical staging and dimensional-model construction
* Natural-key, surrogate-key, foreign-key, datatype, and row-count validation
* Power BI-ready Parquet export
* Leave-one-facility-out LOS and estimated-cost benchmark calculation
* Primary-versus-fallback benchmark assignment
* Benchmark coverage and peer-size diagnostics
* Independent mathematical reconciliation of benchmark calculations
* Machine-readable validation and business-readable documentation exports

Planned later stages include:

* Explicit DAX measure implementation
* Power BI semantic-model construction and relationship verification
* Small-cell suppression implementation in Power BI
* Semantic-model memory and performance testing
* Power BI executive and operational report development
* Retrospective expected-LOS model development and validation
* Model calibration and subgroup validation
* Versioned model scoring outputs
* Multi-year compatibility testing
* Microsoft Fabric architecture and deployment design
* Deferred peer-median contextual benchmarks

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
* 2,290 records are released as `120 +`
* Top-coded records represent approximately 0.108% of the dataset

When a numeric value is needed, `120 +` is represented as an observable lower bound of 120 days. It must not be interpreted as an exact 120-day stay.

### Financial Findings

Charges and estimated costs are also strongly right-skewed.

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

It defines how metrics should be calculated but does not calculate hospital performance from the raw discharge file.

### Main Work Completed

* Loaded and validated Notebook 01 outputs
* Confirmed availability of metric- and benchmark-critical fields
* Defined source grain and aggregation standards
* Created a machine-readable metric catalog
* Defined valid-record, denominator, exclusion, and display rules
* Added robust LOS statistics, including median, IQR, and P95
* Defined financial, admission-context, case-mix, disposition, and outcome metrics
* Created and approved category-mapping specifications
* Defined leave-one-facility-out LOS and estimated-cost peer benchmarks
* Separated descriptive peer expectations from later model predictions
* Defined conservative small-cell suppression controls
* Exported validated specifications and business-readable documentation

### Metric Framework

The metric catalog contains 32 governed metrics across:

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

Each facility is excluded from its own comparison benchmark. This prevents the focal facility from influencing the expected value used to evaluate it.

LOS and estimated-cost comparison populations are handled independently according to their governed validity rules.

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
export_manifest.csv
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

It designs the semantic model but does not physically construct the tables, create DAX measures, or build report pages.

### Main Work Completed

* Loaded and validated Notebook 01 and Notebook 02 outputs
* Confirmed required metrics and primary benchmark specifications
* Defined the one-discharge-per-row `FactDischarge` grain
* Defined dimension-table grains and business roles
* Classified every audited source field as included or staging-only
* Defined source-to-model lineage
* Specified whole-number surrogate keys
* Reserved key `0` for Unknown or Not Available members
* Defined active one-to-many, single-direction relationships
* Confirmed required metric dependencies are represented in the model
* Defined storage requirements for LOS and estimated-cost peer benchmarks
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

`DimService` uses the composite natural key:

```text
APR-DRG Code × APR MDC Code
```

This physical dimension grain is required because APR-DRG alone does not uniquely determine APR-MDC in the validated 2023 source.

The service-dimension grain does not change the analytical peer-benchmark grain, which remains APR-DRG × severity with APR-DRG fallback.

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

### Physical Validations Implemented Downstream

Notebook 04 subsequently validates the physical implementation for:

* Dimension-key uniqueness
* Natural-key-to-description consistency
* Orphan foreign keys
* Fact-row reconciliation
* Unknown-member assignment
* Data-type conversion
* Financial and LOS validity flags
* Exported Parquet row and schema reconciliation

Actual Power BI relationship behavior and semantic-model memory usage remain downstream.

### What This Notebook Does Not Do

Notebook 03 does not build:

* Physical fact or dimension tables
* DAX measures
* Power BI report pages
* Hospital rankings
* Predictive models
* Fabric pipelines

## Notebook 04: Physical Data Model Build and Validation

Notebook 04 converts the approved logical schema into a reproducible physical star schema and validates that the implementation preserves the governed source grain, transformation rules, and schema specifications.

### Main Work Completed

* Loaded and validated committed outputs from Notebooks 01–03
* Confirmed the raw file matches the Notebook 01 SHA-256 source snapshot
* Confirmed source schema and row count match the audit
* Applied only approved Notebook 02 category mappings
* Validated complete mapping coverage before transformation
* Standardized text and missing-value handling
* Parsed LOS while preserving `120 +` as an observable 120-day lower bound
* Created LOS top-code and validity flags
* Parsed positive charges and estimated costs and created financial validity flags
* Retained repeated released-value rows rather than treating them as proven duplicates
* Validated natural-key-to-description consistency before constructing dimensions
* Built all 10 approved physical dimensions
* Assigned deterministic whole-number surrogate keys
* Reserved surrogate key `0` for Unknown / Not Available
* Built `FactDischarge` with 2,125,754 rows
* Preserved complete source-to-fact row reconciliation
* Validated dimension-key uniqueness and foreign-key integrity
* Validated physical columns and datatypes against Notebook 03
* Created six typed peer-benchmark placeholder columns
* Exported and re-read Power BI-ready compressed Parquet tables
* Generated physical-model documentation

### Physical Model

The physical build contains:

```text
FactDischarge           2,125,754 rows
DimHospital                   208 rows
DimDate                         2 rows
DimService                    483 rows
DimCaseMix                     17 rows
DimDiagnosis                  483 rows
DimProcedure                  321 rows
DimPatientSegment            203 rows
DimGeography                  51 rows
DimPayer                       10 rows
DimAdmissionContext           201 rows
```

All 10 dimensions contain exactly one key-`0` Unknown / Not Available member.

The fact table contains no null foreign keys and no orphan foreign keys.

### Validation Highlights

Notebook 04 validates:

* Raw-source snapshot reproducibility
* Approved mapping coverage
* Source-to-staging row reconciliation
* Source-to-fact row reconciliation
* Natural-key attribute consistency
* APR severity code/description domain consistency
* Dimension primary-key uniqueness
* Unknown-member policy
* Foreign-key completeness
* Physical column agreement with Notebook 03
* Physical datatype agreement with Notebook 03
* LOS and financial flag consistency
* Parquet row-count and schema reconciliation

All physical-model validation gates pass in Notebook 04.

### Outputs Created

Notebook 04 exports Power BI-ready tables to:

```text
outputs/physical_model/tables/
```

including:

```text
FactDischarge.parquet
DimHospital.parquet
DimDate.parquet
DimService.parquet
DimCaseMix.parquet
DimDiagnosis.parquet
DimProcedure.parquet
DimPatientSegment.parquet
DimGeography.parquet
DimPayer.parquet
DimAdmissionContext.parquet
```

Validation and documentation artifacts are exported to:

```text
outputs/physical_model/
docs/physical_data_model.md
```

### What This Notebook Does Not Do

Notebook 04 does not:

* Calculate descriptive peer expectations
* Calculate final business KPIs
* Implement DAX
* Build Power BI report pages
* Train predictive models
* Create patient or longitudinal identifiers
* Perform causal analysis

The six peer-benchmark columns are intentionally left empty for Notebook 05.

## Notebook 05: Leave-One-Facility-Out Peer Benchmark Calculation and Validation

Notebook 05 implements the governed descriptive peer-benchmark methodology defined in Notebook 02 and populates the six benchmark columns reserved in the physical fact table by Notebooks 03 and 04.

### Main Work Completed

* Loaded and validated committed outputs from Notebooks 02–04
* Confirmed all Notebook 04 benchmark placeholders were initially empty
* Loaded the validated physical star schema from Parquet
* Recovered facility, APR-DRG, and severity context from the dimensions
* Profiled LOS and estimated-cost benchmark eligibility
* Calculated leave-one-facility-out APR-DRG × severity LOS expectations
* Calculated APR-DRG LOS fallback expectations
* Calculated leave-one-facility-out APR-DRG × severity estimated-cost expectations
* Calculated APR-DRG estimated-cost fallback expectations
* Enforced a minimum of 30 comparison discharges after focal-facility exclusion
* Resolved primary, fallback, and unavailable benchmark levels independently for LOS and cost
* Populated all six governed benchmark fields
* Preserved all 2,125,754 fact rows and every non-benchmark fact value
* Validated benchmark-level selection logic
* Reconciled benchmark calculations through an independent query path
* Validated fact-table schema preservation
* Exported and re-read the benchmarked compressed Parquet fact table
* Generated benchmark coverage and peer-size diagnostics
* Generated business-readable benchmark methodology documentation

### Implemented Benchmark Logic

Primary peer group:

```text
APR-DRG Code × APR Severity of Illness Code
```

Fallback peer group:

```text
APR-DRG Code
```

For every focal hospital:

1. All eligible records from that hospital are excluded from its own comparison population.
2. The primary peer expectation is used when at least 30 comparison discharges remain.
3. The APR-DRG fallback is used when the primary group is insufficient but the fallback contains at least 30 comparison discharges.
4. Otherwise, the expectation remains unavailable.
5. LOS and estimated-cost eligibility are evaluated independently.
6. Unavailable expected values remain null rather than zero.

Hospital key `0` does not receive a leave-one-facility-out benchmark.

### Benchmark Coverage

The benchmarked fact table contains 2,125,754 rows.

For both LOS and estimated cost:

* 2,120,362 rows receive a benchmark: approximately 99.7463%
* 2,117,792 rows use the primary APR-DRG × severity benchmark: approximately 99.6255%
* 2,570 rows use the APR-DRG fallback: approximately 0.1209%
* 5,392 rows are unavailable: approximately 0.2537%

Of the unavailable rows:

* 5,333 have an unresolved hospital
* 59 have insufficient comparison volume

The primary benchmark therefore covers nearly the entire released dataset while preserving an explicit fallback and unavailable state.

### Downstream Measures Supported

The benchmarked fact table can support governed measures such as:

* Peer-Expected LOS Days
* LOS Actual-to-Peer-Expected Ratio
* Excess LOS Days — Lower Bound
* Peer-Expected Estimated Cost
* Estimated Cost Actual-to-Peer-Expected Ratio
* Excess Estimated Cost

These measures are not yet implemented as DAX in these notebooks.

### Validation Highlights

Notebook 05 validates that:

* Notebook 02, 03, and 04 validation gates have passed
* Benchmark context preserves the 2,125,754-row fact grain
* Benchmarked `FactDischarge` preserves the same row count
* Non-benchmark fact columns remain unchanged
* Benchmark-selection logic has no violations
* Direct mathematical reconciliation passes for sampled comparisons
* The fact-table schema remains unchanged
* Both LOS and estimated-cost benchmarks have nonzero coverage
* Exported Parquet row counts and schema reconcile to the in-memory build

### Outputs Created

Notebook 05 exports the benchmarked fact table to:

```text
outputs/peer_benchmarks/tables/FactDischarge.parquet
```

Key diagnostic and validation outputs include:

```text
benchmark_standards.csv
benchmark_specification_snapshot.csv
benchmark_eligibility.csv
benchmark_coverage.csv
benchmark_peer_size_summary.csv
manual_reconciliation.csv
selection_logic_validation.csv
benchmark_validation_results.csv
parquet_validation.csv
export_manifest.csv
```

It also generates:

```text
docs/peer_benchmarks.md
```

Notebook 04 outputs remain the immutable pre-benchmark physical layer.

### What This Notebook Does Not Do

Notebook 05 does not perform:

* Machine-learning prediction
* Formal clinical risk adjustment
* Causal attribution
* Hospital-quality grading
* Clinical recommendation
* DAX implementation
* Power BI report construction

## Project Structure

```text
04_hospital_operations_powerbi/
├── data/
│   └── raw/
│       └── sparcs_inpatient_2023.csv
├── docs/
│   ├── project_charter.md
│   ├── metric_catalog.md
│   ├── star_schema.md
│   ├── physical_data_model.md
│   └── peer_benchmarks.md
├── notebooks/
│   ├── 01_data_audit.ipynb
│   ├── 02_metric_catalog_and_benchmark_design.ipynb
│   ├── 03_star_schema_design.ipynb
│   ├── 04_physical_data_model_build.ipynb
│   └── 05_peer_benchmark_calculation.ipynb
├── outputs/
│   ├── data_audit/
│   ├── metric_catalog/
│   ├── star_schema/
│   ├── physical_model/
│   │   └── tables/
│   └── peer_benchmarks/
│       └── tables/
├── .gitignore
└── README.md
```

## Execution Order

For a complete clean run, execute the notebooks in numerical order:

```text
01_data_audit.ipynb
02_metric_catalog_and_benchmark_design.ipynb
03_star_schema_design.ipynb
04_physical_data_model_build.ipynb
05_peer_benchmark_calculation.ipynb
```

Notebook 02 depends on exported audit outputs from Notebook 01.

Notebook 03 depends on the audited schema and validated metric-catalog outputs from Notebooks 01 and 02.

Notebook 04 depends on committed specifications and validation outputs from Notebooks 01–03 and independently verifies that the raw source still matches the audited snapshot before constructing the physical model.

Notebook 05 depends on the governed benchmark specification, logical schema, and validated physical Parquet outputs from Notebooks 02–04.

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
* LOS values released as `120 +` are right-censored and are represented only as observable lower bounds when numeric analysis is required
* Charges are not reimbursement, revenue, or profit
* Estimated costs are not audited hospital expenses
* APR-DRG and severity do not capture every case-mix difference
* Hospital structural characteristics are not yet incorporated
* Peer benchmarks are descriptive rather than formal clinical risk adjustment
* Peer differences do not prove inefficiency, preventability, poor quality, or causality
* Multi-year schema compatibility and future-year stability have not yet been established
* The current project phase does not include a completed Power BI report or validated predictive model

## Planned Next Steps

Planned work includes:

* Defining and implementing explicit DAX measures
* Implementing conservative small-cell suppression logic in Power BI
* Building and validating the Power BI semantic model
* Verifying relationship cardinality and filter direction in Power BI
* Testing semantic-model memory and performance
* Building executive and operational report pages
* Reconciling Power BI measures to independent Python calculations
* Developing baseline and candidate expected-LOS models
* Comparing models using identical validation data
* Evaluating calibration and subgroup performance
* Producing versioned prediction outputs
* Evaluating multi-year data compatibility
* Designing the Desktop-to-Fabric deployment path
* Defining aggregation rules before implementing deferred peer-median contextual benchmarks

## Final Project Statement

This project builds an end-to-end hospital operations analytics solution that combines reproducible Python and DuckDB data engineering, governed metrics, validated star-schema modeling, transparent leave-one-facility-out benchmarking, planned machine learning, Microsoft Fabric, and Power BI to identify inpatient resource-utilization patterns after accounting for observable case complexity.
