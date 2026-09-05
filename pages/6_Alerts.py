import re

import streamlit as st

from terrain import get_terrain
from utils.predict import predict_risk
from weather import get_weather

st.set_page_config(page_title="Landslide AI Alerts", page_icon="🚨", layout="wide")

with open("assets/styles.css") as css_file:
	st.markdown(f"<style>{css_file.read()}</style>", unsafe_allow_html=True)


st.markdown("<div class='alerts-shell-anchor'></div>", unsafe_allow_html=True)
st.markdown(
	"""
	<div class="weather-header alerts-header">
		<div class="main-brand-mark">▲</div>
		<div>
			<div class="assistant-kicker">LANDSLIDE INTELLIGENCE</div>
			<h1>Alerts & notifications</h1>
			<p>Stay ahead of changing conditions around your selected location.</p>
		</div>
	</div>
	""",
	unsafe_allow_html=True
)

selected_latitude = st.session_state.get("latitude", 24.5)
selected_longitude = st.session_state.get("longitude", 93.5)
weather = get_weather(selected_latitude, selected_longitude)
terrain = get_terrain(selected_latitude, selected_longitude)

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
	risk_level, risk_class = "Data unavailable", "neutral"
elif risk_score >= 70:
	risk_level, risk_class = "High Risk", "high"
elif risk_score >= 30:
	risk_level, risk_class = "Moderate Risk", "moderate"
else:
	risk_level, risk_class = "Low Risk", "low"

st.markdown("<div class='section-kicker'>01 <span>Risk Overview</span></div>", unsafe_allow_html=True)
overview_columns = st.columns([1.25, 1, 1, 1])
with overview_columns[0]:
	score_label = f"{risk_score:.1f}%" if risk_score is not None else "N/A"
	st.markdown(
		f"<div class='card alert-score-card {risk_class}'><div class='card-kicker'>Current risk level</div><h2>{risk_level}</h2><p class='card-caption'>Model score <strong>{score_label}</strong></p></div>",
		unsafe_allow_html=True
	)
with overview_columns[1]:
	st.metric("Rainfall", f"{weather['rain']} mm" if weather else "N/A")
with overview_columns[2]:
	st.metric("Humidity", f"{weather['humidity']}%" if weather else "N/A")
with overview_columns[3]:
	st.metric("Location", f"{selected_latitude:.2f}, {selected_longitude:.2f}")

st.markdown("<div class='section-kicker'>02 <span>Recent Alerts</span></div>", unsafe_allow_html=True)
alert_columns = st.columns(3)
alert_items = [
	("high", "High Risk Detection", "Risk prediction is elevated for this location.", "Now"),
	("moderate", "Weather Watch", "Rainfall and humidity are being monitored continuously.", "Live"),
	("low", "Data Updated", "Weather and terrain readings were refreshed successfully.", "Recent"),
]
if risk_level == "Low Risk":
	alert_items[0] = ("low", "No Immediate Threat", "Current model output is below the high-risk threshold.", "Now")
elif risk_level == "Data unavailable":
	alert_items[0] = ("moderate", "Data Unavailable", "Risk cannot be evaluated until readings return.", "Action needed")

for column, (severity, title, message, timestamp) in zip(alert_columns, alert_items):
	with column:
		st.markdown(
			f"<div class='alert-card alert-item {severity}'><div class='alert-icon'>!</div><div><strong>{title}</strong><p>{message}</p><small>{timestamp}</small></div></div>",
			unsafe_allow_html=True
		)

st.markdown("<div class='section-kicker'>03 <span>Mobile Notifications</span></div>", unsafe_allow_html=True)
notification_columns = st.columns([1.35, 1])
with notification_columns[0]:
	st.markdown(
		"<div class='card notification-copy'><div class='card-kicker'>Optional safety updates</div><h2>Get notified when risk changes</h2><p>Add a mobile number to receive high-risk alert updates. You can leave this turned off and remove your number at any time.</p></div>",
		unsafe_allow_html=True
	)
with notification_columns[1]:
	with st.form("mobile_alert_preferences"):
		enabled = st.checkbox("Enable mobile risk alerts", value=st.session_state.get("alert_enabled", False))
		phone_number = st.text_input("Mobile number", value=st.session_state.get("alert_phone", ""), placeholder="e.g. +91 98765 43210")
		save_preferences = st.form_submit_button("Save alert preference", use_container_width=True)

	if save_preferences:
		cleaned_number = re.sub(r"[\s()-]", "", phone_number)
		if enabled and not re.fullmatch(r"\+?[0-9]{10,15}", cleaned_number):
			st.error("Enter a valid mobile number or turn alerts off.")
		else:
			st.session_state.alert_enabled = enabled
			st.session_state.alert_phone = cleaned_number if enabled else ""
			if enabled:
				st.success("Mobile alert preference saved.")
				st.caption("SMS delivery requires a configured notification provider.")
			else:
				st.info("Mobile alerts are turned off.")