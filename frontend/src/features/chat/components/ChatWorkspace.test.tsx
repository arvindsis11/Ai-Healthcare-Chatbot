import { render, screen } from '@testing-library/react'
import ChatWorkspace from './ChatWorkspace'

describe('ChatWorkspace', () => {
  it('renders healthcare platform title', () => {
    render(<ChatWorkspace />)
    expect(screen.getByText('AI Healthcare Platform')).toBeInTheDocument()
  })
})
