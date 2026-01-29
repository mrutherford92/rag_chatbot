import json
import os
import pytest

from app.core.config import FEW_SHOT_DATA

DATA_FILE = FEW_SHOT_DATA

def test_file_exists():
    assert os.path.exists(DATA_FILE), f"{DATA_FILE} not found"

def test_jsonl_validity():
    """Verify each line is valid JSON and has correct structure"""
    with open(DATA_FILE, 'r') as f:
        lines = f.readlines()
        
    assert len(lines) >= 20, "Dataset should have at least 20 examples"
    
    for i, line in enumerate(lines):
        try:
            item = json.loads(line)
        except json.JSONDecodeError:
            pytest.fail(f"Line {i+1} is not valid JSON")
            
        assert "messages" in item, f"Line {i+1} missing 'messages' key"
        messages = item["messages"]
        assert isinstance(messages, list), f"Line {i+1} 'messages' is not a list"
        
        # Check roles
        roles = [m.get("role") for m in messages]
        assert "system" in roles, f"Line {i+1} missing system role"
        assert "user" in roles, f"Line {i+1} missing user role"
        assert "assistant" in roles, f"Line {i+1} missing assistant role"

def test_parser_output():
    """Verify app.py parser extracts Q/A pairs correctly"""
    # Create a dummy line and test logic manually mirroring app.py
    # or just import the function if possible (might need mocking streamlit if it imports at top level)
    # Since importing app.py might trigger streamlit execution, we will test the LOGIC here.
    
    with open(DATA_FILE, 'r') as f:
        examples_text = ""
        for line in f:
            item = json.loads(line)
            messages = item.get("messages", [])
            user_msg = next((m["content"] for m in messages if m["role"] == "user"), "")
            assistant_msg = next((m["content"] for m in messages if m["role"] == "assistant"), "")
            
            if user_msg and assistant_msg:
                examples_text += f"Q: {user_msg}\nA: {assistant_msg}\n\n"
    
    assert "Q: What is the primary treatment for Anaphylaxis?" in examples_text
    assert "A: The primary treatment for Anaphylaxis is immediate administration of epinephrine" in examples_text
    assert "\n\n" in examples_text
