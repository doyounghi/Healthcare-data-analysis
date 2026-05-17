# 02 Healthcare Outreach A/B Testing

## Project Overview

This project is a synthetic healthcare analytics portfolio project focused on A/B testing. It evaluates whether a new outreach strategy increases Annual Wellness Visit (AWV) completion compared with a standard outreach strategy.

The project is designed for learning experiment design, two-proportion hypothesis testing, confidence intervals, power analysis, and business interpretation.

No real patient data is used. The dataset is fully synthetic and contains no PHI.

## Business Problem

Healthcare organizations often use outreach campaigns to encourage members to complete preventive visits. The business question is:

> Does a new outreach message increase AWV completion compared with the standard outreach message?

The control group receives the standard outreach message. The treatment group receives the new outreach message.

## Dataset Description

The synthetic member-level dataset includes:

- `member_id`: synthetic member identifier
- `age`: member age
- `gender`: synthetic gender category
- `region`: Urban, Suburban, or Rural
- `risk_score`: synthetic health risk score from 0 to 100
- `prior_awv_completed`: whether the member completed an AWV previously
- `prior_ed_visits`: prior emergency department visit count
- `engagement_score`: synthetic engagement score from 0 to 100
- `outreach_channel`: Phone, SMS, Email, or Mail
- `experiment_group`: control or treatment
- `awv_completed`: outcome variable for AWV completion
- `days_to_completion`: days until completion for members who completed

The processed dataset adds simple segment flags for business interpretation.

## Methodology

The primary method is a two-proportion A/B test:

1. Randomly assign members to control or treatment.
2. Compare AWV completion rates between groups.
3. Calculate absolute lift and relative lift.
4. Run a two-proportion z-test.
5. Calculate a 95% confidence interval for the absolute lift.
6. Interpret both statistical and practical significance.
7. Use power analysis to understand sample size needs.

## Key Metrics

- Control conversion rate
- Treatment conversion rate
- Absolute lift
- Relative lift
- Z-statistic
- P-value
- 95% confidence interval
- Required sample size per group

## Main Findings

In the synthetic data, the treatment group is designed to have a modest positive effect. The control AWV completion rate is approximately 24%, and the treatment completion rate is approximately 29%.

The A/B test notebooks calculate whether this difference is statistically significant and whether it may be practically meaningful for a healthcare outreach program.

## Limitations

- This project uses synthetic data only.
- No clinical claims should be made from the results.
- Segment analysis is exploratory unless pre-planned and powered.
- Statistical significance does not automatically mean business value.
- Real healthcare outreach programs require privacy, compliance, equity, and operational review.

## How to Run the Project

Install dependencies:

```bash
pip install -r requirements.txt
```

Run notebooks in order:

```text
notebooks/01_data_generation.ipynb
notebooks/02_experiment_eda.ipynb
notebooks/03_ab_test_analysis.ipynb
notebooks/04_power_sample_size_analysis.ipynb
notebooks/05_business_interpretation.ipynb
```

Generated outputs are saved under:

```text
outputs/figures/
outputs/tables/
```

## What I Learned

This project demonstrates how to:

- Design a simple randomized A/B test
- Check randomization balance using pre-treatment variables
- Calculate conversion rates and lift
- Run a two-proportion z-test
- Interpret p-values and confidence intervals
- Distinguish statistical significance from business value
- Estimate sample size requirements for different detectable effects
- Communicate experiment results with practical limitations
