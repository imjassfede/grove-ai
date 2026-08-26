from langgraph.constants import Send
from langgraph.graph import StateGraph

from app.reasoning import classifier, evaluator, planner
from app.reasoning.state import GrowthState


def _dispatch_agents(state: GrowthState) -> list[Send]:
    """Fan out to selected intelligence agents in parallel."""
    from app.intelligence import registry

    return [
        Send(
            agent_name,
            {
                "challenge": state["challenge"],
                "analysis_id": state["analysis_id"],
                "business_area": state["business_area"],
                "problem_type": state["problem_type"],
                "urgency": state["urgency"],
                "key_questions": state["key_questions"],
                "focus_areas": state["agent_focus"].get(agent_name, []),
            },
        )
        for agent_name in state["selected_agents"]
        if agent_name in registry
    ]


def build_graph() -> StateGraph:
    builder = StateGraph(GrowthState)

    # Core reasoning nodes
    builder.add_node("classify", classifier.classify)
    builder.add_node("plan", planner.plan)
    builder.add_node("evaluate", evaluator.evaluate)

    # Intelligence agent nodes (registered dynamically)
    from app.intelligence import registry
    for name, agent in registry.items():
        builder.add_node(name, agent.run)

    # Edges
    builder.set_entry_point("classify")
    builder.add_edge("classify", "plan")
    builder.add_conditional_edges("plan", _dispatch_agents)

    # All agent nodes converge to evaluate
    from app.intelligence import registry as reg
    for name in reg:
        builder.add_edge(name, "evaluate")

    builder.set_finish_point("evaluate")

    return builder.compile()


graph = build_graph()
