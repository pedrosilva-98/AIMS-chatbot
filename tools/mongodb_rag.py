import streamlit as st
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langfuse import observe, get_client

@st.cache_resource
def load_embedding_model():
    api_key= st.secrets["GOOGLE_API_KEY"]
    return GoogleGenerativeAIEmbeddings(
        model="models/text-embedding-004",
        api_key= api_key)



def search_documents(query_text, collection, model):

    try:
        query_vector=model.embed_query(query_text)

        pipeline = [
            {
                "$vectorSearch": {
                    "queryVector": query_vector,
                    "path": "embedding", 
                    "numCandidates": 100,
                    "limit": 4,
                    "index": "vector_index"
                }
            },
            {"$project": {"_id": 0, "conteudo_limpo": 1, "score": {"$meta": "vectorSearchScore"}}}
        ]

        results= collection.aggregate(pipeline)
        return [doc['conteudo_limpo'] for doc in results]
    
    except Exception as e:
        print(f"Error during vector search: {e}")
        return []



@observe(as_type="generation")
def retrieve_context(user_query: str, embedding_model, collection):

    langfuse= get_client()
    langfuse.update_current_trace(tags=["MongoDB-Used", "RAG"])

    if collection is None or embedding_model is None:
        return "Error: MongoDB collection or embedding model not initialized."
    
    try:
        context_chunks= search_documents(user_query, collection, embedding_model)

        if not context_chunks:
            return "Não foram encontrados contextos relevantes."
        
        context= "\n\n".join(context_chunks)

        return context
    except Exception as e:
        return f"Error during vectorial search: {e}"