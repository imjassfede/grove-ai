from langgraph.graph import END, StateGraph

from app.reasoning import classifier, critic, evaluator, planner
from app.reasoning.state import GrowthState


_CORE_AGENTS = ("market", "customer", "revenue", "gtm")
_ALL_AGENTS = ("competitor", "market", "customer", "revenue", "gtm", "experiment")


def _followup_route(state: GrowthState):
    agent = state.get("followup_agent")
    if agent in _ALL_AGENTS and state.get("research_round", 0) <= 2:
        return agent
    return "evaluate"


def build_graph() -> StateGraph:
    builder = StateGraph(GrowthState)
    builder.add_node("classify", classifier.classify)
    builder.add_node("plan", planner.plan)
    builder.add_node("critic", critic.critique)
    builder.add_node("evaluate", evaluator.evaluate)

    from app.intelligence import registry
    for name, agent in registry.items():
        builder.add_node(name, agent.run)

    builder.set_entry_point("classify")
    builder.add_edge("classify", "plan")
    # Competitor discovery is intentionally first because its validated Top 3
    # dossier becomes shared context for market/customer/revenue/GTM.
    builder.add_edge("plan", "competitor")
    for name in _CORE_AGENTS:
        builder.add_edge("competitor", name)
    builder.add_edge(list(_CORE_AGENTS), "experiment")
    builder.add_edge("experiment", "critic")

    # The critic can delegate exactly one targeted follow-up to a specialist.
    # That specialist returns to the critic, creating a bounded adaptive loop.
    builder.add_conditional_edges(
        "critic",
        _followup_route,
        {**{name: name for name in _ALL_AGENTS}, "evaluate": "evaluate"},
    )
    for name in _ALL_AGENTS:
        builder.add_edge(name, "critic")

    builder.set_finish_point("evaluate")
    return builder.compile()


graph = build_graph()
