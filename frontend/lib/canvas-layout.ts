import type { Edge, Node } from "@xyflow/react";
import type { Analysis, CanvasNodeData } from "./types";

export type GroveNode = Node<CanvasNodeData>;
const list = (value: unknown[] | null | undefined): string[] => Array.isArray(value) ? value.filter(Boolean).map(String) : [];

export function buildCanvasLayout(analysis: Analysis): { nodes: GroveNode[]; edges: Edge[] } {
  const nodes: GroveNode[] = [];
  const edges: Edge[] = [];
  const add = (id: string, type: string, label: string, description: string | undefined, items: string[], x: number, y: number) => nodes.push({ id, type, position: { x, y }, data: { label, description, items } });
  add("problem", "problemNode", analysis.problem_type ?? "Growth problem", analysis.executive_summary ?? undefined, [], 0, 0);
  const roots = Array.isArray(analysis.root_causes) ? analysis.root_causes.map(r => `${r.cause}: ${r.evidence}`) : [];
  const insights = list(analysis.insights);
  const recommendations = Array.isArray(analysis.recommendations) ? analysis.recommendations.map(r => r.action) : [];
  const experiments = Array.isArray(analysis.experiments) ? analysis.experiments.map(e => e.hypothesis) : [];
  if (roots.length) { add("root-causes", "rootCauseNode", "Root causes", undefined, roots, 360, -160); edges.push({ id: "e-problem-root", source: "problem", target: "root-causes" }); }
  if (insights.length) { add("insights", "insightNode", "Insights", undefined, insights, 360, 100); edges.push({ id: "e-problem-insight", source: "problem", target: "insights" }); }
  if (recommendations.length) { add("recommendations", "recommendationNode", "Growth opportunities", undefined, recommendations, 760, -160); edges.push({ id: "e-rec", source: roots.length ? "root-causes" : "insights", target: "recommendations" }); }
  if (experiments.length) { add("experiments", "experimentNode", "Next experiments", undefined, experiments, 760, 140); edges.push({ id: "e-exp", source: "recommendations", target: "experiments" }); }
  return { nodes, edges };
}
