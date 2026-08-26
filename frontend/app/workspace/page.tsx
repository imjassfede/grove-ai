"use client";

import { useRouter, useSearchParams } from "next/navigation";
import { Suspense, useEffect, useRef, useState } from "react";
import { ArrowRight, Lightbulb, TrendingUp } from "lucide-react";
import { submitChallenge } from "@/lib/api";
import { Spinner } from "@/components/ui/Spinner";

const EXAMPLES = [
  "Why is our enterprise churn increasing despite product improvements?",
  "Revenue growth slowed in Europe — what's driving it?",
  "Why is activation dropping after our latest onboarding?",
  "Where should we invest our growth budget next quarter?",
  "Why is our pipeline conversion declining?",
  "How do we break into the SMB market?",
];

function WorkspaceContent() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [challenge, setChallenge] = useState(searchParams.get("q") ?? "");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    textareaRef.current?.focus();
  }, []);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!challenge.trim() || loading) return;
    setLoading(true);
    setError(null);
    try {
      const analysis = await submitChallenge(challenge.trim());
      router.push(`/workspace/${analysis.id}`);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong");
      setLoading(false);
    }
  }

  const charCount = challenge.length;
  const isValid = charCount >= 10 && charCount <= 2000;

  return (
    <main className="min-h-screen bg-[#050507] flex flex-col">
      {/* Header */}
      <div className="border-b border-white/5 px-6 py-4 flex items-center justify-between">
        <a href="/" className="flex items-center gap-2 text-white/70 hover:text-white transition-colors">
          <TrendingUp className="w-4 h-4 text-blue-500" />
          <span className="font-semibold text-sm">Growth AI</span>
        </a>
        <span className="text-xs text-white/20">New analysis</span>
      </div>

      {/* Content */}
      <div className="flex-1 flex flex-col items-center justify-center px-6 py-16 max-w-2xl mx-auto w-full">
        <div className="text-center mb-10">
          <h1 className="text-3xl font-bold mb-3">What's your growth challenge?</h1>
          <p className="text-white/40 text-sm leading-relaxed">
            Describe a business problem you're facing. Be specific — the more context, the sharper the analysis.
          </p>
        </div>

        <form onSubmit={handleSubmit} className="w-full space-y-4">
          <div className="relative">
            <textarea
              ref={textareaRef}
              value={challenge}
              onChange={(e) => setChallenge(e.target.value)}
              placeholder="e.g. Revenue growth slowed in Europe despite increased ad spend. Enterprise deals are closing but smaller accounts are churning at 8% monthly…"
              rows={6}
              className="w-full rounded-xl border border-white/10 bg-white/[0.03] text-white placeholder-white/20 p-4 text-sm leading-relaxed resize-none focus:outline-none focus:border-blue-500/50 focus:ring-1 focus:ring-blue-500/20 transition-all"
              maxLength={2000}
            />
            <div className="absolute bottom-3 right-3 text-[10px] text-white/20">
              {charCount}/2000
            </div>
          </div>

          {error && (
            <div className="rounded-lg border border-red-500/30 bg-red-500/10 px-4 py-3 text-sm text-red-300">
              {error}
            </div>
          )}

          <button
            type="submit"
            disabled={!isValid || loading}
            className="w-full flex items-center justify-center gap-2 px-6 py-3.5 rounded-xl bg-blue-600 hover:bg-blue-500 disabled:opacity-40 disabled:cursor-not-allowed font-semibold text-white transition-all text-sm"
          >
            {loading ? (
              <>
                <Spinner className="w-4 h-4" />
                Starting analysis…
              </>
            ) : (
              <>
                Analyze with AI
                <ArrowRight className="w-4 h-4" />
              </>
            )}
          </button>
        </form>

        {/* Example challenges */}
        <div className="mt-10 w-full">
          <div className="flex items-center gap-2 mb-4">
            <Lightbulb className="w-3.5 h-3.5 text-white/30" />
            <span className="text-xs text-white/30 uppercase tracking-widest">Try an example</span>
          </div>
          <div className="space-y-2">
            {EXAMPLES.map((ex) => (
              <button
                key={ex}
                onClick={() => setChallenge(ex)}
                className="w-full text-left px-4 py-2.5 rounded-lg border border-white/5 bg-white/[0.02] hover:bg-white/[0.05] hover:border-white/10 text-white/50 hover:text-white/70 text-xs leading-relaxed transition-all"
              >
                "{ex}"
              </button>
            ))}
          </div>
        </div>
      </div>
    </main>
  );
}

export default function WorkspacePage() {
  return (
    <Suspense>
      <WorkspaceContent />
    </Suspense>
  );
}
