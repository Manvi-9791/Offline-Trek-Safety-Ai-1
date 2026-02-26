# Dataset Schema: Trekking Safety AI

Single source of truth for features and labels is `config/schema.py`. This document summarizes the schema for reports and documentation.

---

## Feature Columns (Inputs)

| Column             | Type   | Range / Values | Description |
|--------------------|--------|----------------|-------------|
| `slope_angle`      | float  | 0–45           | Terrain slope in degrees |
| `altitude_change`  | float  | -500 to +500   | Net altitude change in meters |
| `weather_severity` | int    | 1–5            | 1=clear, 5=storm/heavy fog |
| `trail_difficulty` | int    | 1–5            | 1=easy, 5=expert only |
| `path_width_m`     | float  | 0.5–5.0        | Path width in meters |
| `visibility_km`    | float  | 0.1–20.0       | Visibility in kilometers |

---

## Target Column (Output)

| Column        | Type | Values | Description |
|---------------|------|--------|-------------|
| `risk_level`  | str  | `Safe`, `Moderate_Risk`, `High_Risk` | Risk classification for the segment |

---

## Usage

- **Synthetic data**: `simulation/` generates these features; `scripts/generate_dataset.py` produces CSV with these columns.
- **Training**: `training/train_model.py` uses `FEATURE_COLUMNS` and `TARGET_COLUMN` from `config/schema.py`.
- **Prediction**: `prediction/predictor.py` expects a dict with the same feature keys.
