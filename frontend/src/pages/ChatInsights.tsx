import React, { useState, useEffect } from 'react';
import { Navigate } from 'react-router-dom';
import { TrendingUp, MessageSquare } from 'lucide-react';
import { Card } from '@/components/ui/Card';
import { useAuth } from '@/context/AuthContext';
import { api } from '@/utils/api';

interface Question {
  question: string;
  count: number;
}

interface PeakHour {
  hour: number;
  count: number;
}

interface GptRecommendation {
  summary: string;
  suggestions?: string[];
}

interface DashboardInsights {
  top_questions: Question[];
  peak_hours: PeakHour[];
  gpt_recommendations: GptRecommendation;
  stats?: Record<string, any>;
}

export const ChatInsights: React.FC = () => {
  const { isAuthenticated, token } = useAuth();
  const [insights, setInsights] = useState<DashboardInsights | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  useEffect(() => {
  const fetchInsights = async () => {
    try {
      const response = await api.getChatInsights(token!);
      console.log('Raw response:', response);
      setInsights(response);
    } catch (err: any) {
      console.error('FetchInsights Error:', err);
      if (err.response) {
        console.error('Response text:', await err.response.text?.());
      }
      setError('Failed to load chat insights');
    } finally {
      setLoading(false);
    }
  };

  fetchInsights();
}, [token]);


  if (loading) {
    return (
      <Card padding="lg">
        <div className="text-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-500 mx-auto"></div>
          <p className="mt-4 text-app-secondary">Loading insights...</p>
        </div>
      </Card>
    );
  }

  if (error) {
    return (
      <Card padding="lg">
        <div className="text-center py-12 text-red-600 dark:text-red-400">
          {error}
        </div>
      </Card>
    );
  }

  if (!insights) {
    return (
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
    );
  }

  const { top_questions, peak_hours, gpt_recommendations } = insights;

  return (
    <div className="max-w-5xl mx-auto space-y-6">
      {/* Header */}
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
          GPT-powered analytics and user behavior overview
        </p>
      </div>

      {/* GPT Recommendations */}
      <Card padding="lg" className="bg-gradient-to-r from-blue-500 to-blue-600 text-white">
        <h2 className="text-xl font-semibold mb-2">🧠 GPT Recommendations</h2>
        <p>{gpt_recommendations?.summary || 'No recommendations yet.'}</p>
        {gpt_recommendations?.suggestions && (
          <ul className="list-disc list-inside mt-2">
            {gpt_recommendations.suggestions.map((s, i) => (
              <li key={i}>{s}</li>
            ))}
          </ul>
        )}
      </Card>

      {/* Most Asked Questions */}
      <Card padding="lg">
        <h2 className="text-xl font-semibold text-app-primary mb-3">❓ Most Asked Questions</h2>
        {top_questions?.length ? (
          <ul className="space-y-2">
            {top_questions.map((q, i) => (
              <li key={i} className="flex justify-between border-b pb-2">
                <span className="text-gray-700 dark:text-gray-200">{q.question}</span>
                <span className="font-semibold text-app-primary">{q.count}</span>
              </li>
            ))}
          </ul>
        ) : (
          <p className="text-app-secondary">No questions data available.</p>
        )}
      </Card>

      {/* Peak Chat Hours */}
      <Card padding="lg">
        <h2 className="text-xl font-semibold text-app-primary mb-3">⏰ Peak Chat Hours</h2>
        {peak_hours?.length ? (
          <ul className="space-y-2">
            {peak_hours.map((h, i) => (
              <li key={i} className="flex justify-between border-b pb-2">
                <span className="text-gray-700 dark:text-gray-200">
                  {String(h.hour).padStart(2, '0')}:00
                </span>
                <span className="font-semibold text-app-primary">{h.count} messages</span>
              </li>
            ))}
          </ul>
        ) : (
          <p className="text-app-secondary">No peak hour data available.</p>
        )}
      </Card>
    </div>
  );
};
