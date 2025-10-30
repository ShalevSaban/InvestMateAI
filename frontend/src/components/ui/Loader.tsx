import React from 'react';

export const Loader: React.FC<{ text?: string }> = ({ text = 'Loading agents...' }) => {
  return (
    <div className="fixed inset-0 flex flex-col items-center justify-center bg-white/90 dark:bg-gray-900/90 backdrop-blur-sm z-50">
      <div className="relative flex items-center justify-center">
        <div className="absolute animate-ping h-16 w-16 rounded-full bg-primary-400 opacity-75"></div>
        <div className="animate-spin rounded-full h-12 w-12 border-t-4 border-b-4 border-primary-500"></div>
      </div>
      <p className="mt-6 text-primary-700 dark:text-primary-200 font-semibold text-lg animate-fade-in">
        {text}
      </p>
    </div>
  );
};
