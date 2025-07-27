import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    MODEL_NAME = os.getenv("MODEL_NAME", "gemma2:1b")
    MAX_REVIEWS_PER_SUMMARY = int(os.getenv("MAX_REVIEWS_PER_SUMMARY", "10"))
    DEFAULT_MAX_TOKENS = int(os.getenv("DEFAULT_MAX_TOKENS", "400"))
    REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "60"))