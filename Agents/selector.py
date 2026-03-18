from .base import BaseAgent

class SelectorAgent(BaseAgent):
    def __init__(self):
        super().__init__("C1_Selector", "Idea Selector")

    def run(self, input_data):
        ideas = input_data["ideas"]
        financial = input_data["financial_scores"]
        impact = input_data["impact_scores"]
        ethics = input_data["ethics_scores"]

        combined = []

        for idea in ideas:
            fid = idea["id"]

            # FIX: All evaluators now return {"id": ..., "score": ...}
            f = next((x["score"] for x in financial if x["id"] == fid), 0)
            i = next((x["score"] for x in impact if x["id"] == fid), 0)
            e = next((x["score"] for x in ethics if x["id"] == fid), 0)

            # You can adjust weights here if needed
            combined_score = (f * 0.5) + (i * 0.3) + ((100 - e) * 0.2)

            combined.append({
                "idea": idea,
                "combined_score": combined_score,
                "financial_score": f,
                "impact_score": i,
                "ethics_score": e
            })

        combined.sort(key=lambda x: x["combined_score"], reverse=True)

        return {"top_recommendations": combined[:10]}
