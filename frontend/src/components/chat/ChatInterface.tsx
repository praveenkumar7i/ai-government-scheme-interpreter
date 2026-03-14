"use client";

import { useMutation } from "@tanstack/react-query";
import { useState } from "react";

import type { AskResponse } from "../../services/api";
import { askQuestion } from "../../services/api";
import CitationViewer from "../citations/CitationViewer";
import EligibilityResultCard from "../eligibility/EligibilityResultCard";
import LanguageSelector from "../language/LanguageSelector";

type Message = {
  role: "user" | "assistant";
  content: string;
  response?: AskResponse;
};

export default function ChatInterface() {
  const [documentId, setDocumentId] = useState("");
  const [question, setQuestion] = useState("Am I eligible if my income is 4 lakh?");
  const [language, setLanguage] = useState("en");
  const [messages, setMessages] = useState<Message[]>([]);

  const askMutation = useMutation({
    mutationFn: askQuestion,
    onSuccess: (response) => {
      const translated = response.translations[language] || response.answer;
      setMessages((prev) => [
        ...prev,
        { role: "user", content: question },
        { role: "assistant", content: translated, response },
      ]);
    },
  });

  const submitQuestion = () => {
    if (!documentId.trim() || !question.trim()) return;

    askMutation.mutate({
      document_id: documentId,
      question,
      preferred_language: language,
      target_languages: ["hi", "kn", "ta", "te"],
    });
  };

  return (
    <main className="mx-auto grid max-w-5xl grid-cols-1 gap-6 p-8 md:grid-cols-3">
      <section className="md:col-span-1 space-y-3">
        <h2 className="text-2xl font-semibold">Eligibility Chat</h2>
        <input
          className="w-full rounded border border-slate-300 p-2"
          placeholder="Document ID"
          value={documentId}
          onChange={(e) => setDocumentId(e.target.value)}
        />
        <LanguageSelector value={language} onChange={setLanguage} />
        <textarea
          className="min-h-28 w-full rounded border border-slate-300 p-2"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
        />
        <button className="rounded bg-emerald-600 px-4 py-2 text-white disabled:opacity-50" onClick={submitQuestion} disabled={askMutation.isPending}>
          {askMutation.isPending ? "Asking..." : "Ask"}
        </button>
      </section>

      <section className="md:col-span-2 space-y-4">
        <div className="rounded-lg border border-slate-200 bg-white p-4">
          <h3 className="mb-3 text-lg font-semibold">Conversation History</h3>
          <div className="space-y-3">
            {messages.length === 0 ? <p className="text-sm text-slate-500">No conversation yet.</p> : null}
            {messages.map((message, idx) => (
              <div
                key={idx}
                className={`rounded-lg px-3 py-2 text-sm ${
                  message.role === "user" ? "bg-slate-900 text-white" : "bg-slate-100 text-slate-800"
                }`}
              >
                <p className="font-semibold">{message.role === "user" ? "You" : "Assistant"}</p>
                <p>{message.content}</p>
                {message.response ? (
                  <div className="mt-3 space-y-3">
                    <EligibilityResultCard
                      eligibility={message.response.eligibility}
                      confidence={message.response.confidence}
                      reasoning={message.response.eligibility_reasoning}
                    />
                    <CitationViewer citations={message.response.citations} />
                  </div>
                ) : null}
              </div>
            ))}
          </div>
        </div>
      </section>
    </main>
  );
}
