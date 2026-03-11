#!/bin/bash

# Full Stack Startup Script
# Starts both backend and frontend servers

echo "🏥 AI Healthcare Chatbot - Full Stack Startup"
echo "=============================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping servers..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit 0
}

trap cleanup SIGINT SIGTERM

# Start Backend
echo -e "${BLUE}Starting Backend...${NC}"
bash run_backend.sh &
BACKEND_PID=$!
sleep 3

# Start Frontend
echo ""
echo -e "${BLUE}Starting Frontend...${NC}"
bash run_frontend.sh &
FRONTEND_PID=$!
sleep 3

echo ""
echo -e "${GREEN}✅ Both servers are running!${NC}"
echo ""
echo "Backend:  http://localhost:8000"
echo "Frontend: http://localhost:3000"
echo "Docs:     http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop both servers"
echo ""

# Wait for both processes
wait $BACKEND_PID $FRONTEND_PID
