from .base import BaseAgent

class TrendScannerAgent(BaseAgent):
    def __init__(self):
        super().__init__("A1_TrendScanner", "Trend Scanner")

    def run(self, input_data):
        budget = input_data.get("budget")
        constraints = input_data.get("constraints", {})

        return {
            "opportunity_themes": [
                "AI tools for students",
                "Micro digital products for freelancers",
                "Automation for small online sellers"
            ]
        }
