"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { ArrowRight, Check, Globe, Target, UserRound } from "lucide-react";
import { getProfile, updateProfile } from "@/lib/api";

const GOALS = ["Find growth opportunities", "Understand competitors", "Improve GTM", "Increase revenue", "Validate a new product", "Understand my market"];
const INTERESTS = ["Market", "Customer", "Competitors", "Revenue", "Product", "GTM"];

export default function OnboardingPage() {
  const router = useRouter();
  const [step, setStep] = useState(1);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [role, setRole] = useState("");
  const [company, setCompany] = useState("");
  const [website, setWebsite] = useState("");
  const [goals, setGoals] = useState<string[]>([]);
  const [interests, setInterests] = useState<string[]>([]);

  useEffect(() => {
    getProfile().then((profile) => {
      if (profile.onboarding_completed) { router.replace("/account"); return; }
      setFirstName(profile.first_name ?? ""); setLastName(profile.last_name ?? ""); setRole(profile.role ?? "");
      setCompany(profile.company ?? ""); setWebsite(profile.website ?? ""); setGoals(profile.goals ?? []); setInterests(profile.interests ?? []);
      setLoading(false);
    }).catch(() => router.replace("/auth"));
  }, [router]);

  function toggle(value: string, current: string[], setter: (v: string[]) => void) {
    setter(current.includes(value) ? current.filter((x) => x !== value) : [...current, value]);
  }

  async function finish() {
    setSaving(true); setError(null);
    try {
      await updateProfile({ first_name: firstName, last_name: lastName, role, company, website, goals, interests, onboarding_completed: true });
      router.replace("/account");
    } catch (err) { setError(err instanceof Error ? err.message : "Unable to save your profile"); setSaving(false); }
  }

  if (loading) return <main className="min-h-screen bg-[#050507] text-white flex items-center justify-center text-sm text-white/40">Loading your profile…</main>;

  return <main className="min-h-screen bg-[#050507] text-white">
    <nav className="h-14 border-b border-white/5 px-6 flex items-center gap-2"><TrendingLogo /><span className="font-semibold text-sm">Grove</span></nav>
    <div className="max-w-2xl mx-auto px-6 py-12 sm:py-16">
      <div className="mb-10"><div className="flex items-center justify-between mb-4"><span className="text-xs text-white/35">Set up your Grove profile</span><span className="text-xs text-white/35">{step} / 3</span></div><div className="h-1 rounded-full bg-white/5 overflow-hidden"><div className="h-full bg-blue-500 transition-all" style={{ width: `${(step / 3) * 100}%` }} /></div></div>
      {step === 1 && <section><div className="w-11 h-11 rounded-xl bg-blue-500/10 border border-blue-500/20 flex items-center justify-center mb-5"><UserRound className="w-5 h-5 text-blue-400" /></div><h1 className="text-3xl font-bold tracking-tight">Tell us about you.</h1><p className="text-sm text-white/40 mt-2 mb-8">Grove uses this to make your analyses more relevant.</p><div className="grid sm:grid-cols-2 gap-4"><Field label="First name" value={firstName} onChange={setFirstName} placeholder="Jasmin" /><Field label="Last name" value={lastName} onChange={setLastName} placeholder="Fedele" /><Field label="Role" value={role} onChange={setRole} placeholder="e.g. Founder, Product Manager" /><Field label="Company" value={company} onChange={setCompany} placeholder="Your company" /></div><button onClick={() => setStep(2)} className="mt-8 inline-flex items-center gap-2 px-5 py-3 rounded-lg bg-blue-600 hover:bg-blue-500 font-semibold text-sm">Continue <ArrowRight className="w-4 h-4" /></button></section>}
      {step === 2 && <section><div className="w-11 h-11 rounded-xl bg-blue-500/10 border border-blue-500/20 flex items-center justify-center mb-5"><Globe className="w-5 h-5 text-blue-400" /></div><h1 className="text-3xl font-bold tracking-tight">What are you working on?</h1><p className="text-sm text-white/40 mt-2 mb-8">This becomes the context behind your Grove workspace.</p><Field label="Company website" value={website} onChange={setWebsite} placeholder="yourcompany.com" /><h2 className="text-xs font-semibold uppercase tracking-widest text-white/35 mt-8 mb-3">Your main goals</h2><div className="grid sm:grid-cols-2 gap-2">{GOALS.map((goal) => <Choice key={goal} selected={goals.includes(goal)} onClick={() => toggle(goal, goals, setGoals)}>{goal}</Choice>)}</div><div className="flex gap-3 mt-8"><button onClick={() => setStep(1)} className="px-5 py-3 rounded-lg border border-white/10 text-sm text-white/50 hover:text-white">Back</button><button onClick={() => setStep(3)} className="inline-flex items-center gap-2 px-5 py-3 rounded-lg bg-blue-600 hover:bg-blue-500 font-semibold text-sm">Continue <ArrowRight className="w-4 h-4" /></button></div></section>}
      {step === 3 && <section><div className="w-11 h-11 rounded-xl bg-blue-500/10 border border-blue-500/20 flex items-center justify-center mb-5"><Target className="w-5 h-5 text-blue-400" /></div><h1 className="text-3xl font-bold tracking-tight">Choose what Grove should watch.</h1><p className="text-sm text-white/40 mt-2 mb-8">You can change these preferences later from your account.</p><div className="grid sm:grid-cols-2 gap-2">{INTERESTS.map((interest) => <Choice key={interest} selected={interests.includes(interest)} onClick={() => toggle(interest, interests, setInterests)}>{interest}</Choice>)}</div>{error && <p className="text-xs text-red-300 mt-4">{error}</p>}<div className="flex gap-3 mt-8"><button onClick={() => setStep(2)} className="px-5 py-3 rounded-lg border border-white/10 text-sm text-white/50 hover:text-white">Back</button><button disabled={saving} onClick={finish} className="inline-flex items-center gap-2 px-5 py-3 rounded-lg bg-blue-600 hover:bg-blue-500 disabled:opacity-40 font-semibold text-sm">{saving ? "Saving…" : "Enter my Grove account"} <ArrowRight className="w-4 h-4" /></button></div></section>}
    </div>
  </main>;
}

function Field({ label, value, onChange, placeholder }: { label: string; value: string; onChange: (v: string) => void; placeholder: string }) { return <label className="block"><span className="block text-xs font-medium text-white/50 mb-2">{label}</span><input value={value} onChange={(e) => onChange(e.target.value)} placeholder={placeholder} className="field" /></label>; }
function Choice({ selected, onClick, children }: { selected: boolean; onClick: () => void; children: React.ReactNode }) { return <button type="button" onClick={onClick} className={`flex items-center gap-3 p-3 rounded-lg border text-left text-sm transition-colors ${selected ? "border-blue-500/50 bg-blue-500/10 text-white" : "border-white/8 bg-white/[0.02] text-white/55 hover:text-white"}`}><span className={`w-4 h-4 rounded border flex items-center justify-center ${selected ? "border-blue-400 bg-blue-500" : "border-white/20"}`}>{selected && <Check className="w-3 h-3 text-white" />}</span>{children}</button>; }
function TrendingLogo() { return <div className="w-4 h-4 rounded-md bg-blue-500/20 flex items-center justify-center"><span className="text-[9px] text-blue-400">G</span></div>; }
