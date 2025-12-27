# app/config.py
import os

from dotenv import load_dotenv
from pydantic import BaseModel
from tavily import TavilyClient

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

class GeminiSettings(BaseModel):
    Gemini_API_Key: str = ""
    Gemini_model_name : str = ""


GeminiSettings = GeminiSettings(
    Gemini_API_Key=os.getenv("GEMINI_API_KEY") or "",
    Gemini_model_name=os.getenv("GEMINI_MODEL_NAME", "gemini-2.5-pro")
)


class DBSettings(BaseModel):
    DB_USER_NAME: str = ""
    DB_PASSWORD : str = ""
    DB_HOST : str =  ""
    DB_NAME : str = ""

dbSettings = DBSettings(
    DB_HOST= os.getenv("DB_HOST")  or "",
    DB_PASSWORD = os.getenv("DB_PASSWORD") or "",
    DB_USER_NAME= os.getenv("DB_USERNAME") or "",
    DB_NAME= os.getenv("DB_NAME") or "",
)
#print(dbSettings)

if dbSettings.DB_HOST == "" or dbSettings.DB_PASSWORD == "" or dbSettings.DB_USER_NAME == "" or dbSettings.DB_NAME == "":
    raise ValueError("Database configurations not set")


tavily_client = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])

