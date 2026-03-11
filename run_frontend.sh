#!/bin/bash

# Start Frontend Server
echo "🎨 Starting Healthcare Assistant Frontend..."
echo "=============================================="

cd frontend || { echo "❌ Frontend directory not found"; exit 1; }

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "⚠️  Dependencies not installed. Installing..."
    npm install
fi

echo ""
echo "✅ Frontend starting on http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

npm run dev
