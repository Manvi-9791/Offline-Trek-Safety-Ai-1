"""
Generate synthetic trekking dataset for Offline Trekking Safety AI.

Uses simulation modules (terrain + weather) to create rows with features
and assigns risk_level (Safe / Moderate_Risk / High_Risk) so that
a Decision Tree or Random Forest can learn the mapping.

Run from project root:
    python scripts/generate_dataset.py
"""

import os
import sys
import numpy as np
import pandas as pd

# Add project root to path so we can import config and simulation
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from config.schema import (
    FEATURE_COLUMNS,
    TARGET_COLUMN,
    RISK_LEVELS,
    RAW_DATA_DIR,
)
from simulation.terrain_simulator import generate_terrain_row
from simulation.weather_simulator import generate_weather_row


def generate_one_sample(rng: np.random.Generator, risk_level: str) -> dict:
    """
    Generate one trekking segment with all features and the given risk_level.
    risk_level is used as bias when calling terrain and weather simulators.
    """
    # Map label to risk_bias for simulators
    risk_bias = "high_risk" if risk_level == "High_Risk" else ("safe" if risk_level == "Safe" else "neutral")
    terrain = generate_terrain_row(rng, risk_bias)
    weather = generate_weather_row(rng, risk_bias)
    row = {**terrain, **weather, TARGET_COLUMN: risk_level}
    return row


def generate_synthetic_dataset(
    n_per_class: int = 200,
    seed: int = 42,
) -> pd.DataFrame:
    """
    Generate balanced synthetic dataset with n_per_class samples per risk level.
    """
    rng = np.random.default_rng(seed)
    rows = []
    for risk in RISK_LEVELS:
        for _ in range(n_per_class):
            rows.append(generate_one_sample(rng, risk))
    df = pd.DataFrame(rows)
    # Ensure column order: features first, then target
    columns = FEATURE_COLUMNS + [TARGET_COLUMN]
    return df[columns]


def main():
    # Default: 200 samples per class = 600 rows total
    n_per_class = 200
    seed = 42
    df = generate_synthetic_dataset(n_per_class=n_per_class, seed=seed)

    raw_dir = os.path.join(PROJECT_ROOT, RAW_DATA_DIR)
    os.makedirs(raw_dir, exist_ok=True)
    out_path = os.path.join(raw_dir, "trekking_synthetic.csv")
    df.to_csv(out_path, index=False)
    print(f"Generated {len(df)} samples. Saved to {out_path}")
    print("Risk level counts:")
    print(df[TARGET_COLUMN].value_counts().to_string())


if __name__ == "__main__":
    main()
