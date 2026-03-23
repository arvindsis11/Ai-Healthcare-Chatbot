export interface SymptomAnalysis {
  symptoms: string[]
  severity_score: number
  risk_level: 'low' | 'medium' | 'high'
  possible_conditions: string[]
  urgency_recommendation: string
}

export interface Citation {
  id: string
  source: string
  excerpt: string
}

export interface ChatMessage {
  id: string
  role: 'user' | 'assistant'
  content: string
  timestamp: Date
  symptom_analysis?: SymptomAnalysis
  sources?: string[]
  citations?: Citation[]
  recommended_specialist?: string
}
export interface Conversation  {
  id: string
  title: string
}