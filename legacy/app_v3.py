import streamlit as st
import pandas as pd
import joblib
import folium
from streamlit_folium import st_folium

from weather import get_weather
from online_terrain import get_online_terrain


# ============================================================
# PAGE
# ============================================================

st.set_page_config(
    page_title="Landslide Risk Predictor v3.0",
    page_icon="🏔️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# EXACT DEMO-STYLE THEME
# ============================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

:root {
    --bg: #0d1117;
    --panel: rgba(22,27,34,.78);
    --line: rgba(255,255,255,.09);
    --muted: #9ca3af;
    --text: #e6edf3;
    --amber: #f59e0b;
    --amber-light: #fef3c7;
    --red: #ef4444;
    --green: #22c55e;
    --blue: #38bdf8;
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        linear-gradient(rgba(5,8,12,.78), rgba(5,8,12,.92)),
        radial-gradient(circle at 10% 0%, rgba(245,158,11,.12), transparent 30%),
        #0d1117;
    color: var(--text);
}

header[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    max-width: 1600px !important;
    padding: 12px 14px 28px !important;
}

[data-testid="stSidebar"] {
    background: rgba(5,8,12,.96);
    border-right: 1px solid var(--line);
}

[data-testid="stSidebar"] > div:first-child {
    padding-top: 18px;
}

.stMarkdown {
    margin-bottom: 0;
}

div[data-testid="column"] {
    min-width: 0;
}

.glass {
    background: var(--panel);
    backdrop-filter: blur(12px);
    border: 1px solid var(--line);
    border-radius: 14px;
    box-shadow: 0 12px 30px rgba(0,0,0,.18);
}

.glass-amber {
    background: var(--panel);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(217,119,6,.34);
    border-radius: 14px;
}

.glow-red {
    box-shadow: 0 0 18px rgba(239,68,68,.25);
    border: 1px solid rgba(239,68,68,.58);
}

.glow-green {
    box-shadow: 0 0 18px rgba(34,197,94,.20);
    border: 1px solid rgba(34,197,94,.50);
}

.card-title {
    color: #9ca3af;
    font: 10px/1.2 monospace;
    text-transform: uppercase;
    letter-spacing: .25px;
}

.big-value {
    color: #fef3c7;
    font-size: 20px;
    font-weight: 700;
}

.muted {
    color: #9ca3af;
    font-size: 10px;
}

.small {
    color: #d1d5db;
    font-size: 11px;
}

.stButton > button {
    border-radius: 9px;
    border: 1px solid rgba(245,158,11,.32);
    background: rgba(245,158,11,.10);
    color: #fbbf24;
    font-weight: 600;
    min-height: 34px;
}

.stButton > button:hover {
    border-color: rgba(245,158,11,.72);
    background: rgba(245,158,11,.20);
    color: white;
}

div[data-baseweb="input"] {
    background: rgba(0,0,0,.34);
    border-color: rgba(255,255,255,.10);
}

div[data-baseweb="input"] input {
    color: #fbbf24 !important;
    font-family: monospace;
}

[data-testid="stMetric"] {
    background: rgba(0,0,0,.24);
    border: 1px solid rgba(255,255,255,.08);
    border-radius: 10px;
    padding: 10px;
}

[data-testid="stMetricLabel"] {
    color: #9ca3af;
    font-size: 10px;
}

[data-testid="stMetricValue"] {
    color: #fef3c7;
    font-size: 21px;
}

div[data-testid="stRadio"] label {
    color: #9ca3af;
}

div[data-testid="stRadio"] label:hover {
    color: white;
}

hr {
    border-color: rgba(255,255,255,.08);
}

/* Hide Streamlit chrome that fights the dashboard composition */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


# ============================================================
# DATA
# ============================================================

@st.cache_resource
def load_model():
    return joblib.load("landslide_baseline_model.pkl")


@st.cache_data(ttl=900)
def fetch_weather(latitude, longitude):
    try:
        return get_weather(latitude, longitude)
    except Exception:
        return None


@st.cache_data(ttl=900)
def fetch_terrain(latitude, longitude):
    try:
        return get_online_terrain(latitude, longitude)
    except Exception:
        return None, None


ml_model = load_model()


def risk_class(score):
    if score >= 75:
        return "HIGH"
    if score >= 50:
        return "MODERATE"
    return "LOW"


def risk_color(level):
    return {
        "HIGH": "#ef4444",
        "MODERATE": "#eab308",
        "LOW": "#22c55e",
    }[level]


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.markdown("""
    <div style="
        height:92px;
        border-radius:12px;
        margin-bottom:16px;
        background:
            linear-gradient(rgba(0,0,0,.20),rgba(0,0,0,.50)),
            linear-gradient(135deg,#27351f,#111a14);
        border:1px solid rgba(255,255,255,.08);
        display:flex;
        align-items:center;
        justify-content:center;
        font-size:42px;
    ">🏔️</div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="
        color:#f59e0b;
        font-size:11px;
        font-weight:700;
        letter-spacing:.6px;
        margin:4px 3px 10px;
    ">LANDSLIDE MONITORING</div>
    """, unsafe_allow_html=True)

    page = st.radio(
        "Navigation",
        [
            "Dashboard",
            "Risk Map",
            "Weather",
            "Terrain Analysis",
            "Reports",
            "Alerts",
            "Settings",
        ],
        label_visibility="collapsed",
    )

    st.markdown("---")

    st.markdown("""
    <div class="glass glow-green" style="padding:12px;">
        <div style="display:flex;align-items:center;gap:8px;">
            <span style="
                width:9px;height:9px;border-radius:50%;
                background:#22c55e;display:inline-block;
                box-shadow:0 0 10px rgba(34,197,94,.7);
            "></span>
            <span style="color:#4ade80;font-size:11px;font-weight:600;">
                System Status
            </span>
        </div>
        <div style="color:#d1d5db;font-size:11px;margin-top:4px;">
            Operational
        </div>
        <div style="color:#6b7280;font-size:9px;">
            All systems normal
        </div>
    </div>

    <div style="
        display:flex;align-items:center;justify-content:space-between;
        padding:10px 2px 0;
    ">
        <div style="display:flex;align-items:center;gap:9px;">
            <div style="
                width:31px;height:31px;border-radius:50%;
                background:rgba(180,83,9,.45);
                border:1px solid #f59e0b;
                display:flex;align-items:center;justify-content:center;
                font-size:10px;font-weight:700;
            ">AU</div>
            <div>
                <div style="font-size:10px;color:white;font-weight:600;">
                    Admin User
                </div>
                <div style="font-size:9px;color:#9ca3af;">
                    Research Team
                </div>
            </div>
        </div>
        <span style="color:#6b7280;font-size:14px;">⋮</span>
    </div>
    """, unsafe_allow_html=True)


# ============================================================
# HEADER
# ============================================================

st.markdown("""
<div class="glass" style="
    padding:13px 18px;
    margin-bottom:12px;
    background:rgba(0,0,0,.42);
">
    <div style="
        display:flex;
        align-items:center;
        justify-content:space-between;
        gap:15px;
    ">
        <div style="display:flex;align-items:center;gap:12px;">
            <div style="
                padding:8px 10px;
                background:rgba(217,119,6,.18);
                border:1px solid rgba(245,158,11,.30);
                border-radius:9px;
                font-size:24px;
            ">🏔️</div>
            <div>
                <div style="
                    font-size:20px;
                    font-weight:700;
                    letter-spacing:.2px;
                    color:#fef3c7;
                ">
                    Landslide Risk Predictor v3.0
                    <span style="
                        font-size:9px;font-weight:400;
                        padding:3px 7px;border-radius:5px;
                        background:rgba(255,255,255,.08);
                        color:#d1d5db;margin-left:5px;
                    ">Advanced Analytics</span>
                </div>
                <div style="
                    font-size:9px;color:#9ca3af;margin-top:3px;
                ">
                    AI/ML-based landslide susceptibility prediction for Northeast India
                </div>
            </div>
        </div>

        <div style="display:flex;align-items:center;gap:8px;">
            <div style="
                padding:7px 11px;border-radius:8px;
                background:rgba(34,197,94,.10);
                border:1px solid rgba(34,197,94,.28);
                color:#4ade80;font-size:9px;font-weight:600;
            ">● SYSTEM OPERATIONAL</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# ============================================================
# LOCATION INPUT
# ============================================================

left, right = st.columns([1, 2])

with left:
    st.markdown("""
    <div class="glass" style="padding:11px;">
        <div class="card-title">01 Location</div>
    </div>
    """, unsafe_allow_html=True)

    latitude = st.number_input(
        "Latitude",
        min_value=22.0,
        max_value=29.1,
        value=24.5,
        step=0.0001,
        format="%.4f",
    )

with right:
    st.markdown("""
    <div class="glass" style="padding:11px;">
        <div class="card-title">Geological Context</div>
        <div class="small" style="margin-top:5px;">
            Lithology: Dataset required &nbsp; • &nbsp;
            Soil Type: Dataset required &nbsp; • &nbsp;
            Hydrological conditions: Weather-derived
        </div>
    </div>
    """, unsafe_allow_html=True)

    longitude = st.number_input(
        "Longitude",
        min_value=88.0,
        max_value=96.8,
        value=93.5,
        step=0.0001,
        format="%.4f",
    )


weather = fetch_weather(latitude, longitude)
elevation, slope = fetch_terrain(latitude, longitude)

if elevation is not None:
    input_data = pd.DataFrame([{
        "Latitude": latitude,
        "Longitude": longitude,
        "Elevation_m": elevation,
        "Slope_degrees": slope,
    }])
    probability = float(ml_model.predict_proba(input_data)[0][1])
    risk_score = probability * 100
    risk_level = risk_class(risk_score)
else:
    probability = None
    risk_score = None
    risk_level = "LOW"


# ============================================================
# DASHBOARD
# ============================================================

if page == "Dashboard":

    main_col, risk_col = st.columns([2, 1], gap="small")

    # ---------------- MAP ----------------
    with main_col:
        st.markdown("""
        <div class="glass" style="padding:10px 10px 0;">
            <div style="
                display:flex;justify-content:space-between;
                align-items:center;margin-bottom:7px;
            ">
                <span class="card-title">03 Risk Map</span>
                <span style="
                    color:#4ade80;font-size:8px;
                    padding:3px 7px;border-radius:5px;
                    background:rgba(34,197,94,.10);
                    border:1px solid rgba(34,197,94,.20);
                ">● LIVE DATA FEED</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        m = folium.Map(
            location=[latitude, longitude],
            zoom_start=10,
            tiles="OpenStreetMap",
            control_scale=True,
        )

        folium.TileLayer(
            "OpenTopoMap",
            name="Terrain",
            control=True,
        ).add_to(m)

        folium.Marker(
            [latitude, longitude],
            tooltip="Selected Location",
            popup=(
                f"<b>Selected Location</b><br>"
                f"Latitude: {latitude:.4f}<br>"
                f"Longitude: {longitude:.4f}"
            ),
            icon=folium.Icon(color="red", icon="info-sign"),
        ).add_to(m)

        folium.LayerControl().add_to(m)

        st_folium(m, width=None, height=380, returned_objects=[])

        # map overlays that visually match the demo
        st.markdown("""
        <div style="
            margin-top:-72px;
            margin-left:15px;
            position:relative;
            z-index:10;
            pointer-events:none;
        ">
            <div style="
                display:inline-flex;gap:4px;
                background:rgba(0,0,0,.72);
                padding:5px;border-radius:8px;
                border:1px solid rgba(255,255,255,.10);
            ">
                <span style="
                    padding:4px 9px;border-radius:5px;
                    background:rgba(245,158,11,.30);
                    color:#fcd34d;font-size:9px;
                ">Map</span>
                <span style="padding:4px 8px;color:#9ca3af;font-size:9px;">Satellite</span>
                <span style="padding:4px 8px;color:#9ca3af;font-size:9px;">Terrain</span>
            </div>
        </div>
        <div style="
            height:60px;
            position:relative;
            z-index:9;
        "></div>
        """, unsafe_allow_html=True)

    # ---------------- RISK ----------------
    with risk_col:
        color = risk_color(risk_level)

        if risk_score is not None:
            score_text = f"{risk_score:.0f}%"
            confidence_text = "Baseline model probability"
            analysis_text = "Current analysis"
        else:
            score_text = "--"
            confidence_text = "Terrain data unavailable"
            analysis_text = "Awaiting terrain data"

        st.markdown(f"""
        <div class="glass-amber" style="
            padding:12px;height:100%;
            border-color:{color}70;
            box-shadow:0 0 16px {color}22;
        ">
            <div class="card-title">04 Risk Prediction</div>

            <div class="glow-red" style="
                margin-top:7px;padding:11px;border-radius:11px;
                background:rgba(69,10,10,.35);
                border-color:{color}80;
            ">
                <div style="
                    display:flex;justify-content:space-between;
                    align-items:center;
                ">
                    <div>
                        <div style="
                            color:{color};font-size:23px;
                            font-weight:900;text-transform:uppercase;
                        ">{risk_level} RISK</div>
                        <div style="
                            color:#d1d5db;font-size:9px;margin-top:3px;
                        ">{confidence_text}</div>
                        <div style="
                            color:#6b7280;font-size:8px;margin-top:3px;
                        ">{analysis_text}</div>
                    </div>

                    <div style="
                        width:58px;height:58px;border-radius:50%;
                        border:4px solid {color};
                        display:flex;align-items:center;
                        justify-content:center;
                        color:{color};font-size:14px;font-weight:800;
                    ">{score_text}</div>
                </div>
            </div>

            <div style="margin-top:13px;">
                <div class="small" style="font-weight:600;margin-bottom:6px;">
                    Key Risk Drivers
                </div>
        """, unsafe_allow_html=True)

        drivers = []

        if slope is not None:
            if slope >= 40:
                drivers.append(("Critical Slope", f"{slope:.1f}° — very steep terrain"))
            elif slope >= 30:
                drivers.append(("High-Risk Slopes", f"{slope:.1f}° — steep terrain"))
            else:
                drivers.append(("Slope", f"{slope:.1f}°"))

        if elevation is not None and elevation >= 2000:
            drivers.append(("High Elevation", f"{elevation:.0f} m"))

        if weather and weather.get("rain", 0) > 50:
            drivers.append(("Heavy Rainfall", f"{weather['rain']} mm"))

        if not drivers:
            drivers.append(("Terrain Factors", "No major rule trigger"))

        for name, detail in drivers[:4]:
            st.markdown(f"""
            <div style="
                padding:7px;margin-bottom:5px;
                background:rgba(0,0,0,.30);
                border:1px solid rgba(255,255,255,.07);
                border-radius:7px;
            ">
                <div style="color:{color};font-size:9px;font-weight:600;">
                    {name}
                </div>
                <div style="color:#9ca3af;font-size:8px;">
                    {detail}
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("""
            </div>

            <div style="
                margin-top:8px;padding:8px;
                background:rgba(0,0,0,.28);
                border:1px solid rgba(255,255,255,.07);
                border-radius:8px;
            ">
                <div class="muted">Confidence Interval</div>
                <div style="
                    height:6px;margin-top:7px;border-radius:6px;
                    background:linear-gradient(
                        90deg,#22c55e 0%,#eab308 55%,#ef4444 100%
                    );
                "></div>
                <div style="
                    display:flex;justify-content:space-between;
                    color:#6b7280;font-size:7px;margin-top:3px;
                ">
                    <span>Low</span><span>Extreme</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ---------------- BOTTOM ROW ----------------

    wcol, tcol, vcol = st.columns(3, gap="small")

    with wcol:
        temp = weather["temperature"] if weather else None
        rain = weather["rain"] if weather else None
        st.markdown(f"""
        <div class="glass" style="padding:11px;min-height:132px;">
            <div style="
                display:flex;justify-content:space-between;
                border-bottom:1px solid rgba(255,255,255,.05);
                padding-bottom:7px;
            ">
                <span class="card-title">02 Current Weather</span>
                <span style="color:#38bdf8;font-size:8px;">LIVE</span>
            </div>
            <div style="
                display:grid;grid-template-columns:1fr 1fr;
                gap:10px;margin-top:12px;
            ">
                <div>
                    <div class="muted">Temperature</div>
                    <div style="font-size:21px;font-weight:700;color:#fff;">
                        {f"{temp:.1f} °C" if temp is not None else "--"}
                    </div>
                </div>
                <div>
                    <div class="muted">Rainfall</div>
                    <div style="font-size:21px;font-weight:700;color:#38bdf8;">
                        {f"{rain:.1f} mm" if rain is not None else "--"}
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with tcol:
        st.markdown(f"""
        <div class="glass" style="padding:11px;min-height:132px;">
            <div style="
                display:flex;justify-content:space-between;
                border-bottom:1px solid rgba(255,255,255,.05);
                padding-bottom:7px;
            ">
                <span class="card-title">05 Terrain Overview</span>
                <span style="color:#fbbf24;font-size:9px;font-weight:700;">
                    {f"{slope:.1f}° Slope" if slope is not None else "--"}
                </span>
            </div>
            <div style="
                display:grid;grid-template-columns:repeat(3,1fr);
                gap:5px;margin-top:9px;text-align:center;
            ">
                <div style="padding:7px;background:rgba(0,0,0,.28);border-radius:8px;">
                    <div class="muted">Slope Stability</div>
                    <div style="font-size:24px;margin-top:5px;">◔</div>
                </div>
                <div style="padding:7px;background:rgba(0,0,0,.28);border-radius:8px;">
                    <div class="muted">Land Use</div>
                    <div style="font-size:24px;margin-top:5px;">🌲</div>
                </div>
                <div style="padding:7px;background:rgba(0,0,0,.28);border-radius:8px;">
                    <div class="muted">Wetness</div>
                    <div style="font-size:24px;margin-top:5px;">💧</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with vcol:
        st.markdown("""
        <div class="glass" style="padding:11px;min-height:132px;">
            <div class="card-title" style="
                border-bottom:1px solid rgba(255,255,255,.05);
                padding-bottom:7px;
            ">06 Vulnerability Metrics</div>

            <div style="
                display:grid;grid-template-columns:1fr 1fr;
                gap:8px;margin-top:9px;
            ">
                <div>
                    <div class="muted">Exposed Elements</div>
                    <div class="small" style="margin-top:5px;">🔴 Critical infrastructure</div>
                    <div class="small">🏠 Buildings: dataset required</div>
                    <div class="small">🛣️ Roads: dataset required</div>
                </div>
                <div>
                    <div class="muted">Population at Risk</div>
                    <div style="font-size:19px;font-weight:700;color:#f87171;">N/A</div>
                    <div class="muted">Dataset required</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ---------------- RECENT ALERTS ----------------
    alert_text = (
        f"High susceptibility detected ({risk_score:.0f}%)"
        if risk_level == "HIGH" and risk_score is not None
        else f"{risk_level} susceptibility according to baseline model"
    )

    st.markdown(f"""
    <div class="glass" style="
        margin-top:10px;padding:11px;
        border-color:rgba(239,68,68,.45);
    ">
        <div style="
            display:flex;justify-content:space-between;
            align-items:center;
        ">
            <div>
                <div style="color:#d1d5db;font-size:11px;font-weight:600;">
                    🔔 Recent Alerts & Notifications
                </div>
                <div class="muted">Stay updated with the latest analysis</div>
            </div>
            <div style="color:#9ca3af;font-size:9px;">View All Alerts →</div>
        </div>

        <div style="
            display:grid;grid-template-columns:repeat(3,1fr);
            gap:8px;margin-top:8px;
        ">
            <div style="
                padding:8px;border-radius:9px;
                background:rgba(127,29,29,.25);
                border:1px solid rgba(239,68,68,.45);
            ">
                <div style="color:#f87171;font-size:9px;font-weight:600;">
                    ⚠️ Risk Status
                </div>
                <div class="muted">{alert_text}</div>
            </div>
            <div style="
                padding:8px;border-radius:9px;
                background:rgba(120,53,15,.22);
                border:1px solid rgba(245,158,11,.35);
            ">
                <div style="color:#fbbf24;font-size:9px;font-weight:600;">
                    🌧️ Weather
                </div>
                <div class="muted">
                    {f"Rainfall: {weather['rain']:.1f} mm" if weather else "Weather unavailable"}
                </div>
            </div>
            <div style="
                padding:8px;border-radius:9px;
                background:rgba(8,47,73,.25);
                border:1px solid rgba(56,189,248,.30);
            ">
                <div style="color:#38bdf8;font-size:9px;font-weight:600;">
                    ⛰️ Terrain Data
                </div>
                <div class="muted">
                    {f"Elevation {elevation:.0f} m • Slope {slope:.1f}°" if elevation is not None else "Awaiting terrain data"}
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ============================================================
# OTHER PAGES
# ============================================================

elif page == "Risk Map":
    st.markdown('<div class="card-title">03 Risk Map</div>', unsafe_allow_html=True)
    m = folium.Map(
        location=[latitude, longitude],
        zoom_start=9,
        tiles="OpenStreetMap",
        control_scale=True,
    )
    folium.TileLayer("OpenTopoMap", name="Terrain").add_to(m)
    folium.Marker(
        [latitude, longitude],
        tooltip="Selected Location",
        icon=folium.Icon(color="red", icon="info-sign"),
    ).add_to(m)
    folium.LayerControl().add_to(m)
    st_folium(m, width=None, height=650, returned_objects=[])

elif page == "Weather":
    st.markdown('<div class="card-title">02 Current Weather</div>', unsafe_allow_html=True)
    if weather:
        a, b = st.columns(2)
        with a:
            st.metric("Temperature", f"{weather['temperature']:.1f} °C")
        with b:
            st.metric("Rainfall", f"{weather['rain']:.1f} mm")
    else:
        st.warning("Weather data unavailable.")

elif page == "Terrain Analysis":
    st.markdown('<div class="card-title">05 Terrain Analysis</div>', unsafe_allow_html=True)
    if elevation is not None:
        a, b = st.columns(2)
        with a:
            st.metric("Elevation", f"{elevation:.1f} m")
        with b:
            st.metric("Slope", f"{slope:.2f}°")
    else:
        st.error("Terrain data unavailable for this location.")

elif page == "Reports":
    st.markdown('<div class="card-title">Reports</div>', unsafe_allow_html=True)
    report = {
        "Latitude": latitude,
        "Longitude": longitude,
        "Elevation_m": elevation,
        "Slope_degrees": slope,
        "Temperature_C": weather["temperature"] if weather else None,
        "Rain_mm": weather["rain"] if weather else None,
        "Risk_score": risk_score,
        "Risk_level": risk_level,
    }
    st.json(report)
    st.download_button(
        "Download Analysis Data",
        data=pd.DataFrame([report]).to_csv(index=False),
        file_name="landslide_analysis.csv",
        mime="text/csv",
        use_container_width=True,
    )

elif page == "Alerts":
    st.markdown('<div class="card-title">Alerts</div>', unsafe_allow_html=True)
    if risk_score is None:
        st.info("Terrain data is required to generate the risk alert.")
    elif risk_level == "HIGH":
        st.error(f"HIGH RISK — {risk_score:.2f}% susceptibility")
    elif risk_level == "MODERATE":
        st.warning(f"MODERATE RISK — {risk_score:.2f}% susceptibility")
    else:
        st.success(f"LOW RISK — {risk_score:.2f}% susceptibility")

    if weather and weather["rain"] > 50:
        st.error(f"Rainfall trigger: {weather['rain']:.1f} mm")

elif page == "Settings":
    st.markdown('<div class="card-title">Settings</div>', unsafe_allow_html=True)
    st.checkbox("Show safety recommendations", value=True)
    st.checkbox("Automatic terrain analysis", value=True)
    st.info(
        "The current baseline model uses Latitude, Longitude, "
        "Elevation and Slope. Geological, vulnerability and "
        "historical inventory layers are not connected yet."
    )
