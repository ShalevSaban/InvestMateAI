import { Agent, Property, ChatResponse, AuthTokens, LoginCredentials, RegisterData } from '@/types';

export const api = {
  // Auth
  async login(credentials: LoginCredentials): Promise<AuthTokens> {
    const formData = new URLSearchParams();
    formData.append('username', credentials.email);
    formData.append('password', credentials.password);

    const response = await fetch('/auth/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: formData,
    });

    if (!response.ok) {
      throw new Error('Login failed');
    }

    return response.json();
  },

  async register(data: RegisterData): Promise<Agent> {
    const response = await fetch('/agents/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      throw new Error('Registration failed');
    }

    return response.json();
  },

  // Agents
  async getAgents(): Promise<Agent[]> {
    const response = await fetch('/agents/');
    if (!response.ok) {
      throw new Error('Failed to fetch agents');
    }
    return response.json();
  },

  async getAgentById(id: number, token: string): Promise<Agent> {
    const response = await fetch(`/agents/${id}`, {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });
    if (!response.ok) {
      throw new Error('Failed to fetch agent');
    }
    return response.json();
  },

  // Properties
  async getProperties(token?: string): Promise<Property[]> {
    const headers: HeadersInit = {};
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    const response = await fetch('/properties/', { headers });
    if (!response.ok) {
      throw new Error('Failed to fetch properties');
    }
    return response.json();
  },

  async createProperty(data: Omit<Property, 'id' | 'agent'>, token: string): Promise<Property> {
    const response = await fetch('/properties/', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      throw new Error('Failed to create property');
    }
    return response.json();
  },

  async uploadPropertyImage(propertyId: number, file: File, token: string): Promise<{ image_url: string }> {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch(`/properties/${propertyId}/upload-image`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
      },
      body: formData,
    });

    if (!response.ok) {
      throw new Error('Failed to upload image');
    }
    return response.json();
  },

  async getPropertyImageUrl(propertyId: number): Promise<{ image_url: string }> {
    const response = await fetch(`/properties/${propertyId}/image-url`);
    if (!response.ok) {
      throw new Error('Failed to fetch image URL');
    }
    return response.json();
  },

  // Chat
  async chat(question: string, agentId: number, token?: string): Promise<ChatResponse> {
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
    };
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    const response = await fetch('/gpt/chat/', {
      method: 'POST',
      headers,
      body: JSON.stringify({
        question,
        agent_id: agentId,
      }),
    });

    if (!response.ok) {
      throw new Error('Chat request failed');
    }
    return response.json();
  },

  async getChatInsights(token: string): Promise<any[]> {
    const response = await fetch('/gpt/insights/', {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      throw new Error('Failed to fetch insights');
    }
    return response.json();
  },
};
