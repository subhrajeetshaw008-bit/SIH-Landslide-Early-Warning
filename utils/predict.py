import joblib
from pathlib import Path
import streamlit as st


MODEL_PATH = Path(__file__).resolve().parents[1] / "models" / "landslide_model.pkl"

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

    prediction = model.predict_proba(
        [[
            temperature,
            humidity,
            rainfall,
            elevation
        ]]
    )

    return round(
        prediction[0][1] * 100,
        2
    )
