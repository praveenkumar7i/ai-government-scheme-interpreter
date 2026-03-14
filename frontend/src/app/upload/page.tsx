"use client";

import { useState } from "react";
import { uploadPdf } from "../../services/api";

export default function UploadPage() {
  const [file, setFile] = useState<File | null>(null);
  const [documentId, setDocumentId] = useState<string>("");

  const onUpload = async () => {
    if (!file) return;
    const res = await uploadPdf(file, "PMAY", 2024, "Karnataka");
    setDocumentId(res.document_id);
  };

  return (
    <main className="mx-auto max-w-xl p-8 space-y-4">
      <h2 className="text-2xl font-semibold">Upload Scheme PDF</h2>
      <input type="file" accept="application/pdf" onChange={(e) => setFile(e.target.files?.[0] ?? null)} />
      <button onClick={onUpload} className="rounded bg-blue-600 px-4 py-2 text-white">Upload</button>
      {documentId && <p className="text-sm">Document ID: {documentId}</p>}
    </main>
  );
}
