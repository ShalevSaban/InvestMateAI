/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        // Light Mode Colors
        light: {
          bg: '#F8F9FB',
          card: '#FFFFFF',
          text: '#1E1E1E',
          textSecondary: '#555B65',
          border: '#E2E4E8',
        },
        // Dark Mode Colors
        dark: {
          bg: '#0D0E0F',
          card: '#1A1B1E',
          text: '#E0E3E7',
          textSecondary: '#A0A4AA',
          border: '#2B2D31',
        },
        // Primary Blue
        primary: {
          light: '#007BFF',
          dark: '#0099FF',
          hover: '#005FCC',
          hoverDark: '#4E68FF',
        },
        // Accent Purple
        accent: {
          light: '#6B3EFF',
          dark: '#9142FF',
        },
      }
    },
  },
  plugins: [],
}
