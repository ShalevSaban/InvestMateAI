import React, { useEffect, useState } from 'react';
import { MapPin, DollarSign, Bed, Building2, TrendingUp, Phone, User } from 'lucide-react';
import { Property } from '@/types';
import { Card } from './ui/Card';
import { api } from '@/utils/api';

interface PropertyCardProps {
  property: Property;
}

export const PropertyCard: React.FC<PropertyCardProps> = ({ property }) => {
  const [imageUrl, setImageUrl] = useState<string | null>(null);

  useEffect(() => {
    const fetchImage = async () => {
      try {
        const { image_url } = await api.getPropertyImageUrl(property.id);
        setImageUrl(image_url);
      } catch (error) {
        console.warn('Failed to fetch image for property', property.id);
      }
    };

    fetchImage();
  }, [property.id]);

  return (
    <Card padding="none" hover className="overflow-hidden">
      <div className="flex flex-col md:flex-row">
        {imageUrl && (
          <div className="md:w-1/3 h-48 md:h-auto">
            <img
              src={imageUrl}
              alt={`${property.city} property`}
              className="w-full h-full object-cover"
            />
          </div>
        )}
        <div className={`p-6 flex-1 ${!imageUrl ? 'w-full' : ''}`}>
          <div className="flex items-start justify-between mb-3">
            <div>
              <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-1">
                {property.city}
              </h3>
              <div className="flex items-center text-gray-600 dark:text-gray-400 text-sm">
                <MapPin size={16} className="mr-1" />
                {property.address}
              </div>
            </div>
            <div className="bg-primary-500 text-white px-3 py-1 rounded-full text-sm font-semibold">
              {property.property_type}
            </div>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-3 gap-4 mb-4">
            <div className="flex items-center space-x-2 text-gray-700 dark:text-gray-300">
              <DollarSign size={18} className="text-primary-500" />
              <div>
                <div className="text-xs text-gray-500 dark:text-gray-400">Price</div>
                <div className="font-semibold">{property.price.toLocaleString()}₪</div>
              </div>
            </div>

            <div className="flex items-center space-x-2 text-gray-700 dark:text-gray-300">
              <Bed size={18} className="text-primary-500" />
              <div>
                <div className="text-xs text-gray-500 dark:text-gray-400">Rooms</div>
                <div className="font-semibold">{property.rooms}</div>
              </div>
            </div>

            <div className="flex items-center space-x-2 text-gray-700 dark:text-gray-300">
              <Building2 size={18} className="text-primary-500" />
              <div>
                <div className="text-xs text-gray-500 dark:text-gray-400">Floor</div>
                <div className="font-semibold">{property.floor}</div>
              </div>
            </div>

            {property.yield_percent && (
              <div className="flex items-center space-x-2 text-gray-700 dark:text-gray-300">
                <TrendingUp size={18} className="text-green-500" />
                <div>
                  <div className="text-xs text-gray-500 dark:text-gray-400">Yield</div>
                  <div className="font-semibold">{property.yield_percent}%</div>
                </div>
              </div>
            )}

            {property.rental_estimate && (
              <div className="flex items-center space-x-2 text-gray-700 dark:text-gray-300">
                <DollarSign size={18} className="text-green-500" />
                <div>
                  <div className="text-xs text-gray-500 dark:text-gray-400">Est. Rent</div>
                  <div className="font-semibold">{property.rental_estimate.toLocaleString()}₪</div>
                </div>
              </div>
            )}
          </div>

          {property.description && (
            <p className="text-gray-600 dark:text-gray-400 text-sm mb-4 line-clamp-2">
              {property.description}
            </p>
          )}

          {property.agent && (
            <div className="border-t border-gray-200 dark:border-gray-700 pt-4 mt-4">
              <div className="flex items-center justify-between text-sm">
                <div className="flex items-center space-x-2 text-gray-700 dark:text-gray-300">
                  <User size={16} />
                  <span className="font-medium">{property.agent.full_name}</span>
                </div>
                <div className="flex items-center space-x-2 text-gray-600 dark:text-gray-400">
                  <Phone size={16} />
                  <span>{property.agent.phone_number}</span>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </Card>
  );
};
