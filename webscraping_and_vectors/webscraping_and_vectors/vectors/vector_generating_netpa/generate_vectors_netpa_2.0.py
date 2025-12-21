import os
import json
import time
from pathlib import Path
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
import streamlit as st

caminho_script = Path(__file__).resolve().parent.parent

api_key = st.secrets["GOOGLE_API_KEY"]
if not api_key:
    print("GOOGLE_API_KEY não encontrada no ficheiro .env")
    exit()

def gerar_vetores_gemini():

    pasta_raiz = caminho_script.parent
    input_file = pasta_raiz / "webscraping" / "cleaning" /"netpa_btns" / "netpa_dump_2.0_limpo.json"
    output_file = pasta_raiz / "vectors" / "vector_generating_netpa" / "netpa_vectors_netpa_2.0.json"

    if not os.path.exists(input_file):
        print(f"Ficheiro não encontrado: {input_file}")
        return

    # Read JSON 
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Erro ao ler JSON: {e}")
        return

    # Prepare documents and splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", " ", ""]
    )

    docs = []
    for item in data:
        doc = Document(
            page_content=item.get("conteudo", ""),
            metadata={
                "nome": item.get("nome", ""),
                "xpath": item.get("xpath", "")
            }
        )
        docs.append(doc)

    splitted_docs = text_splitter.split_documents(docs)
    
    # Model of embeddings
    embeddings_model = GoogleGenerativeAIEmbeddings(
        model="models/text-embedding-004",
        google_api_key=api_key
    )
    
    # Embeddings generation with batching
    vetores_totais = []
    textos = [doc.page_content for doc in splitted_docs]

    tamanho_lote = 50
    total_chunks = len(textos)

    for i in range(0, total_chunks, tamanho_lote):
        fim = min(i + tamanho_lote, total_chunks)
        lote_atual = textos[i:fim]
        
        try:
            vetores_lote = embeddings_model.embed_documents(lote_atual)
            vetores_totais.extend(vetores_lote)
            
            time.sleep(1) 
            
        except Exception as e:
            print(f"Erro no lote {i}: {e}")
            return

    # Final Json with embeddings
    dados_finais = []
    
    for i, doc in enumerate(splitted_docs):
        item_novo = doc.metadata.copy()
        item_novo["conteudo"] = doc.page_content
        
        if i < len(vetores_totais):
            item_novo["embedding"] = vetores_totais[i]
        
        dados_finais.append(item_novo)

    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(dados_finais, f, ensure_ascii=False, indent=4)

    print(f"Ficheiro salvo: {output_file}")

if __name__ == "__main__":
    gerar_vetores_gemini()