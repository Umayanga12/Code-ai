# from langchain_google_vertexai import VertexAI

from langchain_openai import ChatOpenAI
from config.config import settings

model_coding = ChatOpenAI(model=settings.OPENAI_MODEL_NAME, api_key=settings.OPENAI_API_KEY)


# # To use model
# model_coding = VertexAI(model_name="gemini-2.5-pro")