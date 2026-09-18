import streamlit as st
from google import genai

_client = None

def _get_client():
    global _client
    if _client is None:
        api_key = st.secrets.get("GEMINI_API_KEY")
        _client = genai.Client(api_key=api_key)
    return _client

def ask_gemini(prompt: str) -> str:
    try:
        client = _get_client()
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"Sorry, I couldn't process that right now. ({e})"