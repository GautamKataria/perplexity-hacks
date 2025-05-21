import requests
import json
from config import PERPLEXITY_API_KEY

API_URL = "https://api.perplexity.ai/chat/completions"

DEFAULT_PILLARS = ["financial", "news", "market", "adoption", "competitor", "contextual"]

def get_subject_and_focus_from_agent(query: str) -> dict:
    """
    Use Perplexity Sonar to:
    - Detect if the query requires a full analysis or just a direct answer
    - Extract subject and relevant pillars (if analysis)
    Returns:
        {
            "type": "analysis" or "direct_answer",
            "subject": "Nvidia",
            "focus": ["news", "market"],
            "answer": "The stock price of Nvidia is $X.XX"
        }
    """
    payload = {
        "model": "sonar",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are an AI assistant that detects whether a query needs analytical breakdown "
                    "(like financial, market, news, competitor analysis), or is a factual question that can be directly answered.\n"
                    "Respond ONLY in this strict JSON format:\n"
                    '{ "type": "analysis" or "direct_answer", "subject": "string", "focus": ["pillar1", "pillar2", ...], "answer": "answer to direct question" }\n\n'
                    "Examples:\n"
                    '- "what’s up with nvidia this week" → {"type": "analysis", "subject": "Nvidia", "focus": ["news", "market"]}\n'
                    '- "what is the stock price of nvidia?" → {"type": "direct_answer", "subject": "Nvidia", "focus": [], "answer": "The stock price of Nvidia is $X.XX"}\n'
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

        output = {
            "type": parsed.get("type", "analysis"),
            "subject": parsed.get("subject", "Unknown"),
            "focus": [f for f in parsed.get("focus", DEFAULT_PILLARS) if f in DEFAULT_PILLARS],
            "answer": parsed.get("answer", "")
        }

        if output["type"] == "analysis" and not output["focus"]:
            output["focus"] = DEFAULT_PILLARS

        return output

    except Exception as e:
        print(f"[Agent Intent Parsing Error] {e}")
        return {
            "type": "analysis",
            "subject": "Unknown",
            "focus": DEFAULT_PILLARS
        }
