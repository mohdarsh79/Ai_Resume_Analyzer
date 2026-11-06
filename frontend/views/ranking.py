import streamlit as st
from frontend.state import get_selected_candidate_data

def render_ranking_page():
    st.header("🏆 Candidate Ranking & Skill Gap Analysis")
    df = st.session_state.get("ranking_df")

    if df is None or df.empty:
        st.warning("⚠️ No candidate ranking data available. Please upload resumes and a job description first.")
        if st.button("📤 Go to Upload Page"):
            st.session_state.current_page = "📤 Upload Resumes & JD"
            st.rerun()
        return

    st.subheader("Overall Candidate Scores")
    display_cols = [
        "Candidate", "Overall Score (%)", "Similarity (%)", "Matched Skills",
        "Missing Skills", "Experience", "Education", "Email", "Phone"
    ]
    avail_cols = [c for c in display_cols if c in df.columns]
    st.dataframe(df[avail_cols], use_container_width=True)

    csv = df[avail_cols].to_csv(index=True).encode("utf-8")
    st.download_button("📥 Download Ranking as CSV", data=csv, file_name="candidate_ranking.csv", mime="text/csv")

    st.divider()
    st.subheader("🔍 Detailed Candidate Analysis")
    selected_candidate = st.selectbox("Select Candidate", df["Candidate"].tolist())
    cand_data = get_selected_candidate_data(selected_candidate)

    if cand_data is not None:
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Overall Score", f"{cand_data['Overall Score (%)']}%")
        c2.metric("Text Similarity", f"{cand_data['Similarity (%)']}%")
        c3.metric("Matched Skills", len(cand_data["_matched_skills"]))
        c4.metric("Missing Skills", len(cand_data["_missing_skills"]))

        st.markdown("### 🟢 Matched Skills")
        matched = cand_data["_matched_skills"]
        if matched:
            st.success(", ".join(matched))
        else:
            st.info("No matched skills detected.")

        st.markdown("### 🔴 Missing Skills")
        missing = cand_data["_missing_skills"]
        if missing:
            st.warning(", ".join(missing))
        else:
            st.success("No missing JD skills detected.")

        st.markdown("### 🔵 Additional Skills")
        extra = cand_data["_extra_skills"]
        if extra:
            st.info(", ".join(extra))
        else:
            st.write("No additional skills detected.")

        st.markdown("### 💡 Score Explanation")
        st.info(
            f"**{selected_candidate}**\n\n"
            f"Semantic similarity: **{cand_data['Similarity (%)']}%**\n"
            f"Matched skills: **{len(matched)}** / Required JD skills: **{len(cand_data['_jd_skills'])}**\n\n"
            "Overall score combines 60% semantic similarity and 40% detected skill match ratio."
        )
