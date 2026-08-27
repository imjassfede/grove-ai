from langgraph.graph import StateGraph

from app.reasoning import classifier, evaluator, planner
from app.reasoning.state import GrowthState


# Grove currently uses a deliberately simple staged research DAG.
# The sequence makes dependencies explicit:
#   competitor -> market/customer/revenue/gtm -> experiment -> synthesis
#
# This is the foundation for later adaptive routing, critic loops, and
# specialist-to-specialist delegation.


def build_graph() -> StateGraph:
    builder = StateGraph(GrowthState)

    builder.add_node("classify", classifier.classify)
    builder.add_node("plan", planner.plan)
    builder.add_node("evaluate", evaluator.evaluate)

    from app.intelligence import registry
    for name, agent in registry.items():
        builder.add_node(name, agent.run)

    builder.set_entry_point("classify")
    builder.add_edge("classify", "plan")

    # Competitive intelligence is the shared foundation. All downstream
    # specialists receive its result through the shared LangGraph state.
    builder.add_edge("plan", "competitor")

    # Cross-functional research runs in parallel after the competitor dossier
    # is available. Their results are merged into agent_results.
    for name in ("market", "customer", "revenue", "gtm"):
        builder.add_edge("competitor", name)

    # Experiment design only starts once all four research perspectives have
    # completed, so it can reason over the complete intelligence set.
    builder.add_edge(["market", "customer", "revenue", "gtm"], "experiment")
    builder.add_edge("experiment", "evaluate")

    builder.set_finish_point("evaluate")
    return builder.compile()


graph = build_graph()
