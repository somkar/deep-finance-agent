import os

from dotenv import load_dotenv


load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1:8b")


def require_tavily_api_key() -> str:
    if not TAVILY_API_KEY:
        raise RuntimeError("TAVILY_API_KEY is not set. Configure it in .env before running the agent.")
    return TAVILY_API_KEY
