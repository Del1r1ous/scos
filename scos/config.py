"""Configuration for SCOS-PSST Chain"""

import os
from pathlib import Path

# Project root
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)

# Database
DATABASE_PATH = DATA_DIR / "chain.db"
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

# API Configuration
API_HOST = os.getenv("SCOS_API_HOST", "127.0.0.1")
API_PORT = int(os.getenv("SCOS_API_PORT", "5000"))
API_DEBUG = os.getenv("SCOS_API_DEBUG", "False").lower() == "true"

# Witness Configuration
WITNESS_MODELS = {
    "W1": {"name": "Claude-3.5-Sonnet-Physics", "api": "anthropic"},
    "W2": {"name": "GPT-4-Philosophy", "api": "openai"},
    "W3": {"name": "Gemini-Ethics", "api": "google"},
    "W4": {"name": "Llama-3-History", "api": "meta"},
    "W5": {"name": "Mistral-Systems", "api": "mistral"},
    "W6": {"name": "Claude-3-Haiku-Phenomenology", "api": "anthropic"},
    "W7": {"name": "Ensemble-Unwitnessed", "api": "ensemble"},
}

# Consensus Parameters
CONSENSUS_THRESHOLD = 0.800
MINIMUM_WITNESSES = 5
MAXIMUM_WITNESSES = 7

# Chain Parameters
GENESIS_BLOCK_ID = 0
BLOCK_REWARD = 1.0

# Logging
LOG_LEVEL = os.getenv("SCOS_LOG_LEVEL", "INFO")
LOG_FILE = DATA_DIR / "scos.log"

# Security
SIGNING_KEY = os.getenv("SCOS_SIGNING_KEY", None)
ENCRYPTION_ENABLED = os.getenv("SCOS_ENCRYPTION", "True").lower() == "true"
