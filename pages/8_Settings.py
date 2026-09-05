import re

import streamlit as st

st.set_page_config(page_title="Landslide AI Settings", page_icon="⚙️", layout="wide")

with open("assets/styles.css") as css_file:
	st.markdown(f"<style>{css_file.read()}</style>", unsafe_allow_html=True)


st.markdown("<div class='settings-shell-anchor'></div>", unsafe_allow_html=True)
st.markdown(
	"""
	<div class="weather-header settings-header">
		<div class="main-brand-mark">▲</div>
		<div>
			<div class="assistant-kicker">LANDSLIDE INTELLIGENCE</div>
			<h1>Settings</h1>
			<p>Shape your monitoring workspace around the way you work.</p>
		</div>
	</div>
	""",
	unsafe_allow_html=True
)

st.markdown("<div class='section-kicker'>01 <span>Monitoring Location</span></div>", unsafe_allow_html=True)
with st.form("location_settings"):
	location_columns = st.columns(2)
	with location_columns[0]:
		saved_latitude = st.number_input(
			"Latitude",
			value=float(st.session_state.get("latitude", 24.5)),
			format="%.4f"
		)
	with location_columns[1]:
		saved_longitude = st.number_input(
			"Longitude",
			value=float(st.session_state.get("longitude", 93.5)),
			format="%.4f"
		)
	save_location = st.form_submit_button("Save monitoring location", use_container_width=True)

if save_location:
	st.session_state["latitude"] = saved_latitude
	st.session_state["longitude"] = saved_longitude
	st.success("Monitoring location updated.")

st.markdown("<div class='section-kicker'>02 <span>Alert Preferences</span></div>", unsafe_allow_html=True)
alert_columns = st.columns([1.2, 1])
with alert_columns[0]:
	st.markdown(
		"""
		<div class='card settings-copy-card'>
			<div class='card-kicker'>Optional mobile safety updates</div>
			<h2>Stay informed when conditions change</h2>
			<p>Enable alerts and add a mobile number for high-risk notifications. Your number is only used for this preference and is hidden when it is not enabled.</p>
		</div>
		""",
		unsafe_allow_html=True
	)
with alert_columns[1]:
	with st.form("notification_settings"):
		alerts_enabled = st.checkbox(
			"Enable mobile risk alerts",
			value=st.session_state.get("alert_enabled", False)
		)
		alert_phone = st.text_input(
			"Mobile number",
			value=st.session_state.get("alert_phone", ""),
			placeholder="e.g. +91 98765 43210"
		)
		save_alerts = st.form_submit_button("Save alert settings", use_container_width=True)

	if save_alerts:
		cleaned_phone = re.sub(r"[\s()-]", "", alert_phone)
		if alerts_enabled and not re.fullmatch(r"\+?[0-9]{10,15}", cleaned_phone):
			st.error("Enter a valid mobile number or turn alerts off.")
		else:
			st.session_state["alert_enabled"] = alerts_enabled
			st.session_state["alert_phone"] = cleaned_phone if alerts_enabled else ""
			st.success("Alert settings saved.")

st.markdown("<div class='section-kicker'>03 <span>Assistant Preferences</span></div>", unsafe_allow_html=True)
assistant_columns = st.columns(2)
with assistant_columns[0]:
	response_style = st.selectbox(
		"Response style",
		["Clear and concise", "Detailed analysis", "Safety-first guidance"],
		index=["Clear and concise", "Detailed analysis", "Safety-first guidance"].index(
			st.session_state.get("response_style", "Clear and concise")
		)
	)
with assistant_columns[1]:
	show_location_context = st.checkbox(
		"Include selected location context",
		value=st.session_state.get("show_location_context", True)
	)

if st.button("Save assistant preferences", type="primary"):
	st.session_state["response_style"] = response_style
	st.session_state["show_location_context"] = show_location_context
	st.success("Assistant preferences saved.")

st.markdown("<div class='section-kicker'>04 <span>Data & Session</span></div>", unsafe_allow_html=True)
data_columns = st.columns([1, 1, 1])
with data_columns[0]:
	conversation_count = len([message for message in st.session_state.get("messages", []) if message["role"] == "user"])
	st.metric("Saved conversations", conversation_count)
with data_columns[1]:
	if st.button("Clear chat history", use_container_width=True):
		st.session_state["messages"] = []
		st.success("Chat history cleared.")
with data_columns[2]:
	if st.button("Reset preferences", use_container_width=True):
		st.session_state["alert_enabled"] = False
		st.session_state["alert_phone"] = ""
		st.session_state["response_style"] = "Clear and concise"
		st.session_state["show_location_context"] = True
		st.success("Preferences reset to defaults.")

st.caption("Password and other authentication secrets are never displayed in Settings.")