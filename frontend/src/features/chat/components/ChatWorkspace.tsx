'use client'

import { useMemo, useState } from 'react'
import { AlertTriangle } from 'lucide-react'
import { motion } from 'framer-motion'

import InputBar from '../../../components/InputBar'
import MessageBubble from '../../../components/MessageBubble'
import { sendChatMessage } from '../../../services/chatService'
import CitationList from './CitationList'
import ChatHistorySidebar from './ChatHistorySidebar'
import SymptomAnalysisPanel from './SymptomAnalysisPanel'
import type { ChatMessage } from '../types/chat'
import LoadingDots from "../../../components/LoadingDots";

const initialMessage: ChatMessage = {
  id: 'welcome',
  role: 'assistant',
  content:
    'Welcome to the enterprise AI healthcare assistant. Share your symptoms for general guidance, triage insight, and source citations.',
  timestamp: new Date(),
}

export default function ChatWorkspace() {
  const [messages, setMessages] = useState<ChatMessage[]>([initialMessage])
  const [isLoading, setIsLoading] = useState(false)
  const [activeConversationId, setActiveConversationId] = useState('current')

  const historyItems = useMemo(() => {
    const userItems = messages
      .filter((m) => m.role === 'user')
      .slice(-8)
      .reverse()
      .map((m) => ({ id: m.id, label: m.content.slice(0, 40) || 'New conversation' }))

    return userItems.length ? userItems : [{ id: 'current', label: 'Current conversation' }]
  }, [messages])

  const latestAssistant = [...messages].reverse().find((m) => m.role === 'assistant')

  const onSend = async (content: string) => {
    const userMessage: ChatMessage = {
      id: String(Date.now()),
      role: 'user',
      content,
      timestamp: new Date(),
    }
    setMessages((prev) => [...prev, userMessage])

    setIsLoading(true)
    try {
      const response = await sendChatMessage({ message: content })
      const assistantMessage: ChatMessage = {
        id: String(Date.now() + 1),
        role: 'assistant',
        content: response.response,
        timestamp: new Date(),
        symptom_analysis: response.symptom_analysis,
        sources: response.sources || [],
        citations: response.citations || [],
        recommended_specialist: response.recommended_specialist,
      }
      setMessages((prev) => [...prev, assistantMessage])
    } catch (_error) {
      setMessages((prev) => [
        ...prev,
        {
          id: String(Date.now() + 2),
          role: 'assistant',
          content: 'Unable to process your request right now. Please try again shortly.',
          timestamp: new Date(),
        },
      ])
    } finally {
      setIsLoading(false)
    }
  }

  const onNewChat = () => {
    setMessages([{ ...initialMessage, id: `welcome-${Date.now()}`, timestamp: new Date() }])
    setActiveConversationId('current')
  }

  return (
    <div className="relative flex min-h-screen overflow-hidden">
      <ChatHistorySidebar
        items={historyItems}
        activeId={activeConversationId}
        onSelect={setActiveConversationId}
        onNewChat={onNewChat}
      />

      <main className="relative flex min-w-0 flex-1 flex-col">
        <header className="panel-surface border-b border-slate-200/70 px-4 py-4 dark:border-slate-800/70 md:px-8">
          <h1 className="text-xl font-semibold tracking-tight">AI Healthcare Platform</h1>
          <p className="text-sm text-slate-600 dark:text-slate-300">Scalable clinical guidance with retrieval citations and triage signals</p>
        </header>

        <div className="border-b border-amber-300/70 bg-amber-50/90 px-4 py-2 text-sm text-amber-800 dark:border-amber-800/60 dark:bg-amber-900/30 dark:text-amber-200 md:px-8">
          <p className="flex items-center gap-2">
            <AlertTriangle className="h-4 w-4" />
            This assistant provides educational information only and is not a substitute for professional medical advice.
          </p>
        </div>

        <div className="grid flex-1 gap-4 overflow-hidden px-2 py-3 md:grid-cols-[minmax(0,1fr),300px] md:px-6">
          <motion.section
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.28 }}
            className="overflow-y-auto rounded-2xl border border-slate-200/70 bg-white/50 pb-24 dark:border-slate-800/70 dark:bg-slate-900/40"
          >
            {messages.map((message) => (
              <div key={message.id}>
                <MessageBubble message={message} isLatestAssistant={message.id === latestAssistant?.id} />
                {message.role === 'assistant' && <CitationList citations={message.citations} />}
              </div>
            ))}
            {isLoading && (
              <div className="flex items-center gap-2 px-6 py-4 text-sm text-slate-600 dark:text-slate-300">
                <p>Generating response</p>
                <LoadingDots />
              </div>
            )}
          </motion.section>

          <section className="hidden md:block">
            <SymptomAnalysisPanel
              analysis={latestAssistant?.symptom_analysis}
              specialist={latestAssistant?.recommended_specialist}
            />
          </section>
        </div>

        <InputBar onSend={onSend} disabled={isLoading} />
      </main>
    </div>
  )
}
