import streamlit as st

def get_gemini_history():
    """Converte o histórico do Streamlit para o formato do Gemini"""
    gemini_history = []
    if "messages" in st.session_state:
        for msg in st.session_state["messages"]:
            role = "model" if msg["role"] == "assistant" else "user"
            gemini_history.append({
                "role": role,
                "parts": [msg["content"]]
            })
    return gemini_history