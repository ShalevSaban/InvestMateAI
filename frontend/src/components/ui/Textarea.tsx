import React from 'react';

interface TextareaProps extends React.TextareaHTMLAttributes<HTMLTextAreaElement> {
  label?: string;
  error?: string;
  fullWidth?: boolean;
}

export const Textarea: React.FC<TextareaProps> = ({
  label,
  error,
  fullWidth = true,
  className = '',
  ...props
}) => {
  const widthClass = fullWidth ? 'w-full' : '';

  return (
    <div className={`${widthClass}`}>
      {label && (
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
          {label}
        </label>
      )}
      <textarea
        className={`
          ${widthClass}
          px-4 py-2
          border border-gray-300 dark:border-gray-600
          rounded-lg
          bg-white dark:bg-dark-card
          text-gray-900 dark:text-white
          placeholder-gray-400 dark:placeholder-gray-500
          focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent
          transition-colors
          resize-vertical
          ${error ? 'border-red-500 focus:ring-red-500' : ''}
          ${className}
        `}
        {...props}
      />
      {error && (
        <p className="mt-1 text-sm text-red-600 dark:text-red-400">{error}</p>
      )}
    </div>
  );
};
