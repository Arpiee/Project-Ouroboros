import streamlit as st
from orchestrator import Orchestrator
from auth import signup, login
import pandas as pd
import altair as alt
from groq import Groq
import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

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

# ---------------- AUTHENTICATION ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:

    st.title("🔐 Welcome to Ouroboros Venture Advisor")

    tab1, tab2 = st.tabs(["Login", "Signup"])

    with tab1:
        st.subheader("Login")
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")
        if st.button("Login"):
            ok, msg = login(username, password)
            if ok:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("Login successful! Redirecting...")
                st.rerun()
            else:
                st.error(msg)

    with tab2:
        st.subheader("Signup")
        new_user = st.text_input("Choose a username", key="signup_user")
        new_pass = st.text_input("Choose a password", type="password", key="signup_pass")
        if st.button("Create Account"):
            ok, msg = signup(new_user, new_pass)
            if ok:
                st.success(msg)
            else:
                st.error(msg)

    st.stop()

# ---------------- SIDEBAR ----------------
st.sidebar.title(f"Welcome, {st.session_state.username} 👋")

st.sidebar.markdown("---")
if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.experimental_rerun()

st.sidebar.markdown("---")

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

run_button = st.sidebar.button("🚀 Generate Ideas")

# ---------------- MAIN TITLE ----------------
st.title("🚀 Ouroboros Venture Advisor (Groq-Powered)")
st.markdown(
    "Turn your budget into **actionable, AI‑generated venture ideas**, "
    "with scoring, comparison, and execution plans."
)

result = None

# ---------------- RUN ORCHESTRATOR ----------------
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

        financial_scores = result["financial_scores_by_title"]
        impact_scores = result["impact_scores_by_title"]
        ethics_scores = result["ethics_scores_by_title"]

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

else:
    st.info("Set your parameters in the sidebar and click **Generate Ideas** to begin.")
