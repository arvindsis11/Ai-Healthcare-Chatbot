import { ActivitySquare, ShieldAlert, Stethoscope, Users } from 'lucide-react'
import * as Accordion from '@radix-ui/react-accordion'
import type { DoctorRecommendation, SymptomAnalysis } from '../types/chat'

interface SymptomAnalysisPanelProps {
  analysis?: SymptomAnalysis
  specialist?: string
  doctorRecommendation?: DoctorRecommendation
}

function severityTone(level: SymptomAnalysis['risk_level']) {
  if (level === 'high') return 'text-red-700 bg-red-50 border-red-200 dark:text-red-300 dark:bg-red-500/10 dark:border-red-700/50'
  if (level === 'medium') return 'text-yellow-700 bg-yellow-50 border-yellow-200 dark:text-yellow-300 dark:bg-yellow-500/10 dark:border-yellow-700/50'
  return 'text-green-700 bg-green-50 border-green-200 dark:text-green-300 dark:bg-green-500/10 dark:border-green-700/50'
}

function confidenceLabel(confidence: number): string {
  if (confidence >= 0.8) return 'High'
  if (confidence >= 0.5) return 'Moderate'
  return 'Low'
}

function confidenceColor(confidence: number): string {
  if (confidence >= 0.8) return 'bg-green-500'
  if (confidence >= 0.5) return 'bg-yellow-500'
  return 'bg-slate-400'
}

export default function SymptomAnalysisPanel({ analysis, specialist, doctorRecommendation }: SymptomAnalysisPanelProps) {
  if (!analysis) {
    return null
  }

  return (
    <aside className="panel-surface rounded-2xl border border-slate-200/80 p-4 dark:border-slate-700/80">
      <h3 className="mb-3 inline-flex items-center gap-2 text-sm font-semibold">
        <ActivitySquare className="h-4 w-4" />
        Symptom Analysis
      </h3>
      <div className={`mb-3 rounded-lg border px-3 py-2 text-sm ${severityTone(analysis.risk_level)}`}>
        Risk: {analysis.risk_level.toUpperCase()} ({analysis.severity_score}/10)
      </div>
      <p className="mb-2 text-xs font-semibold uppercase tracking-wide text-slate-500">Symptoms</p>
      <p className="mb-3 text-sm text-slate-700 dark:text-slate-200">{analysis.symptoms.join(', ') || 'No clear symptoms detected'}</p>
      <p className="mb-2 text-xs font-semibold uppercase tracking-wide text-slate-500">Urgency</p>
      <p className="mb-3 inline-flex items-start gap-2 text-sm text-slate-700 dark:text-slate-200">
        <ShieldAlert className="mt-0.5 h-4 w-4" />
        {analysis.urgency_recommendation}
      </p>
      {!!analysis.possible_conditions.length && (
        <Accordion.Root type="single" collapsible className="mb-3">
          <Accordion.Item value="conditions" className="rounded-lg border border-slate-200/80 dark:border-slate-700/80">
            <Accordion.Header>
              <Accordion.Trigger className="w-full px-3 py-2 text-left text-xs font-semibold uppercase tracking-wide text-slate-600 dark:text-slate-300">
                Possible Conditions (general guidance)
              </Accordion.Trigger>
            </Accordion.Header>
            <Accordion.Content className="px-3 pb-3 text-sm text-slate-700 dark:text-slate-200">
              {analysis.possible_conditions.join(', ')}
            </Accordion.Content>
          </Accordion.Item>
        </Accordion.Root>
      )}

      {doctorRecommendation ? (
        <div className="rounded-lg border border-blue-200 bg-blue-50 p-3 dark:border-blue-700/50 dark:bg-blue-500/10">
          <p className="mb-2 inline-flex items-center gap-2 text-sm font-semibold text-blue-700 dark:text-blue-300">
            <Stethoscope className="h-4 w-4" />
            Recommended: {doctorRecommendation.specialist}
          </p>
          <div className="mb-2 flex items-center gap-2">
            <div className="h-1.5 flex-1 rounded-full bg-slate-200 dark:bg-slate-700">
              <div
                className={`h-1.5 rounded-full ${confidenceColor(doctorRecommendation.confidence)}`}
                style={{ width: `${doctorRecommendation.confidence * 100}%` }}
              />
            </div>
            <span className="text-xs text-slate-500 dark:text-slate-400">
              {confidenceLabel(doctorRecommendation.confidence)} confidence
            </span>
          </div>
          <p className="mb-2 text-xs text-slate-600 dark:text-slate-300">
            {doctorRecommendation.reasoning}
          </p>
          {doctorRecommendation.alternative_specialists.length > 0 && (
            <p className="inline-flex items-center gap-2 text-xs text-slate-500 dark:text-slate-400">
              <Users className="h-3.5 w-3.5" />
              Also consider: {doctorRecommendation.alternative_specialists.join(', ')}
            </p>
          )}
        </div>
      ) : specialist ? (
        <p className="inline-flex items-center gap-2 rounded-lg bg-blue-50 px-3 py-2 text-sm text-blue-700 dark:bg-blue-500/10 dark:text-blue-300">
          <Stethoscope className="h-4 w-4" />
          Recommended specialist: {specialist}
        </p>
      ) : null}
    </aside>
  )
}
