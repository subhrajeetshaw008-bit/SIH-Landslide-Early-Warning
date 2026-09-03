import joblib


model = joblib.load(
    "landslide_baseline_model.pkl"
)


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
