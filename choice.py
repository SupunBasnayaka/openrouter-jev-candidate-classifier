import os
import requests
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if not OPENROUTER_API_KEY:
    raise ValueError("CRITICAL: OPENROUTER_API_KEY is missing from your .env file.")

url = "https://openrouter.ai/api/alpha/decisions"

payload = {
    "model": "typesafe/jev-1.13",
    "state": "The user said: 'I think this feature is completely unnecessary and ruins the workflow.'",
    "questions": {
        "user_stance": {
            "type": "choice",
            "instructions": "Determine if the user agrees or disagrees with the feature.",
            "criteria": {
                "agree": "The user supports, likes, or agrees with the feature",
                "disagree": "The user opposes, dislikes, or disagrees with the feature",
                "neutral": "The user expresses no clear opinion either way"
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

probabilities = data["answers"]["user_stance"]["probabilities"]
best_choice = max(probabilities, key=probabilities.get)
best_score = probabilities[best_choice]
print(best_choice)