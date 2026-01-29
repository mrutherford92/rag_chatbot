"""
Script Name:  app.py
Description:  Streamlit Frontend for the Medical RAG Chatbot.
Author:       Michael R. Rutherford
Date:         2026-01-28

Copyright (c) 2026
License: MIT
"""

import streamlit as st
import requests
import json
from typing import Any

# Backend URL
# Backend URL
from app.core.config import (
    API_URL, 
    DOC_HALLUCINATION, 
    DOC_MODEL_PARAMETERS, 
    DOC_SAMPLE_QUESTIONS,
    DOC_PROMPTING,
    DOC_RAG_CONCEPTS,
    DOC_UI_GUIDE
)

st.set_page_config(page_title="Medical AI Assistant", page_icon="app/frontend/assets/favicon.png", layout="wide")

# --- CSS STYLING ---
st.markdown("""
<style>
    /* Robust fix for Streamlit dropdown hover */
    div[data-baseweb="popover"] li:hover {
        background-color: rgba(30, 200, 200, 0.3) !important;
        color: white !important;
    }
    div[data-baseweb="select"] > div:hover {
         border-color: rgba(30, 200, 200, 0.5) !important;
    }
    div[data-baseweb="popover"] li {
        color: white;
    }
</style>
""", unsafe_allow_html=True)


# --- HEADER ---
col_h1, col_h2 = st.columns([3, 1])
with col_h1:
    st.title(":material/smart_toy: Medical AI Assistant")
with col_h2:
    selected_model = st.selectbox(
        "Model", 
        ["gemini-2.5-flash", "gemini-3-pro-preview"],
        index=0,
        label_visibility="collapsed"
    )

# --- PROMPT TEMPLATES ---
PROMPT_TEMPLATES: dict[str, str] = {
    "According-to (Standard)": """You are a precise medical research assistant.
Instruction: Answer the question strictly according to the provided medical documents.
Grounding:
1. Base your response ONLY on the factual data in the context.
2. Cite specific sections or values (e.g., "BP: 120/80") to support your answer.
3. If the documents do not contain the answer, state that the information is not available in the provided context.

Question: {input_text}""",

    "Chain of Verification (CoVe)": """You are a thorough researcher. Use a Chain of Verification to ensure accuracy.
Step 1: Draft an initial response strictly according to the provided documents.
Step 2: Create validational questions to check if the response is supported by the context.
Step 3: Answer the validation questions using the context.
Step 4: Revise the response to ensure complete accuracy.

Question: {input_text}""",

    "Step-Back Prompting": """You are an expert assistant. Use Step-Back Prompting to answer.
Step 1: Abstract the key concepts and principles relevant to this question.
Step 2: Use the abstractions to reason through the question.
Let's think step by step to answer this.

Question: {input_text}""",

    "Source Grounding (Pre-training)": """You are a helpful assistant.
Instruction: Ground your response in factual data from your pre-training set, specifically referencing **{source}**.
Rules:
1. Provide a COMPREHENSIVE and DETAILED answer.
2. Ensure all claims can be attributed to {source}.
3. Structure your response with clear headings and bullet points.

Question: {input_text}""",

    "Medical Expert (Example-Based)": """You are a highly experienced medical expert.
Instruction: Answer the question by mimicking the tone and format of the following expert examples.

{examples}

Question: {input_text}"""
}

# --- HELPER FUNCTIONS ---

def get_dynamic_examples(query_text: str) -> str:
    """Fetches relevant few-shot examples from the backend."""
    try:
        if not query_text:
            query_text = "medical" 
            
        payload = {"query": query_text, "k": 3}
        res = requests.post(f"{API_URL}/features/select_examples", json=payload)
        
        if res.status_code == 200:
            return res.json().get("examples", "")
        else:
            return f"Error fetching examples: {res.status_code}"
    except Exception as e:
        return f"Error connecting to backend: {str(e)}"

@st.dialog("Documentation")
def show_docs(file_path: str):
    """Displays a markdown file in a modal dialog."""
    try:
        with open(file_path, "r") as f:
            content = f.read()
        st.markdown(content)
    except FileNotFoundError:
        st.error(f"Documentation file not found: {file_path}")
    except Exception as e:
        st.error(f"Error loading docs: {e}")


# --- SIDEBAR ---

with st.sidebar:
    st.header("Documentation")
    
    with st.expander("Hallucination Theory", icon=":material/psychology:"):
        try:
            with open(DOC_HALLUCINATION, "r") as f:
                st.markdown(f.read())
        except Exception:
             st.error("Doc not found")



    with st.expander("RAG Concepts", icon=":material/school:"):
        try:
            with open(DOC_RAG_CONCEPTS, "r") as f:
                st.markdown(f.read())
        except Exception:
             st.error("Doc not found")

    with st.expander("Prompt Strategies", icon=":material/lightbulb:"):
        try:
            with open(DOC_PROMPTING, "r") as f:
                st.markdown(f.read())
        except Exception:
             st.error("Doc not found")

    with st.expander("Model Parameters", icon=":material/tune:"):
        try:
            with open(DOC_MODEL_PARAMETERS, "r") as f:
                st.markdown(f.read())
        except Exception:
             st.error("Doc not found")

    with st.expander("UI Guide", icon=":material/map:"):
        try:
            with open(DOC_UI_GUIDE, "r") as f:
                st.markdown(f.read())
        except Exception:
             st.error("Doc not found")

    with st.expander("Sample Questions", icon=":material/quiz:"):
        try:
            with open(DOC_SAMPLE_QUESTIONS, "r") as f:
                st.markdown(f.read())
        except Exception:
             st.error("Doc not found")
        
    st.markdown("---")
    
    # 1. ACTIONS
    st.header("Actions")
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        if st.button("Clear Chat", icon=":material/delete:", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
    with col_s2:
        if st.button("Rebuild Index", icon=":material/refresh:", use_container_width=True):
            with st.spinner("Rebuilding..."):
                try:
                    requests.post(f"{API_URL}/rebuild")
                    st.success("Done!")
                except:
                    st.error("Failed")
                    
    st.markdown("---")

    # 2. CONFIGURATION
    st.header("Configuration")

    # Profiles Manager
    with st.expander("Profiles", icon=":material/save:"):
        try:
            profiles_res = requests.get(f"{API_URL}/settings")
            profiles = profiles_res.json() if profiles_res.status_code == 200 else []
        except:
            profiles = []

        if profiles:
            selected_profile = st.selectbox("Select Profile", profiles, key="profile_selector")
            col_p1, col_p2 = st.columns(2)
            with col_p1:
                if st.button("Load", use_container_width=True):
                    try:
                        res = requests.get(f"{API_URL}/settings/{selected_profile}")
                        if res.status_code == 200:
                            data = res.json()
                            st.session_state.prompt_template_selector = data["prompt_template"]
                            st.session_state.target_source_selector = data["target_source"] if data["target_source"] else ""
                            st.session_state.temp_slider = data["temperature"]
                            st.session_state.tokens_slider = data["max_output_tokens"]
                            st.session_state.top_p_slider = data["top_p"]
                            st.session_state.top_k_slider = data["top_k"]
                            st.success(f"Loaded '{selected_profile}'")
                            st.rerun()
                    except Exception as e:
                        st.error(f"Error: {e}")
            with col_p2:
                with st.popover("Delete", icon=":material/delete:", use_container_width=True):
                    st.write(f"Delete **{selected_profile}**?")
                    if st.button("Confirm", type="primary", use_container_width=True):
                        requests.delete(f"{API_URL}/settings/{selected_profile}")
                        st.rerun()
        
        # Save Profile
        new_profile_name = st.text_input("New Profile Name", placeholder="e.g. Creative Writing")
        if st.button("Save Current Settings", use_container_width=True):
            if new_profile_name:
                payload = {
                    "name": new_profile_name,
                    "temperature": st.session_state.temp_slider,
                    "max_output_tokens": st.session_state.tokens_slider,
                    "top_p": st.session_state.top_p_slider,
                    "top_k": st.session_state.top_k_slider,
                    "prompt_template": st.session_state.prompt_template_selector,
                    "target_source": st.session_state.get("target_source_selector", None)
                }
                requests.post(f"{API_URL}/settings", json=payload)
                st.success("Saved!")
                st.rerun()

    # Prompt Engineering
    st.subheader("Prompt Engineering")
    template_style = st.selectbox(
        "Prompt Template",
        list(PROMPT_TEMPLATES.keys()),
        key="prompt_template_selector",
        help="**Strategy Selector**\n\nChoose 'how' the AI should think:\n* **Standard**: Just answers.\n* **Chain of Verification**: Double-checks its own specific facts.\n* **Medical Expert**: Mimics a doctor's tone using examples."
    )
    
    target_source = ""
    if template_style == "Source Grounding (Pre-training)":
        target_source = st.selectbox(
            "Target Source", 
            ["CDC", "WHO", "Mayo Clinic"],
            key="target_source_selector",
            help="**Authority Limiter**\n\nForces the AI to only cite information that could be attributed to this organization."
        )
        st.info("Database Search is disabled.", icon=":material/search_off:")
    
    use_rag = st.toggle(
        "Search Medical Database", 
        value=True, 
        key="rag_toggle",
        help="**Truth Toggle**\n\n* **ON**: Reads your local PDFs to find the answer. Minimizes hallucinations.\n* **OFF**: Uses only the AI's general training (like standard ChatGPT)."
    )

    # Active Prompt Viewer
    if st.toggle("View Active System Prompt", value=False):
        st.info(f"Strategy: **{template_style}**")
        raw_template = PROMPT_TEMPLATES[template_style]
        preview_text = raw_template
        
        if "{source}" in raw_template:
             preview_text = preview_text.format(source=target_source if target_source else "[SOURCE]", input_text="[YOUR QUESTION]")
        
        if "{examples}" in raw_template:
             examples_content = get_dynamic_examples("medical help")
             short_preview = "\n".join(examples_content.split("\n")[:4]) + "\n... (more dynamic examples) ..."
             preview_text = preview_text.replace("{examples}", short_preview).replace("{input_text}", "[YOUR QUESTION]")
        
        if "{input_text}" in preview_text:
             preview_text = preview_text.replace("{input_text}", "[YOUR QUESTION]")

        st.code(preview_text, language="text")

    # Model Parameters
    st.subheader("Model Parameters")
    temperature = st.slider(
        "Heat (Temperature)", 
        0.0, 2.0, 0.7, 0.1, 
        key="temp_slider",
        help="**Creativity Control** (0.0 - 2.0)\n\n* **Low (0.2)**: Serious, factual, boring. Good for medicine.\n* **High (1.2)**: Creative, random, hallucinations likely."
    )
    max_output_tokens = st.number_input(
        "Max Output Tokens", 
        1, 8192, 2048, 128, 
        key="tokens_slider",
        help="**Length Limit**\n\nMaximum number of words the AI can generate.\n* 2048 ~= 1,500 words."
    )
    top_p = st.slider(
        "Top-P (Nucleus)", 
        0.0, 1.0, 0.95, 0.05, 
        key="top_p_slider",
        help="**Vocabulary Breadth** (0.0 - 1.0)\n\n* **Low (0.1)**: Only uses the most obvious words.\n* **High (0.9)**: Uses a wider vocabulary."
    )
    top_k = st.slider(
        "Top-K", 
        1, 100, 40, 1, 
        key="top_k_slider",
        help="**Choice Hard-Limit** (1 - 100)\n\nLimits the AI to choosing from only the top K most likely next words.\n* Lower = More predictable."
    )
    
    st.markdown("---")
    
    try:
        status_res = requests.get(f"{API_URL}/")
        if status_res.status_code == 200:
            st.success("Backend: Online")
        else:
            st.error(f"Backend Status: {status_res.status_code}")
    except requests.exceptions.ConnectionError:
        st.error("Backend: Offline")

# --- CHAT INTERFACE ---

if "messages" not in st.session_state:
    st.session_state.messages = []

st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True) 

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Type your medical question..."):
    
    # 1. Apply Template Logic
    raw_template = PROMPT_TEMPLATES[template_style]
    
    if "{source}" in raw_template:
        source_text = target_source if target_source else "MEDICAL SCIENCE"
        final_prompt = raw_template.format(source=source_text, input_text=prompt)
    elif "{examples}" in raw_template:
        examples_content = get_dynamic_examples(prompt)
        final_prompt = raw_template.format(examples=examples_content, input_text=prompt)
    else:
        final_prompt = raw_template.format(input_text=prompt)
    
    # 2. Add to History
    st.session_state.messages.append({"role": "user", "content": prompt}) 
    with st.chat_message("user"):
        st.markdown(prompt)

    # 3. Generate Response
    with st.chat_message("assistant"):
        with st.status("Processing request...", expanded=True) as status:
            st.write(f"Applying template: {template_style}...")
            st.write("Connecting to knowledge base...")
            
            payload = {
                "query": final_prompt, # WRAPPED QUERY
                "wrapped_query": final_prompt, # NEW FIELD in models.py (sending same for now as main.py handles it)
                "use_rag": use_rag,
                "temperature": temperature,
                "max_output_tokens": int(max_output_tokens),
                "top_p": top_p,
                "top_p": top_p,
                "top_k": top_k,
                "model": selected_model
            }
            
            # NOTE: Backend expects 'query' as raw and 'wrapped_query' as templated.
            # Fix: Send RAW prompt as 'query' and TEMPLATED prompt as 'wrapped_query'
            payload["query"] = prompt 
            
            answer = None
            try:
                response = requests.post(f"{API_URL}/chat", json=payload)
                if response.status_code == 200:
                    answer = response.json()["response"]
                    status.update(label="Complete", state="complete", expanded=False)
                else:
                    status.update(label="Error", state="error", expanded=True)
                    st.error(f"Backend Error: {response.text}")
            except Exception as e:
                status.update(label="Connection Failed", state="error", expanded=True)
                st.error(f"Connection Error: {e}")
        
        if answer:
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
