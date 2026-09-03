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

    return f"""
🌦️ Current Weather

Temperature: {weather['temperature']} °C

Humidity: {weather['humidity']} %

Rainfall: {weather['rain']} mm

Wind Speed: {weather['wind_speed']} km/h
"""