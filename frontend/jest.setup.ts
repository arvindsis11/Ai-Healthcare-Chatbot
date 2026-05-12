import '@testing-library/jest-dom'

// jsdom does not implement window.matchMedia — stub it globally for all tests.
// addListener/removeListener are included for framer-motion compatibility.
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: jest.fn().mockImplementation((query: string) => ({
    matches: false,
    media: query,
    addEventListener: jest.fn(),
    removeEventListener: jest.fn(),
    addListener: jest.fn(),
    removeListener: jest.fn(),
  })),
})
