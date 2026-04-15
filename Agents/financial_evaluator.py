import os
import json
from groq import Groq


class FinancialEvaluatorAgent:
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
                    "financial_score": 50,
                    "revenue_potential": "Unknown",
                    "cost_intensity": "Unknown",
                    "payback_period": "Unknown",
                    "key_assumptions": ["Model returned invalid JSON."],
                    "summary": "Financial analysis unavailable due to parsing error."
                }

    def run(self, payload: dict):
        idea = payload.get("idea", {})
        budget = payload.get("budget", None)
        time_horizon = payload.get("time_horizon", None)

        prompt = f"""
You are a startup financial analyst.

Evaluate the financial potential of this idea.

Return ONLY valid JSON. No explanations, no markdown, no text outside the JSON.

Use this exact structure:

{{
  "financial_score": 0,
  "revenue_potential": "short text",
  "cost_intensity": "short text",
  "payback_period": "short text",
  "key_assumptions": ["bullet 1", "bullet 2"],
  "summary": "1-2 sentence summary"
}}

Idea: {idea.get("idea_description", "")}
Problem: {idea.get("problem", "")}
Customer: {idea.get("target_customer", "")}
Competitors: {idea.get("competitors", "")}
Revenue Model: {idea.get("revenue_model", "")}
Stage: {idea.get("stage", "")}
Budget: {budget}
Time Horizon (days): {time_horizon}
"""

        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4
        )

        content = response.choices[0].message.content.strip()

        if self.debug:
            print("FinancialEvaluator RAW:", content)

        return self._parse_json(content)
