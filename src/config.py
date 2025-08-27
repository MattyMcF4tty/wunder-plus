from dotenv import load_dotenv
import os
from pathlib import Path

# Load .env file
load_dotenv()

DOMAIN_NAME = os.getenv("DOMAIN")
DEFAULT_PAGE = f"https://{DOMAIN_NAME}/site/login#/dashboard"
CACHE_FILE = Path(__file__).parent / 'cache' / 'cache.json'

# Page tags
AUTH_FLOW_TAG = "WUNDER_AUTH_FLOW"
LISTENER_TAG = 'LISTENING'