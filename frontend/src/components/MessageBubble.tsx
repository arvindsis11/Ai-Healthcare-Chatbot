'use client'

import { useEffect, useMemo, useState } from 'react'
import { Bot, Copy, User } from 'lucide-react'

interface Message {
  id: string
  role: 'user' | 'assistant'
  content: string
  timestamp: Date
  sources?: string[]
  symptom_analysis?: {
    risk_level: 'low' | 'medium' | 'high'
  }
}

interface MessageBubbleProps {
  message: Message
  isLatestAssistant?: boolean
  onRegenerate?: () => void
}

const codeFenceRegex = /```([\s\S]*?)```/g

function markdownToHtml(content: string): string {
  const escaped = content
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')

  const withCodeBlocks = escaped.replace(codeFenceRegex, (_match, code) => {
    return `<pre class="mt-3 overflow-x-auto rounded-lg bg-slate-900 p-3 text-xs text-slate-100"><code>${code.trim()}</code></pre>`
  })

  const withBold = withCodeBlocks.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
  const withInlineCode = withBold.replace(/`([^`]+)`/g, '<code class="rounded bg-slate-200/70 px-1 py-0.5 text-xs dark:bg-slate-700">$1</code>')

  return withInlineCode.replace(/\n/g, '<br />')
}

function getRiskStyles(level?: 'low' | 'medium' | 'high') {
  switch (level) {
    case 'high':
      return 'bg-red-100 text-red-700 dark:bg-red-500/20 dark:text-red-300'
    case 'medium':
      return 'bg-yellow-100 text-yellow-700 dark:bg-yellow-500/20 dark:text-yellow-300'
    case 'low':
      return 'bg-green-100 text-green-700 dark:bg-green-500/20 dark:text-green-300'
    default:
      return 'bg-slate-100 text-slate-700 dark:bg-slate-800 dark:text-slate-200'
  }
}

export default function MessageBubble({ message, isLatestAssistant = false, onRegenerate }: MessageBubbleProps) {
  const isUser = message.role === 'user'
  const riskLevel = message.symptom_analysis?.risk_level
  const [timeLabel, setTimeLabel] = useState('')

  const dateTime = useMemo(() => {
  const value =
    message.timestamp instanceof Date
      ? message.timestamp
      : new Date(message.timestamp)

  if (isNaN(value.getTime())) return new Date().toISOString()

  return value.toISOString()
  }, [message.timestamp])

  useEffect(() => {
    const value =
  message.timestamp instanceof Date
    ? message.timestamp
    : new Date(message.timestamp)

  if (!isNaN(value.getTime())) {
    setTimeLabel(value.toLocaleTimeString([], { hour: 'numeric', minute: '2-digit' }))
  }
  }, [message.timestamp])

  return (
    <div className={`flex items-start gap-3 px-3 py-4 md:px-4 ${isUser ? 'justify-end' : 'justify-start'}`}>
      {!isUser && (
        <div className="mt-1 flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-full bg-gradient-to-br from-cyan-500 to-blue-600 text-white shadow-md shadow-blue-500/30">
          <Bot className="h-4 w-4" />
        </div>
      )}

      <div className={`max-w-[88%] rounded-2xl px-4 py-3 shadow-sm md:max-w-2xl ${
        isUser
          ? 'bg-gradient-to-br from-blue-600 via-brand-500 to-cyan-500 text-white shadow-glow'
          : 'panel-surface border border-slate-200/70 text-slate-800 dark:border-slate-700/70 dark:text-slate-100'
      }`}>
        {!isUser && riskLevel && (
          <span className={`mb-2 inline-flex rounded-full px-2.5 py-1 text-[11px] font-semibold uppercase tracking-wide ${getRiskStyles(riskLevel)}`}>
            {riskLevel} risk
          </span>
        )}

        <div className="max-w-none break-words whitespace-pre-wrap text-[14px] leading-6" dangerouslySetInnerHTML={{ __html: markdownToHtml(message.content) }} />

        {!!message.sources?.length && !isUser && (
          <div className="mt-3 rounded-xl border border-slate-200/80 bg-white/80 p-3 dark:border-slate-700/80 dark:bg-slate-900/70">
            <p className="mb-2 text-xs font-semibold uppercase tracking-wide text-slate-500 dark:text-slate-300">
              Sources used
            </p>
            <ul className="space-y-1 text-xs text-slate-600 dark:text-slate-300">
              {message.sources.map((source, index) => (
                <li key={`${message.id}-source-${index}`} className="truncate">
                  {index + 1}. {source}
                </li>
              ))}
            </ul>
          </div>
        )}

        <div className={`mt-3 flex items-center justify-between gap-3 text-xs ${isUser ? 'text-blue-100' : 'text-slate-500 dark:text-slate-400'}`}>
          <time dateTime={dateTime} suppressHydrationWarning>
            {timeLabel}
          </time>
          {!isUser && (
            <div className="flex items-center gap-2">
              <button
                type="button"
                onClick={() => navigator.clipboard.writeText(message.content)}
                className="inline-flex items-center gap-1 rounded-md px-2 py-1 transition hover:bg-slate-200/80 dark:hover:bg-slate-700"
                aria-label="Copy message"
              >
                <Copy className="h-3.5 w-3.5" />
                Copy
              </button>
              {isLatestAssistant && onRegenerate && (
                <button
                  type="button"
                  onClick={onRegenerate}
                  className="rounded-md px-2 py-1 transition hover:bg-slate-200/80 dark:hover:bg-slate-700"
                >
                  Regenerate
                </button>
              )}
            </div>
          )}
        </div>
      </div>

      {isUser && (
        <div className="mt-1 flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-full border border-slate-300 bg-white text-slate-600 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-300">
          <User className="h-4 w-4" />
        </div>
      )}
    </div>
  )
}