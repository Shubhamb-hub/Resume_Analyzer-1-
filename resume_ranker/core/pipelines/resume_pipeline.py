from core.services.ocr_service import extract_text_from_file
from core.services.cleaning_service import clean_text
from core.services.regex_service import (
    extract_primary_email,
    extract_phone_numbers,
)
from core.services.genai_service import extract_info
from core.services.embedding_service import embed
from core.services.similarity_service import cosine_similarity
from core.services.scoring_service import calculate_final_score
from core.services.explanation_service import generate_explanation


def analyze_and_rank_resumes(file_paths, job_description):
    """
    Analyze multiple resumes and rank them based on suitability
    for the given job description.

    Fully offline, ATS-style NLP pipeline.
    """

    results = []

    # --------------------------------------------------
    # 1. Prepare job description
    # --------------------------------------------------
    job_description_cleaned = clean_text(job_description)

    if not job_description_cleaned:
        return results

    job_vector = embed(job_description_cleaned)

    # Extract job-side skills
    job_info = extract_info(job_description_cleaned)
    job_skills = {
        skill.lower()
        for skill in job_info.get("skills", [])
    }

    # --------------------------------------------------
    # 2. Process each resume
    # --------------------------------------------------
    for file_path in file_paths:
        try:
            # ---------------- OCR ----------------
            raw_text = extract_text_from_file(file_path)
            if not raw_text:
                continue

            # ---------------- Cleaning ----------------
            cleaned_text = clean_text(raw_text)
            if not cleaned_text:
                continue

            # ---------------- Contact Info ----------------
            email = extract_primary_email(cleaned_text)
            phones = extract_phone_numbers(cleaned_text)

            # ---------------- Resume NLP Extraction ----------------
            resume_info = extract_info(cleaned_text)

            skills = resume_info.get("skills", [])
            education = resume_info.get("education", "Unknown")
            experience_years = resume_info.get("experience_years", 0.0)
            domain = resume_info.get("domain", "Unknown")

            resume_skills = {
                skill.lower()
                for skill in skills
            }

            # ---------------- Semantic Similarity (0–10 or None) ----------------
            resume_vector = embed(cleaned_text)

            semantic_score = cosine_similarity(
                resume_vector,
                job_vector
            )

            # ❌ Skip resumes with no meaningful semantic match
            if semantic_score is None:
                continue

            # ---------------- Skill Overlap ----------------
            if job_skills:
                skill_overlap_ratio = (
                    len(job_skills & resume_skills)
                    / len(job_skills)
                )
            else:
                skill_overlap_ratio = 0.0

            # ---------------- Final ATS Score (0–10) ----------------
            match_score = calculate_final_score(
                semantic_similarity=semantic_score / 10,  # normalize back to 0–1
                experience_years=experience_years,
                skill_overlap=skill_overlap_ratio
            )

            # ---------------- Explanation ----------------
            explanation = generate_explanation(
                job_description=job_description_cleaned,
                skills=skills,
                experience_years=experience_years,
                match_score=match_score,
                semantic_similarity=semantic_score,
                skill_overlap=skill_overlap_ratio
            )

            # ---------------- Collect Result ----------------
            results.append({
                "email": email,
                "phone_numbers": phones,
                "skills": skills,
                "education": education,
                "experience_years": round(experience_years, 2),
                "domain": domain,
                "semantic_similarity": round(semantic_score, 2),
                "skill_overlap": round(skill_overlap_ratio, 2),
                "match_score": match_score,
                "explanation": explanation
            })

        except Exception as e:
            # One resume failure should NOT stop the pipeline
            print(f"[Resume skipped] {file_path} → {e}")
            continue

    # --------------------------------------------------
    # 3. Sort by match score (descending)
    # --------------------------------------------------
    results.sort(
        key=lambda x: x["match_score"],
        reverse=True
    )

    return results
