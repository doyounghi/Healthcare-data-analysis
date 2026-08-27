# Physical Data Model — Hospital Operations & Cost Efficiency

## Purpose

This document describes the reproducible physical implementation of the approved SPARCS analytical star schema.

## Analytical Grain

`FactDischarge` contains one row per released inpatient discharge.

- Raw source rows: 2,125,754
- Clean staging rows: 2,125,754
- FactDischarge rows: 2,125,754

## Transformation Standards

| standard_id | decision | rationale |
| --- | --- | --- |
| SOURCE_GRAIN_PRESERVED | Every released source row is retained in FactDischarge. | The audited grain is one released inpatient discharge. |
| SNAPSHOT_SOURCE_ROW_KEY | FactDischarge persists a unique source-row ordinal scoped to the audited snapshot. | The key supports reproducible downstream joins without implying patient identity or longitudinal discharge linkage. |
| NO_DUPLICATE_REMOVAL | Repeated released-value patterns are not removed. | No durable public discharge identifier exists to prove that repeated rows are erroneous duplicates. |
| TEXT_NORMALIZATION | Text values are trimmed and blank strings become null. | This prevents whitespace from creating artificial dimension members. |
| APPROVED_MAPPINGS_ONLY | Only category mappings approved in Notebook 02 are applied. | The physical build must not introduce undocumented business grouping logic. |
| LOS_TOP_CODE | Released 120+ LOS values are represented as the observable lower bound of 120 days and flagged. | The exact stay duration is unavailable for top-coded rows. |
| FINANCIAL_VALIDITY | Charges and estimated costs are retained only when numeric and greater than zero. | This implements the Notebook 02 financial valid-record rules. |
| DETERMINISTIC_KEYS | Dimension surrogate keys are assigned deterministically from sorted natural-key values. | The same source snapshot should generate the same keys across clean reruns. |
| UNKNOWN_KEY_ZERO | Dimension key 0 represents Unknown / Not Available. | Missing or unresolved dimension values must not remove fact rows. |
| NO_FACT_IDENTIFIER | No durable patient or discharge identifier is invented. | The public source does not support longitudinal linkage. |
| BENCHMARK_COLUMNS_DEFERRED | Approved peer-benchmark fact columns are created as typed null placeholders. | Notebook 05 will calculate benchmark values without changing the approved fact-table schema. |
| PARQUET_EXPORT | Physical model tables are exported as compressed Parquet. | Columnar storage is appropriate for the 2.1-million-row fact table and future Power BI/Fabric workflows. |

## Dimension Row Counts

| table_name | row_count |
| --- | --- |
| DimHospital | 208 |
| DimDate | 2 |
| DimService | 483 |
| DimCaseMix | 17 |
| DimDiagnosis | 483 |
| DimProcedure | 321 |
| DimPatientSegment | 203 |
| DimGeography | 51 |
| DimPayer | 10 |
| DimAdmissionContext | 201 |

## Unknown-Member Usage

| dimension_table | fact_foreign_key | unknown_fact_row_n | unknown_fact_row_pct |
| --- | --- | --- | --- |
| DimHospital | hospital_key | 5333 | 0.2509 |
| DimDate | date_key | 0 | 0.0 |
| DimService | service_key | 0 | 0.0 |
| DimCaseMix | case_mix_key | 474 | 0.0223 |
| DimDiagnosis | diagnosis_key | 0 | 0.0 |
| DimProcedure | procedure_key | 611024 | 28.7439 |
| DimPatientSegment | patient_segment_key | 0 | 0.0 |
| DimGeography | geography_key | 41883 | 1.9703 |
| DimPayer | payer_key | 0 | 0.0 |
| DimAdmissionContext | admission_context_key | 0 | 0.0 |

## Physical Validation Results

| validation_test | passed | details |
| --- | --- | --- |
| Source snapshot matches Notebook 01 | True |  |
| Approved category mappings cover source values | True |  |
| Staging row count reconciles to source | True | 2125754 vs 2125754 |
| Fact row count reconciles to source | True | 2125754 vs 2125754 |
| Natural-key attributes are consistent | True |  |
| APR severity code/description domain is valid | True |  |
| Dimension primary keys are unique | True |  |
| Each dimension contains exactly one key 0 member | True |  |
| Fact foreign keys contain no null values | True | 0 |
| Fact foreign keys contain no orphan values | True |  |
| Physical columns match Notebook 03 | True |  |
| Physical datatypes match Notebook 03 | True |  |
| Source row keys, LOS flags, and financial flags are internally consistent | True | 0 |
| Peer benchmark columns remain unpopulated | True | 0 |

## Power BI-Ready Parquet Tables

| table_name | row_count | file_size_mb | output_path |
| --- | --- | --- | --- |
| FactDischarge | 2125754 | 30.11 | outputs/physical_model/tables/FactDischarge.parquet |
| DimHospital | 208 | 0.01 | outputs/physical_model/tables/DimHospital.parquet |
| DimDate | 2 | 0.0 | outputs/physical_model/tables/DimDate.parquet |
| DimService | 483 | 0.01 | outputs/physical_model/tables/DimService.parquet |
| DimCaseMix | 17 | 0.0 | outputs/physical_model/tables/DimCaseMix.parquet |
| DimDiagnosis | 483 | 0.01 | outputs/physical_model/tables/DimDiagnosis.parquet |
| DimProcedure | 321 | 0.01 | outputs/physical_model/tables/DimProcedure.parquet |
| DimPatientSegment | 203 | 0.0 | outputs/physical_model/tables/DimPatientSegment.parquet |
| DimGeography | 51 | 0.0 | outputs/physical_model/tables/DimGeography.parquet |
| DimPayer | 10 | 0.0 | outputs/physical_model/tables/DimPayer.parquet |
| DimAdmissionContext | 201 | 0.0 | outputs/physical_model/tables/DimAdmissionContext.parquet |

## Deferred Benchmark Columns

`FactDischarge` contains the approved peer-benchmark columns as typed null placeholders.

Notebook 05 will calculate leave-one-facility-out LOS and estimated-cost peer expectations.