import os  # Used to create folders and file paths
import numpy as np  # Used for random number generation and numerical calculations
import pandas as pd  # Used to create and save the final dataframe


# Reproducibility
np.random.seed(42)  # Set a random seed so the generated dataset is the same each time the code runs


# Number of mock members
N = 3000  # Larger synthetic population for more stable model diagnostics

# Output path
from pathlib import Path  # Use pathlib for safer project-relative paths

PROJECT_ROOT = Path(__file__).resolve().parents[1]  # src file -> project root

output_dir = PROJECT_ROOT / "data" / "raw"  # Always point to project-root/data/raw
output_dir.mkdir(parents=True, exist_ok=True)  # Create folder if needed

output_path = output_dir / "mock_member_data.csv"  # Final CSV path
# Basic member attributes
member_id = [f"M{str(i).zfill(5)}" for i in range(1, N + 1)]  # Create unique member IDs

age = np.random.randint(
    18, 90, size=N
)  # Generate random ages from 18 to 89

gender = np.random.choice(
    ["Female", "Male"],
    size=N,
    p=[0.55, 0.45]
)  # Randomly assign gender with slightly more female members

region = np.random.choice(
    ["Urban", "Suburban", "Rural"],
    size=N,
    p=[0.50, 0.30, 0.20]
)  # Randomly assign region with more urban members

plan_type = np.random.choice(
    ["Medicaid", "Medicare Advantage", "DSNP"],
    size=N,
    p=[0.50, 0.35, 0.15]
)  # Randomly assign plan type with DSNP as a smaller high-risk group


# Chronic condition count
base_chronic = np.random.poisson(
    lam=1.5,
    size=N
)  # Generate baseline chronic condition count

age_effect = np.where(
    age >= 65,
    2,
    np.where(age >= 50, 1, 0)
)  # Older members receive higher expected chronic burden

chronic_condition_count = np.clip(
    base_chronic + age_effect,
    0,
    8
)  # Cap chronic condition count between 0 and 8


# SDOH risk score
# Higher score means higher social risk, such as transportation barriers, food insecurity, housing instability, or financial stress

region_sdoh_base = np.select(
    [
        region == "Urban",
        region == "Suburban",
        region == "Rural"
    ],
    [
        55,
        40,
        60
    ]
)  # Assign region-based SDOH baseline

plan_sdoh_adjustment = np.select(
    [
        plan_type == "Medicaid",
        plan_type == "Medicare Advantage",
        plan_type == "DSNP"
    ],
    [
        10,
        0,
        15
    ]
)  # Add plan-based SDOH adjustment

sdoh_risk_score = np.clip(
    region_sdoh_base
    + plan_sdoh_adjustment
    + np.random.normal(0, 12, size=N),
    0,
    100
).round(1)  # Create final SDOH score from 0 to 100


# Engagement score
# Higher SDOH risk and rural access barriers reduce expected engagement

region_engagement_adjustment = np.select(
    [
        region == "Urban",
        region == "Suburban",
        region == "Rural"
    ],
    [
        0,
        5,
        -8
    ]
)  # Adjust engagement based on region

engagement_score = np.clip(
    65
    + region_engagement_adjustment
    - 0.35 * sdoh_risk_score
    + np.random.normal(0, 12, size=N),
    5,
    100
).round(1)  # Create engagement score from 5 to 100


# PCP attribution in the last 24 months
# Members with higher engagement are more likely to have PCP attribution
# Members with higher SDOH risk or rural barriers are less likely to have PCP attribution

pcp_score = (
    -0.8
    + 0.035 * engagement_score
    - 0.012 * sdoh_risk_score
    - 0.35 * (region == "Rural").astype(int)
)  # Create log-odds score for PCP attribution

pcp_probability = 1 / (1 + np.exp(-pcp_score))  # Convert log-odds into probability

pcp_attributed_24mo = np.random.binomial(
    n=1,
    p=np.clip(pcp_probability, 0.05, 0.95),
    size=N
)  # Generate PCP attribution flag


# ED visits
# Higher chronic burden, SDOH risk, low engagement, and DSNP status increase ED use
# PCP attribution lowers expected ED use

is_dsnp = (plan_type == "DSNP").astype(int)  # Flag DSNP members

low_engagement = (engagement_score < 35).astype(int)  # Flag low-engagement members

ed_lambda = (
    0.20
    + 0.22 * chronic_condition_count
    + 0.008 * sdoh_risk_score
    + 0.25 * low_engagement
    + 0.25 * is_dsnp
    - 0.20 * pcp_attributed_24mo
)  # Create expected ED visit count

ed_lambda = np.clip(
    ed_lambda,
    0.05,
    None
)  # Prevent invalid negative Poisson rates

ed_visits = np.random.poisson(
    lam=ed_lambda,
    size=N
)  # Generate ED visit counts

ed_visits = np.clip(
    ed_visits,
    0,
    12
)  # Cap ED visits at 12


# Inpatient admissions
# Higher age, chronic burden, SDOH risk, and ED visits increase admission risk
# PCP attribution lowers expected admission risk

ip_lambda = (
    0.04
    + 0.035 * chronic_condition_count
    + np.where(age >= 65, 0.12, 0)
    + 0.004 * sdoh_risk_score
    + 0.08 * ed_visits
    - 0.08 * pcp_attributed_24mo
)  # Create expected inpatient admission count

ip_lambda = np.clip(
    ip_lambda,
    0.01,
    None
)  # Prevent invalid negative Poisson rates

ip_admits = np.random.poisson(
    lam=ip_lambda,
    size=N
)  # Generate inpatient admission counts

ip_admits = np.clip(
    ip_admits,
    0,
    6
)  # Cap inpatient admits at 6


# Prior AWV behavior
# Members with higher engagement and lower SDOH risk are more likely to have completed AWVs historically

prior_awv_lambda = (
    0.30
    + 0.025 * engagement_score
    - 0.010 * sdoh_risk_score
    + 0.35 * pcp_attributed_24mo
)  # Create expected prior AWV count over 3 years

prior_awv_lambda = np.clip(
    prior_awv_lambda,
    0.05,
    3.00
)  # Keep expected count inside a reasonable 3-year range

prior_awv_count = np.random.poisson(
    lam=prior_awv_lambda,
    size=N
)  # Generate prior AWV count

prior_awv_count = np.clip(
    prior_awv_count,
    0,
    3
)  # Prior AWV count cannot exceed 3 in a 3-year lookback

prior_awv_rate = prior_awv_count / 3  # Normalize prior AWV count into a 0 to 1 rate


# Current-year AWV completion
# Engagement, prior AWV behavior, PCP attribution, and age increase AWV probability
# ED use and SDOH risk reduce AWV probability

awv_score = (
    -1.8
    + 0.035 * engagement_score
    + 0.012 * age
    + 1.25 * prior_awv_rate
    + 0.60 * pcp_attributed_24mo
    - 0.12 * ed_visits
    - 0.015 * sdoh_risk_score
)  # Create log-odds score for AWV completion

awv_probability = 1 / (1 + np.exp(-awv_score))  # Convert log-odds into probability

awv_completed = np.random.binomial(
    n=1,
    p=np.clip(awv_probability, 0.01, 0.95),
    size=N
)  # Generate current-year AWV completion flag


# Monthly cost
# More realistic cost generation using nonlinear effects, interactions, rare acute events, skewed noise, and hidden risk

plan_cost_map = {
    "Medicaid": 250,
    "Medicare Advantage": 400,
    "DSNP": 700
}  # Assign baseline cost by plan type

plan_cost = np.array(
    [plan_cost_map[p] for p in plan_type]
)  # Convert plan type into numeric baseline cost

high_chronic_burden = (chronic_condition_count >= 4).astype(int)  # Flag members with high chronic burden

is_senior = (age >= 65).astype(int)  # Flag senior members

acute_event = np.random.binomial(
    n=1,
    p=0.07,
    size=N
)  # Generate rare high-cost acute event flag

acute_event_cost = acute_event * np.random.lognormal(
    mean=7.2,
    sigma=0.55,
    size=N
)  # Generate right-skewed acute event cost

skewed_noise = np.random.lognormal(
    mean=4.8,
    sigma=0.6,
    size=N
)  # Add right-skewed random healthcare cost noise

unobserved_risk = np.random.normal(
    loc=0,
    scale=250,
    size=N
)  # Add hidden risk not captured by visible predictors

monthly_cost = (
    100
    + age * 3.5
    + chronic_condition_count * 130
    + (chronic_condition_count ** 2) * 35
    + ed_visits * 180
    + ip_admits * 850
    + plan_cost
    + high_chronic_burden * 350
    + is_senior * high_chronic_burden * 300
    + is_dsnp * high_chronic_burden * 450
    + low_engagement * ed_visits * 120
    - pcp_attributed_24mo * 150
    + acute_event_cost
    + skewed_noise
    + unobserved_risk
)  # Generate final monthly cost

monthly_cost = np.clip(
    monthly_cost,
    50,
    15000
).round(2)  # Keep monthly cost in a plausible synthetic range


# Final dataframe
df = pd.DataFrame({
    "member_id": member_id,
    "age": age,
    "gender": gender,
    "region": region,
    "plan_type": plan_type,
    "sdoh_risk_score": sdoh_risk_score,
    "chronic_condition_count": chronic_condition_count,
    "engagement_score": engagement_score,
    "pcp_attributed_24mo": pcp_attributed_24mo,
    "prior_awv_count": prior_awv_count,
    "prior_awv_rate": prior_awv_rate,
    "ed_visits": ed_visits,
    "ip_admits": ip_admits,
    "monthly_cost": monthly_cost,
    "awv_completed": awv_completed
})  # Combine all generated arrays into one dataframe


# Save CSV
df.to_csv(output_path, index=False)  # Save the generated dataset to CSV


# Quick validation output
print(f"Mock dataset created successfully: {output_path}")  # Confirm file creation
print(df.head())  # Preview first five rows
print("\nShape:", df.shape)  # Show row and column count

print("\nMonthly cost summary:")  # Label monthly cost summary
print(df["monthly_cost"].describe())  # Check cost distribution

print("\nAWV completion rate:")  # Label AWV completion summary
print(df["awv_completed"].mean())  # Check current-year AWV completion rate

print("\nPCP attribution rate:")  # Label PCP attribution summary
print(df["pcp_attributed_24mo"].mean())  # Check PCP attribution rate

print("\nAverage ED visits by SDOH risk quartile:")  # Label ED by SDOH summary
print(
    df.groupby(pd.qcut(df["sdoh_risk_score"], q=4))["ed_visits"].mean()
)  # Check whether higher SDOH risk is associated with more ED visits