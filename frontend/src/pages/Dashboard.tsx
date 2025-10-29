import React from 'react';
import { Link, Navigate } from 'react-router-dom';
import { LayoutDashboard, Home, Upload, TrendingUp, MessageSquare } from 'lucide-react';
import { Card } from '@/components/ui/Card';
import { useAuth } from '@/context/AuthContext';

export const Dashboard: React.FC = () => {
  const { isAuthenticated } = useAuth();

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  const dashboardCards = [
    {
      title: 'Chat Insights',
      description: 'View client interactions and chat analytics',
      icon: TrendingUp,
      link: '/insights',
      color: 'bg-blue-500',
    },
    {
      title: 'Add New Property',
      description: 'List a new property in your portfolio',
      icon: Home,
      link: '/add-property',
      color: 'bg-green-500',
    },
    {
      title: 'Upload Property Image',
      description: 'Add or update property photos',
      icon: Upload,
      link: '/upload-image',
      color: 'bg-purple-500',
    },
    {
      title: 'Client Chat',
      description: 'See how clients interact with your properties',
      icon: MessageSquare,
      link: '/chat',
      color: 'bg-orange-500',
    },
  ];

  return (
    <div className="max-w-6xl mx-auto">
      <div className="mb-8">
        <div className="flex items-center space-x-3 mb-4">
          <div className="w-12 h-12 bg-primary-500 rounded-xl flex items-center justify-center">
            <LayoutDashboard size={28} className="text-white" />
          </div>
          <div>
            <h1 className="text-3xl font-bold text-app-primary">
              Agent Dashboard
            </h1>
            <p className="text-app-secondary">
              Welcome back! Manage your properties and view insights
            </p>
          </div>
        </div>
      </div>

      <div className="grid md:grid-cols-2 gap-6">
        {dashboardCards.map((card) => {
          const Icon = card.icon;
          return (
            <Link key={card.link} to={card.link}>
              <Card padding="lg" hover className="h-full">
                <div className="flex items-start space-x-4">
                  <div className={`${card.color} w-14 h-14 rounded-xl flex items-center justify-center flex-shrink-0`}>
                    <Icon size={28} className="text-white" />
                  </div>
                  <div className="flex-1">
                    <h3 className="text-xl font-bold text-app-primary mb-2">
                      {card.title}
                    </h3>
                    <p className="text-app-secondary">
                      {card.description}
                    </p>
                  </div>
                </div>
              </Card>
            </Link>
          );
        })}
      </div>

      <Card padding="lg" className="mt-8 bg-gradient-to-r from-primary-500 to-primary-600">
        <div className="text-white">
          <h3 className="text-2xl font-bold mb-2">Need Help?</h3>
          <p className="text-primary-100 mb-4">
            Check out our documentation or contact support at:+972 527991409 for assistance with managing your properties
            and maximizing your reach.
          </p>
          <div className="flex flex-wrap gap-3">
           <Link
            to="/"
            className="px-4 py-2 border border-primary-500 text-primary-500 rounded-lg font-semibold bg-transparent hover:bg-primary-50 transition-colors"
            >
            Back to Home
            </Link>

          </div>
        </div>
      </Card>
    </div>
  );
};
