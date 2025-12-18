import json
from pymongo import MongoClient
import os

MONGO_URI= os.getenv("MONGO_URI")
DB_NAME= "Projeto_curso"
COLLECTION_NAME= "data"

BASE_DIR= os.path.dirname(os.path.abspath(__file__))
CAMINHO_FICHEIRO= os.path.join(BASE_DIR, 'netpa_final_gemini.json')

try:
    with open(CAMINHO_FICHEIRO, 'r', encoding='utf-8') as f:
        data= json.load(f)
except FileNotFoundError:
    print("Error: File 'netpa_final_com_vetores.json' not found.")
    data= []

client= MongoClient(MONGO_URI)
db= client[DB_NAME]
collection= db[COLLECTION_NAME]

print(f"Ligação bem-sucedida ao MongoDB Atlas. A inserir {len(data)} documentos...")

if data:
    try:
        collection.insert_many(data)
        print("Data inserted successfully.")
    except Exception as e:
        print(f"Error inserting data: {e}")
else:
    print("No data to insert.")

client.close()