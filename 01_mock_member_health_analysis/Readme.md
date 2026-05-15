# Mock Member Health Analysis

Practice project for Python, data analysis, and introductory machine learning.

## Notebook 1 : Explornatory Data Analysis

This notebook performs initial exploratory analysis on a synthetic healthcare member dataset. Each row represents one health plan member with demographic, plan, SDOH, utilization, cost, PCP attribution, and AWV completion fields.

The analysis checks data structure, missing values, duplicate member IDs, categorical distributions, numeric ranges, and basic visualizations. It also compares cost, utilization, and AWV completion patterns across plan type, region, PCP attribution, chronic condition burden, engagement quartiles, and age groups.

Key findings:
- DSNP members showed higher average SDOH risk, ED visits, and monthly cost.
- Rural members showed higher average SDOH risk, lower engagement, and higher ED utilization.
- PCP-attributed members had higher AWV completion and lower average utilization.
- AWV completion increased strongly across engagement score quartiles.
- Non-AWV-compliant members had higher average monthly cost in this synthetic dataset.

These findings are descriptive and should not be interpreted causally.

### Notebook 2 : Feature Engineering

- Loaded the EDA-ready synthetic healthcare member dataset from the prior notebook.
- Created stakeholder-friendly analytical features including age group, engagement quartile, chronic burden group, SDOH risk quartile, prior AWV group, PCP attribution status, acute utilization flag, and high-cost member flag.
- Defined high-cost members as the top 25% of monthly cost, creating a potential future classification target.
- Validated engineered features by checking distributions and grouped summaries.
- Found that higher chronic burden, higher acute utilization, older age, and higher SDOH risk were associated with higher average monthly cost.
- Found that AWV completion was higher among members with stronger engagement and prior AWV history.
- Exported the analysis-ready dataset to `data/processed/member_analysis_ready.csv`.

These findings are descriptive and based on synthetic data. They should not be interpreted causally.
