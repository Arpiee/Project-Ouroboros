from .base import BaseAgent

class ImpactEvaluatorAgent(BaseAgent):
    def __init__(self):
        super().__init__("B3_ImpactEvaluator", "Impact Evaluator")

    def run(self, input_data):
        ideas = input_data.get("ideas", [])
        evaluations = []

        for idea in ideas:
            evaluations.append({
                "idea_id": idea["id"],
                "impact_score": 0.7,
                "novelty_score": 0.6,
                "overall_recommendation": "strong"
            })

        return {"impact_evaluations": evaluations}
