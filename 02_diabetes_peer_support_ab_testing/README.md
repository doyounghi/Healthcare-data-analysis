### Notebook 01: EDA and Randomization Balance Check

Notebook 01 validates the synthetic Diabetes Peer Support A/B testing dataset before formal treatment-effect analysis.

The goal of this notebook is to confirm that the dataset is structurally sound, the randomized experiment groups are reasonably balanced, and the peer-support funnel logic is valid before moving into statistical testing.

Main work completed:

* Loaded the synthetic member-level outreach dataset
* Confirmed the unit of analysis is one targetable diabetic member
* Reviewed dataset shape, column structure, data types, and missing values
* Checked that all members belong to the intended diabetic outreach target population
* Verified the experiment group distribution between:

  * **Standard Outreach**
  * **Diabetes Peer Support**
* Reviewed age and plan-type realism
* Compared baseline numeric and binary characteristics between treatment and control groups
* Calculated standardized mean differences to evaluate baseline balance
* Checked categorical balance using dummy-variable standardized mean differences
* Reviewed missingness balance for baseline engagement and health literacy
* Highlighted SDOH-related balance results
* Created exploratory SDOH risk groups using quantile-based splitting
* Reviewed PCP attribution and prior diabetes testing compliance balance
* Visualized baseline balance using an SMD balance plot
* Validated peer-support funnel integrity
* Reviewed treatment-only funnel rates
* Confirmed diabetes testing outcome logic
* Checked the diabetes test difficulty hierarchy
* Previewed outcome differences without making final causal claims

Key findings:

* The dataset contains 4,000 targetable diabetic members.
* Each row represents one member in the outreach experiment.
* The treatment and control groups are reasonably balanced after random assignment.
* All observed baseline standardized mean differences are below the common 0.10 imbalance threshold.
* Categorical variables such as gender, region, and plan type are reasonably balanced after dummy-variable conversion.
* Missingness exists in baseline engagement and health literacy, but missingness is not strongly imbalanced by experiment group.
* SDOH-related variables appear reasonably balanced between experiment groups.
* The peer-support funnel is structurally valid: control members are not invited, and members do not skip impossible funnel stages.
* Diabetes testing outcome variables are internally consistent.
* Outcome differences are shown only as an exploratory preview and should not be interpreted as final treatment effects.

Output notebook:

`notebooks/01_EDA_And_Randomization_Balance_Check.ipynb`

Key design note:

This notebook does not estimate the final treatment effect. It prepares the dataset for formal A/B testing by validating randomization balance, missingness patterns, funnel logic, and outcome consistency.

The next notebook should use an intent-to-treat framework to compare members based on randomized assignment, including absolute lift, relative lift, confidence intervals, p-values, and practical significance.
