import React from 'react';

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  fullWidth?: boolean;
}

export const Input: React.FC<InputProps> = ({
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
        <label className="block text-sm font-medium text-light-textSecondary dark:text-dark-textSecondary mb-1">
          {label}
        </label>
      )}
      <input
        className={`
          ${widthClass}
          px-4 py-2
          border border-light-border dark:border-dark-border
          rounded-lg
          bg-light-card dark:bg-dark-card
          text-light-text dark:text-dark-text
          placeholder-light-textSecondary/60 dark:placeholder-dark-textSecondary/60
          focus:outline-none focus:ring-2 focus:ring-primary-light dark:focus:ring-primary-dark focus:border-transparent
          transition-all duration-200
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
