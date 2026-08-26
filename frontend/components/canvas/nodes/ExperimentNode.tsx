"use client";

import { Handle, Position } from "@xyflow/react";

interface ExperimentNodeData {
  hypothesis: string;
  ice_score: number;
  impact_score: number;
  confidence_score: number;
  ease_score: number;
  measurement: string;
  timeline: string;
}

function ScorePill({ label, value }: { label: string; value: number }) {
  return (
    <div className="flex flex-col items-center rounded bg-white/5 px-2 py-1 min-w-[40px]">
      <span className="text-[9px] text-white/40 uppercase">{label}</span>
      <span className="text-sm font-bold text-amber-300">{value.toFixed(1)}</span>
    </div>
  );
}

export function ExperimentNode({ data }: { data: ExperimentNodeData }) {
  return (
    <div className="w-[350px] rounded-xl border border-amber-500/40 bg-gradient-to-br from-amber-950/40 to-slate-900/80 backdrop-blur-sm shadow-lg p-4">
      <Handle type="target" position={Position.Top} className="!bg-amber-500 !border-amber-400" />
      <div className="flex items-center justify-between mb-2">
        <span className="text-[10px] font-semibold text-amber-400 uppercase tracking-widest">Experiment</span>
        <div className="flex items-center gap-1 text-[10px]">
          <span className="text-white/40">ICE</span>
          <span className="font-bold text-amber-300 text-sm">{data.ice_score.toFixed(1)}</span>
        </div>
      </div>
      <p className="text-white text-xs leading-relaxed mb-3 italic">"{data.hypothesis}"</p>
      <div className="flex gap-2 mb-3">
        <ScorePill label="Impact" value={data.impact_score} />
        <ScorePill label="Conf." value={data.confidence_score} />
        <ScorePill label="Ease" value={data.ease_score} />
      </div>
      <div className="text-[10px] text-white/40 space-y-0.5">
        <div>📊 {data.measurement}</div>
        <div>⏱ {data.timeline}</div>
      </div>
    </div>
  );
}
