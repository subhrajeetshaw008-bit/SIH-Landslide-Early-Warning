import os
from pathlib import Path

from dotenv import load_dotenv
from mistralai.client import Mistral

load_dotenv(
    dotenv_path=Path(__file__).resolve().parents[1] / ".env"
)

def ask_mistral(messages):
    api_key = os.getenv("MISTRAL_API_KEY")

    if not api_key:
        return "Mistral AI is not configured. Add MISTRAL_API_KEY to the .env file for general questions."

    client = Mistral(api_key=api_key)

    response = client.chat.complete(

        model="mistral-small-latest",

        messages=messages

    )

    return response.choices[0].message.content