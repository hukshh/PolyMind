# AI Research Assistant (RAG-Ready Backend)

A clean, modular FastAPI backend designed for an AI-powered research assistant.

## 🚀 Features
- **PDF Upload API**: Accept and store documents securely.
- **Chat API**: Interactive endpoint for AI research conversations.
- **Modular Architecture**: Clean separation of routes, services, and utilities.
- **RAG-Ready Design**: Structured to support FAISS and LLM integration in the next phase.

## 🛠️ Tech Stack
- **FastAPI**: Modern, high-performance web framework.
- **Streamlit**: Frontend interface (upcoming).
- **Groq**: High-speed LLM inference (upcoming).
- **FAISS**: Vector database for document retrieval (upcoming).

## 🏁 Run Locally

```bash
cd backend
uvicorn main:app --reload
```

## 🌐 API Docs
Once the server is running, you can access the interactive Swagger documentation at:
[http://localhost:8000/docs](http://localhost:8000/docs)

---

## ❌ Legacy Code
The previous PolyMind system, including legacy configurations and Docker setups, has been moved to [/legacy-polymind](./legacy-polymind) for reference.

---
Created with ❤️ by the AI Research Assistant Team.
