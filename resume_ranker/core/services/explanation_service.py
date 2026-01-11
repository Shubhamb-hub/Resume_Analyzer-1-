"""
explanation_service.py

Offline, deterministic explanation generator
for resume ranking decisions.
No external APIs used.
Enhanced with more humanistic and understandable explanations.
"""


def generate_explanation(
    job_description,
    skills,
    experience_years,
    match_score,
    semantic_similarity=None,
    skill_overlap=None
):
    """
    Generate a human-readable explanation for why the resume received this score.
    Enhanced with more natural, conversational language.
    """

    explanation_parts = []
    
    # Score interpretation helper
    def interpret_score(score):
        if score >= 0.85:
            return "excellent", "highly suitable", "a strong match"
        elif score >= 0.70:
            return "good", "well-suited", "a good fit"
        elif score >= 0.50:
            return "moderate", "somewhat suitable", "a reasonable match"
        elif score >= 0.30:
            return "limited", "partially suitable", "a partial match"
        else:
            return "low", "not well-suited", "a poor match"
    
    score_quality, suitability_level, match_phrase = interpret_score(match_score)
    
    # Opening statement
    opening_phrases = [
        f"This candidate shows {suitability_level} for the role based on our analysis.",
        f"Based on our evaluation, this candidate appears to be {suitability_level} for the position.",
        f"Our assessment indicates {suitability_level} between this candidate and the role requirements."
    ]
    
    import random
    explanation_parts.append(random.choice(opening_phrases))
    
    # ----------------------------
    # Skills explanation (more natural)
    # ----------------------------
    if skills:
        if len(skills) >= 8:
            skill_text = "The candidate demonstrates a diverse set of relevant skills including "
        elif len(skills) >= 4:
            skill_text = "The candidate has several key skills such as "
        else:
            skill_text = "The candidate has skills in "
        
        # Select top skills smartly
        top_skills = skills[:5]
        if len(top_skills) > 2:
            skill_list = ', '.join(top_skills[:-1]) + ', and ' + top_skills[-1]
        else:
            skill_list = ' and '.join(top_skills)
        
        skill_text += f"{skill_list}, which align well with typical requirements for this type of role."
        
        # Add depth comment
        if len(skills) > 10:
            skill_text += " This broad skill set suggests versatility and the ability to handle diverse responsibilities."
        elif len(skills) < 3:
            skill_text += " While these skills are relevant, the candidate may benefit from demonstrating additional competencies."
        
        explanation_parts.append(skill_text)
    else:
        explanation_parts.append("The resume doesn't clearly highlight specific technical skills, which makes it challenging to assess technical proficiency against the role requirements.")

    # ----------------------------
    # Experience explanation (more human)
    # ----------------------------
    experience_phrases = []
    
    if experience_years >= 10:
        experience_phrases = [
            f"With approximately {experience_years} years of experience, the candidate brings substantial professional depth.",
            f"The candidate offers extensive experience ({experience_years} years), indicating significant industry knowledge.",
            f"Having {experience_years} years in the field suggests strong domain expertise and seasoned judgment."
        ]
    elif experience_years >= 5:
        experience_phrases = [
            f"The candidate has solid professional experience with around {experience_years} years in relevant roles.",
            f"With {experience_years} years of experience, the candidate demonstrates meaningful professional growth.",
            f"This level of experience ({experience_years} years) typically indicates good competency development."
        ]
    elif experience_years >= 2:
        experience_phrases = [
            f"The candidate has gained practical experience over {experience_years} years, showing career progression.",
            f"With {experience_years} years of experience, the candidate has established foundational professional skills.",
            f"This amount of experience suggests the candidate has moved beyond entry-level roles."
        ]
    elif experience_years > 0:
        experience_phrases = [
            f"The candidate has limited but relevant experience of about {experience_years} year(s), indicating early career stage.",
            f"With {experience_years} year(s) of experience, the candidate is building foundational professional capabilities.",
            f"This experience level suggests the candidate is in the early stages of professional development."
        ]
    else:
        experience_phrases = [
            "The candidate appears to have limited professional experience, which may be a consideration for roles requiring prior experience.",
            "With minimal years of experience indicated, the candidate would likely require more training and supervision.",
            "The resume shows little professional experience, suggesting this might be an entry-level candidate."
        ]
    
    explanation_parts.append(random.choice(experience_phrases))
    
    # ----------------------------
    # Semantic similarity explanation (contextual)
    # ----------------------------
    if semantic_similarity is not None:
        if semantic_similarity > 0.8:
            semantic_phrases = [
                "The language and content of the resume strongly resonate with the job description, suggesting excellent contextual fit.",
                "There's remarkable alignment between how the candidate presents themselves and what the role requires.",
                "The resume demonstrates clear relevance to the position based on how experiences and qualifications are articulated."
            ]
        elif semantic_similarity > 0.6:
            semantic_phrases = [
                "The resume shows good alignment with the job requirements in terms of overall content and focus areas.",
                "There's reasonable consistency between the candidate's background and the role's expectations.",
                "The candidate's experience appears relevant to the position based on the content analysis."
            ]
        elif semantic_similarity > 0.4:
            semantic_phrases = [
                "The resume has some alignment with the job description, though not strongly focused on all key areas.",
                "There's moderate relevance between the candidate's background and the position requirements.",
                "The content shows partial overlap with what the role typically demands."
            ]
        else:
            semantic_phrases = [
                "The resume content doesn't closely match the job description's focus areas and requirements.",
                "There appears to be limited alignment between the candidate's background and the specific role needs.",
                "The content suggests this might not be an ideal match based on how experiences are presented."
            ]
        
        explanation_parts.append(random.choice(semantic_phrases))

    # ----------------------------
    # Skill overlap explanation (relational)
    # ----------------------------
    if skill_overlap is not None:
        if skill_overlap > 0.7:
            overlap_phrases = [
                "Most required skills for the role appear to be covered by the candidate's demonstrated abilities.",
                "The candidate matches the majority of technical requirements needed for success in this position.",
                "There's strong overlap between what the role demands and what the candidate offers in terms of capabilities."
            ]
        elif skill_overlap > 0.5:
            overlap_phrases = [
                "The candidate possesses many of the key skills needed for this role.",
                "There's good coverage of the required competencies based on the skills mentioned.",
                "A substantial portion of the necessary skills are reflected in the candidate's profile."
            ]
        elif skill_overlap > 0.3:
            overlap_phrases = [
                "Some important skills are present, though additional development may be needed for certain areas.",
                "The candidate has some relevant capabilities, though not all required skills are clearly demonstrated.",
                "There's partial skill alignment, with room for growth in specific technical areas."
            ]
        else:
            overlap_phrases = [
                "Limited overlap exists between the required skills and those demonstrated by the candidate.",
                "The candidate would need to develop several key skills to fully meet the role requirements.",
                "There appears to be a significant gap between the skills needed and those currently demonstrated."
            ]
        
        explanation_parts.append(random.choice(overlap_phrases))

    # ----------------------------
    # Overall recommendation (conversational)
    # ----------------------------
    if match_score >= 0.75:
        recommendation = [
            "Overall, this candidate appears to be a strong contender worth considering for further review.",
            "In summary, the candidate demonstrates good qualifications and merits serious consideration.",
            "Based on this analysis, the candidate shows promise and could be a valuable addition to the team."
        ]
    elif match_score >= 0.50:
        recommendation = [
            "This candidate shows potential but may require careful evaluation of specific fit aspects.",
            "Overall, there's reasonable alignment though certain areas might need closer examination.",
            "The candidate has some relevant qualifications that could be developed with the right support."
        ]
    else:
        recommendation = [
            "While every candidate has unique strengths, this profile may not align optimally with the current requirements.",
            "This candidate might be better suited for roles with different requirements or focus areas.",
            "Based on this assessment, other candidates may offer stronger alignment with the specific needs of this role."
        ]
    
    explanation_parts.append(random.choice(recommendation))
    
    # ----------------------------
    # Score context (educational)
    # ----------------------------
    score_context = f"Our analysis generated a match score of {match_score:.2f} on a 0-1 scale, where higher scores indicate better alignment. This score considers multiple factors including skills, experience, and overall relevance."
    
    explanation_parts.append(score_context)
    
    # Combine with natural flow
    explanation = " ".join(explanation_parts)
    
    # Clean up any awkward phrasing
    explanation = explanation.replace("  ", " ").replace(" ,", ",").replace(" .", ".")
    
    # Ensure proper capitalization
    if explanation and explanation[0].islower():
        explanation = explanation[0].upper() + explanation[1:]
    
    return explanation


def generate_brief_summary(
    match_score,
    top_skills,
    experience_years
):
    """
    Generate a concise, human-friendly summary for quick review.
    """
    
    def get_score_adjective(score):
        if score >= 0.85:
            return "Excellent match"
        elif score >= 0.70:
            return "Strong candidate"
        elif score >= 0.50:
            return "Moderate fit"
        elif score >= 0.30:
            return "Limited alignment"
        else:
            return "Poor match"
    
    score_label = get_score_adjective(match_score)
    
    # Experience description
    if experience_years >= 8:
        exp_desc = "experienced professional"
    elif experience_years >= 4:
        exp_desc = "mid-level candidate"
    elif experience_years >= 1:
        exp_desc = "early-career candidate"
    else:
        exp_desc = "entry-level candidate"
    
    # Skills highlight
    if top_skills:
        if len(top_skills) >= 3:
            skills_desc = f"Skills include {top_skills[0]}, {top_skills[1]}, and {top_skills[2]}"
        elif len(top_skills) == 2:
            skills_desc = f"Skills include {top_skills[0]} and {top_skills[1]}"
        else:
            skills_desc = f"Skill focus on {top_skills[0]}"
    else:
        skills_desc = "Skills not specified"
    
    summary = f"{score_label} | {exp_desc} | {skills_desc}"
    
    return summary