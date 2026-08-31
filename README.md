# 🏔️ Landslide Risk Predictor

AI/ML-based landslide susceptibility prediction system for Northeast India.

## Current Features

- 📍 Location-based analysis
- 🗺️ Interactive map
- 🌦️ Current weather
- 🏔️ DEM-based elevation
- ⛰️ Terrain slope
- 🤖 Machine-learning prediction
- ⚠️ Risk classification
- 🛡️ Safety recommendations

## Baseline ML Model

The current model uses:

- Latitude
- Longitude
- Elevation
- Slope

Baseline results:

- Accuracy: 93.12%
- ROC-AUC: 0.9734

## Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py