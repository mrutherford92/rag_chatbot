#!/bin/bash
clear
echo "Starting Backend..."
uv run uvicorn app.backend.main:app --host 127.0.0.1 --port 8000 --reload
