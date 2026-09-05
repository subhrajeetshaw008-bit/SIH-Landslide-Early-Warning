import streamlit as st
from online_terrain import get_online_terrain


@st.cache_data(ttl=3600, show_spinner=False)
def get_terrain(latitude, longitude):
    try:
        elevation, slope = get_online_terrain(
            latitude,
            longitude
        )

        return {
            "elevation": elevation,
            "slope": slope
        }

    except Exception:
        return None