from langchain_google_genai import ChatGoogleGenerativeAI

from config.config import GeminiSettings

llm = ChatGoogleGenerativeAI(model=GeminiSettings.Gemini_model_name, 
api_key=GeminiSettings.GEMINI_API_KEY,
temperature=1.0,  # Gemini 3.0+ defaults to 1.0
max_tokens=1000,
timeout=60,
max_retries=2,
)
