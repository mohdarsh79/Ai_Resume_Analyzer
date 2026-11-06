from typing import List, Dict, Any
import pandas as pd
from backend.text_processing import (
    extract_contact_info,
    extract_skills,
    extract_experience,
    extract_education,
)
from backend.similarity import calculate_similarity

def analyze_candidates(resumes: List[Dict[str, Any]], jd_text: str) -> pd.DataFrame:
    """Analyze a list of candidate resumes against a job description."""
    if not jd_text or not resumes:
        return pd.DataFrame()

    jd_skills = extract_skills(jd_text)
    jd_skill_set = set(jd_skills)
    results = []

    for resume in resumes:
        raw_text = resume.get("text", "")
        candidate_name = resume.get("name", "Unknown Candidate")
        if not raw_text:
            continue

        contact = extract_contact_info(raw_text)
        resume_skills = extract_skills(raw_text)
        similarity = calculate_similarity(raw_text, jd_text)
        resume_skill_set = set(resume_skills)

        matched_skills = sorted(list(resume_skill_set & jd_skill_set))
        missing_skills = sorted(list(jd_skill_set - resume_skill_set))
        extra_skills = sorted(list(resume_skill_set - jd_skill_set))
        skill_ratio = (len(matched_skills) / len(jd_skills)) if jd_skills else 0.0

        # Weighted score: 60% semantic similarity + 40% skill match ratio
        overall_score = (similarity * 0.60) + (skill_ratio * 0.40)

        results.append({
            "Candidate": candidate_name,
            "Overall Score (%)": round(overall_score * 100, 2),
            "Similarity (%)": round(similarity * 100, 2),
            "Matched Skills": ", ".join(matched_skills) if matched_skills else "None",
            "Missing Skills": ", ".join(missing_skills) if missing_skills else "None",
            "Extra Skills": ", ".join(extra_skills) if extra_skills else "None",
            "Experience": extract_experience(raw_text),
            "Education": extract_education(raw_text),
            "Email": contact["Email"],
            "Phone": contact["Phone"],
            "LinkedIn": contact["LinkedIn"],
            "_raw_text": raw_text,
            "_matched_skills": matched_skills,
            "_missing_skills": missing_skills,
            "_extra_skills": extra_skills,
            "_jd_skills": jd_skills,
        })

    df = pd.DataFrame(results)
    if not df.empty:
        df = df.sort_values(by="Overall Score (%)", ascending=False).reset_index(drop=True)
        df.index = df.index + 1
        df.index.name = "Rank"

    return df
