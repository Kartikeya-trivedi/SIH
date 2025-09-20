@echo off
echo Building project for debugging...
npm run build
echo.
echo Starting preview server with debugging information...
echo Open your browser to http://localhost:4173/knowledge
echo Check your browser's console (F12) for any errors
echo.
set "VITE_DEBUG=true"
npm run preview