import Link from "next/link";
import {
  BarChart3,
  Brain,
  FlaskConical,
  GitBranch,
  Lightbulb,
  Target,
  TrendingUp,
  Zap,
} from "lucide-react";

const EXAMPLES = [
  "Why is our enterprise churn increasing despite product improvements?",
  "Revenue growth slowed down in Europe — what's driving it?",
  "Why is activation dropping after our latest onboarding update?",
  "Where should we invest our growth budget next quarter?",
  "Our pipeline is slowing — what's the root cause?",
];

const HOW_IT_WORKS = [
  {
    icon: Brain,
    step: "01",
    title: "Describe your challenge",
    desc: "Enter any business problem in plain language. No templates, no forms.",
  },
  {
    icon: GitBranch,
    step: "02",
    title: "AI diagnoses the problem",
    desc: "Our reasoning engine classifies the problem and dispatches specialist agents.",
  },
  {
    icon: BarChart3,
    step: "03",
    title: "Agents investigate in parallel",
    desc: "Market, customer, competitive, revenue, experiment, and GTM agents run simultaneously.",
  },
  {
    icon: Lightbulb,
    step: "04",
    title: "Receive structured intelligence",
    desc: "Root causes, insights, recommendations, and experiments on a visual Growth Canvas.",
  },
];

const AGENT_CHIPS = [
  { label: "Market Intelligence", color: "bg-blue-500/10 border-blue-500/30 text-blue-300" },
  { label: "Customer Intelligence", color: "bg-purple-500/10 border-purple-500/30 text-purple-300" },
  { label: "Competitive Intelligence", color: "bg-red-500/10 border-red-500/30 text-red-300" },
  { label: "Revenue Intelligence", color: "bg-green-500/10 border-green-500/30 text-green-300" },
  { label: "Experiment Design", color: "bg-amber-500/10 border-amber-500/30 text-amber-300" },
  { label: "GTM Strategy", color: "bg-cyan-500/10 border-cyan-500/30 text-cyan-300" },
];

export default function LandingPage() {
  return (
    <main className="min-h-screen bg-[#050507] text-white overflow-x-hidden">

      {/* Nav */}
      <nav className="fixed top-0 inset-x-0 z-50 border-b border-white/5 bg-[#050507]/80 backdrop-blur-md">
        <div className="max-w-6xl mx-auto px-6 h-14 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <TrendingUp className="w-5 h-5 text-blue-500" />
            <span className="font-bold text-white tracking-tight">Growth AI</span>
          </div>
          <Link
            href="/workspace"
            className="text-sm font-medium px-4 py-1.5 rounded-lg bg-blue-600 hover:bg-blue-500 transition-colors"
          >
            Start analyzing →
          </Link>
        </div>
      </nav>

      {/* Hero */}
      <section className="pt-40 pb-28 px-6 text-center max-w-4xl mx-auto">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-blue-500/30 bg-blue-500/10 text-blue-300 text-xs font-medium mb-8">
          <Zap className="w-3 h-3" />
          AI-Powered Growth Intelligence
        </div>

        <h1 className="text-5xl sm:text-6xl font-bold leading-[1.1] mb-6 tracking-tight">
          Turn business problems
          <br />
          into{" "}
          <span className="bg-gradient-to-r from-blue-400 to-violet-400 bg-clip-text text-transparent">
            strategic intelligence
          </span>
        </h1>

        <p className="text-lg text-white/50 max-w-2xl mx-auto mb-10 leading-relaxed">
          Describe any growth challenge. Our AI dispatches specialist agents — market,
          customer, competitive, revenue, and more — to diagnose root causes and
          deliver structured recommendations on a visual Growth Canvas.
        </p>

        <Link
          href="/workspace"
          className="inline-flex items-center gap-2 px-8 py-3.5 rounded-xl bg-blue-600 hover:bg-blue-500 font-semibold text-white transition-all hover:shadow-[0_0_30px_rgba(59,130,246,0.4)] text-base"
        >
          <Target className="w-4 h-4" />
          Submit your challenge
        </Link>

        {/* Example challenges */}
        <div className="mt-12 space-y-2 text-left max-w-2xl mx-auto">
          <p className="text-xs text-white/30 uppercase tracking-widest mb-4 text-center">Example challenges</p>
          {EXAMPLES.map((ex) => (
            <Link
              key={ex}
              href={`/workspace?q=${encodeURIComponent(ex)}`}
              className="block px-4 py-3 rounded-lg border border-white/5 bg-white/[0.02] hover:bg-white/[0.05] hover:border-white/10 text-white/60 hover:text-white/80 text-sm transition-all leading-relaxed"
            >
              "{ex}"
            </Link>
          ))}
        </div>
      </section>

      {/* Agent chips */}
      <section className="py-16 px-6 border-y border-white/5">
        <div className="max-w-3xl mx-auto text-center">
          <p className="text-xs text-white/30 uppercase tracking-widest mb-6">
            6 specialist intelligence agents working in parallel
          </p>
          <div className="flex flex-wrap justify-center gap-2">
            {AGENT_CHIPS.map((chip) => (
              <span
                key={chip.label}
                className={`px-3 py-1.5 rounded-full border text-xs font-medium ${chip.color}`}
              >
                {chip.label}
              </span>
            ))}
          </div>
        </div>
      </section>

      {/* How it works */}
      <section className="py-24 px-6">
        <div className="max-w-5xl mx-auto">
          <h2 className="text-2xl font-bold text-center mb-14 text-white/90">How it works</h2>
          <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-6">
            {HOW_IT_WORKS.map(({ icon: Icon, step, title, desc }) => (
              <div
                key={step}
                className="rounded-xl border border-white/5 bg-white/[0.02] p-6 space-y-3"
              >
                <div className="flex items-center justify-between">
                  <div className="w-9 h-9 rounded-lg bg-blue-500/10 flex items-center justify-center">
                    <Icon className="w-4 h-4 text-blue-400" />
                  </div>
                  <span className="text-2xl font-black text-white/10">{step}</span>
                </div>
                <h3 className="font-semibold text-white/90 text-sm">{title}</h3>
                <p className="text-white/40 text-xs leading-relaxed">{desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Output types */}
      <section className="py-16 px-6 border-t border-white/5">
        <div className="max-w-4xl mx-auto text-center">
          <p className="text-xs text-white/30 uppercase tracking-widest mb-8">Every analysis produces</p>
          <div className="flex flex-wrap justify-center gap-4">
            {[
              { label: "Root Cause Analysis", color: "text-red-400" },
              { label: "Strategic Insights", color: "text-purple-400" },
              { label: "Recommendations", color: "text-green-400" },
              { label: "Growth Experiments", color: "text-amber-400" },
              { label: "Priority Ranking", color: "text-blue-400" },
              { label: "Impact Estimation", color: "text-cyan-400" },
            ].map(({ label, color }) => (
              <div key={label} className="flex items-center gap-2 text-sm text-white/60">
                <span className={`text-base ${color}`}>◆</span>
                {label}
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-28 px-6 text-center">
        <div className="max-w-xl mx-auto">
          <FlaskConical className="w-8 h-8 text-blue-400 mx-auto mb-6 opacity-60" />
          <h2 className="text-3xl font-bold mb-4">Ready to solve your growth problem?</h2>
          <p className="text-white/40 mb-8 text-sm">
            No setup. No templates. Just describe your challenge.
          </p>
          <Link
            href="/workspace"
            className="inline-flex items-center gap-2 px-8 py-3.5 rounded-xl bg-blue-600 hover:bg-blue-500 font-semibold text-white transition-all hover:shadow-[0_0_30px_rgba(59,130,246,0.4)]"
          >
            Start your first analysis →
          </Link>
        </div>
      </section>
    </main>
  );
}
