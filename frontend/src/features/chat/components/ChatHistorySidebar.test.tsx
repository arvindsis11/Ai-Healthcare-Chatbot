import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import ChatHistorySidebar from './ChatHistorySidebar'

const baseProps = {
  items: [{ id: 'conv-1', label: 'Headache symptoms' }],
  activeId: null as string | null,
  onSelect: jest.fn(),
  onNewChat: jest.fn(),
  onClose: jest.fn(),
}

beforeEach(() => jest.clearAllMocks())

describe('ChatHistorySidebar — desktop', () => {
  it('renders conversation items', () => {
    render(<ChatHistorySidebar {...baseProps} isOpen={false} />)
    // Both desktop and mobile asides are in the DOM (CSS hides them, not JS)
    expect(screen.getAllByText('Headache symptoms').length).toBeGreaterThanOrEqual(1)
  })

  it('calls onNewChat when New chat is clicked', async () => {
    render(<ChatHistorySidebar {...baseProps} isOpen={false} />)
    await userEvent.click(screen.getAllByRole('button', { name: /new chat/i })[0])
    expect(baseProps.onNewChat).toHaveBeenCalledTimes(1)
  })

  it('calls onSelect with the conversation id', async () => {
    render(<ChatHistorySidebar {...baseProps} isOpen={false} />)
    await userEvent.click(screen.getAllByText('Headache symptoms')[0])
    expect(baseProps.onSelect).toHaveBeenCalledWith('conv-1')
  })

  it('applies active styles to the selected conversation', () => {
    render(<ChatHistorySidebar {...baseProps} activeId="conv-1" isOpen={false} />)
    const activeButtons = screen.getAllByText('Headache symptoms')
    expect(activeButtons[0]).toHaveClass('bg-blue-50')
  })
})

describe('ChatHistorySidebar — mobile overlay', () => {
  it('does not render the backdrop when isOpen is false', () => {
    const { container } = render(<ChatHistorySidebar {...baseProps} isOpen={false} />)
    expect(container.querySelector('[aria-hidden="true"]')).toBeNull()
  })

  it('renders the backdrop when isOpen is true', () => {
    const { container } = render(<ChatHistorySidebar {...baseProps} isOpen={true} />)
    expect(container.querySelector('[aria-hidden="true"]')).toBeInTheDocument()
  })

  it('clicking the backdrop calls onClose', async () => {
    const { container } = render(<ChatHistorySidebar {...baseProps} isOpen={true} />)
    await userEvent.click(container.querySelector('[aria-hidden="true"]') as HTMLElement)
    expect(baseProps.onClose).toHaveBeenCalledTimes(1)
  })

  it('clicking the close button calls onClose', async () => {
    render(<ChatHistorySidebar {...baseProps} isOpen={true} />)
    await userEvent.click(screen.getAllByLabelText('Close sidebar')[0])
    expect(baseProps.onClose).toHaveBeenCalledTimes(1)
  })

  it('selecting a conversation calls both onSelect and onClose', async () => {
    render(<ChatHistorySidebar {...baseProps} isOpen={true} />)
    await userEvent.click(screen.getAllByText('Headache symptoms')[0])
    expect(baseProps.onSelect).toHaveBeenCalledWith('conv-1')
    expect(baseProps.onClose).toHaveBeenCalledTimes(1)
  })
})

