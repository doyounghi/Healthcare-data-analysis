Project 2: Diabetes Peer Support A/B Testing

This project analyzes a synthetic healthcare outreach A/B test designed to evaluate whether a diabetes peer-support program can improve diabetes testing compliance compared with standard outreach.

The project follows a practical healthcare analytics workflow: generating realistic member-level data, validating randomization, checking baseline balance, reviewing funnel behavior, and preparing the dataset for formal treatment-effect analysis.

Day 1: Synthetic Data Generation

Day 1 focused on creating the synthetic member-level dataset used throughout the project.

The goal was to build a realistic healthcare outreach dataset that includes member demographics, baseline health and engagement characteristics, SDOH barriers, peer-support participation behavior, and diabetes testing outcomes.

Main work completed:

Defined the target diabetic member population
Simulated member demographics, plan type, health risk, baseline engagement, health literacy, and SDOH barriers
Randomly assigned members into two experiment groups:
Standard Outreach
Diabetes Peer Support
Created a selective peer-support funnel:
program invitation
program enrollment
attendance
number of sessions attended
Generated diabetes testing outcomes:
A1c test completion
kidney screening completion
eye exam completion
diabetes testing compliance rate
diabetes testing compliant flag
Added intentional structured missingness to reflect common healthcare data quality issues
Ran validation checks for dataset shape, missingness, age realism, experiment group distribution, funnel integrity, and diabetes testing outcome logic

Output file:

data/raw/mock_diabetes_peer_support_ab_test.csv

Key design note:

Random assignment supports an intent-to-treat analysis, where members are compared based on their assigned experiment group rather than their later participation behavior.

Enrollment, attendance, and session count occur after assignment and are intentionally selective. These variables should be treated as downstream funnel variables, not randomized baseline characteristics. Comparing attendees directly against non-attendees may introduce selection bias because participation can be influenced by engagement, health literacy, transportation barriers, and unobserved motivation.

Notebook 01: EDA and Randomization Balance Check

Notebook 01 validates the synthetic A/B testing dataset before formal treatment-effect analysis.

The goal of this notebook is to confirm that the dataset is structurally sound, the treatment and control groups are reasonably balanced, and the peer-support funnel logic is valid before moving into statistical testing.

Main work completed:

Loaded and inspected the synthetic member-level outreach dataset
Confirmed the unit of analysis is one targetable diabetic member
Reviewed dataset shape, column structure, data types, and missing values
Verified that all members belong to the intended diabetic outreach target population
Checked the experiment group distribution between:
Standard Outreach
Diabetes Peer Support
Reviewed age and plan-type realism
Compared baseline numeric and binary characteristics between treatment and control groups
Calculated standardized mean differences to evaluate baseline balance
Checked categorical balance using dummy-variable standardized mean differences
Reviewed missingness balance for baseline engagement and health literacy
Highlighted SDOH-related balance results
Created exploratory SDOH risk groups using quantile-based splitting
Reviewed PCP attribution and prior diabetes testing compliance balance
Visualized baseline balance using an SMD balance plot
Validated peer-support funnel integrity
Reviewed treatment-only funnel rates
Confirmed diabetes testing outcome logic
Checked the diabetes test difficulty hierarchy
Previewed outcome differences without making final treatment-effect claims

Key findings:

The dataset contains 4,000 targetable diabetic members.
Each row represents one member in the outreach experiment.
The treatment and control groups are reasonably balanced after random assignment.
All observed baseline standardized mean differences are below the common 0.10 imbalance threshold.
Categorical variables such as gender, region, and plan type are reasonably balanced after dummy-variable conversion.
Missingness exists in baseline engagement and health literacy, but missingness is not strongly imbalanced by experiment group.
SDOH-related variables appear reasonably balanced between experiment groups.
The peer-support funnel is structurally valid: control members are not invited, and members do not skip impossible funnel stages.
Diabetes testing outcome variables are internally consistent.
Outcome differences are included only as an exploratory preview and should not be interpreted as final treatment effects.

Output notebook:

notebooks/01_EDA_And_Randomization_Balance_Check.ipynb

Key design note:

This notebook does not estimate the final treatment effect. It prepares the dataset for formal A/B testing by validating randomization balance, missingness patterns, funnel logic, and outcome consistency.

The next notebook will use an intent-to-treat framework to compare members based on randomized assignment. That analysis should include absolute lift, relative lift, confidence intervals, p-values, and practical significance.