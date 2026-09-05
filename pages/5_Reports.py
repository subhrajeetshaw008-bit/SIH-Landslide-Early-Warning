import streamlit as st

from terrain import get_terrain
from utils.auth import require_login
from utils.predict import predict_risk
from weather import get_weather


st.set_page_config(page_title="Landslide AI Report", page_icon="📄", layout="wide")

with open("assets/styles.css") as css_file:
	st.markdown(f"<style>{css_file.read()}</style>", unsafe_allow_html=True)


user = require_login()

latitude = st.session_state.get("latitude", 24.5)
longitude = st.session_state.get("longitude", 93.5)

st.title(f"📄 {user['name']}'s Location Report")
st.caption(f"Personalized report for {user['email']}")
st.write(f"**Coordinates:** {latitude:.4f}, {longitude:.4f}")

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
	risk_level = "Low Risk"
elif risk_score < 70:
	risk_level = "Moderate Risk"
else:
	risk_level = "High Risk"

report_columns = st.columns(4)
with report_columns[0]:
	st.metric("Risk score", f"{risk_score:.1f}%" if risk_score is not None else "N/A")
with report_columns[1]:
	st.metric("Risk level", risk_level)
with report_columns[2]:
	st.metric("Rainfall", f"{weather['rain']} mm" if weather else "N/A")
with report_columns[3]:
	st.metric("Elevation", f"{terrain['elevation']} m" if terrain else "N/A")

st.divider()
st.subheader("Assessment details")

if weather:
	st.write(f"Temperature: {weather['temperature']} °C")
	st.write(f"Humidity: {weather['humidity']} %")
	st.write(f"Wind speed: {weather['wind_speed']} km/h")
else:
	st.error("Weather data is currently unavailable for this location.")

if risk_score is not None and risk_score >= 70:
	st.error("High risk detected. Follow local authority alerts and keep evacuation plans ready.")
elif risk_score is not None and risk_score >= 30:
	st.warning("Moderate risk detected. Monitor rainfall and local advisories.")
else:
	st.success("Current predicted risk is low, but conditions can change.")

st.download_button(
	"Download report",
	f"Landslide AI Report\nUser: {user['name']}\nLocation: {latitude:.4f}, {longitude:.4f}\nRisk: {risk_level} ({risk_score if risk_score is not None else 'N/A'}%)\n",
	file_name="landslide_report.txt",
	mime="text/plain"
)