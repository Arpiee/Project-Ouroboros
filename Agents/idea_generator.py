from .base import BaseAgent
from groq import Groq
import os
import json

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

class IdeaGeneratorAgent(BaseAgent):
    def __init__(self):
        super().__init__("A2_IdeaGenerator", "AI Idea Generator")

    def run(self, input_data):
        budget = input_data.get("budget", 100)
        goal = input_data.get("goal", "general")

        prompt = f"""
        Generate 20 business ideas under ${budget} in the category: "{goal}".
        Return ONLY JSON in this format:

        [
          {{
            "id": "idea_1",
            "title": "AI Resume Tool",
            "description": "A tool that analyzes resumes using AI.",
            "budget_required": 40,
            "target_user": "Students",
            "time_horizon_days": 14
          }}
        ]
        """

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )

        raw = response.choices[0].message.content
        return {"ideas": self._safe_parse(raw)}

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
