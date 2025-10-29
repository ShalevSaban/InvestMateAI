import React, { useState } from 'react';
import { useNavigate, Navigate } from 'react-router-dom';
import { Home, CheckCircle } from 'lucide-react';
import { Card } from '@/components/ui/Card';
import { Input } from '@/components/ui/Input';
import { Textarea } from '@/components/ui/Textarea';
import { Button } from '@/components/ui/Button';
import { Select } from '@/components/ui/Select'; // 👈 נוסיף את הרכיב Select
import { useAuth } from '@/context/AuthContext';
import { api } from '@/utils/api';

export const AddProperty: React.FC = () => {
  const { isAuthenticated, token } = useAuth();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);
  const [formData, setFormData] = useState({
    address: '',
    city: '',
    price: '',
    rooms: '',
    floor: '',
    property_type: '',
    description: '',
    yield_percent: '',
    rental_estimate: '',
  });

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  const handleChange = (
    e: React.ChangeEvent<
      HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement
    >
  ) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const propertyData = {
        address: formData.address,
        city: formData.city,
        price: parseFloat(formData.price),
        rooms: parseInt(formData.rooms),
        floor: parseInt(formData.floor),
        property_type: formData.property_type,
        description: formData.description || undefined,
        yield_percent: formData.yield_percent
          ? parseFloat(formData.yield_percent)
          : undefined,
        rental_estimate: formData.rental_estimate
          ? parseFloat(formData.rental_estimate)
          : undefined,
      };

      await api.createProperty(propertyData, token!);
      setSuccess(true);
      setTimeout(() => navigate('/dashboard'), 2000);
    } catch (err) {
      setError('Failed to add property. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto">
      <div className="text-center mb-8">
        <div className="flex justify-center mb-4">
          <div className="w-16 h-16 bg-green-500 rounded-xl flex items-center justify-center">
            <Home size={32} className="text-white" />
          </div>
        </div>
        <h1 className="text-3xl font-bold text-app-primary mb-2">
          Add New Property
        </h1>
        <p className="text-app-secondary">
          List a new property in your portfolio
        </p>
      </div>



      <Card padding="lg">
        <form onSubmit={handleSubmit} className="space-y-6">
          {error && (
            <div className="bg-red-100 dark:bg-red-900/30 border border-red-400 dark:border-red-800 text-red-700 dark:text-red-400 px-4 py-3 rounded-lg">
              {error}
            </div>
          )}

          {success && (
            <div className="flex items-center gap-2 bg-green-100 dark:bg-green-900/30 border border-green-400 dark:border-green-700 text-green-800 dark:text-green-300 px-4 py-3 rounded-lg animate-fade-in">
              <CheckCircle size={20} />
              <span>Property added successfully!</span>
            </div>
          )}

          <div className="grid md:grid-cols-2 gap-4">
            <Input
              type="text"
              name="address"
              label="Address"
              value={formData.address}
              onChange={handleChange}
              placeholder="123 Main St"
              required
            />

            <Input
              type="text"
              name="city"
              label="City"
              value={formData.city}
              onChange={handleChange}
              placeholder="Tel Aviv"
              required
            />

            <Input
              type="number"
              name="price"
              label="Price (₪)"
              value={formData.price}
              onChange={handleChange}
              placeholder="1500000"
              required
            />

            <Input
              type="number"
              name="rooms"
              label="Number of Rooms"
              value={formData.rooms}
              onChange={handleChange}
              placeholder="3"
              required
            />

            <Input
              type="number"
              name="floor"
              label="Floor"
              value={formData.floor}
              onChange={handleChange}
              placeholder="2"
              required
            />

            {/* 👇 שינוי כאן: במקום Input השתמשנו ב-Select */}
            <Select
              label="Property Type"
              value={formData.property_type}
              onChange={(e) =>
                handleChange({
                  target: {
                    name: 'property_type',
                    value: e.target.value,
                  },
                } as any)
              }
              options={[
                { value: '', label: 'Select property type...' },
                { value: 'apartment', label: 'Apartment' },
                { value: 'house', label: 'House' },
                { value: 'penthouse', label: 'Penthouse' },
              ]}
              required
            />

            <Input
              type="number"
              name="yield_percent"
              label="Yield Percentage (Optional)"
              value={formData.yield_percent}
              onChange={handleChange}
              placeholder="5.5"
              step="0.1"
            />

            <Input
              type="number"
              name="rental_estimate"
              label="Rental Estimate (₪) (Optional)"
              value={formData.rental_estimate}
              onChange={handleChange}
              placeholder="5000"
            />
          </div>

          <Textarea
            name="description"
            label="Description (Optional)"
            value={formData.description}
            onChange={handleChange}
            placeholder="Beautiful apartment with sea view..."
            rows={4}
          />

          <div className="flex gap-4">
            <Button type="submit" fullWidth size="lg" disabled={loading}>
              {loading ? 'Adding Property...' : 'Add Property'}
            </Button>
            <Button
              type="button"
              variant="outline"
              size="lg"
              onClick={() => navigate('/dashboard')}
            >
              Cancel
            </Button>
          </div>
        </form>
      </Card>
    </div>
  );
};
