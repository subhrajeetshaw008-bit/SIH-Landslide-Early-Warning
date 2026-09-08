import folium
import streamlit as st

from streamlit_folium import st_folium
from terrain import get_terrain
from utils.auth import require_login
from utils.predict import predict_risk
from weather import get_weather

st.set_page_config(page_title="Landslide Risk Map", page_icon="🗺️", layout="wide")

with open("assets/styles.css") as css_file:
	st.markdown(f"<style>{css_file.read()}</style>", unsafe_allow_html=True)


user = require_login()
latitude = st.session_state.get("latitude", 24.5)
longitude = st.session_state.get("longitude", 93.5)

st.title("🗺️ Risk Intelligence Map")
st.caption(f"Location intelligence for {user['name']} • {latitude:.4f}, {longitude:.4f}")
st.info(
    "🖱️ Click anywhere on the map to update the monitored location."
)


weather = get_weather(latitude, longitude)
terrain = get_terrain(latitude, longitude)

if weather and terrain:
	risk_score = predict_risk(
		temperature=weather["temperature"],
		humidity=weather["humidity"],
		rainfall=weather["rain"],
		elevation=terrain["elevation"]
	)
else:
	risk_score = None

if risk_score is None:
	risk_level = "Data unavailable"
elif risk_score < 30:
	risk_level = "Low risk"
elif risk_score < 70:
	risk_level = "Moderate risk"
else:
	risk_level = "High risk"

map_column, insight_column = st.columns([2.1, 1])

with map_column:
	st.subheader("Live risk location")
	risk_map = folium.Map(
		location=[latitude, longitude],
		zoom_start=11,
		tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
		attr="Esri World Imagery"
	)

	if risk_score is None:
		circle_color = "gray"
		fill_color = "gray"
	elif risk_score < 30:
		circle_color = "green"
		fill_color = "green"
	elif risk_score < 70:
		circle_color = "orange"
		fill_color = "orange"
	else:
		circle_color = "red"
		fill_color = "red"

	folium.Circle(
		[latitude, longitude],
		radius=5000,
		color=circle_color,
		fill=True,
		fill_color=fill_color,
		fill_opacity=0.30
	).add_to(risk_map)

	folium.Marker(
		[latitude, longitude],
		tooltip=f"{user['name']}'s selected place",
		popup=f"{latitude:.4f}, {longitude:.4f} | {risk_level}",
		icon=folium.Icon(
			color=(
				"green"
				if risk_score is not None and risk_score < 30
				else "orange"
				if risk_score is not None and risk_score < 70
				else "red"
			)
		)
	).add_to(risk_map)

	folium.LayerControl().add_to(risk_map)

	map_data = st_folium(
		risk_map,
		width=None,
		height=560
	)
	if map_data and map_data.get("last_clicked"):
		clicked_lat = map_data["last_clicked"]["lat"]
		clicked_lon = map_data["last_clicked"]["lng"]

		st.session_state["latitude"] = clicked_lat
		st.session_state["longitude"] = clicked_lon

		st.rerun()

with insight_column:
	st.subheader("Place profile")
	st.markdown(
		f"<div class='card'><h4>👤 {user['name']}</h4><p>{user['email']}</p><p><b>Tracked coordinates</b><br>{latitude:.4f}, {longitude:.4f}</p></div>",
		unsafe_allow_html=True
	)
	st.metric("Risk score", f"{risk_score:.1f}%" if risk_score is not None else "N/A", risk_level)
	st.metric("Elevation", f"{terrain['elevation']} m" if terrain else "N/A")
	st.metric("Rainfall", f"{weather['rain']} mm" if weather else "N/A")

st.divider()
st.subheader("Risk factors and guidance")
factor_columns = st.columns(3)

with factor_columns[0]:
	st.markdown("**Weather exposure**")
	st.write(f"Temperature: {weather['temperature']} °C" if weather else "Unavailable")
	st.write(f"Humidity: {weather['humidity']} %" if weather else "Unavailable")
	st.write(f"Wind: {weather['wind_speed']} km/h" if weather else "Unavailable")

with factor_columns[1]:
	st.markdown("**Terrain profile**")
	st.write(f"Elevation: {terrain['elevation']} m" if terrain else "Unavailable")
	st.write(f"Slope: {terrain['slope']:.1f}°" if terrain else "Unavailable")
	st.write("Elevation and slope are used as model features.")
	st.write("Soil composition data is not currently available.")

with factor_columns[2]:
	st.markdown("**Recommended action**")
	if risk_score is not None and risk_score >= 70:
		st.error("Follow local authority alerts and prepare to evacuate.")
	elif risk_score is not None and risk_score >= 30:
		st.warning("Monitor rainfall, cracks and local advisories.")
	else:
		st.success("Continue monitoring changing weather conditions.")