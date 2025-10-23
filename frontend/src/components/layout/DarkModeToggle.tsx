import React from 'react';
import { Moon, Sun } from 'lucide-react';
import { useTheme } from '@/context/ThemeContext';

export const DarkModeToggle: React.FC = () => {
  const { isDarkMode, toggleDarkMode } = useTheme();

  return (
    <button
      onClick={toggleDarkMode}
      className="p-2 rounded-lg bg-light-border dark:bg-dark-border text-light-text dark:text-yellow-400 hover:bg-light-border/70 dark:hover:bg-dark-border/70 transition-all duration-300 border border-app shadow-sm"
      aria-label="Toggle dark mode"
      title={isDarkMode ? 'Switch to light mode' : 'Switch to dark mode'}
    >
      {isDarkMode ? <Sun size={20} className="animate-pulse" /> : <Moon size={20} />}
    </button>
  );
};
