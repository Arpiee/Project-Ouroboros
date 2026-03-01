from .base import BaseAgent
from groq import Groq
import os
import json

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

class ExecutionPlanAgent(BaseAgent):
    def __init__(self):
        super().__init__("D1_ExecutionPlan", "Execution Plan Generator")

    def run(self, input_data):
        idea = input_data["idea"]
        days = input_data.get("time_horizon_days", 14)

        prompt = f"""
        Create a detailed day-by-day execution plan for this idea:

        Title: {idea['title']}
        Description: {idea['description']}
        Budget Required: {idea['budget_required']}

        Create a {days}-day plan.
        Return ONLY JSON:

        [
          {{
            "day": 1,
            "task": "Research competitors"
          }}
        ]
        """

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )

        raw = response.choices[0].message.content
        return {"execution_plan": self._safe_parse(raw)}

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
