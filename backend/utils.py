"""backend/utils.py - Main Facade Module re-exporting backend utilities."""

from backend.config import (
    BASE_DIR,
    ENV_FILE,
    AI_BASE_URL,
    AI_API_KEY,
    AI_MODEL,
    EMBEDDING_MODEL,
    STOPWORDS,
    LEMMATIZER,
    setup_nltk,
)
from backend.parsers import parse_resume
from backend.text_processing import (
    SKILL_DB,
    clean_text,
    extract_contact_info,
    extract_skills,
    extract_experience,
    extract_education,
)
from backend.similarity import get_sentence_model, calculate_similarity
from backend.analyzer import analyze_candidates
from backend.ai_client import (
    get_ai_client,
    test_ai_connection,
    generate_with_ai,
    generate_resume_feedback,
    generate_professional_summary,
    generate_job_opportunities,
    generate_skill_development_plan,
    generate_job_profile,
    get_system_status,
    initialize_ai,
)
