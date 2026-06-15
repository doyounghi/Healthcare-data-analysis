# Diabetes Peer Support A/B Testing

A synthetic healthcare analytics and experimentation portfolio project built to practice Python, randomized A/B testing, intent-to-treat analysis, randomization balance checks, funnel analysis, subgroup exploration, adjusted sensitivity analysis, and business recommendation writing.

This project uses fully synthetic healthcare-style data generated for portfolio and learning purposes. It does **not** contain real patient data, PHI, claims data, employer data, or production healthcare records. Results should be interpreted as an experimentation workflow demonstration, not real-world clinical or financial evidence.

## Executive Summary

| Area | Summary |
| --- | --- |
| Problem | Evaluate whether Diabetes Peer Support improves diabetes testing compliance compared with Standard Outreach |
| Methods | Synthetic data generation, randomization balance checks, intent-to-treat A/B testing, funnel analysis, SDOH segment analysis, and adjusted sensitivity analysis |
| Primary Result | Diabetes Peer Support increased binary compliance from 37.6% to 42.3%, a 4.7 percentage point absolute lift |
| Sensitivity Result | Adjusted OLS estimated a positive 2.7 percentage point lift after controlling for observed baseline characteristics |
| Business Recommendation | Use targeted expansion rather than immediate full-population rollout, while improving enrollment and attendance conversion |
| Caveat | This is a synthetic workflow project, not real-world healthcare evidence |

Final primary A/B test result: Diabetes Peer Support achieved a 4.7 percentage point absolute lift, 12.6% relative lift, two-proportion z-test p-value of 0.0023, and 95% confidence interval of 1.7 to 7.8 percentage points for binary diabetes testing compliance.

## Project Overview

This project analyzes a synthetic member-level healthcare outreach experiment with 4,000 targetable diabetic members. Each row represents one member and includes simulated demographic, plan, health risk, engagement, health literacy, SDOH barrier, PCP attribution, peer-support funnel, and diabetes testing outcome fields.

The project includes three main analytical tracks:

1. **Randomized A/B Testing**
   Estimate whether assignment to Diabetes Peer Support improved diabetes testing compliance compared with Standard Outreach.

2. **Operational Funnel Analysis**
   Review how members moved from assignment to invitation, enrollment, attendance, and session participation.

3. **Business Recommendation and Targeting Strategy**
   Use segment analysis and adjusted sensitivity checks to inform whether the program should be expanded, where bottlenecks exist, and what a future experiment should test.

The main focus of the project is not to prove real healthcare findings, but to demonstrate a complete experimentation workflow: synthetic data generation, data validation, balance checking, intent-to-treat analysis, statistical testing, confidence intervals, funnel diagnostics, subgroup exploration, robustness checks, and careful business interpretation.

## Start Here

Recommended notebooks for a quick review:

| Notebook | Purpose |
| --- | --- |
| `01_EDA_And_Randomization_Balance_Check.ipynb` | Validate the synthetic dataset, randomization balance, missingness, and outcome logic |
| `02_ab_test_primary_outcome.ipynb` | Review the main intent-to-treat A/B testing result |
| `03_Peer_Support_Funnel_Analysis.ipynb` | Understand program enrollment and attendance drop-off |
| `04_SDOH_Segment_Analysis.ipynb` | Explore SDOH and engagement subgroup patterns |
| `05_adjusted_sensitivity_analysis.ipynb` | Check whether the A/B result remains stable after baseline adjustment |
| `06_Business_Recommendation_Summary.ipynb` | Review the final business recommendation and next experiment proposal |

## Reproducibility: How to Run This Project

To reproduce the project workflow:

1. Clone the repository.

```bash
git clone https://github.com/doyounghi/synthetic-data-analysis.git
cd synthetic-data-analysis/02_diabetes_peer_support_ab_testing
```

2. Create and activate a virtual environment.

```bash
python -m venv .venv
```

On Windows:

```bash
.venv\Scripts\activate
```

On Mac/Linux:

```bash
source .venv/bin/activate
```

3. Install required packages.

```bash
pip install -r requirements.txt
```

4. Generate the synthetic dataset.

```bash
python src/generate_diabetes_peer_support_data.py
```

5. Launch Jupyter.

```bash
jupyter notebook
```

6. Run the notebooks in order from `01` to `06`.

Notebook outputs should remain broadly consistent because the synthetic data generator uses a fixed random seed, though minor differences may occur across package versions.

Generated data files are stored under:

```text
data/raw/
```

### Synthetic Data Generation

The data generation script creates the synthetic member-level dataset used throughout the project.

The goal was to build a realistic healthcare outreach dataset that includes member demographics, baseline health and engagement characteristics, health literacy, SDOH barriers, peer-support participation behavior, and diabetes testing outcomes.

Main work completed:

- Defined the target diabetic member population.
- Simulated member demographics, plan type, health risk, baseline engagement, health literacy, and SDOH barriers.
- Randomly assigned members into Standard Outreach and Diabetes Peer Support groups.
- Created a selective peer-support funnel including invitation, enrollment, attendance, and session count.
- Generated diabetes testing outcomes including A1c completion, kidney screening completion, eye exam completion, compliance rate, and binary compliance flag.
- Added intentional structured missingness to reflect common healthcare data quality issues.
- Ran validation checks for dataset shape, missingness, age realism, experiment group distribution, funnel integrity, and diabetes testing outcome logic.

Output file:

```text
data/raw/mock_diabetes_peer_support_ab_test.csv
```

Key design note:

Random assignment supports an intent-to-treat analysis, where members are compared based on assigned experiment group rather than later participation behavior. Enrollment, attendance, and session count occur after assignment and are intentionally selective, so they should be treated as downstream funnel variables rather than randomized baseline characteristics.

### Notebook 1: EDA and Randomization Balance Check

This notebook validates the synthetic A/B testing dataset before formal treatment-effect analysis.

The analysis checks the dataset structure, unit of analysis, missing values, experiment group distribution, age and plan-type realism, baseline numeric and categorical balance, SDOH balance, funnel integrity, and diabetes testing outcome logic.

Key findings:

- The dataset contains 4,000 targetable diabetic members.
- Each row represents one member in the outreach experiment.
- Treatment and control groups are reasonably balanced after random assignment.
- All observed baseline standardized mean differences are below the common 0.10 imbalance threshold.
- Missingness exists in baseline engagement and health literacy, but missingness is not strongly imbalanced by experiment group.
- SDOH-related variables appear reasonably balanced between experiment groups.
- The peer-support funnel is structurally valid, with control members not invited and no impossible funnel-stage skips.
- Diabetes testing outcome variables are internally consistent.
- Outcome differences are included only as an exploratory preview and should not be interpreted as final treatment effects.

This notebook does not estimate the final treatment effect. It prepares the dataset for formal A/B testing by validating randomization balance, missingness patterns, funnel logic, and outcome consistency.

### Notebook 2: A/B Test Primary Outcome Analysis

This notebook estimates the primary A/B testing result for the Diabetes Peer Support outreach experiment.

The analysis compares members assigned to Diabetes Peer Support against members assigned to Standard Outreach using an intent-to-treat framework. Members are analyzed based on randomized assignment, regardless of whether they enrolled in or attended the peer-support program.

Key findings:

- Standard Outreach binary compliance rate: 37.6%.
- Diabetes Peer Support binary compliance rate: 42.3%.
- Absolute lift: 4.7 percentage points.
- Relative lift: 12.6%.
- Two-proportion z-test p-value: 0.0023.
- 95% confidence interval for binary absolute lift: 1.7 to 7.8 percentage points.
- Average diabetes testing compliance rate improved from 71.3% to 74.5%.
- Individual diabetes test completion differences were reviewed as exploratory secondary outcomes.

This notebook is the primary randomized treatment-effect analysis. It protects the main comparison from participation-based selection bias by avoiding attendee-only causal claims.

### Notebook 3: Peer Support Funnel Analysis

This notebook analyzes the operational funnel for the Diabetes Peer Support intervention.

The analysis evaluates how members assigned to Diabetes Peer Support moved from assignment to invitation, enrollment, attendance, and session participation.

Key findings:

- The peer-support funnel logic was valid, with no detected structural violations.
- Members assigned to Diabetes Peer Support moved through the expected funnel stages.
- Funnel counts were: 2,078 assigned, 1,758 invited, 765 enrolled, and 280 attended at least one session.
- The largest member-count drop-off occurred between invitation and enrollment.
- The highest stage-to-stage drop-off rate occurred between enrollment and attendance.
- Members with higher session attendance showed higher diabetes testing compliance patterns than members with no sessions.
- Baseline characteristics also varied across attendance groups, suggesting attendance may reflect member selection as well as program engagement.

Attendance-based comparisons are operational and exploratory, not randomized causal evidence. The main A/B testing result remains the intent-to-treat comparison from Notebook 2.

### Notebook 4: SDOH Segment Analysis

This notebook explores whether observed Diabetes Peer Support outcomes differ across SDOH and baseline engagement segments.

The analysis compares treatment and control outcomes within SDOH risk groups, specific SDOH barrier groups, and baseline engagement groups. Segment-level results are treated as exploratory and hypothesis-generating.

Key findings:

- Diabetes Peer Support showed positive observed lift across low, medium, and high SDOH risk groups.
- Observed binary compliance lift by SDOH risk group was 5.4 percentage points for Low SDOH Risk, 4.0 percentage points for Medium SDOH Risk, and 4.8 percentage points for High SDOH Risk.
- Among specific SDOH barriers, members with financial barriers showed one of the stronger observed binary compliance lifts.
- Baseline engagement segments showed different observed response patterns.
- Members with higher baseline engagement appeared more responsive to the peer-support intervention in observed subgroup comparisons.
- Segment sample sizes were reviewed to reduce the risk of overinterpreting small subgroups.

These subgroup findings may help guide future targeting and program design, but they should not replace the overall intent-to-treat result from Notebook 2. Because multiple segments were reviewed, these results should be interpreted as exploratory subgroup evidence rather than confirmed causal differences.

### Notebook 5: Adjusted Sensitivity Analysis

This notebook evaluates whether the Diabetes Peer Support result remains stable after adjusting for observed baseline member characteristics.

The analysis compares unadjusted and adjusted estimates to assess whether the main A/B testing result is sensitive to baseline differences in demographics, health risk, engagement, health literacy, prior testing behavior, PCP attribution, and SDOH risk.

Key findings:

- The adjusted OLS treatment estimate remained positive after controlling for observed baseline characteristics.
- The estimated average compliance-rate lift changed from approximately 3.2 percentage points unadjusted to approximately 2.7 percentage points adjusted.
- The adjusted OLS estimate remained statistically significant, with a 95% confidence interval of approximately 1.2 to 4.2 percentage points.
- The adjusted logistic regression model also showed a positive treatment association for the binary compliance outcome.
- The adjusted odds ratio was approximately 1.20, meaning treatment-assigned members had about 20% higher odds of binary compliance after adjustment for observed baseline characteristics.
- Baseline engagement, health literacy, and PCP attribution were positively associated with compliance.
- SDOH risk was negatively associated with compliance.
- The adjusted results were directionally consistent with the unadjusted intent-to-treat findings from Notebook 2.

This notebook is a sensitivity analysis, not a replacement for the primary randomized result. Median imputation is used as a simple robustness strategy, not as a claim that it is the best possible missing-data method.

### Notebook 6: Business Recommendation Summary

This notebook synthesizes the statistical, causal, operational, and segment-level findings from the Diabetes Peer Support A/B testing project.

The goal is to translate the analysis results into a practical business recommendation for healthcare leadership, including whether the program should be expanded, where operational improvements are needed, and how a future experiment should be designed.

Key findings and recommendations:

- Diabetes Peer Support showed a positive intent-to-treat result in the synthetic randomized experiment.
- The program should be considered for targeted expansion rather than immediate full-population rollout.
- Enrollment and onboarding should be improved before scaling because the peer-support funnel showed major drop-off between invitation and enrollment.
- Future expansion should prioritize members with incomplete prior diabetes testing compliance, moderate-to-high SDOH risk, and barriers that may be addressable through peer support, reminders, scheduling flexibility, or care-navigation support.
- A follow-up randomized experiment should test whether enhanced enrollment support improves down-funnel participation and diabetes testing compliance.
- A strong next-phase design would compare standard peer-support outreach against peer-support outreach with digital session options, automated text reminders, or care-navigation follow-up.

Notebook 6 is a business-facing summary notebook. It does not replace the primary statistical analysis from Notebook 2 or the adjusted sensitivity analysis from Notebook 5. The main business conclusion is targeted expansion with continued measurement, not immediate full-population rollout.
