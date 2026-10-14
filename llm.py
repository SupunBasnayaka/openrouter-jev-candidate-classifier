import os
import requests
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if not OPENROUTER_API_KEY:
    raise ValueError("CRITICAL: OPENROUTER_API_KEY is missing from your .env file.")

# OpenRouter Endpoints
DECISION_URL = "https://openrouter.ai/api/alpha/decisions"
LLM_URL = "https://openrouter.ai/api/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json"
}

# Fixed job requirements
job_requirements = """
JOB REQUIREMENTS:
- Position: Senior Data Scientist
- Required Skills: Python, SQL, Machine Learning, FAISS, FastMCP/LangChain
- Experience: 3+ years in AI development, production model deployment, and agentic workflows.
"""

# Get candidate profile dynamically from user input
print("--- Enter Candidate Profile Information ---")
candidate_skills = input("Enter candidate skills (e.g. Python, SQL, Docker): ")
candidate_experience = input("Enter candidate experience (e.g. 2 years building RAG pipelines): ")

# Construct the dynamic state
state_description = f"""
{job_requirements}

CANDIDATE PROFILE:
- Skills: 
{candidate_skills}
- Experience: 
{candidate_experience}
"""

# STEP 1: Decision Model Request
payload_decision = {
    "model": "typesafe/jev-1.13",
    "state": state_description,
    "questions": {
        "candidate_evaluation": {
            "type": "choice",
            "instructions": "Evaluate how well the candidate's skills and experience match the job requirements.",
            "criteria": {
                "strong_match": "Candidate meets or exceeds all required technical skills and experience levels",
                "potential_match": "Candidate has strong related technical skills but may be slightly missing explicit years or core criteria",
                "reject": "Candidate lacks core technical experience or required background"
            }
        }
    }
}

response_decision = requests.post(DECISION_URL, json=payload_decision, headers=headers)
data_decision = response_decision.json()

probabilities = data_decision["answers"]["candidate_evaluation"]["probabilities"]
best_choice = max(probabilities, key=probabilities.get)
best_score = probabilities[best_choice]

print(f"\n[Decision API Output]: {best_choice} (Confidence: {best_score:.2%})")

# STEP 2: Generative LLM Response Generation
prompt = f"""
You are an HR technical recruiter evaluating a candidate for a Senior Data Scientist position.

Job Requirements:
{job_requirements}

Candidate Details:
- Skills: {candidate_skills}
- Experience: {candidate_experience}

Automated Screening Verdict: {best_choice} (Confidence Score: {best_score:.2%})

Task:
Write a brief, professional evaluation note summarizing why the candidate received this verdict. Highlight key matching skills or missing qualifications based on the job criteria.
"""

payload_llm = {
    "model": "meta-llama/llama-3.3-70b-instruct",
    "messages": [
        {"role": "system", "content": "You are a concise, professional technical recruiter."},
        {"role": "user", "content": prompt}
    ],
    "temperature": 0.7
}

response_llm = requests.post(LLM_URL, json=payload_llm, headers=headers)
data_llm = response_llm.json()

# Print the natural language output
llm_reply = data_llm["choices"][0]["message"]["content"]
print("\n--- Candidate Evaluation Summary ---")
print(llm_reply)