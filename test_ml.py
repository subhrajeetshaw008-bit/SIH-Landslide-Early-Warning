import joblib

# Load trained model
model = joblib.load("landslide_ml_model.pkl")

# Test conditions
rainfall = 400
slope = 45
soil_moisture = 80
vegetation = 10
river_distance = 50

# Make prediction
prediction = model.predict([[
    rainfall,
    slope,
    soil_moisture,
    vegetation,
    river_distance
]])

print("🤖 ML Prediction")
print("----------------")
print("Predicted Risk Score:", round(prediction[0], 2))