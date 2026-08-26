"use client";

import { Handle, Position } from "@xyflow/react";

interface InsightNodeData {
  insight: string;
  confidence: number;
  agents: string[];
  category: string;
}

export function InsightNode({ data }: { data: InsightNodeData }) {
  const pct = Math.round(data.confidence * 100);
  return (
    <div className="w-[310px] rounded-xl border border-purple-500/40 bg-gradient-to-br from-purple-950/60 to-slate-900/80 backdrop-blur-sm shadow-lg p-4">
      <Handle type="target" position={Position.Top} className="!bg-purple-500 !border-purple-400" />
      <div className="flex items-center justify-between mb-2">
        <span className="text-[10px] font-semibold text-purple-400 uppercase tracking-widest">Insight</span>
        <div className="flex items-center gap-1.5">
          <div className="w-16 h-1.5 rounded-full bg-white/10">
            <div
              className="h-1.5 rounded-full bg-purple-400"
              style={{ width: `${pct}%` }}
            />
          </div>
          <span className="text-[10px] text-purple-300 font-semibold">{pct}%</span>
        </div>
      </div>
      <p className="text-white text-sm font-medium leading-snug mb-2">{data.insight}</p>
      {data.agents?.length > 0 && (
        <div className="flex flex-wrap gap-1">
          {data.agents.map((a) => (
            <span key={a} className="text-[9px] px-1.5 py-0.5 rounded bg-purple-500/20 text-purple-300 border border-purple-500/20">
              {a}
            </span>
          ))}
        </div>
      )}
      <Handle type="source" position={Position.Bottom} className="!bg-purple-500 !border-purple-400" />
    </div>
  );
}
