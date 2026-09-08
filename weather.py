import requests
import streamlit as st


@st.cache_data(ttl=300, show_spinner=False)
def get_weather(latitude, longitude):

    url = (
    "https://api.open-meteo.com/v1/forecast"
    f"?latitude={latitude}"
    f"&longitude={longitude}"
    "&current=temperature_2m,relative_humidity_2m,rain,wind_speed_10m"
    "&daily=temperature_2m_max,temperature_2m_min,precipitation_sum"
    "&timezone=auto"
    )

    try:

        response = requests.get(url, timeout=(3, 6))
        response.raise_for_status()

        data = response.json()

        current = data["current"]

        return {
    "temperature": current["temperature_2m"],
    "humidity": current["relative_humidity_2m"],
    "rain": current["rain"],
    "wind_speed": current["wind_speed_10m"],

    "forecast_dates": data["daily"]["time"],
    "forecast_rain": data["daily"]["precipitation_sum"],
    "forecast_temp_max": data["daily"]["temperature_2m_max"],
    "forecast_temp_min": data["daily"]["temperature_2m_min"]
        }

    except Exception as e:

        print(e)

        return None
