import type { Node } from "@xyflow/react";
import type { Analysis, CanvasNodeData } from "./types";

export type GroveNode = Node<CanvasNodeData>;

function items(value?: string[] | null): string[] {
  return Array.isArray(value) ? value.filter(Boolean).map(String) : [];
}

function makeNode(id: string, label: string, description: string | undefined, list: string[], x: number, y: number): GroveNode {
  return {
    id,
    type: "default",
    position: { x, y },
    data: { label, description, items: list },
  };
}

export function buildCanvasLayout(analysis: Analysis): GroveNode[] {
  const nodes: GroveNode[] = [];
  const root = items(analysis.root_causes);
  const insights = items(analysis.insights);
  const recommendations = items(analysis.recommendations);
  const experiments = items(analysis.experiments);

  nodes.push(makeNode("summary", "Grove diagnosis", analysis.executive_summary ?? undefined, [], 0, 0));
  if (root.length) nodes.push(makeNode("root-causes", "Root causes", undefined, root, 360, -120));
  if (insights.length) nodes.push(makeNode("insights", "Insights", undefined, insights, 360, 120));
  if (recommendations.length) nodes.push(makeNode("recommendations", "Growth opportunities", undefined, recommendations, 760, -120));
  if (experiments.length) nodes.push(makeNode("experiments", "Next experiments", undefined, experiments, 760, 180));

  return nodes;
}
