"""
Script Name:  rag.py
Description:  Core RAG service handling document ingestion, vector retrieval, and LLM generation.
Author:       Michael R. Rutherford
Date:         2026-01-28

Copyright (c) 2026
License: MIT
"""

import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from app.core.config import DATA_DIR, INDEX_DIR_PDFS, EMBEDDING_MODEL

class RAGService:
    def __init__(self, data_dir: str = DATA_DIR, index_dir: str = INDEX_DIR_PDFS):
        self.data_dir = data_dir
        self.index_dir = index_dir
        self.vector_store: FAISS | None = None
        
        # Initialize Embeddings
        self.embeddings = GoogleGenerativeAIEmbeddings(model=EMBEDDING_MODEL)
        
        # Initialize LLM
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash", 
            temperature=0.7,
            convert_system_message_to_human=True
        )

    def load_and_index(self) -> None:
        """
        Loads PDFs, processes them into chunks, and creates (or loads) a FAISS index.
        Persists the index to disk for valid startup.
        """
        # 1. Try to load existing index
        if os.path.exists(self.index_dir):
            print(f"Loading existing FAISS index from {self.index_dir}...")
            try:
                self.vector_store = FAISS.load_local(
                    self.index_dir, 
                    self.embeddings, 
                    allow_dangerous_deserialization=True
                )
                print("Index loaded successfully.")
                return
            except Exception as e:
                print(f"Error loading index: {e}. Rebuilding...")

        # 2. Rebuild index from source documents
        print("Loading documents from disk...")
        all_docs = []
        
        if not os.path.exists(self.data_dir):
            print(f"Warning: Data directory {self.data_dir} not found.")
            return

        for filename in os.listdir(self.data_dir):
            if filename.endswith(".pdf"):
                path = os.path.join(self.data_dir, filename)
                try:
                    loader = PyPDFLoader(path)
                    docs = loader.load()
                    all_docs.extend(docs)
                    print(f"Loaded {filename}, {len(docs)} pages.")
                except Exception as e:
                    print(f"Failed to load {filename}: {e}")

        if not all_docs:
            print("No documents found to index.")
            return

        # 3. Chunk Documents
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        splits = text_splitter.split_documents(all_docs)
        print(f"Created {len(splits)} document chunks.")

        # 4. Create and Save Vector Store
        print("Creating Vector Store...")
        self.vector_store = FAISS.from_documents(splits, self.embeddings)
        print(f"Saving Vector Store to {self.index_dir}...")
        self.vector_store.save_local(self.index_dir)
        print("Vector Store created and saved.")

    def query(self, 
              input_text: str, 
              wrapped_query: str | None = None, 
              use_rag: bool = True, 
              temperature: float = 0.7, 
              max_output_tokens: int = 1024, 
              top_p: float = 0.95, 
              top_k: int = 40,
              model_name: str = "gemini-2.5-flash") -> str:
        """
        Executes a query against the LLM, optionally using RAG.
        """
        
        # 1. Initialize LLM Dynamically (to support model switching)
        llm = ChatGoogleGenerativeAI(
            model=model_name,
            temperature=temperature,
            max_output_tokens=max_output_tokens,
            top_p=top_p,
            top_k=top_k,
            convert_system_message_to_human=True
        )
        
        # 2. Define Prompts
        rag_system_prompt = (
            "You are a helpful assistant for medical question answering. "
            "Use the following pieces of retrieved context to answer the question. "
            "If you don't know the answer, say that you don't know. "
            "Provide a comprehensive and detailed answer."
            "\n\n"
            "{context}"
        )
        
        rag_prompt = ChatPromptTemplate.from_messages([
            ("system", rag_system_prompt),
            ("human", "{input}"),
        ])
        
        basic_prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful assistant. Answer the user's question to the best of your ability."),
            ("human", "{input}"),
        ])
        
        generation_input = wrapped_query if wrapped_query else input_text

        # 3. Execute Chain
        if use_rag:
            if not self.vector_store:
                return "Error: Vector Index is not built. Please click 'Rebuild Index' in settings."
            
            # A. Retrieve using RAW QUERY (input_text)
            retriever = self.vector_store.as_retriever()
            docs = retriever.invoke(input_text)
            
            # Format retrieved docs
            context_str = "\n\n".join(doc.page_content for doc in docs)

            # B. Generate using WRAPPED PROMPT (generation_input)
            chain = rag_prompt | llm | StrOutputParser()
            return chain.invoke({"context": context_str, "input": generation_input})
            
        else:
            # Basic Chain (No Retrieval)
            chain = basic_prompt | llm | StrOutputParser()
            return chain.invoke({"input": generation_input})

# Global Instance
rag_service = RAGService()
