import streamlit as st
from model import calculate_risk
import pandas as pd
import plotly.graph_objects as go
from weather import get_weather
import joblib

ml_model = joblib.load("landslide_ml_model.pkl")

st.set_page_config(
    page_title="Landslide Risk Predictor",
    page_icon="🏔️",
    layout="wide"
)

st.title("🏔️ Landslide Risk Predictor")

st.write(
    "Enter environmental conditions to estimate landslide risk."
)

st.divider()

# Location
st.subheader("📍 Location")

col1, col2 = st.columns(2)

with col1:
    latitude = st.number_input(
        "Latitude",
        min_value=-90.0,
        max_value=90.0,
        value=22.05,
        format="%.4f"
    )

with col2:
    longitude = st.number_input(
        "Longitude",
        min_value=-180.0,
        max_value=180.0,
        value=88.10,
        format="%.4f"
    )

# Map
location_data = pd.DataFrame({
    "latitude": [latitude],
    "longitude": [longitude]
})

st.map(location_data)

# Current Weather
st.subheader("🌦️ Current Weather")

weather = get_weather(latitude, longitude)

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
    st.warning("⚠️ Unable to fetch current weather data.")

st.subheader("🌍 Environmental Conditions")

# Rainfall
use_live_rain = st.checkbox(
    "🌦️ Use current rainfall from weather data",
    value=True
)

if use_live_rain and weather:
    rainfall = weather["rain"]

    st.info(
        f"🌧️ Live rainfall being used: {rainfall} mm"
    )
else:
    rainfall = st.slider(
        "🌧️ Rainfall (mm)",
        min_value=0.0,
        max_value=1000.0,
        value=100.0
    )

# Environmental inputs
col1, col2 = st.columns(2)

with col1:

    slope = st.slider(
        "⛰️ Slope (degrees)",
        min_value=0.0,
        max_value=90.0,
        value=30.0
    )

    soil_moisture = st.slider(
        "💧 Soil Moisture (%)",
        min_value=0.0,
        max_value=100.0,
        value=50.0
    )

with col2:

    vegetation = st.slider(
        "🌿 Vegetation Coverage (%)",
        min_value=0.0,
        max_value=100.0,
        value=50.0
    )

    river_distance = st.slider(
        "🌊 Distance from River (m)",
        min_value=0.0,
        max_value=1000.0,
        value=500.0
    )

if st.button("🔍 Predict Landslide Risk", use_container_width=True):

    score, level = calculate_risk(
        rainfall,
        slope,
        soil_moisture,
        vegetation,
        river_distance
    )

        # ML prediction
    ml_prediction = ml_model.predict([[
        rainfall,
        slope,
        soil_moisture,
        vegetation,
        river_distance
    ]])

    ml_score = round(float(ml_prediction[0]), 2)

    # Risk Factors
    reasons = []

    if rainfall > 200:
        reasons.append("🌧️ Heavy rainfall is increasing the landslide risk.")

    if slope > 30:
        reasons.append("⛰️ Steep slope is increasing the landslide risk.")

    if soil_moisture > 70:
        reasons.append("💧 High soil moisture can reduce ground stability.")

    if vegetation < 30:
        reasons.append("🌿 Low vegetation coverage can reduce slope stability.")

    if river_distance < 100:
        reasons.append("🌊 Being close to a river can increase erosion risk.")

    st.subheader("⚠️ Risk Factors")

    if reasons:
        for reason in reasons:
            st.write("• " + reason)
    else:
        st.success("✅ No major risk factors detected.")

    st.info(
    f"📍 Analyzing location: "
    f"{latitude:.4f}, {longitude:.4f}")

    # Prediction
    st.subheader("📊 Prediction")

    st.metric(
        "🤖 ML Predicted Risk",
        f"{ml_score}%"
    )

    # Risk factor explanation
    st.subheader("⚠️ Risk Factors Detected")

    risk_factors = []

    if rainfall > 300:
        risk_factors.append(
            "🌧️ Very high rainfall"
        )
    elif rainfall > 200:
        risk_factors.append(
            "🌧️ High rainfall"
        )

    if slope > 40:
        risk_factors.append(
            "⛰️ Very steep slope"
        )
    elif slope > 30:
        risk_factors.append(
            "⛰️ Steep slope"
        )

    if soil_moisture > 70:
        risk_factors.append(
            "💧 High soil moisture"
        )

    if vegetation < 20:
        risk_factors.append(
            "🌿 Low vegetation coverage"
        )

    if river_distance < 100:
        risk_factors.append(
            "🌊 Very close to river"
        )

    if risk_factors:

        for factor in risk_factors:
            st.warning(factor)

    else:
        st.success(
            "✅ No major risk factors detected."
        )

    # Risk summary
    st.subheader("📝 Risk Summary")

    if score >= 70:
        st.error(
            "🔴 HIGH RISK: Multiple environmental "
            "conditions indicate an increased likelihood "
            "of landslide activity."
        )

    elif score >= 40:
        st.warning(
            "🟠 MODERATE RISK: Some environmental "
            "conditions may contribute to landslide risk. "
            "Monitoring is recommended."
        )

    else:
        st.success(
            "🟢 LOW RISK: Current environmental conditions "
            "indicate relatively low landslide risk."
        )

    # Risk gauge
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=score,
            title={"text": "Landslide Risk Score"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "black"},
                "steps": [
                    {"range": [0, 40], "color": "lightgreen"},
                    {"range": [40, 70], "color": "orange"},
                    {"range": [70, 100], "color": "red"}
                ]
            }
        )
    )

    st.plotly_chart(fig, use_container_width=True)

    # Risk level
    if score >= 70:
        st.error(f"🔴 HIGH RISK — {score}%")
    elif score >= 40:
        st.warning(f"🟠 MODERATE RISK — {score}%")
    else:
        st.success(f"🟢 LOW RISK — {score}%")

    # Safety Recommendations
    st.subheader("🛡️ Safety Recommendations")

    if score >= 70:
        st.error("🚨 Immediate caution recommended.")

        st.write("• Avoid travelling through steep or unstable slopes.")
        st.write("• Stay away from river banks and landslide-prone areas.")
        st.write("• Monitor rainfall and soil conditions closely.")
        st.write("• Follow local disaster-management warnings.")
        st.write("• If the area is already showing cracks or movement, evacuate to a safer location.")

    elif score >= 40:
        st.warning("⚠️ Increased caution is recommended.")

        st.write("• Monitor rainfall and slope conditions.")
        st.write("• Avoid unnecessary travel near steep slopes.")
        st.write("• Check for cracks, falling rocks, or unusual ground movement.")
        st.write("• Keep emergency contacts and supplies ready.")

    else:
        st.success("✅ Current conditions indicate relatively low risk.")

        st.write("• Continue monitoring environmental conditions.")
        st.write("• Maintain vegetation on slopes where possible.")
        st.write("• Stay alert during periods of heavy rainfall.")    