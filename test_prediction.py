import joblib
import pandas as pd


# Load model
model = joblib.load(
    "landslide_baseline_model.pkl"
)


print("===================================")
print("LANDSLIDE ML TEST")
print("===================================")


# Example test location
latitude = 24.5
longitude = 93.5
elevation = 900
slope = 30


# Create input
data = pd.DataFrame([
    {
        "Latitude": latitude,
        "Longitude": longitude,
        "Elevation_m": elevation,
        "Slope_degrees": slope
    }
])


# Predict probability
probability = model.predict_proba(
    data
)[0][1]


risk_score = probability * 100


# Risk level
if risk_score >= 75:
    risk = "HIGH"
elif risk_score >= 50:
    risk = "MODERATE"
else:
    risk = "LOW"


print("\nLocation:")
print("Latitude:", latitude)
print("Longitude:", longitude)

print("\nTerrain:")
print("Elevation:", elevation, "m")
print("Slope:", slope, "degrees")

print("\n===================================")
print("ML PREDICTION")
print("===================================")

print(
    f"Risk probability: {risk_score:.2f}%"
)

print(
    "Risk level:",
    risk
)