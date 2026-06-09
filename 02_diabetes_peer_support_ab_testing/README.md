## Project 2: Diabetes Peer Support A/B Testing

This project analyzes a synthetic healthcare outreach A/B test designed to evaluate whether a diabetes peer-support program can improve diabetes testing compliance compared with standard outreach.

The project follows a practical healthcare analytics workflow: generating realistic member-level data, validating randomization, checking baseline balance, reviewing funnel behavior, and preparing the dataset for formal treatment-effect analysis.

### Day 1: Synthetic Data Generation

Day 1 focused on creating the synthetic member-level dataset used throughout the project.

The goal was to build a realistic healthcare outreach dataset that includes member demographics, baseline health and engagement characteristics, SDOH barriers, peer-support participation behavior, and diabetes testing outcomes.

Main work completed:

* Defined the target diabetic member population
* Simulated member demographics, plan type, health risk, baseline engagement, health literacy, and SDOH barriers
* Randomly assigned members into two experiment groups:

  * **Standard Outreach**
  * **Diabetes Peer Support**
* Created a selective peer-support funnel:

  * program invitation
  * program enrollment
  * attendance
  * number of sessions attended
* Generated diabetes testing outcomes:

  * A1c test completion
  * kidney screening completion
  * eye exam completion
  * diabetes testing compliance rate
  * diabetes testing compliant flag
* Added intentional structured missingness to reflect common healthcare data quality issues
* Ran validation checks for dataset shape, missingness, age realism, experiment group distribution, funnel integrity, and diabetes testing outcome logic

Output file:

`data/raw/mock_diabetes_peer_support_ab_test.csv`

Key design note:

Random assignment supports an **intent-to-treat** analysis, where members are compared based on their assigned experiment group rather than their later participation behavior.

Enrollment, attendance, and session count occur after assignment and are intentionally selective. These variables should be treated as downstream funnel variables, not randomized baseline characteristics. Comparing attendees directly against non-attendees may introduce selection bias because participation can be influenced by engagement, health literacy, transportation barriers, and unobserved motivation.

---

### Notebook 01: EDA and Randomization Balance Check

Notebook 01 validates the synthetic A/B testing dataset before formal treatment-effect analysis.

The goal of this notebook is to confirm that the dataset is structurally sound, the treatment and control groups are reasonably balanced, and the peer-support funnel logic is valid before moving into statistical testing.

Main work completed:

* Loaded and inspected the synthetic member-level outreach dataset
* Confirmed the unit of analysis is one targetable diabetic member
* Reviewed dataset shape, column structure, data types, and missing values
* Verified that all members belong to the intended diabetic outreach target population
* Checked the experiment group distribution between:

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
* Previewed outcome differences without making final treatment-effect claims

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
* Outcome differences are included only as an exploratory preview and should not be interpreted as final treatment effects.

Output notebook:

`notebooks/01_EDA_And_Randomization_Balance_Check.ipynb`

Key design note:

This notebook does not estimate the final treatment effect. It prepares the dataset for formal A/B testing by validating randomization balance, missingness patterns, funnel logic, and outcome consistency.

The next notebook will use an intent-to-treat framework to compare members based on randomized assignment. That analysis should include absolute lift, relative lift, confidence intervals, p-values, and practical significance.

### Notebook 02: A/B Test Primary Outcome Analysis

Notebook 02 estimates the primary A/B testing result for the Diabetes Peer Support outreach experiment.

The goal of this notebook is to compare members assigned to Diabetes Peer Support against members assigned to Standard Outreach using an intent-to-treat framework.

Main work completed:

- Loaded the validated synthetic A/B testing dataset
- Confirmed treatment and control group definitions
- Defined the primary binary compliance outcome
- Compared compliance rates between Standard Outreach and Diabetes Peer Support
- Calculated absolute lift and relative lift
- Ran a two-proportion z-test for the binary compliance outcome
- Calculated a 95% confidence interval for the absolute lift
- Analyzed average diabetes testing compliance rate as a secondary outcome
- Ran a Welch two-sample t-test for average compliance rate
- Reviewed individual diabetes test completion rates
- Interpreted results using an intent-to-treat framework
- Avoided attendee-only causal claims because enrollment and attendance are selective

Key findings:

- Members assigned to Diabetes Peer Support had a higher binary compliance rate than members assigned to Standard Outreach.
- The binary compliance rate increased from 37.6% in Standard Outreach to 42.3% in Diabetes Peer Support.
- The absolute lift was 4.7 percentage points.
- The relative lift was 12.6%.
- The two-proportion z-test p-value was 0.0023.
- The 95% confidence interval for the binary absolute lift was 1.7 to 7.8 percentage points.
- The average diabetes testing compliance rate also improved from 71.3% to 74.5%.
- Individual diabetes test completion differences were reviewed as exploratory secondary outcomes.

Output notebook:

`notebooks/02_ab_test_primary_outcome.ipynb`

Key design note:

This notebook uses an intent-to-treat design. Members are compared based on randomized assignment, regardless of whether they enrolled in or attended the peer-support program.

This protects the main treatment comparison from participation-based selection bias. Funnel participation analysis should be handled separately.

### Notebook 03: Peer Support Funnel Analysis

Notebook 03 analyzes the operational funnel for the Diabetes Peer Support intervention.

The goal of this notebook is to evaluate how members assigned to Diabetes Peer Support moved through the program funnel from assignment to invitation, enrollment, attendance, and session participation.

Main work completed:

* Loaded the validated synthetic A/B testing dataset
* Defined the Diabetes Peer Support treatment group
* Kept the Standard Outreach group for funnel validation checks
* Validated peer-support funnel logic
* Confirmed that Standard Outreach members were not invited to the peer-support program
* Confirmed that enrollment only occurred after invitation
* Confirmed that attendance only occurred after enrollment
* Confirmed that positive session counts only occurred for members who attended at least one session
* Calculated member counts at each funnel stage
* Calculated invitation, enrollment, and attendance conversion rates
* Visualized peer-support funnel counts
* Visualized peer-support funnel conversion rates
* Reviewed the distribution of sessions attended
* Created business-friendly attendance groups
* Compared diabetes testing compliance across attendance groups
* Reviewed baseline differences across attendance groups
* Checked whether attendance groups differed by baseline engagement, health literacy, SDOH risk, and prior testing compliance
* Interpreted attendance results as exploratory associations, not causal effects

Key findings:

* The peer-support funnel logic was valid, with no detected structural violations.
* Members assigned to Diabetes Peer Support moved through the expected funnel stages: assignment, invitation, enrollment, and attendance.
* Funnel conversion rates helped identify where program drop-off occurred.
* Session attendance varied across treatment-group members.
* Members with higher session attendance showed different diabetes testing compliance patterns compared with members who attended no sessions.
* Baseline characteristics also varied across attendance groups, suggesting that attendance may reflect member selection as well as program engagement.
* Attendance-based comparisons were treated as operational and exploratory, not randomized causal evidence.

Output notebook:

`notebooks/03_peer_support_funnel_analysis.ipynb`

Key design note:

This notebook does not estimate the main randomized treatment effect.

The main A/B testing result remains the intent-to-treat comparison from Notebook 02. Notebook 03 focuses on implementation, engagement, and funnel performance among members assigned to the peer-support intervention.

Because enrollment and attendance are selective behaviors, higher compliance among attendees should be interpreted as an association, not proof that attending more sessions caused better diabetes testing compliance.

### Notebook 04: SDOH Segment Analysis

Notebook 04 explores whether observed Diabetes Peer Support outcomes differ across SDOH and baseline engagement segments.

The goal of this notebook is to identify which member subgroups may show stronger or weaker observed response patterns, while treating all segment-level results as exploratory and hypothesis-generating.

Main work completed:

* Loaded the validated synthetic A/B testing dataset
* Created SDOH risk groups using quantile-based segmentation
* Checked whether the SDOH risk score had enough unique values to support clean quantile grouping
* Compared treatment and control outcomes within Low, Medium, and High SDOH risk groups
* Analyzed specific SDOH barriers, including food insecurity, transportation barriers, financial barriers, and housing instability
* Created baseline engagement groups using quantile-based segmentation
* Reviewed missingness in baseline engagement before creating engagement groups
* Compared diabetes testing compliance across SDOH and engagement segments
* Calculated absolute and relative lift within each segment
* Reviewed subgroup sample sizes to reduce the risk of overinterpreting small segments
* Visualized segment-level outcome differences using percentage-formatted charts
* Interpreted all subgroup findings as exploratory, not definitive evidence of heterogeneous treatment effects

Key findings:

* Diabetes Peer Support showed positive observed lift across SDOH risk groups.
* Observed lift was not limited to only one SDOH risk tier.
* Among specific SDOH barriers, some barrier groups showed stronger observed lift than others.
* Members with financial barriers showed one of the stronger observed binary compliance lifts.
* Baseline engagement segments showed different observed response patterns.
* Members with higher baseline engagement appeared more responsive to the peer-support intervention in observed subgroup comparisons.
* Segment-level findings may help guide future targeting and program design, but they should not replace the overall intent-to-treat result from Notebook 02.
* Because multiple segments were reviewed, these results should be treated as exploratory subgroup evidence rather than confirmed causal differences.

Output notebook:

`notebooks/04_sdoh_segment_analysis.ipynb`

Key design note:

The primary randomized treatment effect remains the overall intent-to-treat analysis completed in Notebook 02.

Notebook 04 is an exploratory segment analysis. It helps identify possible targeting opportunities across SDOH risk, specific barriers, and baseline engagement levels, but it does not formally prove that the treatment effect differs across subgroups.

To formally test heterogeneous treatment effects, a later adjusted model should include treatment-by-segment interaction terms.
