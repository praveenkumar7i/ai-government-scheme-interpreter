"use client";

import { useState } from "react";

type Props = {
  onFileSelect: (file: File) => void;
  isLoading: boolean;
};

export default function PdfUploader({ onFileSelect, isLoading }: Props) {
  const [isDragActive, setIsDragActive] = useState(false);
  const [fileName, setFileName] = useState("");

  const selectFile = (file: File | null) => {
    if (!file) return;
    setFileName(file.name);
    onFileSelect(file);
  };

  return (
    <div
      className={`rounded-lg border-2 border-dashed p-6 text-center transition ${
        isDragActive ? "border-blue-600 bg-blue-50" : "border-slate-300 bg-white"
      }`}
      onDragOver={(e) => {
        e.preventDefault();
        setIsDragActive(true);
      }}
      onDragLeave={() => setIsDragActive(false)}
      onDrop={(e) => {
        e.preventDefault();
        setIsDragActive(false);
        selectFile(e.dataTransfer.files?.[0] ?? null);
      }}
    >
      <p className="mb-3 text-sm text-slate-600">Drag & drop a PDF file here</p>
      <input
        type="file"
        accept="application/pdf"
        id="pdf-uploader-input"
        className="hidden"
        onChange={(e) => selectFile(e.target.files?.[0] ?? null)}
      />
      <label htmlFor="pdf-uploader-input" className="inline-block cursor-pointer rounded bg-blue-600 px-4 py-2 text-white">
        Choose PDF
      </label>
      {isLoading && <p className="mt-3 text-sm text-blue-700">Uploading and processing...</p>}
      {!!fileName && <p className="mt-3 text-sm text-slate-700">Selected: {fileName}</p>}
    </div>
  );
}
