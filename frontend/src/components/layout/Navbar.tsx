import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Home, LogOut, LayoutDashboard } from 'lucide-react';
import { DarkModeToggle } from './DarkModeToggle';
import { useAuth } from '@/context/AuthContext';
import { Button } from '@/components/ui/Button';

export const Navbar: React.FC = () => {
  const { isAuthenticated, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <nav className="bg-light-card dark:bg-dark-card shadow-soft sticky top-0 z-50 transition-all duration-300 border-b border-light-border dark:border-dark-border">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <Link to="/" className="flex items-center space-x-2">
            <div className="w-10 h-10 bg-gradient-to-br from-primary-light to-accent-light dark:from-primary-dark dark:to-accent-dark rounded-lg flex items-center justify-center shadow-md">
              <span className="text-white font-bold text-xl">IM</span>
            </div>
            <span className="text-xl font-bold text-light-text dark:text-dark-text">
              InvestMateAI
            </span>
          </Link>

          <div className="flex items-center space-x-4">
            <Link
              to="/"
              className="text-light-textSecondary dark:text-dark-textSecondary hover:text-primary-light dark:hover:text-primary-dark transition-colors flex items-center space-x-1"
            >
              <Home size={20} />
              <span className="hidden sm:inline">Home</span>
            </Link>

            {isAuthenticated && (
              <Link
                to="/dashboard"
                className="text-light-textSecondary dark:text-dark-textSecondary hover:text-primary-light dark:hover:text-primary-dark transition-colors flex items-center space-x-1"
              >
                <LayoutDashboard size={20} />
                <span className="hidden sm:inline">Dashboard</span>
              </Link>
            )}

            <DarkModeToggle />

            {isAuthenticated && (
              <Button
                variant="ghost"
                size="sm"
                onClick={handleLogout}
                className="flex items-center space-x-1"
              >
                <LogOut size={18} />
                <span className="hidden sm:inline">Logout</span>
              </Button>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
};
