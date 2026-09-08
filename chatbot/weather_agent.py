
from weather import get_weather


def weather_response(
    latitude,
    longitude
):

    weather = get_weather(
        latitude,
        longitude
    )

    if not weather:

        return "Weather data unavailable."

    forecast_text = ""

    for i in range(
        min(
            3,
            len(weather["forecast_dates"])
        )
    ):

        rain = weather["forecast_rain"][i]

        if rain >= 100:
            risk = "High Risk 🔴"

        elif rain >= 50:
            risk = "Moderate Risk 🟠"

        else:
            risk = "Low Risk 🟢"

        forecast_text += (
            f"\n📅 {weather['forecast_dates'][i]}"
            f"\nRainfall: {rain} mm"
            f"\nRisk: {risk}\n"
        )

    return f"""
    
🌈 Current Weather

Temperature: {weather['temperature']} °C

Humidity: {weather['humidity']} %

Rainfall: {weather['rain']} mm

Wind Speed: {weather['wind_speed']} km/h


📈 Next 3 Days Forecast

{forecast_text}


⚠️ Forecast risk is estimated using expected rainfall.
"""

