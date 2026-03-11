'use client'

import { useEffect, useRef, useState } from 'react'
import { Mic, Send } from 'lucide-react'

interface InputBarProps {
  onSend: (value: string) => void
  disabled?: boolean
}

export default function InputBar({ onSend, disabled = false }: InputBarProps) {
  const [value, setValue] = useState('')
  const [isListening, setIsListening] = useState(false)
  const textareaRef = useRef<HTMLTextAreaElement>(null)

  useEffect(() => {
    const textarea = textareaRef.current
    if (!textarea) {
      return
    }
    textarea.style.height = 'auto'
    textarea.style.height = `${Math.min(textarea.scrollHeight, 180)}px`
  }, [value])

  const submit = () => {
    if (!value.trim() || disabled) {
      return
    }
    onSend(value.trim())
    setValue('')
  }

  const handleMic = () => {
    if (disabled) {
      return
    }

    const SpeechRecognition =
      typeof window !== 'undefined' &&
      ((window as any).SpeechRecognition || (window as any).webkitSpeechRecognition)

    if (!SpeechRecognition) {
      window.alert('Speech recognition is not supported in this browser.')
      return
    }

    const recognition = new SpeechRecognition()
    recognition.lang = 'en-US'
    recognition.interimResults = false
    recognition.maxAlternatives = 1

    recognition.onstart = () => setIsListening(true)
    recognition.onend = () => setIsListening(false)
    recognition.onerror = () => setIsListening(false)
    recognition.onresult = (event: any) => {
      const transcript = event?.results?.[0]?.[0]?.transcript ?? ''
      setValue((prev) => `${prev} ${transcript}`.trim())
    }

    recognition.start()
  }

  return (
    <div className="sticky bottom-0 z-20 border-t border-slate-200 bg-white/95 p-3 backdrop-blur dark:border-slate-800 dark:bg-slate-950/95">
      <div className="mx-auto flex w-full max-w-4xl items-end gap-2 rounded-2xl border border-slate-200 bg-white p-2 shadow-sm dark:border-slate-700 dark:bg-slate-900">
        <textarea
          ref={textareaRef}
          value={value}
          disabled={disabled}
          rows={1}
          placeholder="Describe your symptoms or ask a health question..."
          onChange={(event) => setValue(event.target.value)}
          onKeyDown={(event) => {
            if (event.key === 'Enter' && !event.shiftKey) {
              event.preventDefault()
              submit()
            }
          }}
          className="max-h-[180px] min-h-[44px] flex-1 resize-none bg-transparent px-3 py-2 text-sm text-slate-900 outline-none placeholder:text-slate-400 disabled:opacity-50 dark:text-slate-100 dark:placeholder:text-slate-500"
        />

        <button
          type="button"
          onClick={handleMic}
          disabled={disabled}
          className={[
            'rounded-xl p-2 text-slate-600 transition hover:bg-slate-100 dark:text-slate-300 dark:hover:bg-slate-800',
            isListening ? 'bg-red-100 text-red-600 dark:bg-red-500/20 dark:text-red-300' : '',
          ].join(' ')}
          aria-label="Use microphone"
        >
          <Mic className="h-5 w-5" />
        </button>

        <button
          type="button"
          onClick={submit}
          disabled={disabled || !value.trim()}
          className="rounded-xl bg-gradient-to-br from-cyan-500 to-blue-600 p-2 text-white shadow-md shadow-blue-500/30 transition hover:brightness-110 disabled:cursor-not-allowed disabled:opacity-50"
          aria-label="Send message"
        >
          <Send className="h-5 w-5" />
        </button>
      </div>
      <p className="mx-auto mt-2 w-full max-w-4xl px-2 text-xs text-slate-500 dark:text-slate-400">
        Press Enter to send, Shift+Enter for a new line.
      </p>
    </div>
  )
}