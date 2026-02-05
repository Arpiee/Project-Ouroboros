from .base import BaseAgent

class IdeaGeneratorAgent(BaseAgent):
    def __init__(self):
        super().__init__("A2_IdeaGenerator", "Idea Generator")

    def run(self, input_data):
        budget = input_data.get("budget", 100)

        # Simple idea generation based on budget
        ideas = [
            {
                "id": "idea_1",
                "title": "AI Resume Review Tool",
                "description": "A micro-service that reviews resumes.",
                "budget_required": 40,
                "time_horizon_days": 14,
                "target_user": "Students"
            },
            {
                "id": "idea_2",
                "title": "Notion Templates",
                "description": "Sell productivity templates.",
                "budget_required": 20,
                "time_horizon_days": 10,
                "target_user": "Freelancers"
            },
            {
                "id": "idea_3",
                "title": "Etsy Automation Scripts",
                "description": "Scripts to help Etsy sellers.",
                "budget_required": 60,
                "time_horizon_days": 14,
                "target_user": "Etsy Sellers"
            },
            {
                "id": "idea_4",
                "title": "AI Study Planner",
                "description": "A tool that generates study plans for students.",
                "budget_required": 30,
                "time_horizon_days": 7,
                "target_user": "Students"
            }
        ]

        return {"ideas": ideas}
