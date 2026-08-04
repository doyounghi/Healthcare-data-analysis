# Project Charter — Hospital Operations & Cost Efficiency Analytics

## 1. Project Overview

This project develops an end-to-end hospital operations analytics product using publicly available, de-identified New York State inpatient discharge data.

The solution will integrate:

- Python for data auditing, analysis, feature engineering, and modeling
- Machine learning for case-mix-adjusted length-of-stay benchmarking
- Power BI for semantic modeling and executive reporting
- Microsoft Fabric for scalable ingestion, transformation, scoring, and deployment

The analytical unit is one inpatient discharge.

---

## 2. Business Problem

Hospital performance cannot be evaluated fairly using raw volume, length of stay, charges, estimated costs, or mortality alone.

Hospitals treat populations with different:

- Diagnoses
- Severity levels
- Mortality risks
- Admission types
- Age distributions
- Payer mixes
- Regional and structural characteristics

The project will identify hospitals and service lines that use more inpatient resources than expected after accounting for observable case complexity.

The central business question is:

> Which hospitals and service lines demonstrate unusually high utilization, length of stay, estimated cost, or unfavorable outcomes relative to comparable cases?

---

## 3. Business Objectives

The project will:

1. Measure inpatient demand, utilization, financial indicators, and outcomes.
2. Compare hospitals and service lines using transparent peer benchmarks.
3. Develop and validate models estimating case-mix-adjusted length of stay.
4. Quantify excess inpatient days relative to modeled expectations.
5. Surface operational areas requiring further investigation.
6. Deliver results through an executive Power BI dashboard.
7. Demonstrate a scalable Desktop-to-Fabric analytics architecture.

The project supports investigation and prioritization. It does not prove why a hospital performs differently or prescribe clinical interventions.

---

## 4. Intended Users

Primary users:

- Hospital chief operating officers
- Hospital chief financial officers
- Operations directors
- Service-line leaders
- Business intelligence and analytics teams

Secondary users:

- Quality-improvement teams
- Population-health analysts
- Data science and analytics engineering teams

---

## 5. Decisions Supported

The dashboard should help users decide:

- Which hospitals or service lines require operational investigation?
- Where are inpatient stays longer than expected?
- Which areas contribute the most excess inpatient days?
- Which facilities have high estimated costs, and are those patterns associated with volume, LOS, or case mix?
- How are unfavorable results associated with case mix, volume, and actual-versus-expected performance?
- Which operational opportunities are sufficiently large and reliable to prioritize?

The dashboard will not independently determine staffing, contracting, reimbursement, or clinical-treatment decisions.

---

## 6. Data Source

The primary source will be the New York State SPARCS public-use inpatient discharge data.

Initial development will use one compatible year, tentatively 2023. Multi-year data will be added only after evaluating:

- Schema consistency
- Category-definition changes
- Coding changes
- Missingness
- File size
- Data availability
- Comparability across years

The data are de-identified and do not support longitudinal patient tracking.

Raw data files will not be committed to GitHub. The repository will provide official source links and reproducible ingestion instructions.

---

## 7. Analytical Scope

### Included

- Inpatient discharge volume
- Total inpatient days
- Length-of-stay distribution
- Emergency versus elective admission mix
- APR-DRG and service-line composition
- Severity-of-illness distribution
- Risk-of-mortality distribution
- Discharge disposition
- In-hospital mortality
- Payer mix
- Hospital and geographic comparisons
- Charges
- Estimated costs, when consistently available and documented
- Case-mix-adjusted expected length of stay
- Actual-versus-expected performance
- Excess inpatient days
- Model performance and stability monitoring

### Excluded

- Patient-level longitudinal analysis
- Readmission measurement or prediction
- Causal claims about hospital performance
- Clinical treatment recommendations
- Real-time admission-level predictions
- True bed-capacity utilization without staffed-bed data
- Audited profitability or reimbursement analysis
- Claims that charges represent costs or payments
- Hospital-quality rankings based only on raw mortality
- Real-time streaming architecture

---

## 8. Primary Metrics

### Volume and utilization

- Discharges
- Total inpatient days
- Average length of stay
- Median length of stay
- Interquartile range of length of stay
- Extended-stay rate
- Emergency admission rate

### Financial indicators

- Total charges
- Median charge per discharge
- Estimated cost per discharge
- Estimated cost per inpatient day
- Charge-to-estimated-cost ratio
- Average and median charge per discharge
- Average and median estimated cost per discharge

Charges will be labeled as charges—not revenue, reimbursement, payment, or cost.

Any available estimated-cost field will be described as an analytical estimate rather than audited operating expense.

### Outcomes

- Home discharge rate
- In-hospital mortality rate
- Disposition distribution

### Case-mix-adjusted metrics

- Predicted length of stay
- Actual-minus-predicted length of stay
- Aggregate excess inpatient days
- Actual-to-expected LOS ratio
- Percentage of stays exceeding predicted P90 LOS, if a validated quantile model is implemented
- Model coverage and missing-prediction rate

The meaning of “expected LOS” will depend on the selected model:

- Conditional-mean predictions may support aggregate expected-day calculations.
- Conditional-median predictions will be labeled as predicted median LOS.
- Log-scale models will require an appropriate retransformation method before producing raw-day expectations.

---

## 9. Distributional Strategy

Length of stay, charges, and estimated costs are expected to be strongly right-skewed.

Therefore:

- Means will not be used alone.
- Medians, percentiles, and interquartile ranges will accompany averages.
- Extreme values will be investigated rather than automatically removed.
- Transformations such as `log1p()` may be evaluated during modeling.
- Raw-scale and transformed-scale performance will be reported separately where appropriate.
- Business benchmarking will prioritize interpretable day-level errors.

---

## 10. Peer Benchmarking Strategy

The initial transparent benchmark will compare discharges with similar:

- APR-DRG
- Severity of illness
- Age group, when justified
- Admission type, when justified

Additional structural variables may include:

- Region
- Teaching or academic status
- Safety-net status
- Hospital size
- Regional wage environment

These variables will only be included if they can be linked from reliable public sources with defensible definitions.

If structural variables are unavailable, the limitation will be reported explicitly. Sensitivity analyses may compare models with and without hospital identity because including hospital identity could absorb the performance differences the project is intended to measure.

Peer-group results will require adequate sample volume.

---

## 11. Machine-Learning Objective

The primary data science task is retrospective case-mix-adjusted LOS estimation.

The model will estimate the length of stay associated with observable discharge-level case complexity. Model outputs will support hospital and service-line benchmarking.

This is not an admission-time clinical prediction model because some SPARCS variables may only be finalized during or after discharge.

Features that directly encode the target or downstream resource use—including LOS-derived variables, charges, estimated costs, and other post-outcome information—will be excluded from the primary expected-LOS model. Discharge disposition and hospital identity will be evaluated only through documented sensitivity analyses when their inclusion could absorb the operational differences being measured.

### Candidate approaches

The project will compare:

1. Statewide median LOS
2. APR-DRG median LOS
3. APR-DRG × severity median LOS
4. Regularized regression
5. Count, Gamma, or Tweedie regression where distributionally appropriate
6. Random-forest regression
7. Gradient-boosted regression
8. Optional quantile regression for P50 and P90 estimates

Gradient boosting is a candidate—not a predetermined winner.

### Model-selection criteria

- Mean absolute error
- Median absolute error
- Root mean squared error
- Calibration
- Aggregate actual-to-expected calibration
- Performance across hospitals and major subgroups
- Stability across years
- Interpretability
- Runtime and maintainability
- Improvement over strong peer-group baselines

The final model will not be selected using one accuracy metric alone.

---

## 12. Validation Strategy

If compatible multi-year data are available:

- Train on older years
- Validate on an intermediate period
- Test on the newest year

If only one year is used:

- Apply an appropriate cross-validation strategy
- Test generalization across hospitals or data partitions
- Clearly state that future-year stability has not been demonstrated

The final split design will be selected after the data audit.

Evaluation will include performance by:

- Hospital
- Region
- APR-DRG
- Severity level
- Age group
- Payer
- Admission type

---

## 13. Privacy and Reporting Standards

Although the source data are publicly released and de-identified, the dashboard will apply conservative reporting controls.

Planned controls:

- Suppress or mask displayed groups with fewer than 11 discharges
- Prevent suppressed values from being reconstructed through totals where practical
- Flag statistically unstable low-volume comparisons
- Avoid patient-level dashboard views
- Avoid exporting unnecessarily granular records
- Document the suppression method in the metric catalog

The threshold of 11 is a conservative project reporting standard. Its relationship to the specific SPARCS public-use terms will be verified during the data audit rather than represented as a universal SPARCS requirement.

---

## 14. Technical Architecture

### Desktop version

- Python data audit and exploratory analysis
- Reproducible preprocessing
- Star-schema semantic model
- Explicit DAX measures
- Power BI executive and operational dashboards
- PBIP source-control format

### Fabric version

- Bronze raw-data layer
- Silver validated discharge-level layer
- Gold analytical fact, dimension, benchmark, and prediction tables
- Fabric pipeline orchestration
- Python-based training and batch scoring
- Versioned model outputs
- Direct Lake semantic model where technically appropriate
- Development, testing, and production deployment design

Python will train and score the models. Power BI will consume, aggregate, and explain the results.

---

## 15. Dashboard Deliverables

The planned report will contain:

1. Executive Overview
2. Demand and Utilization
3. Operational Efficiency
4. Financial Indicators
5. Outcomes and Patient Mix
6. Facility Drill-Through
7. Model Performance and Methodology

The final number of pages may change after data profiling and user-story prioritization.

---

## 16. Success Criteria

### Business success

- A user can identify major operational opportunities within two minutes.
- Each KPI has a documented definition and intended decision.
- Raw performance is separated from case-mix-adjusted performance.
- Low-volume results are not presented as reliable findings.

### Analytical success

- Candidate models are compared using identical validation data.
- The selected model improves meaningfully over strong peer baselines.
- Aggregate predictions are reasonably calibrated.
- Subgroup errors and model limitations are reported.
- Findings are presented as associations and benchmarks—not causal effects.

### Technical success

- Transformations are reproducible.
- Major dashboard measures reconcile to independent Python calculations.
- The semantic model follows a documented star schema.
- The report remains usable at multi-year scale.
- Model version and scoring date are traceable.
- Fabric adds measurable scalability or maintainability rather than unnecessary complexity.

### Portfolio success

A recruiter should be able to understand:

1. The operational problem
2. The analytical approach
3. The model-selection process
4. The data architecture
5. The dashboard’s major findings
6. The limitations of the conclusions

---

## 17. Known Limitations

- Public data may omit important clinical and hospital structural variables.
- De-identification may reduce geographic or patient-level detail.
- Patients cannot be followed across encounters.
- Estimated costs may not represent audited hospital expenses.
- Charges do not represent reimbursement or revenue.
- APR-DRG and severity information may not be available at admission.
- Observational benchmarking cannot establish causality.
- Results may not generalize beyond New York hospitals or the selected years.
- Hospital comparisons may retain unmeasured case-mix differences.
- Fabric implementation will depend on available licensing and capacity.

---

## 18. Final Project Statement

> This project builds an end-to-end hospital operations analytics solution that combines Python, machine learning, Microsoft Fabric, semantic modeling, and Power BI to identify excess inpatient resource utilization after accounting for observable case complexity.