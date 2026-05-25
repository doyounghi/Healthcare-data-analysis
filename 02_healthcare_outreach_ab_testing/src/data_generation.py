"""Synthetic data generation for the healthcare outreach A/B testing project.

All data is synthetic. It contains no real patient data and no PHI.
"""
from pathlib import Path

import numpy as np
import pandas as pd


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def generate_outreach_data(n_members=8000, random_state=42):
    """Generate synthetic member-level outreach experiment data."""
    rng = np.random.default_rng(random_state)
    member_id = [f"M{i:05d}" for i in range(1, n_members + 1)]
    age = np.clip(rng.normal(67, 12, n_members).round(), 18, 95).astype(int)
    gender = rng.choice(["Female", "Male"], n_members, p=[0.54, 0.46])
    region = rng.choice(["Urban", "Suburban", "Rural"], n_members, p=[0.42, 0.38, 0.20])
    risk_score = np.clip(rng.normal(52, 18, n_members), 0, 100).round(1)
    prior_awv_completed = rng.binomial(1, 0.38, n_members)
    prior_ed_visits = rng.poisson(np.clip(risk_score / 45, 0.1, 3.5)).clip(0, 8)
    engagement_score = np.clip(
        rng.normal(58, 18, n_members) + prior_awv_completed * 8 - (region == "Rural") * 4,
        0,
        100,
    ).round(1)
    outreach_channel = rng.choice(["Phone", "SMS", "Email", "Mail"], n_members, p=[0.30, 0.30, 0.25, 0.15])

    # Random assignment: treatment should not depend on member characteristics.
    experiment_group = rng.choice(["control", "treatment"], n_members, p=[0.50, 0.50])

    # Treatment effect is modest and positive, creating roughly 24% vs 29% completion.
    linear_score = (
        -1.40
        + 0.33 * (experiment_group == "treatment")
        + 0.45 * prior_awv_completed
        + 0.012 * (engagement_score - 58)
        - 0.006 * (risk_score - 52)
        - 0.10 * (region == "Rural")
        + 0.05 * (outreach_channel == "Phone")
        + 0.04 * (outreach_channel == "SMS")
        - 0.03 * (prior_ed_visits >= 2)
    )
    awv_completed = rng.binomial(1, sigmoid(linear_score))
    days_to_completion = np.where(
        awv_completed == 1,
        np.clip(rng.gamma(shape=3.0, scale=9.0, size=n_members).round(), 1, 90),
        np.nan,
    )

    return pd.DataFrame({
        "member_id": member_id,
        "age": age,
        "gender": gender,
        "region": region,
        "risk_score": risk_score,
        "prior_awv_completed": prior_awv_completed,
        "prior_ed_visits": prior_ed_visits,
        "engagement_score": engagement_score,
        "outreach_channel": outreach_channel,
        "experiment_group": experiment_group,
        "awv_completed": awv_completed,
        "days_to_completion": days_to_completion,
    })


def save_outreach_data(df, project_root):
    project_root = Path(project_root)
    raw_path = project_root / "data" / "raw" / "synthetic_outreach_ab_test_raw.csv"
    processed_path = project_root / "data" / "processed" / "outreach_ab_test_processed.csv"
    raw_path.parent.mkdir(parents=True, exist_ok=True)
    processed_path.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(raw_path, index=False)

    processed = df.copy()
    processed["is_treatment"] = (processed["experiment_group"] == "treatment").astype(int)
    processed["high_risk_member"] = (processed["risk_score"] >= 70).astype(int)
    processed["low_engagement_member"] = (processed["engagement_score"] < 40).astype(int)
    processed["has_prior_ed_visit"] = (processed["prior_ed_visits"] > 0).astype(int)
    processed["no_prior_awv"] = (processed["prior_awv_completed"] == 0).astype(int)
    processed.to_csv(processed_path, index=False)
    return raw_path, processed_path


if __name__ == "__main__":
    project_root = Path(__file__).resolve().parents[1]
    data = generate_outreach_data()
    print(save_outreach_data(data, project_root))
