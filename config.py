import os
from dotenv import load_dotenv

load_dotenv()

# Выбор LLM провайдера: 'openrouter', 'openai', 'anthropic', и т.д.
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openrouter").lower()

# Настройки OpenRouter API
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

DEFAULT_MODEL = "google/gemini-3-flash-preview" 
DEFAULT_VISION_MODEL = "google/gemini-3-flash-preview" 

MAX_FILE_SIZE_MB = 50
SUPPORTED_IMAGE_FORMATS = {'.png', '.jpg', '.jpeg', '.webp', '.gif', '.bmp'}
SUPPORTED_PDF_FORMATS = {'.pdf'}
SUPPORTED_FORMATS = SUPPORTED_IMAGE_FORMATS | SUPPORTED_PDF_FORMATS

MAX_TOKENS = 4000
TEMPERATURE = 0.7

IMAGE_MAX_SIZE = (2048, 2048) 
IMAGE_MAX_SIZE_MB = 20 
