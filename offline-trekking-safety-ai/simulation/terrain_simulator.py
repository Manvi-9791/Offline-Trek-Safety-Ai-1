"""
Terrain simulator for synthetic trekking segments.

Generates slope_angle, altitude_change, trail_difficulty, and path_width_m
using simple rules so that the dataset reflects realistic trekking conditions.
"""

import numpy as np


def generate_slope_angle(rng: np.random.Generator, risk_bias: str = "neutral") -> float:
    """
    Generate slope angle in degrees (0-45).
    risk_bias: 'safe' -> lower slopes, 'high_risk' -> steeper, 'neutral' -> mixed.
    """
    if risk_bias == "safe":
        # Safe routes: mostly gentle slopes
        return float(rng.uniform(0, 15))
    if risk_bias == "high_risk":
        return float(rng.uniform(25, 45))
    # neutral / moderate
    return float(rng.uniform(0, 45))


def generate_altitude_change(rng: np.random.Generator, risk_bias: str = "neutral") -> float:
    """
    Generate altitude change in meters (-500 to +500).
    Large absolute change can correlate with difficulty.
    """
    if risk_bias == "safe":
        return float(rng.uniform(-200, 200))
    if risk_bias == "high_risk":
        # Large gain or drop: pick one at random
        return float(rng.uniform(300, 500)) if rng.random() > 0.5 else float(rng.uniform(-500, -300))
    return float(rng.uniform(-500, 500))


def generate_trail_difficulty(rng: np.random.Generator, risk_bias: str = "neutral") -> int:
    """Generate trail difficulty 1-5. 1=easy, 5=expert."""
    if risk_bias == "safe":
        return int(rng.integers(1, 3))
    if risk_bias == "high_risk":
        return int(rng.integers(4, 6))  # 4 or 5
    return int(rng.integers(1, 6))


def generate_path_width(rng: np.random.Generator, risk_bias: str = "neutral") -> float:
    """Generate path width in meters (0.5-5.0). Narrow = more risk."""
    if risk_bias == "safe":
        return float(rng.uniform(2.0, 5.0))
    if risk_bias == "high_risk":
        return float(rng.uniform(0.5, 1.5))
    return float(rng.uniform(0.5, 5.0))


def generate_terrain_row(rng: np.random.Generator, risk_bias: str = "neutral") -> dict:
    """
    Generate one row of terrain-related features.
    risk_bias influences the distributions to match Safe / Moderate / High Risk.
    """
    return {
        "slope_angle": generate_slope_angle(rng, risk_bias),
        "altitude_change": generate_altitude_change(rng, risk_bias),
        "trail_difficulty": generate_trail_difficulty(rng, risk_bias),
        "path_width_m": generate_path_width(rng, risk_bias),
    }
