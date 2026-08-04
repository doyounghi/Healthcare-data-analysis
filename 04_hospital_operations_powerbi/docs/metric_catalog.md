# Metric Catalog — Hospital Operations & Cost Efficiency

## Purpose

This document defines the approved metrics, denominator rules, benchmark logic,
and interpretation limitations for the initial 2023 SPARCS analysis.

## Analytical Grain

The source grain is one inpatient discharge. Discharge counts must not be
interpreted as unique-patient counts.

## Aggregation Standards

- Ratios use ratio-of-sums.
- LOS, charges, and estimated costs require robust statistics.
- LOS values recorded as 120+ are treated as observable lower bounds.
- Charges are not reimbursement or revenue.
- Estimated costs are not audited hospital expenses.
- Visible cells are subject to the documented suppression policy.

## Approved Metrics

| metric_name | metric_group | business_definition | calculation_rule | important_caveat |
| --- | --- | --- | --- | --- |
| Discharges | Volume | Number of inpatient discharge records in the selected context. | COUNT_ROWS | Discharge count is not a unique-patient count. |
| Facilities | Volume | Number of distinct nonmissing permanent facility identifiers. | DISTINCT_COUNT(Permanent Facility Id) | Facility identifiers may be suppressed for some records. |
| Total LOS Days — Lower Bound | Length of Stay | Total observed inpatient days after representing 120+ as 120. | SUM(LOS numeric lower bound) | This understates exact inpatient days because 120+ values are right-censored. |
| Average LOS — Lower Bound | Length of Stay | Average numeric LOS after representing 120+ as 120. | SUM(LOS numeric lower bound) / COUNT(valid LOS records) | The result is a lower-bound mean and is sensitive to skewness. |
| Median LOS | Length of Stay | Median LOS after representing 120+ as its observable lower bound. | MEDIAN(LOS numeric lower bound) | Median LOS is robust but does not replace total-days analysis. |
| P95 LOS | Length of Stay | Ninety-fifth percentile of the observable LOS lower bound. | PERCENTILE_CONT(LOS numeric lower bound, 0.95) | The percentile may be affected when top-coded cases are included. |
| Top-Coded LOS Discharges | Length of Stay | Number of discharges whose released LOS is 120 days or more. | COUNT(Length of Stay classified as 120+) | The exact stay duration is unavailable. |
| Top-Coded LOS Rate | Length of Stay | Percentage of valid LOS records that are top-coded. | Top-coded LOS discharges / discharges with valid LOS | This measures censoring prevalence, not clinical performance. |
| Total Charges | Financial | Total valid billed hospital charges. | SUM(valid Total Charges) | Charges are not reimbursement, revenue, or audited expense. |
| Average Charge per Discharge | Financial | Average billed charge among discharges with valid charges. | SUM(valid Total Charges) / COUNT(valid charge records) | Highly sensitive to right-skewed observations. |
| Median Charge per Discharge | Financial | Median valid billed charge per discharge. | MEDIAN(valid Total Charges) | Charges do not measure hospital profitability. |
| Total Estimated Costs | Financial | Total released analytical cost estimate. | SUM(valid Total Costs) | Total Costs does not represent audited hospital expense. |
| Average Estimated Cost per Discharge | Financial | Average estimated cost among records with valid cost values. | SUM(valid Total Costs) / COUNT(valid cost records) | Case-mix-adjusted cost performance is not established here. |
| Median Estimated Cost per Discharge | Financial | Median valid estimated cost per discharge. | MEDIAN(valid Total Costs) | This is an analytical estimate—not audited expense. |
| Charge-to-Cost Ratio | Financial | Aggregate charges divided by aggregate estimated costs. | SUM(Total Charges for paired-valid records) / SUM(Total Costs for the same paired-valid records) | Do not calculate the mean of discharge-level charge-to-cost ratios. |
| ED-Origin Discharge Rate | Admission Context | Percentage of eligible inpatient discharges associated with the emergency department indicator. | ED-indicator discharges / discharges with known ED indicator | This should not automatically be described as avoidable ED use. |
| Emergency Admission Rate | Admission Context | Percentage of eligible discharges classified as emergency admissions. | Emergency admissions / discharges with known admission type | Admission mix reflects patient population and service structure. |
| Major or Extreme Severity Rate | Case Mix | Percentage of discharges classified as major or extreme APR severity. | Major-or-extreme severity discharges / discharges with known severity | This is a case-mix descriptor—not an outcome metric. |
| Major or Extreme Mortality-Risk Rate | Case Mix | Percentage of discharges classified as major or extreme APR risk of mortality. | Major-or-extreme risk discharges / discharges with known APR mortality risk | APR risk of mortality is not observed mortality. |
| Peer-Expected LOS Days | Benchmarking | Expected total LOS based on statewide peer-group mean LOS, excluding the benchmarked facility. | SUM(discharge-level leave-one-facility-out peer mean LOS) | This is a descriptive peer baseline—not a predicted clinical LOS. |
| LOS Actual-to-Peer-Expected Ratio | Benchmarking | Observed LOS days divided by peer-expected LOS days. | SUM(observed LOS lower bound) / SUM(peer-expected LOS) | Unmeasured hospital structure and case-mix differences remain. |
| Excess LOS Days — Lower Bound | Benchmarking | Observed LOS days minus peer-expected LOS days. | SUM(observed LOS lower bound) - SUM(peer-expected LOS) | Positive excess days identify variation—not preventable days. |

## Benchmark Design

| benchmark_name | primary_peer_keys | minimum_peer_n | intended_use | status |
| --- | --- | --- | --- | --- |
| Primary Peer Mean LOS | APR DRG Code\|APR Severity of Illness Code | 30 | Descriptive case-mix-contextualized LOS benchmark | APPROVED_BASELINE |
| Peer Median LOS Context | APR DRG Code\|APR Severity of Illness Code | 30 | Robust descriptive comparison alongside peer mean | APPROVED_CONTEXT |
| Model-Predicted Expected LOS | To be defined during modeling |  | Later case-mix-adjusted predictive benchmarking | DEFERRED_TO_MODELING |

## Interpretation Limits

The peer benchmark controls only for the fields explicitly included in its peer
definition. It does not eliminate all case-mix or hospital-structure differences.

Positive excess LOS days identify observed variation relative to the benchmark.
They do not prove inefficiency, preventability, poor quality, or causal hospital
performance.

The initial peer benchmark is distinct from the expected-LOS model that will be
developed and validated later.
