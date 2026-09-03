SYSTEM_PROMPT = """
You are LandslideGPT, an advanced AI Disaster Intelligence Assistant designed for landslide risk assessment, terrain analysis, weather interpretation, disaster preparedness, and emergency decision support.

Your primary objective is to help users understand, analyze, predict, and mitigate landslide-related risks using available weather data, terrain information, machine learning predictions, and real-time information.

CORE RESPONSIBILITIES:

1. Landslide Risk Analysis
- Interpret landslide risk predictions.
- Explain why a location may be at risk.
- Identify major contributing factors such as rainfall, slope, elevation, soil saturation, and terrain conditions.
- Communicate risk levels clearly.

2. Weather Intelligence
- Analyze rainfall, humidity, temperature, and weather conditions.
- Explain how weather influences landslide probability.
- Highlight severe weather situations that may increase risk.

3. Terrain Intelligence
- Interpret elevation and terrain characteristics.
- Explain the impact of steep slopes and mountainous regions.
- Provide terrain-based observations when relevant.

4. Disaster Awareness
- Educate users about landslides, floods, erosion, and related natural hazards.
- Explain disaster concepts in simple language when requested.
- Adapt explanations for students, researchers, officials, or general users.

5. Safety Guidance
- Provide practical preparedness recommendations.
- Suggest evacuation readiness when appropriate.
- Encourage users to follow local authority guidance during emergencies.

6. News & Situation Awareness
- Summarize recent disaster-related information when available.
- Highlight important developments.
- Distinguish between confirmed information and uncertainty.

COMMUNICATION RULES:

- Be accurate, structured, and concise.
- Use bullet points when useful.
- Explain technical concepts clearly.
- When uncertainty exists, state it explicitly.
- Never fabricate weather data, terrain data, risk scores, or news.
- If data is unavailable, clearly say so.
- Avoid exaggerated or sensational language.

RISK COMMUNICATION RULES:

For LOW risk:
- Explain that risk is currently limited.
- Mention that conditions can change.

For MODERATE risk:
- Explain contributing factors.
- Suggest monitoring weather and local advisories.

For HIGH risk:
- Clearly explain the reasons.
- Recommend heightened caution.
- Encourage attention to official alerts and emergency guidance.

STYLE:

- Professional
- Calm
- Analytical
- Evidence-driven
- Helpful
- Safety-focused

Always prioritize public safety, factual accuracy, and clear communication.
"""

import streamlit as st

from chatbot.mistral_client import ask_mistral

from chatbot.router import route_query

from chatbot.weather_agent import (
    weather_response
)

from chatbot.risk_agent import (
    risk_response
)

from chatbot.news_agent import (
    news_response
)

st.set_page_config(
    page_title="Landslide AI Assistant",
    page_icon="✦",
    layout="wide"
)

with open("assets/styles.css") as css_file:
    st.markdown(f"<style>{css_file.read()}</style>", unsafe_allow_html=True)

latitude = st.session_state.get(
    "latitude",
    24.5
)

longitude = st.session_state.get(
    "longitude",
    93.5
)

st.markdown("<div class='assistant-workspace-anchor'></div>", unsafe_allow_html=True)
st.markdown(
    f"""
    <div class="assistant-hero">
        <div class="assistant-hero-topline">
            <div class="assistant-hero-identity">
                <div class="main-brand-mark">▲</div>
                <div>
                    <div class="assistant-kicker">LANDSLIDE INTELLIGENCE</div>
                    <h1>LandslideGPT</h1>
                    <p>Your calm, field-ready guide to risk, weather and terrain.</p>
                </div>
            </div>
            <div class="assistant-status"><span></span> Online</div>
        </div>
        <div class="assistant-context-row">
            <span>Monitoring location</span>
            <strong>{latitude:.4f}, {longitude:.4f}</strong>
            <span class="context-separator">•</span>
            <span>Safety intelligence mode</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# =========================
# CHAT HISTORY
# =========================

if "messages" not in st.session_state:

    st.session_state.messages = []

quick_prompt = None

if not st.session_state.messages:
    st.markdown(
        """
        <div class="assistant-welcome">
            <div class="welcome-spark">✦</div>
            <h2>How can I help you prepare?</h2>
            <p>Ask a focused question and I will connect the answer to your selected location.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown("<div class='assistant-prompt-label'>Start with a question</div>", unsafe_allow_html=True)
    prompt_columns = st.columns(3)
    quick_prompts = [
        ("Risk snapshot", "What is the current landslide risk?"),
        ("Weather impact", "How is the current weather affecting risk?"),
        ("Safety plan", "What should I do to prepare for a landslide?"),
    ]
    for column, (label, prompt_text) in zip(prompt_columns, quick_prompts):
        with column:
            if st.button(label, key=f"assistant_quick_{label}", use_container_width=True):
                quick_prompt = prompt_text

# =========================
# SHOW OLD MESSAGES
# =========================

for msg in st.session_state.messages:

    with st.chat_message(
        msg["role"]
    ):

        st.write(
            msg["content"]
        )

# =========================
# USER INPUT
# =========================

prompt = quick_prompt
with st.form("assistant_composer", clear_on_submit=True, border=False):
    st.markdown("<div class='assistant-composer-anchor'></div>", unsafe_allow_html=True)
    input_column, send_column = st.columns([8, 1.2])
    with input_column:
        typed_prompt = st.text_input(
            "Message",
            placeholder="Ask about risk, weather, terrain or safety...",
            label_visibility="collapsed"
        )
    with send_column:
        send_clicked = st.form_submit_button("Send", use_container_width=True)

    if send_clicked and typed_prompt.strip():
        prompt = typed_prompt.strip()

# =========================
# PROCESS MESSAGE
# =========================

if prompt:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):

        st.write(prompt)

    # ---------------------
    # ROUTER
    # ---------------------

    route = route_query(
        prompt
    )

    # ---------------------
    # WEATHER AGENT
    # ---------------------

    if route["type"] == "weather":

        response = weather_response(
            latitude,
            longitude
        )

    # ---------------------
    # RISK AGENT
    # ---------------------

    elif route["type"] == "risk":

        response = risk_response(
            latitude,
            longitude
        )
    #----------------------
    # NEWS RESPONSE
    #----------------------

    elif route["type"] == "news":

        response = news_response(
            prompt
        )
    # ---------------------
    # MISTRAL
    # ---------------------

    else:

        mistral_messages = [
            {
                "role":"system",
                "content": SYSTEM_PROMPT
            }
        ]

        for msg in st.session_state.messages:

            mistral_messages.append(
                {
                    "role": msg["role"],
                    "content": msg["content"]
                }
            )

        response = ask_mistral(
            mistral_messages
        )

    # ---------------------
    # SHOW RESPONSE
    # ---------------------

    with st.chat_message(
            "assistant"
        ):

        st.write(
            response
        )

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )