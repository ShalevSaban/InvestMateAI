import React from 'react';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  fullWidth?: boolean;
  children: React.ReactNode;
}

export const Button: React.FC<ButtonProps> = ({
  variant = 'primary',
  size = 'md',
  fullWidth = false,
  children,
  className = '',
  disabled,
  ...props
}) => {
  const baseStyles = 'font-semibold rounded-lg transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed';

  const variants = {
    primary: 'bg-primary-light hover:bg-primary-hover dark:bg-primary-dark dark:hover:bg-primary-hoverDark text-white focus:ring-primary-light dark:focus:ring-primary-dark',
    secondary: 'bg-accent-light hover:bg-accent-light/80 dark:bg-accent-dark dark:hover:bg-accent-dark/80 text-white focus:ring-accent-light dark:focus:ring-accent-dark',
    outline: 'border-2 border-primary-light dark:border-primary-dark text-primary-light dark:text-primary-dark hover:bg-primary-light/10 dark:hover:bg-primary-dark/10 focus:ring-primary-light dark:focus:ring-primary-dark',
    ghost: 'text-light-textSecondary dark:text-dark-textSecondary hover:bg-light-border dark:hover:bg-dark-border focus:ring-primary-light dark:focus:ring-primary-dark',
  };

  const sizes = {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-4 py-2 text-base',
    lg: 'px-6 py-3 text-lg',
  };

  const widthClass = fullWidth ? 'w-full' : '';

  return (
    <button
      className={`${baseStyles} ${variants[variant]} ${sizes[size]} ${widthClass} ${className}`}
      disabled={disabled}
      {...props}
    >
      {children}
    </button>
  );
};
