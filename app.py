import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import rasterio
import glob
import os
import joblib

from weather import get_weather


# ==========================================
# CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Landslide Risk Predictor",
    page_icon="🏔️",
    layout="wide"
)


# ==========================================
# LOAD ML MODEL
# ==========================================

ml_model = joblib.load(
    "landslide_baseline_model.pkl"
)


# ==========================================
# TERRAIN EXTRACTION
# ==========================================

def get_terrain(latitude, longitude):

    dem_files = glob.glob(
        "data/dem*/*.tif"
    )

    for dem_file in dem_files:

        try:

            with rasterio.open(dem_file) as src:

                bounds = src.bounds

                # Check whether location is inside DEM
                if not (
                    bounds.left <= longitude <= bounds.right
                    and
                    bounds.bottom <= latitude <= bounds.top
                ):
                    continue

                row, col = src.index(
                    longitude,
                    latitude
                )

                # Read small 3x3 area
                window = rasterio.windows.Window(
                    col - 1,
                    row - 1,
                    3,
                    3
                )

                elevation = src.read(
                    1,
                    window=window,
                    boundless=True,
                    fill_value=np.nan
                ).astype(float)

                # Remove nodata
                if src.nodata is not None:

                    elevation[
                        elevation == src.nodata
                    ] = np.nan

                center = elevation[1, 1]

                if not np.isfinite(center):
                    continue

                # ==========================================
                # Calculate slope
                # ==========================================

                lat_rad = np.radians(latitude)

                dx = (
                    src.res[0]
                    * 111320
                    * np.cos(lat_rad)
                )

                dy = (
                    src.res[1]
                    * 111320
                )

                gy, gx = np.gradient(
                    elevation,
                    dy,
                    dx
                )

                slope = np.degrees(
                    np.arctan(
                        np.sqrt(
                            gx[1, 1] ** 2
                            +
                            gy[1, 1] ** 2
                        )
                    )
                )

                if not np.isfinite(slope):
                    continue

                return float(center), float(slope)

        except Exception:
            continue

    return None, None


# ==========================================
# TITLE
# ==========================================

st.title(
    "🏔️ Landslide Risk Predictor"
)

st.write(
    "AI/ML-based landslide susceptibility "
    "prediction for Northeast India."
)

st.divider()


# ==========================================
# LOCATION
# ==========================================

st.subheader("📍 Location")

col1, col2 = st.columns(2)

with col1:

    latitude = st.number_input(
        "Latitude",
        min_value=22.0,
        max_value=29.1,
        value=24.5,
        format="%.4f"
    )

with col2:

    longitude = st.number_input(
        "Longitude",
        min_value=88.0,
        max_value=96.8,
        value=93.5,
        format="%.4f"
    )


# ==========================================
# MAP
# ==========================================

location_data = pd.DataFrame({
    "latitude": [latitude],
    "longitude": [longitude]
})

st.map(location_data)


# ==========================================
# WEATHER
# ==========================================

st.subheader("🌦️ Current Weather")

weather = get_weather(
    latitude,
    longitude
)

if weather:

    weather_col1, weather_col2 = st.columns(2)

    with weather_col1:

        st.metric(
            "🌡️ Temperature",
            f"{weather['temperature']} °C"
        )

    with weather_col2:

        st.metric(
            "🌧️ Current Rain",
            f"{weather['rain']} mm"
        )

else:

    st.warning(
        "⚠️ Unable to fetch current weather data."
    )


# ==========================================
# TERRAIN
# ==========================================

st.subheader(
    "⛰️ Terrain Analysis"
)

if st.button(
    "🔍 Analyze Location",
    use_container_width=True
):

    with st.spinner(
        "Extracting terrain data..."
    ):

        elevation, slope = get_terrain(
            latitude,
            longitude
        )


    # ======================================
    # TERRAIN NOT FOUND
    # ======================================

    if elevation is None:

        st.error(
            "❌ No DEM coverage found for "
            "this location."
        )

        st.stop()


    # ======================================
    # DISPLAY TERRAIN
    # ======================================

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "🏔️ Elevation",
            f"{elevation:.1f} m"
        )

    with col2:

        st.metric(
            "⛰️ Slope",
            f"{slope:.2f}°"
        )


    # ======================================
    # ML INPUT
    # ======================================

    input_data = pd.DataFrame([
        {
            "Latitude": latitude,
            "Longitude": longitude,
            "Elevation_m": elevation,
            "Slope_degrees": slope
        }
    ])


    # ======================================
    # ML PREDICTION
    # ======================================

    probability = ml_model.predict_proba(
        input_data
    )[0][1]

    risk_score = probability * 100


    # ======================================
    # RISK LEVEL
    # ======================================

    if risk_score >= 75:

        risk_level = "HIGH"

    elif risk_score >= 50:

        risk_level = "MODERATE"

    else:

        risk_level = "LOW"


    # ======================================
    # PREDICTION
    # ======================================

    st.divider()

    st.subheader(
        "🤖 ML Prediction"
    )

    st.metric(
        "Landslide Susceptibility",
        f"{risk_score:.2f}%"
    )


    if risk_level == "HIGH":

        st.error(
            f"🔴 HIGH RISK — {risk_score:.2f}%"
        )

    elif risk_level == "MODERATE":

        st.warning(
            f"🟠 MODERATE RISK — {risk_score:.2f}%"
        )

    else:

        st.success(
            f"🟢 LOW RISK — {risk_score:.2f}%"
        )


    # ======================================
    # RISK GAUGE
    # ======================================

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=risk_score,
            title={
                "text":
                "Landslide Susceptibility"
            },
            gauge={
                "axis": {
                    "range": [0, 100]
                },
                "steps": [
                    {
                        "range": [0, 50],
                        "color": "lightgreen"
                    },
                    {
                        "range": [50, 75],
                        "color": "orange"
                    },
                    {
                        "range": [75, 100],
                        "color": "red"
                    }
                ]
            }
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # ======================================
    # RISK FACTORS
    # ======================================

    st.subheader(
        "⚠️ Terrain Risk Factors"
    )

    factors = []

    if slope >= 40:

        factors.append(
            "⛰️ Very steep terrain"
        )

    elif slope >= 30:

        factors.append(
            "⛰️ Steep terrain"
        )

    if elevation >= 2000:

        factors.append(
            "🏔️ High elevation"
        )

    if weather:

        rainfall = weather["rain"]

        if rainfall > 50:

            factors.append(
                "🌧️ Significant current rainfall"
            )

    if factors:

        for factor in factors:

            st.warning(factor)

    else:

        st.success(
            "✅ No major terrain risk factors detected."
        )


    # ======================================
    # LOCATION INFO
    # ======================================

    st.subheader(
        "📍 Analysis Details"
    )

    st.write(
        f"**Latitude:** {latitude:.4f}"
    )

    st.write(
        f"**Longitude:** {longitude:.4f}"
    )

    st.write(
        f"**Elevation:** {elevation:.1f} m"
    )

    st.write(
        f"**Slope:** {slope:.2f}°"
    )

    st.info(
        "ℹ️ This baseline model estimates "
        "landslide susceptibility from geographic "
        "location and terrain features. It is not "
        "a real-time landslide warning system yet."
    )


    # ======================================
    # SAFETY
    # ======================================

    st.subheader(
        "🛡️ Safety Recommendations"
    )

    if risk_score >= 75:

        st.error(
            "🚨 High susceptibility detected. "
            "Exercise extreme caution around "
            "steep slopes, especially during "
            "heavy rainfall."
        )

        st.write(
            "• Avoid unnecessary travel through steep slopes."
        )

        st.write(
            "• Monitor local disaster-management warnings."
        )

        st.write(
            "• Watch for cracks, falling rocks, "
            "or unusual ground movement."
        )

    elif risk_score >= 50:

        st.warning(
            "⚠️ Moderate susceptibility detected. "
            "Continue monitoring conditions."
        )

        st.write(
            "• Be cautious near steep slopes."
        )

        st.write(
            "• Monitor rainfall conditions."
        )

    else:

        st.success(
            "✅ Low susceptibility according to "
            "the current baseline model."
        )

        st.write(
            "• Continue normal environmental monitoring."
        )