import React from 'react';
import { MessageCircle, RefreshCw, Send } from 'lucide-react';

interface TelegramFallbackProps {
  onRetry?: () => void;
}

export const TelegramFallback: React.FC<TelegramFallbackProps> = ({ onRetry }) => {
  const handleTelegramRedirect = () => {
    window.open('https://t.me/InvestMate_bot', '_blank');
  };

  const handleRetry = () => {
    if (onRetry) {
      onRetry();
    } else {
      window.location.reload();
    }
  };

  return (
    <div className="fixed inset-0 flex flex-col items-center justify-center bg-white/95 dark:bg-gray-900/95 backdrop-blur-sm z-50 transition-all duration-700">
      {/* Animated Icon Container */}
      <div className="relative mb-8">
        {/* Outer glow effect */}
        <div className="absolute inset-0 bg-gradient-to-r from-primary-400 to-purple-500 rounded-full blur-3xl opacity-30 animate-pulse"></div>

        {/* Pulsing ring */}
        <div className="absolute inset-0 animate-ping h-24 w-24 rounded-full bg-primary-400 opacity-20"></div>

        {/* Icon container */}
        <div className="relative w-24 h-24 bg-gradient-to-br from-primary-500 to-purple-600 rounded-full flex items-center justify-center shadow-2xl">
          <MessageCircle size={48} className="text-white" strokeWidth={2.5} />
        </div>
      </div>

      {/* Main Message */}
      <div className="text-center max-w-md px-6 mb-8">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-3">
          Web Chat Temporarily Unavailable
        </h1>
        <p className="text-lg text-gray-600 dark:text-gray-300 mb-2">
          We're having trouble loading the chat agents right now.
        </p>
        <p className="text-base text-gray-500 dark:text-gray-400">
          Don't worry! You can still chat with our AI through Telegram.
        </p>
      </div>

      {/* Action Buttons */}
      <div className="flex flex-col sm:flex-row gap-4 w-full max-w-md px-6">
        {/* Telegram Button - Primary */}
        <button
          onClick={handleTelegramRedirect}
          className="flex-1 group relative px-6 py-4 rounded-xl
            bg-gradient-to-r from-primary-500 via-primary-600 to-purple-600
            hover:from-primary-600 hover:via-primary-700 hover:to-purple-700
            text-white font-semibold text-lg
            shadow-xl hover:shadow-2xl
            transform hover:scale-105 active:scale-95
            transition-all duration-200
            flex items-center justify-center gap-3"
        >
          {/* Button glow effect */}
          <div className="absolute -inset-1 bg-gradient-to-r from-primary-500 to-purple-600 rounded-xl blur-lg opacity-50 group-hover:opacity-75 transition duration-200"></div>

          <div className="relative flex items-center gap-3">
            <Send size={24} strokeWidth={2.5} />
            <span>Chat on Telegram</span>
          </div>
        </button>

        {/* Try Again Button - Secondary */}
        <button
          onClick={handleRetry}
          className="flex-1 px-6 py-4 rounded-xl
            bg-white dark:bg-slate-800
            border-2 border-gray-200 dark:border-slate-700
            hover:border-primary-400 dark:hover:border-primary-500
            text-gray-700 dark:text-gray-200 font-semibold text-lg
            shadow-lg hover:shadow-xl
            transform hover:scale-105 active:scale-95
            transition-all duration-200
            flex items-center justify-center gap-3"
        >
          <RefreshCw size={24} strokeWidth={2.5} />
          <span>Try Again</span>
        </button>
      </div>

      {/* Additional Info */}
      <div className="mt-8 text-center">
        <p className="text-sm text-gray-500 dark:text-gray-400">
          Our Telegram bot is available 24/7 and offers the same AI-powered property search
        </p>
      </div>
    </div>
  );
};
