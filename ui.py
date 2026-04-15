# ui.py
import streamlit as st
from orchestrator import Orchestrator

# ---------------------------------------------------------
# APP CONFIG
# ---------------------------------------------------------
st.set_page_config(
    page_title="Ouroboros Venture Advisor",
    page_icon="🌀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------
# GLOBAL STYLES (FUTURISTIC NEON CYBER-SaaS)
# ---------------------------------------------------------
NEON_CSS = """
<style>
body {
    background: radial-gradient(circle at top, #050816 0, #02010a 40%, #000000 100%) !important;
    color: #f5f5f5 !important;
    font-family: "Inter", system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}
.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #050816 0%, #050816 40%, #020617 100%) !important;
    border-right: 1px solid rgba(148, 163, 184, 0.25);
}
.sidebar-title {
    font-size: 1.2rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #e5e7eb;
}
.sidebar-subtitle {
    font-size: 0.8rem;
    color: #9ca3af;
}
.neon-logo {
    font-size: 1.8rem;
    font-weight: 800;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    background: linear-gradient(90deg, #22d3ee, #a855f7, #f97316);
    -webkit-background-clip: text;
    color: transparent;
}
.glass-panel {
    background: linear-gradient(135deg, rgba(15, 23, 42, 0.85), rgba(15, 23, 42, 0.65));
    border-radius: 18px;
    border: 1px solid rgba(148, 163, 184, 0.35);
    box-shadow:
        0 18px 45px rgba(15, 23, 42, 0.9),
        0 0 0 1px rgba(15, 23, 42, 0.9);
    padding: 1.4rem 1.6rem;
    margin-bottom: 1.2rem;
}
.section-title {
    font-size: 1.1rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #9ca3af;
    margin-bottom: 0.4rem;
}
.section-heading {
    font-size: 1.4rem;
    font-weight: 700;
    color: #e5e7eb;
}
.score-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.25rem 0.7rem;
    border-radius: 999px;
    font-size: 0.8rem;
    font-weight: 600;
    background: radial-gradient(circle at top left, rgba(56, 189, 248, 0.25), rgba(15, 23, 42, 0.9));
    border: 1px solid rgba(56, 189, 248, 0.6);
    color: #e0f2fe;
}
.neon-bar-container {
    width: 100%;
    height: 10px;
    border-radius: 999px;
    background: rgba(15, 23, 42, 0.9);
    overflow: hidden;
    border: 1px solid rgba(31, 41, 55, 0.9);
}
.neon-bar-fill {
    height: 100%;
    border-radius: 999px;
    background: linear-gradient(90deg, #22d3ee, #a855f7, #f97316);
}
.pill {
    display: inline-flex;
    align-items: center;
    padding: 0.2rem 0.7rem;
    border-radius: 999px;
    font-size: 0.78rem;
    border: 1px solid rgba(148, 163, 184, 0.6);
    color: #e5e7eb;
    margin-right: 0.3rem;
    margin-bottom: 0.3rem;
}
.timeline-week {
    border-left: 2px solid rgba(56, 189, 248, 0.7);
    padding-left: 0.9rem;
    margin-bottom: 0.8rem;
}
.timeline-dot {
    width: 10px;
    height: 10px;
    border-radius: 999px;
    background: #22d3ee;
    box-shadow: 0 0 12px rgba(34, 211, 238, 0.9);
    margin-right: 0.4rem;
}
.idea-card {
    background: linear-gradient(135deg, rgba(15, 23, 42, 0.9), rgba(15, 23, 42, 0.7));
    border-radius: 16px;
    border: 1px solid rgba(148, 163, 184, 0.4);
    padding: 1rem 1.1rem;
    margin-bottom: 0.8rem;
}
.footer {
    font-size: 0.75rem;
    color: #6b7280;
    text-align: right;
    margin-top: 1.5rem;
}
</style>
"""
st.markdown(NEON_CSS, unsafe_allow_html=True)

# ---------------------------------------------------------
# ORCHESTRATOR INSTANCE
# ---------------------------------------------------------
@st.cache_resource
def get_orchestrator():
    return Orchestrator(debug=False)


orch = get_orchestrator()

# ---------------------------------------------------------
# SIDEBAR NAVIGATION
# ---------------------------------------------------------
with st.sidebar:
    st.markdown('<div class="sidebar-title">OUROBOROS</div>', unsafe_allow_html=True)
    st.markdown('<div class="neon-logo">Venture Advisor</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-subtitle">AI co-pilot for startup decisions</div>', unsafe_allow_html=True)
    st.markdown("---")

    page = st.radio(
        "Navigation",
        ["Validate Idea", "Generate Ideas", "Compare Ideas"],
        index=0,
    )

    st.markdown("---")
    st.caption("Powered by Groq · llama-3.3-70b-versatile")


# ---------------------------------------------------------
# HELPER: NEON SCORE BAR
# ---------------------------------------------------------
def neon_score_bar(label: str, value: int, invert: bool = False):
    value = max(0, min(100, int(value)))
    display_value = 100 - value if invert else value

    st.markdown(
        f"""
        <div style="margin-bottom:0.35rem; display:flex; justify-content:space-between; align-items:center;">
            <span style="font-size:0.85rem; color:#e5e7eb;">{label}</span>
            <span style="font-size:0.85rem; color:#e5e7eb; opacity:0.8;">{display_value}</span>
        </div>
        <div class="neon-bar-container">
            <div class="neon-bar-fill" style="width:{display_value}%;"></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------
# PAGE 1: VALIDATE IDEA
# ---------------------------------------------------------
def page_validate_idea():
    st.markdown('<div class="section-title">Mode · Validation</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">Evaluate a Startup Idea</div>', unsafe_allow_html=True)
    st.write(
        "Describe your idea and Ouroboros Venture Advisor will score it across trends, "
        "financials, impact, and risk—then generate a 30‑day execution roadmap."
    )

    with st.container():
        col_form, col_result = st.columns([1.1, 1.4])

        # LEFT: FORM
        with col_form:
            st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
            st.markdown("#### Idea Details")

            idea_description = st.text_area(
                "Idea Description",
                placeholder="AI‑powered co‑pilot for solo founders to validate and prioritize startup ideas...",
                height=120,
            )
            target_customer = st.text_input(
                "Target Customer",
                placeholder="Solo founders, indie hackers, early‑stage builders...",
            )
            problem = st.text_area(
                "Problem",
                placeholder="Founders struggle to objectively evaluate ideas across market demand, feasibility, and risk...",
                height=100,
            )
            competitors = st.text_area(
                "Competitors",
                placeholder="Notion, Airtable templates, generic AI chatbots, startup idea lists...",
                height=80,
            )
            revenue_model = st.text_input(
                "Revenue Model",
                placeholder="Subscription, usage‑based, one‑time fee, consulting upsell...",
            )
            stage = st.selectbox(
                "Current Stage",
                ["Idea only", "Prototype", "MVP live", "Paying users", "Scaling"],
                index=0,
            )

            validate_btn = st.button("⚡ Run Idea Evaluation", use_container_width=True)

            st.markdown("</div>", unsafe_allow_html=True)

        # RIGHT: RESULTS
        with col_result:
            st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
            st.markdown("#### Evaluation Summary")

            if validate_btn:
                if not idea_description.strip():
                    st.warning("Please provide at least an idea description to run evaluation.")
                else:
                    with st.spinner("Analyzing your idea across trends, financials, impact, and risk..."):
                        result = orch.validate_idea(
                            idea_description=idea_description,
                            target_customer=target_customer,
                            problem=problem,
                            competitors=competitors,
                            revenue_model=revenue_model,
                            stage=stage,
                        )

                    scores = result.get("scores", {})
                    summary = result.get("summary", "")
                    strengths = result.get("strengths", [])
                    weaknesses = result.get("weaknesses", [])

                    overall = scores.get("overall_viability", 50)
                    recommendation = scores.get("recommendation", "PROCEED WITH CAUTION")

                    st.markdown(
                        f"""
                        <div class="score-badge">
                            <span>Overall Viability</span>
                            <span style="font-size:0.9rem;">{overall}/100</span>
                            <span style="opacity:0.7;">·</span>
                            <span>{recommendation}</span>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                    st.markdown(f"<p style='margin-top:0.6rem; color:#e5e7eb;'>{summary}</p>", unsafe_allow_html=True)

                    st.markdown("##### Score Breakdown")
                    neon_score_bar("Market Demand", scores.get("market_demand", 50))
                    neon_score_bar("Feasibility", scores.get("feasibility", 50))
                    neon_score_bar("Impact", scores.get("impact", 50))
                    neon_score_bar("Risk (lower is better)", scores.get("risk", 50), invert=True)

                    col_s, col_w = st.columns(2)
                    with col_s:
                        st.markdown("##### Strengths")
                        if strengths:
                            for s in strengths:
                                st.markdown(f"- {s}")
                        else:
                            st.markdown("- No strengths identified.")
                    with col_w:
                        st.markdown("##### Weaknesses")
                        if weaknesses:
                            for w in weaknesses:
                                st.markdown(f"- {w}")
                        else:
                            st.markdown("- No weaknesses identified.")
            else:
                st.info("Fill in the idea details on the left and click **Run Idea Evaluation**.")

            st.markdown("</div>", unsafe_allow_html=True)

    # EXECUTION PLAN
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.markdown("#### Suggested 30‑Day Execution Plan")

    if "result" in locals() and result.get("next_steps"):
        plan = result["next_steps"]
        for step in plan:
            week = step.get("week", "?")
            tasks = step.get("tasks", [])
            st.markdown(
                f"""
                <div class="timeline-week">
                    <div style="display:flex; align-items:center; margin-bottom:0.2rem;">
                        <div class="timeline-dot"></div>
                        <span style="font-size:0.95rem; font-weight:600; color:#e5e7eb;">Week {week}</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            for t in tasks:
                st.markdown(f"- {t}")
    else:
        st.caption("Execution plan will appear here after you run an evaluation.")

    st.markdown("</div>", unsafe_allow_html=True)


# ---------------------------------------------------------
# PAGE 2: GENERATE IDEAS
# ---------------------------------------------------------
def page_generate_ideas():
    st.markdown('<div class="section-title">Mode · Generation</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">Generate Startup Ideas</div>', unsafe_allow_html=True)
    st.write(
        "Describe your budget, goals, and constraints. Ouroboros Venture Advisor will generate multiple startup ideas "
        "and score them across financials, impact, and risk."
    )

    with st.container():
        col_form, col_result = st.columns([1.1, 1.4])

        # LEFT: FORM
        with col_form:
            st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
            st.markdown("#### Generation Settings")

            budget = st.number_input("Budget (USD)", min_value=0, value=1000, step=100)
            goal = st.text_area(
                "Goal",
                placeholder="Build a SaaS or AI‑powered product that can reach $X MRR in Y months...",
                height=100,
            )
            constraints = st.text_area(
                "Constraints",
                placeholder="Solo founder, limited engineering time, no paid ads, prefer B2B, etc...",
                height=80,
            )
            time_horizon = st.number_input("Time Horizon (days)", min_value=7, max_value=365, value=90, step=7)

            generate_btn = st.button("🚀 Generate & Rank Ideas", use_container_width=True)

            st.markdown("</div>", unsafe_allow_html=True)

        # RIGHT: RESULTS
        with col_result:
            st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
            st.markdown("#### Generated Ideas & Ranking")

            if generate_btn:
                if not goal.strip():
                    st.warning("Please provide at least a goal to generate ideas.")
                else:
                    with st.spinner("Generating ideas, scoring them, and computing a ranking..."):
                        session = orch.run_session(
                            budget=budget,
                            goal=goal,
                            constraints=constraints,
                            time_horizon=time_horizon,
                        )

                    ideas = session.get("ideas", [])
                    financial_scores = session.get("financial_scores", {})
                    impact_scores = session.get("impact_scores", {})
                    ethics_scores = session.get("ethics_scores", {})
                    top_recs = session.get("top_recommendations", [])

                    if ideas:
                        for idea in ideas:
                            title = idea.get("title", "Untitled Idea")
                            desc = idea.get("description", "")
                            category = idea.get("category", "Uncategorized")
                            why_now = idea.get("why_now", "")
                            target_customer = idea.get("target_customer", "")
                            problem = idea.get("problem", "")
                            revenue_model = idea.get("revenue_model", "")

                            f_score = financial_scores.get(title, 0)
                            i_score = impact_scores.get(title, 0)
                            r_score = ethics_scores.get(title, 0)

                            st.markdown('<div class="idea-card">', unsafe_allow_html=True)
                            st.markdown(f"**{title}**")
                            st.caption(category)
                            st.markdown(desc)

                            st.markdown(
                                f"""
                                <div style="margin-top:0.3rem; margin-bottom:0.3rem;">
                                    <span class="pill">Why now: {why_now}</span>
                                    <span class="pill">Customer: {target_customer}</span>
                                    <span class="pill">Revenue: {revenue_model}</span>
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )

                            neon_score_bar("Financial Potential", f_score)
                            neon_score_bar("Impact", i_score)
                            neon_score_bar("Risk (lower is better)", r_score, invert=True)

                            st.markdown("</div>", unsafe_allow_html=True)

                        if top_recs:
                            st.markdown("##### Top Recommendation")
                            top = top_recs[0]
                            top_idea = top.get("idea", {})
                            top_score = top.get("combined_score", 0)
                            reason = top.get("reason", "")

                            st.success(
                                f"**{top_idea.get('title', 'Top Idea')}** · Combined Score: {top_score}\n\n{reason}"
                            )
                    else:
                        st.info("No ideas generated. Try adjusting your goal or constraints.")
            else:
                st.info("Fill in the generation settings on the left and click **Generate & Rank Ideas**.")

            st.markdown("</div>", unsafe_allow_html=True)

    # EXECUTION PLAN FOR TOP IDEA
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.markdown("#### Suggested Execution Plan for Top Idea")

    if "session" in locals() and session.get("execution_plan"):
        plan = session["execution_plan"]
        for step in plan:
            week = step.get("week", "?")
            tasks = step.get("tasks", [])
            st.markdown(
                f"""
                <div class="timeline-week">
                    <div style="display:flex; align-items:center; margin-bottom:0.2rem;">
                        <div class="timeline-dot"></div>
                        <span style="font-size:0.95rem; font-weight:600; color:#e5e7eb;">Week {week}</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            for t in tasks:
                st.markdown(f"- {t}")
    else:
        st.caption("Execution plan for the top idea will appear here after you generate ideas.")

    st.markdown("</div>", unsafe_allow_html=True)


# ---------------------------------------------------------
# PAGE 3: COMPARE IDEAS
# ---------------------------------------------------------
def page_compare_ideas():
    st.markdown('<div class="section-title">Mode · Comparison</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">Compare Multiple Ideas</div>', unsafe_allow_html=True)
    st.write(
        "Use this page to quickly compare multiple ideas you’ve already evaluated. "
        "Adjust the sliders to reflect their scores and see them side‑by‑side."
    )

    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.markdown("#### Manual Comparison Grid")

    col1, col2, col3 = st.columns(3)

    with col1:
        idea_a = st.text_input("Idea A Title", value="Idea A")
        a_market = st.slider("A · Market Demand", 0, 100, 70)
        a_feas = st.slider("A · Feasibility", 0, 100, 60)
        a_impact = st.slider("A · Impact", 0, 100, 75)
        a_risk = st.slider("A · Risk (lower better)", 0, 100, 40)

    with col2:
        idea_b = st.text_input("Idea B Title", value="Idea B")
        b_market = st.slider("B · Market Demand", 0, 100, 65)
        b_feas = st.slider("B · Feasibility", 0, 100, 55)
        b_impact = st.slider("B · Impact", 0, 100, 80)
        b_risk = st.slider("B · Risk (lower better)", 0, 100, 35)

    with col3:
        idea_c = st.text_input("Idea C Title", value="Idea C")
        c_market = st.slider("C · Market Demand", 0, 100, 60)
        c_feas = st.slider("C · Feasibility", 0, 100, 65)
        c_impact = st.slider("C · Impact", 0, 100, 70)
        c_risk = st.slider("C · Risk (lower better)", 0, 100, 45)

    st.markdown("---")
    st.markdown("#### Visual Comparison")

    comp_cols = st.columns(3)
    ideas = [
        (idea_a, a_market, a_feas, a_impact, a_risk),
        (idea_b, b_market, b_feas, b_impact, b_risk),
        (idea_c, c_market, c_feas, c_impact, c_risk),
    ]

    for col, (title, m, f, i, r) in zip(comp_cols, ideas):
        with col:
            st.markdown('<div class="idea-card">', unsafe_allow_html=True)
            st.markdown(f"**{title}**")
            neon_score_bar("Market Demand", m)
            neon_score_bar("Feasibility", f)
            neon_score_bar("Impact", i)
            neon_score_bar("Risk (lower is better)", r, invert=True)
            st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


# ---------------------------------------------------------
# ROUTER
# ---------------------------------------------------------
if page == "Validate Idea":
    page_validate_idea()
elif page == "Generate Ideas":
    page_generate_ideas()
elif page == "Compare Ideas":
    page_compare_ideas()

# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------
st.markdown(
    '<div class="footer">Ouroboros Venture Advisor · Built for founders who take their ideas seriously.</div>',
    unsafe_allow_html=True,
)
