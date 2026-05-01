from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv


DEFAULT_OPENAI_MODEL = "gpt-5-mini"
DISABLE_OPENAI_ENV = "AGENTIC_SITE_FACTORY_DISABLE_OPENAI"


@dataclass(frozen=True)
class OpenAISettings:
    api_key: str
    model: str
    disabled: bool = False

    @property
    def enabled(self) -> bool:
        return bool(self.api_key) and not self.disabled


def truthy(value: str | None) -> bool:
    if value is None:
        return False

    return value.strip().lower() in {"1", "true", "yes", "y", "on"}


def streamlit_secret(name: str) -> str:
    try:
        import streamlit as st

        value = st.secrets.get(name, "")
        return str(value) if value else ""
    except Exception:
        return ""


def load_openai_settings() -> OpenAISettings:
    load_dotenv()

    disabled = truthy(os.getenv(DISABLE_OPENAI_ENV))
    api_key = os.getenv("OPENAI_API_KEY", "") or streamlit_secret("OPENAI_API_KEY")
    model = (
        os.getenv("OPENAI_MODEL", "")
        or streamlit_secret("OPENAI_MODEL")
        or DEFAULT_OPENAI_MODEL
    )

    if api_key and not os.getenv("OPENAI_API_KEY"):
        os.environ["OPENAI_API_KEY"] = api_key

    return OpenAISettings(api_key=api_key, model=model, disabled=disabled)
