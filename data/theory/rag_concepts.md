# What is RAG?

**Retrieval-Augmented Generation (RAG)** allows an AI to answer questions using *your* private data, not just what it learned from the internet.

## The Special Cookie Recipe Analogy
Imagine you ask a professional chef (the LLM) for a cookie recipe. 
- **Without RAG**: The chef gives you a standard, generic chocolate chip recipe they learned in culinary school (Pre-training data).
- **The Problem**: You want your *Grandma's Special Cookie* recipe, which has a secret ingredient. The chef doesn't know this because it was never published online.
- **With RAG**: You hand the chef an index card with Grandma's recipe on it (Context). The chef reads it and says, "Ah, for this specific cookie, you need to add a pinch of nutmeg."

**In this app:**
- **Chef** = Gemini 2.5 Flash
- **Index Card** = Your PDF Medical Records
- **Result** = Accurate answers based on *your* specific patient cases.

## Enterprise Use Cases
This isn't just for cookies. Companies use RAG to query confidential data safely:
- **Project History**: A new hire asks, "What happened in Project X ten years ago?" The AI retrieves the answer from 20 years of archived PDFs.
- **Privacy**: Creating an on-premise RAG system (like `Llama` + `ChromaDB`) ensures confidential data never leaves the building.

## RAG vs. Custom GPTs
- **Custom GPTs**: Easy, no-code way to upload files and "simulate" RAG (like on OpenAI).
- **Custom Apps (This Project)**: Gives developers full control over the *Retrieval* logic (FAISS), *Generation* parameters (Temperature), and *UI/UX* (Streamlit).
