"use client";

import { useMutation } from "@tanstack/react-query";
import { useState } from "react";

import PdfUploader from "../../components/upload/PdfUploader";
import { uploadPdf } from "../../services/api";

export default function UploadPage() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [documentId, setDocumentId] = useState<string>("");

  const uploadMutation = useMutation({
    mutationFn: (file: File) => uploadPdf(file, "PMAY", 2024, "Karnataka"),
    onSuccess: (response) => setDocumentId(response.document_id),
  });

  return (
    <main className="mx-auto max-w-2xl space-y-4 p-8">
      <h2 className="text-2xl font-semibold">Upload Scheme PDF</h2>
      <PdfUploader onFileSelect={setSelectedFile} isLoading={uploadMutation.isPending} />
      <button
        onClick={() => selectedFile && uploadMutation.mutate(selectedFile)}
        disabled={!selectedFile || uploadMutation.isPending}
        className="rounded bg-blue-600 px-4 py-2 text-white disabled:opacity-50"
      >
        {uploadMutation.isPending ? "Uploading..." : "Upload PDF"}
      </button>

      {documentId ? <p className="text-sm">Document ID: {documentId}</p> : null}
      {uploadMutation.isError ? <p className="text-sm text-red-600">Upload failed. Please try again.</p> : null}
    </main>
  );
}
