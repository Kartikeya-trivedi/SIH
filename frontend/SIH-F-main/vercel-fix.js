import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

// Get the current directory
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Simple script to make a copy of each component file with proper capitalization
// Will only run in the Vercel environment where the filesystem is case-sensitive

// Always run this script
console.log('Running case-sensitivity fix for Vercel deployment...');

const componentsDir = path.join(__dirname, 'src', 'components');

// List of files to duplicate with proper capitalization
const files = [
  { source: 'navbar.jsx', target: 'Navbar.jsx' },
  { source: 'home.jsx', target: 'Home.jsx' },
  { source: 'knowledge.jsx', target: 'Knowledge.jsx' },
  { source: 'recognize.jsx', target: 'Recognize.jsx' },
  { source: 'analysis.jsx', target: 'Analysis.jsx' },
  { source: 'quiz.jsx', target: 'Quiz.jsx' }
];

files.forEach(file => {
  const sourcePath = path.join(componentsDir, file.source);
  const targetPath = path.join(componentsDir, file.target);
  
  try {
    if (fs.existsSync(sourcePath)) {
      const content = fs.readFileSync(sourcePath, 'utf8');
      fs.writeFileSync(targetPath, content);
      console.log(`Created ${file.target} from ${file.source}`);
    } else {
      console.log(`Source file ${file.source} not found`);
    }
  } catch (error) {
    console.error(`Error processing ${file.source}:`, error);
  }
});

console.log('Case sensitivity fix complete.');