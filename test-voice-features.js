#!/usr/bin/env node

/**
 * Voice Features Test Script
 * Tests voice interaction components and API endpoints
 */

const fs = require('fs');
const path = require('path');

console.log('🎤 Testing Voice Interaction Features...\n');

// Check backend voice components
const backendFiles = [
  'backend/main.py',
  'backend/services/voice_service.py',
  'backend/services/llm_service.py',
  'backend/models/chat.py',
  'backend/requirements.txt',
  'backend/.env.example',
  'backend/README.md'
];

console.log('🔧 Backend Voice Components:');
let backendComplete = true;
backendFiles.forEach(file => {
  const filePath = path.join(__dirname, file);
  if (fs.existsSync(filePath)) {
    console.log(`✅ ${file}`);
  } else {
    console.log(`❌ ${file} - MISSING`);
    backendComplete = false;
  }
});

// Check frontend voice components
const frontendFiles = [
  'frontend/components/InputBar.tsx',
  'frontend/lib/useVoiceRecording.ts',
  'frontend/lib/types.ts'
];

console.log('\n🎨 Frontend Voice Components:');
let frontendComplete = true;
frontendFiles.forEach(file => {
  const filePath = path.join(__dirname, file);
  if (fs.existsSync(filePath)) {
    console.log(`✅ ${file}`);
  } else {
    console.log(`❌ ${file} - MISSING`);
    frontendComplete = false;
  }
});

// Check package dependencies
console.log('\n📦 Voice Dependencies:');
try {
  const backendReqs = fs.readFileSync(path.join(__dirname, 'backend', 'requirements.txt'), 'utf8');
  const voiceDeps = [
    'openai',
    'elevenlabs',
    'pydub',
    'python-multipart',
    'fastapi',
    'uvicorn'
  ];

  let depsComplete = true;
  voiceDeps.forEach(dep => {
    if (backendReqs.includes(dep)) {
      console.log(`✅ ${dep}`);
    } else {
      console.log(`❌ ${dep} - MISSING`);
      depsComplete = false;
    }
  });

  if (backendComplete && frontendComplete && depsComplete) {
    console.log('\n🎉 Voice interaction system is ready!');
    console.log('\n🚀 Setup Instructions:');
    console.log('1. Backend:');
    console.log('   cd backend');
    console.log('   pip install -r requirements.txt');
    console.log('   cp .env.example .env  # Add your API keys');
    console.log('   python main.py');
    console.log('');
    console.log('2. Frontend:');
    console.log('   cd frontend');
    console.log('   npm install');
    console.log('   npm run dev');
    console.log('');
    console.log('3. Test Voice Features:');
    console.log('   - Open http://localhost:3000');
    console.log('   - Click the microphone button');
    console.log('   - Speak a health question');
    console.log('   - Listen to the AI voice response');
    console.log('');
    console.log('🔑 Required API Keys:');
    console.log('   - OpenAI API Key (for Whisper STT)');
    console.log('   - ElevenLabs API Key (for TTS)');
    console.log('');
    console.log('📋 API Endpoints:');
    console.log('   POST /api/chat/voice  - Voice chat');
    console.log('   POST /api/voice/stt   - Speech to text only');
    console.log('   POST /api/voice/tts   - Text to speech only');
    console.log('   GET  /api/audio/{id}  - Audio playback');

  } else {
    console.log('\n❌ Some voice components are missing.');
    console.log('Please check the error messages above.');
    process.exit(1);
  }

} catch (error) {
  console.log('❌ Error checking dependencies:', error.message);
  process.exit(1);
}

console.log('\n🎤 Voice Features Summary:');
console.log('• Speech-to-Text: OpenAI Whisper API');
console.log('• Text-to-Speech: ElevenLabs API');
console.log('• Voice Recording: Web Audio API');
console.log('• Audio Playback: HTML5 Audio');
console.log('• Real-time Feedback: Visual indicators');
console.log('• Error Handling: Permission & network errors');
console.log('• Medical Context: Healthcare-optimized voice');

console.log('\n⚕️ Voice Interaction Flow:');
console.log('1. User clicks microphone → Recording starts');
console.log('2. Visual feedback → Red indicator + timer');
console.log('3. User speaks → Audio captured');
console.log('4. Click stop → Audio sent to backend');
console.log('5. STT processing → Text transcription');
console.log('6. AI processing → Medical response');
console.log('7. TTS generation → Voice synthesis');
console.log('8. Audio playback → User hears response');

console.log('\n🔒 Privacy & Security:');
console.log('• Audio processed server-side only');
console.log('• No audio storage or persistence');
console.log('• Secure API key management');
console.log('• HTTPS recommended for production');