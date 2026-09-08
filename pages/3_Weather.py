import streamlit as st
import pandas as pd

from weather import get_weather

st.set_page_config(
	page_title="Landslide AI Weather",
	page_icon="🌦️",
	layout="wide"
)

with open("assets/styles.css") as css_file:
	st.markdown(f"<style>{css_file.read()}</style>", unsafe_allow_html=True)


st.markdown("<div class='weather-shell-anchor'></div>", unsafe_allow_html=True)
st.markdown(
	"""
	<div class="weather-header">
		<div class="main-brand-mark">▲</div>
		<div>
			<div class="assistant-kicker">LANDSLIDE INTELLIGENCE</div>
			<h1>Weather intelligence</h1>
			<p>Live atmospheric conditions for landslide monitoring.</p>
		</div>
	</div>
	""",
	unsafe_allow_html=True
)

st.markdown("<div class='section-kicker'>01 <span>Selected Location</span></div>", unsafe_allow_html=True)
location_column, action_column = st.columns([4, 1])

with location_column:
	latitude, longitude = st.columns(2)
	with latitude:
		selected_latitude = st.number_input(
			"Latitude",
			value=st.session_state.get("latitude", 24.5),
			format="%.4f"
		)
	with longitude:
		selected_longitude = st.number_input(
			"Longitude",
			value=st.session_state.get("longitude", 93.5),
			format="%.4f"
		)

with action_column:
	st.write("")
	st.write("")
	refresh_weather = st.button("Refresh Weather", use_container_width=True)

if refresh_weather:
	get_weather.clear()

st.session_state["latitude"] = selected_latitude
st.session_state["longitude"] = selected_longitude
weather = get_weather(selected_latitude, selected_longitude)

if weather:
	temperature = weather["temperature"]
	humidity = weather["humidity"]
	rainfall = weather["rain"]
	wind_speed = weather["wind_speed"]
	weather_status = "Live data available"
else:
	temperature = humidity = rainfall = wind_speed = None
	weather_status = "Weather service unavailable"

st.markdown("<div class='section-kicker'>02 <span>Current Conditions</span></div>", unsafe_allow_html=True)
temperature_label = f"{temperature} °C" if temperature is not None else "N/A"
humidity_label = f"{humidity}%" if humidity is not None else "N/A"
rainfall_label = f"{rainfall} mm" if rainfall is not None else "N/A"
wind_label = f"{wind_speed} km/h" if wind_speed is not None else "N/A"

metric_columns = st.columns(4)
metrics = [
	("🌡️", "Temperature", temperature_label, "Current air temperature"),
	("💧", "Humidity", humidity_label, "Relative humidity"),
	("☔", "Rainfall", rainfall_label, "Current precipitation"),
	("≋", "Wind speed", wind_label, "Surface wind movement"),
]

for column, (icon, label, value, caption) in zip(metric_columns, metrics):
	with column:
		st.markdown(
			f"""
			<div class='card weather-metric-card'>
				<div class='weather-metric-icon'>{icon}</div>
				<div class='card-kicker'>{label}</div>
				<h2>{value}</h2>
				<p class='card-caption'>{caption}</p>
			</div>
			""",
			unsafe_allow_html=True
		)

st.markdown("<div class='section-kicker'>03 <span>Weather Assessment</span></div>", unsafe_allow_html=True)
assessment_columns = st.columns([2, 1])
with assessment_columns[0]:
	st.markdown(
		f"""
		<div class='card weather-assessment'>
			<div class='card-kicker'>Live conditions at selected location</div>
			<h2>{weather_status}</h2>
			<p>Rainfall, humidity and wind can change the stability of exposed slopes. Monitor this panel alongside the risk prediction and local authority alerts.</p>
		</div>
		""",
		unsafe_allow_html=True
	)
with assessment_columns[1]:
	if rainfall is not None and rainfall > 20:
		st.warning("Heavy rainfall may increase landslide risk.")
	elif weather:
		st.success("No heavy rainfall detected right now.")
	else:
		st.info("Weather data is currently unavailable.")
		
st.markdown(
    "<div class='section-kicker'>04 <span>7 Day Forecast</span></div>",
    unsafe_allow_html=True
)

if weather and "forecast_dates" in weather:

    forecast_df = pd.DataFrame({
        "Date": weather["forecast_dates"],
        "Max Temp (°C)": weather["forecast_temp_max"],
        "Min Temp (°C)": weather["forecast_temp_min"],
        "Rainfall (mm)": weather["forecast_rain"]
    })

    st.dataframe(
        forecast_df,
        use_container_width=True,
        hide_index=True
    )

    st.markdown(
        "<div class='section-kicker'>05 <span>Forecast Trend</span></div>",
        unsafe_allow_html=True
    )

    chart_df = forecast_df.set_index("Date")

    st.line_chart(
        chart_df[
            [
                "Max Temp (°C)",
                "Min Temp (°C)"
            ]
        ]
    )

else:

    st.info(
        "Forecast weather data unavailable."
    )


st.markdown(
    "<div class='section-kicker'>06 <span>Forecast Landslide Risk</span></div>",
    unsafe_allow_html=True
)

if weather and "forecast_rain" in weather:

    risk_rows = []

    for i in range(len(weather["forecast_dates"])):

        rain = weather["forecast_rain"][i]

        if rain >= 100:
            risk = "🔴 High"

        elif rain >= 50:
            risk = "🟠 Moderate"

        else:
            risk = "🟢 Low"

        risk_rows.append({
            "Date": weather["forecast_dates"][i],
            "Forecast Rainfall (mm)": rain,
            "Risk Level": risk
        })

    risk_df = pd.DataFrame(risk_rows)

    st.dataframe(
        risk_df,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "Forecast risk data unavailable."
    )
