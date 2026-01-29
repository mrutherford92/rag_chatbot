# 🧭 User Interface Guide

Welcome to the Medical RAG Chatbot. Here is what everything on the screen does.

## 1. The Sidebar (Left Panel)

### 📚 Documentation
Click these dropdowns to learn about the concepts behind the AI:
*   **Hallucination Theory**: Why AI lies and how we stop it.
*   **Model Parameters**: How to control the AI's creativity.
*   **RAG Concepts**: How the "Retrieval" part works.
*   **Prompt Strategies**: The science of asking good questions.

### ⚙️ Actions
*   **Clear Chat**: Wipes the screen. Good for starting a fresh topic.
*   **Rebuild Index**: If you add new PDF files to the `data/pdfs` folder, click this to teach the AI about them.

### 💾 Configuration (Profiles)
*   **Select Profile**: Load saved settings (e.g., "Creative Mode" or "Strict Doctor").
*   **Save/Delete**: Manage your custom presets.

### 🧠 Prompt Engineering
This is where you control *how* the AI thinks.
*   **Prompt Template**: Choose a strategy (e.g., "Medical Expert" or "Step-Back Prompting").
*   **Search Medical Database (Toggle)**: 
    *   **ON (Red)**: The AI reads your medical PDFs before answering. It helps prevent lies.
    *   **OFF (Gray)**: The AI relies only on its general training (Google's data). Good for testing general knowledge.

### 🎛️ Model Parameters
Fine-tune the engine. See the **Model Parameters** documentation for deep dives into Heat, Top-P, and Top-K.

## 2. The Main Chat (Center)
*   **Chat Input**: Type your question here.
*   **Assistant Response**:
    *   **Status Spinner**: Shows what the AI is thinking ("Connecting to knowledge base...", "Applying template...").
    *   **Final Answer**: The text response.
