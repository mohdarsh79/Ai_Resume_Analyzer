import streamlit as st

def render_home_page():
    st.header("Welcome to the AI Resume Screener")
    st.write(
        "This application uses NLP, semantic similarity, skill extraction, "
        "and Hugging Face AI models to analyze candidate resumes against job descriptions."
    )
    st.markdown(
        """
        ### 🚀 Key Features
        - 📄 **PDF & TXT Parsing**: Fast document text extraction with fallback parsers.
        - 🧠 **Semantic Matching**: Sentence-Transformers cosine similarity.
        - 🎯 **Skill Gap Analysis**: Extracts technical skills, detects missing & extra skills.
        - 🏆 **Automated Ranking**: Weighted scoring combining text match and skill ratio.
        - 🤖 **AI Feedback & Summary**: Practical, non-hallucinated feedback & ATS summary.
        - 💼 **Career Directions**: Suggested job roles & 30-day skill development plans.
        - 📊 **Analytics Dashboard**: Visual charts for candidate scores & skill frequency.
        """
    )
    st.info("💡 **Tip**: Navigate to 'Upload Resumes & JD' in the sidebar to get started.")
