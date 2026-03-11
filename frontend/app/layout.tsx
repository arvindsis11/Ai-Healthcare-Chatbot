import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import '../styles/globals.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'AI Healthcare Assistant',
  description: 'Your AI-powered healthcare companion',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={`${inter.className} min-h-screen bg-white text-slate-900 antialiased dark:bg-gray-900 dark:text-gray-100`}>
        <main className="min-h-screen">
          {children}
        </main>
      </body>
    </html>
  )
}