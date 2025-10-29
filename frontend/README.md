# InvestMateAI Frontend

A professional, modern React + TypeScript frontend for the InvestMateAI real estate platform, featuring dark mode support and full mobile responsiveness.

## Features

- **React 19** with **TypeScript** for type safety
- **Vite** for lightning-fast development and builds
- **Tailwind CSS** for modern, utility-first styling
- **Dark Mode** with system preference detection
- **Fully Responsive** - optimized for mobile, tablet, and desktop
- **React Router** for client-side routing
- **Lucide React** for beautiful, consistent icons

## Tech Stack

- React 19.2.0
- TypeScript 5.9.3
- Vite 7.1.12
- Tailwind CSS 4.1.16
- React Router DOM 7.9.4
- Lucide React (icons)

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── layout/          # Layout components (Navbar, Layout, DarkModeToggle)
│   │   ├── ui/              # Reusable UI components (Button, Input, Card, etc.)
│   │   └── PropertyCard.tsx # Property display component
│   ├── context/             # React Context (Theme, Auth)
│   ├── pages/               # Page components
│   │   ├── Home.tsx
│   │   ├── Login.tsx
│   │   ├── Register.tsx
│   │   ├── Dashboard.tsx
│   │   ├── Chat.tsx
│   │   ├── AddProperty.tsx
│   │   ├── UploadImage.tsx
│   │   └── ChatInsights.tsx
│   ├── types/               # TypeScript type definitions
│   ├── utils/               # Utility functions (API calls)
│   ├── App.tsx              # Main app component with routing
│   ├── main.tsx             # App entry point
│   └── index.css            # Global styles with Tailwind
├── public/
│   └── logo.svg             # App logo (placeholder)
├── index.html               # HTML template with logo placeholder
├── vite.config.ts           # Vite configuration
├── tailwind.config.js       # Tailwind configuration with dark mode
├── tsconfig.json            # TypeScript configuration
└── package.json             # Dependencies and scripts
```

## Getting Started

### Prerequisites

- Node.js 18+ and npm

### Installation

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

### Development

Start the development server:
```bash
npm run dev
```

The app will be available at `http://localhost:3000`

### Building for Production

Build the app for production:
```bash
npm run build
```

Preview the production build:
```bash
npm run preview
```

### Type Checking

Run TypeScript type checking:
```bash
npm run lint
```

## Pages & Features

### Public Pages
- **Home** (`/`) - Landing page with logo and navigation
- **Login** (`/login`) - Agent authentication
- **Register** (`/register`) - New agent registration
- **Chat** (`/chat`) - Public chat interface with AI agent

### Protected Pages (Require Authentication)
- **Dashboard** (`/dashboard`) - Agent dashboard with quick actions
- **Add Property** (`/add-property`) - Create new property listings
- **Upload Image** (`/upload-image`) - Upload property photos
- **Chat Insights** (`/insights`) - View client interaction analytics

## Dark Mode

The app includes a built-in dark mode toggle that:
- Saves preference to localStorage
- Supports system preference detection
- Smoothly transitions between themes
- Uses Tailwind's `dark:` classes for styling

Toggle dark mode using the button in the navbar.

## Mobile Responsiveness

All components are fully responsive with:
- Mobile-first design approach
- Tailwind responsive breakpoints (sm, md, lg)
- Touch-friendly UI elements
- Optimized layouts for different screen sizes

## API Integration

The frontend connects to the backend API (assumed to run on port 8000) through:
- Vite proxy configuration for development
- API utility functions in `src/utils/api.ts`
- Auth context for token management
- TypeScript types for all API responses

## Customization

### Logo
Replace the placeholder logo at:
- `public/logo.svg` - Main logo
- Update the logo display component in `src/pages/Home.tsx`

### Colors
Modify the color scheme in `tailwind.config.js`:
```javascript
colors: {
  primary: {
    // Your brand colors
  }
}
```

### API Endpoint
Update the backend URL in `vite.config.ts` proxy settings if needed.

## Components

### UI Components
- **Button** - Flexible button with variants (primary, secondary, outline, ghost)
- **Input** - Form input with label and error support
- **Card** - Container with consistent styling
- **Select** - Dropdown select component
- **Textarea** - Multi-line text input

### Layout Components
- **Layout** - Main app layout wrapper
- **Navbar** - Top navigation with logo and dark mode toggle
- **DarkModeToggle** - Theme switcher button

## License

ISC

## Notes

- All pages are styled with dark mode support
- Mobile-responsive design implemented throughout
- Logo placeholder included (replace with actual logo)
- Clean, organized, and easily maintainable code structure
