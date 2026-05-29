# src/generate_diabetes_peer_support_data.py

"""
Generate synthetic member-level data for Project 02:
Diabetes Peer Support Program A/B Testing.

Business question:
Does inviting diabetic members to a bi-weekly peer-support program improve
diabetes testing compliance compared with standard outreach?

Design Note:
- This synthetic dataset represents the final targetable diabetic population:
  adult members with diabetes who have at least one assigned diabetes test.
  We are not simulating the full health plan population first.
- Separates randomized assignment (ITT) from selective down-funnel participation.
"""

from pathlib import Path
import numpy as np
import pandas as pd

# ---------------------------------------------------------------------
# 1. Global settings
# ---------------------------------------------------------------------
RANDOM_SEED = 42
N_MEMBERS = 4000

np.random.seed(RANDOM_SEED)

# ---------------------------------------------------------------------
# 2. Project paths
# ---------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
OUTPUT_FILE = RAW_DATA_DIR / "mock_diabetes_peer_support_ab_test.csv"

RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------
# 3. Helper function
# ---------------------------------------------------------------------
def sigmoid(x):
    """Convert a numeric score into a probability between 0 and 1."""
    return 1 / (1 + np.exp(-x))

# ---------------------------------------------------------------------
# 4. Generate baseline plan type and conditioned demographics
# ---------------------------------------------------------------------
member_id = np.arange(1, N_MEMBERS + 1)

plan_type = np.random.choice(
    ["Medicaid", "Medicare Advantage", "D-SNP"],
    size=N_MEMBERS,
    p=[0.50, 0.25, 0.25]
)

# Plan-conditioned age generation to match insurance eligibility rules
age = np.where(
    plan_type == "Medicaid",
    np.random.normal(loc=48, scale=12, size=N_MEMBERS),
    np.random.normal(loc=72, scale=7, size=N_MEMBERS)
)
age = np.round(age).astype(int)

# FIX: Clip Medicare/D-SNP to 65+ to avoid reviewer confusion regarding disability eligibility
age = np.where(
    plan_type == "Medicaid",
    np.clip(age, 18, 89),
    np.clip(age, 65, 89)
)

gender = np.random.choice(["Female", "Male"], size=N_MEMBERS, p=[0.54, 0.46])
region = np.random.choice(["Urban", "Suburban", "Rural"], size=N_MEMBERS, p=[0.45, 0.35, 0.20])

# Explicit indicator that this cohort isolates the active diabetic target population
target_population_flag = np.repeat(1, N_MEMBERS)

# ---------------------------------------------------------------------
# 5. Internal Latent Factors (Hidden Confounders)
# ---------------------------------------------------------------------
# Unobserved motivation explains selection bias in attendance
unobserved_motivation = np.random.normal(loc=0, scale=1, size=N_MEMBERS)

# ---------------------------------------------------------------------
# 6. Generate health, engagement, and access features
# ---------------------------------------------------------------------
diabetes_severity_score = np.random.beta(a=2.2, b=2.8, size=N_MEMBERS)

chronic_condition_count = np.random.poisson(
    lam=1.8 + diabetes_severity_score * 2.2,
    size=N_MEMBERS
)
chronic_condition_count = np.clip(chronic_condition_count, 0, 8)

baseline_engagement_score = np.random.beta(a=2.3, b=2.2, size=N_MEMBERS)
health_literacy_score = np.random.beta(a=2.5, b=2.4, size=N_MEMBERS)

pcp_prob = sigmoid(
    -0.2
    + 1.0 * baseline_engagement_score
    + 0.6 * health_literacy_score
    - 0.4 * diabetes_severity_score
)
pcp_attributed_24mo = np.random.binomial(1, pcp_prob, size=N_MEMBERS)

# ---------------------------------------------------------------------
# 7. Generate explicit SDOH barriers
# ---------------------------------------------------------------------
food_insecurity_prob = sigmoid(
    -1.1
    + 0.6 * (plan_type == "Medicaid")
    + 0.4 * (plan_type == "D-SNP")
    + 0.3 * (region == "Rural")
)

transportation_barrier_prob = sigmoid(
    -1.3
    + 0.7 * (region == "Rural")
    + 0.3 * (plan_type == "Medicaid")
    + 0.3 * diabetes_severity_score
)

financial_barrier_prob = sigmoid(
    -1.0
    + 0.8 * (plan_type == "Medicaid")
    + 0.4 * (plan_type == "D-SNP")
)

housing_instability_prob = sigmoid(
    -1.8
    + 0.7 * (plan_type == "Medicaid")
    + 0.3 * food_insecurity_prob
)

food_insecurity = np.random.binomial(1, food_insecurity_prob, size=N_MEMBERS)
transportation_barrier = np.random.binomial(1, transportation_barrier_prob, size=N_MEMBERS)
financial_barrier = np.random.binomial(1, financial_barrier_prob, size=N_MEMBERS)
housing_instability = np.random.binomial(1, housing_instability_prob, size=N_MEMBERS)

sdoh_risk_score = (
    0.30 * food_insecurity
    + 0.30 * transportation_barrier
    + 0.25 * financial_barrier
    + 0.15 * housing_instability
    + np.random.normal(0, 0.08, N_MEMBERS)
)
sdoh_risk_score = np.clip(sdoh_risk_score, 0, 1)

# ---------------------------------------------------------------------
# 8. Generate prior testing compliance
# ---------------------------------------------------------------------
prior_compliance_prob = sigmoid(
    -0.4
    + 1.2 * baseline_engagement_score
    + 0.8 * health_literacy_score
    + 0.5 * pcp_attributed_24mo
    - 1.0 * sdoh_risk_score
)
prior_testing_compliance_rate = np.random.beta(
    a=1 + prior_compliance_prob * 5,
    b=1 + (1 - prior_compliance_prob) * 5
)

# ---------------------------------------------------------------------
# 9. Randomized A/B assignment (Intent-to-Treat Engine)
# ---------------------------------------------------------------------
experiment_group = np.random.choice(
    ["Standard Outreach", "Diabetes Peer Support"],
    size=N_MEMBERS,
    p=[0.50, 0.50]
)
outreach_type = experiment_group.copy()
is_treatment = (experiment_group == "Diabetes Peer Support")

# ---------------------------------------------------------------------
# 10. Peer-support funnel logic (Selective Participation)
# ---------------------------------------------------------------------
program_invited = np.where(is_treatment, np.random.binomial(1, 0.85, N_MEMBERS), 0)

enrollment_prob = sigmoid(
    -0.7
    + 0.7 * baseline_engagement_score
    + 0.4 * health_literacy_score
    + 0.3 * unobserved_motivation
    - 0.5 * transportation_barrier
)
program_enrolled = np.where(program_invited == 1, np.random.binomial(1, enrollment_prob, N_MEMBERS), 0)

attendance_prob = sigmoid(
    -0.9
    + 0.9 * baseline_engagement_score
    + 0.3 * unobserved_motivation
    - 0.7 * transportation_barrier
)
attended_at_least_one_session = np.where(program_enrolled == 1, np.random.binomial(1, attendance_prob, N_MEMBERS), 0)

# Safe Poisson lambda clipping to prevent runtime crashes
session_lambda = (
    2.4
    + 2.0 * baseline_engagement_score
    + 0.5 * unobserved_motivation
)
session_lambda = np.clip(session_lambda, 0.1, None)

sessions_attended_count = np.where(
    attended_at_least_one_session == 1,
    np.random.poisson(lam=session_lambda, size=N_MEMBERS),
    0
)
sessions_attended_count = np.clip(sessions_attended_count, 0, 8)

peer_leader_supervised = np.where(is_treatment, 1, 0)
contact_frequency_per_month = np.where(is_treatment, 2, 1)

# Operational data quality anomalies flag used as an indicator for system logging friction
program_data_quality_issue = np.random.binomial(1, 0.02, size=N_MEMBERS)

# ---------------------------------------------------------------------
# 11. Generate diabetes testing outcomes (Causal Separation)
# ---------------------------------------------------------------------
itt_assignment_effect = 0.08 * is_treatment

support_dose_effect = (
    0.08 * program_enrolled
    + 0.14 * attended_at_least_one_session
    + 0.04 * sessions_attended_count
)

sdoh_buffer_effect = (0.20 * sdoh_risk_score * attended_at_least_one_session)

base_test_score = (
    -0.3
    + 1.1 * baseline_engagement_score
    + 0.8 * health_literacy_score
    + 0.5 * pcp_attributed_24mo
    + 0.4 * prior_testing_compliance_rate
    - 0.9 * sdoh_risk_score
    + itt_assignment_effect
    + support_dose_effect
    + sdoh_buffer_effect
)

a1c_prob = sigmoid(base_test_score + 0.6)
kidney_prob = sigmoid(base_test_score + 0.1)
eye_exam_prob = sigmoid(base_test_score - 0.4)

a1c_test_completed = np.random.binomial(1, a1c_prob, size=N_MEMBERS)
kidney_screening_completed = np.random.binomial(1, kidney_prob, size=N_MEMBERS)
eye_exam_completed = np.random.binomial(1, eye_exam_prob, size=N_MEMBERS)

assigned_diabetes_tests_count = np.repeat(3, N_MEMBERS)
diabetes_tests_completed_count = a1c_test_completed + kidney_screening_completed + eye_exam_completed
diabetes_testing_compliance_rate = diabetes_tests_completed_count / assigned_diabetes_tests_count
diabetes_testing_compliant = (diabetes_testing_compliance_rate >= 0.75).astype(int)

# ---------------------------------------------------------------------
# 12. Build DataFrame & Apply Non-Random Missingness (MAR Engine)
# ---------------------------------------------------------------------
df = pd.DataFrame({
    "member_id": member_id,
    "age": age,
    "gender": gender,
    "region": region,
    "plan_type": plan_type,
    "target_population_flag": target_population_flag,
    "diabetes_severity_score": diabetes_severity_score.round(3),
    "chronic_condition_count": chronic_condition_count,
    "baseline_engagement_score": baseline_engagement_score.round(3),
    "health_literacy_score": health_literacy_score.round(3),
    "prior_testing_compliance_rate": prior_testing_compliance_rate.round(3),
    "sdoh_risk_score": sdoh_risk_score.round(3),
    "food_insecurity": food_insecurity,
    "transportation_barrier": transportation_barrier,
    "financial_barrier": financial_barrier,
    "housing_instability": housing_instability,
    "pcp_attributed_24mo": pcp_attributed_24mo,
    "experiment_group": experiment_group,
    "outreach_type": outreach_type,
    "program_invited": program_invited,
    "program_enrolled": program_enrolled,
    "attended_at_least_one_session": attended_at_least_one_session,
    "sessions_attended_count": sessions_attended_count,
    "peer_leader_supervised": peer_leader_supervised,
    "contact_frequency_per_month": contact_frequency_per_month,
    "assigned_diabetes_tests_count": assigned_diabetes_tests_count,
    "a1c_test_completed": a1c_test_completed,
    "kidney_screening_completed": kidney_screening_completed,
    "eye_exam_completed": eye_exam_completed,
    "diabetes_tests_completed_count": diabetes_tests_completed_count,
    "diabetes_testing_compliance_rate": diabetes_testing_compliance_rate.round(3),
    "diabetes_testing_compliant": diabetes_testing_compliant,
    "program_data_quality_issue": program_data_quality_issue
})

# Generate structured missingness mapped to features & operational data quality flags
health_literacy_missing_prob = sigmoid(
    -2.6
    + 0.8 * df["sdoh_risk_score"]
    - 0.5 * df["baseline_engagement_score"].fillna(df["baseline_engagement_score"].mean())
)

engagement_missing_prob = sigmoid(
    -3.0
    + 0.7 * df["sdoh_risk_score"]
    + 0.4 * df["program_data_quality_issue"]
)

health_literacy_missing = np.random.binomial(1, health_literacy_missing_prob, size=N_MEMBERS).astype(bool)
engagement_missing = np.random.binomial(1, engagement_missing_prob, size=N_MEMBERS).astype(bool)

df.loc[health_literacy_missing, "health_literacy_score"] = np.nan
df.loc[engagement_missing, "baseline_engagement_score"] = np.nan

# ---------------------------------------------------------------------
# 13. Enhanced Validation Checks
# ---------------------------------------------------------------------
print("\n=== EXPANDED COMPLIANCE VALIDATION RUN ===")
print(f"Dataset shape: {df.shape}")

# FIX: Renamed output label to prevent academic overclaiming
print("\nMissing Values Capture Rate (Intentional Structured Missingness):")
print(df.isna().sum()[df.isna().sum() > 0])

print("\nAge Demographics Profile by Insurance Plan Type:")
print(df.groupby("plan_type")["age"].agg(["min", "mean", "max"]).round(1))

print("\nExperiment Group Structural Balance Check:")
print(df["experiment_group"].value_counts(normalize=True).round(3))

# FIX: Clarified terminology from "clinical" to "peer-support" sessions
print("\nPeer-Support Funnel Operational Progression Rates (Treatment Only):")
treatment_df = df[df["experiment_group"] == "Diabetes Peer Support"]
print("Invitation rate:", treatment_df["program_invited"].mean().round(3))
print("Enrollment rate among invited:", treatment_df.loc[treatment_df["program_invited"] == 1, "program_enrolled"].mean().round(3))
print("Attendance rate among enrolled:", treatment_df.loc[treatment_df["program_enrolled"] == 1, "attended_at_least_one_session"].mean().round(3))
print("Average peer-support sessions attended:", treatment_df["sessions_attended_count"].mean().round(3))

print("\nDiabetes Screening Performance Outcomes by Assigned Arm:")
print(
    df.groupby("experiment_group")[
        [
            "diabetes_testing_compliance_rate",
            "diabetes_testing_compliant",
            "a1c_test_completed",
            "kidney_screening_completed",
            "eye_exam_completed"
        ]
    ].mean().round(3)
)

print("\nClinical Measure Barrier Hierarchy Order (Expected: A1c -> Kidney -> Eye):")
print(
    df[
        [
            "a1c_test_completed",
            "kidney_screening_completed",
            "eye_exam_completed"
        ]
    ].mean().sort_values(ascending=False).round(3)
)

print("\nFunnel State Invalidation Metric (Expected: 0):")
funnel_violations = (
    ((df["experiment_group"] == "Standard Outreach") & (df["program_invited"] == 1)).sum()
    + ((df["program_invited"] == 0) & (df["program_enrolled"] == 1)).sum()
    + ((df["program_enrolled"] == 0) & (df["attended_at_least_one_session"] == 1)).sum()
    + ((df["attended_at_least_one_session"] == 0) & (df["sessions_attended_count"] > 0)).sum()
)
print(f"Total Structural Violations Observed: {funnel_violations}")

# ---------------------------------------------------------------------
# 14. Save output
# ---------------------------------------------------------------------
df.to_csv(OUTPUT_FILE, index=False)
print(f"\nSynthetic dataset successfully saved to: {OUTPUT_FILE}")