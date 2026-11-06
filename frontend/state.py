import streamlit as st
import pandas as pd
from backend.ai_client import (
    generate_resume_feedback,
    generate_professional_summary,
    generate_job_opportunities,
    generate_skill_development_plan,
)

def initialize_session_state():
    """Initialize default session state keys."""
    defaults = {
        "current_page": "🏠 Home",
        "ranking_df": pd.DataFrame(),
        "jd_text": "",
        "ai_feedback": {},
        "ai_summary": {},
        "job_opportunities": {},
        "skill_plan": {},
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

def get_selected_candidate_data(candidate_name: str):
    """Retrieve row data dictionary for chosen candidate."""
    df = st.session_state.get("ranking_df", pd.DataFrame())
    if df.empty or candidate_name not in df["Candidate"].values:
        return None
    return df[df["Candidate"] == candidate_name].iloc[0]

def generate_ai_content(candidate_name: str, content_type: str):
    """Generic AI generator helper for feedback, jobs, summary, and skill plan."""
    cand_data = get_selected_candidate_data(candidate_name)
    if cand_data is None:
        return

    cand_dict = cand_data.to_dict()
    jd_text = st.session_state.get("jd_text", "")

    generators = {
        "feedback": ("🤖 Generating personalized AI feedback...", generate_resume_feedback, "ai_feedback"),
        "summary": ("✍️ Creating professional summary...", generate_professional_summary, "ai_summary"),
        "jobs": ("💼 Finding suitable career directions...", generate_job_opportunities, "job_opportunities"),
        "plan": ("📚 Creating skill development plan...", generate_skill_development_plan, "skill_plan"),
    }

    if content_type not in generators:
        return

    spinner_msg, func, state_key = generators[content_type]
    with st.spinner(spinner_msg):
        res = func(cand_dict, jd_text)

    st.session_state[state_key][candidate_name] = res
