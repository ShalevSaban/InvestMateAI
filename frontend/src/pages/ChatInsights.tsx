import React, { useState, useEffect } from 'react';
import { Navigate } from 'react-router-dom';
import { TrendingUp, MessageSquare, Clock } from 'lucide-react';
import { Card } from '@/components/ui/Card';
import { useAuth } from '@/context/AuthContext';
import { api } from '@/utils/api';

interface Insight {
  id: number;
  question: string;
  response: string;
  timestamp: string;
  properties_count?: number;
}

export const ChatInsights: React.FC = () => {
  const { isAuthenticated, token } = useAuth();
  const [insights, setInsights] = useState<Insight[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  useEffect(() => {
    const fetchInsights = async () => {
      try {
        const data = await api.getChatInsights(token!);
        setInsights(data);
      } catch (err) {
        setError('Failed to load chat insights');
      } finally {
        setLoading(false);
      }
    };

    fetchInsights();
  }, [token]);

  return (
    <div className="max-w-5xl mx-auto">
      <div className="text-center mb-8">
        <div className="flex justify-center mb-4">
          <div className="w-16 h-16 bg-blue-500 rounded-xl flex items-center justify-center">
            <TrendingUp size={32} className="text-white" />
          </div>
        </div>
        <h1 className="text-3xl font-bold text-app-primary mb-2">
          Chat Insights
        </h1>
        <p className="text-app-secondary">
          View client interactions and analytics
        </p>
      </div>

      {loading ? (
        <Card padding="lg">
          <div className="text-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-500 mx-auto"></div>
            <p className="mt-4 text-app-secondary">Loading insights...</p>
          </div>
        </Card>
      ) : error ? (
        <Card padding="lg">
          <div className="text-center py-12 text-red-600 dark:text-red-400">
            {error}
          </div>
        </Card>
      ) : insights.length === 0 ? (
        <Card padding="lg">
          <div className="text-center py-12">
            <MessageSquare size={48} className="mx-auto text-gray-400 mb-4" />
            <h3 className="text-xl font-semibold text-app-primary mb-2">
              No insights yet
            </h3>
            <p className="text-app-secondary">
              Chat interactions with clients will appear here
            </p>
          </div>
        </Card>
      ) : (
        <div className="space-y-4">
          <Card padding="md" className="bg-gradient-to-r from-blue-500 to-blue-600 text-white">
            <div className="flex justify-around text-center">
              <div>
                <div className="text-3xl font-bold">{insights.length}</div>
                <div className="text-blue-100 text-sm">Total Chats</div>
              </div>
              <div>
                <div className="text-3xl font-bold">
                  {insights.reduce((sum, i) => sum + (i.properties_count || 0), 0)}
                </div>
                <div className="text-blue-100 text-sm">Properties Shown</div>
              </div>
            </div>
          </Card>

          {insights.map((insight) => (
            <Card key={insight.id} padding="lg" hover>
              <div className="space-y-3">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center space-x-2 mb-2">
                      <MessageSquare size={18} className="text-primary-500" />
                      <span className="font-semibold text-app-primary">
                        Client Question
                      </span>
                    </div>
                    <p className="text-gray-700 dark:text-slate-200 ml-6">
                      {insight.question}
                    </p>
                  </div>
                  {insight.properties_count !== undefined && (
                    <div className="bg-primary-100 dark:bg-primary-900/30 text-primary-700 dark:text-primary-300 px-3 py-1 rounded-full text-sm font-semibold ml-4">
                      {insight.properties_count} properties
                    </div>
                  )}
                </div>

                <div className="border-l-4 border-gray-200 dark:border-gray-700 pl-6 ml-2">
                  <div className="flex items-center space-x-2 mb-2">
                    <TrendingUp size={18} className="text-green-500" />
                    <span className="font-semibold text-app-primary">
                      AI Response
                    </span>
                  </div>
                  <p className="text-app-secondary">
                    {insight.response}
                  </p>
                </div>

                {insight.timestamp && (
                  <div className="flex items-center space-x-2 text-sm text-gray-500 dark:text-slate-300 mt-3">
                    <Clock size={16} />
                    <span>{new Date(insight.timestamp).toLocaleString()}</span>
                  </div>
                )}
              </div>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
};
