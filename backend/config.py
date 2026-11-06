import os
import logging
import nltk
from dotenv import load_dotenv

# Base Directory & Env Loading
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_FILE = os.path.join(BASE_DIR, ".env")
load_dotenv(ENV_FILE, override=True)

# Logging Setup
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# AI & Model Configuration
AI_BASE_URL = os.getenv("AI_BASE_URL", "https://generativelanguage.googleapis.com/v1beta/openai/")
AI_API_KEY = os.getenv("AI_API_KEY") or os.getenv("GEMINI_API_KEY") or os.getenv("HF_TOKEN") or ""
AI_MODEL = os.getenv("AI_MODEL") or "gemini-3.8-flash"
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")

# NLTK Setup
def setup_nltk():
    """Download required NLTK resources silently if not available."""
    resources = [
        ("tokenizers/punkt", "punkt"),
        ("tokenizers/punkt_tab", "punkt_tab"),
        ("corpora/stopwords", "stopwords"),
        ("corpora/wordnet", "wordnet"),
    ]
    for res_path, res_name in resources:
        try:
            nltk.data.find(res_path)
        except LookupError:
            try:
                nltk.download(res_name, quiet=True)
            except Exception as e:
                logging.warning("Failed NLTK download %s: %s", res_name, e)

setup_nltk()

try:
    from nltk.corpus import stopwords
    from nltk.stem import WordNetLemmatizer
    STOPWORDS = set(stopwords.words("english"))
    LEMMATIZER = WordNetLemmatizer()
except Exception as e:
    logging.warning("Could not load NLTK stopwords/lemmatizer: %s", e)
    STOPWORDS = set()
    LEMMATIZER = None
