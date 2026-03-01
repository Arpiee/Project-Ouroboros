import streamlit as st
from orchestrator import Orchestrator
import pandas as pd
import altair as alt
from groq import Groq
import os
import json

# Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.set_page_config(page_title="Ouroboros Venture Advisor", layout="wide")

# ---------------- THEME-AWARE COLORS ----------------
theme = st.get_option("theme.base")

if theme == "dark":
    CARD_BG = "#1e1e1e"
    CARD_BORDER = "#333333"
    CARD_TEXT = "#f5f5f5"
    BANNER_BG = "#2a2a2a"
else:
    CARD_BG = "#ffffff"
    CARD_BORDER = "#e0e0e0"
    CARD_TEXT = "#000000"
    BANNER_BG = "#f0f2f6"

# ---------------- SIDEBAR ----------------
st.sidebar.title("⚙️ Input Parameters")

investment = st.sidebar.number_input(
    "Investment Amount ($)", min_value=50, max_value=100000, value=300
)

goal = st.sidebar.text_input(
    "Optional Goal (e.g., AI tools, student tools)", value="general"
)

industry = st.sidebar.selectbox(
    "Industry Preference", ["Any", "AI", "Education", "Finance", "Healthcare", "Retail"]
)
constraints = {"industry": industry}

time_horizon = st.sidebar.slider(
    "Time Horizon (days)", min_value=7, max_value=60, value=30
)

st.sidebar.markdown("---")
run_button = st.sidebar.button("🚀 Generate Ideas")

# ---------------- MAIN TITLE ----------------
st.title("🚀 Ouroboros Venture Advisor (Groq-Powered)")
st.markdown(
    "Turn your budget into **actionable, AI‑generated venture ideas**, "
    "with scoring, comparison, and execution plans."
)

result = None

# ---------------- RUN ORCHESTRATOR WITH ANIMATION ----------------
if run_button:
    status = st.empty()
    status.markdown("🧠 Scanning trends...")

    with st.spinner("Thinking through trends, ideas, and plans…"):
        orch = Orchestrator()
        result = orch.run_session(
            budget=investment,
            goal=goal,
            constraints=constraints,
            time_horizon=time_horizon
        )

    status.markdown("✅ Ideas generated and evaluated.")
    st.success("Ideas generated successfully!")

# ---------------- DISPLAY RESULTS ----------------
if result:

    # ---------- SUMMARY BANNER ----------
    top = result["top_recommendations"][0]["idea"]
    score = result["top_recommendations"][0]["combined_score"]

    st.markdown(
        f"""
        <div style="
            padding: 20px;
            border-radius: 10px;
            background-color: {BANNER_BG};
            margin-bottom: 20px;
            border: 1px solid {CARD_BORDER};
            color: {CARD_TEXT};
        ">
            <h2 style="margin: 0; color: {CARD_TEXT};">🏆 Top Idea: {top['title']}</h2>
            <p>{top['description']}</p>
            <p><b>Score:</b> {score:.2f}</p>
            <p><b>Budget Required:</b> ${top['budget_required']}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ---------- MARKET TRENDS ----------
    with st.expander("📈 Market Trends", expanded=True):
        for t in result["trends"]:
            st.markdown(f"- **{t['trend']}** — {t['description']}")

    # ---------- GENERATED IDEAS ----------
    with st.expander("💡 Generated Ideas", expanded=True):
        for idea in result["ideas"]:
            st.markdown(
                f"""
                <div style="
                    padding: 15px;
                    border-radius: 8px;
                    border: 1px solid {CARD_BORDER};
                    margin-bottom: 15px;
                    background-color: {CARD_BG};
                    color: {CARD_TEXT};
                ">
                    <h3 style="margin-top: 0; color: {CARD_TEXT};">{idea['title']}</h3>
                    <p>{idea['description']}</p>
                    <p><b>Budget Required:</b> ${idea['budget_required']}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

    # ---------- COMPARISON DASHBOARD ----------
    with st.expander("📊 Idea Comparison Dashboard", expanded=True):

        ideas = [i["title"] for i in result["ideas"]]

        financial_scores = result.get("financial_scores_by_title", {})
        impact_scores = result.get("impact_scores_by_title", {})
        ethics_scores = result.get("ethics_scores_by_title", {})

        data = []
        for title in ideas:
            data.append({
                "Idea": title,
                "Financial Score": financial_scores.get(title, 0),
                "Impact Score": impact_scores.get(title, 0),
                "Ethics Score": ethics_scores.get(title, 0),
            })

        df_scores = pd.DataFrame(data)
        st.dataframe(df_scores, use_container_width=True)

        # ----- BAR CHART -----
        st.markdown("#### Multi‑Metric Score Chart")
        st.bar_chart(df_scores.set_index("Idea"))

        # ----- RADAR CHART -----
        long_df = df_scores.melt(id_vars="Idea", var_name="Metric", value_name="Score")
        radar = (
            alt.Chart(long_df)
            .mark_line(point=True)
            .encode(
                theta="Metric:N",
                radius="Score:Q",
                color="Idea:N"
            )
            .properties(height=400)
        )
        st.markdown("#### Radar View of Scores")
        st.altair_chart(radar, use_container_width=True)

        # ----- ROI PROJECTION -----
        st.markdown("#### ROI Projection (Simulated)")
        roi_rows = []
        for _, row in df_scores.iterrows():
            base = row["Financial Score"] / 100
            for month in range(1, 13):
                roi_rows.append({
                    "Idea": row["Idea"],
                    "Month": month,
                    "Projected ROI": base * month
                })
        roi_df = pd.DataFrame(roi_rows)
        roi_chart = (
            alt.Chart(roi_df)
            .mark_line()
            .encode(
                x="Month:Q",
                y="Projected ROI:Q",
                color="Idea:N"
            )
            .properties(height=300)
        )
        st.altair_chart(roi_chart, use_container_width=True)

        # ----- RISK VS REWARD -----
        st.markdown("#### Risk vs Reward")
        rr_df = pd.DataFrame({
            "Idea": df_scores["Idea"],
            "Reward": df_scores["Financial Score"],
            "Risk": 100 - df_scores["Ethics Score"]
        })
        rr_chart = (
            alt.Chart(rr_df)
            .mark_circle(size=120)
            .encode(
                x="Risk:Q",
                y="Reward:Q",
                color="Idea:N",
                tooltip=["Idea", "Risk", "Reward"]
            )
            .properties(height=300)
        )
        st.altair_chart(rr_chart, use_container_width=True)

    # ---------- TOP RECOMMENDATIONS ----------
    with st.expander("🏆 Top Recommendations", expanded=True):
        for rec in result["top_recommendations"]:
            idea = rec["idea"]
            st.markdown(
                f"""
                <div style="
                    padding: 15px;
                    border-radius: 8px;
                    border: 1px solid {CARD_BORDER};
                    margin-bottom: 15px;
                    background-color: {CARD_BG};
                    color: {CARD_TEXT};
                ">
                    <h3 style="margin-top: 0; color: {CARD_TEXT};">{idea['title']}</h3>
                    <p>{idea['description']}</p>
                    <p><b>Combined Score:</b> {rec['combined_score']:.2f}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

    # ---------- PORTFOLIO SIMULATOR ----------
    with st.expander("💼 Portfolio Simulator (Virtual Only)", expanded=False):
        st.write("This is a simulation only.")

        top_ideas = [rec["idea"]["title"] for rec in result["top_recommendations"]]
        allocations = {}

        if top_ideas:
            mode = st.radio("Allocation Mode", ["Equal Allocation", "Custom Allocation"], horizontal=True)

            if mode == "Equal Allocation":
                per = investment / len(top_ideas)
                allocations = {title: per for title in top_ideas}
                st.write(f"Each idea receives **${per:.2f}**.")
            else:
                remaining = investment
                for title in top_ideas:
                    val = st.number_input(
                        f"Allocate to {title}",
                        min_value=0.0,
                        max_value=float(remaining),
                        value=0.0,
                        key=f"alloc_{title}"
                    )
                    allocations[title] = val
                    remaining = investment - sum(allocations.values())

                st.write(f"Remaining unallocated: **${remaining:.2f}**")

            # Pie chart
            alloc_df = pd.DataFrame(
                [{"Idea": k, "Amount": v} for k, v in allocations.items() if v > 0]
            )
            if not alloc_df.empty:
                st.markdown("#### Allocation Pie Chart")
                pie = alt.Chart(alloc_df).mark_arc().encode(
                    theta="Amount:Q",
                    color="Idea:N"
                )
                st.altair_chart(pie, use_container_width=True)

            # Diversification score
            funded = [k for k, v in allocations.items() if v > 0]
            diversification = len(funded) / len(top_ideas) * 100 if funded else 0
            st.write(f"**Diversification score:** {diversification:.1f} / 100")

            # Risk buckets
            risk_rows = []
            for title in funded:
                ethics = ethics_scores.get(title, 50)

                if ethics >= 70:
                    bucket = "Low"
                elif ethics >= 40:
                    bucket = "Medium"
                else:
                    bucket = "High"

                risk_rows.append({"Idea": title, "Risk Bucket": bucket})

            if risk_rows:
                st.write("**Risk buckets:**")
                st.dataframe(pd.DataFrame(risk_rows), use_container_width=True)

    # ---------- EXECUTION PLAN ----------
    with st.expander("🗂 Execution Plan for Top Idea", expanded=True):
        for step in result["execution_plan"]:
            st.markdown(
                f"""
                <div style="
                    padding: 10px;
                    border-radius: 6px;
                    border: 1px solid {CARD_BORDER};
                    margin-bottom: 8px;
                    background-color: {CARD_BG};
                    color: {CARD_TEXT};
                ">
                    <b>Day {step['day']}</b> — {step['task']}
                </div>
                """,
                unsafe_allow_html=True
            )

    # ---------- EXPORT FEATURES ----------
    st.markdown("### 📄 Export Data")

    ideas_df = pd.DataFrame(result["ideas"])
    scores_df = pd.DataFrame({
        "Idea": list(financial_scores.keys()),
        "Financial Score": list(financial_scores.values()),
        "Impact Score": list(impact_scores.values()),
        "Ethics Score": list(ethics_scores.values()),
    })
    exec_df = pd.DataFrame(result["execution_plan"])

    st.download_button(
        "⬇️ Download Ideas (CSV)",
        data=ideas_df.to_csv(index=False),
        file_name="ideas.csv",
        mime="text/csv",
    )

    st.download_button(
        "⬇️ Download Scores (CSV)",
        data=scores_df.to_csv(index=False),
        file_name="scores.csv",
        mime="text/csv",
    )

    st.download_button(
        "⬇️ Download Execution Plan (CSV)",
        data=exec_df.to_csv(index=False),
        file_name="execution_plan.csv",
        mime="text/csv",
    )

    html_report = f"""
    <h1>Ouroboros Venture Advisor Report</h1>
    <h2>Top Idea: {top['title']}</h2>
    <p>{top['description']}</p>
    <p><b>Score:</b> {score:.2f}</p>
    <p><b>Budget Required:</b> ${top['budget_required']}</p>
    <hr>
    <h2>Ideas</h2>
    {ideas_df.to_html(index=False)}
    <hr>
    <h2>Scores</h2>
    {scores_df.to_html(index=False)}
    <hr>
    <h2>Execution Plan</h2>
    {exec_df.to_html(index=False)}
    """

    st.download_button(
        "⬇️ Download Report (HTML)",
        data=html_report,
        file_name="venture_report.html",
        mime="text/html",
    )

    # ---------- GROQ CHATBOT ASSISTANT ----------
    with st.expander("🧠 Assistant (Chatbot)", expanded=False):
        st.markdown(
            "Ask questions about the ideas, scores, and plan. "
            "This AI assistant does **not** provide financial advice."
        )

        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        # Show full chat history
        for role, msg in st.session_state.chat_history:
            if role == "user":
                st.markdown(f"**You:** {msg}")
            else:
                st.markdown(f"**Assistant:** {msg}")

        user_q = st.text_input("Your question:", key="assistant_input")

        if st.button("Ask", key="assistant_button") and user_q:
            st.session_state.chat_history.append(("user", user_q))

            context = {
                "top_idea": top,
                "scores": {
                    "financial": financial_scores,
                    "impact": impact_scores,
                    "ethics": ethics_scores,
                },
                "ideas": result["ideas"],
                "execution_plan": result["execution_plan"],
            }

            messages = [
                {
                    "role": "system",
                    "content": (
                        "You are an analytical assistant for a venture idea tool. "
                        "Explain ideas, scores, and plans clearly. "
                        "Do NOT give real financial, legal, or investment advice."
                    ),
                },
                {
                    "role": "user",
                    "content": "Here is the current session context:\n" + json.dumps(context, indent=2),
                },
            ]

            # Add last few messages
            for role, msg in st.session_state.chat_history[-6:]:
                messages.append({"role": role, "content": msg})

            messages.append({"role": "user", "content": user_q})

            with st.spinner("Thinking..."):
                resp = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=messages,
                    temperature=0.4,
                )
                answer = resp.choices[0].message.content.strip()

            st.session_state.chat_history.append(("assistant", answer))

else:
    st.info("Set your parameters in the sidebar and click **Generate Ideas** to begin.")
