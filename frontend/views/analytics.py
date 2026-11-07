import streamlit as st
import pandas as pd
import plotly.express as px

def render_analytics_page():
    st.header("📊 Analytics Dashboard")
    df = st.session_state.get("ranking_df")

    if df is None or df.empty:
        st.warning("⚠️ No analytics data available. Please upload resumes and a job description first.")
        if st.button("📤 Go to Upload Page"):
            st.session_state.current_page = "📤 Upload Resumes & JD"
            st.rerun()
        return

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Candidates", len(df))
    c2.metric("Average Score", f"{df['Overall Score (%)'].mean():.2f}%")
    c3.metric("Highest Score", f"{df['Overall Score (%)'].max():.2f}%")
    c4.metric("Average Similarity", f"{df['Similarity (%)'].mean():.2f}%")

    st.divider()
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Candidate Score Distribution")
        fig_bar = px.bar(
            df, x="Candidate", y="Overall Score (%)", color="Overall Score (%)",
            color_continuous_scale="Blues", title="Overall Match Scores"
        )
        st.plotly_chart(fig_bar, width="stretch")

    with col2:
        st.subheader("Skill Frequency")
        all_matched = []
        for s_list in df["_matched_skills"]:
            if isinstance(s_list, list):
                all_matched.extend(s_list)

        if all_matched:
            counts = pd.Series(all_matched).value_counts().head(10)
            fig_pie = px.pie(values=counts.values, names=counts.index, title="Top 10 Matched Skills")
            st.plotly_chart(fig_pie, width="stretch")
        else:
            st.info("No matched skills found.")

    st.subheader("🔴 Most Common Missing Skills")
    all_missing = []
    for s_list in df["_missing_skills"]:
        if isinstance(s_list, list):
            all_missing.extend(s_list)

    if all_missing:
        m_counts = pd.Series(all_missing).value_counts().head(10)
        fig_missing = px.bar(
            x=m_counts.values, y=m_counts.index, orientation="h",
            title="Top 10 Frequently Missing Skills", labels={"x": "Candidate Count", "y": "Skill"}
        )
        st.plotly_chart(fig_missing, width="stretch")
    else:
        st.info("No missing skills found.")
