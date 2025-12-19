# [AIMS- Chatbot]

AIMS: Your Intelligent Campus Companion at NOVA IMS 

## Overview

AIMS is a comprehensive AI-powered virtual assistant designed to streamline the academic experience for Nova IMS students. Powered by Google Gemini and MongoDB Atlas, it utilizes RAG to answer administrative and academic queries with precison. It features a secure , real-time integration with NetPA to retrieve personalized timetables and offers dynamic integration modes, ensuring students have instant access to the information they need, when they need.

## Features
- Language: Switch between Portuguese and English language;
- Multi-Personality: Switch between Academic Advisor, Career Coach, and Buddy Modes;
- Securaty: it only can be used by people who have their data in the database and have their student number and password in the securaty database
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
- MongoDB Atlas: Serves as a database, functioning as a Vector Store for RAG and storing static university data.

**AI/ML:**
- Langfuse: Observability, tracing and monitoring LLM interactions;
- LangChain: Framework to orchestrating the RAG pipeline and managing document retrieval;
- Function Calling (Tools): Custom implementation allowing the LLM to autonomously choose between searching the vector database (MongoDB) or scraping real-time data (NetPA);
- Sentence Transformers: Used for generating vector embeddings for document ingestion.

## Architecture

### AIMS - Architecture

    User[Student] --> (interects) UI[Streamlit Frontend]
    UI --> (sendes query) Logic[Python Backend]
    Logic --> (invokes) LLM[Google Gemini API]
    LLM --> (decision tool) Router{Tool Router}

    Router --> (data base) RAG[MongoDB Atlas (Vector Store)]
    Router --> (real time data) Scraper[Selenium/Chromium (Netpa)]

    RAG --> (context)LLM
    Trace --> Langfuse

    LLM --> (final response) UI

### Layer Structure

    UI Layer: 
        - Streamlit: handles user input, chat session state management and manages authentication via student number/ password verification.

    Service Layer: Initializates connections, manages the chat history and coordinates the flow between UI and AI.

    AI Layer: 
        - Google Gemini: manages system prompts, handles context window limits and integrates Langfuse for tracing and monitoring model performance. (gemini_init_function.py, langfuse_function.py)

    Tools Layer: 
        - Vector Store: MongoDB Atlas stores embedding of Nova IMS documents for RAG operations (mongodb_rag.py)
        - Web Scraper: Selenium based tool that performs real-time authentication on the NetPA portal to retrieve live schedule data. (scrapping_tool.py)

### Key Design Decisions and Justifications

- RAG and Scraping: we implemented two approaches to address different data needs. RAG is used for static, unstructure data, while Scraping is used for private, real-time data.

- MongoDB as Vector Store: we chose it because it handles standard NoSQL data and vector embeddings, avoiding a separate database just for vectors.

- Sreamlit: we chose it for its rapida development capabilities and native Python integration.

- Selenium: utilizes Chromium drivers to ensure the application functions correctly on Streamlit Cloud (Linux)

- Langfuse: we integrate from the start to understand which tool was used in each interaction, monitoring AI applications.

## Installation & Setup

### Prerequisites
- Python 3.x
- API keys for [required services]

### Installation Steps

1. Clone the repository:
```bash
git clone pedrosilva-98/AIMS-chatbot
cd AIMS-Chatbot
```

2. Install dependencies:
```bash
uv sync
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys
```

**Required environment variables:**
```
langfuse_secret_key = "sk-lf-57db3c7c-b936-4b93-8a29-65458665be94"
langfuse_public_key = "pk-lf-3e54915a-9181-4623-b71b-b560a740604d"
langfuse_host = "https://cloud.langfuse.com"

GOOGLE_API_KEY= "AIzaSyDaUlrumleZCduEYmFfzhYzEM3T7qzX0tM"

MONGO_URI= "mongodb+srv://chatbot_user:PapiPauligol@cluster0.zf2kzct.mongodb.net/?appName=Cluster0"

**Database with Student Numbers and Password**
- Only we can use the app
```

4. Run the application:
```bash
uv run streamlit run PROJECT4.0.py
```

## Usage

Instructions and examples for using your application. Include:
- How to navigate the interface
- Key workflows
- Screenshots or GIFs demonstrating functionality (recommended for visual clarity)

**Example:**

1. Navigate to the main page
2. Upload a document or enter your query
3. Interact with the AI assistant through the chat interface
4. View results and explore additional features

*Add screenshots or GIFs here to visually demonstrate your application's key features*

## Deployment

**Live Application:** [(https://aims-chatbot.streamlit.app/)]

**Deployment Platform:** 
Streamlit Community Cloud: Hosting platform for the application

Instructions for deploying your own instance (if applicable).

## Project Structure

```
project-root/
├── PROJECT4.0.py          # Main application entry point
├── services/              # Business logic layer
├── tools/                 # Function calling tools
├── utils/                 # Utility functions
├── docs/
│   └── ARCHITECTURE.md    # Architecture decisions and explanations
├── requirements.txt       # Dependencies
├── .env.example          # Environment variable template
└── README.md             # This file
```

**Note:** Component-level READMEs (e.g., `services/README.md`, `tools/README.md`) are recommended if those components need detailed explanation.

## Team

- Team Member 1 - [Role/Responsibilities]
- Team Member 2 - [Role/Responsibilities]
- Team Member 3 - [Role/Responsibilities]
- Team Member 4 - [Role/Responsibilities]

## License

[Your chosen license - MIT, Apache, etc. - not necessary]

---

## What Makes a Good README?

Your README should answer:
- **What** does this application do?
- **Why** does it exist / what problem does it solve?
- **How** do I run it locally?
- **Who** built it?

Keep it clear, organized, and professional. This is often the first thing evaluators and potential users will see.

