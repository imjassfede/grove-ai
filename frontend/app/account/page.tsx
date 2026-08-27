"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { ArrowRight, BarChart3, Check, LogOut, Settings, Target, UserRound } from "lucide-react";
import { getAnalyses, getProfile, logout, startDomainAnalysis, updateProfile } from "@/lib/api";
import type { Analysis, Profile } from "@/lib/types";

const INTERESTS = ["Market", "Customer", "Competitors", "Revenue", "Product", "GTM"];

export default function AccountPage() {
  const router = useRouter();
  const [profile, setProfile] = useState<Profile | null>(null);
  const [analyses, setAnalyses] = useState<Analysis[]>([]);
  const [editing, setEditing] = useState(false);
  const [saving, setSaving] = useState(false);
  const [domain, setDomain] = useState("");
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    Promise.all([getProfile(), getAnalyses()]).then(([p, a]) => {
      if (!p.onboarding_completed) { router.replace("/onboarding"); return; }
      setProfile(p); setAnalyses(a);
    }).catch(() => router.replace("/auth"));
  }, [router]);

  async function save() {
    if (!profile) return;
    setSaving(true); setError(null);
    try { setProfile(await updateProfile(profile)); setEditing(false); }
    catch (err) { setError(err instanceof Error ? err.message : "Unable to save"); }
    finally { setSaving(false); }
  }

  async function newAnalysis(e: React.FormEvent) {
    e.preventDefault();
    if (!domain.trim()) return;
    try { const analysis = await startDomainAnalysis(domain); router.push(`/workspace/${analysis.id}`); }
    catch (err) { setError(err instanceof Error ? err.message : "Unable to start analysis"); }
  }

  if (!profile) return <main className="min-h-screen bg-[#050507] text-white flex items-center justify-center text-sm text-white/40">Loading your Grove account…</main>;
  const fullName = [profile.first_name, profile.last_name].filter(Boolean).join(" ") || "Your account";

  return <main className="min-h-screen bg-[#050507] text-white">
    <nav className="h-14 border-b border-white/5 px-6 flex items-center justify-between"><Link href="/account" className="flex items-center gap-2"><span className="w-5 h-5 rounded-md bg-blue-500/20 text-blue-400 text-[10px] flex items-center justify-center">G</span><span className="font-semibold text-sm">Grove</span></Link><div className="flex items-center gap-4"><Link href="/account" className="text-xs text-white/70">Account</Link><button onClick={async () => { await logout(); router.replace("/auth"); }} className="inline-flex items-center gap-1.5 text-xs text-white/35 hover:text-white"><LogOut className="w-3.5 h-3.5" /> Log out</button></div></nav>
    <div className="max-w-6xl mx-auto px-6 py-10">
      <header className="flex flex-col sm:flex-row sm:items-end justify-between gap-5 mb-8"><div><p className="text-xs text-blue-400 uppercase tracking-widest mb-2">Personal Grove</p><h1 className="text-3xl font-bold tracking-tight">Welcome, {fullName}.</h1><p className="text-sm text-white/40 mt-2">Your growth workspace, preferences and analysis history.</p></div><div className="rounded-xl border border-white/10 bg-white/[0.025] px-4 py-3 min-w-36"><p className="text-[10px] uppercase tracking-widest text-white/30">Credits</p><p className="text-2xl font-bold mt-1">{profile.credits}</p></div></header>
      {error && <p className="mb-5 text-xs text-red-300">{error}</p>}
      <div className="grid lg:grid-cols-[1.35fr_.65fr] gap-6">
        <section className="rounded-2xl border border-white/10 bg-white/[0.02] p-5 sm:p-6">
          <div className="flex items-center justify-between mb-5"><div><h2 className="font-semibold">Start a new analysis</h2><p className="text-xs text-white/35 mt-1">Use your saved context as the starting point.</p></div><BarChart3 className="w-5 h-5 text-blue-400" /></div>
          <form onSubmit={newAnalysis} className="flex gap-2 p-1.5 rounded-xl border border-white/10 bg-white/[0.03]"><input value={domain} onChange={(e) => setDomain(e.target.value)} placeholder="yourcompany.com" className="min-w-0 flex-1 bg-transparent px-3 py-2.5 text-sm outline-none placeholder-white/20" /><button className="inline-flex items-center gap-2 px-4 py-2.5 rounded-lg bg-blue-600 hover:bg-blue-500 font-semibold text-sm">Analyze <ArrowRight className="w-4 h-4" /></button></form>
          <h3 className="text-xs font-semibold uppercase tracking-widest text-white/30 mt-8 mb-3">Recent analyses</h3>
          <div className="space-y-2">{analyses.length === 0 ? <p className="text-sm text-white/30 py-6">No analyses yet. Start your first one above.</p> : analyses.slice(0, 8).map((analysis) => <Link key={analysis.id} href={`/workspace/${analysis.id}`} className="flex items-center gap-3 rounded-lg border border-white/5 bg-white/[0.02] p-3 hover:bg-white/[0.04]"><div className="w-8 h-8 rounded-lg bg-blue-500/10 flex items-center justify-center"><Target className="w-4 h-4 text-blue-400" /></div><div className="min-w-0 flex-1"><p className="text-sm text-white/80 truncate">{analysis.domain || analysis.challenge}</p><p className="text-[11px] text-white/30">{analysis.status} {analysis.created_at ? `· ${new Date(analysis.created_at).toLocaleDateString()}` : ""}</p></div><ArrowRight className="w-4 h-4 text-white/20" /></Link>)}</div>
        </section>
        <section className="rounded-2xl border border-white/10 bg-white/[0.02] p-5 sm:p-6">
          <div className="flex items-center justify-between mb-5"><div><h2 className="font-semibold">Your profile</h2><p className="text-xs text-white/35 mt-1">Customize your Grove context.</p></div><button onClick={() => setEditing(!editing)} className="text-xs text-blue-400 hover:text-blue-300"><Settings className="w-4 h-4 inline mr-1" />{editing ? "Close" : "Edit"}</button></div>
          {editing ? <div className="space-y-3"><Field label="First name" value={profile.first_name ?? ""} onChange={(v) => setProfile({ ...profile, first_name: v })} /><Field label="Last name" value={profile.last_name ?? ""} onChange={(v) => setProfile({ ...profile, last_name: v })} /><Field label="Role" value={profile.role ?? ""} onChange={(v) => setProfile({ ...profile, role: v })} /><Field label="Company" value={profile.company ?? ""} onChange={(v) => setProfile({ ...profile, company: v })} /><Field label="Website" value={profile.website ?? ""} onChange={(v) => setProfile({ ...profile, website: v })} /><p className="text-[10px] text-white/30 pt-2">Focus areas</p><div className="grid grid-cols-2 gap-2">{INTERESTS.map((interest) => <button type="button" key={interest} onClick={() => setProfile({ ...profile, interests: profile.interests.includes(interest) ? profile.interests.filter((x) => x !== interest) : [...profile.interests, interest] })} className={`text-left px-2.5 py-2 rounded-md border text-[11px] ${profile.interests.includes(interest) ? "border-blue-500/40 bg-blue-500/10 text-white" : "border-white/5 text-white/40"}`}>{profile.interests.includes(interest) && <Check className="w-3 h-3 inline mr-1" />}{interest}</button>)}</div><button disabled={saving} onClick={save} className="w-full mt-2 py-2.5 rounded-lg bg-blue-600 hover:bg-blue-500 disabled:opacity-40 text-sm font-semibold">{saving ? "Saving…" : "Save changes"}</button></div> : <div className="space-y-4"><Info label="Name" value={fullName} /><Info label="Email" value={profile.email} /><Info label="Role" value={profile.role || "Not set"} /><Info label="Company" value={profile.company || "Not set"} /><Info label="Website" value={profile.website || "Not set"} /><div><p className="text-[10px] uppercase tracking-widest text-white/25 mb-2">Focus areas</p><div className="flex flex-wrap gap-1.5">{profile.interests.length ? profile.interests.map((x) => <span key={x} className="px-2 py-1 rounded-md bg-white/5 text-[10px] text-white/50">{x}</span>) : <span className="text-xs text-white/30">None selected</span>}</div></div></div>}
        </section>
      </div>
    </div>
  </main>;
}

function Field({ label, value, onChange }: { label: string; value: string; onChange: (v: string) => void }) { return <label className="block"><span className="block text-[10px] uppercase tracking-widest text-white/25 mb-1.5">{label}</span><input value={value} onChange={(e) => onChange(e.target.value)} className="field" /></label>; }
function Info({ label, value }: { label: string; value: string }) { return <div><p className="text-[10px] uppercase tracking-widest text-white/25">{label}</p><p className="text-sm text-white/70 mt-1 break-words">{value}</p></div>; }
