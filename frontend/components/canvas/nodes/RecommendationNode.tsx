"use client";

import { Handle, Position } from "@xyflow/react";
import { Badge } from "@/components/ui/Badge";

interface RecommendationNodeData {
  action: string;
  priority: "p1" | "p2" | "p3";
  effort: "low" | "medium" | "high";
  impact: "low" | "medium" | "high";
  timeline: string;
  owner: string;
}

const priorityVariant: Record<string, "red" | "orange" | "gray"> = {
  p1: "red",
  p2: "orange",
  p3: "gray",
};

export function RecommendationNode({ data }: { data: RecommendationNodeData }) {
  return (
    <div className="w-[340px] rounded-xl border border-green-500/40 bg-gradient-to-br from-green-950/60 to-slate-900/80 backdrop-blur-sm shadow-lg p-4">
      <Handle type="target" position={Position.Top} className="!bg-green-500 !border-green-400" />
      <div className="flex items-center justify-between mb-2">
        <span className="text-[10px] font-semibold text-green-400 uppercase tracking-widest">Recommendation</span>
        <Badge label={data.priority.toUpperCase()} variant={priorityVariant[data.priority] ?? "gray"} />
      </div>
      <p className="text-white text-sm font-semibold leading-snug mb-3">{data.action}</p>
      <div className="grid grid-cols-3 gap-2 text-[10px]">
        <div className="rounded bg-white/5 px-2 py-1 text-center">
          <div className="text-white/40 mb-0.5">Effort</div>
          <div className="text-white/80 font-semibold capitalize">{data.effort}</div>
        </div>
        <div className="rounded bg-white/5 px-2 py-1 text-center">
          <div className="text-white/40 mb-0.5">Impact</div>
          <div className="text-white/80 font-semibold capitalize">{data.impact}</div>
        </div>
        <div className="rounded bg-white/5 px-2 py-1 text-center">
          <div className="text-white/40 mb-0.5">Owner</div>
          <div className="text-white/80 font-semibold">{data.owner}</div>
        </div>
      </div>
      <div className="mt-2 text-[10px] text-white/40">⏱ {data.timeline}</div>
      <Handle type="source" position={Position.Bottom} className="!bg-green-500 !border-green-400" />
    </div>
  );
}
