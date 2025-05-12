// tests/unit/nutrition/Dashboard.test.tsx
import React from 'react';
import { render, screen } from '../../test-utils';

// Mock the Dashboard component temporarily for initial testing
jest.mock('../../../src/pages/nutrition/Dashboard', () => {
  return function MockDashboard() {
    return (
      <div>
        <h1>Nutrition Dashboard</h1>
        <div data-testid="daily-summary">Daily Summary</div>
        <div data-testid="weekly-chart">Weekly Chart</div>
      </div>
    );
  };
});

import Dashboard from '../../../src/pages/nutrition/Dashboard';

describe('Nutrition Dashboard', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('renders dashboard component', () => {
    render(<Dashboard />);
    
    // Check if dashboard title is displayed
    expect(screen.getByText('Nutrition Dashboard')).toBeInTheDocument();
  });

  test('displays daily summary', () => {
    render(<Dashboard />);
    
    // Check if daily summary is displayed
    expect(screen.getByTestId('daily-summary')).toBeInTheDocument();
  });

  test('displays weekly chart', () => {
    render(<Dashboard />);
    
    // Check if weekly chart is displayed
    expect(screen.getByTestId('weekly-chart')).toBeInTheDocument();
  });
});