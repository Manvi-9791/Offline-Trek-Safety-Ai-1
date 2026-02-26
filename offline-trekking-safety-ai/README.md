# Offline Trekking Safety AI using Simulation and Synthetic Data

A B.Tech level AI project that helps trekkers navigate safely in areas with no internet. The system predicts risky routes, detects danger zones, and suggests safer paths using pre-downloaded data and GPS.

---

## Project Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     OFFLINE TREKKING SAFETY AI                           │
├─────────────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │   data/      │  │ simulation/  │  │   model/     │  │  training/   │  │
│  │ Preloaded    │  │ Terrain &    │  │ Trained      │  │ Train ML     │  │
│  │ route data   │  │ env params   │  │ .pkl model   │  │ (RF/DT)      │  │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  │
│         │                 │                 │                 │          │
│         └─────────────────┴────────┬────────┴─────────────────┘          │
│                                    ▼                                      │
│  ┌─────────────────────────────────────────────────────────────────────┐  │
│  │                     prediction/                                      │  │
│  │  Risk classification (Safe / Moderate Risk / High Risk)              │  │
│  │  Alternate route suggestion, danger zone detection                   │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
│                                    │                                      │
│  ┌─────────────────────────────────┴───────────────────────────────────┐  │
│  │  app_interface/  │  maps/  │  (Future: Flutter app, offline maps)   │  │
│  │  CLI for testing │  Geo data for routes                              │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────┘
```

## Folder Structure

```
offline-trekking-safety-ai/
├── data/                 # Preloaded & generated datasets
│   ├── raw/               # Raw synthetic data (CSV)
│   └── processed/         # Cleaned data for training
├── simulation/            # Simulated trekking environment
│   ├── __init__.py
│   ├── terrain_simulator.py
│   └── weather_simulator.py
├── model/                 # Saved trained models
│   └── .gitkeep
├── training/              # Model training scripts
│   ├── __init__.py
│   └── train_model.py
├── prediction/            # Risk prediction logic
│   ├── __init__.py
│   └── predictor.py
├── maps/                  # Offline map / route data (future)
│   └── .gitkeep
├── app_interface/         # CLI and future app hooks
│   ├── __init__.py
│   └── cli.py
├── config/                # Schema and configuration
│   ├── __init__.py
│   └── schema.py
├── scripts/               # Dataset generation entry point
│   ├── __init__.py
│   └── generate_dataset.py
├── requirements.txt
├── README.md
└── ARCHITECTURE.md
```

## Dataset Schema

See `config/schema.py` and `ARCHITECTURE.md` for full field definitions.

| Feature            | Type   | Description                    |
|--------------------|--------|--------------------------------|
| slope_angle        | float  | Terrain slope (degrees)       |
| altitude_change    | float  | Altitude delta (m)             |
| weather_severity   | int    | 1–5 scale                      |
| trail_difficulty   | int    | 1–5 scale                      |
| path_width_m       | float  | Path width in meters           |
| visibility_km      | float  | Visibility in km               |
| risk_level         | str    | Safe / Moderate_Risk / High_Risk |

## Quick Start

1. **Create virtual environment (recommended)**
   ```bash
   python -m venv venv
   venv\Scripts\activate   # Windows
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Generate synthetic dataset**
   ```bash
   python scripts/generate_dataset.py
   ```

4. **Train the model**
   ```bash
   python training/train_model.py
   ```

5. **Test predictions via CLI**
   ```bash
   python app_interface/cli.py
   ```

## Future Scope (Structure Only)

- **Mobile app**: Flutter integration (app_interface/ will expose APIs)
- **Offline maps**: maps/ for tile or vector data
- **GPS real-time alerts**: prediction/ will consume lat/lon and trigger alerts

## License

Educational use — B.Tech project.
