# Project-Ouroboros

# 🐍 Ouroboros Venture Advisor  
A Streamlit‑powered AI tool that helps users generate, evaluate, and refine business ideas using a multi‑agent intelligence system.

## 🚀 Features

### 🔐 User Authentication  
- Secure signup and login  
- Password hashing  
- Local JSON‑based user storage  

### 🧠 Multi‑Agent Idea Evaluation  
The system uses several specialized agents to analyze each idea:

| Agent | Purpose |
|-------|---------|
| **Idea Generator** | Produces business ideas based on user inputs |
| **Trend Scanner** | Identifies market trends and opportunities |
| **Financial Evaluator** | Estimates cost, ROI, and financial feasibility |
| **Impact Evaluator** | Assesses social, environmental, and market impact |
| **Ethics Evaluator** | Flags ethical risks and compliance issues |
| **Execution Planner** | Generates a step‑by‑step execution roadmap |
| **Selector Agent** | Ranks and recommends the best ideas |

## 🖥️ Tech Stack

- Python 3.10+
- Streamlit
- Custom Multi‑Agent Architecture
- dotenv for environment variables
- JSON for user storage

## 📦 Installation

```bash
git clone https://github.com/Arpiee/Project-Ouroboros.git
cd Project-Ouroboros
pip install -r requirements.txt
Create a .env file: (OPENAI_API_KEY=your_key_here)

▶️ Running the App (streamlit run ui.py)
