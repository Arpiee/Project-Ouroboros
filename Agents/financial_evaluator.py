from .base import BaseAgent
from groq import Groq
import os
import json

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

class FinancialEvaluatorAgent(BaseAgent):
    def __init__(self):
        super().__init__("B1_FinancialEvaluator", "Financial Evaluator")

    def run(self, input_data):
        # FIX: Accept a single idea instead of a list
        idea = input_data["idea"]

        prompt = f"""
        You are a financial analyst.

        Evaluate the financial potential of the following startup idea:

        {json.dumps(idea, indent=2)}

        Score it from 0 to 100 based on:
        - ROI potential
        - Cost efficiency
        - Market demand

        Return ONLY valid JSON in this exact format:

        {{
            "id": "idea_1",
            "score": 85
        }}
        """

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )

        raw = response.choices[0].message.content
        parsed = self._safe_parse(raw)

        # Ensure valid structure
        if isinstance(parsed, dict) and "id" in parsed and "score" in parsed:
            return {
                "id": str(parsed["id"]),
                "score": float(parsed["score"])
            }

        # Fallback if model returns weird output
        return {
            "id": str(idea["id"]),
            "score": 50.0
        }

    def _safe_parse(self, text):
        try:
            return json.loads(text)
        except:
            # Try to extract JSON object
            start = text.find("{")
            end = text.rfind("}") + 1
            if start != -1 and end != -1:
                try:
                    return json.loads(text[start:end])
                except:
                    pass
        return {}
