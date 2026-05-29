## Project Progress

### Day 1: Synthetic Data Generation

Created a synthetic member-level dataset for a diabetes peer-support A/B testing project.

Day 1 focused on:
- Defining the target diabetic member population
- Simulating randomized assignment into Standard Outreach vs. Diabetes Peer Support
- Creating selective peer-support funnel behavior: invitation, enrollment, attendance, and session count
- Generating SDOH barriers, baseline engagement, health literacy, and diabetes testing outcomes
- Adding intentional structured missingness to better reflect healthcare data quality issues
- Running validation checks for group balance, funnel integrity, age realism, and diabetes test hierarchy

Output file:

`data/raw/mock_diabetes_peer_support_ab_test.csv`

Key design note:

Random assignment supports intent-to-treat analysis, while enrollment and attendance are selective and should be interpreted carefully because they may contain selection bias.