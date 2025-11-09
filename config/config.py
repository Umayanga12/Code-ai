# app/config.py
import os

from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()


class Settings(BaseModel):
    """Loads settings from environment variables."""

    OPENAI_API_KEY: str = ""
    OPENAI_MODEL_NAME: str = "gpt-4.1"


settings = Settings(
    OPENAI_API_KEY=os.getenv("OPENAI_API_KEY") or "",
    OPENAI_MODEL_NAME=os.getenv("OPENAI_MODEL_NAME", "gpt-4.1"),
)

# Fail fast if essential keys are missing
if not settings.OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable not set.")
