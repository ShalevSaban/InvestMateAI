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
        primary: {
          50: '#e6f2ff',
          100: '#bae0ff',
          200: '#8dceff',
          300: '#61bcff',
          400: '#34aaff',
          500: '#3498db',
          600: '#2980b9',
          700: '#1f6897',
          800: '#145075',
          900: '#0a3853',
        },
        dark: {
          bg: '#0f172a',
          card: '#1e293b',
          hover: '#334155',
        }
      }
    },
  },
  plugins: [],
}
