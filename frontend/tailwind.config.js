/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          50: '#eff6ff',
          200: '#9fc6ff',
          400: '#4496ff',
          500: '#1b7bff',
          600: '#0f63d6',
          700: '#124fa7',
        },
      },
      boxShadow: {
        glow: '0 12px 42px rgba(27, 123, 255, 0.28)',
      },
      keyframes: {
        pulseSoft: {
          '0%, 100%': { opacity: '0.55' },
          '50%': { opacity: '1' },
        },
      },
      animation: {
        pulseSoft: 'pulseSoft 2.2s ease-in-out infinite',
      },
    },
  },
  plugins: [],
}