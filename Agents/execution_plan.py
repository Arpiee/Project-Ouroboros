import os
import json
from groq import Groq


class ExecutionPlanAgent:
    def __init__(self, debug: bool = False):
        self.debug = debug
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    def _parse_json(self, content: str):
        """Attempts strict JSON parsing, then repairs if needed."""
        try:
            return json.loads(content)
        except Exception:
            try:
                start = content.index("[")
                end = content.rindex("]") + 1
                return json.loads(content[start:end])
            except Exception:
                return [
                    {"week": 1, "tasks": ["Define problem and customer clearly.", "Talk to 5 potential users."]},
                    {"week": 2, "tasks": ["Sketch MVP scope.", "Map competitors and differentiation."]},
                    {"week": 3, "tasks": ["Build or fake the MVP.", "Run first user tests."]},
                    {"week": 4, "tasks": ["Refine based on feedback.", "Decide next experiment or pivot."]},
                ]

    def run(self, payload: dict):
        idea = payload.get("idea", {})
        stage = payload.get("stage", idea.get("stage", "Idea only"))
        time_horizon = payload.get("time_horizon", 30)

        prompt = f"""
You are a startup execution coach.

Create a 30-day execution roadmap for this idea, tailored to its stage.

Return ONLY valid JSON. No explanations, no markdown, no text outside the JSON.

Use this exact structure:

[
  {{
    "week": 1,
    "tasks": ["task 1", "task 2", "task 3"]
  }}
]

Idea: {idea.get("idea_description", "")}
Problem: {idea.get("problem", "")}
Customer: {idea.get("target_customer", "")}
Stage: {stage}
Time Horizon (days): {time_horizon}
"""

        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4
        )

        content = response.choices[0].message.content.strip()

        if self.debug:
            print("ExecutionPlan RAW:", content)

        return self._parse_json(content)
