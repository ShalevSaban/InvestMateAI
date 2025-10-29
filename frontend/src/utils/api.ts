import {
  Agent,
  Property,
  ChatResponse,
  AuthTokens,
  LoginCredentials,
  RegisterData,
} from '@/types';

const API_URL =
  import.meta.env.VITE_API_URL || 'http://localhost:8000';

console.log('🔗 Using API URL:', API_URL);

// פונקציה כללית להוספת base URL לכל fetch
async function fetchWithBase(path: string, options: RequestInit = {}) {
  const url = `${API_URL}${path.startsWith('/') ? path : `/${path}`}`;
  return fetch(url, options);
}

export const api = {
  // 🧾 Auth
  async login(credentials: LoginCredentials): Promise<AuthTokens> {
    const formData = new URLSearchParams();
    formData.append('username', credentials.email);
    formData.append('password', credentials.password);

    const response = await fetchWithBase('/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: formData,
    });

    if (!response.ok) {
      const text = await response.text();
      console.error('❌ Login failed:', text);
      throw new Error('Login failed');
    }

    return response.json();
  },

  async register(data: RegisterData): Promise<Agent> {
    const response = await fetchWithBase('/agents/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      const text = await response.text();
      console.error('❌ Registration failed:', text);
      throw new Error('Registration failed');
    }

    return response.json();
  },

  // 🧍‍♂️ Agents
  async getAgents(): Promise<Agent[]> {
    const response = await fetchWithBase('/agents/');
    if (!response.ok) {
      throw new Error('Failed to fetch agents');
    }
    return response.json();
  },

  async getAgentById(id: number, token: string): Promise<Agent> {
    const response = await fetchWithBase(`/agents/${id}`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    if (!response.ok) {
      throw new Error('Failed to fetch agent');
    }
    return response.json();
  },

  // 🏠 Properties
  async getProperties(token?: string): Promise<Property[]> {
    const headers: HeadersInit = {};
    if (token) headers['Authorization'] = `Bearer ${token}`;

    const response = await fetchWithBase('/properties/', { headers });
    if (!response.ok) {
      throw new Error('Failed to fetch properties');
    }
    return response.json();
  },

  async createProperty(
    data: Omit<Property, 'id' | 'agent'>,
    token: string
  ): Promise<Property> {
    const response = await fetchWithBase('/properties/', {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      const text = await response.text();
      console.error('❌ Failed to create property:', text);
      throw new Error('Failed to create property');
    }
    return response.json();
  },

  async uploadPropertyImage(
    propertyId: string,
    file: File,
    token: string
  ): Promise<{ image_url: string }> {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetchWithBase(
      `/properties/${propertyId}/upload-image`,
      {
        method: 'POST',
        headers: { Authorization: `Bearer ${token}` },
        body: formData,
      }
    );

    if (!response.ok) {
      throw new Error('Failed to upload image');
    }
    return response.json();
  },

  async getPropertyImageUrl(
    propertyId: string
  ): Promise<{ image_url: string }> {
    const response = await fetchWithBase(`/properties/${propertyId}/image-url`);
    if (!response.ok) {
      throw new Error('Failed to fetch image URL');
    }
    return response.json();
  },

  // 💬 Chat
  async chat(
    question: string,
    agentId: string,
    token?: string
  ): Promise<ChatResponse> {
    const headers: HeadersInit = { 'Content-Type': 'application/json' };
    if (token) headers['Authorization'] = `Bearer ${token}`;

    const body = JSON.stringify({ question, agent_id: agentId });
    const response = await fetchWithBase('/gpt/chat/', {
      method: 'POST',
      headers,
      body,
    });

    if (!response.ok) {
      const text = await response.text();
      console.error('❌ Chat request failed:', text);
      throw new Error(`Chat request failed (${response.status})`);
    }
    return response.json();
  },

  // 📊 Dashboard
  async getChatInsights(token: string): Promise<any> {
    const response = await fetchWithBase('/api/dashboard/insights', {
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
    });

    const text = await response.text();
    if (!response.ok) {
      console.error('❌ Insights fetch failed:', text);
      throw new Error(`Failed to fetch insights (${response.status})`);
    }

    try {
      return JSON.parse(text);
    } catch (err) {
      console.error('❌ Failed to parse insights JSON:', err);
      throw new Error('Response is not valid JSON');
    }
  },
};
