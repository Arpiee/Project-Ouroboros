from .base import BaseAgent

class FinancialEvaluatorAgent(BaseAgent):
    def __init__(self):
        super().__init__("B1_FinancialEvaluator", "Financial Evaluator")

    def run(self, input_data):
        ideas = input_data.get("ideas", [])
        evaluations = []

        for idea in ideas:
            evaluations.append({
                "idea_id": idea["id"],
                "risk_score": 0.4,
                "reward_score": 0.7,
                "difficulty": 0.5,
                "expected_roi": 0.6,
                "comments": "Placeholder financial evaluation."
            })

        return {"financial_evaluations": evaluations}
