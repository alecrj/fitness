import React from 'react';

interface SpinnerProps {
  size?: 'sm' | 'md' | 'lg';
  color?: string;
  className?: string;
}

/**
 * Loading spinner component with configurable size and color
 */
const Spinner: React.FC<SpinnerProps> = ({ 
  size = 'md', 
  color = 'text-blue-600',
  className = '' 
}) => {
  // Size classes
  const sizeClass = {
    sm: 'h-4 w-4',
    md: 'h-8 w-8',
    lg: 'h-12 w-12'
  };

  // Border width based on size
  const borderWidth = {
    sm: 'border-2',
    md: 'border-3',
    lg: 'border-4'
  };

  return (
    <div 
      className={`
        ${sizeClass[size]} 
        ${borderWidth[size]} 
        ${color} 
        rounded-full 
        animate-spin 
        border-b-transparent
        ${className}
      `}
      style={{ borderStyle: 'solid' }}
      role="status"
      aria-label="Loading"
    >
      <span className="sr-only">Loading...</span>
    </div>
  );
};

export default Spinner;