# ---------------- hybrid.py ----------------
from pipelines.nlp_pipeline import analyze_resume_nlp, compute_similarity
from pipelines.llm_pipeline import analyze_resume_llm
from typing import Dict, List

# ---------------- WEIGHTS ----------------
NLP_WEIGHT = 0.6
LLM_WEIGHT = 0.4
MAYBE_THRESHOLD = 0.5


# ---------------- NORMALIZATION ----------------
def normalize_nlp_output(nlp_result):
    return {
        "match_score": nlp_result.get("match_score", 0),
        "skills": nlp_result.get("skills", []),
        "missing_skills": nlp_result.get("missing_skills", []),
        "strengths": nlp_result.get("strengths", []),
        "experience_years": nlp_result.get("experience_years", 0)
    }


def normalize_llm_output(llm_result):
    return {
        "match_score": llm_result.get("match_score", 0),
        "skills": llm_result.get("skills", []),
        "missing_skills": llm_result.get("missing_skills", []),
        "strengths": llm_result.get("strengths", []),
        "suggestions": llm_result.get("suggestions", []),
        "summary": llm_result.get("summary", "")
    }


# ---------------- HELPER ----------------
def normalize_skill(skill: str) -> str:
    return skill.strip().lower()


# ---------------- INSIGHT GENERATOR ----------------
def generate_insights(strengths, improvements, score):
    if score >= 75:
        decision = "Shortlist Candidate"
    elif score >= 50:
        decision = "Consider with verification"
    else:
        decision = "Not recommended"

    if strengths:
        insight = f"Candidate shows strong knowledge in {', '.join(strengths[:3])}. "
    else:
        insight = "Candidate lacks strong core skills. "

    if improvements:
        insight += f"However, skills like {', '.join(improvements[:3])} are not clearly demonstrated. "
        insight += "Verify these during interview."
    else:
        insight += "Candidate matches job requirements very well."

    return insight, decision


# ---------------- HYBRID FUNCTION ----------------
def analyze_resume_hybrid(resume_text: str, job_description: str) -> Dict:

    # 1️⃣ RAW OUTPUTS
    nlp_raw = analyze_resume_nlp(resume_text, job_description)
    llm_raw = analyze_resume_llm(resume_text, job_description)

    # 2️⃣ NORMALIZE OUTPUT FORMAT
    nlp_result = normalize_nlp_output(nlp_raw)
    llm_result = normalize_llm_output(llm_raw)

    # 3️⃣ EXTRACT SKILLS
    nlp_skills_raw = nlp_result["skills"]
    llm_skills_raw = llm_result["skills"]

    # Handle LLM dict case
    if isinstance(llm_skills_raw, dict):
        llm_skills_dict_raw = llm_skills_raw
        llm_skills_list_raw = list(llm_skills_raw.keys())
    else:
        llm_skills_list_raw = llm_skills_raw
        llm_skills_dict_raw = {s: 1.0 for s in llm_skills_list_raw}

    #  NORMALIZE SKILLS (IMPORTANT FIX)
    nlp_skills = [normalize_skill(s) for s in nlp_skills_raw]
    llm_skills = [normalize_skill(s) for s in llm_skills_list_raw]

    # Also normalize LLM dict keys
    llm_skills_dict = {
        normalize_skill(k): v for k, v in llm_skills_dict_raw.items()
    }

    # 5COMBINE UNIQUE SKILLS
    resume_skills = list(set(nlp_skills + llm_skills))

    # JD SKILLS (normalized)
    jd_raw = analyze_resume_nlp(job_description, job_description).get("skills", [])
    jd_skills = list(set([normalize_skill(s) for s in jd_raw]))

    # ---------------- MATCH SCORE ----------------
    resume_text_skills = " ".join(resume_skills)
    jd_text_skills = " ".join(jd_skills)

    similarity = compute_similarity(resume_text_skills, jd_text_skills)
    hybrid_match_score = int(round(similarity))

    # ---------------- SKILL CONFIDENCE ----------------
    hybrid_skills: List[Dict] = []
    strengths = []
    improvements = []

    for skill in resume_skills:
        nlp_score = 1.0 if skill in nlp_skills else 0.0
        llm_score = llm_skills_dict.get(skill, 0.0)

        hybrid_score = NLP_WEIGHT * nlp_score + LLM_WEIGHT * llm_score
        flag = "confirmed" if hybrid_score >= MAYBE_THRESHOLD else "maybe"

        skill_obj = {
            "name": skill.capitalize(),  # UI friendly
            "nlp": int(nlp_score * 100),
            "llm": int(llm_score * 100),
            "hybrid": int(hybrid_score * 100),
            "status": flag
        }

        hybrid_skills.append(skill_obj)

        if flag == "confirmed":
            strengths.append(skill)
        else:
            improvements.append(skill)

    # ---------------- MISSING SKILLS ----------------
    missing_skills_raw = list(set(
        nlp_result["missing_skills"] + llm_result["missing_skills"]
    ))

    missing_skills = list(set([normalize_skill(s) for s in missing_skills_raw]))

    missing_skills_formatted = [
        {
            "name": s.capitalize(),
            "note": "Recommended to add in resume or gain experience"
        }
        for s in missing_skills
    ]

    # ---------------- INSIGHTS ----------------
    insights, decision = generate_insights(
        strengths, improvements, hybrid_match_score
    )

    # ---------------- FINAL OUTPUT ----------------
    return {
        "scores": {
            "hybrid": hybrid_match_score
        },
        "matchedSkills": hybrid_skills,
        "missingSkills": missing_skills_formatted,
        "strengths": [s.capitalize() for s in strengths],
        "improvements": [s.capitalize() for s in improvements],
        "suggestions": llm_result["suggestions"],
        "summary": llm_result["summary"],
        "insights": insights,
        "decision": decision,
        "totalExp": f"{nlp_result['experience_years']} yrs"
    }


# ---------------- TEST ----------------
if __name__ == "__main__":
    resume = """
    Python developer with 2 years of experience in machine learning,
    worked with pandas, numpy, and flask.
    """

    jd = """
    Looking for a Machine Learning Engineer with Python,
    numpy, flask, and deep learning experience.
    """

    result = analyze_resume_hybrid(resume, jd)

    from pprint import pprint
    pprint(result)