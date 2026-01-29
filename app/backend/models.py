"""
Script Name:  models.py
Description:  Pydantic models for API request/response validation.
Author:       Michael R. Rutherford
Date:         2026-01-28

Copyright (c) 2026
License: MIT
"""

from pydantic import BaseModel

class ChatRequest(BaseModel):
    query: str
    wrapped_query: str | None = None  # Optional wrapper/template
    use_rag: bool = True
    temperature: float = 0.7
    max_output_tokens: int = 1024
    top_p: float = 0.95
    top_k: int = 40

class ChatResponse(BaseModel):
    response: str

class ExampleLookupRequest(BaseModel):
    query: str
    k: int = 3

class SettingsProfile(BaseModel):
    name: str
    temperature: float
    max_output_tokens: int
    top_p: float
    top_k: int
    prompt_template: str
    target_source: str | None = None
