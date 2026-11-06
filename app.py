import streamlit as st
from frontend.styles import apply_custom_css
from frontend.state import initialize_session_state
from frontend.views.home import render_home_page
from frontend.views.upload import render_upload_page
from frontend.views.ranking import render_ranking_page
from frontend.views.feedback import render_feedback_page
from frontend.views.job_opportunities import render_job_opportunities_page
from frontend.views.skill_plan import render_skill_plan_page
from frontend.views.analytics import render_analytics_page

st.set_page_config(
    page_title="AI Resume Screener",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

def main():
    apply_custom_css()
    initialize_session_state()

    st.markdown('<p class="main-header">🤖 AI Resume Screening & Career Assistant</p>', unsafe_allow_html=True)

    pages = {
        "🏠 Home": render_home_page,
        "📤 Upload Resumes & JD": render_upload_page,
        "🏆 Candidate Ranking": render_ranking_page,
        "🤖 AI Resume Feedback": render_feedback_page,
        "💼 Job Opportunities": render_job_opportunities_page,
        "📚 Skill Development": render_skill_plan_page,
        "📊 Analytics": render_analytics_page,
    }

    current_page = st.session_state.get("current_page", "🏠 Home")
    if current_page not in pages:
        current_page = "🏠 Home"

    selected_page = st.sidebar.radio("Navigation", list(pages.keys()), index=list(pages.keys()).index(current_page))
    st.session_state.current_page = selected_page

    # Render selected view
    pages[selected_page]()

if __name__ == "__main__":
    main()
