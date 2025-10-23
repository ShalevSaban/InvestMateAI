import React from 'react';
import { Moon, Sun } from 'lucide-react';
import { useTheme } from '@/context/ThemeContext';

export const DarkModeToggle: React.FC = () => {
  const { isDarkMode, toggleDarkMode } = useTheme();

  return (
    <button
      onClick={toggleDarkMode}
      className="p-2 rounded-lg bg-gray-200 dark:bg-dark-hover text-gray-800 dark:text-gray-200 hover:bg-gray-300 dark:hover:bg-gray-600 transition-colors"
      aria-label="Toggle dark mode"
    >
      {isDarkMode ? <Sun size={20} /> : <Moon size={20} />}
    </button>
  );
};
