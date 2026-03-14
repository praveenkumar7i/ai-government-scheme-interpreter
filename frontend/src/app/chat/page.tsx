"use client";

import { useState } from "react";
import { askQuestion } from "../../services/api";

export default function ChatPage() {
  const [documentId, setDocumentId] = useState("");
  const [question, setQuestion] = useState("Am I eligible if my income is 4 lakh?");
  const [answer, setAnswer] = useState("");

  const onAsk = async () => {
    const res = await askQuestion({
      document_id: documentId,
      question,
      preferred_language: "en",
      target_languages: ["hi", "kn", "ta", "te"],
    });
    setAnswer(res.answer);
  };

  return (
    <main className="mx-auto max-w-2xl p-8 space-y-4">
      <h2 className="text-2xl font-semibold">Eligibility Chat</h2>
      <input className="w-full rounded border p-2" placeholder="Document ID" value={documentId} onChange={(e) => setDocumentId(e.target.value)} />
      <textarea className="w-full rounded border p-2" value={question} onChange={(e) => setQuestion(e.target.value)} />
      <button className="rounded bg-emerald-600 px-4 py-2 text-white" onClick={onAsk}>Ask</button>
      {answer && <div className="rounded border bg-white p-4"><h3 className="font-semibold">Answer</h3><p>{answer}</p></div>}
    </main>
  );
}
