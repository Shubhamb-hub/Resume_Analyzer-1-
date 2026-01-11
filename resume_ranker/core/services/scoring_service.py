"""
scoring_service.py

Responsible for computing final resume match score
using multiple relevance signals in an ATS-style manner.
Final score is returned on a 0–10 scale.
"""


def normalize_experience(experience_years, max_years=10):
    """
    Normalize experience into 0–1 range.

    Args:
        experience_years (float): extracted experience
        max_years (int): experience cap

    Returns:
        float: normalized experience score
    """
    try:
        experience_years = float(experience_years)
    except (TypeError, ValueError):
        return 0.0

    if experience_years <= 0:
        return 0.0

    return min(experience_years / max_years, 1.0)


def normalize_score(value):
    """
    Clamp any score safely into 0–1 range.
    """
    try:
        value = float(value)
    except (TypeError, ValueError):
        return 0.0

    return max(0.0, min(value, 1.0))


def calculate_final_score(
    semantic_similarity,
    experience_years,
    skill_overlap=0.0,
    weights=None,
    scale=10
):
    """
    Calculate final resume match score using:
    - semantic similarity (embeddings)
    - skill overlap ratio
    - experience relevance

    Final score is returned on a 0–10 scale.

    Args:
        semantic_similarity (float): cosine similarity (0–1)
        experience_years (float): total experience
        skill_overlap (float): ratio of matched skills (0–1)
        weights (dict): optional ATS weight configuration
        scale (int): output score scale (default 10)

    Returns:
        float: final match score (0–10)
    """

    # ----------------------------
    # Default ATS-style weights
    # ----------------------------
    if weights is None:
        weights = {
            "semantic": 0.55,     # Role relevance (embeddings)
            "skills": 0.30,       # Explicit skill match
            "experience": 0.15    # Experience relevance
        }

    # ----------------------------
    # Normalize inputs
    # ----------------------------
    semantic_score = normalize_score(semantic_similarity)
    skill_score = normalize_score(skill_overlap)
    experience_score = normalize_experience(experience_years)

    # ----------------------------
    # Weighted score (0–1)
    # ----------------------------
    normalized_final = (
        weights["semantic"] * semantic_score +
        weights["skills"] * skill_score +
        weights["experience"] * experience_score
    )

    # ----------------------------
    # Scale to 0–10
    # ----------------------------
    final_score = round(normalized_final * scale, 2)

    return final_score
