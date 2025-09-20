@echo off
echo Building project for preview...
npm run build
echo.
echo Starting preview server with SPA routing...
echo You can access your app at http://localhost:4173/
echo Try navigating directly to routes like http://localhost:4173/knowledge to test SPA routing
echo.
npm run preview