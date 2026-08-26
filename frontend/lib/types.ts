export type AnalysisStatus = "pending" | "running" | "completed" | "failed";

export interface Analysis {
  id: string;
  challenge: string;
  domain?: string | null;
  status: AnalysisStatus | string;
  business_area?: string | null;
  problem_type?: string | null;
  urgency?: string | null;
  selected_agents?: string[] | null;
  agent_results?: Record<string, unknown> | null;
  root_causes?: string[] | null;
  insights?: string[] | null;
  recommendations?: string[] | null;
  experiments?: string[] | null;
  executive_summary?: string | null;
  progress?: Array<Record<string, unknown>> | null;
  error?: string | null;
  created_at?: string;
  updated_at?: string;
}

export interface CanvasNodeData {
  label: string;
  description?: string;
  items?: string[];
  [key: string]: unknown;
}
