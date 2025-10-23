import React, { useState } from 'react';
import { useNavigate, Navigate } from 'react-router-dom';
import { Home } from 'lucide-react';
import { Card } from '@/components/ui/Card';
import { Input } from '@/components/ui/Input';
import { Textarea } from '@/components/ui/Textarea';
import { Button } from '@/components/ui/Button';
import { useAuth } from '@/context/AuthContext';
import { api } from '@/utils/api';

export const AddProperty: React.FC = () => {
  const { isAuthenticated, token } = useAuth();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
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
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
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
        yield_percent: formData.yield_percent ? parseFloat(formData.yield_percent) : undefined,
        rental_estimate: formData.rental_estimate ? parseFloat(formData.rental_estimate) : undefined,
      };

      await api.createProperty(propertyData, token!);
      navigate('/dashboard', { state: { message: 'Property added successfully!' } });
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
        <h1 className="text-3xl font-bold text-light-text dark:text-dark-text mb-2">
          Add New Property
        </h1>
        <p className="text-light-textSecondary dark:text-dark-textSecondary">
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

            <Input
              type="text"
              name="property_type"
              label="Property Type"
              value={formData.property_type}
              onChange={handleChange}
              placeholder="Apartment"
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
