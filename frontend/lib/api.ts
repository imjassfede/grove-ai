const API_BASE = "";
import type { Analysis } from "./types";

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

export async function submitChallenge(challenge: string): Promise<Analysis> {
  const response = await fetch(`${API_BASE}/api/v1/analyses`, {
    ...REQUEST_OPTIONS,
    method: "POST",
    body: JSON.stringify({ challenge }),
  });
  if (!response.ok) throw new Error((await response.json().catch(() => null))?.detail ?? "Unable to start analysis");
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
  if (!response.ok) throw new Error((await response.json().catch(() => null))?.detail ?? "Unable to analyze this company");
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
  if (!response.ok) throw new Error((await response.json().catch(() => null))?.detail ?? "Unable to load analysis");
  return response.json();
}
