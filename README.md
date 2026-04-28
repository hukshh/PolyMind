# AI Research Assistant (FastAPI + RAG-Ready)

A clean, modular FastAPI backend for an AI-powered research assistant.

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

## 📁 Project Structure
```text
backend/
├── routes/    (API endpoints)
├── services/  (Business logic)
├── utils/     (Helper functions & Config)
├── models/    (Request/Response schemas)
└── data/      (Local uploads & Indices)
```

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
The previous PolyMind system is preserved inside [/legacy-polymind](./legacy-polymind) for reference.

---
Created with ❤️ by the AI Research Assistant Team.
