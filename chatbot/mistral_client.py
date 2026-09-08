import os
import time
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from google import genai

load_dotenv(
    dotenv_path=Path(__file__).resolve().parents[1] / ".env"
)

def ask_mistral(messages):

    api_key = os.getenv("GEMINI_API_KEY", "")

    if not api_key:
        try:
            api_key = st.secrets.get("GEMINI_API_KEY", "")
        except Exception:
            api_key = ""

    if not api_key:
        return "Gemini API Key not found."

    try:
        client = genai.Client(api_key=api_key)

        prompt = ""

        for msg in messages:
            role = msg.get("role", "")
            content = msg.get("content", "")

            prompt += f"{role.upper()}: {content}\n"

        # Retry up to 3 times if Gemini is overloaded
        for attempt in range(3):

            try:
                response = client.models.generate_content(
                    model="gemini-3.6-flash",
                    contents=prompt
                )

                return response.text

            except Exception as error:

                error_text = str(error)

                if "503" in error_text or "UNAVAILABLE" in error_text:
                    time.sleep(5 * (attempt + 1))
                    continue

                raise error

        return (
            "Gemini servers are currently experiencing high demand. "
            "Please try again in a few moments."
        )

    except Exception as error:
        return (
            "The AI assistant request failed: "
            f"{type(error).__name__}: {error}"
        )
