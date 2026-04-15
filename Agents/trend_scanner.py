import os
import json
from groq import Groq


class TrendScannerAgent:
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
                    "trend_score": 50,
                    "trend_fit": "Unclear trend fit",
                    "trend_risks": ["Model returned invalid JSON."],
                    "trend_opportunities": [],
                    "summary": "Trend analysis unavailable due to parsing error."
                }

    def run(self, payload: dict):
        idea = payload.get("idea_description", "") or payload.get("idea", {}).get("idea_description", "")
        problem = payload.get("problem", "") or payload.get("idea", {}).get("problem", "")
        customer = payload.get("target_customer", "") or payload.get("idea", {}).get("target_customer", "")
        competitors = payload.get("competitors", "") or payload.get("idea", {}).get("competitors", "")
        revenue_model = payload.get("revenue_model", "") or payload.get("idea", {}).get("revenue_model", "")
        stage = payload.get("stage", "") or payload.get("idea", {}).get("stage", "")

        prompt = f"""
You are a startup trend analyst.

Analyze the following startup idea against current market and technology trends.

Return ONLY valid JSON. No explanations, no markdown, no text outside the JSON.

Use this exact structure:

{{
  "trend_score": 0,
  "trend_fit": "short text",
  "trend_risks": ["bullet 1", "bullet 2"],
  "trend_opportunities": ["bullet 1", "bullet 2", "bullet 3"],
  "summary": "1-2 sentence summary"
}}

Idea: {idea}
Problem: {problem}
Customer: {customer}
Competitors: {competitors}
Revenue Model: {revenue_model}
Stage: {stage}
"""

        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4
        )

        content = response.choices[0].message.content.strip()

        if self.debug:
            print("TrendScanner RAW:", content)

        return self._parse_json(content)
