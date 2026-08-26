"use client";

import {
  Background,
  BackgroundVariant,
  Controls,
  MiniMap,
  ReactFlow,
  ReactFlowProvider,
} from "@xyflow/react";
import "@xyflow/react/dist/style.css";

import { ExperimentNode } from "./nodes/ExperimentNode";
import { InsightNode } from "./nodes/InsightNode";
import { ProblemNode } from "./nodes/ProblemNode";
import { RecommendationNode } from "./nodes/RecommendationNode";
import { RootCauseNode } from "./nodes/RootCauseNode";

const nodeTypes = {
  problemNode: ProblemNode,
  rootCauseNode: RootCauseNode,
  insightNode: InsightNode,
  recommendationNode: RecommendationNode,
  experimentNode: ExperimentNode,
};

interface GrowthCanvasProps {
  nodes: ReturnType<typeof import("@xyflow/react")["useNodes"]>;
  edges: ReturnType<typeof import("@xyflow/react")["useEdges"]>;
}

export function GrowthCanvas({
  nodes,
  edges,
}: {
  nodes: object[];
  edges: object[];
}) {
  return (
    <ReactFlowProvider>
      <div className="w-full h-full">
        <ReactFlow
          nodes={nodes as never}
          edges={edges as never}
          nodeTypes={nodeTypes}
          fitView
          fitViewOptions={{ padding: 0.15 }}
          minZoom={0.2}
          maxZoom={1.5}
          className="bg-[#070b14]"
        >
          <Background
            variant={BackgroundVariant.Dots}
            gap={24}
            size={1}
            color="rgba(255,255,255,0.04)"
          />
          <Controls className="!bg-slate-900 !border-white/10 [&>button]:!bg-slate-900 [&>button]:!border-white/10 [&>button]:!text-white/60" />
          <MiniMap
            className="!bg-slate-900 !border-white/10"
            nodeColor={() => "rgba(255,255,255,0.15)"}
            maskColor="rgba(0,0,0,0.6)"
          />
        </ReactFlow>
      </div>
    </ReactFlowProvider>
  );
}
