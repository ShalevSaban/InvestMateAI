import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Home, LogOut, LayoutDashboard } from 'lucide-react';
// import { DarkModeToggle } from './DarkModeToggle';
import { useAuth } from '@/context/AuthContext';
import { useTheme } from '@/context/ThemeContext';
import { Button } from '@/components/ui/Button';
import logoBright from '@/assets/logo bright.png';
import logoDark from '@/assets/logo dark.png';

export const Navbar: React.FC = () => {
  const { isAuthenticated, logout } = useAuth();
  const { isDarkMode } = useTheme();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <nav className="bg-app-card shadow-soft sticky top-0 z-50 transition-all duration-300 border-b border-app">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <Link to="/" className="flex items-center">
            <img
              src={isDarkMode ? logoDark : logoBright}
              alt="InvestMateAI"
              className="h-10 w-auto object-contain"
            />
          </Link>

          <div className="flex items-center space-x-4">
            <Link
              to="/"
              className="text-app-secondary hover:text-btn-primary transition-colors flex items-center space-x-1"
            >
              <Home size={20} />
              <span className="hidden sm:inline">Home</span>
            </Link>

            {isAuthenticated && (
              <Link
                to="/dashboard"
                className="text-app-secondary hover:text-btn-primary transition-colors flex items-center space-x-1"
              >
                <LayoutDashboard size={20} />
                <span className="hidden sm:inline">Dashboard</span>
              </Link>
            )}

            {/* <DarkModeToggle /> */}

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
