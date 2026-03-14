type Props = {
  eligibility: string;
  confidence: number;
  reasoning?: {
    rule_based_verdict?: string;
    reasons?: string[];
  };
};

export default function EligibilityResultCard({ eligibility, confidence, reasoning }: Props) {
  const tone =
    eligibility === "Not Eligible"
      ? "bg-red-50 border-red-300 text-red-800"
      : eligibility === "Likely Eligible"
      ? "bg-emerald-50 border-emerald-300 text-emerald-800"
      : "bg-amber-50 border-amber-300 text-amber-800";

  return (
    <div className={`rounded-lg border p-4 ${tone}`}>
      <h3 className="text-lg font-semibold">Eligibility Result</h3>
      <p className="mt-1 text-sm">Verdict: {eligibility}</p>
      <p className="text-sm">Confidence: {(confidence * 100).toFixed(0)}%</p>
      {reasoning?.reasons?.length ? (
        <ul className="mt-3 list-disc space-y-1 pl-5 text-sm">
          {reasoning.reasons.map((reason, idx) => (
            <li key={idx}>{reason}</li>
          ))}
        </ul>
      ) : null}
    </div>
  );
}
