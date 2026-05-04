import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { ThemeProvider } from '../../../contexts/ThemeContext'
import ChatWorkspace from './ChatWorkspace'

function renderWorkspace() {
  return render(
    <ThemeProvider>
      <ChatWorkspace />
    </ThemeProvider>
  )
}

beforeEach(() => {
  localStorage.clear()
  document.documentElement.classList.remove('dark')
})

describe('ChatWorkspace', () => {
  it('renders healthcare platform title', () => {
    renderWorkspace()
    expect(screen.getByText('AI Healthcare Platform')).toBeInTheDocument()
  })

  it('renders the welcome message', () => {
    renderWorkspace()
    expect(
      screen.getByText(/Share your symptoms for general guidance/i)
    ).toBeInTheDocument()
  })

  it('renders the medical disclaimer banner', () => {
    renderWorkspace()
    expect(
      screen.getByText(/educational information only/i)
    ).toBeInTheDocument()
  })

  it('renders the dark mode toggle button', () => {
    renderWorkspace()
    // aria-label is either "Switch to dark mode" or "Switch to light mode"
    expect(
      screen.getByRole('button', { name: /switch to (dark|light) mode/i })
    ).toBeInTheDocument()
  })

  it('dark mode toggle switches theme on click', async () => {
    renderWorkspace()
    const toggleBtn = screen.getByRole('button', { name: /switch to dark mode/i })
    await userEvent.click(toggleBtn)
    expect(document.documentElement.classList.contains('dark')).toBe(true)
    // Button label should have flipped
    expect(
      screen.getByRole('button', { name: /switch to light mode/i })
    ).toBeInTheDocument()
  })

  it('renders the mobile sidebar hamburger button', () => {
    renderWorkspace()
    expect(screen.getByRole('button', { name: 'Open sidebar' })).toBeInTheDocument()
  })

  it('hamburger button opens the mobile sidebar overlay', async () => {
    const { container } = renderWorkspace()
    expect(container.querySelector('[aria-hidden="true"]')).toBeNull()
    await userEvent.click(screen.getByRole('button', { name: 'Open sidebar' }))
    expect(container.querySelector('[aria-hidden="true"]')).toBeInTheDocument()
  })
})
