# Trek Safety AI – Web app run instructions

## Folder structure

```
offline-trekking-safety-ai/
├── backend/
│   └── app.py          # FastAPI server, loads model/risk_model.pkl, POST /predict
├── frontend/
│   ├── index.html      # Form + result area
│   ├── styles.css      # Trekking theme, Safe=green, Moderate=yellow, High=red
│   └── app.js          # fetch() to backend, display result without reload
├── model/
│   └── risk_model.pkl  # Must exist (run training first if needed)
└── ...
```

## 1. Install dependencies

From the **project root** (`offline-trekking-safety-ai`):

```bash
pip install -r requirements.txt
```

This installs FastAPI and Uvicorn in addition to the existing ML stack.

## 2. Train the model (if you don’t have it yet)

```bash
python scripts/generate_dataset.py
python training/train_model.py
```

This creates `model/risk_model.pkl`.

## 3. Start the backend

From the **project root**:

```bash
uvicorn backend.app:app --reload --host 127.0.0.1 --port 8000
```

- API: http://127.0.0.1:8000  
- Interactive docs: http://127.0.0.1:8000/docs  
- The backend loads the model and serves `POST /predict`.

## 4. Open the website

The frontend is plain HTML/CSS/JS. You can:

**Option A – Single server (easiest)**  
The backend serves the frontend at `/app/`. With the backend running, open **http://127.0.0.1:8000/app/** — no separate frontend server needed.

**Option B – Local server (separate)**  
Serve the frontend folder with any static server so the page is loaded over HTTP (avoids CORS issues with `file://`):

```bash
cd frontend
python -m http.server 5500
```

Then open: **http://127.0.0.1:5500**

**Option C – Open file**  
Open `frontend/index.html` directly in the browser (file://). If the backend runs on 127.0.0.1:8000, some browsers may still allow the request; if you see “Could not reach the server”, use Option A.

## 5. Use the app

1. Enter or adjust the six route fields (slope, altitude change, weather, etc.).  
2. Click **Check Trek Safety**.  
3. The app calls the backend and shows **risk level** (green / yellow / red), **confidence**, and **reasoning** in the result area, without reloading the page.

## Integration summary

- **Backend** (`backend/app.py`): Adds project root to `sys.path`, imports `prediction.predictor` and `app_interface.cli.explain_risk`, exposes `POST /predict` with JSON in/out and CORS enabled.  
- **Frontend**: Form sends the six feature values as JSON to `http://127.0.0.1:8000/predict`; `app.js` uses `fetch()`, then fills the result section with the returned `risk_level`, `confidence`, and `reasons`.
