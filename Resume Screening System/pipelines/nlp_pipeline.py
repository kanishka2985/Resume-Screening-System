import re
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# SKILLS DATABASE 
SKILLS_DB = [
    "python", "machine learning", "deep learning", "nlp",
    "data analysis", "sql", "pandas", "numpy",
    "tensorflow", "pytorch", "docker", "aws",
    "flask", "fastapi", "javascript", "react"
]

# PREPROCESS TEXT
def preprocess_text(text):
    doc = nlp(text.lower())
    
    tokens = [
        token.lemma_
        for token in doc
        if not token.is_stop and not token.is_punct
    ]
    
    return " ".join(tokens)


# EXTRACT SKILLS 
def extract_skills(text):
    text = text.lower()
    found_skills = []

    for skill in SKILLS_DB:
        if skill in text:
            found_skills.append(skill)

    return list(set(found_skills))


# EXTRACT EXPERIENCE 
def extract_experience(text):
    patterns = [
        r"(\d+)\s+years",
        r"(\d+)\+?\s+yrs",
        r"(\d+)\+?\s+year"
    ]

    for pattern in patterns:
        match = re.search(pattern, text.lower())
        if match:
            return int(match.group(1))

    return 0


# COMPUTE SIMILARITY 
def compute_similarity(resume_text, job_description):
    documents = [resume_text, job_description]

    tfidf = TfidfVectorizer()
    vectors = tfidf.fit_transform(documents)

    similarity = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]

    return round(similarity * 100, 2)


#  MAIN FUNCTION 
def analyze_resume_nlp(resume_text, job_description):
    
    # Preprocess text
    clean_resume = preprocess_text(resume_text)
    clean_jd = preprocess_text(job_description)

    # Extract skills
    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(job_description)

    # Extract experience
    experience = extract_experience(resume_text)

    # Match score
    match_score = compute_similarity(clean_resume, clean_jd)

    # Missing skills
    missing_skills = list(set(jd_skills) - set(resume_skills))

    # Strengths (common skills)
    strengths = list(set(resume_skills) & set(jd_skills))

    return {
        "match_score": match_score,
        "skills": resume_skills,
        "experience_years": experience,
        "missing_skills": missing_skills,
        "strengths": strengths
    }


# TEST 
if __name__ == "__main__":
    resume = """
    Python developer with 2 years of experience in machine learning,
    worked with pandas, numpy, and flask.
    """

    jd = """
    Looking for a Machine Learning Engineer with Python,
    numpy, flask, and deep learning experience.
    """
    analyze_resume_nlp(resume, jd)
    