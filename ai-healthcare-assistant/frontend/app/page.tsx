import ChatInterface from '../components/ChatInterface'

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-8">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            AI Healthcare Assistant
          </h1>
          <p className="text-lg text-gray-600">
            Get instant health advice and answers to your medical questions
          </p>
        </div>
        <div className="max-w-4xl mx-auto bg-white rounded-lg shadow-lg overflow-hidden">
          <ChatInterface />
        </div>
      </div>
    </div>
  )
}