"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";
import { ArrowRight, Globe, TrendingUp } from "lucide-react";
import { startDomainAnalysis } from "@/lib/api";
import { Spinner } from "@/components/ui/Spinner";

function normalizeDomain(value: string) {
  return value.trim().replace(/^https?:\/\//, "").replace(/^www\./, "").split("/")[0];
}

function isValidDomain(value: string) {
  const domain = normalizeDomain(value);
  return domain.length >= 4 && domain.includes(".") && !domain.includes(" ") && /^[a-zA-Z0-9.-]+$/.test(domain);
}

export default function WorkspacePage() {
  const router = useRouter();
  const [domain, setDomain] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    const normalized = normalizeDomain(domain);
    if (!isValidDomain(normalized) || loading) return;
    setLoading(true);
    setError(null);
    try {
      const analysis = await startDomainAnalysis(normalized);
      router.push(`/workspace/${analysis.id}`);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong");
      setLoading(false);
    }
  }

  return (
    <main className="min-h-screen bg-[#050507] flex flex-col">
      <div className="border-b border-white/5 px-6 py-4 flex items-center justify-between">
        <a href="/" className="flex items-center gap-2 text-white/70 hover:text-white transition-colors">
          <TrendingUp className="w-4 h-4 text-blue-500" />
          <span className="font-semibold text-sm">Grove</span>
        </a>
        <span className="text-xs text-white/30">5 free credits</span>
      </div>

      <div className="flex-1 flex flex-col items-center justify-center px-6 py-16 max-w-xl mx-auto w-full">
        <div className="text-center mb-9">
          <div className="mx-auto mb-5 w-12 h-12 rounded-2xl border border-blue-500/20 bg-blue-500/10 flex items-center justify-center">
            <Globe className="w-5 h-5 text-blue-400" />
          </div>
          <h1 className="text-3xl sm:text-4xl font-bold mb-3 tracking-tight">Find where to grow next.</h1>
          <p className="text-white/40 text-sm leading-relaxed max-w-md mx-auto">
            Start with your company website. Grove will investigate your market, customers, competitors and growth opportunities.
          </p>
        </div>

        <form onSubmit={handleSubmit} className="w-full">
          <div className="flex gap-2 p-1.5 rounded-xl border border-white/10 bg-white/[0.03] focus-within:border-blue-500/40 transition-colors">
            <input
              value={domain}
              onChange={(e) => setDomain(e.target.value)}
              placeholder="yourcompany.com"
              autoFocus
              disabled={loading}
              className="min-w-0 flex-1 bg-transparent px-3 py-2.5 text-sm text-white placeholder-white/20 outline-none"
              aria-label="Company website"
            />
            <button type="submit" disabled={!isValidDomain(domain) || loading} className="shrink-0 inline-flex items-center gap-2 px-5 py-2.5 rounded-lg bg-blue-600 hover:bg-blue-500 disabled:opacity-30 disabled:cursor-not-allowed font-semibold text-sm transition-all">
              {loading ? <><Spinner className="w-4 h-4" /> Analyzing…</> : <>Analyze <ArrowRight className="w-4 h-4" /></>}
            </button>
          </div>
          {error && <p className="mt-3 text-xs text-red-300 text-center">{error}</p>}
          <p className="mt-3 text-center text-[11px] text-white/25">Free analysis · 5 credits · No credit card required</p>
        </form>

        <div className="mt-12 w-full grid grid-cols-3 gap-2 text-center">
          <div className="rounded-lg border border-white/5 bg-white/[0.02] p-3"><p className="text-xs font-medium text-white/60">Market</p><p className="text-[10px] text-white/25 mt-1">Signals & trends</p></div>
          <div className="rounded-lg border border-white/5 bg-white/[0.02] p-3"><p className="text-xs font-medium text-white/60">Competition</p><p className="text-[10px] text-white/25 mt-1">Positioning & gaps</p></div>
          <div className="rounded-lg border border-white/5 bg-white/[0.02] p-3"><p className="text-xs font-medium text-white/60">Growth</p><p className="text-[10px] text-white/25 mt-1">Next opportunities</p></div>
        </div>
      </div>
    </main>
  );
}
