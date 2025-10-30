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
import houseIcon from '@/assets/house.png';
import {Loader} from '@/components/ui/Loader'


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
  const [loadingAgents, setLoadingAgents] = useState(true);
  const { token } = useAuth();

  useEffect(() => {
    const fetchAgents = async () => {
      try {
        const data = await api.getAgents();
        setAgents(data);
        if (data.length > 0) setSelectedAgentId(data[0].id.toString());
      } catch (error) {
        console.error('Failed to fetch agents', error);
      } finally{
        setLoadingAgents(false);
      }
    };
    fetchAgents();
  }, []);


  if (loadingAgents) {
    return <Loader/>;
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!question.trim() || !selectedAgentId) return;

    const userMessage: Message = { role: 'user', content: question };
    setMessages((prev) => [...prev, userMessage]);
    setLoading(true);
    setQuestion('');

    try {
      const response = await api.chat(question, selectedAgentId, token || undefined);
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
        <h1 className="text-3xl font-bold text-app-primary mb-2">
          Ask The AI Agent
        </h1>
        <p className="text-app-secondary">
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
            placeholder={
              "Example questions:\n" +
              "- Apartment in central Tel Aviv, up to 3 rooms, yield above 2%\n" +
              "- Private house with a pool in Herzliya\n" +
              "- Penthouse in Haifa under 4 million\n" +
                "- Apartment in Ramat Gan near the metro\n"+
                "- To see all available properties, type: 'Properties'"
            }
            rows={5}
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
                  : 'bg-gray-200 dark:bg-slate-700 max-w-2xl'
              }
            >
              <div className="flex items-start space-x-3">
                <div
                  className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 overflow-hidden shadow-sm ${
                    message.role === 'user'
                      ? 'bg-primary-500 text-black dark:text-white'
                      : 'bg-white dark:bg-black'
                  }`}
                >
                  {message.role === 'user' ? (
                    <span className="font-semibold">U</span>
                  ) : (
                    <img
                      src={houseIcon}
                      alt="AI Icon"
                      className="w-6 h-6 object-contain"
                    />
                  )}
                </div>
                <div className="flex-1">
                  <p className="whitespace-pre-wrap text-black dark:text-white">
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
          <Card
            padding="md"
            className="bg-gray-200 dark:bg-slate-700 max-w-2xl"
          >
            <div className="flex items-center space-x-3">
              <div className="w-8 h-8 rounded-full bg-white dark:bg-black flex items-center justify-center overflow-hidden shadow-sm">
                <img
                  src={houseIcon}
                  alt="AI Icon"
                  className="w-6 h-6 object-contain"
                />
              </div>
              <div className="flex space-x-2">
                <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce"></div>
                <div
                  className="w-2 h-2 bg-gray-500 rounded-full animate-bounce"
                  style={{ animationDelay: '0.1s' }}
                ></div>
                <div
                  className="w-2 h-2 bg-gray-500 rounded-full animate-bounce"
                  style={{ animationDelay: '0.2s' }}
                ></div>
              </div>
            </div>
          </Card>
        )}
      </div>
    </div>
  );
};
