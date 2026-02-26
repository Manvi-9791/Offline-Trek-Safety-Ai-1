"""
Trek Safety AI - FastAPI backend.

Serves the trained risk model via POST /predict and POST /predict-by-location.
Run from project root: uvicorn backend.app:app --reload
"""

import hashlib
import os
import sys
from typing import List

import numpy as np

# Project root is parent of backend/ (so model/ and prediction/ are found)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# Import existing prediction and explanation logic (no model retrain)
from config.schema import FEATURE_RANGES
from prediction.predictor import predict_risk
from app_interface.cli import explain_risk

app = FastAPI(title="Trek Safety AI", description="Predict trekking risk from route features or location")

# Allow frontend (e.g. file:// or http://localhost:5500) to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Request/Response models ---

class PredictRequest(BaseModel):
    slope_angle: float
    altitude_change: float
    weather_severity: int
    trail_difficulty: int
    path_width_m: float
    visibility_km: float


class PredictByLocationRequest(BaseModel):
    location: str


class PredictResponse(BaseModel):
    risk_level: str
    confidence: dict
    reasons: List[str]


def _features_from_location(location: str) -> dict:
    """
    Derive route features from a location string (offline, deterministic).
    Same location always yields the same features so risk is consistent.
    Uses hash of location to seed RNG and sample within schema ranges.
    """
    raw = (location or "").strip() or "Unknown"
    seed = int(hashlib.sha256(raw.encode("utf-8")).hexdigest()[:12], 16)
    rng = np.random.default_rng(seed)

    def sample(name: str) -> float:
        lo, hi = FEATURE_RANGES[name]
        if isinstance(lo, int) and isinstance(hi, int):
            return float(rng.integers(lo, hi + 1))
        return float(rng.uniform(lo, hi))

    return {
        "slope_angle": sample("slope_angle"),
        "altitude_change": sample("altitude_change"),
        "weather_severity": int(sample("weather_severity")),
        "trail_difficulty": int(sample("trail_difficulty")),
        "path_width_m": sample("path_width_m"),
        "visibility_km": sample("visibility_km"),
    }


# Serve frontend so one server can run both API and website (open http://127.0.0.1:8000/app/)
FRONTEND_DIR = os.path.join(PROJECT_ROOT, "frontend")
if os.path.isdir(FRONTEND_DIR):
    app.mount("/app", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")


@app.get("/")
def root():
    """Health check. Web UI: /app/ """
    return {"service": "Trek Safety AI", "docs": "/docs", "predict": "POST /predict", "predict_by_location": "POST /predict-by-location", "app": "/app/"}


@app.post("/predict-by-location", response_model=PredictResponse)
def predict_by_location(payload: PredictByLocationRequest):
    """
    Predict trekking risk from a location (place name or coordinates).
    Features are derived offline from the location; same location gives same result.
    """
    features = _features_from_location(payload.location)
    try:
        risk_level, confidence = predict_risk(features)
        reasons = explain_risk(features)
        if not reasons:
            reasons = ["Route conditions are generally safe."]
        confidence_serializable = {k: float(v) for k, v in (confidence or {}).items()}
        return PredictResponse(
            risk_level=risk_level,
            confidence=confidence_serializable,
            reasons=reasons,
        )
    except FileNotFoundError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/predict", response_model=PredictResponse)
def predict(payload: PredictRequest):
    """
    Predict trekking risk from route features.
    Returns risk_level (Safe / Moderate_Risk / High_Risk), confidence scores, and reasons.
    """
    features = {
        "slope_angle": payload.slope_angle,
        "altitude_change": payload.altitude_change,
        "weather_severity": payload.weather_severity,
        "trail_difficulty": payload.trail_difficulty,
        "path_width_m": payload.path_width_m,
        "visibility_km": payload.visibility_km,
    }
    try:
        risk_level, confidence = predict_risk(features)
        # Explainable AI: rule-based reasons from same features
        reasons = explain_risk(features)
        if not reasons:
            reasons = ["Route conditions are generally safe."]
        # Convert numpy floats in confidence to Python floats for JSON
        confidence_serializable = {k: float(v) for k, v in (confidence or {}).items()}
        return PredictResponse(
            risk_level=risk_level,
            confidence=confidence_serializable,
            reasons=reasons,
        )
    except FileNotFoundError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
