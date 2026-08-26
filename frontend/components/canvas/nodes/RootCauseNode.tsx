"use client";

import { Handle, Position } from "@xyflow/react";
import { Badge } from "@/components/ui/Badge";

interface RootCauseNodeData {
  cause: string;
  evidence: string;
  impact: "high" | "medium" | "low";
}

const impactVariant: Record<string, "red" | "orange" | "amber"> = {
  high: "red",
  medium: "orange",
  low: "amber",
};

export function RootCauseNode({ data }: { data: RootCauseNodeData }) {
  return (
    <div className="w-[320px] rounded-xl border border-red-500/40 bg-gradient-to-br from-red-950/60 to-slate-900/80 backdrop-blur-sm shadow-lg p-4">
      <Handle type="target" position={Position.Top} className="!bg-red-500 !border-red-400" />
      <div className="flex items-center justify-between mb-2">
        <span className="text-[10px] font-semibold text-red-400 uppercase tracking-widest">Root Cause</span>
        <Badge label={`${data.impact} impact`} variant={impactVariant[data.impact] ?? "orange"} />
      </div>
      <p className="text-white font-semibold text-sm mb-2 leading-snug">{data.cause}</p>
      <p className="text-white/50 text-xs leading-relaxed">{data.evidence}</p>
      <Handle type="source" position={Position.Bottom} className="!bg-red-500 !border-red-400" />
    </div>
  );
}
