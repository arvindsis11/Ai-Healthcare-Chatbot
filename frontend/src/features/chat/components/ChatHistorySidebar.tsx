'use client'

import { Clock3, MessageSquarePlus, X } from 'lucide-react'

interface ChatHistorySidebarProps {
  items: Array<{ id: string; label: string }>
  activeId?: string | null
  onSelect: (id: string) => void
  onNewChat: () => void
  isOpen?: boolean
  onClose?: () => void
}

export default function ChatHistorySidebar({
  items,
  activeId,
  onSelect,
  onNewChat,
  isOpen = false,
  onClose,
}: ChatHistorySidebarProps) {
  const sidebarContent = (
    <>
      <div className="mb-4 flex items-center justify-between">
        <button
          type="button"
          onClick={onNewChat}
          className="inline-flex flex-1 items-center justify-center gap-2 rounded-xl bg-gradient-to-r from-blue-600 to-cyan-500 px-3 py-2 text-sm font-semibold text-white"
        >
          <MessageSquarePlus className="h-4 w-4" />
          New chat
        </button>
        {/* Close button — mobile only */}
        {onClose && (
          <button
            type="button"
            onClick={onClose}
            className="ml-2 rounded-lg p-2 text-slate-500 hover:bg-slate-100 dark:text-slate-400 dark:hover:bg-slate-800 md:hidden"
            aria-label="Close sidebar"
          >
            <X className="h-5 w-5" />
          </button>
        )}
      </div>

      <p className="mb-2 inline-flex items-center gap-2 text-xs font-semibold uppercase tracking-wide text-slate-500">
        <Clock3 className="h-3.5 w-3.5" />
        Chat history
      </p>

      <div className="space-y-2 overflow-y-auto">
        {items.map((item) => (
          <button
            key={item.id}
            type="button"
            onClick={() => {
              onSelect(item.id)
              onClose?.()
            }}
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
    </>
  )

  return (
    <>
      {/* Desktop sidebar — always visible */}
      <aside className="panel-surface hidden w-72 shrink-0 flex-col border-r border-slate-200/70 p-4 dark:border-slate-800/70 md:flex">
        {sidebarContent}
      </aside>

      {/* Mobile overlay backdrop */}
      {isOpen && (
        <div
          className="fixed inset-0 z-40 bg-black/50 md:hidden"
          onClick={onClose}
          aria-hidden="true"
        />
      )}

      {/* Mobile sidebar — slides in from left */}
      <aside
        className={[
          'panel-surface fixed inset-y-0 left-0 z-50 flex w-72 shrink-0 flex-col border-r border-slate-200/70 p-4 transition-transform duration-300 dark:border-slate-800/70 md:hidden',
          isOpen ? 'translate-x-0' : '-translate-x-full',
        ].join(' ')}
      >
        {sidebarContent}
      </aside>
    </>
  )
}
