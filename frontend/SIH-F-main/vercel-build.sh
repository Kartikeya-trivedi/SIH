#!/bin/bash
# This script creates case-insensitive symlinks for components
# to ensure compatibility between Windows and Linux file systems

# Create symlinks for case-sensitive files
cd src/components
ln -sf navbar.jsx Navbar.jsx
ln -sf home.jsx Home.jsx
ln -sf knowledge.jsx Knowledge.jsx
ln -sf recognize.jsx Recognize.jsx
ln -sf analysis.jsx Analysis.jsx
ln -sf quiz.jsx Quiz.jsx

# Return to root directory and run the regular build
cd ../..
npm run build
npm run build