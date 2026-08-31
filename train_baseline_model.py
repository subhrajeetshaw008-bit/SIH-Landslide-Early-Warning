import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    roc_auc_score
)

import joblib


# ==========================================
# 1. Load dataset
# ==========================================

file = "data/ml_terrain_ready.csv"

df = pd.read_csv(file)

print("Dataset loaded:", len(df))


# ==========================================
# 2. Select features
# ==========================================

features = [
    "Latitude",
    "Longitude",
    "Elevation_m",
    "Slope_degrees"
]

X = df[features]

y = df["Label"]


# ==========================================
# 3. Train/test split
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\nTraining samples:", len(X_train))
print("Testing samples:", len(X_test))


# ==========================================
# 4. Create Random Forest
# ==========================================

model = RandomForestClassifier(
    n_estimators=300,
    max_depth=15,
    min_samples_leaf=3,
    random_state=42,
    n_jobs=-1,
    class_weight="balanced"
)


# ==========================================
# 5. Train
# ==========================================

print("\nTraining model...")

model.fit(
    X_train,
    y_train
)

print("Training complete!")


# ==========================================
# 6. Predictions
# ==========================================

y_pred = model.predict(X_test)

y_probability = model.predict_proba(
    X_test
)[:, 1]


# ==========================================
# 7. Evaluation
# ==========================================

accuracy = accuracy_score(
    y_test,
    y_pred
)

auc = roc_auc_score(
    y_test,
    y_probability
)

print("\n===================================")
print("BASELINE MODEL RESULTS")
print("===================================")

print(
    f"Accuracy: {accuracy:.4f}"
)

print(
    f"ROC-AUC: {auc:.4f}"
)

print("\nClassification Report:")

print(
    classification_report(
        y_test,
        y_pred
    )
)

print("\nConfusion Matrix:")

print(
    confusion_matrix(
        y_test,
        y_pred
    )
)


# ==========================================
# 8. Feature importance
# ==========================================

print("\nFeature Importance:")

importance = pd.Series(
    model.feature_importances_,
    index=features
).sort_values(
    ascending=False
)

print(importance)


# ==========================================
# 9. Save model
# ==========================================

model_file = "landslide_baseline_model.pkl"

joblib.dump(
    model,
    model_file
)

print("\n===================================")
print("MODEL SAVED")
print("===================================")

print(
    "Saved to:",
    model_file
)