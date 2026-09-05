import streamlit as st

from terrain import get_terrain


st.set_page_config(
	page_title="Landslide AI Terrain",
	page_icon="⛰️",
	layout="wide"
)

with open("assets/styles.css") as css_file:
	st.markdown(f"<style>{css_file.read()}</style>", unsafe_allow_html=True)


st.markdown("<div class='terrain-shell-anchor'></div>", unsafe_allow_html=True)
st.markdown(
	"""
	<div class="terrain-header">
		<div class="main-brand-mark">▲</div>
		<div>
			<div class="assistant-kicker">LANDSLIDE INTELLIGENCE</div>
			<h1>Terrain analysis</h1>
			<p>Elevation and slope intelligence for understanding the selected location.</p>
		</div>
	</div>
	""",
	unsafe_allow_html=True
)

st.markdown("<div class='section-kicker'>01 <span>Selected Location</span></div>", unsafe_allow_html=True)
location_column, action_column = st.columns([4, 1])

with location_column:
	latitude_column, longitude_column = st.columns(2)
	with latitude_column:
		selected_latitude = st.number_input(
			"Latitude",
			value=st.session_state.get("latitude", 24.5),
			format="%.4f"
		)
	with longitude_column:
		selected_longitude = st.number_input(
			"Longitude",
			value=st.session_state.get("longitude", 93.5),
			format="%.4f"
		)

with action_column:
	st.write("")
	st.write("")
	refresh_terrain = st.button("Refresh Terrain", use_container_width=True)

if refresh_terrain:
	get_terrain.clear()

st.session_state["latitude"] = selected_latitude
st.session_state["longitude"] = selected_longitude
terrain = get_terrain(selected_latitude, selected_longitude)

elevation = terrain["elevation"] if terrain else None
slope = terrain["slope"] if terrain else None
elevation_label = f"{elevation:.1f} m" if elevation is not None else "N/A"
slope_label = f"{slope:.1f}°" if slope is not None else "N/A"
data_status = "Live terrain data available" if terrain else "Terrain service unavailable"

st.markdown("<div class='section-kicker'>02 <span>Terrain Metrics</span></div>", unsafe_allow_html=True)
metric_columns = st.columns(3)
metrics = [
	("⛰️", "Elevation", elevation_label, "Above mean sea level"),
	("📐", "Slope", slope_label, "Steepness of terrain"),
	("◌", "Data status", data_status, "Source availability"),
]

for column, (icon, label, value, caption) in zip(metric_columns, metrics):
	with column:
		st.markdown(
			f"""
			<div class='card terrain-metric-card'>
				<div class='terrain-metric-icon'>{icon}</div>
				<div class='card-kicker'>{label}</div>
				<h2>{value}</h2>
				<p class='card-caption'>{caption}</p>
			</div>
			""",
			unsafe_allow_html=True
		)

st.markdown("<div class='section-kicker'>03 <span>Terrain Assessment</span></div>", unsafe_allow_html=True)
assessment_column, limitation_column = st.columns([2, 1])

with assessment_column:
	st.markdown(
		f"""
		<div class='card terrain-note'>
			<div class='card-kicker'>Elevation & slope profile</div>
			<h2>{data_status}</h2>
			<p>Elevation and slope are both available as terrain features for the selected point. Combine these readings with rainfall and local observations when assessing landslide conditions.</p>
		</div>
		""",
		unsafe_allow_html=True
	)

with limitation_column:
	if terrain:
		st.info("Aspect and soil composition are not currently available from the terrain service.")
	else:
		st.warning("Terrain data could not be loaded. Check the location and try again.")