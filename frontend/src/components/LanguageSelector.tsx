'use client'

import { Globe } from 'lucide-react'

const LANGUAGES = [
  { code: 'auto', name: 'Auto-detect' },
  { code: 'en', name: 'English' },
  { code: 'es', name: 'Spanish' },
  { code: 'fr', name: 'French' },
  { code: 'hi', name: 'Hindi' },
  { code: 'de', name: 'German' },
  { code: 'pt', name: 'Portuguese' },
  { code: 'ar', name: 'Arabic' },
  { code: 'zh', name: 'Chinese' },
]

interface LanguageSelectorProps {
  value: string
  onChange: (code: string) => void
  disabled?: boolean
}

export default function LanguageSelector({ value, onChange, disabled = false }: LanguageSelectorProps) {
  return (
    <div className="flex items-center gap-1.5">
      <Globe className="h-4 w-4 shrink-0 text-slate-500 dark:text-slate-400" />
      <select
        value={value}
        onChange={(e) => onChange(e.target.value)}
        disabled={disabled}
        aria-label="Select language"
        className="rounded-lg border border-slate-200 bg-white/80 py-1.5 pl-2 pr-6 text-sm text-slate-700 transition hover:border-slate-300 focus:outline-none focus:ring-2 focus:ring-sky-400/50 disabled:opacity-50 dark:border-slate-700 dark:bg-slate-800/80 dark:text-slate-200 dark:hover:border-slate-600"
      >
        {LANGUAGES.map((lang) => (
          <option key={lang.code} value={lang.code}>
            {lang.name}
          </option>
        ))}
      </select>
    </div>
  )
}
