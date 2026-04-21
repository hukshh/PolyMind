# 🧠 PolyMind: Multi-Agent Research Assistant

PolyMind is a state-of-the-art Research Assistant that leverages a **Multi-Agent Crew** to scan documents, synthesize answers, fact-check claims, and recommend further exploration. 

Built with **CrewAI**, **LangChain**, **FastAPI**, and **Streamlit**.

## 🚀 Features
- **PDF & URL Ingestion**: Seamlessly upload documents or scrape web content.
- **RAG Pipeline**: High-speed retrieval using **Pinecone** and Cloud Embeddings.
- **Multi-Agent Collaboration**:
    - 🔍 **Researcher**: Extracts precise data from retrieved document chunks.
    - ✍️ **Summarizer**: Synthesizes notes into a polished, cited response.
    - ⚖️ **Critic**: Fact-checks the output to prevent hallucinations.
    - 💡 **Recommender**: Suggests related topics for deeper exploration.
- **Internal Knowledge Graph**: Stores query history and metrics in **PostgreSQL**.
- **Lite & Fast**: Optimized for **Render Free** and **Streamlit Cloud**.

## 🛠️ Tech Stack
- **AI Core**: CrewAI + LangChain + Groq (Llama 3)
- **Vector DB**: Pinecone
- **Backend**: FastAPI
- **Frontend**: Streamlit
- **Database**: PostgreSQL
- **Infrastructure**: Docker & Docker Compose

## 🏁 Quick Start

### 1. Setup Environment
Rename `.env.example` to `.env` and fill in your keys:
```bash
GROQ_API_KEY=gsk_...
PINECONE_API_KEY=pcsk_...
PINECONE_INDEX_NAME=polymind
```

### 2. Run with Docker
```bash
./setup.sh
```
Or manually:
```bash
docker-compose up --build
```

### 3. Access
- **Frontend**: [http://localhost:8501](http://localhost:8501)
- **API Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)

## 🌐 Deployment
This project is pre-configured for:
- **Backend/DB**: Render
- **Frontend**: Streamlit Cloud

---
Created with ❤️ by PolyMind Crew.
