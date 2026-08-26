"use client";

import { Handle, Position } from "@xyflow/react";
import { Badge } from "@/components/ui/Badge";

interface ProblemNodeData {
  challenge: string;
  urgency: string | null;
}

const urgencyVariant: Record<string, "red" | "orange" | "amber" | "blue"> = {
  critical: "red",
  high: "orange",
  medium: "amber",
  low: "blue",
};

export function ProblemNode({ data }: { data: ProblemNodeData }) {
  return (
    <div className="w-[350px] rounded-xl border border-blue-500/50 bg-gradient-to-br from-blue-950/80 to-slate-900/80 backdrop-blur-sm shadow-[0_0_30px_rgba(59,130,246,0.15)] p-5">
      <div className="flex items-center justify-between mb-3">
        <span className="text-xs font-semibold text-blue-400 uppercase tracking-widest">
          Business Challenge
        </span>
        {data.urgency && (
          <Badge label={data.urgency} variant={urgencyVariant[data.urgency] ?? "blue"} />
        )}
      </div>
      <p className="text-white font-medium leading-snug text-sm">{data.challenge}</p>
      <Handle type="source" position={Position.Bottom} className="!bg-blue-500 !border-blue-400" />
    </div>
  );
}
