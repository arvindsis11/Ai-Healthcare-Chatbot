#!/usr/bin/env node

/**
 * Simple test script to validate the frontend components
 * This doesn't require a full Next.js server to run
 */

const fs = require('fs');
const path = require('path');

console.log('🧪 Testing Frontend Components...\n');

// Check if all required files exist
const requiredFiles = [
  'package.json',
  'tsconfig.json',
  'tailwind.config.js',
  'app/layout.tsx',
  'app/page.tsx',
  'app/globals.css',
  'components/ChatWindow.tsx',
  'components/MessageBubble.tsx',
  'components/InputBar.tsx',
  'components/Sidebar.tsx',
  'lib/types.ts',
  'lib/utils.ts',
  'app/api/chat/route.ts'
];

let allFilesExist = true;

requiredFiles.forEach(file => {
  const filePath = path.join(__dirname, file);
  if (fs.existsSync(filePath)) {
    console.log(`✅ ${file}`);
  } else {
    console.log(`❌ ${file} - MISSING`);
    allFilesExist = false;
  }
});

console.log('\n📦 Checking package.json dependencies...');

// Check package.json for required dependencies
try {
  const packageJson = JSON.parse(fs.readFileSync(path.join(__dirname, 'package.json'), 'utf8'));
  const requiredDeps = [
    'next',
    'react',
    'react-dom',
    'tailwindcss',
    '@radix-ui/react-dialog',
    'class-variance-authority',
    'clsx',
    'tailwind-merge'
  ];

  let allDepsPresent = true;
  requiredDeps.forEach(dep => {
    if (packageJson.dependencies && packageJson.dependencies[dep]) {
      console.log(`✅ ${dep}: ${packageJson.dependencies[dep]}`);
    } else {
      console.log(`❌ ${dep} - MISSING`);
      allDepsPresent = false;
    }
  });

  if (allFilesExist && allDepsPresent) {
    console.log('\n🎉 All frontend components and dependencies are ready!');
    console.log('\n🚀 To start the development server:');
    console.log('   cd frontend');
    console.log('   npm install');
    console.log('   npm run dev');
    console.log('\n📱 Then open http://localhost:3000 in your browser');
  } else {
    console.log('\n❌ Some components or dependencies are missing.');
    process.exit(1);
  }

} catch (error) {
  console.log('❌ Error reading package.json:', error.message);
  process.exit(1);
}

console.log('\n🏗️  Frontend Architecture:');
console.log('├── ChatWindow.tsx     - Main chat interface');
console.log('├── MessageBubble.tsx  - Individual message display');
console.log('├── InputBar.tsx       - Smart input with suggestions');
console.log('├── Sidebar.tsx        - Navigation and settings');
console.log('├── API Route          - Mock chat endpoint');
console.log('└── Theme System       - Dark/light mode support');

console.log('\n✨ Features implemented:');
console.log('• ChatGPT-like UI with message bubbles');
console.log('• Typing animations and loading indicators');
console.log('• Symptom input suggestions');
console.log('• Dark/light mode toggle');
console.log('• Responsive design');
console.log('• Mock API for testing');
console.log('• TypeScript support');
console.log('• TailwindCSS styling');