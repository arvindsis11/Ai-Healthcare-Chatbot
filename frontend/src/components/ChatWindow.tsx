'use client'

import { useEffect, useMemo, useRef, useState } from 'react'
import { Bot, AlertTriangle } from 'lucide-react'
import InputBar from './InputBar'
import MessageBubble from './MessageBubble'
import Sidebar from './Sidebar'
import { sendChatMessage } from '../services/chatService'

interface SymptomAnalysis {
  symptoms: string[]
  severity_score: number
  risk_level: 'low' | 'medium' | 'high'
  possible_conditions: string[]
  urgency_recommendation: string
}

interface Message {
  id: string
  role: 'user' | 'assistant'
  content: string
  timestamp: Date
  symptom_analysis?: SymptomAnalysis
  sources?: string[]
}

const DEFAULT_ASSISTANT_MESSAGE: Message = {
  id: 'welcome-1',
  role: 'assistant',
  content:
    'Hello! I am your AI healthcare assistant. Share your symptoms and I can provide general health information with triage guidance and cited sources.',
  timestamp: new Date(),
}

export default function ChatWindow() {
  const [messages, setMessages] = useState<Message[]>([DEFAULT_ASSISTANT_MESSAGE])
  const [isLoading, setIsLoading] = useState(false)
  const [isDarkMode, setIsDarkMode] = useState(false)
  const [isMobileSidebarOpen, setIsMobileSidebarOpen] = useState(false)
  const [streamingMessageId, setStreamingMessageId] = useState<string | null>(null)
  const [streamingContent, setStreamingContent] = useState('')

  const scrollAreaRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const savedTheme = localStorage.getItem('theme')
    const isDark = savedTheme === 'dark'
    setIsDarkMode(isDark)
    document.documentElement.classList.toggle('dark', isDark)
  }, [])

  useEffect(() => {
    if (!scrollAreaRef.current) {
      return
    }
    scrollAreaRef.current.scrollTo({
      top: scrollAreaRef.current.scrollHeight,
      behavior: 'smooth',
    })
  }, [messages, isLoading, streamingContent])

  useEffect(() => {
    if (!streamingMessageId) {
      return
    }

    const target = messages.find((message) => message.id === streamingMessageId)
    if (!target) {
      return
    }

    let i = 0
    const fullText = target.content
    setStreamingContent('')

    const timer = window.setInterval(() => {
      i += Math.max(1, Math.floor(fullText.length / 60))
      const next = fullText.slice(0, i)
      setStreamingContent(next)
      if (i >= fullText.length) {
        window.clearInterval(timer)
        setStreamingMessageId(null)
        setStreamingContent('')
      }
    }, 20)

    return () => window.clearInterval(timer)
  }, [streamingMessageId, messages])

  const toggleTheme = () => {
    const next = !isDarkMode
    setIsDarkMode(next)
    localStorage.setItem('theme', next ? 'dark' : 'light')
    document.documentElement.classList.toggle('dark', next)
  }

  const runAssistantResponse = async (content: string) => {
    setIsLoading(true)
    try {
      const data = await sendChatMessage({ message: content })

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: data.response,
        timestamp: new Date(),
        symptom_analysis: data.symptom_analysis,
        sources: data.sources ?? [],
      }

      setMessages((prev) => [...prev, assistantMessage])
      setStreamingMessageId(assistantMessage.id)
    } catch (error) {
      console.error('Error sending message:', error)
      setMessages((prev) => [
        ...prev,
        {
          id: (Date.now() + 1).toString(),
          role: 'assistant',
          content: 'Sorry, I encountered an error while generating a response. Please try again.',
          timestamp: new Date(),
        },
      ])
    } finally {
      setIsLoading(false)
    }
  }

  const handleSend = async (content: string) => {
    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content,
      timestamp: new Date(),
    }
    setMessages((prev) => [...prev, userMessage])
    await runAssistantResponse(content)
  }

  const handleRegenerate = async () => {
    const lastUserMessage = [...messages].reverse().find((message) => message.role === 'user')
    if (!lastUserMessage || isLoading) {
      return
    }
    await runAssistantResponse(lastUserMessage.content)
  }

  const handleNewChat = () => {
    setMessages([
      {
        ...DEFAULT_ASSISTANT_MESSAGE,
        id: `welcome-${Date.now()}`,
        timestamp: new Date(),
      },
    ])
    setIsMobileSidebarOpen(false)
  }

  const conversations = useMemo(() => {
    const snippets = messages
      .filter((message) => message.role === 'user')
      .slice(-8)
      .reverse()
      .map((message) => ({
        id: message.id,
        label: message.content.slice(0, 36) || 'New conversation',
      }))

    return snippets.length > 0 ? snippets : [{ id: 'current', label: 'Current conversation' }]
  }, [messages])

  const activeConversationId = conversations[0]?.id ?? 'current'
  const latestAssistantId = [...messages].reverse().find((message) => message.role === 'assistant')?.id

  return (
    <div className="relative flex h-screen overflow-hidden text-slate-900 dark:text-gray-100">
      <Sidebar
        conversations={conversations}
        activeConversationId={activeConversationId}
        onSelectConversation={() => setIsMobileSidebarOpen(false)}
        onNewChat={handleNewChat}
        onToggleTheme={toggleTheme}
        onToggleMobileSidebar={() => setIsMobileSidebarOpen((prev) => !prev)}
        isDarkMode={isDarkMode}
        isMobileSidebarOpen={isMobileSidebarOpen}
      />

      <section className="relative flex min-w-0 flex-1 flex-col">
        <header className="panel-surface border-b border-slate-200/70 px-4 py-4 dark:border-slate-800/70 md:px-8">
          <div className="flex flex-wrap items-center justify-between gap-3">
            <div>
              <h1 className="text-xl font-semibold tracking-tight">AI Healthcare Assistant</h1>
              <p className="text-sm text-slate-600 dark:text-slate-300">Conversational triage with source-aware clinical guidance</p>
            </div>
            <div className="flex items-center gap-2 text-xs">
              <span className="rounded-full border border-emerald-400/50 bg-emerald-500/15 px-3 py-1 text-emerald-700 dark:text-emerald-300">Live</span>
              <span className="rounded-full border border-blue-400/40 bg-blue-500/15 px-3 py-1 text-blue-700 dark:text-blue-300">RAG</span>
            </div>
          </div>
        </header>

        <div className="border-b border-amber-300/70 bg-amber-50/90 px-4 py-2 text-sm text-amber-800 dark:border-amber-800/60 dark:bg-amber-900/30 dark:text-amber-200 md:px-8">
          <p className="flex items-center gap-2">
            <AlertTriangle className="h-4 w-4" />
            This AI provides general health information and is not a substitute for professional medical advice.
          </p>
        </div>

        <div ref={scrollAreaRef} className="flex-1 overflow-y-auto px-2 pb-24 md:px-6">
          {messages.map((message) => {
            const shouldShowStreaming = message.id === streamingMessageId && streamingContent
            return (
              <MessageBubble
                key={message.id}
                message={{
                  ...message,
                  content: shouldShowStreaming ? streamingContent : message.content,
                }}
                isLatestAssistant={message.id === latestAssistantId}
                onRegenerate={handleRegenerate}
              />
            )
          })}

          {isLoading && (
            <div className="flex items-center gap-3 px-6 py-4 text-slate-600 dark:text-slate-300">
              <div className="flex h-8 w-8 items-center justify-center rounded-full bg-gradient-to-br from-cyan-500 to-blue-600 text-white">
                <Bot className="h-4 w-4" />
              </div>
              <div className="panel-surface rounded-xl border border-slate-200/80 px-4 py-3 shadow-glow dark:border-slate-700/80">
                <p className="mb-1 text-sm">AI is thinking...</p>
                <div className="flex gap-1">
                  <span className="h-2 w-2 animate-pulseSoft rounded-full bg-blue-500" />
                  <span className="h-2 w-2 animate-pulseSoft rounded-full bg-blue-500" style={{ animationDelay: '0.15s' }} />
                  <span className="h-2 w-2 animate-pulseSoft rounded-full bg-blue-500" style={{ animationDelay: '0.3s' }} />
                </div>
              </div>
            </div>
          )}
        </div>

        <InputBar onSend={handleSend} disabled={isLoading} />
      </section>
    </div>
  )
}