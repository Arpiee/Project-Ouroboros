import os
import json
from groq import Groq


class EthicsEvaluatorAgent:
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
                    "risk_score": 50,
                    "risk_level": "Medium",
                    "key_risks": ["Model returned invalid JSON."],
                    "mitigations": [],
                    "summary": "Ethics analysis unavailable due to parsing error."
                }

    def run(self, payload: dict):
        idea = payload.get("idea", {})

        prompt = f"""
You are an ethics and risk analyst.

Evaluate ethical, regulatory, and reputational risks of this idea.

Return ONLY valid JSON. No explanations, no markdown, no text outside the JSON.

Use this exact structure:

{{
  "risk_score": 0,
  "risk_level": "Low",
  "key_risks": ["bullet 1", "bullet 2"],
  "mitigations": ["bullet 1", "bullet 2"],
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
            print("EthicsEvaluator RAW:", content)

        return self._parse_json(content)
