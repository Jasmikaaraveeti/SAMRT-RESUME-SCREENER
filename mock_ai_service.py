import random

def generate_mock_screening_result(candidate_text: str, job_description: str, required_skills: str):
    score = random.randint(50, 98)
    skills_score = min(100, score + random.randint(-10, 10))
    experience_score = min(100, score + random.randint(-15, 15))
    education_score = min(100, score + random.randint(-5, 15))

    req_skills_list = [s.strip() for s in required_skills.split(',') if s.strip()]
    matched = []
    missing = []
    
    for skill in req_skills_list:
        if random.random() > 0.3:
            matched.append(skill)
        else:
            missing.append(skill)
            
    strengths = [
        "Strong alignment with core requirements.",
        "Relevant experience in similar roles.",
        f"Solid background in {matched[0] if matched else 'key technologies'}."
    ]
    
    weaknesses = [
        f"Lacks clear evidence of {missing[0]}." if missing else "No major weaknesses identified.",
        "Could benefit from more recent certifications."
    ]

    if score >= 80:
        recommendation = "Shortlist"
        justification = f"This candidate demonstrates strong alignment with the role. The resume highlights experience with {', '.join(matched[:3])}. They exceed the primary requirements and are a strong fit."
    elif score >= 60:
        recommendation = "Review"
        justification = f"This candidate has moderate alignment. While they have {', '.join(matched[:2])}, they are missing {', '.join(missing[:2])}. Worth a closer look by the hiring manager."
    else:
        recommendation = "Reject"
        justification = f"This candidate does not meet the minimum requirements for the role. Significant skill gaps include {', '.join(missing)}."

    return {
        "match_score": score,
        "skills_score": skills_score,
        "experience_score": experience_score,
        "education_score": education_score,
        "matched_skills": ", ".join(matched),
        "missing_skills": ", ".join(missing),
        "strengths": "\n".join(strengths),
        "weaknesses": "\n".join(weaknesses),
        "justification": justification,
        "recommendation": recommendation
    }
