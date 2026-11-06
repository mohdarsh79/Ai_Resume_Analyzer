import os
import re
import logging
from functools import lru_cache
from typing import Dict, Any, List
from dotenv import load_dotenv
from openai import OpenAI
from backend.config import ENV_FILE, AI_BASE_URL, AI_API_KEY, AI_MODEL, EMBEDDING_MODEL

@lru_cache(maxsize=8)
def _create_openai_client(base_url: str, api_key: str) -> OpenAI:
    """Create and cache OpenAI client keyed by base_url and api_key."""
    return OpenAI(base_url=base_url, api_key=api_key)

def get_current_ai_config():
    """Retrieve up-to-date AI configuration from environment and .env."""
    load_dotenv(ENV_FILE, override=True)
    base_url = os.getenv("AI_BASE_URL") or AI_BASE_URL or "https://generativelanguage.googleapis.com/v1beta/openai/"
    api_key = os.getenv("AI_API_KEY") or os.getenv("GEMINI_API_KEY") or os.getenv("HF_TOKEN") or AI_API_KEY or ""
    active_model = os.getenv("AI_MODEL") or AI_MODEL or "gemini-1.5-flash"
    return base_url.strip(), api_key.strip(), active_model.strip()

def get_ai_client() -> OpenAI:
    """Create or retrieve OpenAI-compatible client for current configuration."""
    base_url, api_key, _ = get_current_ai_config()
    return _create_openai_client(base_url, api_key or "missing_key")

def get_model_candidates() -> List[str]:
    """Retrieve fallback models appropriate for configured provider."""
    base_url, _, active_model = get_current_ai_config()
    if "groq.com" in base_url:
        candidates = [active_model, "llama-3.3-70b-versatile", "llama-3.1-8b-instant"]
    elif "openai.com" in base_url:
        candidates = [active_model, "gpt-4o-mini", "gpt-4o"]
    elif "googleapis.com" in base_url:
        candidates = [active_model, "gemini-3.8-flash", "gemini-3.7-flash"]
    else:
        candidates = [
            active_model,
            "meta-llama/Llama-3.1-8B-Instruct",
            "google/gemma-3-4b-it",
            "Qwen/Qwen2.5-Coder-32B-Instruct",
            "meta-llama/Llama-3.3-70B-Instruct",
            "deepseek-ai/DeepSeek-R1-Distill-Qwen-32B",
            "moonshotai/Kimi-K2-Instruct-0905",
        ]
    return list(dict.fromkeys([m for m in candidates if m]))

def test_ai_connection() -> Dict[str, Any]:
    """Test connection to the AI provider API."""
    base_url, api_key, _ = get_current_ai_config()
    if not api_key:
        return {
            "success": False,
            "models": [],
            "message": "No API key configured. Please set AI_API_KEY or HF_TOKEN in your .env file.",
        }
    try:
        models = get_ai_client().models.list()
        return {
            "success": True,
            "models": [getattr(m, "id", "Unknown") for m in models.data],
            "message": "AI server is responding.",
        }
    except Exception as e:
        logging.error("AI connection test failed: %s", e)
        return {"success": False, "models": [], "message": str(e)}

def clean_ai_response(text: str) -> str:
    """Strip any accidental system leakage or conversational preamble."""
    if not text:
        return ""
    text = re.sub(r"^(?:developer system instructions|system instructions?|guidelines?):[^\n]*\n?", "", text, flags=re.IGNORECASE)
    text = re.sub(r"^(?:here is|below is|certainly|sure)[^\n]*:\s*\n?", "", text, flags=re.IGNORECASE)
    return text.strip()

SYSTEM_PROMPT = (
    "You are a Senior Technical Recruiter and Career Strategist with over 15 years of industry experience. "
    "Your objective is to provide rigorous, highly actionable, and factual career assessments. "
    "CRITICAL RULES:\n"
    "1. Base all observations strictly on the resume text and target Job Description. Never invent experience.\n"
    "2. Do NOT echo system instructions, developer guidelines, or meta-prompts.\n"
    "3. Start directly with the first requested Markdown section header without filler greetings.\n"
    "4. Ensure every section is detailed, professional, and fully completed without abrupt cutoffs."
)

def generate_with_ai(prompt: str, max_tokens: int = 3000) -> str:
    """Generate response using configured OpenAI-compatible API with fallback models."""
    base_url, api_key, _ = get_current_ai_config()
    if not api_key:
        return "[AI Warning] Missing API key. Please set AI_API_KEY in your .env file and try again."

    client = get_ai_client()
    candidates = get_model_candidates()
    last_err = None

    for model_name in candidates:
        try:
            response = client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=max_tokens,
                temperature=0.3,
            )
            if response.choices:
                msg = response.choices[0].message
                ans = getattr(msg, "content", None) or getattr(msg, "reasoning_content", None) or ""
                cleaned = clean_ai_response(ans)
                if cleaned:
                    return cleaned
        except Exception as e:
            logging.warning("Model %s failed: %s", model_name, e)
            last_err = e

    err_str = str(last_err)
    if "402" in err_str:
        return (
            "[AI Quota Exceeded] Error 402: You have no remaining credits with this provider.\n"
            "Please verify your API key account balance or switch to a free provider."
        )
    if "401" in err_str:
        return "[AI Authentication Error] Error 401: Invalid API key. Please verify the key in your .env file."

    return f"[AI Warning] Generation failed.\nError details: {last_err or 'No valid response'}"

def generate_resume_feedback(candidate_data: Dict[str, Any], jd_text: str) -> str:
    prompt = f"""
Conduct an in-depth professional resume review evaluating this candidate against the target Job Description.

CANDIDATE: {candidate_data.get('Candidate', '')}
EXPERIENCE: {candidate_data.get('Experience', 'Not explicitly mentioned')}
EDUCATION: {candidate_data.get('Education', 'Not explicitly mentioned')}
OVERALL SCORE: {candidate_data.get('Overall Score (%)', 0)}% (Semantic Similarity: {candidate_data.get('Similarity (%)', 0)}%)
MATCHED SKILLS: {', '.join(candidate_data.get('_matched_skills', [])) or 'None detected'}
MISSING JD SKILLS: {', '.join(candidate_data.get('_missing_skills', [])) or 'None detected'}
ADDITIONAL SKILLS: {', '.join(candidate_data.get('_extra_skills', [])) or 'None detected'}

RESUME TEXT:
{candidate_data.get('_raw_text', '')[:10000]}

TARGET JOB DESCRIPTION:
{jd_text[:10000]}

Format your feedback cleanly using these exact section headers:
## 🎯 Executive Match Summary
Provide a 2-3 paragraph objective assessment of how competitive this candidate is for this specific JD, their level alignment, and hiring manager perception.

## ⭐ Key Strengths & Demonstrated Achievements
Highlight 3-4 distinct strengths proven in the resume with references to actual projects, quantified metrics, and technical accomplishments.

## ⚠️ Critical Skill Gaps & JD Mismatches
Detail the most important requirements from the JD that are missing, underdeveloped, or poorly presented in the candidate's resume.

## ✍️ High-Impact Resume Bullet Revisions
Provide 4-5 concrete "Before vs. After" bullet point rewrites based on the candidate's existing experience, showing how to inject active leadership verbs, business context, and quantifiable metrics.

## 🔑 Missing Keywords for ATS Optimization
List 10-15 high-priority keywords, frameworks, and technical terms from the JD that should be naturally integrated into the resume to pass ATS filters.

## 🛠️ Project Enhancements & Recommendations
Provide 2-3 specific ways the candidate can enhance their existing projects or build a targeted feature to definitively prove the missing JD skills.
"""
    return generate_with_ai(prompt, max_tokens=3500)

def generate_professional_summary(candidate_data: Dict[str, Any], jd_text: str) -> str:
    prompt = f"""
Write 3 tailored, ATS-optimized professional summaries for this candidate targeted at the provided Job Description.

CANDIDATE: {candidate_data.get('Candidate', '')}
DETECTED EXPERIENCE: {candidate_data.get('Experience', '')}
MATCHED SKILLS: {', '.join(candidate_data.get('_matched_skills', []))}
RESUME HIGHLIGHTS:
{candidate_data.get('_raw_text', '')[:8000]}

TARGET JD:
{jd_text[:6000]}

Provide three distinct variations:
## Option 1: Results & Metrics-Driven (Ideal for technical hiring managers)
(3-4 sentences highlighting quantified impact and core engineering capabilities)

## Option 2: Technology & Stack-Focused (Ideal for senior IC & engineering roles)
(3-4 sentences emphasizing specialized tools, architecture, and framework expertise)

## Option 3: Balanced ATS Standard (Versatile across enterprise recruiters)
(3-4 sentences blending leadership, technical stack, and business impact)
"""
    return generate_with_ai(prompt, max_tokens=1200)

def generate_job_opportunities(candidate_data: Dict[str, Any], jd_text: str = "") -> str:
    prompt = f"""
Analyze this candidate's verified background and generate high-probability career directions and job search strategies.

CANDIDATE: {candidate_data.get('Candidate', '')}
EXPERIENCE LEVEL: {candidate_data.get('Experience', 'Junior / Mid')}
DEMONSTRATED SKILLS: {', '.join(candidate_data.get('_matched_skills', []) + candidate_data.get('_extra_skills', []))}
RESUME CONTEXT:
{candidate_data.get('_raw_text', '')[:8000]}
TARGET JD CONTEXT:
{jd_text[:4000]}

IMPORTANT INSTRUCTIONS:
- Calibrate job titles to the candidate's demonstrated skill depth and years of experience.
- Do NOT label everything as "Intern" unless the resume explicitly indicates an enrolled undergraduate student. Offer appropriate entry, associate, or mid-level titles.

Format with these headers:
## 🎯 Primary Target Job Titles
List 5 specific, high-demand job titles where this candidate is currently competitive. For each title, include:
- **Title**: (e.g., Python Backend Engineer, AI Application Developer)
- **Why It Fits**: (2 sentences explaining the stack alignment)
- **Target Experience Bracket**: (e.g., 0-2 yrs / 2-4 yrs)

## 🔄 High-Potential Adjacent & Emerging Roles
List 4 emerging or adjacent job titles (e.g., LLM Workflow Specialist, Data Platform Engineer) that leverage their skill overlaps.

## 🏢 Ideal Company Profiles & Team Types
Describe 3 types of organizations where this candidate's skill profile is in highest demand (e.g., Early-stage AI startups, Enterprise Cloud migration teams).

## 🔍 Targeted Boolean Search Queries
Provide 3 copy-paste Boolean search strings for LinkedIn, Indeed, and Google Jobs (e.g., `"Python" AND ("FastAPI" OR "Django") AND "Docker"`).

## 📈 Highest-ROI Skill Accelerators
Identify 2-3 specific skills that would immediately unlock a higher salary tier or title promotion.
"""
    return generate_with_ai(prompt, max_tokens=2500)

def generate_skill_development_plan(candidate_data: Dict[str, Any], jd_text: str) -> str:
    prompt = f"""
Create an intensive 30-Day Skill Development Roadmap to close the candidate's skill gaps for this Job Description.

CANDIDATE: {candidate_data.get('Candidate', '')}
CURRENT SKILLS: {', '.join(candidate_data.get('_matched_skills', [])) or 'None detected'}
MISSING TARGET SKILLS: {', '.join(candidate_data.get('_missing_skills', [])) or 'None detected'}

TARGET JD REQUIREMENTS:
{jd_text[:8000]}

Structure the roadmap with these exact headers:
## 🎯 Priority Skill Matrix
Rank the top 3-4 missing skills in order of hiring importance for this role, explaining why each is critical.

## 📅 Week 1: Core Fundamentals & Concept Mastery
- **Focus Areas**: Key concepts and syntax to master.
- **Curated Learning Resources**: Official documentation, key tutorials, or books.
- **Milestone Goal**: Concrete knowledge checkpoint at the end of Week 1.

## 📅 Week 2: Practical Exercises & Tooling
- **Focus Areas**: Setting up environments, CLI tools, libraries, and hands-on coding.
- **Hands-On Lab**: 2 practical mini-exercises to build.
- **Milestone Goal**: Verifiable script or mini-tool operational.

## 📅 Week 3: End-to-End Capstone Project
- **Project Name & Concept**: A realistic, resume-worthy project to build from scratch.
- **Tech Stack**: Integration of the newly learned skills with their existing stack.
- **Deliverables**: GitHub repo features, README documentation, and deployment steps.

## 📅 Week 4: Portfolio Integration & Interview Mastery
- **Resume Bullet Points**: 2 ready-to-use resume bullet points describing the completed capstone project.
- **Interview Prep**: 3 technical interview questions hiring managers ask about these skills, with concise model answers.
"""
    return generate_with_ai(prompt, max_tokens=3000)

def generate_job_profile(candidate_data: Dict[str, Any], jd_text: str) -> str:
    prompt = f"""
Create a concise executive career profile for this candidate based on their resume and target role.

RESUME:
{candidate_data.get('_raw_text', '')[:8000]}
TARGET JD:
{jd_text[:6000]}

Provide:
## Candidate Headline
## Core Technical Competencies
## Proven Project Achievements
## Target Role Alignment
"""
    return generate_with_ai(prompt, max_tokens=1200)

def get_system_status() -> Dict[str, Any]:
    return {
        "ai_base_url": AI_BASE_URL,
        "ai_model": AI_MODEL,
        "embedding_model": EMBEDDING_MODEL,
        "ai_server": test_ai_connection(),
    }

def initialize_ai() -> Dict[str, Any]:
    return test_ai_connection()
