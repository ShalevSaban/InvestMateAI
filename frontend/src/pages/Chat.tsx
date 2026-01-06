import React, { useState, useEffect } from 'react';
import { MessageCircle, Search, Sparkles, User } from 'lucide-react';
import { Card } from '@/components/ui/Card';
import { Select } from '@/components/ui/Select';
import { PropertyCard } from '@/components/PropertyCard';
import { api } from '@/utils/api';
import { Agent, Property } from '@/types';
import { useAuth } from '@/context/AuthContext';
import houseIcon from '@/assets/house.png';
import {Loader} from '@/components/ui/Loader'
import {TelegramFallback} from '@/components/ui/TelegramFallback'


interface Message {
  role: 'user' | 'assistant';
  content: string;
  properties?: Property[];
}

const SUGGESTION_QUESTIONS = [
  "Apartment in central Tel Aviv, up to 3 rooms, yield above 2%",
  "Private house with a pool in Herzliya",
  "Penthouse in Haifa under 4 million",
  "Apartment in Ramat Gan near the metro",
  "Apartment in Petah Tikva with an elevator",
  "Show all properties"
];

export const Chat: React.FC = () => {
  const [agents, setAgents] = useState<Agent[]>([]);
  const [selectedAgentId, setSelectedAgentId] = useState<string>('');
  const [question, setQuestion] = useState('');
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);
  const [loadingAgents, setLoadingAgents] = useState(true);
  const [timedOut, setTimedOut] = useState(false);
  const { token } = useAuth();

  const fetchAgents = async () => {
    setLoadingAgents(true);
    setTimedOut(false);

    let timeoutId: NodeJS.Timeout;
    let fetchCompleted = false;

    // Set timeout for 8 seconds
    timeoutId = setTimeout(() => {
      if (!fetchCompleted) {
        setTimedOut(true);
        setLoadingAgents(false);
      }
    }, 8000);

    try {
      const data = await api.getAgents();
      fetchCompleted = true;
      clearTimeout(timeoutId);
      setAgents(data);
      if (data.length > 0) setSelectedAgentId(data[0].id.toString());
      setLoadingAgents(false);
    } catch (error) {
      console.error('Failed to fetch agents', error);
      fetchCompleted = true;
      clearTimeout(timeoutId);
       setTimedOut(true);
      setLoadingAgents(false);
    }
  };

  useEffect(() => {
    fetchAgents();
  }, []);

  if (loadingAgents) {
    return <Loader/>;
  }

  if (timedOut) {
    return <TelegramFallback onRetry={fetchAgents} />; // העבר את הפונקציה
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!question.trim() || !selectedAgentId) return;

    const userMessage: Message = { role: 'user', content: question };
    console.log('Clearing messages, setting to:', [userMessage]);
    setMessages([userMessage]);
    setLoading(true);
    setQuestion('');

    try {
      const response = await api.chat(question, selectedAgentId, token || undefined);
      const assistantMessage: Message = {
        role: 'assistant',
        content: response.message,
        properties: response.results,
      };
      setMessages([userMessage, assistantMessage]);
    } catch (error) {
      const errorMessage: Message = {
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
      };
      setMessages([userMessage, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-5xl mx-auto">
      {/* Hero Section */}
      <div className="text-center mb-10">
        <div className="flex justify-center mb-6">
          <div className="relative">
            {/* Glow effect */}
            <div className="absolute inset-0 bg-gradient-to-r from-primary-400 to-purple-500 rounded-2xl blur-2xl opacity-30 animate-pulse"></div>
            <div className="relative w-20 h-20 bg-gradient-to-br from-primary-500 to-primary-600 rounded-2xl flex items-center justify-center shadow-2xl transform hover:scale-110 transition-transform duration-300">
              <MessageCircle size={40} className="text-white" />
            </div>
          </div>
        </div>
        <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-3">
          Ask The AI Agent
        </h1>
        <p className="text-lg text-app-secondary flex items-center justify-center gap-2">
          <Sparkles size={18} className="text-primary-500" />
          Search for properties and get instant answers
        </p>
      </div>

      {/* Main Search Card */}
      <Card padding="lg" className="mb-8 shadow-xl border-2 border-gray-100 dark:border-slate-700">
        <Select
          label="Filter by Agent"
          value={selectedAgentId}
          onChange={(e) => setSelectedAgentId(e.target.value)}
          options={[
            { value: '', label: 'Select an agent...' },
            ...agents.map((agent) => ({
              value: agent.id.toString(),
              label: agent.full_name,
            })),
          ]}
        />

        <form onSubmit={handleSubmit} className="mt-6">
          {/* Premium Search Bar */}
          <div className="relative mb-6">
            {/* Gradient glow background */}
            <div className="absolute -inset-1 bg-gradient-to-r from-primary-500/20 via-purple-500/20 to-primary-500/20 rounded-3xl blur-lg opacity-75 group-hover:opacity-100 transition duration-300"></div>

            <div className="relative">
              {/* Search Icon */}
              <div className="absolute left-6 top-1/2 -translate-y-1/2 text-gray-400 dark:text-gray-500 z-10">
                <Search size={24} strokeWidth={2.5} />
              </div>

              {/* Input Field */}
              <input
                type="text"
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                placeholder="Which property are you looking for? (e.g., 3-room apartment in Tel Aviv)"
                onKeyDown={(e) => {
                  if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    handleSubmit(e);
                  }
                }}
                className="w-full pl-16 pr-32 py-4 rounded-2xl
                  bg-white dark:bg-slate-800
                  border-2 border-gray-200 dark:border-slate-700
                  focus:border-primary-500 dark:focus:border-primary-400
                  focus:outline-none focus:ring-4 focus:ring-primary-500/20
                  text-app-primary placeholder-gray-400 dark:placeholder-gray-500
                  text-lg font-medium
                  shadow-xl hover:shadow-2xl
                  transition-all duration-300
                  disabled:opacity-50 disabled:cursor-not-allowed"
                disabled={loading}
              />

              {/* Premium Search Button */}
              <button
                type="submit"
                disabled={loading || !selectedAgentId || !question.trim()}
                className="absolute right-3 top-1/2
                  px-6 py-3 rounded-xl
                  bg-gradient-to-r from-primary-500 via-primary-600 to-purple-600
                  hover:from-primary-600 hover:via-primary-700 hover:to-purple-700
                  text-white font-semibold text-base
                  shadow-lg hover:shadow-xl
                  -translate-y-1/2 hover:-translate-y-1/2 hover:scale-105 active:-translate-y-1/2 active:scale-95
                  transition-all duration-200
                  disabled:opacity-50 disabled:cursor-not-allowed
                  flex items-center gap-2"
              >
                <Search size={20} strokeWidth={2.5} />
                <span className="hidden sm:inline">Search</span>
              </button>
            </div>
          </div>

          {/* Enhanced Suggestion Pills */}
          <div className="space-y-3">
            <p className="text-sm font-medium text-gray-600 dark:text-gray-400 flex items-center gap-2">
              <Sparkles size={16} />
              Quick searches:
            </p>
            <div className="flex flex-wrap gap-2">
              {SUGGESTION_QUESTIONS.map((suggestion, index) => (
                <button
                  key={index}
                  type="button"
                  onClick={async () => {
                    if (!selectedAgentId || loading) return;

                    const userMessage: Message = { role: 'user', content: suggestion };
                    setMessages([userMessage]);
                    setLoading(true);
                    setQuestion('');

                    try {
                      const response = await api.chat(suggestion, selectedAgentId, token || undefined);
                      const assistantMessage: Message = {
                        role: 'assistant',
                        content: response.message,
                        properties: response.results,
                      };
                      setMessages([userMessage, assistantMessage]);
                    } catch (error) {
                      const errorMessage: Message = {
                        role: 'assistant',
                        content: 'Sorry, I encountered an error. Please try again.',
                      };
                      setMessages([userMessage, errorMessage]);
                    } finally {
                      setLoading(false);
                    }
                  }}
                  className="group px-5 py-2.5 rounded-full text-sm font-medium
                    bg-gradient-to-r from-primary-50 to-purple-50
                    dark:from-primary-900/20 dark:to-purple-900/20
                    text-primary-700 dark:text-primary-300
                    hover:from-primary-100 hover:to-purple-100
                    dark:hover:from-primary-900/40 dark:hover:to-purple-900/40
                    border-2 border-primary-200 dark:border-primary-700
                    hover:border-primary-400 dark:hover:border-primary-500
                    shadow-sm hover:shadow-md
                    transform hover:scale-105 active:scale-95
                    transition-all duration-200
                    disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
                  disabled={loading || !selectedAgentId}
                >
                  {suggestion}
                </button>
              ))}
            </div>
          </div>
        </form>
      </Card>

      {/* Messages Section */}
      <div className="space-y-6" key={messages.length}>
        {messages.map((message, index) => (
          <div key={index}>
            <Card
              padding="md"
              className={
                message.role === 'user'
                  ? 'bg-gradient-to-br from-primary-50 to-purple-50 dark:from-primary-900/20 dark:to-purple-900/20 ml-auto max-w-2xl border-2 border-primary-200 dark:border-primary-800 shadow-lg'
                  : 'bg-white dark:bg-slate-800 max-w-2xl border-2 border-gray-200 dark:border-slate-700 shadow-lg'
              }
            >
              <div className="flex items-start space-x-3">
                <div
                  className={`w-10 h-10 rounded-xl flex items-center justify-center flex-shrink-0 overflow-hidden shadow-md ${
                    message.role === 'user'
                      ? 'bg-gradient-to-br from-primary-500 to-purple-600 text-white'
                      : 'bg-gradient-to-br from-gray-100 to-gray-200 dark:from-slate-700 dark:to-slate-800'
                  }`}
                >
                  {message.role === 'user' ? (
                    <User size={20} strokeWidth={2.5} />
                  ) : (
                    <img
                      src={houseIcon}
                      alt="AI Icon"
                      className="w-7 h-7 object-contain"
                    />
                  )}
                </div>
                <div className="flex-1">
                  <p className="whitespace-pre-wrap text-gray-900 dark:text-gray-100 leading-relaxed">
                    {message.content}
                  </p>
                </div>
              </div>
            </Card>

            {/* Search Results Summary */}
            {message.role === 'assistant' && message.properties !== undefined && (
              <div className="mt-4 mb-2">
                <div className="flex items-center gap-2 px-4 py-2 bg-primary-50 dark:bg-primary-900/20 border-l-4 border-primary-500 rounded-r-lg">
                  <Search size={18} className="text-primary-600 dark:text-primary-400" />
                  <span className="text-sm font-medium text-primary-700 dark:text-primary-300">
                    {message.properties.length === 0
                      ? 'No properties found matching your search'
                      : `Found ${message.properties.length} ${message.properties.length === 1 ? 'property' : 'properties'}`
                    }
                  </span>
                </div>
              </div>
            )}

            {message.properties && message.properties.length > 0 && (
              <div className="mt-2 space-y-4">
                {message.properties.map((property) => (
                  <PropertyCard key={property.id} property={property} />
                ))}
              </div>
            )}
          </div>
        ))}

        {/* Enhanced Loading State */}
        {loading && (
          <>
            {/* Searching Indicator */}
            <div className="mb-4">
              <div className="flex items-center gap-2 px-4 py-3 bg-gradient-to-r from-primary-50 to-purple-50 dark:from-primary-900/20 dark:to-purple-900/20 border-l-4 border-primary-500 rounded-r-lg shadow-md">
                <div className="relative">
                  <Search size={20} className="text-primary-600 dark:text-primary-400 animate-pulse" />
                  <div className="absolute inset-0 bg-primary-500 rounded-full blur-md opacity-50 animate-ping"></div>
                </div>
                <span className="text-sm font-semibold text-primary-700 dark:text-primary-300 animate-pulse">
                  Searching for properties...
                </span>
              </div>
            </div>

            {/* AI Response Loading */}
            <Card
              padding="md"
              className="bg-white dark:bg-slate-800 max-w-2xl border-2 border-gray-200 dark:border-slate-700 shadow-lg"
            >
              <div className="flex items-center space-x-3">
                <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-gray-100 to-gray-200 dark:from-slate-700 dark:to-slate-800 flex items-center justify-center overflow-hidden shadow-md">
                  <img
                    src={houseIcon}
                    alt="AI Icon"
                    className="w-7 h-7 object-contain"
                  />
                </div>
                <div className="flex space-x-2">
                  <div className="w-3 h-3 bg-gradient-to-r from-primary-500 to-purple-500 rounded-full animate-bounce shadow-lg"></div>
                  <div
                    className="w-3 h-3 bg-gradient-to-r from-primary-500 to-purple-500 rounded-full animate-bounce shadow-lg"
                    style={{ animationDelay: '0.15s' }}
                  ></div>
                  <div
                    className="w-3 h-3 bg-gradient-to-r from-primary-500 to-purple-500 rounded-full animate-bounce shadow-lg"
                    style={{ animationDelay: '0.3s' }}
                  ></div>
                </div>
              </div>
            </Card>
          </>
        )}
      </div>
    </div>
  );
};