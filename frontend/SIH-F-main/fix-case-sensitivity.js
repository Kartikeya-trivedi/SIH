// fix-case-sensitivity.js
// This script creates case-sensitive versions of component files for deployment on case-sensitive file systems
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const componentsDir = path.join(__dirname, 'src', 'components');

// List of components that need case-sensitive versions
const componentsToFix = [
  { lowercase: 'navbar.jsx', uppercase: 'Navbar.jsx' },
  { lowercase: 'home.jsx', uppercase: 'Home.jsx' },
  { lowercase: 'knowledge.jsx', uppercase: 'Knowledge.jsx' },
  { lowercase: 'recognize.jsx', uppercase: 'Recognize.jsx' },
  { lowercase: 'analysis.jsx', uppercase: 'Analysis.jsx' },
  { lowercase: 'quiz.jsx', uppercase: 'Quiz.jsx' }
];

console.log('Creating case-sensitive component files for deployment...');

componentsToFix.forEach(component => {
  const lowerPath = path.join(componentsDir, component.lowercase);
  const upperPath = path.join(componentsDir, component.uppercase);
  
  try {
    if (fs.existsSync(lowerPath)) {
      const content = fs.readFileSync(lowerPath, 'utf8');
      // Create the uppercase version with the same content
      fs.writeFileSync(upperPath, content);
      console.log(`Created ${component.uppercase} from ${component.lowercase}`);
    } else {
      console.error(`Source file ${component.lowercase} not found`);
    }
  } catch (error) {
    console.error(`Error processing ${component.lowercase}:`, error);
  }
});

console.log('Case sensitivity fix complete.');