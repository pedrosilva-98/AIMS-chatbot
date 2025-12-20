import streamlit as st
import google.generativeai as genai
from pymongo import MongoClient

#GEMINI INITIALIZATION
@st.cache_resource
def init_gemini_client():
    """Inicializa e armazena o cliente Gemini."""
    
    api_key = st.secrets["GOOGLE_API_KEY"]
    if api_key:
        genai.configure(api_key=api_key)
        return genai
    return None


#MONGODB INITIALIZATION
@st.cache_resource
def init_connection_mongo():
    mongo_uri= st.secrets["MONGO_URI"]
    return MongoClient(mongo_uri)