import axios from "axios";

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
  return data;
}

export async function askQuestion(payload: {
  document_id: string;
  question: string;
  preferred_language: string;
  target_languages: string[];
}) {
  const { data } = await api.post("/query/ask", payload);
  return data;
}
