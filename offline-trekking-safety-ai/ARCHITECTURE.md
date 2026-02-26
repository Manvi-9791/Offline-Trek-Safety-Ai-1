# Architecture: Offline Trekking Safety AI

## 1. System Overview

The system is designed for **offline-first** operation: all AI inference and route logic run on-device using pre-downloaded data. No server or internet is required after initial setup.

### Design Principles

- **Modular**: Each component (simulation, training, prediction, app_interface) can be developed and tested independently.
- **Explainable**: Decision Tree / Random Forest give interpretable rules (e.g. "if slope > 25° then High Risk").
- **Lightweight**: No deep learning; small `.pkl` model suitable for mobile/embedded later.

---

## 2. Dataset Schema (Simulation Output)

Simulated trekking segments are described by the following features. Risk level is the target label.

| Field             | Type   | Range / Values      | Description |
|-------------------|--------|----------------------|-------------|
| `slope_angle`     | float  | 0–45 (degrees)       | Average slope of the segment |
| `altitude_change` | float  | -500 to +500 (m)     | Net altitude change over segment |
| `weather_severity`| int    | 1–5                  | 1=clear, 5=storm/heavy fog |
| `trail_difficulty`| int    | 1–5                  | 1=easy, 5=expert only |
| `path_width_m`    | float  | 0.5–5.0 (m)          | Effective path width |
| `visibility_km`   | float  | 0.1–20.0 (km)        | Visibility (fog/rain) |
| `risk_level`      | str    | Safe, Moderate_Risk, High_Risk | Target label |

### Risk Level Rules (for synthetic data)

- **Safe**: Low slope, good visibility, mild weather, wider path.
- **Moderate_Risk**: Medium slope or weather, moderate visibility/path.
- **High_Risk**: Steep slope, poor visibility, severe weather, narrow path.

These rules are implemented in the synthetic data generator so the ML model can learn them.

---

## 3. Component Responsibilities

| Component      | Responsibility |
|----------------|----------------|
| **simulation/**| Generate realistic terrain & weather parameters (slope, altitude, weather, path width, visibility). |
| **data/**      | Store raw and processed CSV; hold preloaded route data for offline use. |
| **training/** | Load processed data, train Decision Tree or Random Forest, save model to `model/`. |
| **prediction/**| Load saved model, accept feature vector, return risk class + optional confidence. |
| **app_interface/** | CLI to input segment features and get risk; future: Flutter/API layer. |
| **maps/**      | Reserved for offline map tiles or route geometries (future). |

---

## 4. Data Flow

1. **Offline preparation**
   - Simulation → synthetic CSV → `data/raw/`
   - Preprocessing (if any) → `data/processed/`
   - Training script reads processed data → trains model → saves to `model/`

2. **At trek time (offline)**
   - App gets current segment features (from GPS + preloaded route DB or simulation).
   - Prediction module loads `model/risk_model.pkl` and returns risk level.
   - If High Risk: suggest alternate from preloaded routes; emergency mode can store last known location for SOS.

---

## 5. Future Scope (Structure Only)

- **Mobile (Flutter)**: `app_interface/` will expose a clear API (e.g. `get_risk(features_dict)`, `get_alternate_routes()`).
- **Offline maps**: `maps/` will store tiles or vector data; no implementation in initial version.
- **GPS real-time alerts**: Prediction module will be called with (lat, lon) → lookup segment → return risk and trigger alerts.

No code for Flutter, maps, or GPS is required in the initial deliverable; only the folder structure and this documentation.
