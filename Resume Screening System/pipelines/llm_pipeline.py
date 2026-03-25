import google.generativeai as genai
from dotenv import load_dotenv
import os
import json

# LOAD ENV 
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file")

genai.configure(api_key=api_key)

#MODEL CONFIG 
generation_config = {
    "temperature": 0.4,  # more consistent output
    "top_p": 0.9,
    "top_k": 40,
    "max_output_tokens": 2048,
    "response_mime_type": "application/json"  # ensures JSON output
}

model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    generation_config=generation_config
)

# MAIN FUNCTION 
def analyze_resume_llm(resume_text, job_description):
    try:
        # Limit input size (important for long resumes)
        resume_text = resume_text[:5000]
        job_description = job_description[:3000]

        prompt = f"""
You are an expert HR resume screening system.

Analyze the resume against the job description.

Return ONLY valid JSON in this format:
{{
  "match_score": number,
  "skills": [],
  "missing_skills": [],
  "strengths": [],
  "suggestions": [],
  "summary": ""
}}

Rules:
- match_score must be between 0 and 100
- skills = all relevant skills found in resume
- missing_skills = skills present in job description but missing in resume
- strengths = key matching skills
- suggestions = actionable improvements
- summary = 2-3 lines max

Resume:
{resume_text}

Job Description:
{job_description}
"""

        response = model.generate_content(prompt)

        # Parse JSON safely
        result_text = response.text.strip()
        result = json.loads(result_text)

        return result

    except json.JSONDecodeError:
        return {
            "error": "Invalid JSON response from LLM",
            "raw_output": response.text
        }

    except Exception as e:
        return {
            "error": str(e)
        }


# TEST
if __name__ == "__main__":
    resume = """
    Python developer with 2 years of experience in machine learning,
    worked with pandas, numpy, and flask.
    """

    jd = """
    Looking for a Machine Learning Engineer with Python,
    Docker, AWS, and deep learning experience.
    """

    result = analyze_resume_llm(resume, jd)
    print(result)