# Getting Started

## Prerequisites
- Node.js 18+ (check with `node --version`)
- npm or yarn
- Backend server running on http://localhost:8000

## Initial Setup

1. **Install dependencies**
   ```bash
   cd frontend
   npm install
   ```

2. **Start development server**
   ```bash
   npm run dev
   ```

   The application will be available at http://localhost:3000

3. **Run with backend** (recommended)
   ```bash
   npm run dev:all
   ```

   This starts both the backend and frontend servers concurrently.

## Configuration

### Environment Variables
Nuxt environment variables are configured in `nuxt.config.ts`. Currently, the app uses Nitro route rules for API proxying:

```typescript
nitro: {
  routeRules: {
    '/db/**': { proxy: 'http://localhost:8000/api/**' }
  }
}
```

This proxies frontend requests from `/db/**` to the backend API at `/api/**`.
