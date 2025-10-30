import React, { useEffect, useState } from 'react';

export const Loader: React.FC = () => {
  const messages = [
    "🤖 Recruiting AI agents... some of them are still on coffee break.",
    "💸 Shalev is trying to save hosting costs-  the server takes a nap when nobody’s watching.",
    "💬 In the meantime, Shalev will tell you a bit about himself...",
    "👋 Hey! I’m Shalev, a Computer Science graduate who built this system.",
    "🏗️ InvestMateAI runs on FastAPI, PostgreSQL, React, and GPT magic.",
    "🧠 Teaching the model to remember its manners...",
    "☕ Waking up the backend... it’s still stretching.",
    "🚀 Almost there! Warming up the smart property engine.",
  ];


  const [index, setIndex] = useState(0);
  const [fade, setFade] = useState(true);

  useEffect(() => {
    const interval = setInterval(() => {
      setFade(false);
      setTimeout(() => {
        setIndex((prev) => (prev + 1) % messages.length);
        setFade(true);
      }, 500);
    }, 4000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="fixed inset-0 flex flex-col items-center justify-center bg-white/95 dark:bg-gray-900/95 backdrop-blur-sm z-50 transition-all duration-700">
      {/* Spinner */}
      <div className="relative flex items-center justify-center">
        <div className="absolute animate-ping h-16 w-16 rounded-full bg-primary-400 opacity-75"></div>
        <div className="animate-spin rounded-full h-12 w-12 border-t-4 border-b-4 border-primary-500"></div>
      </div>

      {/* Text */}
      <p
        className={`mt-6 text-primary-700 dark:text-primary-200 font-semibold text-lg text-center max-w-sm transition-opacity duration-700 ${
          fade ? 'opacity-100' : 'opacity-0'
        }`}
      >
        {messages[index]}
      </p>
    </div>
  );
};
