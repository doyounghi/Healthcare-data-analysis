# Expected LOS Model Development — Hospital Operations & Cost Efficiency

## Purpose

This document summarizes retrospective case-mix-adjusted LOS model development and hospital-held-out validation.

## Source Snapshot

- Source snapshot ID: `d69e4b9e47fd2992`
- Eligible modeling rows: 2,120,421
- Development rows: 250,000
- Development hospitals: 207
- Predictions can be joined by the complete, unique `source_record_key` scoped to this snapshot.

## Runtime Versions

| component | version |
| --- | --- |
| python | 3.14.3 |
| pandas | 3.0.5 |
| numpy | 2.5.1 |
| duckdb | 1.5.5 |
| scikit-learn | 1.9.0 |
| xgboost | 3.4.1 |

## Primary Validation Design

The notebook uses 3-fold hospital-held-out cross-validation.

Hospital identity is used only to define held-out groups and is not a primary predictive feature.

## Primary Features

- `apr_drg_code`
- `apr_mdc_code`
- `medical_surgical_classification`
- `apr_severity_code`
- `apr_mortality_risk`
- `ccsr_diagnosis_code`
- `age_group`
- `gender`
- `payer_group`
- `admission_type_group`
- `ed_indicator_group`

## Candidate Model Comparison

| model_name | candidate_type | mae | median_absolute_error | rmse | actual_to_expected_ratio | calibration_error_abs | total_cv_seconds | mae_improvement_vs_strong_baseline_pct | multi_metric_rank_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| APR_DRG_SEVERITY_MEAN | Strong transparent mean baseline | 3.336726562485632 | 1.6340361445783134 | 7.061389849610222 | 0.9998128742917076 | 0.0001871257082923794 | 0.04953486666393776 | 0.0 | 3.25 |
| XGBOOST | Statistical / ML | 3.284979909256935 | 1.658697247505188 | 6.959015182708617 | 1.0010338523147468 | 0.0010338523147468415 | 14.506381000042893 | 1.5508209096447294 | 3.5 |
| APR_DRG_SEVERITY_MEDIAN | Transparent median baseline | 3.087932 | 1.0 | 7.296577965046354 | 1.2927996737368932 | 0.2927996737368932 | 0.04953486666393776 | 7.456246648520615 | 3.75 |
| RIDGE_REGRESSION | Statistical / ML | 3.424587325726013 | 1.7341761589050293 | 7.128632020678226 | 0.9998254627812458 | 0.00017453721875415606 | 5.939482799964026 | -2.633142440504053 | 4.0 |
| RANDOM_FOREST | Statistical / ML | 3.512403924490263 | 2.082931695888762 | 7.361639155710269 | 0.9999445972187504 | 5.540278124960274e-05 | 10.15140839992091 | -5.264961294094277 | 5.0 |
| APR_DRG_MEDIAN | Transparent baseline | 3.3319 | 1.0 | 7.79296965219293 | 1.4178644048843982 | 0.41786440488439824 | 0.04953486666393776 | 0.14464962577084498 | 5.25 |
| APR_DRG_MEAN | Transparent mean baseline | 3.6821330492535167 | 2.0960854092526686 | 7.488385773046536 | 0.9993505439329189 | 0.0006494560670811111 | 0.04953486666393776 | -10.35165693980572 | 6.5 |
| POISSON_REGRESSION | Statistical / ML | 3.886158309876442 | 2.4838063716888428 | 8.026966685864826 | 1.0007735058592289 | 0.0007735058592288624 | 7.762484799954109 | -16.466190354582757 | 7.75 |
| STATEWIDE_MEAN | Transparent mean baseline | 4.618605391767852 | 3.6787344977170315 | 8.752643722291962 | 0.9999996318622639 | 3.681377360731375e-07 | 0.04953486666393776 | -38.41725731122864 | 8.25 |
| STATEWIDE_MEDIAN | Transparent baseline | 3.923728 | 2.0 | 9.182673249114334 | 1.9273333333333333 | 0.9273333333333333 | 0.04953486666393776 | -17.592134881951264 | 9.25 |
| TWEEDIE_REGRESSION | Statistical / ML | 3.9952630318956377 | 2.5884785652160645 | 8.297544409196204 | 1.0403304711560488 | 0.04033047115604882 | 5.814861700171605 | -19.73600344762567 | 9.25 |

## Provisional Statistical / ML Shortlist

| shortlist_rank | model_name | mae | median_absolute_error | rmse | actual_to_expected_ratio | mae_improvement_vs_strong_baseline_pct |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | XGBOOST | 3.284979909256935 | 1.658697247505188 | 6.959015182708617 | 1.0010338523147468 | 1.5508209096447294 |
| 2 | RIDGE_REGRESSION | 3.424587325726013 | 1.7341761589050293 | 7.128632020678226 | 0.9998254627812458 | -2.633142440504053 |
| 3 | RANDOM_FOREST | 3.512403924490263 | 2.082931695888762 | 7.361639155710269 | 0.9999445972187504 | -5.264961294094277 |

## Provisional Candidate

`XGBOOST`

This is a development-stage shortlist result, not a final production-model version.

## Hospital / Disposition Sensitivity

| feature_set | n | mae | median_absolute_error | rmse | actual_to_expected_ratio | mae_change_vs_primary_pct |
| --- | --- | --- | --- | --- | --- | --- |
| Primary | 100000 | 3.2996920449890657 | 1.633836030960083 | 7.011061858143287 | 1.0003835064050304 | 0.0 |
| Primary + Hospital | 100000 | 3.2576297069939493 | 1.6305726766586304 | 6.906167304475919 | 1.0015879760663444 | -1.2747352607947924 |
| Primary + Disposition | 100000 | 3.1670583006831126 | 1.5181403160095215 | 6.849733088119735 | 1.0004318513416566 | -4.019579478859901 |
| Primary + Hospital + Disposition | 100000 | 3.1213249849272846 | 1.5059717893600464 | 6.740385969052896 | 1.001806104972853 | -5.405566871994933 |

This sensitivity uses random row-level folds and must not be interpreted as unseen-hospital generalization.

## Privacy-Safe Subgroup Reporting

Subgroup results with fewer than 11 discharges are omitted from the detailed export. Only aggregate suppressed-group counts are retained below.

| model_name | subgroup_dimension | suppressed_group_n |
| --- | --- | --- |
| APR_DRG_SEVERITY_MEAN | apr_drg_code | 11 |
| APR_DRG_SEVERITY_MEAN | hospital_key | 3 |
| XGBOOST | apr_drg_code | 11 |
| XGBOOST | hospital_key | 3 |

## LOS Top-Coding

The primary development population retains `120 +` LOS records as observable 120-day lower bounds. Separate diagnostics quantify their influence.

## Validation Results

| validation_test | passed | details |
| --- | --- | --- |
| Notebook 02 validation passed | True |  |
| Notebook 03 validation passed | True |  |
| Notebook 04 physical validation passed | True |  |
| Notebook 04 Parquet validation passed | True |  |
| Notebook 05 benchmark validation passed | True |  |
| Notebook 05 Parquet validation passed | True |  |
| Modeling source preserves fact row count | True | 2125754 vs 2125754 |
| Source record key is complete and unique | True | {'row_count': 2125754, 'nonnull_key_n': 2125754, 'distinct_key_n': 2125754} |
| Feature specification covers all primary and forbidden fields | True | 31 |
| Development validation passed | True |  |
| Hospital-held-out folds cover every development row | True | 3 folds |
| All candidate OOF predictions are complete and positive | True |  |
| All governed candidate families were evaluated | True | STATEWIDE_MEDIAN\|APR_DRG_MEDIAN\|APR_DRG_SEVERITY_MEDIAN\|STATEWIDE_MEAN\|APR_DRG_MEAN\|APR_DRG_SEVERITY_MEAN\|RIDGE_REGRESSION\|POISSON_REGRESSION\|TWEEDIE_REGRESSION\|RANDOM_FOREST\|XGBOOST |
| Provisional shortlist exists | True | XGBOOST\|RIDGE_REGRESSION\|RANDOM_FOREST |
| Exported subgroup diagnostics meet minimum reporting size | True | minimum n=11; rows=1118 |
| Low-volume subgroup diagnostics are summarized without group values | True | 28 |
| Top-code sensitivity produced | True | 6 |
| Hospital/disposition sensitivity produced | True | 4 |
| Prediction contract separates modeled from peer expected LOS | True |  |

## Limitations

- The current source contains one implemented year, so future-year stability is not demonstrated.
- The model is retrospective rather than an admission-time clinical prediction model.
- Unmeasured clinical and structural differences may remain.
- Model predictions support operational screening and do not establish causality or preventability.
- Descriptive peer expectations and model predictions remain separate analytical concepts.

## Next Step

Notebook 07 will make the final model-version decision, refit the approved approach, create versioned scoring outputs, and prepare `model_predicted_los_days` for Power BI.
