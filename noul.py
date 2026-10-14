import os
import requests
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Guard clause to check if your .env file is actually being read
if not OPENROUTER_API_KEY:
    raise ValueError(
        "CRITICAL: OPENROUTER_API_KEY is missing or None. "
        "Make sure you have a file named '.env' containing 'OPENROUTER_API_KEY=your_key' "
        "in the same folder as this script."
    )

# Jev uses OpenRouter's Decisions API, not chat/completions
url = "https://openrouter.ai/api/alpha/decisions"

payload = {
    "model": "typesafe/jev-1.13",
    "state": "The user reported: 'I was charged twice on my invoice today.'",
    "questions": {
        "is_billing_issue": {
            "type": "noul",
            "instructions": "Is this a billing-related problem?"
        }
    }
}

headers = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)
print(response.status_code)
print(response.json())