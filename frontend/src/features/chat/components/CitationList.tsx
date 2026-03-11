import { BookOpenText } from 'lucide-react'
import type { Citation } from '../types/chat'

interface CitationListProps {
  citations?: Citation[]
}

export default function CitationList({ citations = [] }: CitationListProps) {
  if (!citations.length) {
    return null
  }

  return (
    <div className="mt-3 rounded-xl border border-slate-200/80 bg-white/80 p-3 dark:border-slate-700/80 dark:bg-slate-900/70">
      <p className="mb-2 inline-flex items-center gap-2 text-xs font-semibold uppercase tracking-wide text-slate-500 dark:text-slate-300">
        <BookOpenText className="h-3.5 w-3.5" />
        Clinical references
      </p>
      <ul className="space-y-2 text-xs text-slate-600 dark:text-slate-300">
        {citations.map((citation) => (
          <li key={citation.id} className="rounded-lg border border-slate-200/60 bg-slate-50/70 p-2 dark:border-slate-700/60 dark:bg-slate-800/60">
            <p className="font-semibold text-slate-700 dark:text-slate-200">{citation.source}</p>
            <p className="line-clamp-3">{citation.excerpt}</p>
          </li>
        ))}
      </ul>
    </div>
  )
}
