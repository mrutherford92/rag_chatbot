"""
Script Name:  demo.py
Description:  Walkthrough script to demonstrate RAG Chatbot capabilities via API.
Author:       Michael R. Rutherford
Date:         2026-01-28

Copyright (c) 2026
License: MIT
"""

import requests
import json
import time

from app.core.config import API_URL

def print_header(title: str) -> None:
    print(f"\n{'='*60}")
    print(f" {title}")
    print(f"{'='*60}")

def test_status() -> None:
    print_header("1. System Status")
    try:
        res = requests.get(f"{API_URL}/")
        print(f"Connection: {'OK' if res.status_code == 200 else 'FAILED'}")
        print(f"Service: {res.json().get('service')}")
    except Exception as e:
        print(f"Failed to connect: {e}")
        exit(1)

def test_direct_chat() -> None:
    print_header("2. Direct LLM Chat (No RAG)")
    payload = {
        "query": "What is the capital of France?",
        "use_rag": False,
        "temperature": 0.7
    }
    print(f"Query: {payload['query']}")
    start = time.time()
    res = requests.post(f"{API_URL}/chat", json=payload)
    print(f"Response: {res.json()['response']}")
    print(f"Time: {time.time() - start:.2f}s")

def test_rag_chat() -> None:
    print_header("3. RAG Chat (Medical Context)")
    # Assuming 'diabetes' or 'asthma' is in the dummy data
    payload = {
        "query": "What are the symptoms of Asthma?",
        "use_rag": True,
        "temperature": 0.3
    }
    print(f"Query: {payload['query']}")
    print("Fetching context from Vector Store...")
    start = time.time()
    res = requests.post(f"{API_URL}/chat", json=payload)
    if res.status_code == 200:
        print(f"Response: {res.json()['response']}")
    else:
        print(f"Error: {res.text}")
    print(f"Time: {time.time() - start:.2f}s")

def test_dynamic_few_shot() -> None:
    print_header("4. Expert Knowledge Selection")
    query = "treatment for anaphylaxis"
    print(f"User Question: {query}")
    print("Selecting 2 most relevant expert examples...")
    
    payload = {"query": query, "k": 2}
    res = requests.post(f"{API_URL}/features/select_examples", json=payload)
    
    if res.status_code == 200:
        examples = res.json().get("examples")
        print("\n--- Selected Examples ---")
        print(examples)
        print("-------------------------")
    else:
        print(f"Error: {res.text}")

def test_settings_persistence() -> None:
    print_header("5. Settings Persistence")
    profile = {
        "name": "demo_mode",
        "temperature": 0.9,
        "max_output_tokens": 512,
        "top_p": 0.9,
        "top_k": 40,
        "prompt_template": "Creative",
        "target_source": "General Knowledge"
    }
    print(f"Saving Profile: {profile['name']} (Temp: {profile['temperature']})")
    requests.post(f"{API_URL}/settings", json=profile)
    
    print("Verifying save...")
    res = requests.get(f"{API_URL}/settings/demo_mode")
    if res.status_code == 200:
        data = res.json()
        print(f"Loaded Profile: {data['name']} | Temp: {data['temperature']}")
        print("Persistence Confirmed.")
    else:
        print("Failed to verify settings.")

if __name__ == "__main__":
    print("Starting Medical AI Walkthrough...")
    test_status()
    test_direct_chat()
    test_rag_chat()
    test_dynamic_few_shot()
    test_settings_persistence()
    print("\nWalkthrough Complete! 🚀")
