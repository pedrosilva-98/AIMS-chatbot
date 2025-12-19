AIMS - Architecture

    User[Student] --> (interects) UI[Streamlit Frontend]
    UI --> (sendes query) Logic[Python Backend]
    Logic --> (invokes) LLM[Google Gemini API]
    LLM --> (decision tool) Router{Tool Router}

    Router --> (data base) RAG[MongoDB Atlas (Vector Store)]
    Router --> (real time data) Scraper[Selenium/Chromium (Netpa)]

    RAG --> (context)LLM
    Trace --> Langfuse

    LLM --> (final response) UI

