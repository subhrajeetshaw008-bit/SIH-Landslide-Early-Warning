import joblib
import pandas as pd
from pathlib import Path
import streamlit as st


MODEL_PATH = Path(__file__).resolve().parents[1] / "models" / "landslide_model.pkl"
FEATURE_COLUMNS = ["temperature", "humidity", "rainfall", "elevation"]

@st.cache_resource(show_spinner=False)
def load_model():
    return joblib.load(MODEL_PATH)


model = load_model()


def predict_risk(
    temperature,
    humidity,
    rainfall,
    elevation
):

    # Pass a DataFrame with the same column names used in training
    # (train_model.py) so scikit-learn matches features by name, not
    # just position. This avoids silent bugs if the feature order ever
    # changes and removes the "X does not have valid feature names" warning.
    features = pd.DataFrame(
        [[temperature, humidity, rainfall, elevation]],
        columns=FEATURE_COLUMNS
    )

    prediction = model.predict_proba(features)

    return round(
        prediction[0][1] * 100,
        2
    )