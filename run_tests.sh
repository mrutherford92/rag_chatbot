#!/bin/bash
# run_tests.sh - Run utility for the test suite

echo "Running Full Test Suite..."
# Ensure PYTHONPATH includes the current directory so 'app' module is found
PYTHONPATH=. uv run pytest tests/
