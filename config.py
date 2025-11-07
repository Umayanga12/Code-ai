from pydantic import BaseModel


class Settings(BaseModel):
    model_name: str
    temperature: float = 0.7


settings = Settings(
    model_name="hf.co/bartowski/Llama-3.2-1B-Instruct-GGUF", temperature=0.7
)


if not settings.model_name:
    raise ValueError("Model name is required")
