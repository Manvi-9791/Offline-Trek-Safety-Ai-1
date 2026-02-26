"""
Weather simulator for synthetic trekking data.

Generates weather_severity (1-5) and visibility_km so that
bad weather and low visibility align with higher risk.
"""

import numpy as np


def generate_weather_severity(rng: np.random.Generator, risk_bias: str = "neutral") -> int:
    """
    Generate weather severity 1-5.
    1 = clear, 5 = storm/heavy fog.
    """
    if risk_bias == "safe":
        return int(rng.integers(1, 3))  # 1 or 2
    if risk_bias == "high_risk":
        return int(rng.integers(4, 6))  # 4 or 5
    return int(rng.integers(1, 6))


def generate_visibility_km(rng: np.random.Generator, risk_bias: str = "neutral") -> float:
    """
    Generate visibility in kilometers (0.1-20).
    Low visibility increases risk.
    """
    if risk_bias == "safe":
        return float(rng.uniform(5.0, 20.0))
    if risk_bias == "high_risk":
        return float(rng.uniform(0.1, 2.0))
    return float(rng.uniform(0.1, 20.0))


def generate_weather_row(rng: np.random.Generator, risk_bias: str = "neutral") -> dict:
    """Generate one row of weather-related features."""
    return {
        "weather_severity": generate_weather_severity(rng, risk_bias),
        "visibility_km": generate_visibility_km(rng, risk_bias),
    }
