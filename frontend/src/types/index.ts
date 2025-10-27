export interface Agent {
  id: string;
  email: string;
  full_name: string;
  phone_number: string;
  agency_name?: string;
  license_number?: string;
}

export interface Property {
  id: string;
  address: string;
  city: string;
  price: number;
  rooms: number;
  floor: number;
  property_type: string;
  description?: string;
  yield_percent?: number;
  rental_estimate?: number;
  agent?: Agent;
  image_url?: string;
}

export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  properties?: Property[];
}

export interface ChatResponse {
  message: string;
  results?: Property[];
}

export interface AuthTokens {
  access_token: string;
  token_type: string;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterData {
  email: string;
  password: string;
  full_name: string;
  phone_number: string;
  agency_name?: string;
  license_number?: string;
}
