"use client";

import Link from "next/link";
import { FormEvent, useState } from "react";
import { ArrowRight, Eye, EyeOff, TrendingUp } from "lucide-react";
import { trackEvent } from "@/lib/api";

const API_BASE = (process.env.NEXT_PUBLIC_API_URL ?? "https://grove-api-u1xv.onrender.com").replace(/\/$/, "");

export default function AuthPage() {
  const [mode, setMode] = useState<"signup" | "login">("signup");
  const [email, setEmail] = useState(""); const [password, setPassword] = useState("");
  const [firstName, setFirstName] = useState(""); const [lastName, setLastName] = useState("");
  const [marketingConsent, setMarketingConsent] = useState(false); const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false); const [error, setError] = useState<string | null>(null);

  async function submit(e: FormEvent) {
    e.preventDefault(); setLoading(true); setError(null);
    try {
      await trackEvent(mode === "signup" ? "signup_started" : "login_started");
      const response = await fetch(`${API_BASE}/api/v1/auth/${mode}`, { method: "POST", credentials: "include", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ email, password, ...(mode === "signup" ? { first_name: firstName, last_name: lastName, marketing_consent: marketingConsent, acquisition_source: typeof window !== "undefined" ? document.referrer.slice(0, 120) || "direct" : "direct" } : {}) }) });
      const body = await response.json().catch(() => null);
      if (!response.ok) throw new Error(body?.detail ?? "Unable to authenticate");
      window.location.href = body?.claimed_analysis_id ? `/workspace/${body.claimed_analysis_id}` : "/workspace";
    } catch (err) { setError(err instanceof Error ? err.message : "Something went wrong"); setLoading(false); }
  }

  return <main className="min-h-screen bg-[#050507] text-white flex flex-col">
    <nav className="h-14 border-b border-white/5 px-6 flex items-center"><Link href="/" className="flex items-center gap-2 text-white/70 hover:text-white"><TrendingUp className="w-4 h-4 text-blue-500" /><span className="font-semibold text-sm">Grove</span></Link></nav>
    <div className="flex-1 flex items-center justify-center px-6 py-16"><div className="w-full max-w-md">
      <div className="text-center mb-8"><h1 className="text-3xl font-bold tracking-tight">{mode === "signup" ? "Start finding where to grow next." : "Welcome back."}</h1><p className="text-sm text-white/40 mt-3">{mode === "signup" ? "Create your free Grove workspace." : "Continue your Grove analysis."}</p></div>
      <div className="rounded-2xl border border-white/10 bg-white/[0.025] p-6 sm:p-8">
        <div className="grid grid-cols-2 p-1 rounded-lg bg-white/[0.04] mb-6"><button type="button" onClick={() => { setMode("signup"); setError(null); }} className={`py-2 text-xs font-semibold rounded-md ${mode === "signup" ? "bg-white/10 text-white" : "text-white/35"}`}>Sign up</button><button type="button" onClick={() => { setMode("login"); setError(null); }} className={`py-2 text-xs font-semibold rounded-md ${mode === "login" ? "bg-white/10 text-white" : "text-white/35"}`}>Log in</button></div>
        <form onSubmit={submit} className="space-y-4">
          {mode === "signup" && <div className="grid grid-cols-2 gap-3"><input value={firstName} onChange={e => setFirstName(e.target.value)} placeholder="First name" className="field" /><input value={lastName} onChange={e => setLastName(e.target.value)} placeholder="Last name" className="field" /></div>}
          <input required type="email" value={email} onChange={e => setEmail(e.target.value)} placeholder="Work email" className="field" />
          <div className="relative"><input required minLength={8} type={showPassword ? "text" : "password"} value={password} onChange={e => setPassword(e.target.value)} placeholder="Password (8+ characters)" className="field pr-10" /><button type="button" onClick={() => setShowPassword(!showPassword)} className="absolute right-3 top-1/2 -translate-y-1/2 text-white/30">{showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}</button></div>
          {mode === "signup" && <label className="flex gap-2 items-start text-[11px] leading-relaxed text-white/35"><input type="checkbox" checked={marketingConsent} onChange={e => setMarketingConsent(e.target.checked)} className="mt-0.5 accent-blue-600" />I want to receive Grove product updates, insights and occasional growth resources by email. I can unsubscribe at any time.</label>}
          {error && <p className="text-xs text-red-300">{error}</p>}
          <button disabled={loading} className="w-full py-3 rounded-lg bg-blue-600 hover:bg-blue-500 disabled:opacity-40 font-semibold text-sm flex items-center justify-center gap-2">{loading ? "Please wait…" : mode === "signup" ? <>Create free workspace <ArrowRight className="w-4 h-4" /></> : <>Log in <ArrowRight className="w-4 h-4" /></>}</button>
        </form>
        {mode === "signup" && <p className="text-[10px] text-white/25 text-center mt-4 leading-relaxed">Your free workspace starts with 5 Grove credits. Marketing emails are optional.</p>}
      </div>
    </div></div>
    <style jsx>{`.field{width:100%;border:1px solid rgba(255,255,255,.08);background:rgba(255,255,255,.025);border-radius:.5rem;padding:.7rem .8rem;font-size:.8rem;outline:none;color:white}.field::placeholder{color:rgba(255,255,255,.2)}.field:focus{border-color:rgba(59,130,246,.45)}`}</style>
  </main>;
}
