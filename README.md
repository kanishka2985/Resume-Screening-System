# 📄 Resume Screening System (AI-Powered)

An **AI-powered Resume Screening System** that evaluates resumes against a job description using a hybrid approach combining **Natural Language Processing (NLP)** and **Large Language Models (LLMs)**.

This system is designed to go beyond basic keyword matching by understanding both **text similarity** and **contextual meaning**, making candidate evaluation more accurate and intelligent.

---

## 🚀 Features

- 📂 **Resume Processing**
  - Supports PDF, DOCX, TXT formats
  - Extracts and processes resume text

- 🧠 **NLP-Based Analysis**
  - Text preprocessing (cleaning, tokenization)
  - Keyword extraction and matching
  - Fast similarity scoring

- 🤖 **LLM-Based Evaluation**
  - Context-aware understanding of resume content
  - Evaluates meaning, not just keywords
  - Handles synonyms and implicit skills

- 🎯 **Hybrid Scoring System**
  - Combines NLP + LLM scores
  - Produces a final **hybrid match score**

- 📊 **Candidate Evaluation**
  - Resume vs Job Description comparison
  - Skill relevance analysis

---

## 🧠 Why Combine NLP and LLM?

Traditional resume screening systems rely only on **NLP-based keyword matching**, which has limitations:

### ❌ Limitations of NLP Alone
- Matches exact keywords only  
- Cannot understand context or meaning  
- Fails when synonyms are used  
  - Example: “ML” vs “Machine Learning”  
- May reject good candidates due to wording differences  

---

### ❌ Limitations of LLM Alone
- Slower and more computationally expensive  
- May produce inconsistent scoring  
- Not optimized for precise keyword matching  

---

### ✅ Advantage of Hybrid Approach (NLP + LLM)

This system combines the strengths of both:

- ⚡ **NLP** → Fast, structured, keyword-based scoring  
- 🧠 **LLM** → Deep semantic understanding  

### 🔥 Result:
- More accurate candidate evaluation  
- Better handling of real-world resumes  
- Balanced performance (speed + intelligence)  

👉 Example:
- Resume says: *“Worked on predictive models using Python”*  
- JD says: *“Machine Learning experience required”*  

✔ NLP might miss this  
✔ LLM understands the relationship  
✔ Hybrid system gives correct score  

---

## 🛠️ Tech Stack

- **Language:** Python  

- **Core Concepts:**
  - Natural Language Processing (NLP)
  - Large Language Models (LLM)
  - Text Similarity & Semantic Matching  

- **Libraries (Expected):**
  - nltk / spacy  
  - scikit-learn  
  - transformers (optional)  
  - PyPDF2 / python-docx  

---

## ⚙️ How It Works

1. **Resume Input**
   - Resume file is provided  

2. **Text Extraction**
   - Extracts raw text from resume  

3. **Preprocessing**
   - Cleans and normalizes text  

4. **NLP Pipeline**
   - Calculates keyword similarity with job description  

5. **LLM Pipeline**
   - Performs semantic evaluation  

6. **Hybrid Scoring**
   - Combines both scores to produce final result  

---

#### Expected Request (Form Data):

- `resume` → Uploaded file (PDF, DOCX, TXT)  
- `jd` → Job description text  

---

### 📤 Expected Response (JSON Format):

```json
{
  "matchedSkills": [
    { "name": "Python", "hybrid": 90, "category": "green" }
  ],
  "missingSkills": [
    { "name": "Docker", "note": "Required in JD" }
  ],
  "experience": [
    {
      "company": "ABC Corp",
      "role": "ML Engineer",
      "dates": "2021 - Present"
    }
  ],
  "scores": {
    "hybrid": 85
  },
  "contact": {
    "Email": "example@mail.com",
    "Phone": "+91XXXXXXXXXX"
  },
  "totalExp": "3 Years",
  "education": "B.Tech CSE"
}
```
---
## 📁 Project Structure
│
├── pipelines/
│ ├── hybrid.py # Combines NLP + LLM scores
│ ├── llm_pipeline.py # LLM-based evaluation logic
│ ├── nlp_pipeline.py # NLP processing & similarity
│
├── utils/
│ ├── preprocessing.py # Text cleaning & preprocessing
│ ├── text_extractor.py # Extract text from resumes
│
├── requirements.txt # Dependencies
└── README.md # Documentation

---
