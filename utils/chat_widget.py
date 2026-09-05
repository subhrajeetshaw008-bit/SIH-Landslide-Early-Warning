import streamlit as st

from chatbot.news_agent import news_response
from chatbot.risk_agent import risk_response
from chatbot.router import route_query
from chatbot.weather_agent import weather_response
from chatbot.mistral_client import ask_mistral


def render_chat_widget(latitude, longitude):
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "dashboard_chat_open" not in st.session_state:
        st.session_state.dashboard_chat_open = False

    launcher_label = "Close AI assistant" if st.session_state.dashboard_chat_open else "Open AI assistant"
    if st.button("✦", key="dashboard_chat_launcher", help=launcher_label):
        st.session_state.dashboard_chat_open = not st.session_state.dashboard_chat_open
        st.rerun()

    if not st.session_state.dashboard_chat_open:
        return

    with st.container():
        st.markdown(
            """
            <div class="dashboard-chat-popup-anchor"></div>
            <div class="dashboard-chat-header">
                <div class="dashboard-chat-avatar">✦</div>
                <div><div class="assistant-eyebrow">LANDSLIDE AI</div><h3>Field assistant</h3><p>Quick answers for your selected location.</p></div>
            </div>
            """,
            unsafe_allow_html=True
        )

        conversation = st.container(height=210)
        with conversation:
            if not st.session_state.messages:
                st.markdown("<div class='dashboard-chat-empty'>Ask about risk, weather, terrain, or safety planning.</div>", unsafe_allow_html=True)
            for message in st.session_state.messages[-4:]:
                with st.chat_message(message["role"]):
                    st.write(message["content"])

        input_column, send_column = st.columns([5, 1])
        with input_column:
            prompt = st.text_input("Message", placeholder="Ask about this location...", label_visibility="collapsed", key="dashboard_chat_message")
        with send_column:
            send_clicked = st.button("Send", key="dashboard_chat_send", type="primary", use_container_width=True)

        close_column, full_column = st.columns(2)
        with close_column:
            close_clicked = st.button("Close", key="dashboard_chat_close", use_container_width=True)
        with full_column:
            full_clicked = st.button("Open Full Assistant", key="dashboard_full_assistant", use_container_width=True)

        if close_clicked:
            st.session_state.dashboard_chat_open = False
            st.rerun()
        if full_clicked:
            st.switch_page("pages/7_AI_Assistant.py")
        if not send_clicked or not prompt.strip():
            return

    prompt = prompt.strip()
    st.session_state.messages.append({"role": "user", "content": prompt})
    route = route_query(prompt)

    if route["type"] == "weather":
        response = weather_response(latitude, longitude)
    elif route["type"] == "risk":
        response = risk_response(latitude, longitude)
    elif route["type"] == "news":
        response = news_response(prompt)
    else:
        response = ask_mistral(
            [
                {
                    "role": "system",
                    "content": "You are a concise landslide safety assistant."
                },
                *st.session_state.messages
            ]
        )

    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()
