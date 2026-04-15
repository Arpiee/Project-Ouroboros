import os
import json
from groq import Groq


class SelectorAgent:
    def __init__(self, debug: bool = False):
        self.debug = debug
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    def _parse_json(self, content: str, fallback: dict):
        try:
            return json.loads(content)
        except Exception:
            try:
                start = content.index("{")
                end = content.rindex("}") + 1
                return json.loads(content[start:end])
            except Exception:
                return fallback

    def run(self, payload: dict):
        if "trends" in payload and "financial" in payload:
            return self._run_validation_mode(payload)
        else:
            return self._run_generator_mode(payload)

    # ---------------------------------------------------------
    # VALIDATION MODE
    # ---------------------------------------------------------
    def _run_validation_mode(self, payload: dict):
        trends = payload["trends"]
        financial = payload["financial"]
        impact = payload["impact"]
        ethics = payload["ethics"]

        prompt = f"""
You are a startup evaluator.

You receive four analyses of the same idea:
- Trends: {trends}
- Financial: {financial}
- Impact: {impact}
- Ethics/Risk: {ethics}

Combine them into a single verdict.

Return ONLY valid JSON with this structure and nothing else:

{{
  "scores": {{
    "overall_viability": 0,
    "market_demand": 0,
    "feasibility": 0,
    "impact": 0,
    "risk": 0,
    "recommendation": "GO"
  }},
  "summary": "2-3 sentence explanation",
  "strengths": ["bullet 1", "bullet 2", "bullet 3"],
  "weaknesses": ["bullet 1", "bullet 2", "bullet 3"]
}}
"""

        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )

        content = response.choices[0].message.content.strip()

        if self.debug:
            print("Selector VALIDATION RAW:", content)

        fallback = {
            "scores": {
                "overall_viability": 50,
                "market_demand": 50,
                "feasibility": 50,
                "impact": 50,
                "risk": 50,
                "recommendation": "PROCEED WITH CAUTION"
            },
            "summary": "Selector failed to parse JSON; using neutral fallback.",
            "strengths": ["Fallback strengths placeholder."],
            "weaknesses": ["Fallback weaknesses placeholder."]
        }

        return self._parse_json(content, fallback)

    # ---------------------------------------------------------
    # GENERATOR MODE
    # ---------------------------------------------------------
    def _run_generator_mode(self, payload: dict):
        ideas = payload["ideas"]
        financial_scores = payload["financial_scores"]
        impact_scores = payload["impact_scores"]
        ethics_scores = payload["ethics_scores"]

        prompt = f"""
You are ranking startup ideas.

You receive:
- ideas: {ideas}
- financial_scores: {financial_scores}
- impact_scores: {impact_scores}
- ethics_scores (risk, higher = more risk): {ethics_scores}

Rank the ideas and compute a combined score.

Return ONLY valid JSON with this structure and nothing else:

{{
  "top_recommendations": [
    {{
      "idea": {{}},
      "combined_score": 0,
      "reason": "short text"
    }}
  ]
}}
"""

        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",   # FIXED HERE
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )

        content = response.choices[0].message.content.strip()

        if self.debug:
            print("Selector GENERATOR RAW:", content)

        # Fallback deterministic ranking
        fallback = None
        try:
            scored = []
            for idea in ideas:
                title = idea["title"]
                score = (
                    financial_scores.get(title, 0)
                    + impact_scores.get(title, 0)
                    - ethics_scores.get(title, 0)
                )
                scored.append((score, idea))

            scored.sort(reverse=True, key=lambda x: x[0])
            top = scored[0] if scored else (0, ideas[0] if ideas else {})

            fallback = {
                "top_recommendations": [
                    {
                        "idea": top[1],
                        "combined_score": top[0],
                        "reason": "Fallback ranking based on simple score."
                    }
                ]
            }
        except Exception:
            fallback = {"top_recommendations": []}

        return self._parse_json(content, fallback)
