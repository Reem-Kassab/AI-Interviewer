import os
import requests
import re
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")


def analyze_answer(all_answers, job_description, profile_summary=""):
    if not api_key:
        raise Exception("API key not found in environment variables.")

    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    answers_text = ""
    for i, ans in enumerate(all_answers, 1):
        answers_text += f"\nQ{i}: Answer:\n\"\"\"{ans.strip()}\"\"\"\n"

    prompt = f"""
You are an AI Interview Coach.

A candidate answered the following technical interview questions:

{answers_text}

Job Description:
\"\"\"{job_description}\"\"\"

Candidate Profile Summary:
\"\"\"{profile_summary}\"\"\"


Please analyze the overall performance of the candidate based on their answers, the job description, and their profile.

Return a clean, structured evaluation. **Do not use JSON or markdown. Only return plain text.**

Format:

Clarity: [Excellent / Good / Average / Poor]  
Confidence: [Excellent / Good / Average / Poor]  
Relevance to Job Description: [Excellent / Good / Average / Poor]  
Language Use: [Excellent / Good / Average / Poor]  

Strengths:
- [list strength points]

Weaknesses:
- [list weakness points]

Suggestions to Improve:
- [list improvement tips]
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
        return re.sub(r"```(?:json)?", "", content).strip()
    else:
        raise Exception(f"Error {response.status_code}: {response.text}")
