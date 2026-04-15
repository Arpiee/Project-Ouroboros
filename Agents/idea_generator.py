import os
import json
from groq import Groq


class IdeaGeneratorAgent:
    def __init__(self, debug: bool = False):
        self.debug = debug
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    def _parse_json(self, content: str):
        """Attempts strict JSON parsing, then repairs if needed."""
        try:
            return json.loads(content)
        except Exception:
            try:
                start = content.index("[")
                end = content.rindex("]") + 1
                return json.loads(content[start:end])
            except Exception:
                return [
                    {
                        "title": "Fallback Idea",
                        "description": "Model returned invalid JSON; this is a placeholder idea.",
                        "category": "General",
                        "why_now": "Fallback.",
                        "target_customer": "General builders.",
                        "problem": "No valid ideas generated.",
                        "revenue_model": "Subscription",
                        "stage": "Idea only"
                    }
                ]

    def run(self, payload: dict):
        budget = payload.get("budget", 1000)
        goal = payload.get("goal", "")
        constraints = payload.get("constraints", "")
        trends = payload.get("trends", {})

        prompt = f"""
You are a startup idea generator.

Generate 5 concrete startup ideas that match:

Goal: {goal}
Budget: {budget}
Constraints: {constraints}
Trend context: {trends}

Return ONLY valid JSON. No explanations, no markdown, no text outside the JSON.

Use this exact structure:

[
  {{
    "title": "short idea name",
    "description": "2-3 sentence description",
    "category": "short category label",
    "why_now": "short explanation",
    "target_customer": "short description",
    "problem": "short description",
    "revenue_model": "short description",
    "stage": "Idea only"
  }}
]
"""

        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )

        content = response.choices[0].message.content.strip()

        if self.debug:
            print("IdeaGenerator RAW:", content)

        return self._parse_json(content)
