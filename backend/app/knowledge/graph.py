from __future__ import annotations

from typing import Any


def build_knowledge_graph(agent_results: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    """Build a lightweight evidence graph from structured agent output.

    This deliberately stays dependency-free for the MVP. The graph is JSON-ready
    and can later be persisted in Postgres/pgvector or a graph database without
    changing the agent contract.
    """
    nodes: dict[str, dict[str, Any]] = {}
    edges: list[dict[str, Any]] = []

    def node(key: str, kind: str, label: str):
        nodes.setdefault(key, {"id": key, "type": kind, "label": label})

    for agent, result in agent_results.items():
        agent_id = f"agent:{agent}"
        node(agent_id, "agent", agent.title())
        for idx, finding in enumerate(result.get("findings", [])):
            text = str(finding.get("finding", "")).strip()
            if not text:
                continue
            finding_id = f"finding:{agent}:{idx}"
            node(finding_id, "finding", text[:180])
            edges.append({"source": agent_id, "target": finding_id, "relation": "produces"})
            for url in finding.get("source_urls", [])[:5]:
                source_id = f"source:{url}"
                node(source_id, "source", url)
                edges.append({"source": finding_id, "target": source_id, "relation": "supported_by"})

        for idx, insight in enumerate(result.get("insights", [])):
            text = str(insight.get("insight", "")).strip()
            if not text:
                continue
            insight_id = f"insight:{agent}:{idx}"
            node(insight_id, "insight", text[:180])
            edges.append({"source": agent_id, "target": insight_id, "relation": "derives"})

    return {"nodes": list(nodes.values()), "edges": edges}
