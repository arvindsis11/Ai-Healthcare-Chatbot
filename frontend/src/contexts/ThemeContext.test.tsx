import { act, render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { ThemeProvider, useTheme } from './ThemeContext'

// Minimal consumer component to expose context values in tests
function ThemeConsumer() {
  const { theme, toggle } = useTheme()
  return (
    <div>
      <span data-testid="theme">{theme}</span>
      <button onClick={toggle}>toggle</button>
    </div>
  )
}

function renderWithProvider() {
  return render(
    <ThemeProvider>
      <ThemeConsumer />
    </ThemeProvider>
  )
}

describe('ThemeContext', () => {
  beforeEach(() => {
    localStorage.clear()
    document.documentElement.classList.remove('dark')
  })

  it('defaults to light when no class or localStorage value present', () => {
    renderWithProvider()
    expect(screen.getByTestId('theme')).toHaveTextContent('light')
  })

  it('reads dark theme from the class already on <html>', () => {
    document.documentElement.classList.add('dark')
    renderWithProvider()
    expect(screen.getByTestId('theme')).toHaveTextContent('dark')
  })

  it('toggle switches from light to dark', async () => {
    renderWithProvider()
    await userEvent.click(screen.getByRole('button', { name: 'toggle' }))
    expect(screen.getByTestId('theme')).toHaveTextContent('dark')
  })

  it('toggle switches from dark to light', async () => {
    document.documentElement.classList.add('dark')
    renderWithProvider()
    await userEvent.click(screen.getByRole('button', { name: 'toggle' }))
    expect(screen.getByTestId('theme')).toHaveTextContent('light')
  })

  it('toggle adds dark class to <html>', async () => {
    renderWithProvider()
    await userEvent.click(screen.getByRole('button', { name: 'toggle' }))
    expect(document.documentElement.classList.contains('dark')).toBe(true)
  })

  it('toggle removes dark class from <html>', async () => {
    document.documentElement.classList.add('dark')
    renderWithProvider()
    await userEvent.click(screen.getByRole('button', { name: 'toggle' }))
    expect(document.documentElement.classList.contains('dark')).toBe(false)
  })

  it('toggle persists preference to localStorage', async () => {
    renderWithProvider()
    await userEvent.click(screen.getByRole('button', { name: 'toggle' }))
    expect(localStorage.getItem('theme')).toBe('dark')
  })

  it('toggling twice saves light to localStorage', async () => {
    renderWithProvider()
    await userEvent.click(screen.getByRole('button', { name: 'toggle' }))
    await userEvent.click(screen.getByRole('button', { name: 'toggle' }))
    expect(localStorage.getItem('theme')).toBe('light')
  })

  describe('live OS theme changes', () => {
    let listeners: Array<(e: MediaQueryListEvent) => void>

    beforeEach(() => {
      listeners = []
      // Override the base stub to capture 'change' event listeners
      window.matchMedia = jest.fn().mockReturnValue({
        matches: false,
        addEventListener: (_: string, cb: (e: MediaQueryListEvent) => void) => listeners.push(cb),
        removeEventListener: jest.fn(),
      })
    })

    it('follows OS change to dark when no explicit preference is set', () => {
      renderWithProvider()
      act(() => listeners.forEach((cb) => cb({ matches: true } as MediaQueryListEvent)))
      expect(screen.getByTestId('theme')).toHaveTextContent('dark')
      expect(document.documentElement.classList.contains('dark')).toBe(true)
    })

    it('follows OS change to light when no explicit preference is set', () => {
      document.documentElement.classList.add('dark')
      renderWithProvider()
      act(() => listeners.forEach((cb) => cb({ matches: false } as MediaQueryListEvent)))
      expect(screen.getByTestId('theme')).toHaveTextContent('light')
      expect(document.documentElement.classList.contains('dark')).toBe(false)
    })

    it('ignores OS change when user has an explicit localStorage preference', () => {
      localStorage.setItem('theme', 'light')
      renderWithProvider()
      act(() => listeners.forEach((cb) => cb({ matches: true } as MediaQueryListEvent)))
      expect(screen.getByTestId('theme')).toHaveTextContent('light')
      expect(document.documentElement.classList.contains('dark')).toBe(false)
    })
  })
})
