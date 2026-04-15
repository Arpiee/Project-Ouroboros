import os
from groq import Groq

# Import updated hybrid agents
from agents.trend_scanner import TrendScannerAgent
from agents.financial_evaluator import FinancialEvaluatorAgent
from agents.impact_evaluator import ImpactEvaluatorAgent
from agents.ethics_evaluator import EthicsEvaluatorAgent
from agents.selector import SelectorAgent
from agents.execution_plan import ExecutionPlanAgent
from agents.idea_generator import IdeaGeneratorAgent


class Orchestrator:
    """
    Hybrid orchestrator that supports:
    - Idea Validator Mode (new)
    - Idea Generator Mode (old)
    """

    def __init__(self, debug: bool = False):
        self.debug = debug
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))

        # Initialize all hybrid agents
        self.trend_agent = TrendScannerAgent(debug=debug)
        self.financial_agent = FinancialEvaluatorAgent(debug=debug)
        self.impact_agent = ImpactEvaluatorAgent(debug=debug)
        self.ethics_agent = EthicsEvaluatorAgent(debug=debug)
        self.selector_agent = SelectorAgent(debug=debug)
        self.execution_plan_agent = ExecutionPlanAgent(debug=debug)
        self.idea_generator_agent = IdeaGeneratorAgent(debug=debug)

    # ---------------------------------------------------------
    # NEW MODE: IDEA VALIDATION (client pivot)
    # ---------------------------------------------------------
    def validate_idea(
        self,
        idea_description: str,
        target_customer: str,
        problem: str,
        competitors: str,
        revenue_model: str,
        stage: str,
    ):
        # Build idea payload
        idea_payload = {
            "idea_description": idea_description,
            "target_customer": target_customer,
            "problem": problem,
            "competitors": competitors,
            "revenue_model": revenue_model,
            "stage": stage,
        }

        # Run all agents
        trends_out = self.trend_agent.run(idea_payload)
        financial_out = self.financial_agent.run({"idea": idea_payload})
        impact_out = self.impact_agent.run({"idea": idea_payload})
        ethics_out = self.ethics_agent.run({"idea": idea_payload})

        # Selector combines scores
        selector_out = self.selector_agent.run({
            "trends": trends_out,
            "financial": financial_out,
            "impact": impact_out,
            "ethics": ethics_out,
        })

        # Execution plan based on stage
        execution_plan = self.execution_plan_agent.run({
            "idea": idea_payload,
            "stage": stage
        })

        # Final result
        result = {
            "idea": idea_payload,
            "trends": trends_out,
            "financial": financial_out,
            "impact": impact_out,
            "ethics": ethics_out,
            "scores": selector_out["scores"],
            "summary": selector_out["summary"],
            "strengths": selector_out["strengths"],
            "weaknesses": selector_out["weaknesses"],
            "next_steps": execution_plan,
        }

        if self.debug:
            result["debug"] = {
                "raw_trends": trends_out,
                "raw_financial": financial_out,
                "raw_impact": impact_out,
                "raw_ethics": ethics_out,
            }

        return result

    # ---------------------------------------------------------
    # OLD MODE: IDEA GENERATOR (your original system)
    # ---------------------------------------------------------
    def run_session(self, budget, goal, constraints, time_horizon):
        """
        Old idea generator flow preserved for backward compatibility.
        """

        # 1. Scan trends
        trends = self.trend_agent.run({
            "goal": goal,
            "constraints": constraints
        })

        # 2. Generate deterministic ideas
        ideas = self.idea_generator_agent.run({
            "budget": budget,
            "goal": goal,
            "constraints": constraints,
            "trends": trends
        })

        # 3. Score each idea financially
        financial_scores = {}
        for idea in ideas:
            out = self.financial_agent.run({
                "idea": idea,
                "budget": budget,
                "time_horizon": time_horizon
            })
            financial_scores[idea["title"]] = out.get("financial_score", 0)

        # 4. Score each idea for impact
        impact_scores = {}
        for idea in ideas:
            out = self.impact_agent.run({"idea": idea})
            impact_scores[idea["title"]] = out.get("impact_score", 0)

        # 5. Score each idea for ethics
        ethics_scores = {}
        for idea in ideas:
            out = self.ethics_agent.run({"idea": idea})
            ethics_scores[idea["title"]] = out.get("risk_score", 0)

        # 6. Rank ideas
        selector_out = self.selector_agent.run({
            "ideas": ideas,
            "financial_scores": financial_scores,
            "impact_scores": impact_scores,
            "ethics_scores": ethics_scores,
        })

        # 7. Execution plan for top idea
        top_idea = selector_out["top_recommendations"][0]["idea"]
        execution_plan = self.execution_plan_agent.run({
            "idea": top_idea,
            "time_horizon": time_horizon
        })

        return {
            "ideas": ideas,
            "trends": trends,
            "financial_scores": financial_scores,
            "impact_scores": impact_scores,
            "ethics_scores": ethics_scores,
            "top_recommendations": selector_out["top_recommendations"],
            "execution_plan": execution_plan,
        }
