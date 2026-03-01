from .base import BaseAgent
from groq import Groq
import os
import json

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

class EthicsEvaluatorAgent(BaseAgent):
    def __init__(self):
        super().__init__("B3_EthicsEvaluator", "Ethics Evaluator")

    def run(self, input_data):
        ideas = input_data["ideas"]

        prompt = f"""
        Evaluate the ethical risks of these ideas:
        {ideas}

        Score each idea from 0–100 (lower = more ethical).
        Return ONLY JSON:

        [
          {{
            "id": "idea_1",
            "ethics_score": 20
          }}
        ]
        """

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )

        raw = response.choices[0].message.content
        return {"ethics_scores": self._safe_parse(raw)}

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
