import os
import requests
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if not OPENROUTER_API_KEY:
    raise ValueError("CRITICAL: OPENROUTER_API_KEY is missing from your .env file.")

url = "https://openrouter.ai/api/alpha/decisions"

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
- Skills: {candidate_skills}
- Experience: {candidate_experience}
"""

payload = {
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
headers = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)
data = response.json()

probabilities = data["answers"]["candidate_evaluation"]["probabilities"]
best_choice = max(probabilities, key=probabilities.get)
best_score = probabilities[best_choice]
print(best_choice)