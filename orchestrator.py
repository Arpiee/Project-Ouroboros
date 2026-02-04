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

class Orchestrator:
    def __init__(self):
        self.a1 = TrendScannerAgent()
        self.a2 = IdeaGeneratorAgent()
        self.b1 = FinancialEvaluatorAgent()
        self.b2 = EthicsEvaluatorAgent()
        self.b3 = ImpactEvaluatorAgent()
        self.c1 = IdeaSelectorAgent()

    def run_session(self, budget, constraints):
        a1_out = self.a1.run({"budget": budget, "constraints": constraints})
        a2_out = self.a2.run({"budget": budget, "constraints": constraints})
        b1_out = self.b1.run({"ideas": a2_out["ideas"]})
        b2_out = self.b2.run({"ideas": a2_out["ideas"], "constraints": constraints})
        b3_out = self.b3.run({"ideas": a2_out["ideas"]})

        c1_out = self.c1.run({
            "ideas": a2_out["ideas"],
            "financial_evaluations": b1_out["financial_evaluations"],
            "ethics_evaluations": b2_out["ethics_evaluations"],
            "impact_evaluations": b3_out["impact_evaluations"]
        })

        return {
            "trend_scan": a1_out,
            "ideas": a2_out,
            "financial": b1_out,
            "ethics": b2_out,
            "impact": b3_out,
            "selection": c1_out
        }


def save_run(result):
    path = os.path.join("data", "history.json")

    # Load existing history
    with open(path, "r") as f:
        data = json.load(f)

    # Add metadata
    result["run_id"] = str(uuid.uuid4())
    result["timestamp"] = time.strftime("%Y-%m-%d %H:%M:%S")

    # Append to history
    data["runs"].append(result)

    # Save updated history
    with open(path, "w") as f:
        json.dump(data, f, indent=4)





if __name__ == "__main__":
    print("Orchestrator file is running...")

    orch = Orchestrator()
    result = orch.run_session(
        budget=100,
        constraints={"ethics": ["no crypto"], "time_horizon_days": 14}
    )

    from pprint import pprint
    pprint(result)

    save_run(result)

