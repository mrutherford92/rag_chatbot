#!/bin/bash
# run_all.sh - Launches both Backend and Frontend

# Function to kill child processes on exit
trap 'kill $(jobs -p)' EXIT

echo "Starting RAG Chatbot System..."

# 1. Start Backend in Background
echo "1. Launching Backend (FastAPI)..."
uv run uvicorn app.backend.main:app --host 127.0.0.1 --port 8000 --reload &
BACKEND_PID=$!

# Wait for backend to be ready
echo "Waiting for backend to start..."
sleep 5

# 2. Start Frontend
echo "2. Launching Frontend (Streamlit)..."
PYTHONPATH=. uv run streamlit run app/frontend/dashboard.py

# When frontend exits, script exits and trap kills backend
