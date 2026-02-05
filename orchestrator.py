print("Orchestrator file is running...")

from Agents.trend_scanner import TrendScannerAgent
from Agents.idea_generator import IdeaGeneratorAgent
from Agents.financial_evaluator import FinancialEvaluatorAgent
from Agents.ethics_evaluator import EthicsEvaluatorAgent
from Agents.impact_evaluator import ImpactEvaluatorAgent
from Agents.selector import IdeaSelectorAgent

import json
import os
import time
import uuid
import argparse


# ---------------------------
# Parse CLI arguments
# ---------------------------
parser = argparse.ArgumentParser()
parser.add_argument("--invest", type=int, help="Investment amount for venture")
parser.add_argument("--goal", type=str, help="Optional goal or theme")
args = parser.parse_args()

investment = args.invest if args.invest else 100
goal = args.goal if args.goal else "general"


# ---------------------------
# Orchestrator Class
# ---------------------------
class Orchestrator:
    def __init__(self):
        self.a1 = TrendScannerAgent()
        self.a2 = IdeaGeneratorAgent()
        self.b1 = FinancialEvaluatorAgent()
        self.b2 = EthicsEvaluatorAgent()
        self.b3 = ImpactEvaluatorAgent()
        self.c1 = IdeaSelectorAgent()

    def run_session(self, budget, goal):
        constraints = {"ethics": ["no crypto"], "time_horizon_days": 14}

        # A-Stage
        a1_out = self.a1.run({"budget": budget, "goal": goal, "constraints": constraints})
        a2_out = self.a2.run({"budget": budget, "constraints": constraints})

        # B-Stage
        b1_out = self.b1.run({"ideas": a2_out["ideas"]})
        b2_out = self.b2.run({"ideas": a2_out["ideas"], "constraints": constraints})
        b3_out = self.b3.run({"ideas": a2_out["ideas"]})

        # C-Stage
        c1_out = self.c1.run({
            "ideas": a2_out["ideas"],
            "financial_evaluations": b1_out["financial_evaluations"],
            "ethics_evaluations": b2_out["ethics_evaluations"],
            "impact_evaluations": b3_out["impact_evaluations"]
        })

        return {
            "input_budget": budget,
            "input_goal": goal,
            "trend_scan": a1_out,
            "ideas": a2_out,
            "financial": b1_out,
            "ethics": b2_out,
            "impact": b3_out,
            "selection": c1_out
        }


# ---------------------------
# Save Run to History
# ---------------------------
def save_run(result):
    path = os.path.join("data", "history.json")

    with open(path, "r") as f:
        data = json.load(f)

    result["run_id"] = str(uuid.uuid4())
    result["timestamp"] = time.strftime("%Y-%m-%d %H:%M:%S")

    data["runs"].append(result)

    with open(path, "w") as f:
        json.dump(data, f, indent=4)


# ---------------------------
# Execute Orchestrator
# ---------------------------
if __name__ == "__main__":
    print("Orchestrator file is running...")

    orch = Orchestrator()
    result = orch.run_session(
        budget=investment,
        goal=goal
    )


print("\n=== TOP RECOMMENDATIONS ===")

top_items = result["selection"].get("top_recommendations")

if not top_items:
    selected = result["selection"]["selected_idea"]
    print(f"\nBest Idea: {selected['title']}")
    print(f"Budget Required: ${selected['budget_required']}")
    print(f"Target User: {selected['target_user']}")
    print(f"Description: {selected['description']}")
else:
    for idx, item in enumerate(top_items, start=1):
        idea = item["idea"]
        print(f"\n#{idx}: {idea['title']}")
        print(f"   Budget Required: ${idea['budget_required']}")
        print(f"   Target User: {idea['target_user']}")
        print(f"   Description: {idea['description']}")
        print(f"   Combined Score: {round(item['combined_score'], 2)}")



    save_run(result)
