import React, { useState, useEffect } from 'react';
import { useNavigate, Navigate } from 'react-router-dom';
import { Upload, Image } from 'lucide-react';
import { Card } from '@/components/ui/Card';
import { Select } from '@/components/ui/Select';
import { Button } from '@/components/ui/Button';
import { useAuth } from '@/context/AuthContext';
import { api } from '@/utils/api';
import { Property } from '@/types';

export const UploadImage: React.FC = () => {
  const { isAuthenticated, token } = useAuth();
  const navigate = useNavigate();
  const [properties, setProperties] = useState<Property[]>([]);
  const [selectedPropertyId, setSelectedPropertyId] = useState<string>('');
  const [file, setFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<string>('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  useEffect(() => {
    const fetchProperties = async () => {
      try {
        const data = await api.getProperties(token!);
        setProperties(data);
      } catch (error) {
        console.error('Failed to fetch properties', error);
      }
    };

    fetchProperties();
  }, [token]);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0];
    if (selectedFile) {
      setFile(selectedFile);
      const reader = new FileReader();
      reader.onloadend = () => {
        setPreview(reader.result as string);
      };
      reader.readAsDataURL(selectedFile);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file || !selectedPropertyId) {
      setError('Please select a property and choose an image');
      return;
    }

    setError('');
    setSuccess('');
    setLoading(true);

    try {
      await api.uploadPropertyImage(selectedPropertyId, file, token!);
      setSuccess('Image uploaded successfully!');
      setFile(null);
      setPreview('');
      setSelectedPropertyId('');
    } catch (err) {
      setError('Failed to upload image. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto">
      <div className="text-center mb-8">
        <div className="flex justify-center mb-4">
          <div className="w-16 h-16 bg-purple-500 rounded-xl flex items-center justify-center">
            <Upload size={32} className="text-white" />
          </div>
        </div>
        <h1 className="text-3xl font-bold text-app-primary mb-2">
          Upload Property Image
        </h1>
        <p className="text-app-secondary">
          Add or update photos for your properties
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
            <div className="bg-green-100 dark:bg-green-900/30 border border-green-400 dark:border-green-800 text-green-700 dark:text-green-400 px-4 py-3 rounded-lg">
              {success}
            </div>
          )}

          <Select
            label="Select Property"
            value={selectedPropertyId}
            onChange={(e) => setSelectedPropertyId(e.target.value)}
            options={[
              { value: '', label: 'Choose a property...' },
              ...properties.map((property) => ({
                value: property.id.toString(),
                label: `${property.city} - ${property.address}`,
              })),
            ]}
          />

          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-slate-200 mb-2">
              Property Image
            </label>
            <div className="border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-lg p-8 text-center hover:border-primary-500 transition-colors">
              {preview ? (
                <div className="space-y-4">
                  <img
                    src={preview}
                    alt="Preview"
                    className="max-h-64 mx-auto rounded-lg"
                  />
                  <Button
                    type="button"
                    variant="outline"
                    size="sm"
                    onClick={() => {
                      setFile(null);
                      setPreview('');
                    }}
                  >
                    Remove Image
                  </Button>
                </div>
              ) : (
                <div className="space-y-3">
                  <div className="flex justify-center">
                    <Image size={48} className="text-gray-400" />
                  </div>
                  <div>
                    <label
                      htmlFor="file-upload"
                      className="cursor-pointer text-primary-500 hover:text-primary-600 font-semibold"
                    >
                      Choose a file
                    </label>
                    <input
                      id="file-upload"
                      type="file"
                      accept="image/*"
                      onChange={handleFileChange}
                      className="hidden"
                    />
                    <p className="text-gray-500 dark:text-slate-300 text-sm mt-1">
                      or drag and drop
                    </p>
                  </div>
                  <p className="text-xs text-gray-500 dark:text-slate-300">
                    PNG, JPG, GIF up to 10MB
                  </p>
                </div>
              )}
            </div>
          </div>

          <div className="flex gap-4">
            <Button
              type="submit"
              fullWidth
              size="lg"
              disabled={loading || !file || !selectedPropertyId}
            >
              {loading ? 'Uploading...' : 'Upload Image'}
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
