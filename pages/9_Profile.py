import streamlit as st

st.set_page_config(
    page_title="Landslide AI Profile",
    page_icon="👤",
    layout="wide"
)

with open("assets/styles.css") as css_file:
    st.markdown(f"<style>{css_file.read()}</style>", unsafe_allow_html=True)


st.markdown("<div class='profile-shell-anchor'></div>", unsafe_allow_html=True)
st.markdown(
    """
    <div class="weather-header profile-header">
        <div class="main-brand-mark">▲</div>
        <div>
            <div class="assistant-kicker">LANDSLIDE INTELLIGENCE</div>
            <h1>Your profile</h1>
            <p>Manage the account details connected to your research workspace.</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

user = st.session_state.get("user")
if not user:
    st.info("Sign in from the account control to view your profile details.")
    st.stop()

st.markdown("<div class='section-kicker'>01 <span>Account Information</span></div>", unsafe_allow_html=True)
st.markdown(
    f"""
    <div class='card profile-card'>
        <div class='profile-avatar'>{user['name'][:2].upper()}</div>
        <div>
            <div class='card-kicker'>Account holder</div>
            <h2>{user['name']}</h2>
            <p>{user['email']}</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("<div class='section-kicker'>02 <span>Saved Preferences</span></div>", unsafe_allow_html=True)
preference_columns = st.columns(3)
with preference_columns[0]:
    st.metric("Mobile alerts", "Enabled" if st.session_state.get("alert_enabled") else "Off")
with preference_columns[1]:
    st.metric("Saved location", f"{st.session_state.get('latitude', 24.5):.2f}, {st.session_state.get('longitude', 93.5):.2f}")
with preference_columns[2]:
    st.metric("Conversations", len([message for message in st.session_state.get("messages", []) if message["role"] == "user"]))

st.caption("Your password is never displayed or stored in this profile view.")