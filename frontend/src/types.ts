export interface Stats {
  total_analyses: number;
  avg_processing: string;
  success_rate: string;
}

export interface AnalysisSummary {
  id: number;
  transcription: string;
  clinical_json: Record<string, unknown> | null;
  summary_pt?: string | null;
  summary_en?: string | null;
  created_at?: string | null;
  processing_ms?: number | null;
  confidence?: number | null;
}

export interface ApiError {
  detail?: string | { message?: string; code?: string };
}
