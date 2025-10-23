/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'selector',
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
      }
    },
  },
  plugins: [],
}
