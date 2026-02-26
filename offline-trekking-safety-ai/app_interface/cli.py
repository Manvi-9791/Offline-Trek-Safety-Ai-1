"""
Simple CLI to test risk predictions.

Prompts for segment features (or uses defaults) and prints predicted risk level
plus Explainable AI (XAI) reasoning in human-readable terms.
Run from project root:
    python app_interface/cli.py
"""

import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from config.schema import FEATURE_COLUMNS, FEATURE_RANGES


def explain_risk(features: dict) -> list:
    """
    Generate rule-based explanations for why a route may be risky.
    Uses only the input feature values (no model internals).
    Returns a list of explanation strings; empty if no major risk factors.
    """
    reasons = []
    # Steep terrain: slope > 25 degrees is a common threshold for increased fall risk
    if features.get("slope_angle", 0) > 25:
        reasons.append("Steep slope increases fall risk")
    # Severe weather: schema is 1-5; 4 or 5 (or invalid >= 6) treated as severe
    if features.get("weather_severity", 0) >= 4:
        reasons.append("Severe weather increases danger")
    # Low visibility makes it harder to see obstacles and path
    if features.get("visibility_km", 20) < 4:
        reasons.append("Low visibility reduces path safety")
    # Narrow path leaves less room for error and passing
    if features.get("path_width_m", 5) < 1.5:
        reasons.append("Narrow trail increases risk")
    # High difficulty rating means the trail demands more experience
    if features.get("trail_difficulty", 0) >= 4:
        reasons.append("Difficult trail requires higher skill level")
    return reasons


def parse_float(s: str, default: float) -> float:
    try:
        return float(s.strip()) if s.strip() else default
    except ValueError:
        return default


def parse_int(s: str, default: int) -> int:
    try:
        return int(s.strip()) if s.strip() else default
    except ValueError:
        return default


def main():
    print("--- Offline Trekking Safety AI - Risk Prediction ---")
    print("Enter segment features (or press Enter for default).\n")
    # Default: moderate segment
    defaults = {
        "slope_angle": 12.0,
        "altitude_change": 80.0,
        "weather_severity": 2,
        "trail_difficulty": 2,
        "path_width_m": 2.0,
        "visibility_km": 8.0,
    }
    features = {}
    for col in FEATURE_COLUMNS:
        low, high = FEATURE_RANGES[col]
        d = defaults.get(col, low)
        prompt = f"  {col} [{low}-{high}] (default {d}): "
        raw = input(prompt)
        if col in ("weather_severity", "trail_difficulty"):
            features[col] = parse_int(raw, d)
        else:
            features[col] = parse_float(raw, d)
    try:
        from prediction.predictor import predict_risk
        risk, confidence = predict_risk(features)
        # --- XAI: explain why this risk level was predicted ---
        reasons = explain_risk(features)
        print("\n-----------------------------------")
        print(f"Predicted Risk Level: {risk}")
        if confidence:
            print("Confidence:")
            for level, prob in confidence.items():
                print(f"  {level}: {prob:.2f}")
        print("\nReasoning:")
        if reasons:
            for r in reasons:
                print(f"- {r}")
        else:
            print("- Route conditions are generally safe.")
        print("-----------------------------------")
    except FileNotFoundError as e:
        print(f"\nError: {e}")
        print("Run: python scripts/generate_dataset.py")
        print("Then: python training/train_model.py")
        sys.exit(1)


if __name__ == "__main__":
    main()
