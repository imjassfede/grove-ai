import Link from "next/link";
import { BarChart3, Brain, GitBranch, Lightbulb, Search, Target, TrendingUp, Zap } from "lucide-react";

const EXAMPLES = [
  "Why is our enterprise churn increasing despite product improvements?",
  "Revenue growth slowed down in Europe — what's driving it?",
  "Why is activation dropping after our latest onboarding update?",
  "Where should we invest our growth budget next quarter?",
];

const HOW_IT_WORKS = [
  { icon: Search, step: "01", title: "Enter your company", desc: "Start with your company website. Grove builds an initial view from your public business signals." },
  { icon: Brain, step: "02", title: "Grove investigates", desc: "Relevant specialist perspectives are selected to investigate your market, customers, competitors and business." },
  { icon: GitBranch, step: "03", title: "Signals come together", desc: "The different analyses are connected and synthesised into a single strategic view." },
  { icon: Lightbulb, step: "04", title: "See where to grow next", desc: "Get prioritised opportunities, recommendations and experiments you can act on." },
];

const AGENT_CHIPS = [
  "Market Intelligence",
  "Customer Intelligence",
  "Competitive Intelligence",
  "Revenue Intelligence",
  "Experiment Design",
  "GTM Strategy",
];

export default function LandingPage() {
  return (
    <main className="min-h-screen bg-[#050507] text-white overflow-x-hidden">
      <nav className="fixed top-0 inset-x-0 z-50 border-b border-white/5 bg-[#050507]/80 backdrop-blur-md">
        <div className="max-w-6xl mx-auto px-6 h-14 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <TrendingUp className="w-5 h-5 text-blue-500" />
            <span className="font-bold text-white tracking-tight">Grove</span>
          </div>
          <Link href="/workspace" className="text-sm font-medium px-4 py-1.5 rounded-lg bg-blue-600 hover:bg-blue-500 transition-colors">
            Try Grove →
          </Link>
        </div>
      </nav>

      <section className="pt-40 pb-28 px-6 text-center max-w-4xl mx-auto">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-blue-500/30 bg-blue-500/10 text-blue-300 text-xs font-medium mb-8">
          <Zap className="w-3 h-3" />
          Free company analysis · 5 credits
        </div>

        <h1 className="text-5xl sm:text-6xl font-bold leading-[1.05] mb-6 tracking-tight">
          Find where to
          <br />
          <span className="bg-gradient-to-r from-blue-400 to-violet-400 bg-clip-text text-transparent">grow next.</span>
        </h1>

        <p className="text-lg text-white/50 max-w-2xl mx-auto mb-10 leading-relaxed">
          Enter your company website and uncover the opportunities worth pursuing next — across your market, customers, competitors and growth strategy.
        </p>

        <Link href="/workspace" className="inline-flex items-center gap-2 px-8 py-3.5 rounded-xl bg-blue-600 hover:bg-blue-500 font-semibold text-white transition-all hover:shadow-[0_0_30px_rgba(59,130,246,0.4)] text-base">
          <Target className="w-4 h-4" />
          Analyze my company
        </Link>
        <p className="mt-3 text-xs text-white/30">No credit card required · Start with 5 free credits</p>

        <div className="mt-12 space-y-2 text-left max-w-2xl mx-auto">
          <p className="text-xs text-white/30 uppercase tracking-widest mb-4 text-center">Or explore a business challenge</p>
          {EXAMPLES.map((ex) => (
            <Link key={ex} href={`/workspace?q=${encodeURIComponent(ex)}`} className="block px-4 py-3 rounded-lg border border-white/5 bg-white/[0.02] hover:bg-white/[0.05] hover:border-white/10 text-white/60 hover:text-white/80 text-sm transition-all leading-relaxed">
              "{ex}"
            </Link>
          ))}
        </div>
      </section>

      <section className="py-16 px-6 border-y border-white/5">
        <div className="max-w-3xl mx-auto text-center">
          <p className="text-xs text-white/30 uppercase tracking-widest mb-6">Look at your business from multiple perspectives</p>
          <div className="flex flex-wrap justify-center gap-2">
            {AGENT_CHIPS.map((label) => (
              <span key={label} className="px-3 py-1.5 rounded-full border border-white/10 bg-white/[0.03] text-xs font-medium text-white/50">
                {label}
              </span>
            ))}
          </div>
        </div>
      </section>

      <section className="py-24 px-6">
        <div className="max-w-5xl mx-auto">
          <h2 className="text-2xl font-bold text-center mb-14 text-white/90">From company domain to next move</h2>
          <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-6">
            {HOW_IT_WORKS.map(({ icon: Icon, step, title, desc }) => (
              <div key={step} className="rounded-xl border border-white/5 bg-white/[0.02] p-6 space-y-3">
                <div className="flex items-center justify-between">
                  <div className="w-9 h-9 rounded-lg bg-blue-500/10 flex items-center justify-center"><Icon className="w-4 h-4 text-blue-400" /></div>
                  <span className="text-2xl font-black text-white/10">{step}</span>
                </div>
                <h3 className="font-semibold text-white/90 text-sm">{title}</h3>
                <p className="text-white/40 text-xs leading-relaxed">{desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="py-20 px-6 border-t border-white/5">
        <div className="max-w-4xl mx-auto grid sm:grid-cols-3 gap-4 text-center">
          <div className="rounded-xl border border-white/5 bg-white/[0.02] p-6"><BarChart3 className="w-5 h-5 text-blue-400 mx-auto mb-3" /><p className="font-semibold text-sm">Find the signals</p><p className="text-xs text-white/35 mt-2">See what's changing across your business and market.</p></div>
          <div className="rounded-xl border border-white/5 bg-white/[0.02] p-6"><Target className="w-5 h-5 text-violet-400 mx-auto mb-3" /><p className="font-semibold text-sm">Prioritise opportunities</p><p className="text-xs text-white/35 mt-2">Separate interesting ideas from opportunities worth pursuing.</p></div>
          <div className="rounded-xl border border-white/5 bg-white/[0.02] p-6"><Lightbulb className="w-5 h-5 text-amber-400 mx-auto mb-3" /><p className="font-semibold text-sm">Decide what to do next</p><p className="text-xs text-white/35 mt-2">Turn insights into recommendations and experiments.</p></div>
        </div>
      </section>

      <section className="py-28 px-6 text-center">
        <div className="max-w-xl mx-auto">
          <h2 className="text-3xl font-bold mb-4">Where could your company grow next?</h2>
          <p className="text-white/40 mb-8 text-sm">Start with your website. Grove does the investigation.</p>
          <Link href="/workspace" className="inline-flex items-center gap-2 px-8 py-3.5 rounded-xl bg-blue-600 hover:bg-blue-500 font-semibold text-white transition-all hover:shadow-[0_0_30px_rgba(59,130,246,0.4)]">
            Analyze my company →
          </Link>
          <p className="mt-3 text-xs text-white/30">5 free credits · No credit card required</p>
        </div>
      </section>
    </main>
  );
}
