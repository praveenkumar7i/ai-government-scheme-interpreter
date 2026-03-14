import Link from "next/link";

export default function Home() {
  return (
    <main className="mx-auto max-w-3xl p-8 space-y-4">
      <h1 className="text-3xl font-bold">AI Government Scheme Interpreter</h1>
      <p>Upload scheme PDFs and ask eligibility questions.</p>
      <div className="space-x-4">
        <Link href="/upload" className="rounded bg-blue-600 px-4 py-2 text-white">Upload PDF</Link>
        <Link href="/chat" className="rounded bg-slate-800 px-4 py-2 text-white">Open Chat</Link>
      </div>
    </main>
  );
}
