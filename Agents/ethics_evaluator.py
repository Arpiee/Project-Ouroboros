from .base import BaseAgent

class EthicsEvaluatorAgent(BaseAgent):
    def __init__(self):
        super().__init__("B2_EthicsEvaluator", "Ethics Evaluator")

    def run(self, input_data):
        ideas = input_data.get("ideas", [])
        constraints = input_data.get("constraints", {})

        evaluations = []
        for idea in ideas:
            evaluations.append({
                "idea_id": idea["id"],
                "ethical_score": 0.9,
                "flags": [],
                "comments": "No ethical issues detected."
            })

        return {"ethics_evaluations": evaluations}
