// src/setupTests.ts
import '@testing-library/jest-dom';

// Mock window.matchMedia
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: jest.fn().mockImplementation(query => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: jest.fn(),
    removeListener: jest.fn(),
    addEventListener: jest.fn(),
    removeEventListener: jest.fn(),
    dispatchEvent: jest.fn(),
  })),
});

// Mock IntersectionObserver with proper TypeScript types
declare global {
  interface Window {
    IntersectionObserver: typeof IntersectionObserver;
    ResizeObserver: typeof ResizeObserver;
  }
}

// Create IntersectionObserver mock
const IntersectionObserverMock = jest.fn().mockImplementation(() => ({
  observe: jest.fn(),
  unobserve: jest.fn(),
  disconnect: jest.fn(),
}));

global.IntersectionObserver = IntersectionObserverMock as any;

// Create ResizeObserver mock
const ResizeObserverMock = jest.fn().mockImplementation(() => ({
  observe: jest.fn(),
  unobserve: jest.fn(),
  disconnect: jest.fn(),
}));

global.ResizeObserver = ResizeObserverMock as any;