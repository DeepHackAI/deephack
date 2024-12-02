import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# OpenAI API Configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Model Configuration
DEFAULT_MODEL = "gpt-3.5-turbo"
MAX_TOKENS = 2000

# ChatGLM Configuration
CHATGLM_MODEL = "THUDM/chatglm-6b"
CHATGLM_REVISION = "v1.1.0"

# Evaluation Configuration
EVAL_TEMPERATURE = 0.5
EVAL_TOP_P = 0.01

# Security Configuration
WORD_EXCLUSION_LIST = [
    # Add sensitive or forbidden words here
]

# Response Templates
SECURITY_BLOCK_MESSAGE = "Sorry, I cannot respond to your request due to security restrictions."

# Logging Configuration
LOG_LEVEL = "INFO"

# Function to validate API keys
def validate_api_keys():
    if not OPENAI_API_KEY:
        raise ValueError("OpenAI API key not found in environment variables")
    return True