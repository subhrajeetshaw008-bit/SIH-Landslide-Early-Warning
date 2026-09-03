from weather import get_weather
from terrain import get_terrain

from utils.predict import (
    predict_risk
)


def risk_response(
    latitude,
    longitude
):

    weather = get_weather(
        latitude,
        longitude
    )

    terrain = get_terrain(
        latitude,
        longitude
    )

    if not weather or not terrain:

        return "Unable to calculate risk."

    risk = predict_risk(
        weather["temperature"],
        weather["humidity"],
        weather["rain"],
        terrain["elevation"]
    )

    return f"""
⚠️ Landslide Risk Analysis

Risk Score: {risk} %

Elevation: {terrain['elevation']} m

Temperature: {weather['temperature']} °C

Humidity: {weather['humidity']} %

Rainfall: {weather['rain']} mm
"""