export interface ChatApiRequest {
  message: string
  conversation_id?: string
  preferred_language?: string
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
  const body: any = {
    message: payload.message,
  }

  if (payload.conversation_id) {
    body.conversation_id = payload.conversation_id
  }

  if (payload.preferred_language && payload.preferred_language !== 'auto') {
    body.preferred_language = payload.preferred_language
  }

  const response = await fetch('/api/v1/chat', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(body),
  })

  if (!response.ok) {
    const errorText = await response.text()
    throw new Error(`Chat request failed (${response.status}): ${errorText}`)
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

export async function downloadHealthReport(conversationId: string, patientName?: string): Promise<void> {
  const body: Record<string, string> = { conversation_id: conversationId }
  if (patientName) {
    body.patient_name = patientName
  }

  const response = await fetch('/api/v1/reports/generate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  })

  if (!response.ok) {
    const errorText = await response.text()
    throw new Error(`Report generation failed (${response.status}): ${errorText}`)
  }

  const blob = await response.blob()
  const url = URL.createObjectURL(blob)
  const anchor = document.createElement('a')
  anchor.href = url
  anchor.download = `health_report_${conversationId.slice(0, 8)}.pdf`
  document.body.appendChild(anchor)
  anchor.click()
  document.body.removeChild(anchor)
  URL.revokeObjectURL(url)
}
