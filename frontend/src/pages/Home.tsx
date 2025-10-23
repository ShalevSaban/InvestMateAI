import React from 'react';
import { Link } from 'react-router-dom';
import { LogIn, UserPlus, MessageCircle, Send } from 'lucide-react';
import { Card } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';

export const Home: React.FC = () => {
  return (
    <div className="max-w-4xl mx-auto">
      <div className="text-center mb-12">
        {/* Logo Placeholder */}
        <div className="flex justify-center mb-6">
          <div className="w-32 h-32 bg-gradient-to-br from-primary-light to-accent-light dark:from-primary-dark dark:to-accent-dark rounded-3xl flex items-center justify-center shadow-soft">
            <span className="text-white font-bold text-5xl">IM</span>
          </div>
        </div>

        <h1 className="text-5xl font-bold text-light-text dark:text-dark-text mb-4">
          Welcome to InvestMateAI
        </h1>
        <p className="text-xl text-light-textSecondary dark:text-dark-textSecondary max-w-2xl mx-auto">
          Your AI-powered real estate assistant. Connect with professional agents,
          discover properties, and make informed investment decisions.
        </p>
      </div>

      <div className="grid md:grid-cols-2 gap-6 mb-8">
        <Card padding="lg" hover>
          <div className="flex flex-col items-center text-center space-y-4">
            <div className="w-16 h-16 bg-primary-light/10 dark:bg-primary-dark/20 rounded-full flex items-center justify-center border border-primary-light/30 dark:border-primary-dark/30">
              <LogIn size={32} className="text-primary-light dark:text-primary-dark" />
            </div>
            <h2 className="text-2xl font-bold text-light-text dark:text-dark-text">
              Agent Login
            </h2>
            <p className="text-light-textSecondary dark:text-dark-textSecondary">
              Access your dashboard, manage properties, and view client interactions
            </p>
            <Link to="/login" className="w-full">
              <Button fullWidth size="lg">
                Login
              </Button>
            </Link>
          </div>
        </Card>

        <Card padding="lg" hover>
          <div className="flex flex-col items-center text-center space-y-4">
            <div className="w-16 h-16 bg-accent-light/10 dark:bg-accent-dark/20 rounded-full flex items-center justify-center border border-accent-light/30 dark:border-accent-dark/30">
              <UserPlus size={32} className="text-accent-light dark:text-accent-dark" />
            </div>
            <h2 className="text-2xl font-bold text-light-text dark:text-dark-text">
              Register as Agent
            </h2>
            <p className="text-light-textSecondary dark:text-dark-textSecondary">
              Join our network of real estate professionals and grow your business
            </p>
            <Link to="/register" className="w-full">
              <Button fullWidth size="lg" variant="secondary">
                Register
              </Button>
            </Link>
          </div>
        </Card>
      </div>

      <Card padding="lg" className="bg-gradient-to-r from-primary-light to-accent-light dark:from-primary-dark dark:to-accent-dark border-none">
        <div className="flex flex-col md:flex-row items-center justify-between text-white space-y-4 md:space-y-0">
          <div className="flex items-center space-x-4">
            <div className="w-12 h-12 bg-white/20 rounded-full flex items-center justify-center backdrop-blur-sm">
              <MessageCircle size={28} />
            </div>
            <div>
              <h3 className="text-2xl font-bold">Ask Our AI Agent</h3>
              <p className="text-white/90">
                Search properties and get instant answers as a client
              </p>
            </div>
          </div>
          <Link to="/chat">
            <Button variant="outline" size="lg" className="border-white text-white hover:bg-white/20 backdrop-blur-sm">
              Start Chat
            </Button>
          </Link>
        </div>
      </Card>

      <div className="mt-8 text-center">
        <a
          href="https://t.me/InvestMateAI_bot"
          target="_blank"
          rel="noopener noreferrer"
          className="inline-flex items-center space-x-2 text-primary-light dark:text-primary-dark hover:text-primary-hover dark:hover:text-primary-hoverDark transition-colors font-semibold"
        >
          <Send size={20} />
          <span>Chat via Telegram</span>
        </a>
      </div>
    </div>
  );
};
