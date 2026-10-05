import os

import streamlit as st


MODEL_NAME = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")


def get_groq_api_key() -> str:
    key = os.getenv("GROQ_API_KEY")

    if not key:
        try:
            key = st.secrets.get("GROQ_API_KEY")
        except Exception:
            key = None

    if not key:
        raise RuntimeError(
            "GROQ_API_KEY is missing. Add it to Streamlit Cloud → "
            "App settings → Secrets."
        )

    return str(key)
