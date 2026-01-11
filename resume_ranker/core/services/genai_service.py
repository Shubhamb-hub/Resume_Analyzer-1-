import re
import spacy
from datetime import datetime

# ==================================================
# Load spaCy model
# ==================================================
nlp = spacy.load("en_core_web_sm")
CURRENT_YEAR = datetime.now().year

# ==================================================
# SKILL TAXONOMY
# ==================================================
SKILL_KEYWORDS = {
    "python", "java", "c++", "c", "sql", "r", "javascript",
    "data science", "machine learning", "deep learning",
    "nlp", "computer vision", "statistics", "data analytics",
    "pandas", "numpy", "scikit-learn", "tensorflow",
    "pytorch", "keras", "opencv", "matplotlib", "seaborn",
    "excel", "power bi", "tableau",
    "aws", "azure", "gcp", "docker", "kubernetes", "git"
}

SKILL_ALIASES = {
    "ml": "machine learning",
    "dl": "deep learning",
    "natural language processing": "nlp",
    "cv": "computer vision",
    "sklearn": "scikit-learn"
}

# ==================================================
# EDUCATION HIERARCHY
# ==================================================
EDUCATION_LEVELS = [
    ("SECONDARY (10TH)", 1, [
        "10th", "ssc", "secondary school", "matriculation"
    ]),
    ("HIGHER SECONDARY (12TH)", 2, [
        "12th", "hsc", "higher secondary", "intermediate"
    ]),
    ("DIPLOMA", 3, ["diploma"]),
    ("BACHELOR", 4, [
        "b.tech", "b.e", "b.sc", "bca",
        "bachelor of technology", "bachelor of engineering",
        "bachelor degree", "undergraduate"
    ]),
    ("MASTER", 5, [
        "m.tech", "m.sc", "mba", "mca",
        "master of technology", "master degree", "postgraduate"
    ]),
    ("PHD", 6, [
        "phd", "doctor of philosophy", "doctoral"
    ])
]

# ==================================================
# EXPERIENCE PATTERNS
# ==================================================
YEAR_PATTERN = re.compile(r"(\d+(?:\.\d+)?)\s*(years|yrs)", re.I)
DATE_RANGE_PATTERN = re.compile(
    r"(19\d{2}|20\d{2})\s*(?:-|to|–)\s*(present|19\d{2}|20\d{2})",
    re.I
)

# ==================================================
# NAME EXTRACTION
# ==================================================
def extract_name(text):
    """
    Extract candidate name using NLP + heuristics.
    """
    lines = text.splitlines()[:5]  # top of resume
    for line in lines:
        doc = nlp(line)
        for ent in doc.ents:
            if ent.label_ == "PERSON" and len(ent.text.split()) <= 3:
                return ent.text.title()
    return "Unknown"

# ==================================================
# EXPERIENCE EXTRACTION
# ==================================================
def extract_experience_years(text):
    text = text.lower()

    matches = YEAR_PATTERN.findall(text)
    if matches:
        return max(float(m[0]) for m in matches)

    ranges = DATE_RANGE_PATTERN.findall(text)
    durations = []

    for start, end in ranges:
        try:
            start_year = int(start)
            end_year = CURRENT_YEAR if end == "present" else int(end)
            durations.append(end_year - start_year)
        except:
            continue

    return max(durations) if durations else 0.0

# ==================================================
# EXPERIENCE LEVEL
# ==================================================
def infer_experience_level(years):
    if years <= 1:
        return "Fresher"
    if years <= 3:
        return "Junior"
    if years <= 6:
        return "Mid-Level"
    return "Senior"

# ==================================================
# EDUCATION EXTRACTION
# ==================================================
def extract_education(text):
    text = text.lower()
    found = []

    for label, rank, patterns in EDUCATION_LEVELS:
        for p in patterns:
            if p in text:
                found.append((label, rank))
                break

    return max(found, key=lambda x: x[1])[0] if found else "Unknown"

# ==================================================
# SKILLS EXTRACTION
# ==================================================
def extract_skills(text):
    text = text.lower()
    found = set()

    for skill in SKILL_KEYWORDS:
        if skill in text:
            found.add(skill)

    for alias, canonical in SKILL_ALIASES.items():
        if alias in text:
            found.add(canonical)

    doc = nlp(text)
    for chunk in doc.noun_chunks:
        if chunk.text in SKILL_KEYWORDS:
            found.add(chunk.text)

    return sorted(s.title() for s in found)

# ==================================================
# CERTIFICATIONS EXTRACTION
# ==================================================
def extract_certifications(text):
    cert_keywords = [
        "certified", "certification", "coursera",
        "udemy", "aws certified", "google certified"
    ]
    return [
        line.strip()
        for line in text.splitlines()
        if any(k in line.lower() for k in cert_keywords)
    ]

# ==================================================
# PROJECT COUNT
# ==================================================
def extract_project_count(text):
    return len(re.findall(r"\bproject\b", text.lower()))

# ==================================================
# DOMAIN INFERENCE
# ==================================================
def infer_domain(skills):
    s = {x.lower() for x in skills}

    if {"machine learning", "deep learning", "nlp"} & s:
        return "Data Science / AI"
    if {"sql", "excel", "power bi"} & s:
        return "Data Analytics"
    if {"aws", "docker", "kubernetes"} & s:
        return "Cloud / DevOps"
    if {"java", "c++", "javascript"} & s:
        return "Software Development"

    return "General"

# ==================================================
# MAIN EXTRACTION FUNCTION
# ==================================================
def extract_info(resume_text):
    """
    Fully offline, high-accuracy ATS-grade extractor.
    """

    if not resume_text:
        return {}

    name = extract_name(resume_text)
    skills = extract_skills(resume_text)
    education = extract_education(resume_text)
    experience_years = extract_experience_years(resume_text)
    experience_level = infer_experience_level(experience_years)
    domain = infer_domain(skills)
    certifications = extract_certifications(resume_text)
    project_count = extract_project_count(resume_text)

    return {
        "name": name,
        "skills": skills,
        "education": education,
        "experience_years": round(experience_years, 2),
        "experience_level": experience_level,
        "domain": domain,
        "certifications": certifications,
        "project_count": project_count
    }
