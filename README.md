# 🧠 PolyMind: Simplified Research Assistant

PolyMind is a lightweight Research Assistant that allows you to upload documents and URLs to build a personal knowledge base.

Built with **FastAPI** and **Streamlit**.

## 🚀 Features
- **PDF & URL Ingestion**: Upload documents or scrape web content.
- **Knowledge Base**: Track uploaded documents in a **PostgreSQL** database.
- **Query Interface**: Query your stored knowledge.
- **Internal History**: Stores query history and metrics.

## 🛠️ Tech Stack
- **Backend**: FastAPI
- **Frontend**: Streamlit
- **Database**: PostgreSQL
- **Infrastructure**: Docker & Docker Compose

## 🏁 Quick Start

### 1. Setup Environment
Rename `.env.example` to `.env`.

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

### 1. Backend (Render)
This project uses a `render.yaml` Blueprint to set up the API and Database.
1. Push to GitHub.
2. Go to [Render Blueprints](https://dashboard.render.com/blueprints).
3. Connect your repo and deploy.

### 2. Frontend (Streamlit Cloud)
1. Go to [Streamlit Cloud](https://share.streamlit.io/).
2. Deploy from your GitHub repo.
3. **Main file path**: `frontend/main.py`.
4. In **Advanced Settings -> Secrets**, add:
   ```toml
   BACKEND_URL = "https://your-backend-url.onrender.com"
   ```

---
Created with ❤️ by PolyMind.
