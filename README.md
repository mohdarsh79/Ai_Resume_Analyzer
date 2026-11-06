# 🤖 AI Resume Screening & Career Assistant

An intelligent, full-featured AI resume screening and career development platform built with **Python**, **Streamlit**, and **Google Gemini**.

---

## ✨ Features

- **Automated Resume Parsing**: Fast text extraction from PDF (using `pdfplumber` and `PyPDF2`) and TXT files.
- **NLP Information Extraction**: Automatically extracts contact info (Email, Phone, LinkedIn), education, experience level, and verified skill sets.
- **Hybrid Matching Engine**:
  - **60% Semantic Cosine Similarity**: Evaluates conceptual fit using `SentenceTransformers` (`all-MiniLM-L6-v2`) with a Scikit-Learn TF-IDF fallback.
  - **40% Skill Match Ratio**: Strict intersection of job requirements against candidate capabilities.
  - **Overall Candidate Ranking**: Sorts candidates by weighted suitability score.
- **Gemini-Powered Career Advisory**:
  - **ATS Feedback & Scoring**: Detailed breakdown of strengths, weaknesses, and missing keywords.
  - **Resume Bullet Rewrites**: Concrete before/after metric-driven rewrites.
  - **Job Role Recommendations**: Target job titles, adjacent roles, and tailored boolean search queries.
  - **30-Day Skill Roadmap**: Week-by-week curriculum with hands-on projects to close skill gaps.
- **Analytics Dashboard**: Interactive Plotly visualizations for candidate score distributions, top matched skills, and common skill deficiencies.

---

## 🛠️ Tech Stack

- **Frontend**: Streamlit, Plotly
- **NLP & Parsing**: PyPDF2, pdfplumber, NLTK, Scikit-Learn, Sentence-Transformers
- **LLM / AI**: Google Gemini via OpenAI-compatible endpoints (`gemini-3.8-flash` / `gemini-3.7-flash`)

---

## 🚀 Quickstart

### 1. Clone the repository
```bash
git clone https://github.com/mohdarsh79/Ai_Resume_Analyzer.git
cd Ai_Resume_Analyzer
```

### 2. Set up virtual environment & dependencies
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Configure environment variables
Copy `.env.example` to `.env` and fill in your Gemini API key:
```bash
cp .env.example .env
```
In `.env`:
```env
AI_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai/
AI_API_KEY=your_gemini_api_key_here
AI_MODEL=gemini-3.8-flash
EMBEDDING_MODEL=all-MiniLM-L6-v2
```

### 4. Launch the application
```bash
streamlit run app.py
```

---

## 📁 Project Structure

```
├── app.py                      # Main entry point & Streamlit page routing
├── requirements.txt            # Python dependencies
├── .env.example                # Example environment variable template
├── backend/
│   ├── ai_client.py            # Gemini integration and prompt pipelines
│   ├── analyzer.py             # Candidate ranking & scoring logic
│   ├── config.py               # Settings & NLTK initialization
│   ├── parsers.py              # PDF and TXT document parsing
│   ├── similarity.py           # Semantic vector similarity calculations
│   └── text_processing.py      # Regex & NLP entity extraction
└── frontend/
    ├── state.py                # Streamlit session state management
    ├── styles.py               # Custom UI styles and themes
    └── views/                  # UI view modules (Home, Upload, Ranking, etc.)
```

---

## 📄 License
MIT License.
