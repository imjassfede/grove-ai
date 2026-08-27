const API_BASE = (process.env.NEXT_PUBLIC_API_URL ?? "https://grove-api-u1xv.onrender.com").replace(/\/$/, "");
import type { Analysis, Profile } from "./types";

const REQUEST_OPTIONS = {
  headers: { "Content-Type": "application/json" },
  credentials: "include" as RequestCredentials,
};

export async function trackEvent(eventName: string, properties: Record<string, unknown> = {}) {
  const anonymousId = typeof window !== "undefined" ? getAnonymousId() : undefined;
  try {
    await fetch(`${API_BASE}/api/v1/events`, {
      ...REQUEST_OPTIONS,
      method: "POST",
      body: JSON.stringify({ event_name: eventName, anonymous_id: anonymousId, properties }),
      keepalive: true,
    });
  } catch {}
}

function getAnonymousId() {
  const key = "grove_anonymous_id";
  const existing = localStorage.getItem(key);
  if (existing) return existing;
  const id = crypto.randomUUID();
  localStorage.setItem(key, id);
  return id;
}

async function parseError(response: Response, fallback: string) {
  const body = await response.json().catch(() => null);
  return body?.detail ?? fallback;
}

export async function getMe() {
  const response = await fetch(`${API_BASE}/api/v1/auth/me`, { ...REQUEST_OPTIONS, cache: "no-store" });
  if (!response.ok) throw new Error(await parseError(response, "Not authenticated"));
  return response.json() as Promise<{ id: string; email: string; first_name?: string | null; last_name?: string | null; credits: number }>;
}

export async function getProfile(): Promise<Profile> {
  const response = await fetch(`${API_BASE}/api/v1/profile`, { ...REQUEST_OPTIONS, cache: "no-store" });
  if (!response.ok) throw new Error(await parseError(response, "Unable to load profile"));
  return response.json();
}

export async function updateProfile(payload: Partial<Profile>): Promise<Profile> {
  const response = await fetch(`${API_BASE}/api/v1/profile`, {
    ...REQUEST_OPTIONS,
    method: "PATCH",
    body: JSON.stringify(payload),
  });
  if (!response.ok) throw new Error(await parseError(response, "Unable to save profile"));
  return response.json();
}

export async function getAnalyses(): Promise<Analysis[]> {
  const response = await fetch(`${API_BASE}/api/v1/analyses`, { ...REQUEST_OPTIONS, cache: "no-store" });
  if (!response.ok) throw new Error(await parseError(response, "Unable to load analyses"));
  const body = await response.json();
  return body.analyses ?? [];
}

export async function logout() {
  await fetch(`${API_BASE}/api/v1/auth/logout`, { ...REQUEST_OPTIONS, method: "POST" });
}

export async function submitChallenge(challenge: string): Promise<Analysis> {
  const response = await fetch(`${API_BASE}/api/v1/analyses`, {
    ...REQUEST_OPTIONS,
    method: "POST",
    body: JSON.stringify({ challenge }),
  });
  if (!response.ok) throw new Error(await parseError(response, "Unable to start analysis"));
  return response.json();
}

export async function startDomainAnalysis(domain: string): Promise<Analysis> {
  const normalized = domain.trim().replace(/^https?:\/\//, "").replace(/^www\./, "").replace(/\/.*$/, "");
  await trackEvent("domain_submitted", { domain: normalized });
  const response = await fetch(`${API_BASE}/api/v1/analyses`, {
    ...REQUEST_OPTIONS,
    method: "POST",
    body: JSON.stringify({
      challenge: `Analyze ${normalized} and identify the company's strongest next growth opportunities.`,
      domain: normalized,
    }),
  });
  if (!response.ok) throw new Error(await parseError(response, "Unable to analyze this company"));
  const analysis = await response.json();
  await trackEvent("analysis_started", { analysis_id: analysis.id, domain: normalized });
  return analysis;
}

export async function getAnalysis(id: string): Promise<Analysis> {
  const response = await fetch(`${API_BASE}/api/v1/analyses/${encodeURIComponent(id)}`, {
    ...REQUEST_OPTIONS,
    method: "GET",
    cache: "no-store",
  });
  if (!response.ok) throw new Error(await parseError(response, "Unable to load analysis"));
  return response.json();
}
