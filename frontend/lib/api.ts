const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export type Analysis = {
  id: string;
  challenge: string;
  status: string;
};

export async function submitChallenge(challenge: string): Promise<Analysis> {
  const response = await fetch(`${API_BASE}/api/analyses`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ challenge }),
  });

  if (!response.ok) {
    const body = await response.json().catch(() => null);
    throw new Error(body?.detail ?? "Unable to start analysis");
  }

  return response.json();
}

export async function startDomainAnalysis(domain: string): Promise<Analysis> {
  const normalized = domain.trim().replace(/^https?:\/\//, "").replace(/\/.*$/, "");
  const response = await fetch(`${API_BASE}/api/analyses`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ challenge: `Analyze ${normalized} and identify the company's strongest next growth opportunities.` }),
  });

  if (!response.ok) {
    const body = await response.json().catch(() => null);
    throw new Error(body?.detail ?? "Unable to analyze this company");
  }

  return response.json();
}
