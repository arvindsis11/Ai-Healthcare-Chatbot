import type { Metadata } from 'next'
import type { ReactNode } from 'react'
import { Space_Grotesk } from 'next/font/google'
import '../styles/globals.css'
import { ThemeProvider } from '../contexts/ThemeContext'

const spaceGrotesk = Space_Grotesk({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'AI Healthcare Assistant',
  description: 'Your AI-powered healthcare companion',
}

export default function RootLayout({
  children,
}: {
  children: ReactNode
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <head>
        {/* Inline script: sets dark class before React hydrates to prevent flash */}
        <script
          dangerouslySetInnerHTML={{
            __html: `try{var t=localStorage.getItem('theme')||(window.matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light');document.documentElement.classList.toggle('dark',t==='dark')}catch(e){}`,
          }}
        />
      </head>
      <body className={`${spaceGrotesk.className} min-h-screen antialiased`}>
        <ThemeProvider>
          <main className="min-h-screen">
            {children}
          </main>
        </ThemeProvider>
      </body>
    </html>
  )
}
