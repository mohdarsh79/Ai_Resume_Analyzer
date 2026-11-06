import streamlit as st

def apply_custom_css():
    """Apply custom UI styling to Streamlit app."""
    st.markdown(
        """
        <style>
        .main-header {
            font-size: 2.3rem;
            color: #1E3A8A;
            font-weight: 800;
            text-align: center;
            margin-bottom: 1.5rem;
        }
        .stButton > button {
            width: 100%;
            border-radius: 8px;
            min-height: 2.8em;
            background-color: #2563EB;
            color: white;
            font-weight: 700;
            border: none;
            transition: all 0.2s ease-in-out;
        }
        .stButton > button:hover {
            background-color: #1D4ED8;
            color: white;
            transform: translateY(-1px);
        }
        .ai-card {
            padding: 24px;
            border-radius: 12px;
            background-color: #F8FAFC;
            color: #0F172A !important;
            border: 1px solid #CBD5E1;
            margin-bottom: 20px;
            font-size: 0.95rem;
            line-height: 1.6;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        }
        .ai-card * {
            color: #0F172A !important;
        }
        .stDataFrame {
            font-size: 0.9rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
