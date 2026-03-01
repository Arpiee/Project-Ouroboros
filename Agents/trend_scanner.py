from .base import BaseAgent
from groq import Groq
import os
import json

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

class TrendScannerAgent(BaseAgent):
    def __init__(self):
        super().__init__("A1_TrendScanner", "Trend Scanner")

    def run(self, input_data):
        goal = input_data.get("goal", "general")

        prompt = f"""
        Identify the top 10 trending business opportunities related to: {goal}.
        Return ONLY JSON:

        [
          {{
            "trend": "AI automation",
            "description": "Businesses are adopting AI tools to automate workflows."
          }}
        ]
        """

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5
        )

        raw = response.choices[0].message.content
        return {"trends": self._safe_parse(raw)}

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
