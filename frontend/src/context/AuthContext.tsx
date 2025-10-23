import React, { createContext, useContext, useState, useEffect } from 'react';
import { Agent, AuthTokens } from '@/types';

interface AuthContextType {
  token: string | null;
  agent: Agent | null;
  login: (tokens: AuthTokens) => void;
  logout: () => void;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [token, setToken] = useState<string | null>(() => {
    return localStorage.getItem('token');
  });
  const [agent, setAgent] = useState<Agent | null>(null);

  useEffect(() => {
    if (token) {
      localStorage.setItem('token', token);
      // Optionally fetch agent details here
    } else {
      localStorage.removeItem('token');
      setAgent(null);
    }
  }, [token]);

  const login = (tokens: AuthTokens) => {
    setToken(tokens.access_token);
  };

  const logout = () => {
    setToken(null);
    setAgent(null);
    localStorage.removeItem('token');
  };

  const isAuthenticated = !!token;

  return (
    <AuthContext.Provider value={{ token, agent, login, logout, isAuthenticated }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
