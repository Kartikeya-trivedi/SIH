import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    // Enable history API fallback for SPA routing in development
    historyApiFallback: true
  },
  preview: {
    // Enable history API fallback for SPA routing in preview mode
    historyApiFallback: true
  }
})
