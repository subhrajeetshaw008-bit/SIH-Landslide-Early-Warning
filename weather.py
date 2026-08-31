import requests


def get_weather(latitude, longitude):
    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={latitude}"
        f"&longitude={longitude}"
        "&current=temperature_2m,rain"
    )

    response = requests.get(url, timeout=10)

    if response.status_code != 200:
        return None

    data = response.json()

    return {
        "temperature": data["current"]["temperature_2m"],
        "rain": data["current"]["rain"]
    }

if __name__ == "__main__":

    weather = get_weather(22.05, 88.10)

    print("🌦️ Weather Data")
    print("----------------")

    if weather:
        print("Temperature:", weather["temperature"], "°C")
        print("Rain:", weather["rain"], "mm")
    else:
        print("❌ Could not fetch weather data")