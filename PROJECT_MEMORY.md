# AI Resume Screening & Career Assistant - Project Context & Memory

## Overview
**AI Resume Screening & Career Assistant** is a Streamlit-based web application that parses candidate resumes (PDF/TXT), analyzes them against a target Job Description (JD), ranks candidates using a hybrid scoring algorithm (semantic similarity + skill matching), and generates AI-driven career advice and ATS optimization insights using Google Gemini (via OpenAI-compatible API endpoints).

---

## Architecture & Directory Structure

```
.
├── app.py                      # Main entrypoint: Streamlit page config & multi-page navigation router
├── requirements.txt            # Python dependencies (Streamlit, PyPDF2, pdfplumber, sentence-transformers, openai, etc.)
├── .env                        # Configuration (AI_BASE_URL, AI_API_KEY, AI_MODEL, etc.)
│
├── backend/                    # Core logic and services
│   ├── __init__.py
│   ├── config.py               # Environment loading, API constants, NLTK resource bootstrapping
│   ├── ai_client.py            # Gemini / OpenAI client wrapper, fallback model retry loop, AI prompts
│   ├── analyzer.py             # Candidate ranking engine (similarity 60% + skill ratio 40%)
│   ├── parsers.py              # Resume extraction from PDF (pdfplumber + PyPDF2 fallback) and TXT
│   ├── similarity.py           # Cosine similarity using SentenceTransformers (all-MiniLM-L6-v2) or TF-IDF
│   ├── text_processing.py      # Regex & NLP extraction for skills, contact info, experience, education
│   └── utils.py                # Helper utilities and string cleaners
│
└── frontend/                   # UI views and components
    ├── __init__.py
    ├── state.py                # Streamlit session state management & AI generator trigger helpers
    ├── styles.py               # Custom CSS styles (cards, badges, metric displays)
    └── views/
        ├── home.py             # Overview dashboard and feature highlights
        ├── upload.py           # Resume & JD upload/paste interface + batch processing trigger
        ├── ranking.py          # Candidate leaderboard table, match scores, contact exports
        ├── feedback.py         # AI-powered ATS feedback and bullet point rewrites
        ├── job_opportunities.py # Recommended job roles and career pivots
        ├── skill_plan.py       # 30-60-90 day skill development roadmaps
        └── analytics.py        # Visual charts (score distribution, skill overlap, keyword gaps)
```

---

## Core Workflows & Logic

1. **Document Ingestion & Parsing (`backend/parsers.py`)**:
   - Reads `.pdf` files using `pdfplumber`, falling back to `PyPDF2` if extraction encounters errors.
   - Decodes plain `.txt` files with UTF-8 support.

2. **Information Extraction (`backend/text_processing.py`)**:
   - Contact extraction: Regex for email, phone numbers, and LinkedIn profile URLs.
   - Skill extraction: Matches text against a curated list of technical and soft skills.
   - Experience & Education: Regex and NLP patterns to detect years of experience and degrees.

3. **Hybrid Ranking Algorithm (`backend/analyzer.py` & `backend/similarity.py`)**:
   - **Semantic Similarity (60% weight)**: Encodes resume and JD text into vector embeddings using `all-MiniLM-L6-v2` (`sentence-transformers`) and calculates cosine similarity. If the model is not loaded, it falls back to `TfidfVectorizer`.
   - **Skill Ratio (40% weight)**: Calculated as `len(matched_skills) / len(jd_skills)`.
   - **Overall Score**: `(Similarity * 0.60) + (Skill Ratio * 0.40)`.

4. **AI Generation with Gemini (`backend/ai_client.py`)**:
   - Connects to Google Generative Language OpenAI-compatible endpoint: `https://generativelanguage.googleapis.com/v1beta/openai/`.
   - Default model: `gemini-3.8-flash` (with fallback candidates like `gemini-3.7-flash`).
   - Four dedicated prompt workflows:
     - `generate_resume_feedback`: Executive match summary, strengths, skill gaps, bullet point rewrites, missing ATS keywords.
     - `generate_professional_summary`: 3 tailored variants (results-driven, stack-focused, ATS standard).
     - `generate_job_opportunities`: Primary/adjacent roles and target companies.
     - `generate_skill_development_plan`: 30-60-90 day structured learning roadmap.

---

## Environment Variables (`.env`)
- `AI_BASE_URL`: Endpoint URL (defaults to Gemini v1beta OpenAI compatibility layer).
- `AI_API_KEY` / `GEMINI_API_KEY`: API key for Gemini.
- `AI_MODEL`: Active model name (e.g., `gemini-3.8-flash`).
- `EMBEDDING_MODEL`: Sentence transformer model name (default: `all-MiniLM-L6-v2`).

---

## Running the Project
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the Streamlit application
streamlit run app.py
```

