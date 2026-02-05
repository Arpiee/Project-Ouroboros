from .base import BaseAgent

class IdeaSelectorAgent(BaseAgent):
    def __init__(self):
        super().__init__("C1_IdeaSelector", "Idea Selector")

    def run(self, input_data):
        ideas = input_data["ideas"]
        financial = input_data["financial_evaluations"]
        ethics = input_data["ethics_evaluations"]
        impact = input_data["impact_evaluations"]

        ranked = []

        for idea in ideas:
            idea_id = idea["id"]

            fin = next(f for f in financial if f["idea_id"] == idea_id)
            imp = next(i for i in impact if i["idea_id"] == idea_id)

            combined_score = (
                fin["reward_score"] * 0.4 +
                (1 - fin["risk_score"]) * 0.2 +
                imp["impact_score"] * 0.4
            )

            ranked.append({
                "idea": idea,
                "financial": fin,
                "impact": imp,
                "combined_score": combined_score
            })

        ranked_sorted = sorted(ranked, key=lambda x: x["combined_score"], reverse=True)

        return {
            "top_recommendations": ranked_sorted[:3],
            "selected_idea": ranked_sorted[0]["idea"]
        }
