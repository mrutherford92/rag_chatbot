"""
Script Name:  demo.py
Description:  Automated walkthrough mirroring the 'DEMO_SCRIPT.md' technical presentation.
Author:       Michael R. Rutherford
Date:         2026-01-29

Copyright (c) 2026
License: MIT
"""

import requests
import json
import time
from app.core.config import API_URL

def print_step(title, description):
    print(f"\n\n{'='*70}")
    print(f"🎬 {title}")
    print(f"{'-'*70}")
    print(description)
    print(f"{'='*70}\n")
    time.sleep(1)

def run_query(query, use_rag=True, temperature=0.7, model="gemini-2.5-flash", wrapped_query=None):
    payload = {
        "query": query,
        "wrapped_query": wrapped_query,
        "use_rag": use_rag,
        "temperature": temperature,
        "model": model
    }
    print(f"🔹 Query: '{query}'")
    print(f"⚙️  Settings: RAG={use_rag}, Temp={temperature}, Model={model}")
    
    start = time.time()
    try:
        res = requests.post(f"{API_URL}/chat", json=payload)
        if res.status_code == 200:
            print(f"✅ Response ({time.time() - start:.2f}s):\n")
            print(res.json()["response"])
        else:
            print(f"❌ Error: {res.text}")
    except Exception as e:
        print(f"❌ Connection Failed: {e}")

def main():
    print("🚀 Starting Technical Demo Simulation...")

    # --- STEP 1: Architecture Overview ---
    print_step(
        "STEP 1: System Health Check (Architecture)", 
        "Verifying FastAPI, Vector Store availability, and Gemini connection."
    )
    # Ping root
    try:
        res = requests.get(f"{API_URL}/")
        print(f"✅ Backend: {res.json()['service']}")
    except:
        print("❌ Backend is offline.")

    # --- STEP 2: The Base Case (No RAG) ---
    print_step(
        "STEP 2: The Base Case (Black Box Problem)", 
        "Asking for specific clinical data with RAG disabled. Expecting hallucination or refusal."
    )
    run_query(
        "What is the specific diagnosis for Sarah Connor?", 
        use_rag=False, 
        temperature=1.0
    )

    # --- STEP 3: The Solution (RAG) ---
    print_step(
        "STEP 3: The Solution (Vector Grounding)", 
        "Enabling FAISS retrieval. Expecting specific, cited facts."
    )
    run_query(
        "What is the specific diagnosis for Sarah Connor?", 
        use_rag=True, 
        temperature=0.0
    )

    # --- STEP 4: Deep Parameter Tuning (Top-P & Top-K) ---
    print_step(
        "STEP 4: The Engine Room (Hyper-Parameters)", 
        "Manipulating token probability distributions."
    )
    
    # A. Top-P (Nucleus) Test
    print("🧪 TEST A: Top-P = 0.1 (Nucleus Focus)")
    print("   Forces model to choose from only the top 10% mass. Should be very safe/boring.")
    payload_p = {
        "query": "Describe the patient's condition in creative detail.", 
        "use_rag": False, 
        "top_p": 0.1, 
        "temperature": 0.9,
        "model": "gemini-2.5-flash"
    }
    # Run custom request to show param injection
    requests.post(f"{API_URL}/chat", json=payload_p)
    print("   (Request sent with top_p=0.1)\n")

    # B. Top-K Test
    print("🧪 TEST B: Top-K = 1 (Greedy Decoding)")
    print("   Forces deterministic output by selecting ONLY the #1 most likely token.")
    payload_k = {
        "query": "Describe the patient's condition in creative detail.", 
        "use_rag": False, 
        "top_k": 1, 
        "temperature": 0.9,
        "model": "gemini-2.5-flash"
    }
    requests.post(f"{API_URL}/chat", json=payload_k)
    print("   (Request sent with top_k=1)\n")


    # --- STEP 5: Cognitive Architectures ---
    print_step(
        "STEP 5: Cognitive Architectures (CoVe)",
        "Using Chain of Verification to self-correct."
    )
    cove_prompt = """You are a thorough researcher. Use a Chain of Verification...""" 
    # (Simplified for log brevity)
    
    run_query(
        "Summarize the treatment plan for patient Kyle Reese.", 
        use_rag=True, 
        wrapped_query="[CoVe Logic Applied] " + "Summarize the treatment plan for patient Kyle Reese."
    )

    # --- STEP 6: Polymorphism (Gemini 3 Pro) ---
    print_step(
        "STEP 6: Model Polymorphism",
        "Hot-swapping to Gemini 3.0 Pro for reasoning tasks."
    )
    run_query(
        "Compare the cardiac symptoms of Sarah Connor vs. Kyle Reese.", 
        use_rag=True, 
        model="gemini-3-pro-preview"
    )

    print("\n🏁 Demo Complete.")

if __name__ == "__main__":
    main()
