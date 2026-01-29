"""
Script Name:  main.py
Description:  FastAPI entry point for the Medical RAG Chatbot backend.
Author:       Michael R. Rutherford
Date:         2026-01-28

Copyright (c) 2026
License: MIT
"""

from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager

# Internal Modules
from app.core.rag import rag_service
from app.core.expert_knowledge import expert_service
from app.backend.models import (
    ChatRequest, ChatResponse, ExampleLookupRequest, SettingsProfile
)
from app.backend import database as db

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for FastAPI.
    Handles startup and shutdown events.
    """
    # Startup
    print("Initializing Database...")
    db.init_db()
    
    print("Initializing RAG Service...")
    rag_service.load_and_index()
    
    print("Initializing Expert Knowledge Service...")
    expert_service.load_and_index()
    
    yield
    # Shutdown logic (if any) goes here

app = FastAPI(lifespan=lifespan)

# --- SYSTEM ENDPOINTS ---

@app.get("/")
async def root():
    """Health check endpoint."""
    return {"status": "ok", "service": "RAG Chatbot with Gemini 2.5 Flash"}

@app.post("/rebuild")
async def rebuild_index():
    """Force rebuilds the vector index from disk."""
    try:
        rag_service.load_and_index()
        return {"status": "success", "message": "Index rebuilt successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- FEATURES ENDPOINTS ---

@app.post("/features/select_examples")
async def select_examples(request: ExampleLookupRequest):
    """
    Dynamic Few-Shot Learning: Selects relevant Q&A examples 
    based on semantic similarity to the query.
    """
    examples = expert_service.search(request.query, k=request.k)
    return {"examples": examples}

# --- SETTINGS ENDPOINTS ---

@app.get("/settings", response_model=list[str])
async def get_profiles():
    """List all available settings profiles."""
    return db.get_all_profile_names()

@app.get("/settings/{name}", response_model=SettingsProfile)
async def get_profile(name: str):
    """Retrieve a specific settings profile by name."""
    profile = db.get_profile_by_name(name)
    if profile:
        return profile
    raise HTTPException(status_code=404, detail="Profile not found")

@app.post("/settings")
async def save_profile(profile: SettingsProfile):
    """Create or update a settings profile."""
    try:
        db.save_profile(profile)
        return {"status": "saved", "name": profile.name}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/settings/{name}")
async def delete_profile(name: str):
    """Delete a settings profile."""
    db.delete_profile(name)
    return {"status": "deleted", "name": name}

# --- CHAT & RAG ENDPOINTS ---

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Primary Chat Interface.
    Orchestrates the RAG retrieval and generation process.
    """
    # Delegate logic to the RAG Service
    answer = rag_service.query(
        request.query, 
        wrapped_query=request.wrapped_query,
        use_rag=request.use_rag,
        temperature=request.temperature,
        max_output_tokens=request.max_output_tokens,
        top_p=request.top_p,
        top_k=request.top_k
    )
    return ChatResponse(response=answer)
