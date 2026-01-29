#!/bin/bash
# run_frontend.sh - Run utility for the Streamlit UI

echo "Starting Frontend..."
PYTHONPATH=. uv run streamlit run app/frontend/dashboard.py
