import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import joblib


# Create training data
np.random.seed(42)

data = []

for _ in range(2000):

    rainfall = np.random.uniform(0, 500)
    slope = np.random.uniform(0, 60)
    soil_moisture = np.random.uniform(0, 100)
    vegetation = np.random.uniform(0, 100)
    river_distance = np.random.uniform(0, 1000)

    score = 0

    # Rainfall contribution
    if rainfall > 300:
        score += 30
    elif rainfall > 200:
        score += 20
    elif rainfall > 100:
        score += 10

    # Slope contribution
    if slope > 40:
        score += 25
    elif slope > 30:
        score += 15
    elif slope > 20:
        score += 10

    # Soil moisture contribution
    if soil_moisture > 70:
        score += 20
    elif soil_moisture > 50:
        score += 10

    # Vegetation contribution
    if vegetation < 20:
        score += 15
    elif vegetation < 40:
        score += 10

    # River distance contribution
    if river_distance < 100:
        score += 10

    score = min(score, 100)

    data.append([
        rainfall,
        slope,
        soil_moisture,
        vegetation,
        river_distance,
        score
    ])


data = np.array(data)

X = data[:, :5]
y = data[:, 5]


# Split training and testing data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


# Create ML model
model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)


# Train model
model.fit(X_train, y_train)


# Test model
predictions = model.predict(X_test)

mae = mean_absolute_error(y_test, predictions)

print("ML model trained successfully!")
print("Mean Absolute Error:", round(mae, 2))


# Save model
joblib.dump(model, "landslide_ml_model.pkl")

print("Model saved as landslide_ml_model.pkl")