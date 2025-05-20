import requests
import json
from config import PERPLEXITY_API_KEY

API_URL = "https://api.perplexity.ai/chat/completions"

DEFAULT_PILLARS = ["financial", "news", "market", "adoption", "competitor", "contextual"]

def get_subject_and_focus_from_agent(query: str) -> (str, list):
    """
    Use Perplexity Sonar to extract the subject and multiple analysis focuses.
    If extraction fails, defaults to all pillars.
    """
    payload = {
        "model": "sonar",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are an AI assistant that extracts structured analytical intent from vague user queries.\n"
                    "Respond ONLY in this strict JSON format:\n"
                    '{ "subject": "subject string", "focus": ["financial", "news", "market", "adoption", "competitor", "contextual"] }\n\n'
                    "Choose multiple relevant focus values if needed.\n"
                    "Examples:\n"
                    '- "what’s up with nvidia this week" → {"subject": "Nvidia", "focus": ["news", "financial", "market"]}\n'
                    '- "how is the ai smbs market trending" → {"subject": "AI SMBs", "focus": ["market", "adoption"]}'
                )
            },
            {"role": "user", "content": query}
        ]
    }

    headers = {
        "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        res = requests.post(API_URL, headers=headers, json=payload, timeout=20)
        res.raise_for_status()
        raw = res.json()["choices"][0]["message"]["content"].strip()

        json_start = raw.find("{")
        json_end = raw.rfind("}") + 1
        parsed = json.loads(raw[json_start:json_end])

        subject = parsed.get("subject", "Unknown")
        focuses = parsed.get("focus", DEFAULT_PILLARS)
        valid_focuses = [f for f in focuses if f in DEFAULT_PILLARS]

        return subject, valid_focuses or DEFAULT_PILLARS

    except Exception as e:
        print(f"[Agent Intent Parsing Error] {e}")
        return "Unknown", DEFAULT_PILLARS
