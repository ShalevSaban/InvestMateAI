import { defineConfig, loadEnv } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';
import process from 'process';

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '');
  const API_URL = env.VITE_API_URL || 'http://investmate-backend:8000';

  return {
    plugins: [react()],
    resolve: {
      alias: {
        '@': path.resolve(__dirname, './src'),
      },
    },
    css: {
      postcss: './postcss.config.js',
    },
    server: {
      port: 3000,
      proxy: {
        // ✅ כל הנתיבים הרלוונטיים
        '/agents': {
          target: API_URL,
          changeOrigin: true,
          secure: false,
        },
        '/auth': {
          target: API_URL,
          changeOrigin: true,
          secure: false,
        },
        '/properties': {
          target: API_URL,
          changeOrigin: true,
          secure: false,
        },
        '/gpt': {
          target: API_URL,
          changeOrigin: true,
          secure: false,
        },
        '/api': {
          target: API_URL,
          changeOrigin: true,
          secure: false,
        },
      },
    },
    // ✅ מאפשר גישה טובה יותר בפרודקשן (build)
    preview: {
      port: 4173,
      proxy: {
        '/agents': API_URL,
        '/auth': API_URL,
        '/properties': API_URL,
        '/gpt': API_URL,
      },
    },
  };
});
