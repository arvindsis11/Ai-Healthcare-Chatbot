'use client'

import { useState, useRef, useEffect } from 'react'
import { cn } from '@/lib/utils'
import { useVoiceRecording } from '@/lib/useVoiceRecording'

interface InputBarProps {
  onSendMessage: (message: string) => void
  onSendVoiceMessage?: (audioBlob: Blob) => void
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

export function InputBar({ onSendMessage, onSendVoiceMessage, disabled = false }: InputBarProps) {
  const [input, setInput] = useState('')
  const [showSuggestions, setShowSuggestions] = useState(false)
  const [filteredSuggestions, setFilteredSuggestions] = useState<string[]>([])
  const inputRef = useRef<HTMLTextAreaElement>(null)

  const { isRecording, recordingTime, startRecording, stopRecording } = useVoiceRecording()

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

  // Recording timer
  useEffect(() => {
    if (isRecording) {
      recordingIntervalRef.current = setInterval(() => {
        setRecordingTime(prev => prev + 1)
      }, 1000)
    } else {
      if (recordingIntervalRef.current) {
        clearInterval(recordingIntervalRef.current)
        recordingIntervalRef.current = null
      }
      setRecordingTime(0)
    }

    return () => {
      if (recordingIntervalRef.current) {
        clearInterval(recordingIntervalRef.current)
      }
    }
  }, [isRecording])

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

  const handleVoiceButtonClick = async () => {
    if (isRecording) {
      // Stop recording and send voice message
      const audioBlob = await stopRecording()
      if (audioBlob && onSendVoiceMessage) {
        onSendVoiceMessage(audioBlob)
      }
    } else {
      // Start recording
      try {
        await startRecording()
      } catch (error) {
        console.error('Failed to start recording:', error)
        alert('Could not access microphone. Please check permissions.')
      }
    }
  }

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60)
    const secs = seconds % 60
    return `${mins}:${secs.toString().padStart(2, '0')}`
  }

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
              disabled={disabled || isRecording}
              className={cn(
                "w-full resize-none rounded-lg border border-input bg-background px-4 py-3 text-sm",
                "placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring",
                "disabled:opacity-50 disabled:cursor-not-allowed",
                "min-h-[44px] max-h-[120px]"
              )}
              rows={1}
            />

            {/* Recording Indicator */}
            {isRecording && (
              <div className="absolute inset-0 bg-red-500/10 border border-red-500/20 rounded-lg flex items-center justify-center">
                <div className="flex items-center space-x-3 text-red-600">
                  <div className="w-3 h-3 bg-red-500 rounded-full animate-pulse"></div>
                  <span className="font-medium">Recording... {formatTime(recordingTime)}</span>
                </div>
              </div>
            )}

            {/* Character Count */}
            {input.length > 0 && !isRecording && (
              <div className="absolute bottom-2 right-3 text-xs text-muted-foreground">
                {input.length}/1000
              </div>
            )}
          </div>

          {/* Voice Button */}
          <button
            type="button"
            onClick={handleVoiceButtonClick}
            disabled={disabled}
            className={cn(
              "flex items-center justify-center w-12 h-12 rounded-lg transition-all duration-200",
              isRecording
                ? "bg-red-500 hover:bg-red-600 text-white animate-pulse"
                : "bg-secondary hover:bg-secondary/80 text-secondary-foreground",
              "disabled:opacity-50 disabled:cursor-not-allowed"
            )}
            title={isRecording ? "Stop recording" : "Start voice recording"}
          >
            {isRecording ? (
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4" />
              </svg>
            ) : (
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
              </svg>
            )}
          </button>

          {/* Send Button */}
          <button
            type="submit"
            disabled={!input.trim() || disabled || isRecording}
            className={cn(
              "flex items-center justify-center w-12 h-12 rounded-lg transition-colors",
              "bg-primary text-primary-foreground hover:bg-primary/90",
              "disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:bg-primary"
            )}
          >
            {disabled ? (
              <div className="w-4 h-4 border-2 border-current border-t-transparent rounded-full animate-spin" />
            ) : (
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
              </svg>
            )}
          </button>
        </form>

        {/* Helper Text */}
        <div className="flex items-center justify-between mt-2 text-xs text-muted-foreground">
          <span>Press Enter to send, Shift+Enter for new line • Click 🎤 to use voice</span>
          <span>💡 Try describing your symptoms for personalized advice</span>
        </div>
      </div>
    </div>
  )
}