export interface ChatApiRequest {
  message: string
}

export interface ChatApiResponse {
  response: string
  conversation_id: string
  sources?: string[]
  citations?: Array<{
    id: string
    source: string
    excerpt: string
  }>
  symptom_analysis?: {
    symptoms: string[]
    severity_score: number
    risk_level: 'low' | 'medium' | 'high'
    possible_conditions: string[]
    urgency_recommendation: string
  }
  detected_language?: string
  recommended_specialist?: string
  disclaimer?: string
}

export interface SessionHistoryResponse {
  conversation_id: string
  messages: Array<{
    role: 'user' | 'assistant'
    content: string
    created_at: string
  }>
}

export async function sendChatMessage(payload: ChatApiRequest): Promise<ChatApiResponse> {
  const response = await fetch('/api/v1/chat', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
  })

  if (!response.ok) {
    throw new Error(`Chat request failed with status ${response.status}`)
  }

  return response.json()
}

export async function fetchSessionHistory(conversationId: string): Promise<SessionHistoryResponse> {
  const response = await fetch(`/api/v1/sessions/${conversationId}`)
  if (!response.ok) {
    throw new Error(`Session fetch failed with status ${response.status}`)
  }
  return response.json()
}
