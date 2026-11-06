import re
from typing import List, Dict
from nltk.tokenize import word_tokenize
from backend.config import STOPWORDS, LEMMATIZER

SKILL_DB = [
    # Programming
    "Python", "Java", "C++", "C", "C#", "JavaScript", "TypeScript", "Go", "Rust", "Ruby", "PHP", "Swift", "Kotlin",
    # Web
    "HTML", "CSS", "React", "Angular", "Vue", "Node.js", "Express", "Django", "Flask", "FastAPI", "Spring Boot",
    # AI / ML
    "Machine Learning", "Deep Learning", "NLP", "Natural Language Processing", "Computer Vision",
    "TensorFlow", "PyTorch", "Keras", "Scikit-learn", "Hugging Face", "Transformers", "LLM",
    "Generative AI", "Artificial Intelligence",
    # Data
    "Pandas", "NumPy", "Matplotlib", "Seaborn", "Data Analysis", "Data Science", "SQL", "NoSQL",
    "MongoDB", "PostgreSQL", "MySQL", "Oracle",
    # Cloud & DevOps
    "AWS", "Azure", "GCP", "Google Cloud", "Docker", "Kubernetes", "Jenkins", "CI/CD", "Terraform", "Ansible", "Linux",
    # Version Control & Tools
    "Git", "GitHub", "GitLab", "Bitbucket", "Spark", "Hadoop", "Kafka", "Hive", "HBase",
    # BI / Management / Soft Skills
    "Power BI", "Tableau", "Excel", "Jira", "Confluence", "Figma", "Postman",
    "Leadership", "Communication", "Problem Solving", "Critical Thinking", "Teamwork", "Time Management", "Agile", "Scrum"
]

def clean_text(text: str) -> str:
    """Clean text for TF-IDF processing."""
    if not text:
        return ""

    text = text.lower()
    text = re.sub(r"https?://\S+|www\.\S+|\S+@\S+\.\S+|\b\d{10}\b|\b\d{3}[-.]?\d{3}[-.]?\d{4}\b", " ", text)
    text = re.sub(r"[^\w\s]|\d+", " ", text)
    text = re.sub(r"\s+", " ", text).strip()

    try:
        tokens = word_tokenize(text)
    except Exception:
        tokens = text.split()

    cleaned = []
    for word in tokens:
        if word in STOPWORDS or len(word) <= 1:
            continue
        if LEMMATIZER:
            try:
                word = LEMMATIZER.lemmatize(word)
            except Exception:
                pass
        cleaned.append(word)

    return " ".join(cleaned)

def extract_contact_info(text: str) -> Dict[str, str]:
    """Extract email, phone, and LinkedIn from raw text."""
    if not text:
        return {"Email": "Not Found", "Phone": "Not Found", "LinkedIn": "Not Found"}

    emails = re.findall(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b", text)
    phones = re.findall(r"(?:\+?\d{1,3}[-.\s]?)?(?:\d{10}|\d{3}[-.\s]?\d{3}[-.\s]?\d{4})", text)
    linkedin = re.findall(r"(?:https?://)?(?:www\.)?linkedin\.com/in/[A-Za-z0-9_\-]+", text, re.IGNORECASE)

    linkedin_val = f"https://{linkedin[0].replace('https://', '')}" if linkedin else "Not Found"

    return {
        "Email": emails[0] if emails else "Not Found",
        "Phone": phones[0] if phones else "Not Found",
        "LinkedIn": linkedin_val,
    }

def extract_skills(text: str) -> List[str]:
    """Extract known skills from text."""
    if not text:
        return []
    found = [skill for skill in SKILL_DB if re.search(r"(?<!\w)" + re.escape(skill) + r"(?!\w)", text, re.IGNORECASE)]
    return sorted(list(set(found)))

def extract_experience(text: str) -> str:
    """Detect explicitly mentioned years of experience."""
    if not text:
        return "Not explicitly mentioned"

    patterns = [
        r"(\d+\+?\s*(?:years?|yrs?))\s*(?:of)?\s*(?:professional\s+)?(?:experience|exp)",
        r"(\d+\+?\s*(?:years?|yrs?))\s+experience",
    ]
    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            return matches[0].strip()
    return "Not explicitly mentioned"

def extract_education(text: str) -> str:
    """Detect degree qualifications in text."""
    if not text:
        return "Not explicitly mentioned"

    degrees = [
        "Bachelor", "Bachelor's", "Master", "Master's", "Ph.D", "PhD",
        "B.S", "B.S.", "M.S", "M.S.", "B.Tech", "B.E", "B.E.",
        "M.Tech", "M.E", "M.E.", "MBA", "BBA", "MCA", "BCA"
    ]
    text_lower = text.lower()
    found = [d for d in degrees if d.lower() in text_lower]
    return ", ".join(sorted(set(found))) if found else "Not explicitly mentioned"
