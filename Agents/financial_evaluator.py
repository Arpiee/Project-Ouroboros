from .base import BaseAgent
from groq import Groq
import os
import json

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

class FinancialEvaluatorAgent(BaseAgent):
    def __init__(self):
        super().__init__("B1_FinancialEvaluator", "Financial Evaluator")

    def run(self, input_data):
        ideas = input_data["ideas"]

        prompt = f"""
        You are a financial analyst.

        Evaluate the financial potential of these ideas:

        {json.dumps(ideas, indent=2)}

        For each idea, score it from 0 to 100 based on:
        - ROI potential
        - Cost efficiency
        - Market demand

        Return ONLY valid JSON in this exact format:

        [
          {{
            "id": "idea_1",
            "score": 85
          }}
        ]
        """

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )

        raw = response.choices[0].message.content
        scores = self._safe_parse(raw)

        # Ensure structure is always a list of {id, score}
        clean = []
        for item in scores:
            if isinstance(item, dict) and "id" in item and "score" in item:
                try:
                    clean.append({"id": str(item["id"]), "score": float(item["score"])})
                except:
                    continue

        return {"financial_scores": clean}

    def _safe_parse(self, text):
        try:
            return json.loads(text)
        except:
            start = text.find("[")
            end = text.rfind("]") + 1
            if start != -1 and end != -1:
                try:
                    return json.loads(text[start:end])
                except:
                    pass
        return []
