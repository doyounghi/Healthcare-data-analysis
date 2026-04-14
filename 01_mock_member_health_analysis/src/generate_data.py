import os
import numpy as np
import pandas as pd

# Reproducibility
np.random.seed(42)

# Number of mock members
N = 500

# Output path
output_dir = os.path.join("data", "raw")
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "mock_member_data.csv")

# Basic member attributes
member_id = [f"M{str(i).zfill(5)}" for i in range(1, N + 1)]
age = np.random.randint(18, 90, size=N)
gender = np.random.choice(["Female", "Male"], size=N, p=[0.55, 0.45])
region = np.random.choice(
    ["Urban", "Suburban", "Rural"],
    size=N,
    p=[0.5, 0.3, 0.2]
)
plan_type = np.random.choice(
    ["Medicaid", "Medicare Advantage", "DSNP"],
    size=N,
    p=[0.5, 0.35, 0.15]
)

# Chronic condition count increases somewhat with age
base_chronic = np.random.poisson(lam=1.5, size=N)
age_effect = np.where(age >= 65, 2, np.where(age >= 50, 1, 0))
chronic_condition_count = np.clip(base_chronic + age_effect, 0, 8)

# Engagement score from 0 to 100
engagement_score = np.clip(
    np.random.normal(loc=55, scale=18, size=N),
    5,
    100
).round(1)

# Higher chronic burden -> more ED visits
ed_lambda = 0.3 + 0.25 * chronic_condition_count
ed_visits = np.random.poisson(lam=ed_lambda, size=N)
ed_visits = np.clip(ed_visits, 0, 12)

# Higher age + chronic burden -> more inpatient admits
ip_lambda = 0.05 + 0.03 * chronic_condition_count + np.where(age >= 65, 0.15, 0)
ip_admits = np.random.poisson(lam=ip_lambda, size=N)
ip_admits = np.clip(ip_admits, 0, 6)

# AWV completion probability influenced by engagement and age
awv_score = (
    -1.5
    + 0.03 * engagement_score
    + 0.015 * age
    - 0.15 * ed_visits
)
awv_probability = 1 / (1 + np.exp(-awv_score))
awv_completed = np.random.binomial(1, np.clip(awv_probability, 0.01, 0.95), size=N)

# Monthly cost formula with signal
plan_cost_map = {
    "Medicaid": 250,
    "Medicare Advantage": 400,
    "DSNP": 650
}
plan_cost = np.array([plan_cost_map[p] for p in plan_type])

monthly_cost = (
    80
    + age * 4
    + chronic_condition_count * 180
    + ed_visits * 220
    + ip_admits * 900
    + plan_cost
    + np.random.normal(0, 120, size=N)
)
monthly_cost = np.clip(monthly_cost, 50, None).round(2)

# Final dataframe
df = pd.DataFrame({
    "member_id": member_id,
    "age": age,
    "gender": gender,
    "region": region,
    "plan_type": plan_type,
    "chronic_condition_count": chronic_condition_count,
    "engagement_score": engagement_score,
    "ed_visits": ed_visits,
    "ip_admits": ip_admits,
    "monthly_cost": monthly_cost,
    "awv_completed": awv_completed
})

# Save CSV
df.to_csv(output_path, index=False)

print(f"Mock dataset created successfully: {output_path}")
print(df.head())
print("\nShape:", df.shape)