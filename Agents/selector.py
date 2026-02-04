from .base import BaseAgent

class IdeaSelectorAgent(BaseAgent):
    def __init__(self):
        super().__init__("C1_IdeaSelector", "Idea Selector")

    def run(self, input_data):
        ideas = input_data.get("ideas", [])
        selected_idea = ideas[0] if ideas else None

        return {
            "selected_idea": selected_idea,
            "reasoning": {
                "summary": "Selected first idea as placeholder.",
                "financial_reason": "Good ROI.",
                "ethical_reason": "No ethical issues.",
                "impact_reason": "Strong impact.",
                "rejected_ideas": [
                    {"idea_id": idea["id"], "reason": "Not selected."}
                    for idea in ideas[1:]
                ]
            }
        }
