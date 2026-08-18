# Peer Benchmark Methodology — Hospital Operations & Cost Efficiency

## Purpose

This document describes the implemented leave-one-facility-out descriptive peer benchmarks for length of stay and released estimated cost.

## Primary Peer Definition

The primary comparison group is `APR-DRG Code × APR Severity of Illness Code`.

All eligible records from the focal hospital are removed before calculating that hospital's peer expectation.

## Fallback Peer Definition

If fewer than 30 eligible comparison discharges remain at the primary level, the benchmark falls back to `APR-DRG Code`.

If fewer than 30 eligible comparison discharges remain after fallback, the expected value remains unavailable.

## Measure Eligibility

- LOS benchmarking uses records where `is_valid_los = 1`.
- Estimated-cost benchmarking uses records where `is_valid_cost = 1`.
- LOS and cost peer populations are calculated independently.

## LOS Interpretation

The LOS expectation uses `los_days_lower_bound`.

Records released as `120 +` contribute an observable lower bound of 120 days.

## Implementation Standards

| standard_id | decision | rationale |
| --- | --- | --- |
| LEAVE_ONE_FACILITY_OUT | All eligible records from the focal hospital are excluded from its peer expectation. | The facility being evaluated must not influence its own expected value. |
| PRIMARY_PEER_GROUP | Primary peer groups use APR-DRG Code and APR Severity of Illness Code. | This is the governed primary peer definition approved in Notebook 02. |
| FALLBACK_PEER_GROUP | APR-DRG Code alone is used when the primary comparison group is insufficient. | This preserves benchmark availability while retaining clinical grouping. |
| MINIMUM_COMPARISON_N | At least 30 eligible comparison discharges must remain after excluding the focal hospital. | Low-volume peer expectations are not treated as sufficiently stable for the governed benchmark. |
| LOS_ELIGIBILITY | LOS peer calculations use records where is_valid_los = 1. | The benchmark uses the governed LOS valid-record population. |
| COST_ELIGIBILITY | Estimated-cost peer calculations use records where is_valid_cost = 1. | The benchmark uses the governed estimated-cost valid-record population. |
| FOCAL_RECORD_ELIGIBILITY | A focal record receives a benchmark only when its corresponding measure is valid. | Expected values are not attached to records whose actual measure failed the governed validity rule. |
| UNKNOWN_HOSPITAL | Hospital key 0 does not receive a peer benchmark. | Leave-one-facility-out logic requires a resolved focal hospital. |
| SERVICE_GRAIN_INDEPENDENCE | DimService may use APR-DRG × APR-MDC as its physical natural key, but peer grouping uses APR-DRG as governed by Notebook 02. | Dimension grain and analytical benchmark grain serve different purposes. |
| LOW_VOLUME_STORAGE | When no benchmark qualifies, expectation remains null and benchmark level is labeled Unavailable. | Missing expected values must be distinguishable from valid zero values. |
| DESCRIPTIVE_NOT_PREDICTIVE | Peer expectations remain separate from future model-predicted LOS. | Descriptive benchmark values and machine-learning predictions have different interpretations. |

## Benchmark Coverage

| benchmark_metric | benchmark_level | benchmark_status | row_n | row_pct |
| --- | --- | --- | --- | --- |
| Estimated Cost | APR-DRG | Fallback benchmark available | 2570 | 0.1209 |
| Estimated Cost | APR-DRG × Severity | Primary benchmark available | 2117792 | 99.6255 |
| Estimated Cost | Unavailable | Insufficient comparison volume | 59 | 0.0028 |
| Estimated Cost | Unavailable | Unresolved hospital | 5333 | 0.2509 |
| LOS | APR-DRG | Fallback benchmark available | 2570 | 0.1209 |
| LOS | APR-DRG × Severity | Primary benchmark available | 2117792 | 99.6255 |
| LOS | Unavailable | Insufficient comparison volume | 59 | 0.0028 |
| LOS | Unavailable | Unresolved hospital | 5333 | 0.2509 |

## Peer Comparison Volumes

| benchmark_metric | benchmark_level | benchmarked_row_n | min_peer_n | median_peer_n | p95_peer_n | max_peer_n |
| --- | --- | --- | --- | --- | --- | --- |
| Estimated Cost | APR-DRG | 2570 | 30 | 375.0 | 4731.399999999998 | 164903 |
| Estimated Cost | APR-DRG × Severity | 2117792 | 30 | 5162.0 | 118935.0 | 122766 |
| LOS | APR-DRG | 2570 | 30 | 375.0 | 4731.399999999998 | 164903 |
| LOS | APR-DRG × Severity | 2117792 | 30 | 5162.0 | 118935.0 | 122766 |

## Validation Results

| validation_test | passed | details |
| --- | --- | --- |
| Notebook 02 validation passed | True |  |
| Notebook 03 validation passed | True |  |
| Notebook 04 physical validation passed | True |  |
| Input benchmark columns were empty | True |  |
| Benchmark context preserves fact row count | True | 2125754 vs 2125754 |
| Benchmarked fact preserves fact row count | True | 2125754 vs 2125754 |
| Non-benchmark fact columns are unchanged | True | 0 input-only; 0 output-only |
| Benchmark selection logic has no violations | True | 0 |
| Direct mathematical reconciliation passes | True | 12 sample comparisons |
| Fact schema remains unchanged | True |  |
| At least one LOS benchmark is available | True | 2120362 |
| At least one estimated-cost benchmark is available | True | 2120362 |

## Important Limitations

- Peer benchmarks are descriptive operational screening tools.
- They are not machine-learning predictions.
- They are not formal clinical risk-adjustment models.
- They do not establish causality, preventability, or hospital quality.
- APR-DRG and severity do not capture all clinical or structural differences among facilities.
- Estimated costs are released analytical estimates rather than audited hospital operating expenses.

## Downstream Use

Power BI will use the benchmarked fact table for actual-to-peer-expected ratios, excess LOS days, estimated-cost comparisons, and related operational investigation measures.

Future model-predicted LOS must remain separate from these descriptive peer expectations.
