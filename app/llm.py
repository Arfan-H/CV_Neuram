import os
import json
import requests
import re

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")


def extract_json(text: str) -> dict:
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise ValueError("No JSON found in LLM output")
    return json.loads(match.group())


def summarize_cv_with_llm(cv_text: str) -> dict:
    prompt = f"""
Extract the following information from the CV.

Return ONLY valid JSON:
{{
  "name": "",
  "location": "",
  "work_experience_summary": ""
}}

CV:
{cv_text}
"""

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost",
            "X-Title": "Neuram Technical Assessment",
        },
        json={
            "model": "nvidia/nemotron-3-nano-30b-a3b:free",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0,
        },
        timeout=30,
    )

    response.raise_for_status()

    raw_output = response.json()["choices"][0]["message"]["content"]
    return extract_json(raw_output)
