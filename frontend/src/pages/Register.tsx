import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { UserPlus } from 'lucide-react';
import { Card } from '@/components/ui/Card';
import { Input } from '@/components/ui/Input';
import { Button } from '@/components/ui/Button';
import { api } from '@/utils/api';

export const Register: React.FC = () => {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    confirmPassword: '',
    full_name: '',
    phone_number: '',
    agency_name: '',
    license_number: '',
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    if (formData.password !== formData.confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    setLoading(true);

    try {
      const { confirmPassword, ...registerData } = formData;
      await api.register(registerData);
      navigate('/login', { state: { message: 'Registration successful! Please login.' } });
    } catch (err) {
      setError('Registration failed. Email might already be registered.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto">
      <div className="text-center mb-8">
        <div className="flex justify-center mb-4">
          <div className="w-16 h-16 bg-green-500 rounded-xl flex items-center justify-center">
            <UserPlus size={32} className="text-white" />
          </div>
        </div>
        <h1 className="text-3xl font-bold text-app-primary mb-2">
          Register as Agent
        </h1>
        <p className="text-app-secondary">
          Join our network of real estate professionals
        </p>
      </div>

      <Card padding="lg">
        <form onSubmit={handleSubmit} className="space-y-6">
          {error && (
            <div className="bg-red-100 dark:bg-red-900/30 border border-red-400 dark:border-red-800 text-red-700 dark:text-red-400 px-4 py-3 rounded-lg">
              {error}
            </div>
          )}

          <div className="grid md:grid-cols-2 gap-4">
            <Input
              type="text"
              name="full_name"
              label="Full Name"
              value={formData.full_name}
              onChange={handleChange}
              placeholder="John Doe"
              required
            />

            <Input
              type="email"
              name="email"
              label="Email"
              value={formData.email}
              onChange={handleChange}
              placeholder="agent@example.com"
              required
            />

            <Input
              type="tel"
              name="phone_number"
              label="Phone Number"
              value={formData.phone_number}
              onChange={handleChange}
              placeholder="+1234567890"
              required
            />

            <Input
              type="text"
              name="agency_name"
              label="Agency Name (Optional)"
              value={formData.agency_name}
              onChange={handleChange}
              placeholder="Real Estate Agency"
            />

            <Input
              type="text"
              name="license_number"
              label="License Number (Optional)"
              value={formData.license_number}
              onChange={handleChange}
              placeholder="RE-12345"
            />
          </div>

          <div className="grid md:grid-cols-2 gap-4">
            <Input
              type="password"
              name="password"
              label="Password"
              value={formData.password}
              onChange={handleChange}
              placeholder="••••••••"
              required
            />

            <Input
              type="password"
              name="confirmPassword"
              label="Confirm Password"
              value={formData.confirmPassword}
              onChange={handleChange}
              placeholder="••••••••"
              required
            />
          </div>

          <Button type="submit" fullWidth size="lg" disabled={loading}>
            {loading ? 'Registering...' : 'Register'}
          </Button>
        </form>

        <div className="mt-6 text-center">
          <p className="text-app-secondary">
            Already have an account?{' '}
            <Link
              to="/login"
              className="text-primary-500 hover:text-primary-600 font-semibold"
            >
              Login here
            </Link>
          </p>
        </div>

        <div className="mt-4 text-center">
          <Link
            to="/"
            className="text-sm text-gray-500 dark:text-slate-300 hover:text-gray-700 dark:hover:text-gray-300"
          >
            Back to home
          </Link>
        </div>
      </Card>
    </div>
  );
};
