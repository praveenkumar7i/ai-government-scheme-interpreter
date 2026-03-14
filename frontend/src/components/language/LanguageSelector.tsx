"use client";

type Props = {
  value: string;
  onChange: (language: string) => void;
};

const languages = [
  { code: "en", label: "English" },
  { code: "hi", label: "Hindi" },
  { code: "kn", label: "Kannada" },
  { code: "ta", label: "Tamil" },
  { code: "te", label: "Telugu" },
];

export default function LanguageSelector({ value, onChange }: Props) {
  return (
    <label className="block space-y-1">
      <span className="text-sm font-medium text-slate-700">Output language</span>
      <select
        className="w-full rounded border border-slate-300 bg-white p-2 text-sm"
        value={value}
        onChange={(e) => onChange(e.target.value)}
      >
        {languages.map((language) => (
          <option key={language.code} value={language.code}>
            {language.label}
          </option>
        ))}
      </select>
    </label>
  );
}
