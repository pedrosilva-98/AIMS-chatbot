import streamlit as st
from langfuse import observe, get_client
import google.generativeai as genai

langfuse_secret_key = st.secrets['langfuse_secret_key']
langfuse_public_key = st.secrets['langfuse_public_key']
langfuse_host = st.secrets['langfuse_host']




@observe()
def generate_response_with_tools_and_langfuse(user_input, model_name, system_instr, user_name, api_key, chat_history, my_tools):
    langfuse= get_client()
    langfuse.update_current_trace(
        user_id=user_name,
        input=user_input,
        metadata={
            "mode": "automatic_function_calling",
            "environment": "streamlit_app"
        },
        tags=["Pure-Gemini"]
    )
    if api_key:
            genai.configure(api_key=api_key)
    

    
    model = genai.GenerativeModel(
        model_name=model_name,
        tools=my_tools,
        system_instruction=system_instr  
    )
    chat= model.start_chat(history=chat_history, enable_automatic_function_calling=True)
    response = chat.send_message(user_input)
    used_tools=[]
    
    for message in chat.history:
        for part in message.parts:
            if part.function_call:
                used_tools.append(part.function_call.name)
    
    if "get_horario_atualizado_tool" in used_tools:
        langfuse.update_current_trace(
            name="NetPA Horarios Query",
            tags=["Tool-Used", "Web-Scraping", "NetPA"]
        )
    elif "retrieve_context_tool" in used_tools: 
        langfuse.update_current_trace(
            name="MongoDB RAG Query",
            tags=["Tool-Used", "RAG", "MongoDB"]
        )
    elif len(used_tools) > 0:
        langfuse.update_current_trace(
            name="Multi-Tool Query",
            tags=["Tool-Used", "Complex-Query"]
        )
    else:
        langfuse.update_current_trace(
            name="Gemini Chat",
            tags=["Pure-LLM"]
        )
    final_text = response.text

    return final_text
