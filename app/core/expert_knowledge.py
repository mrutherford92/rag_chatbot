"""
Script Name:  expert_knowledge.py
Description:  Service for indexing/retrieving expert medical examples via semantic search.
              See: https://reference.langchain.com/v0.3/python/core/example_selectors.html
Author:       Michael R. Rutherford
Date:         2026-01-28

Copyright (c) 2026
License: MIT
"""

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_core.example_selectors import BaseExampleSelector
import json
import os

from app.core.config import INDEX_DIR_EXAMPLES, EMBEDDING_MODEL, FEW_SHOT_DATA

class ExpertKnowledgeService(BaseExampleSelector):
    def __init__(self, index_dir: str = INDEX_DIR_EXAMPLES):
        self.vector_store: FAISS | None = None
        self.index_dir = index_dir
        # Reuse the same embedding model as RAG
        self.embeddings = GoogleGenerativeAIEmbeddings(model=EMBEDDING_MODEL)
        self.data_path = FEW_SHOT_DATA

    def add_example(self, example: dict[str, str]) -> None:
        """Required by BaseExampleSelector, but we load from disk efficiently."""
        pass

    def load_and_index(self) -> None:
        """
        Loads JSONL examples and builds a FAISS index, utilizing disk persistence.
        If an index exists, it loads it; otherwise, it builds a new one.
        """
        # 1. Try to load existing index
        if os.path.exists(self.index_dir):
            print(f"Loading existing Expert Knowledge index from {self.index_dir}...")
            try:
                self.vector_store = FAISS.load_local(
                    self.index_dir, 
                    self.embeddings, 
                    allow_dangerous_deserialization=True
                )
                print("Expert Index loaded successfully.")
                return
            except Exception as e:
                print(f"Error loading Expert index: {e}. Rebuilding...")

        # 2. Rebuild index from Source
        if not os.path.exists(self.data_path):
            print(f"Warning: Example data not found at {self.data_path}")
            return

        documents = []
        try:
            with open(self.data_path, "r") as f:
                for line in f:
                    item = json.loads(line)
                    messages = item.get("messages", [])
                    user_msg = next((m["content"] for m in messages if m["role"] == "user"), "")
                    assistant_msg = next((m["content"] for m in messages if m["role"] == "assistant"), "")
                    
                    if user_msg and assistant_msg:
                        # Improve semantic search by embedding only the Question
                        # but storing the full Q/A pair in metadata for retrieval.
                        full_text = f"Q: {user_msg}\nA: {assistant_msg}"
                        doc = Document(page_content=user_msg, metadata={"full_example": full_text})
                        documents.append(doc)
            
            if documents:
                print(f"Indexing {len(documents)} expert examples...")
                self.vector_store = FAISS.from_documents(documents, self.embeddings)
                print(f"Saving Expert Store to {self.index_dir}...")
                self.vector_store.save_local(self.index_dir)
                print("Expert Store created and saved.")
                
        except Exception as e:
            print(f"Error indexing examples: {e}")

    def select_examples(self, input_variables: dict[str, str] | str) -> list[dict]:
        """
        Selects examples based on input variables. 
        Note: The BaseExampleSelector signature expects a dict, but we often pass a string query text.
        We return a list of examples (dicts) to match the interface, 
        but our consumer (app.py) currently expects a string block.
        
        To maintain backward compatibility with our own app:
        We will keep the `select_examples` as the main logic but add a standardized method if needed.
        """
        # Standardize query extraction
        query = input_variables
        if isinstance(input_variables, dict):
             query = input_variables.get("query", "")

        return self.search(query)

    def search(self, query: str, k: int = 3) -> str:
        """
        Public custom method to return the formatted string block directly.
        Returns a string of formatted Q/A pairs.
        """
        if not self.vector_store:
            return "No examples indexed."
        
        try:
            docs = self.vector_store.similarity_search(query, k=k)
            return "\n\n".join([d.metadata["full_example"] for d in docs])
        except Exception as e:
            return f"Error selecting examples: {e}"

# Singleton instance
expert_service = ExpertKnowledgeService()
