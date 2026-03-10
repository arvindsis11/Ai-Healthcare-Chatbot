'use client'

import { useState, useRef, useEffect } from 'react'
import { cn } from '@/lib/utils'

interface InputBarProps {
  onSendMessage: (message: string) => void
  disabled?: boolean
}

const SYMPTOM_SUGGESTIONS = [
  "I have a headache",
  "I'm feeling nauseous",
  "I have chest pain",
  "I have a fever",
  "I'm experiencing shortness of breath",
  "I have abdominal pain",
  "I feel dizzy",
  "I have a sore throat",
  "I have joint pain",
  "I have fatigue",
  "What are the symptoms of diabetes?",
  "How to treat a cold?",
  "What should I do for high blood pressure?",
  "Explain what pneumonia is",
  "How to prevent heart disease?"
]

export function InputBar({ onSendMessage, disabled = false }: InputBarProps) {
  const [input, setInput] = useState('')
  const [showSuggestions, setShowSuggestions] = useState(false)
  const [filteredSuggestions, setFilteredSuggestions] = useState<string[]>([])
  const inputRef = useRef<HTMLTextAreaElement>(null)

  // Filter suggestions based on input
  useEffect(() => {
    if (input.trim()) {
      const filtered = SYMPTOM_SUGGESTIONS.filter(suggestion =>
        suggestion.toLowerCase().includes(input.toLowerCase())
      ).slice(0, 5)
      setFilteredSuggestions(filtered)
      setShowSuggestions(filtered.length > 0)
    } else {
      setFilteredSuggestions(SYMPTOM_SUGGESTIONS.slice(0, 5))
      setShowSuggestions(true)
    }
  }, [input])

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (input.trim() && !disabled) {
      onSendMessage(input.trim())
      setInput('')
      setShowSuggestions(false)
    }
  }

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit(e)
    }
  }

  const handleSuggestionClick = (suggestion: string) => {
    setInput(suggestion)
    setShowSuggestions(false)
    inputRef.current?.focus()
  }

  const adjustTextareaHeight = () => {
    const textarea = inputRef.current
    if (textarea) {
      textarea.style.height = 'auto'
      textarea.style.height = `${Math.min(textarea.scrollHeight, 120)}px`
    }
  }

  useEffect(() => {
    adjustTextareaHeight()
  }, [input])

  return (
    <div className="border-t border-border bg-background p-4">
      <div className="max-w-4xl mx-auto relative">
        {/* Suggestions Dropdown */}
        {showSuggestions && (
          <div className="absolute bottom-full mb-2 w-full bg-popover border border-border rounded-lg shadow-lg max-h-48 overflow-y-auto">
            {filteredSuggestions.map((suggestion, index) => (
              <button
                key={index}
                onClick={() => handleSuggestionClick(suggestion)}
                className="w-full text-left px-4 py-2 hover:bg-accent transition-colors text-sm"
              >
                {suggestion}
              </button>
            ))}
          </div>
        )}

        {/* Input Form */}
        <form onSubmit={handleSubmit} className="flex items-end space-x-3">
          <div className="flex-1 relative">
            <textarea
              ref={inputRef}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              onFocus={() => setShowSuggestions(true)}
              onBlur={() => setTimeout(() => setShowSuggestions(false), 200)}
              placeholder="Describe your symptoms or ask a health question..."
              disabled={disabled}
              className={cn(
                "w-full resize-none rounded-lg border border-input bg-background px-4 py-3 text-sm",
                "placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring",
                "disabled:opacity-50 disabled:cursor-not-allowed",
                "min-h-[44px] max-h-[120px]"
              )}
              rows={1}
            />

            {/* Character Count */}
            {input.length > 0 && (
              <div className="absolute bottom-2 right-3 text-xs text-muted-foreground">
                {input.length}/1000
              </div>
            )}
          </div>

          {/* Send Button */}
          <button
            type="submit"
            disabled={!input.trim() || disabled}
            className={cn(
              "flex items-center justify-center w-10 h-10 rounded-lg transition-colors",
              "bg-primary text-primary-foreground hover:bg-primary/90",
              "disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:bg-primary"
            )}
          >
            {disabled ? (
              <div className="w-4 h-4 border-2 border-current border-t-transparent rounded-full animate-spin" />
            ) : (
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
              </svg>
            )}
          </button>
        </form>

        {/* Helper Text */}
        <div className="flex items-center justify-between mt-2 text-xs text-muted-foreground">
          <span>Press Enter to send, Shift+Enter for new line</span>
          <span>💡 Try describing your symptoms for personalized advice</span>
        </div>
      </div>
    </div>
  )
}