"""
Dataset schema for Offline Trekking Safety AI.

Defines feature names, types, ranges, and risk levels used across
simulation, training, and prediction. Single source of truth for the project.
"""

# --- Feature names (input to model) ---
FEATURE_COLUMNS = [
    "slope_angle",       # degrees, 0-45
    "altitude_change",   # meters, typically -500 to +500
    "weather_severity",  # 1-5 scale
    "trail_difficulty",  # 1-5 scale
    "path_width_m",      # meters
    "visibility_km",     # kilometers
]

# --- Target label ---
TARGET_COLUMN = "risk_level"

# --- Risk classes (explainable output) ---
RISK_LEVELS = ["Safe", "Moderate_Risk", "High_Risk"]

# --- Valid ranges for synthetic generation and validation ---
FEATURE_RANGES = {
    "slope_angle": (0.0, 45.0),
    "altitude_change": (-500.0, 500.0),
    "weather_severity": (1, 5),
    "trail_difficulty": (1, 5),
    "path_width_m": (0.5, 5.0),
    "visibility_km": (0.1, 20.0),
}

# --- Output paths ---
RAW_DATA_DIR = "data/raw"
PROCESSED_DATA_DIR = "data/processed"
MODEL_DIR = "model"
DEFAULT_MODEL_FILENAME = "risk_model.pkl"
