import streamlit as st
from frontend.state import get_selected_candidate_data, generate_ai_content

def render_job_opportunities_page():
    st.header("💼 AI Job Opportunity Suggestions")
    df = st.session_state.get("ranking_df")

    if df is None or df.empty:
        st.warning("⚠️ No processed resume data found. Please upload resumes and a job description first.")
        if st.button("📤 Go to Upload Page"):
            st.session_state.current_page = "📤 Upload Resumes & JD"
            st.rerun()
        return

    st.info("Career directions and job-title suggestions based on demonstrated skills.")
    selected_candidate = st.selectbox("Select Candidate", df["Candidate"].tolist(), key="jobs_candidate")
    cand_data = get_selected_candidate_data(selected_candidate)

    if cand_data is not None:
        c1, c2, c3 = st.columns(3)
        c1.metric("Match Score", f"{cand_data['Overall Score (%)']}%")
        c2.metric("Experience", cand_data["Experience"])
        c3.metric("Education", cand_data["Education"])

        st.divider()
        if st.button("💼 Generate Job Opportunities", key="btn_jobs"):
            generate_ai_content(selected_candidate, "jobs")

        jobs = st.session_state.job_opportunities.get(selected_candidate)
        if jobs:
            st.subheader("💡 Suggested Opportunities")
            with st.container(border=True):
                st.markdown(jobs)

            st.divider()
            st.download_button(
                "📥 Download Job Suggestions",
                data=jobs,
                file_name=f"{selected_candidate}_job_opportunities.txt",
                mime="text/plain",
            )
