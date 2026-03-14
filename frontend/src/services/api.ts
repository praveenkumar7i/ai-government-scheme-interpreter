import axios from "axios";

export type AskPayload = {
  document_id: string;
  question: string;
  preferred_language: string;
  target_languages: string[];
};

export type Citation = {
  page: number | null;
  section: string | null;
  snippet: string;
  overlap_score?: number;
};

export type AskResponse = {
  status: string;
  answer: string;
  eligibility: string;
  citations: Citation[];
  confidence: number;
  translations: Record<string, string>;
  eligibility_reasoning?: {
    extracted_signals?: Record<string, string | number | null>;
    rule_based_verdict?: string;
    reasons?: string[];
  };
};

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1",
});

export async function uploadPdf(file: File, scheme_name: string, scheme_year?: number, state?: string) {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("scheme_name", scheme_name);
  if (scheme_year) formData.append("scheme_year", String(scheme_year));
  if (state) formData.append("state", state);
  const { data } = await api.post("/documents/upload", formData);
  return data as { document_id: string; status: string };
}

export async function askQuestion(payload: AskPayload) {
  const { data } = await api.post("/query/ask", payload);
  return data as AskResponse;
}
