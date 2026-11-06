import streamlit as st
from backend.parsers import parse_resume
from backend.analyzer import analyze_candidates

def render_upload_page():
    st.header("📤 Upload Job Description & Resumes")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📋 Job Description")
        jd_option = st.radio("Input Method", ["Paste Text", "Upload File"], horizontal=True)
        jd_text = ""
        if jd_option == "Paste Text":
            jd_text = st.text_area("Paste Job Description Here", height=280, placeholder="Paste job description...")
        else:
            jd_file = st.file_uploader("Upload JD (PDF/TXT)", type=["pdf", "txt"], key="jd_uploader")
            if jd_file:
                jd_text = parse_resume(jd_file)
                st.text_area("Extracted JD Text", jd_text, height=200)

    with col2:
        st.subheader("📄 Candidate Resumes")
        resume_files = st.file_uploader(
            "Upload Resumes (PDF/TXT)", type=["pdf", "txt"], accept_multiple_files=True, key="resume_uploader"
        )
        if resume_files:
            st.success(f"{len(resume_files)} resume(s) selected.")
            for file in resume_files:
                st.write(f"📄 {file.name}")

    st.divider()

    if st.button("🚀 Process & Analyze Candidates"):
        if not jd_text.strip():
            st.error("Please provide a Job Description.")
            return
        if not resume_files:
            st.error("Please upload at least one resume.")
            return

        with st.spinner("🧠 Processing resumes and analyzing candidates..."):
            resumes_data = []
            for file in resume_files:
                text = parse_resume(file)
                if not text.strip():
                    st.warning(f"Could not extract text from {file.name}.")
                    continue
                resumes_data.append({
                    "name": file.name.rsplit(".", 1)[0],
                    "text": text
                })

            if not resumes_data:
                st.error("No readable resumes found.")
                return

            df = analyze_candidates(resumes_data, jd_text)
            if df.empty:
                st.error("Unable to analyze resumes.")
                return

            st.session_state.ranking_df = df
            st.session_state.jd_text = jd_text
            st.session_state.ai_feedback = {}
            st.session_state.ai_summary = {}
            st.session_state.job_opportunities = {}
            st.session_state.skill_plan = {}

        st.success(f"Successfully analyzed {len(df)} candidate(s).")
        st.session_state.current_page = "🏆 Candidate Ranking"
        st.rerun()
