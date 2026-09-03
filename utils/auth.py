import streamlit as st


def render_user_menu():
    if "user" not in st.session_state:
        st.session_state.user = None

    _, menu_column = st.columns([5.5, 1.5])

    with menu_column:
        if st.session_state.user:
            user = st.session_state.user
            st.markdown(
                f"<div class='user-badge'><span>👤</span><strong>{user['name']}</strong></div>",
                unsafe_allow_html=True
            )
            if st.button("Log out", key="logout_button"):
                st.session_state.user = None
                st.rerun()
        else:
            with st.popover("Sign in  👤"):
                st.markdown(
                    "<div class='login-kicker'>ACCOUNT ACCESS</div><h3 class='login-title'>Welcome back</h3><p class='login-copy'>Sign in to unlock your reports and saved locations.</p>",
                    unsafe_allow_html=True
                )
                name = st.text_input("Name", key="login_name")
                email = st.text_input("Email", key="login_email")
                password = st.text_input("Password", type="password", key="login_password")

                if st.button("Continue securely", type="primary", use_container_width=True):
                    if not name.strip() or not email.strip() or not password:
                        st.error("Enter your name, email and password.")
                    else:
                        st.session_state.user = {
                            "name": name.strip(),
                            "email": email.strip()
                        }
                        st.success("Logged in successfully.")
                        st.rerun()


def require_login():
    if not st.session_state.get("user"):
        st.warning("Please log in to view your personal report.")
        st.stop()

    return st.session_state.user