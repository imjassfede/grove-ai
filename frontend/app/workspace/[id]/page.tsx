"use client";

import { useParams, useRouter } from "next/navigation";
import { useCallback, useEffect, useRef, useState } from "react";
import {
  AlertCircle,
  ArrowLeft,
  BarChart3,
  Brain,
  ChevronRight,
  FlaskConical,
  Lightbulb,
  TrendingUp,
  Users,
} from "lucide-react";
import { getAnalysis } from "@/lib/api";
import { buildCanvasLayout } from "@/lib/canvas-layout";
import type { Analysis, Recommendation } from "@/lib/types";
import { GrowthCanvas } from "@/components/canvas/GrowthCanvas";
import { Badge } from "@/components/ui/Badge";
import { Spinner } from "@/components/ui/Spinner";

const AGENT_ICONS: Record<string, React.ElementType> = {
  market: BarChart3,
  customer: Users,
  competitor: Brain,
  revenue: TrendingUp,
  experiment: FlaskConical,
  gtm: Lightbulb,
};

const URGENCY_VARIANT: Record<string, "red" | "orange" | "amber" | "blue"> = {
  critical: "red",
  high: "orange",
  medium: "amber",
  low: "blue",
};

const STATUS_LABELS: Record<string, string> = {
  pending: "Queued",
  running: "Initializing…",
  classifying: "Classifying problem…",
  planning: "Planning investigation…",
  analyzing: "Agents analyzing…",
  synthesizing: "Synthesizing results…",
  complete: "Complete",
  error: "Error",
};

type TabId = "canvas" | "report";

export default function AnalysisPage() {
  const { id } = useParams<{ id: string }>();
  const router = useRouter();
  const [analysis, setAnalysis] = useState<Analysis | null>(null);
  const [tab, setTab] = useState<TabId>("canvas");
  const pollRef = useRef<ReturnType<typeof setInterval> | null>(null);

  const fetchAnalysis = useCallback(async () => {
    try {
      const data = await getAnalysis(id);
      setAnalysis(data);
      if (data.status === "complete" || data.status === "error") {
        if (pollRef.current) clearInterval(pollRef.current);
      }
    } catch {
      // network error — keep polling
    }
  }, [id]);

  useEffect(() => {
    fetchAnalysis();
    pollRef.current = setInterval(fetchAnalysis, 2000);
    return () => {
      if (pollRef.current) clearInterval(pollRef.current);
    };
  }, [fetchAnalysis]);

  const { nodes, edges } = analysis?.status === "complete"
    ? buildCanvasLayout(analysis)
    : { nodes: [], edges: [] };

  const isRunning = analysis && !["complete", "error"].includes(analysis.status);

  return (
    <main className="h-screen bg-[#050507] flex flex-col overflow-hidden">
      {/* Header */}
      <div className="border-b border-white/5 px-5 py-3 flex items-center gap-4 flex-shrink-0">
        <button
          onClick={() => router.push("/workspace")}
          className="flex items-center gap-1.5 text-white/40 hover:text-white/70 transition-colors text-sm"
        >
          <ArrowLeft className="w-3.5 h-3.5" />
          New
        </button>

        <div className="flex-1 min-w-0">
          <p className="text-white/70 text-sm font-medium truncate">
            {analysis?.challenge ?? "Loading…"}
          </p>
        </div>

        <div className="flex items-center gap-3 flex-shrink-0">
          {analysis?.urgency && (
            <Badge label={analysis.urgency} variant={URGENCY_VARIANT[analysis.urgency] ?? "blue"} />
          )}
          {analysis?.business_area && (
            <Badge label={analysis.business_area} variant="gray" />
          )}
          <div className="flex items-center gap-1.5 text-xs text-white/40">
            {isRunning && <Spinner className="w-3.5 h-3.5" />}
            <span>{STATUS_LABELS[analysis?.status ?? "pending"] ?? analysis?.status}</span>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="border-b border-white/5 px-5 flex gap-6 flex-shrink-0">
        {(["canvas", "report"] as TabId[]).map((t) => (
          <button
            key={t}
            onClick={() => setTab(t)}
            className={`py-2.5 text-xs font-semibold uppercase tracking-widest border-b-2 transition-colors ${
              tab === t
                ? "border-blue-500 text-white"
                : "border-transparent text-white/30 hover:text-white/50"
            }`}
          >
            {t === "canvas" ? "Growth Canvas" : "Report"}
          </button>
        ))}
      </div>

      {/* Body */}
      <div className="flex-1 flex min-h-0">
        {/* Sidebar */}
        <aside className="w-64 border-r border-white/5 flex flex-col overflow-y-auto flex-shrink-0">
          {/* Progress */}
          {(analysis?.progress?.length ?? 0) > 0 && (
            <div className="p-4 border-b border-white/5">
              <p className="text-[10px] text-white/30 uppercase tracking-widest mb-3">Progress</p>
              <div className="space-y-2">
                {analysis!.progress!.map((msg, i) => (
                  <div key={i} className="flex items-start gap-2 text-xs text-white/50 leading-relaxed">
                    <ChevronRight className="w-3 h-3 text-blue-500 mt-0.5 flex-shrink-0" />
                    {msg}
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Agents */}
          {(analysis?.selected_agents?.length ?? 0) > 0 && (
            <div className="p-4 border-b border-white/5">
              <p className="text-[10px] text-white/30 uppercase tracking-widest mb-3">Agents deployed</p>
              <div className="space-y-2">
                {analysis!.selected_agents!.map((agent) => {
                  const Icon = AGENT_ICONS[agent] ?? Brain;
                  const done = analysis?.status === "complete";
                  return (
                    <div key={agent} className="flex items-center gap-2 text-xs">
                      <div className={`w-5 h-5 rounded flex items-center justify-center flex-shrink-0 ${done ? "bg-green-500/20" : "bg-blue-500/10"}`}>
                        <Icon className={`w-3 h-3 ${done ? "text-green-400" : "text-blue-400"}`} />
                      </div>
                      <span className="text-white/60 capitalize">{agent}</span>
                      {done && <span className="ml-auto text-green-400 text-[9px]">✓</span>}
                    </div>
                  );
                })}
              </div>
            </div>
          )}

          {/* Summary */}
          {analysis?.executive_summary && (
            <div className="p-4">
              <p className="text-[10px] text-white/30 uppercase tracking-widest mb-3">Executive summary</p>
              <p className="text-xs text-white/60 leading-relaxed">{analysis.executive_summary}</p>
            </div>
          )}

          {/* Error */}
          {analysis?.status === "error" && (
            <div className="p-4">
              <div className="flex items-start gap-2 text-red-300 text-xs">
                <AlertCircle className="w-4 h-4 flex-shrink-0 mt-0.5" />
                <p>{analysis.error ?? "An error occurred"}</p>
              </div>
            </div>
          )}
        </aside>

        {/* Main */}
        <div className="flex-1 min-w-0 overflow-hidden">
          {tab === "canvas" ? (
            <div className="h-full">
              {analysis?.status === "complete" ? (
                <GrowthCanvas nodes={nodes} edges={edges} />
              ) : (
                <div className="h-full flex flex-col items-center justify-center gap-4 text-white/30">
                  {analysis?.status === "error" ? (
                    <>
                      <AlertCircle className="w-8 h-8 text-red-400" />
                      <p className="text-sm">Analysis failed</p>
                    </>
                  ) : (
                    <>
                      <Spinner className="w-8 h-8" />
                      <p className="text-sm">{STATUS_LABELS[analysis?.status ?? "pending"]}</p>
                      <p className="text-xs text-white/20">Growth Canvas will appear when complete</p>
                    </>
                  )}
                </div>
              )}
            </div>
          ) : (
            <div className="h-full overflow-y-auto p-6 space-y-8 max-w-3xl">
              {/* Root Causes */}
              {(analysis?.root_causes?.length ?? 0) > 0 && (
                <section>
                  <h2 className="text-xs font-semibold text-red-400 uppercase tracking-widest mb-4">Root Causes</h2>
                  <div className="space-y-3">
                    {analysis!.root_causes!.map((rc, i) => (
                      <div key={i} className="rounded-lg border border-white/5 bg-white/[0.02] p-4">
                        <div className="flex items-start justify-between gap-3 mb-1.5">
                          <p className="text-sm font-semibold text-white/90">{rc.cause}</p>
                          <Badge label={rc.impact} variant={rc.impact === "high" ? "red" : rc.impact === "medium" ? "orange" : "amber"} />
                        </div>
                        <p className="text-xs text-white/40 leading-relaxed">{rc.evidence}</p>
                      </div>
                    ))}
                  </div>
                </section>
              )}

              {/* Recommendations */}
              {(analysis?.recommendations?.length ?? 0) > 0 && (
                <section>
                  <h2 className="text-xs font-semibold text-green-400 uppercase tracking-widest mb-4">Recommendations</h2>
                  <div className="space-y-3">
                    {analysis!.recommendations!.map((rec: Recommendation, i: number) => (
                      <div key={i} className="rounded-lg border border-white/5 bg-white/[0.02] p-4">
                        <div className="flex items-start justify-between gap-3 mb-2">
                          <p className="text-sm font-semibold text-white/90">{rec.action}</p>
                          <Badge label={rec.priority.toUpperCase()} variant={rec.priority === "p1" ? "red" : rec.priority === "p2" ? "orange" : "gray"} />
                        </div>
                        <div className="flex gap-4 text-[10px] text-white/40">
                          <span>Effort: <span className="text-white/60 capitalize">{rec.effort}</span></span>
                          <span>Impact: <span className="text-white/60 capitalize">{rec.impact}</span></span>
                          <span>Owner: <span className="text-white/60">{rec.owner}</span></span>
                          <span>Timeline: <span className="text-white/60">{rec.timeline}</span></span>
                        </div>
                      </div>
                    ))}
                  </div>
                </section>
              )}

              {/* Experiments */}
              {(analysis?.experiments?.length ?? 0) > 0 && (
                <section>
                  <h2 className="text-xs font-semibold text-amber-400 uppercase tracking-widest mb-4">Experiments</h2>
                  <div className="space-y-3">
                    {analysis!.experiments!.map((exp, i) => (
                      <div key={i} className="rounded-lg border border-white/5 bg-white/[0.02] p-4">
                        <div className="flex items-start justify-between gap-3 mb-2">
                          <p className="text-xs text-white/80 leading-relaxed italic">"{exp.hypothesis}"</p>
                          <div className="flex-shrink-0 text-center">
                            <div className="text-lg font-black text-amber-300">{exp.ice_score.toFixed(1)}</div>
                            <div className="text-[9px] text-white/30 uppercase">ICE</div>
                          </div>
                        </div>
                        <div className="flex gap-4 text-[10px] text-white/40">
                          <span>📊 {exp.measurement}</span>
                          <span>⏱ {exp.timeline}</span>
                        </div>
                      </div>
                    ))}
                  </div>
                </section>
              )}

              {!analysis?.root_causes && analysis?.status !== "complete" && (
                <div className="flex flex-col items-center justify-center h-64 text-white/20 gap-3">
                  <Spinner className="w-6 h-6" />
                  <p className="text-sm">Analysis in progress…</p>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </main>
  );
}
