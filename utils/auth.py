import streamlit as st


def render_user_menu():
    if "user" not in st.session_state:
        st.session_state.user = None

    _, menu_column = st.columns([7.5, 1])

    with menu_column:
        if st.session_state.user:
            user = st.session_state.user
            
            
            trigger_spacer, trigger_column = st.columns([0.1, 0.9])
            with trigger_column:
                user_popover = st.popover(f"👤 {user['name']}")
                
            with user_popover:
                st.markdown("<div class='login-kicker'>ACCOUNT SETTINGS</div>", unsafe_allow_html=True)
                
                if st.button("Log out", key="logout_button", use_container_width=True):
                    st.session_state.user = None
                    st.rerun()
        else:
            trigger_spacer, trigger_column = st.columns([0.1, 0.9])
            with trigger_column:
                login_popover = st.popover("Sign in  👤")

            with login_popover:
                st.markdown(
                    "<div class='login-kicker'>ACCOUNT ACCESS</div><h3 class='login-title'>Welcome back</h3><p class='login-copy'>Sign in to unlock your reports and saved locations.</p>",
                    unsafe_allow_html=True
                )
                name = st.text_input("Name", key="login_name")
                email = st.text_input("Email", key="login_email")
                password = st.text_input("Password", type="password", key="login_password")

                if st.button("Continue securely", key="login_continue_button", type="primary"):
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
