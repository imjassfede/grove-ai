export type AnalysisStatus = "pending" | "running" | "classifying" | "planning" | "analyzing" | "synthesizing" | "complete" | "error";
export interface RootCause { cause: string; evidence: string; impact: string; }
export interface Recommendation { action: string; priority: string; effort: string; impact: string; owner: string; timeline: string; }
export interface Experiment { hypothesis: string; measurement: string; timeline: string; ice_score: number; }
export interface Analysis {
  id: string; challenge: string; domain?: string | null; status: AnalysisStatus | string;
  business_area?: string | null; problem_type?: string | null; urgency?: string | null;
  selected_agents?: string[] | null; agent_results?: Record<string, unknown> | null;
  root_causes?: RootCause[] | null; insights?: string[] | null;
  recommendations?: Recommendation[] | null; experiments?: Experiment[] | null;
  executive_summary?: string | null; progress?: string[] | null; error?: string | null;
  created_at?: string; updated_at?: string;
}
export interface Profile {
  id: string;
  email: string;
  first_name?: string | null;
  last_name?: string | null;
  credits: number;
  role?: string | null;
  company?: string | null;
  website?: string | null;
  goals: string[];
  interests: string[];
  onboarding_completed: boolean;
}
export interface CanvasNodeData { label: string; description?: string; items?: string[]; [key: string]: unknown; }
