'use client'

import { cn } from '@/lib/utils'

interface SidebarProps {
  isOpen: boolean
  onToggle: () => void
  darkMode: boolean
  onToggleDarkMode: () => void
  onClearChat: () => void
  messageCount: number
}

export function Sidebar({
  isOpen,
  onToggle,
  darkMode,
  onToggleDarkMode,
  onClearChat,
  messageCount
}: SidebarProps) {
  return (
    <>
      {/* Overlay */}
      {isOpen && (
        <div
          className="fixed inset-0 bg-black/50 z-40 lg:hidden"
          onClick={onToggle}
        />
      )}

      {/* Sidebar */}
      <div className={cn(
        "fixed left-0 top-0 z-50 h-full w-80 bg-card border-r border-border transition-transform duration-300 ease-in-out",
        "lg:translate-x-0 lg:static lg:inset-0",
        isOpen ? "translate-x-0" : "-translate-x-full"
      )}>
        <div className="flex flex-col h-full">
          {/* Header */}
          <div className="flex items-center justify-between p-4 border-b border-border">
            <h2 className="text-lg font-semibold">Healthcare Assistant</h2>
            <button
              onClick={onToggle}
              className="p-2 rounded-lg hover:bg-accent transition-colors lg:hidden"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          {/* Content */}
          <div className="flex-1 overflow-y-auto p-4 space-y-6">
            {/* Quick Actions */}
            <div>
              <h3 className="text-sm font-medium text-muted-foreground mb-3">Quick Actions</h3>
              <div className="space-y-2">
                <button className="w-full text-left px-3 py-2 rounded-lg hover:bg-accent transition-colors text-sm">
                  🏥 Emergency Contacts
                </button>
                <button className="w-full text-left px-3 py-2 rounded-lg hover:bg-accent transition-colors text-sm">
                  📋 Health Checklist
                </button>
                <button className="w-full text-left px-3 py-2 rounded-lg hover:bg-accent transition-colors text-sm">
                  💊 Medication Reminders
                </button>
                <button className="w-full text-left px-3 py-2 rounded-lg hover:bg-accent transition-colors text-sm">
                  📞 Find Healthcare Providers
                </button>
              </div>
            </div>

            {/* Common Symptoms */}
            <div>
              <h3 className="text-sm font-medium text-muted-foreground mb-3">Common Symptoms</h3>
              <div className="grid grid-cols-2 gap-2">
                {[
                  "Headache",
                  "Fever",
                  "Cough",
                  "Fatigue",
                  "Nausea",
                  "Chest Pain",
                  "Shortness of Breath",
                  "Abdominal Pain"
                ].map((symptom) => (
                  <button
                    key={symptom}
                    className="px-3 py-2 text-xs bg-secondary hover:bg-secondary/80 rounded-lg transition-colors"
                  >
                    {symptom}
                  </button>
                ))}
              </div>
            </div>

            {/* Health Topics */}
            <div>
              <h3 className="text-sm font-medium text-muted-foreground mb-3">Health Topics</h3>
              <div className="space-y-2">
                {[
                  "Cardiovascular Health",
                  "Mental Health",
                  "Nutrition & Diet",
                  "Exercise & Fitness",
                  "Preventive Care",
                  "Chronic Conditions",
                  "Women's Health",
                  "Men's Health"
                ].map((topic) => (
                  <button
                    key={topic}
                    className="w-full text-left px-3 py-2 rounded-lg hover:bg-accent transition-colors text-sm"
                  >
                    {topic}
                  </button>
                ))}
              </div>
            </div>

            {/* Chat Statistics */}
            <div>
              <h3 className="text-sm font-medium text-muted-foreground mb-3">Session Info</h3>
              <div className="space-y-2 text-sm">
                <div className="flex justify-between">
                  <span className="text-muted-foreground">Messages:</span>
                  <span>{messageCount}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-muted-foreground">Session:</span>
                  <span>{new Date().toLocaleDateString()}</span>
                </div>
              </div>
            </div>
          </div>

          {/* Footer */}
          <div className="p-4 border-t border-border space-y-3">
            {/* Settings */}
            <div>
              <h3 className="text-sm font-medium text-muted-foreground mb-2">Settings</h3>
              <div className="space-y-2">
                <button
                  onClick={onToggleDarkMode}
                  className="w-full flex items-center justify-between px-3 py-2 rounded-lg hover:bg-accent transition-colors text-sm"
                >
                  <span>Dark Mode</span>
                  <div className={cn(
                    "w-8 h-4 rounded-full transition-colors",
                    darkMode ? "bg-primary" : "bg-muted"
                  )}>
                    <div className={cn(
                      "w-3 h-3 rounded-full bg-white transition-transform duration-200",
                      darkMode ? "translate-x-4" : "translate-x-0.5"
                    )} />
                  </div>
                </button>
              </div>
            </div>

            {/* Actions */}
            <div className="space-y-2">
              <button
                onClick={onClearChat}
                className="w-full px-3 py-2 rounded-lg bg-destructive/10 hover:bg-destructive/20 text-destructive transition-colors text-sm"
              >
                Clear Chat History
              </button>
              <button className="w-full px-3 py-2 rounded-lg hover:bg-accent transition-colors text-sm">
                Export Conversation
              </button>
            </div>

            {/* Disclaimer */}
            <div className="text-xs text-muted-foreground bg-muted/50 p-3 rounded-lg">
              <p className="font-medium mb-1">⚕️ Medical Disclaimer</p>
              <p>This AI assistant provides general health information only. Always consult healthcare professionals for medical advice, diagnosis, or treatment.</p>
            </div>
          </div>
        </div>
      </div>
    </>
  )
}