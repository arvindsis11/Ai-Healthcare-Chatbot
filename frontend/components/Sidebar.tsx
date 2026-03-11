'use client'

import { Plus, Settings, Moon, Sun, Stethoscope, Menu, X } from 'lucide-react'

interface ConversationSummary {
  id: string
  label: string
}

interface SidebarProps {
  conversations: ConversationSummary[]
  activeConversationId: string
  onSelectConversation: (id: string) => void
  onNewChat: () => void
  onToggleTheme: () => void
  onToggleMobileSidebar: () => void
  isDarkMode: boolean
  isMobileSidebarOpen: boolean
}

export default function Sidebar({
  conversations,
  activeConversationId,
  onSelectConversation,
  onNewChat,
  onToggleTheme,
  onToggleMobileSidebar,
  isDarkMode,
  isMobileSidebarOpen,
}: SidebarProps) {
  return (
    <>
      <button
        type="button"
        onClick={onToggleMobileSidebar}
        className="fixed left-4 top-4 z-50 rounded-xl border border-slate-200 bg-white/90 p-2 text-slate-700 shadow-md backdrop-blur md:hidden dark:border-slate-700 dark:bg-slate-900/90 dark:text-slate-100"
        aria-label="Toggle menu"
      >
        {isMobileSidebarOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
      </button>

      {isMobileSidebarOpen && (
        <button
          type="button"
          onClick={onToggleMobileSidebar}
          className="fixed inset-0 z-30 bg-black/40 md:hidden"
          aria-label="Close menu overlay"
        />
      )}

      <aside
        className={[
          'fixed inset-y-0 left-0 z-40 w-72 border-r border-slate-200 bg-white/90 backdrop-blur transition-transform duration-300',
          'dark:border-slate-800 dark:bg-slate-950/90',
          isMobileSidebarOpen ? 'translate-x-0' : '-translate-x-full',
          'md:static md:translate-x-0',
        ].join(' ')}
      >
        <div className="flex h-full flex-col">
          <div className="border-b border-slate-200 p-4 dark:border-slate-800">
            <div className="mb-4 flex items-center gap-3">
              <div className="rounded-xl bg-gradient-to-br from-cyan-500 to-blue-600 p-2 text-white shadow-lg shadow-blue-500/25">
                <Stethoscope className="h-5 w-5" />
              </div>
              <div>
                <p className="text-sm font-semibold text-slate-900 dark:text-slate-100">Health AI</p>
                <p className="text-xs text-slate-500 dark:text-slate-400">RAG Assistant</p>
              </div>
            </div>

            <button
              type="button"
              onClick={onNewChat}
              className="flex w-full items-center justify-center gap-2 rounded-xl bg-slate-900 px-3 py-2 text-sm font-medium text-white transition hover:bg-slate-800 dark:bg-slate-100 dark:text-slate-900 dark:hover:bg-white"
            >
              <Plus className="h-4 w-4" />
              New chat
            </button>
          </div>

          <div className="flex-1 overflow-y-auto px-3 py-4">
            <p className="mb-2 px-2 text-xs font-medium uppercase tracking-wide text-slate-500 dark:text-slate-400">
              Conversations
            </p>
            <div className="space-y-1">
              {conversations.map((conversation) => (
                <button
                  key={conversation.id}
                  type="button"
                  onClick={() => onSelectConversation(conversation.id)}
                  className={[
                    'w-full rounded-lg px-3 py-2 text-left text-sm transition',
                    conversation.id === activeConversationId
                      ? 'bg-blue-50 text-blue-700 dark:bg-blue-500/20 dark:text-blue-200'
                      : 'text-slate-700 hover:bg-slate-100 dark:text-slate-300 dark:hover:bg-slate-800',
                  ].join(' ')}
                >
                  <p className="truncate">{conversation.label}</p>
                </button>
              ))}
            </div>
          </div>

          <div className="border-t border-slate-200 p-3 dark:border-slate-800">
            <div className="grid grid-cols-2 gap-2">
              <button
                type="button"
                className="flex items-center justify-center gap-2 rounded-lg border border-slate-200 px-3 py-2 text-sm text-slate-700 transition hover:bg-slate-100 dark:border-slate-700 dark:text-slate-300 dark:hover:bg-slate-800"
                onClick={() => window.alert('Settings panel can be wired here.')}
              >
                <Settings className="h-4 w-4" />
                Settings
              </button>
              <button
                type="button"
                onClick={onToggleTheme}
                className="flex items-center justify-center gap-2 rounded-lg border border-slate-200 px-3 py-2 text-sm text-slate-700 transition hover:bg-slate-100 dark:border-slate-700 dark:text-slate-300 dark:hover:bg-slate-800"
              >
                {isDarkMode ? <Sun className="h-4 w-4" /> : <Moon className="h-4 w-4" />}
                {isDarkMode ? 'Light' : 'Dark'}
              </button>
            </div>
          </div>
        </div>
      </aside>
    </>
  )
}