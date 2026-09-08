"""
Landslide risk model training script.

NOTE ON DATA: This uses a domain-informed SYNTHETIC dataset (not real
historical landslide records). The relationships between rainfall,
humidity, temperature, elevation and risk are modeled using published
landslide-triggering factors (rainfall intensity/saturation is the
dominant driver, followed by humidity and terrain elevation), with
randomness added so the data is not perfectly separable.

For a production/next-round version, replace `generate_synthetic_dataset()`
with real records (e.g. GSI Bhukosh landslide inventory, or a labeled
Kaggle landslide susceptibility dataset) loaded via pandas.read_csv().
"""

import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import train_test_split

RANDOM_SEED = 42
N_SAMPLES = 1200


def generate_synthetic_dataset(n_samples=N_SAMPLES, seed=RANDOM_SEED):
    """Generate a realistic, noisy synthetic dataset for prototyping."""
    rng = np.random.default_rng(seed)

    temperature = rng.uniform(10, 40, n_samples)             # deg C
    humidity = rng.uniform(30, 100, n_samples)                # %
    rainfall = rng.gamma(shape=2.0, scale=20.0, size=n_samples)  # mm, right-skewed
    elevation = rng.uniform(50, 2000, n_samples)               # meters

    # Normalize features to comparable 0-1 ranges for the risk function
    rainfall_n = np.clip(rainfall / 150.0, 0, 1)
    humidity_n = (humidity - 30) / 70.0
    elevation_n = (elevation - 50) / 1950.0
    temperature_n = (temperature - 10) / 30.0

    # Domain-informed weighting: rainfall dominant, then humidity/saturation,
    # elevation and temperature as secondary contributors.
    linear_score = (
        -3.0
        + 4.2 * rainfall_n
        + 1.6 * humidity_n
        + 1.0 * elevation_n
        + 0.4 * temperature_n
    )

    # Add noise so classes aren't perfectly separable (realistic uncertainty)
    noise = rng.normal(0, 0.6, n_samples)
    probability = 1 / (1 + np.exp(-(linear_score + noise)))

    # Sample binary labels from the probability (not a hard threshold)
    risk = rng.binomial(1, probability)

    df = pd.DataFrame({
        "temperature": np.round(temperature, 1),
        "humidity": np.round(humidity, 1),
        "rainfall": np.round(rainfall, 1),
        "elevation": np.round(elevation, 1),
        "risk": risk,
    })
    return df


def train_and_evaluate(df):
    X = df[["temperature", "humidity", "rainfall", "elevation"]]
    y = df["risk"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_SEED, stratify=y
    )

    candidates = {
        "RandomForest": RandomForestClassifier(
            n_estimators=200, max_depth=8, random_state=RANDOM_SEED
        ),
        "LogisticRegression": LogisticRegression(max_iter=1000),
    }

    results = {}
    for name, model in candidates.items():
        model.fit(X_train, y_train)
        preds = model.predict(X_test)

        results[name] = {
            "model": model,
            "accuracy": accuracy_score(y_test, preds),
            "precision": precision_score(y_test, preds),
            "recall": recall_score(y_test, preds),
            "f1": f1_score(y_test, preds),
            "confusion_matrix": confusion_matrix(y_test, preds).tolist(),
        }

        print(f"\n=== {name} ===")
        print(classification_report(y_test, preds, target_names=["No Risk", "Risk"]))

    best_name = max(results, key=lambda n: results[n]["f1"])
    best_model = results[best_name]["model"]
    print(f"\n>>> Selected model: {best_name} (highest F1 on held-out test set)")

    return best_name, best_model, results


def save_artifacts(best_name, best_model, results):
    model_dir = Path(__file__).resolve().parent / "models"
    model_dir.mkdir(exist_ok=True)

    joblib.dump(best_model, model_dir / "landslide_model.pkl")

    # Save metrics separately so the dashboard/report pages (or a slide deck)
    # can display real numbers instead of hardcoding claims.
    metrics_to_save = {
        name: {k: v for k, v in r.items() if k != "model"}
        for name, r in results.items()
    }
    with open(model_dir / "model_metrics.json", "w") as f:
        json.dump({
            "selected_model": best_name,
            "features": ["temperature", "humidity", "rainfall", "elevation"],
            "training_samples": N_SAMPLES,
            "data_source": "synthetic (domain-informed) - see train_model.py docstring",
            "results": metrics_to_save,
        }, f, indent=2)

    print(f"\nModel saved to {model_dir / 'landslide_model.pkl'}")
    print(f"Metrics saved to {model_dir / 'model_metrics.json'}")


if __name__ == "__main__":
    dataset = generate_synthetic_dataset()
    print(f"Generated {len(dataset)} synthetic samples")
    print(f"Class balance -> Risk=1: {dataset['risk'].mean():.2%}, Risk=0: {1 - dataset['risk'].mean():.2%}")

    best_name, best_model, results = train_and_evaluate(dataset)
    save_artifacts(best_name, best_model, results)