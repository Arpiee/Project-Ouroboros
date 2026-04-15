import os
import json
from groq import Groq


class ImpactEvaluatorAgent:
    def __init__(self, debug: bool = False):
        self.debug = debug
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    def _parse_json(self, content: str):
        """Attempts strict JSON parsing, then repairs if needed."""
        try:
            return json.loads(content)
        except Exception:
            try:
                start = content.index("{")
                end = content.rindex("}") + 1
                return json.loads(content[start:end])
            except Exception:
                return {
                    "impact_score": 50,
                    "user_impact": "Unknown",
                    "market_impact": "Unknown",
                    "long_term_potential": "Unknown",
                    "impact_drivers": ["Model returned invalid JSON."],
                    "summary": "Impact analysis unavailable due to parsing error."
                }

    def run(self, payload: dict):
        idea = payload.get("idea", {})

        prompt = f"""
You are a startup impact analyst.

Evaluate the potential impact of this idea on users and the market.

Return ONLY valid JSON. No explanations, no markdown, no text outside the JSON.

Use this exact structure:

{{
  "impact_score": 0,
  "user_impact": "short text",
  "market_impact": "short text",
  "long_term_potential": "short text",
  "impact_drivers": ["bullet 1", "bullet 2"],
  "summary": "1-2 sentence summary"
}}

Idea: {idea.get("idea_description", "")}
Problem: {idea.get("problem", "")}
Customer: {idea.get("target_customer", "")}
Stage: {idea.get("stage", "")}
"""

        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4
        )

        content = response.choices[0].message.content.strip()

        if self.debug:
            print("ImpactEvaluator RAW:", content)

        return self._parse_json(content)
