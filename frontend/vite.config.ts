import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    port: 3000,
    proxy: {
      '/agents': 'http://localhost:8000',
      '/gpt': 'http://localhost:8000',
      '/properties': 'http://localhost:8000',
      '/auth': 'http://localhost:8000',
    }
  }
})
