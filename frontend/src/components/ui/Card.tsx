import React from 'react';

interface CardProps {
  children: React.ReactNode;
  className?: string;
  padding?: 'none' | 'sm' | 'md' | 'lg';
  hover?: boolean;
}

export const Card: React.FC<CardProps> = ({
  children,
  className = '',
  padding = 'md',
  hover = false,
}) => {
  const paddingClasses = {
    none: '',
    sm: 'p-4',
    md: 'p-6',
    lg: 'p-8',
  };

  const hoverClass = hover ? 'hover:shadow-lg hover:-translate-y-1 transition-all duration-200' : '';

  return (
    <div
      className={`
        bg-light-card dark:bg-dark-card
        rounded-xl
        shadow-soft
        border border-light-border dark:border-dark-border
        transition-all duration-300
        ${paddingClasses[padding]}
        ${hoverClass}
        ${className}
      `}
    >
      {children}
    </div>
  );
};
