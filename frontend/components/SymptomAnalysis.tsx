import { AlertTriangle, Info, CheckCircle, XCircle } from 'lucide-react'

interface SymptomAnalysis {
  symptoms: string[]
  severity_score: number
  risk_level: 'low' | 'medium' | 'high'
  possible_conditions: string[]
  urgency_recommendation: string
}

interface SymptomAnalysisProps {
  analysis: SymptomAnalysis
}

export default function SymptomAnalysis({ analysis }: SymptomAnalysisProps) {
  const getRiskColor = (level: string) => {
    switch (level) {
      case 'high': return 'text-red-600 bg-red-50 border-red-200'
      case 'medium': return 'text-yellow-600 bg-yellow-50 border-yellow-200'
      case 'low': return 'text-green-600 bg-green-50 border-green-200'
      default: return 'text-gray-600 bg-gray-50 border-gray-200'
    }
  }

  const getRiskIcon = (level: string) => {
    switch (level) {
      case 'high': return <XCircle className="w-5 h-5" />
      case 'medium': return <AlertTriangle className="w-5 h-5" />
      case 'low': return <CheckCircle className="w-5 h-5" />
      default: return <Info className="w-5 h-5" />
    }
  }

  return (
    <div className="mx-4 mb-4 p-4 border rounded-lg bg-gray-50">
      <div className="flex items-center space-x-2 mb-3">
        <Info className="w-5 h-5 text-blue-500" />
        <h3 className="font-semibold text-gray-800">Symptom Analysis</h3>
      </div>

      {/* Symptoms */}
      {analysis.symptoms.length > 0 && (
        <div className="mb-3">
          <h4 className="text-sm font-medium text-gray-700 mb-1">Identified Symptoms:</h4>
          <div className="flex flex-wrap gap-1">
            {analysis.symptoms.map((symptom, index) => (
              <span
                key={index}
                className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded-full"
              >
                {symptom}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Severity Score */}
      <div className="mb-3">
        <h4 className="text-sm font-medium text-gray-700 mb-1">Severity Score:</h4>
        <div className="flex items-center space-x-2">
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div
              className={`h-2 rounded-full ${
                analysis.severity_score >= 7 ? 'bg-red-500' :
                analysis.severity_score >= 4 ? 'bg-yellow-500' : 'bg-green-500'
              }`}
              style={{ width: `${(analysis.severity_score / 10) * 100}%` }}
            ></div>
          </div>
          <span className="text-sm font-medium">{analysis.severity_score}/10</span>
        </div>
      </div>

      {/* Risk Level */}
      <div className="mb-3">
        <h4 className="text-sm font-medium text-gray-700 mb-1">Risk Level:</h4>
        <div className={`inline-flex items-center space-x-2 px-3 py-1 rounded-full border ${getRiskColor(analysis.risk_level)}`}>
          {getRiskIcon(analysis.risk_level)}
          <span className="text-sm font-medium capitalize">{analysis.risk_level}</span>
        </div>
      </div>

      {/* Possible Conditions */}
      {analysis.possible_conditions.length > 0 && (
        <div className="mb-3">
          <h4 className="text-sm font-medium text-gray-700 mb-1">Possible General Conditions:</h4>
          <ul className="text-sm text-gray-600 space-y-1">
            {analysis.possible_conditions.map((condition, index) => (
              <li key={index} className="flex items-start space-x-2">
                <span className="text-gray-400">•</span>
                <span>{condition}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Urgency Recommendation */}
      <div className="mb-3">
        <h4 className="text-sm font-medium text-gray-700 mb-1">Recommendation:</h4>
        <div className={`p-3 rounded-lg ${
          analysis.risk_level === 'high' ? 'bg-red-50 border border-red-200' :
          analysis.risk_level === 'medium' ? 'bg-yellow-50 border border-yellow-200' :
          'bg-green-50 border border-green-200'
        }`}>
          <p className="text-sm text-gray-800">{analysis.urgency_recommendation}</p>
        </div>
      </div>

      {/* Medical Disclaimer */}
      <div className="mt-4 p-3 bg-yellow-50 border border-yellow-200 rounded-lg">
        <div className="flex items-start space-x-2">
          <AlertTriangle className="w-5 h-5 text-yellow-600 flex-shrink-0 mt-0.5" />
          <div>
            <h4 className="text-sm font-medium text-yellow-800 mb-1">Medical Disclaimer</h4>
            <p className="text-xs text-yellow-700">
              This is not medical advice. Please consult a healthcare professional for proper diagnosis and treatment.
              This analysis is for informational purposes only.
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}