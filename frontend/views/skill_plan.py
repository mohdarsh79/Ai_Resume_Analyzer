import streamlit as st
from frontend.state import get_selected_candidate_data, generate_ai_content

def render_skill_plan_page():
    st.header("📚 Personalized Skill Development Plan")
    df = st.session_state.get("ranking_df")

    if df is None or df.empty:
        st.warning("⚠️ No processed resume data found. Please upload resumes and a job description first.")
        if st.button("📤 Go to Upload Page"):
            st.session_state.current_page = "📤 Upload Resumes & JD"
            st.rerun()
        return

    selected_candidate = st.selectbox("Select Candidate", df["Candidate"].tolist(), key="plan_candidate")
    cand_data = get_selected_candidate_data(selected_candidate)

    if cand_data is not None:
        missing = cand_data["_missing_skills"]
        if missing:
            st.warning("Skills detected as missing from target JD: " + ", ".join(missing))
        else:
            st.success("No missing skills detected.")

        if st.button("📚 Generate 30-Day Skill Plan", key="btn_plan"):
            generate_ai_content(selected_candidate, "plan")

        plan = st.session_state.skill_plan.get(selected_candidate)
        if plan:
            st.subheader("📅 30-Day Skill Roadmap")
            with st.container(border=True):
                st.markdown(plan)

            st.divider()
            st.download_button(
                "📥 Download Skill Plan",
                data=plan,
                file_name=f"{selected_candidate}_skill_plan.txt",
                mime="text/plain",
            )
