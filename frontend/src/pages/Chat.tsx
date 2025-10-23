import React, { useState, useEffect } from 'react';
import { MessageCircle, Send } from 'lucide-react';
import { Card } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Textarea } from '@/components/ui/Textarea';
import { Select } from '@/components/ui/Select';
import { PropertyCard } from '@/components/PropertyCard';
import { api } from '@/utils/api';
import { Agent, Property } from '@/types';
import { useAuth } from '@/context/AuthContext';

interface Message {
  role: 'user' | 'assistant';
  content: string;
  properties?: Property[];
}

export const Chat: React.FC = () => {
  const [agents, setAgents] = useState<Agent[]>([]);
  const [selectedAgentId, setSelectedAgentId] = useState<string>('');
  const [question, setQuestion] = useState('');
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);
  const { token } = useAuth();

  useEffect(() => {
    const fetchAgents = async () => {
      try {
        const data = await api.getAgents();
        setAgents(data);
        if (data.length > 0) {
          setSelectedAgentId(data[0].id.toString());
        }
      } catch (error) {
        console.error('Failed to fetch agents', error);
      }
    };

    fetchAgents();
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!question.trim() || !selectedAgentId) return;

    const userMessage: Message = {
      role: 'user',
      content: question,
    };

    setMessages((prev) => [...prev, userMessage]);
    setLoading(true);
    setQuestion('');

    try {
      const response = await api.chat(question, parseInt(selectedAgentId), token || undefined);

      const assistantMessage: Message = {
        role: 'assistant',
        content: response.message,
        properties: response.results,
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      const errorMessage: Message = {
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-5xl mx-auto">
      <div className="text-center mb-8">
        <div className="flex justify-center mb-4">
          <div className="w-16 h-16 bg-primary-500 rounded-xl flex items-center justify-center">
            <MessageCircle size={32} className="text-white" />
          </div>
        </div>
        <h1 className="text-3xl font-bold text-light-text dark:text-dark-text mb-2">
          Ask The AI Agent
        </h1>
        <p className="text-light-textSecondary dark:text-dark-textSecondary">
          Search for properties and get instant answers
        </p>
      </div>

      <Card padding="lg" className="mb-6">
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

        <form onSubmit={handleSubmit} className="mt-4">
          <Textarea
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="e.g., Show me apartments in Netanya under 2M..."
            rows={3}
            disabled={loading}
          />
          <Button
            type="submit"
            className="mt-4 flex items-center space-x-2"
            disabled={loading || !selectedAgentId}
          >
            <Send size={18} />
            <span>{loading ? 'Sending...' : 'Send'}</span>
          </Button>
        </form>
      </Card>

      <div className="space-y-6">
        {messages.map((message, index) => (
          <div key={index}>
            <Card
              padding="md"
              className={
                message.role === 'user'
                  ? 'bg-primary-50 dark:bg-primary-900/20 ml-auto max-w-2xl'
                  : 'bg-gray-100 dark:bg-slate-700 max-w-2xl'
              }
            >
              <div className="flex items-start space-x-3">
                <div
                  className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 ${
                    message.role === 'user'
                      ? 'bg-primary-500 text-white'
                      : 'bg-gray-500 text-white'
                  }`}
                >
                  {message.role === 'user' ? 'U' : 'AI'}
                </div>
                <div className="flex-1">
                  <p className="text-light-text dark:text-dark-text whitespace-pre-wrap">
                    {message.content}
                  </p>
                </div>
              </div>
            </Card>

            {message.properties && message.properties.length > 0 && (
              <div className="mt-4 space-y-4">
                {message.properties.map((property) => (
                  <PropertyCard key={property.id} property={property} />
                ))}
              </div>
            )}
          </div>
        ))}

        {loading && (
          <Card padding="md" className="bg-gray-100 dark:bg-slate-700 max-w-2xl">
            <div className="flex items-center space-x-3">
              <div className="w-8 h-8 rounded-full bg-gray-500 flex items-center justify-center text-white">
                AI
              </div>
              <div className="flex space-x-2">
                <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce"></div>
                <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
              </div>
            </div>
          </Card>
        )}
      </div>
    </div>
  );
};
