import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// Vite configuration for React + TypeScript
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    // Proxy API requests to backend server (optional if using direct URL in api.ts)
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')
      }
    }
  }
})
