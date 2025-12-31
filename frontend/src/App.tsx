import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider } from './context/ThemeContext';
import { AuthProvider } from './context/AuthContext';
import { Layout } from './components/layout/Layout';
import { Home } from './pages/Home';
import { Login } from './pages/Login';
import { Register } from './pages/Register';
import { Dashboard } from './pages/Dashboard';
import { Chat } from './pages/Chat';
import { AddProperty } from './pages/AddProperty';
import { UploadImage } from './pages/UploadImage';
import { ChatInsights } from './pages/ChatInsights';
import { useEffect } from 'react';

function App() {
  useEffect(() => {
  const wakeBackend = async () => {
    const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

    try {
      const start = performance.now();
      const response = await fetch(`${API_URL}/agents/health`); // ✅ עם base URL

      if (response.ok) {
        const duration = Math.round(performance.now() - start);
        console.log(`✅ Backend awake in ${duration}ms`);
      }
    } catch (err) {
      console.error('❌ Backend wake failed:', err);
    }
  };

  wakeBackend();
}, []);
  return (
    <ThemeProvider>
      <AuthProvider>
        <Router>
          <Layout>
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/login" element={<Login />} />
              <Route path="/register" element={<Register />} />
              <Route path="/dashboard" element={<Dashboard />} />
              <Route path="/chat" element={<Chat />} />
              <Route path="/add-property" element={<AddProperty />} />
              <Route path="/upload-image" element={<UploadImage />} />
              <Route path="/insights" element={<ChatInsights />} />

            </Routes>
          </Layout>
        </Router>
      </AuthProvider>
    </ThemeProvider>
  );
}

export default App;
