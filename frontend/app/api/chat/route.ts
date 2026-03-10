import { NextRequest, NextResponse } from 'next/server'

// Mock responses for demonstration
const MOCK_RESPONSES = {
  headache: "Headaches can have many causes including tension, dehydration, or migraines. For mild headaches, try resting in a quiet, dark room and staying hydrated. If headaches are severe, persistent, or accompanied by other symptoms like nausea or vision changes, please consult a healthcare professional.",
  fever: "A fever is your body's natural response to infection. For low-grade fevers (under 101°F/38.3°C), rest and stay hydrated. Take acetaminophen (Tylenol) or ibuprofen if needed. See a doctor if fever exceeds 103°F (39.4°C), lasts more than 3 days, or is accompanied by severe symptoms.",
  cough: "Coughs can be caused by viral infections, allergies, or irritants. For a dry cough, try honey and lemon tea or over-the-counter cough syrups. Stay hydrated and use a humidifier. Consult a doctor if cough persists over 2 weeks or is accompanied by chest pain, shortness of breath, or blood.",
  "chest pain": "Chest pain can be serious and requires immediate medical attention. This could indicate heart problems, pulmonary embolism, or other serious conditions. Please call emergency services (911) immediately if you experience chest pain, especially if accompanied by shortness of breath, sweating, or pain radiating to your arm or jaw.",
  diabetes: "Diabetes is a condition where your body can't properly regulate blood sugar. Type 1 diabetes requires insulin, while Type 2 can often be managed with diet, exercise, and medication. Common symptoms include frequent urination, excessive thirst, fatigue, and slow-healing wounds. Please consult a healthcare provider for proper diagnosis and management.",
  default: "I'm here to help with your health questions. For personalized medical advice, please consult with a qualified healthcare professional. Can you provide more details about your symptoms or question?"
}

function getMockResponse(message: string): string {
  const lowerMessage = message.toLowerCase()

  // Check for specific keywords
  for (const [keyword, response] of Object.entries(MOCK_RESPONSES)) {
    if (keyword !== 'default' && lowerMessage.includes(keyword)) {
      return response
    }
  }

  return MOCK_RESPONSES.default
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    const { message } = body

    if (!message || typeof message !== 'string') {
      return NextResponse.json(
        { error: 'Message is required and must be a string' },
        { status: 400 }
      )
    }

    // Simulate processing delay
    await new Promise(resolve => setTimeout(resolve, 1000 + Math.random() * 2000))

    // Get mock response
    const response = getMockResponse(message)

    // Mock symptom analysis (only for symptom-related messages)
    const symptomAnalysis = message.toLowerCase().includes('symptom') || message.toLowerCase().includes('pain') || message.toLowerCase().includes('fever') || message.toLowerCase().includes('cough') || message.toLowerCase().includes('headache')
      ? {
          severity_score: Math.floor(Math.random() * 6) + 1, // 1-6 for demo
          risk_level: Math.random() > 0.7 ? 'medium' : 'low',
          possible_conditions: ['Common cold', 'Viral infection', 'Allergies'],
          urgency_recommendation: 'Monitor symptoms and consult a healthcare provider if they worsen.'
        }
      : undefined

    return NextResponse.json({
      message: response,
      symptom_analysis: symptomAnalysis,
      timestamp: new Date().toISOString()
    })

  } catch (error) {
    console.error('Chat API error:', error)
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    )
  }
}