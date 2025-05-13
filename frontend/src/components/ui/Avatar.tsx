import React from 'react';

interface AvatarProps {
  src?: string;
  alt?: string;
  name?: string;
  size?: 'sm' | 'md' | 'lg' | 'xl' | '2xl';
  showOnlineStatus?: boolean;
  isOnline?: boolean;
}

const sizeClasses = {
  sm: 'h-6 w-6',
  md: 'h-8 w-8',
  lg: 'h-10 w-10',
  xl: 'h-12 w-12',
  '2xl': 'h-16 w-16',
};

const statusSizeClasses = {
  sm: 'h-2 w-2',
  md: 'h-2.5 w-2.5',
  lg: 'h-3 w-3',
  xl: 'h-3.5 w-3.5',
  '2xl': 'h-4 w-4',
};

/**
 * Avatar component with optional online status indicator
 */
export const Avatar: React.FC<AvatarProps> = ({
  src,
  alt,
  name,
  size = 'md',
  showOnlineStatus = false,
  isOnline = false,
}) => {
  const getInitials = (name: string): string => {
    return name
      .split(' ')
      .map(part => part[0])
      .join('')
      .toUpperCase()
      .slice(0, 2);
  };

  const fallbackInitials = name ? getInitials(name) : '?';

  return (
    <div className="relative inline-flex items-center justify-center">
      {src ? (
        <img
          className={`${sizeClasses[size]} rounded-full object-cover`}
          src={src}
          alt={alt || name || 'Avatar'}
        />
      ) : (
        <div
          className={`${sizeClasses[size]} rounded-full bg-gray-200 flex items-center justify-center text-gray-600 font-medium`}
        >
          <span className={size === 'sm' ? 'text-xs' : size === 'lg' || size === 'xl' || size === '2xl' ? 'text-lg' : 'text-sm'}>
            {fallbackInitials}
          </span>
        </div>
      )}
      
      {showOnlineStatus && (
        <span
          className={`absolute bottom-0 right-0 block ${statusSizeClasses[size]} rounded-full ring-2 ring-white ${
            isOnline ? 'bg-green-400' : 'bg-gray-400'
          }`}
        />
      )}
    </div>
  );
};