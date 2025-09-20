@echo off
echo Building and serving your React app with React Router...
echo.
echo Step 1: Building the application...
call npm run build
echo.
echo Step 2: Starting the preview server...
echo You can access your app at http://localhost:4173/
echo Try navigating directly to routes like:
echo - http://localhost:4173/knowledge
echo - http://localhost:4173/recognize
echo - http://localhost:4173/recreate
echo.
echo Press Ctrl+C to stop the server when done.
call npm run preview