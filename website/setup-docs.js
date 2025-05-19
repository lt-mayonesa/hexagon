const fs = require('fs');
const path = require('path');

// Create necessary directories
const directories = [
  'docs/getting-started',
  'docs/guides',
  'docs/advanced',
  'docs/api',
  'docs/api/actions',
  'docs/api/support'
];

directories.forEach(dir => {
  const fullPath = path.join(__dirname, dir);
  if (!fs.existsSync(fullPath)) {
    fs.mkdirSync(fullPath, { recursive: true });
    console.log(`Created directory: ${fullPath}`);
  }
});

console.log('Documentation structure setup complete!');
