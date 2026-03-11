interface MetricsCardsProps {
  metrics: Array<{ label: string; value: string; delta: string }>
}

export default function MetricsCards({ metrics }: MetricsCardsProps) {
  return (
    <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
      {metrics.map((metric) => (
        <article key={metric.label} className="panel-surface rounded-xl border border-slate-200/70 p-4 dark:border-slate-700/70">
          <p className="text-xs uppercase tracking-wide text-slate-500">{metric.label}</p>
          <p className="mt-2 text-2xl font-semibold">{metric.value}</p>
          <p className="mt-1 text-xs text-emerald-600">{metric.delta}</p>
        </article>
      ))}
    </div>
  )
}
