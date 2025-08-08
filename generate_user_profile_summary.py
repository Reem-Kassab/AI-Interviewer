import os
import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

def generate_user_profile_summary(cv_text, intro_answer):
    if not api_key:
        raise Exception("API key not found.")

    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    prompt = f"""
You are an intelligent assistant that summarizes candidate profiles.

Below is the candidate's self-introduction:
\"\"\"{intro_answer}\"\"\"

{"Here is their CV content:" if cv_text else ""}
\"\"\"{cv_text if cv_text else ""}\"\"\"

Based on the above, generate a short and smart summary of the candidate’s profile that includes:
- Their name (if mentioned)
- Background and studies
- Technical skills and strengths
- Any other useful personality or professional traits

Do not repeat the full text. Write a clean 5-7 line summary in natural human language.
"""

    data = {
        "model": "z-ai/glm-4.5-air:free",
        "messages": [{"role": "user", "content": prompt}]
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        result = response.json()
        return result["choices"][0]["message"]["content"].strip()
    else:
        raise Exception(f"Error: {response.status_code} - {response.text}")
