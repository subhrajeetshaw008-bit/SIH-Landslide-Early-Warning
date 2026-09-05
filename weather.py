import requests
import streamlit as st


@st.cache_data(ttl=300, show_spinner=False)
def get_weather(latitude, longitude):

    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={latitude}"
        f"&longitude={longitude}"
        "&current=temperature_2m,relative_humidity_2m,rain,wind_speed_10m"
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
            "wind_speed": current["wind_speed_10m"]
        }

    except Exception as e:

        print(e)

        return None
