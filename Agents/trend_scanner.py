from .base import BaseAgent

class TrendScannerAgent(BaseAgent):
    def __init__(self):
        super().__init__("A1_TrendScanner", "Trend Scanner")

    def run(self, input_data):
        """
        Trend scanner that reacts to:
        - Customer investment amount
        - Customer goal (optional)
        - Constraints (optional)
        """

        budget = input_data.get("budget", 100)
        goal = input_data.get("goal", "general")
        constraints = input_data.get("constraints", {})

        # Budget-based themes
        if budget < 100:
            themes = [
                "micro digital products",
                "low-cost AI tools",
                "simple automations",
                "printable templates",
                "low-budget student tools"
            ]
        elif budget < 500:
            themes = [
                "AI automations",
                "digital services",
                "content products",
                "template businesses",
                "resume/portfolio tools",
                "freelancer productivity tools"
            ]
        else:
            themes = [
                "software tools",
                "subscription products",
                "AI SaaS",
                "automation platforms",
                "AI-powered marketplaces",
                "scalable digital products"
            ]

        # Add customer goal if provided
        if goal != "general":
            themes.append(goal)

        # Apply constraints (optional)
        if constraints.get("no_ai"):
            themes = [t for t in themes if "AI" not in t]

        return {
            "input_budget": budget,
            "input_goal": goal,
            "constraints": constraints,
            "opportunity_themes": themes
        }
