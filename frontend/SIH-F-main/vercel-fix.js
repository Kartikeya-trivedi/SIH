import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

// Get the current directory
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Simple script to make a copy of each component file with proper capitalization
// Will only run in the Vercel environment where the filesystem is case-sensitive

console.log('Running case-sensitivity fix for Vercel deployment...');

const componentsDir = path.join(__dirname, 'src', 'components');

// List of files to duplicate with proper capitalization for JSX files
const jsxFiles = [
  { source: 'navbar.jsx', target: 'Navbar.jsx' },
  { source: 'home.jsx', target: 'Home.jsx' },
  { source: 'knowledge.jsx', target: 'Knowledge.jsx' },
  { source: 'recognize.jsx', target: 'Recognize.jsx' },
  { source: 'analysis.jsx', target: 'Analysis.jsx' },
  { source: 'quiz.jsx', target: 'Quiz.jsx' },
  { source: 'AiRecreate.jsx', target: 'airecreate.jsx' },
  { source: 'features.jsx', target: 'Features.jsx' },
  { source: 'knowledge-query.jsx', target: 'Knowledge-query.jsx' },
  { source: 'levelselect.jsx', target: 'Levelselect.jsx' },
  { source: 'progressbar.jsx', target: 'Progressbar.jsx' },
  { source: 'quizcard.jsx', target: 'Quizcard.jsx' },
  { source: 'quizData.jsx', target: 'QuizData.jsx' },
  { source: 'quizgame.jsx', target: 'Quizgame.jsx' },
  { source: 'splashcard.jsx', target: 'Splashcard.jsx' },
  { source: 'splashscreen.jsx', target: 'Splashscreen.jsx' }
];

// List of files to duplicate with proper capitalization for CSS files
const cssFiles = [
  { source: 'home.css', target: 'Home.css' },
  { source: 'Home.css', target: 'home.css' },
  { source: 'navbar.css', target: 'Navbar.css' },
  { source: 'Navbar.css', target: 'navbar.css' },
  { source: 'knowledge.css', target: 'Knowledge.css' },
  { source: 'Knowledge.css', target: 'knowledge.css' },
  { source: 'recognize.css', target: 'Recognize.css' },
  { source: 'Recognize.css', target: 'recognize.css' },
  { source: 'analysis.css', target: 'Analysis.css' },
  { source: 'Analysis.css', target: 'analysis.css' },
  { source: 'quiz.css', target: 'Quiz.css' },
  { source: 'Quiz.css', target: 'quiz.css' },
  { source: 'AiRecreate.css', target: 'airecreate.css' },
  { source: 'airecreate.css', target: 'AiRecreate.css' },
  { source: 'features.css', target: 'Features.css' },
  { source: 'Features.css', target: 'features.css' },
  { source: 'analyze-button.css', target: 'Analyze-button.css' },
  { source: 'Analyze-button.css', target: 'analyze-button.css' },
  { source: 'knowledge-query.css', target: 'Knowledge-query.css' },
  { source: 'Knowledge-query.css', target: 'knowledge-query.css' },
  { source: 'knowledge-query-section.css', target: 'Knowledge-query-section.css' },
  { source: 'Knowledge-query-section.css', target: 'knowledge-query-section.css' },
  { source: 'quizcard.css', target: 'Quizcard.css' },
  { source: 'Quizcard.css', target: 'quizcard.css' }
];

// Function to safely create a copy of a file if it exists
const safelyCopyFile = (sourcePath, targetPath) => {
  try {
    if (fs.existsSync(sourcePath)) {
      const content = fs.readFileSync(sourcePath, 'utf8');
      fs.writeFileSync(targetPath, content);
      console.log(`Created ${path.basename(targetPath)} from ${path.basename(sourcePath)}`);
      return true;
    } else {
      console.log(`Source file ${path.basename(sourcePath)} not found - skipping`);
      return false;
    }
  } catch (error) {
    console.error(`Error processing ${path.basename(sourcePath)}:`, error);
    return false;
  }
};

// Process JSX files
jsxFiles.forEach(file => {
  const sourcePath = path.join(componentsDir, file.source);
  const targetPath = path.join(componentsDir, file.target);
  safelyCopyFile(sourcePath, targetPath);
});

// Process CSS files
cssFiles.forEach(file => {
  const sourcePath = path.join(componentsDir, file.source);
  const targetPath = path.join(componentsDir, file.target);
  safelyCopyFile(sourcePath, targetPath);
});

console.log('Case sensitivity fix complete.');