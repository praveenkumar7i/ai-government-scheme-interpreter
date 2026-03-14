import type { Citation } from "../../services/api";

type Props = {
  citations: Citation[];
};

export default function CitationViewer({ citations }: Props) {
  if (!citations.length) return null;

  return (
    <div className="rounded-lg border border-slate-200 bg-slate-50 p-4">
      <h4 className="mb-2 text-sm font-semibold text-slate-800">Citations</h4>
      <ul className="space-y-3">
        {citations.map((citation, index) => (
          <li key={`${citation.page}-${index}`} className="rounded border border-slate-200 bg-white p-3 text-sm">
            <p className="font-medium text-slate-700">
              Page {citation.page ?? "N/A"} • {citation.section ?? "Unknown section"}
            </p>
            <p className="mt-1 text-slate-600">{citation.snippet}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}
