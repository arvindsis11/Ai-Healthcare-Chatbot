export interface ChatApiRequest {
  message: string
}

export interface ChatApiResponse {
  response: string
  conversation_id: string
  sources?: string[]
  symptom_analysis?: {
    symptoms: string[]
    severity_score: number
    risk_level: 'low' | 'medium' | 'high'
    possible_conditions: string[]
    urgency_recommendation: string
  }
  disclaimer?: string
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
