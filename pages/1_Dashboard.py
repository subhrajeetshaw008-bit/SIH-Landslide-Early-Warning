import streamlit as st
import folium

from streamlit_folium import st_folium
from terrain import get_terrain
from utils.predict import predict_risk
from weather import get_weather


st.set_page_config(
	page_title="Landslide AI Dashboard",
	page_icon="🏔️",
	layout="wide"
)

with open("assets/styles.css") as css_file:
	st.markdown(
		f"<style>{css_file.read()}</style>",
		unsafe_allow_html=True
	)


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

analyze_clicked = st.button("🔍 Analyze Location", use_container_width=True)

if analyze_clicked:
	get_weather.clear()
	get_terrain.clear()

st.session_state["latitude"] = selected_latitude
st.session_state["longitude"] = selected_longitude

st.title("📊 Landslide Risk Dashboard")
st.caption("Live weather, terrain and machine-learning risk assessment")

weather = get_weather(selected_latitude, selected_longitude)
terrain = get_terrain(selected_latitude, selected_longitude)

if weather:
	temperature = weather["temperature"]
	humidity = weather["humidity"]
	rainfall = weather["rain"]
else:
	temperature = humidity = rainfall = None

elevation = terrain["elevation"] if terrain else None

if weather and terrain:
	risk_score = predict_risk(
		temperature=temperature,
		humidity=humidity,
		rainfall=rainfall,
		elevation=elevation
	)
else:
	risk_score = None

if risk_score is None:
	risk_level = "Data unavailable"
elif risk_score < 30:
	risk_level = "Low Risk"
elif risk_score < 70:
	risk_level = "Moderate Risk"
else:
	risk_level = "High Risk"

card_1, card_2, card_3, card_4 = st.columns(4)

with card_1:
	st.metric("Risk Score", f"{risk_score:.1f}%" if risk_score is not None else "N/A", risk_level)

with card_2:
	st.metric("Temperature", f"{temperature} °C" if temperature is not None else "N/A")

with card_3:
	st.metric("Rainfall", f"{rainfall} mm" if rainfall is not None else "N/A")

with card_4:
	st.metric("Elevation", f"{elevation} m" if elevation is not None else "N/A")

st.divider()

map_column, detail_column = st.columns([2, 1])

with map_column:
	st.subheader("🗺️ Selected Location")
	risk_map = folium.Map(
		location=[selected_latitude, selected_longitude],
		zoom_start=10
	)
	folium.Marker(
		[selected_latitude, selected_longitude],
		tooltip="Selected location",
		popup=f"Lat: {selected_latitude}, Lon: {selected_longitude}"
	).add_to(risk_map)
	st_folium(risk_map, width=None, height=450)

with detail_column:
	st.subheader("📌 Current Conditions")
	st.write(f"**Humidity:** {humidity}%" if humidity is not None else "Humidity data unavailable")
	st.write(f"**Wind speed:** {weather['wind_speed']} km/h" if weather else "Wind data unavailable")
	st.write(f"**Risk level:** {risk_level}")
	st.write("Monitor rainfall and local authority alerts when conditions change.")

st.subheader("🚨 Alerts")
alert_columns = st.columns(3)

with alert_columns[0]:
	st.info("Weather data updated for the selected coordinates." if weather else "Weather service unavailable.")

with alert_columns[1]:
	st.warning("Rainfall may increase landslide risk." if rainfall and rainfall > 20 else "No heavy rainfall detected.")

with alert_columns[2]:
	if risk_score is not None and risk_score >= 70:
		st.error("High landslide risk detected.")
	else:
		st.success("No high-risk prediction detected.")
