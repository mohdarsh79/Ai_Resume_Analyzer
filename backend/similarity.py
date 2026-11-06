import logging
from functools import lru_cache
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from backend.config import EMBEDDING_MODEL
from backend.text_processing import clean_text

try:
    from sentence_transformers import SentenceTransformer, util
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SentenceTransformer, util = None, None
    SENTENCE_TRANSFORMERS_AVAILABLE = False
    logging.warning("sentence-transformers unavailable. TF-IDF fallback will be used.")

@lru_cache(maxsize=1)
def get_sentence_model():
    """Load and cache the sentence-transformer embedding model."""
    if not SENTENCE_TRANSFORMERS_AVAILABLE:
        return None
    try:
        logging.info("Loading embedding model: %s", EMBEDDING_MODEL)
        return SentenceTransformer(EMBEDDING_MODEL)
    except Exception as e:
        logging.error("Could not load embedding model: %s", e)
        return None

def calculate_similarity(resume_text: str, jd_text: str) -> float:
    """Calculate semantic similarity with fallback to TF-IDF cosine similarity."""
    if not resume_text or not jd_text:
        return 0.0

    model = get_sentence_model()
    if model is not None:
        try:
            emb_res = model.encode(resume_text, convert_to_tensor=True)
            emb_jd = model.encode(jd_text, convert_to_tensor=True)
            score = float(util.cos_sim(emb_res, emb_jd)[0][0])
            return max(0.0, min(1.0, score))
        except Exception as e:
            logging.warning("Embedding similarity failed (%s). Using TF-IDF fallback.", e)

    try:
        c_res, c_jd = clean_text(resume_text), clean_text(jd_text)
        if not c_res or not c_jd:
            return 0.0
        matrix = TfidfVectorizer().fit_transform([c_res, c_jd])
        score = float(cosine_similarity(matrix[0:1], matrix[1:2])[0][0])
        return max(0.0, min(1.0, score))
    except Exception as e:
        logging.error("TF-IDF similarity failed: %s", e)
        return 0.0
