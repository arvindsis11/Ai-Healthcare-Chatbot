'use client'

import { Clock3, MessageSquarePlus } from 'lucide-react'

interface ChatHistorySidebarProps {
  items: Array<{ id: string; label: string }>
  activeId?: string
  onSelect: (id: string) => void
  onNewChat: () => void
}

export default function ChatHistorySidebar({ items, activeId, onSelect, onNewChat }: ChatHistorySidebarProps) {
  return (
    <aside className="panel-surface hidden w-72 shrink-0 border-r border-slate-200/70 p-4 md:flex md:flex-col dark:border-slate-800/70">
      <button
        type="button"
        onClick={onNewChat}
        className="mb-4 inline-flex items-center justify-center gap-2 rounded-xl bg-gradient-to-r from-blue-600 to-cyan-500 px-3 py-2 text-sm font-semibold text-white"
      >
        <MessageSquarePlus className="h-4 w-4" />
        New chat
      </button>

      <p className="mb-2 inline-flex items-center gap-2 text-xs font-semibold uppercase tracking-wide text-slate-500">
        <Clock3 className="h-3.5 w-3.5" />
        Chat history
      </p>

      <div className="space-y-2 overflow-y-auto">
        {items.map((item) => (
          <button
            key={item.id}
            type="button"
            onClick={() => onSelect(item.id)}
            className={[
              'w-full rounded-lg border px-3 py-2 text-left text-sm',
              item.id === activeId
                ? 'border-blue-300/80 bg-blue-50 text-blue-700 dark:border-blue-500/70 dark:bg-blue-500/20 dark:text-blue-200'
                : 'border-slate-200/70 hover:bg-slate-100 dark:border-slate-700/70 dark:hover:bg-slate-800',
            ].join(' ')}
          >
            {item.label}
          </button>
        ))}
      </div>
    </aside>
  )
}
