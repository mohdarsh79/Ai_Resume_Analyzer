import streamlit as st
from frontend.state import get_selected_candidate_data, generate_ai_content

def render_feedback_page():
    st.header("🤖 Personalized AI Resume Feedback")
    df = st.session_state.get("ranking_df")

    if df is None or df.empty:
        st.warning("⚠️ No processed resume data found. Please upload resumes and a job description first.")
        if st.button("📤 Go to Upload Page"):
            st.session_state.current_page = "📤 Upload Resumes & JD"
            st.rerun()
        return

    selected_candidate = st.selectbox("Select Candidate", df["Candidate"].tolist(), key="feedback_candidate")
    cand_data = get_selected_candidate_data(selected_candidate)

    if cand_data is not None:
        c1, c2, c3 = st.columns(3)
        c1.metric("Overall Match", f"{cand_data['Overall Score (%)']}%")
        c2.metric("Matched Skills", len(cand_data["_matched_skills"]))
        c3.metric("Missing Skills", len(cand_data["_missing_skills"]))

        st.divider()
        if st.button("🤖 Generate Personalized Resume Feedback", key="btn_feedback"):
            generate_ai_content(selected_candidate, "feedback")

        feedback = st.session_state.ai_feedback.get(selected_candidate)
        if feedback:
            st.subheader("📋 AI Analysis & Recommendations")
            with st.container(border=True):
                st.markdown(feedback)

            st.divider()
            st.download_button(
                "📥 Download AI Feedback Report",
                data=feedback,
                file_name=f"{selected_candidate}_resume_feedback.txt",
                mime="text/plain",
            )
