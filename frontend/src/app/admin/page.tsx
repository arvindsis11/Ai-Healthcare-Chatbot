import MetricsCards from '../../features/analytics/components/MetricsCards'

const metrics = [
  { label: 'Daily Active Users', value: '12,480', delta: '+8.2% vs yesterday' },
  { label: 'Avg API Latency', value: '143ms', delta: '-11ms vs yesterday' },
  { label: 'High-Risk Alerts', value: '216', delta: '+4.1% vs yesterday' },
  { label: 'Citation Coverage', value: '96.3%', delta: '+0.8% vs yesterday' },
]

export default function AdminDashboardPage() {
  return (
    <main className="min-h-screen px-4 py-8 md:px-8">
      <header className="mb-6">
        <h1 className="text-2xl font-semibold">Admin Analytics Dashboard</h1>
        <p className="text-sm text-slate-600 dark:text-slate-300">
          Monitor chatbot usage, symptom trends, and performance indicators.
        </p>
      </header>

      <MetricsCards metrics={metrics} />

      <section className="mt-6 grid gap-4 lg:grid-cols-2">
        <article className="panel-surface rounded-xl border border-slate-200/70 p-4 dark:border-slate-700/70">
          <h2 className="mb-2 text-lg font-semibold">Symptom Trends</h2>
          <p className="text-sm text-slate-600 dark:text-slate-300">Top trends: fever, cough, headache, fatigue, sore throat.</p>
        </article>

        <article className="panel-surface rounded-xl border border-slate-200/70 p-4 dark:border-slate-700/70">
          <h2 className="mb-2 text-lg font-semibold">User Activity</h2>
          <p className="text-sm text-slate-600 dark:text-slate-300">Peak usage windows: 08:00-11:00 and 19:00-22:00 local time.</p>
        </article>
      </section>
    </main>
  )
}
