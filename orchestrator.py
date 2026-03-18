from Agents.trend_scanner import TrendScannerAgent
from Agents.idea_generator import IdeaGeneratorAgent
from Agents.financial_evaluator import FinancialEvaluatorAgent
from Agents.impact_evaluator import ImpactEvaluatorAgent
from Agents.ethics_evaluator import EthicsEvaluatorAgent
from Agents.selector import SelectorAgent
from Agents.execution_plan import ExecutionPlanAgent


class Orchestrator:
    def __init__(self):
        self.trend_scanner = TrendScannerAgent()
        self.idea_generator = IdeaGeneratorAgent()
        self.financial_evaluator = FinancialEvaluatorAgent()
        self.impact_evaluator = ImpactEvaluatorAgent()
        self.ethics_evaluator = EthicsEvaluatorAgent()
        self.selector = SelectorAgent()
        self.execution_plan = ExecutionPlanAgent()

    def run_session(self, budget, goal, constraints, time_horizon):

        # A1: Trends
        trends_out = self.trend_scanner.run({"goal": goal})

        # A2: Ideas
        ideas_out = self.idea_generator.run({
            "budget": budget,
            "goal": goal,
            "constraints": constraints
        })
        ideas = ideas_out["ideas"]

        # Build id → idea map
        ideas_by_id = {idea["id"]: idea for idea in ideas if "id" in idea}

        # -------------------------------
        # B: SCORE EACH IDEA INDIVIDUALLY
        # -------------------------------

        financial_scores = []
        impact_scores = []
        ethics_scores = []

        for idea in ideas:
            idea_id = idea["id"]

            # Score individually
            fin = self.financial_evaluator.run({"idea": idea})
            imp = self.impact_evaluator.run({"idea": idea})
            eth = self.ethics_evaluator.run({"idea": idea})

            financial_scores.append({"id": idea_id, "score": float(fin["score"])})
            impact_scores.append({"id": idea_id, "score": float(imp["score"])})
            ethics_scores.append({"id": idea_id, "score": float(eth["score"])})

        # Convert to id → score maps
        fin_by_id = {str(item["id"]): item["score"] for item in financial_scores}
        imp_by_id = {str(item["id"]): item["score"] for item in impact_scores}
        eth_by_id = {str(item["id"]): item["score"] for item in ethics_scores}

        # -------------------------------
        # C: SELECTOR
        # -------------------------------
        selector_out = self.selector.run({
            "ideas": ideas,
            "financial_scores": financial_scores,
            "impact_scores": impact_scores,
            "ethics_scores": ethics_scores
        })

        top_idea = selector_out["top_recommendations"][0]["idea"]

        # -------------------------------
        # D: EXECUTION PLAN
        # -------------------------------
        execution_out = self.execution_plan.run({
            "idea": top_idea,
            "time_horizon_days": time_horizon
        })

        # -------------------------------
        # BUILD TITLE-KEYED SCORE MAPS
        # -------------------------------
        fin_by_title = {}
        imp_by_title = {}
        eth_by_title = {}

        for idea in ideas:
            iid = str(idea.get("id", ""))
            title = idea.get("title", iid)

            fin_by_title[title] = fin_by_id.get(iid, 0)
            imp_by_title[title] = imp_by_id.get(iid, 0)
            eth_by_title[title] = eth_by_id.get(iid, 0)

        return {
            "trends": trends_out["trends"],
            "ideas": ideas,
            "financial_scores": financial_scores,
            "impact_scores": impact_scores,
            "ethics_scores": ethics_scores,
            "financial_scores_by_title": fin_by_title,
            "impact_scores_by_title": imp_by_title,
            "ethics_scores_by_title": eth_by_title,
            "top_recommendations": selector_out["top_recommendations"],
            "execution_plan": execution_out["execution_plan"]
        }
