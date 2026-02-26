"""
Train risk classification model (Decision Tree or Random Forest).

Reads processed data from data/processed/ (or raw from data/raw/),
trains a lightweight classifier, and saves it to model/ for offline use.

Run from project root:
    python training/train_model.py
"""

import os
import sys
import pickle
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

# Project root
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from config.schema import (
    FEATURE_COLUMNS,
    TARGET_COLUMN,
    RAW_DATA_DIR,
    PROCESSED_DATA_DIR,
    MODEL_DIR,
    DEFAULT_MODEL_FILENAME,
)


def load_data(use_processed: bool = False) -> pd.DataFrame:
    """Load dataset from processed or raw folder."""
    if use_processed:
        path = os.path.join(PROJECT_ROOT, PROCESSED_DATA_DIR, "trekking_processed.csv")
    else:
        path = os.path.join(PROJECT_ROOT, RAW_DATA_DIR, "trekking_synthetic.csv")
    if not os.path.isfile(path):
        raise FileNotFoundError(
            "Dataset not found. Run scripts/generate_dataset.py first."
        )
    return pd.read_csv(path)


def train_and_save(
    df: pd.DataFrame,
    model_type: str = "random_forest",
    test_size: float = 0.2,
    random_state: int = 42,
) -> None:
    """
    Train classifier and save to model/.
    model_type: 'random_forest' or 'decision_tree'
    """
    X = df[FEATURE_COLUMNS]
    y = df[TARGET_COLUMN]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    if model_type == "decision_tree":
        clf = DecisionTreeClassifier(random_state=random_state, max_depth=10)
    else:
        clf = RandomForestClassifier(
            n_estimators=50, random_state=random_state, max_depth=10
        )
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    print("Test set accuracy:", accuracy_score(y_test, y_pred))
    print(classification_report(y_test, y_pred))
    out_dir = os.path.join(PROJECT_ROOT, MODEL_DIR)
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, DEFAULT_MODEL_FILENAME)
    with open(out_path, "wb") as f:
        pickle.dump(
            {"model": clf, "features": FEATURE_COLUMNS, "target": TARGET_COLUMN}, f
        )
    print("Model saved to", out_path)


def main():
    df = load_data(use_processed=False)
    train_and_save(df, model_type="random_forest")


if __name__ == "__main__":
    main()
