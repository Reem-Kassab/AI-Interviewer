import os
import requests
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

def generate_questions(job_description, num_questions, user_profile_summary):
    if not api_key:
        raise Exception("API key not found in environment variables.")

    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    prompt = f"""
You are an AI interviewer.

Below is the candidate's profile summary:
\"\"\"{user_profile_summary}\"\"\"

First, extract the candidate's name from the summary (if available), and then use it while generating {num_questions} technical interview questions.

Make the questions personalized by addressing the candidate by name where appropriate. Use a conversational and human tone.

Only return the questions as a numbered list, one per line, without any explanations or extra text.

Job Description:
\"\"\"{job_description}\"\"\"
"""

    data = {
        "model": "z-ai/glm-4.5-air:free",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        result = response.json()
        content = result["choices"][0]["message"]["content"]
        questions = content.strip().split("\n")
        cleaned = [q.strip().lstrip("1234567890. ").strip() for q in questions if q.strip()]
        return cleaned
    else:
        raise Exception(f"Error {response.status_code}: {response.text}")
