# [AIMS- Chatbot]

AIMS: Your Intelligent Campus Companion at NOVA IMS 

## Overview

AIMS is a comprehensive AI-powered virtual assistant designed to streamline the academic experience for Nova IMS students. Powered by Google Gemini and MongoDB Atlas, it utilizes RAG to answer administrative and academic queries with precison. It features a secure , real-time integration with NetPA to retrieve personalized timetables and offers dynamic integration modes, ensuring students have instant access to the information they need, when they need.

## Features
- Web Scraping: we scraped the NetPA to extract relevant information from each link of the website. And stored it in MongoDB Atlas.
- Language: Switch between Portuguese and English language;
- Multi-Personality: Switch between Academic Advisor, Career Coach, Administrative Assistant, and Buddy Modes;
- Security: it only can be used by people who have their data in the database and have their student number and password in the security database;
- Real-Time Data: Fetches live timetables directly from NetPA using secure web scrapping;
- RAG Architecture: Uses MongoDB Atlas Vector Search to answer questions based on official university documents;
- Observability: Full trace monitoring with Langfuse.

## Tech Stack

**Backend:**
- Python
- Google Gemini API: Utilizes the gemini-2.5-flash-lite model for generating responses and processing natural language;
- Selenium: Used in headless mode (Chromium) for real-time web scrapping of the NetPA student portal.

**Frontend:**
- Streamlit: Used to build the interactive web interface.

**Database:**
- MongoDB Atlas: Serves as a database, functioning as a Vector Store for RAG and storing static university data. This data was obtained by web scraping the NetPA accounts of two people. Since this is an MVP, we consider two people sufficient to show how it works.

**AI/ML:**
- Langfuse: Observability, tracing and monitoring LLM interactions;
- LangChain: Framework to orchestrating the RAG pipeline and managing document retrieval;
- Function Calling (Tools): Custom implementation allowing the LLM to autonomously choose between searching the vector database (MongoDB) or scraping real-time data (NetPA);
- Sentence Transformers: Used for generating vector embeddings for document ingestion.

## Architecture

### AIMS - Architecture

    User[Student] --> (interects) UI[Streamlit Frontend]
    UI --> (sende query) Logic[Python Backend]
    Logic --> (invokes) LLM[Google Gemini API]
    LLM --> (decision tool) Router{Tool Router}

    Router --> (data base) RAG[MongoDB Atlas (Vector Store)]
    Router --> (real time data) Scraper[Selenium/Chromium (Netpa)]

    RAG --> (context)LLM
    Trace --> Langfuse

    LLM --> (final response) UI

### Layer Structure

## UI Layer: 
- Streamlit: handles user input, chat session state management and manages authentication via student number/ password verification.

## Service Layer: 
Initializates connections, manages the chat history and coordinates the flow between UI and AI.

## AI Layer: 
- Google Gemini: manages system prompts, handles context window limits and integrates Langfuse for tracing and monitoring model performance. (gemini_init_function.py, langfuse_function.py)

## Tools Layer: 
- Vector Store: MongoDB Atlas stores embedding of Nova IMS documents for RAG operations (mongodb_rag.py)
- Web Scraper: Selenium based tool that performs real-time authentication on the NetPA portal to retrieve live schedule data. (scrapping_tool.py)

### Key Design Decisions and Justifications

- RAG and Scraping: we implemented two approaches to address different data needs. RAG is used for static, unstructure data, while Scraping is used for private, real-time data.

- MongoDB as Vector Store: we chose it because it handles standard NoSQL data and vector embeddings, avoiding a separate database just for vectors.

- Sreamlit: we chose it for its simple development capabilities and native Python integration.

- Selenium: utilizes Chromium drivers to ensure the application functions correctly on Streamlit Cloud (Linux)

- Langfuse: we integrate from the start to understand which tool was used in each interaction, monitoring AI applications.

## Installation & Setup

### Prerequisites
- Python 3.10 or higher
- Google Chrome or Microsoft Edge installed
- API keys for required services:
    - present in Required enviroment variables

### Installation Steps

1. Clone the repository:
```bash
git clone https://github.com/pedrosilva-98/AIMS-chatbot.git
cd AIMS-Chatbot
```

2. Install dependencies:
This project uses 'requirements.txt' file to manage all library dependencies
```bash
uv sync
uv pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Past the Requirement variables 
```
This is to run the locally the code
**Required environment variables:**
```
langfuse_secret_key = "sk-lf-57db3c7c-b936-4b93-8a29-65458665be94"
langfuse_public_key = "pk-lf-3e54915a-9181-4623-b71b-b560a740604d"
langfuse_host = "https://cloud.langfuse.com"

GOOGLE_API_KEY= "AIzaSyDaUlrumleZCduEYmFfzhYzEM3T7qzX0tM"

MONGO_URI= "mongodb+srv://chatbot_user:PapiPauligol@cluster0.zf2kzct.mongodb.net/?appName=Cluster0"
user1='20231675'
user2='20231681'
pass1='5678'
pass2='1234'
#This password is not real, so the web scraping tool will not function locally. You can test this feature using the 'Live Application'. This is the best way we found to maintain security while enabling professors to test all of our tools.
```

4. Run the application:
```bash
uv run streamlit run PROJECT4.0.py
```

## Usage

Authentication: 
- Name: your name 
- Student Number: Enter a valid student number from the database (You have to enter the number 20231681 or 20231675 since they are the only ones that are in the database)
- Password: Enter the corresponding password (The password must be the ones in the 'Required enviroments variables', pass1 is for user1 and pass2 is for user2)

Sidebar:
- Language: switch language
- Personality: switch chatbot personality
- External links: Give access to NetPA and NOVA IMS webmail

AI:
- Type the query
- Submit the query

<img src="assets/AIresponse.jpeg" alt="Interface de Login" width="700">

This image demonstrates that the question was regarding the schedule and that he provided a response, as classes were still being held during the week the question was raised. 
## Exemples of queries:
- What is my current average?
- How many ECTS credits have I completed?
- What is my timetable for this week?
- How many ECTS is the Text Mining course worth?
- Do I have any outstanding fees?

## Deployment

**Live Application:** [(https://aims-chatbot.streamlit.app/)]

**Deployment Platform:** 
Streamlit Community Cloud: Hosting platform for the application

## Project Structure

```
project-root/
├── PROJECT4.0.py          # Main application
├── assets/
│   └── AIresponse.jpeg
├── database/
│   └── MongoDB_connection.py             
├── tools/
│   └── mongodb_rag.py   
│   └── scrapping_tool.py                    
├── utils/
│   └── chat_history.py
│   └── gemini_init_function.py
│   └── langfuse_function.py                 
├── docs/
│   └── ARCHITECTURE.md
├── .gitignore    
├── requirements.txt
├── .devconteiner
│   └── devconteiner.json
├── webscraping_and_vectors/
│   └── vectors/
|       └── vector_generating_netpa/
|           └── generate_vectors_netpa.py
|           └── generate_vectors_netpa_2.0.py
|           └── # Final Jsons with the embeddings (info of each link)
|       └── vector_generating_netpa_files/
|           └── generate_vectors_files.py
|           └── generate_vectors_files_2.0.py
|           └── # Final Jsons with the embeddings (relevant files extracted)
│   └── webscraping/
|       └── cleaning/
|           └── netpa_btns/
|               └── # Here will happear the cleaned jsons from netpa (the ones generated by netpa_1.0/2.0 ipynb)
|           └── cleaned_json.ipynb
|       └── netpa_scraping/
|           └── dados_netpa/
|               └── downloads/
|                   └── # Extracted files from netpa_1.0
|               └── downloads_2.0/
|                   └── # Extracted files from netpa_2.0
|               └── Explicação.txt # Some explanations about decisions that we made in this step
|           └── files_reading/
|               └── Explicação.txt # Some explanations about decisions that we made in this step
|               └── process_files_from_netpa.py
|               └── process_files_from_netpa_2.0.py
|               └── # Two json files will be generated after running the .py files with the the info of the relevant extracted files only
|           └── netpa_1.0.ipynb
|           └── netpa_2.0.ipynb
|           └── # Two json files will be generated after running both netpa_1.0/2.0.ipynb, with relevant info about each link of the website
├── edgedriver_win64         #Run webscraping
├── packages.txt
├── unnamed-removebg-preview.png
├── fundo verde com simbolo branco.png       
├── .env.example         
└── README.md           
```

## Team
- David Santos: Google Gemini integration and management of the API key.
- Bernardo Caldas: Integration of MongoDB and implementation of RAG.
- Pedro Silva: Responsible for Streamlit UI and Langfuse.
- Inês Vicente: Deployment on Streamlit Cloud.
---


