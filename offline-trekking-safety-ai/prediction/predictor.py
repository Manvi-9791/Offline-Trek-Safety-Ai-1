"""
Risk prediction for trekking segments (offline).

Loads the trained model from model/ and predicts risk level
(Safe / Moderate_Risk / High_Risk) for a given feature vector.
"""

import os
import sys
import pickle

# Project root
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from config.schema import FEATURE_COLUMNS, MODEL_DIR, DEFAULT_MODEL_FILENAME


def load_model():
    """Load saved model and metadata."""
    path = os.path.join(PROJECT_ROOT, MODEL_DIR, DEFAULT_MODEL_FILENAME)
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Model not found at {path}. Run training/train_model.py first.")
    with open(path, "rb") as f:
        return pickle.load(f)


def predict_risk(features: dict) -> tuple:
    """
    Predict risk level for one segment.
    features: dict with keys in FEATURE_COLUMNS (slope_angle, altitude_change, etc.)
    Returns (risk_level_str, confidence_dict or None if not available).
    """
    payload = load_model()
    model = payload["model"]
    feats = payload["features"]
    X = [[features[k] for k in feats]]
    risk = model.predict(X)[0]
    # Probabilities for explainability
    if hasattr(model, "predict_proba"):
        probs = model.predict_proba(X)[0]
        classes = model.classes_
        confidence = dict(zip(classes, probs))
        return risk, confidence
    return risk, None


def predict_risk_simple(slope_angle, altitude_change, weather_severity,
                        trail_difficulty, path_width_m, visibility_km) -> str:
    """
    Convenience: predict from positional args in schema order.
    Returns risk level string.
    """
    features = {
        "slope_angle": slope_angle,
        "altitude_change": altitude_change,
        "weather_severity": weather_severity,
        "trail_difficulty": trail_difficulty,
        "path_width_m": path_width_m,
        "visibility_km": visibility_km,
    }
    risk, _ = predict_risk(features)
    return risk
