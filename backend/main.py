import os
import time
from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
import shutil

from database import get_db
from models import QueryHistory, Document
from rag import RAGPipeline
from agents import PolyMindCrew

app = FastAPI(title="PolyMind API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

rag = None

def get_rag():
    global rag
    if rag is None:
        print("DEBUG: Initializing RAG Pipeline (Lazy Load)...")
        rag = RAGPipeline()
    return rag

@app.on_event("startup")
def startup():
    print("DEBUG: Server starting instantly. All heavy connections deferred.")

@app.get("/")
def root():
    return {"status": "PolyMind Engine Online", "port": 10000}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

class URLIngest(BaseModel):
    url: str

class QueryRequest(BaseModel):
    query: str

@app.get("/debug-status")
async def debug_status(db: Session = Depends(get_db)):
    status = {
        "database": "FAILED",
        "pinecone_api": "MISSING",
        "pinecone_index": "MISSING",
        "pinecone_connection": "FAILED",
        "environment": {
            "PINECONE_INDEX_NAME": os.getenv("PINECONE_INDEX_NAME"),
            "HAS_GROQ_KEY": bool(os.getenv("GROQ_API_KEY")),
            "HAS_PINECONE_KEY": bool(os.getenv("PINECONE_API_KEY"))
        }
    }
    
    # Check DB
    try:
        db.execute("SELECT 1")
        status["database"] = "LIVE"
    except Exception as e:
        status["database"] = f"FAILED: {str(e)}"
        
    # Check Pinecone
    api_key = os.getenv("PINECONE_API_KEY")
    index_name = os.getenv("PINECONE_INDEX_NAME")
    if api_key:
        status["pinecone_api"] = "PROVIDED"
        try:
            from pinecone import Pinecone
            pc = Pinecone(api_key=api_key)
            if index_name:
                status["pinecone_index"] = index_name
                idx = pc.Index(index_name)
                stats = idx.describe_index_stats()
                status["pinecone_connection"] = "LIVE"
                status["pinecone_stats"] = stats
        except Exception as e:
            status["pinecone_connection"] = f"FAILED: {str(e)}"
            
    return status

@app.post("/ingest/pdf")
async def ingest_pdf(file: UploadFile = File(...), db: Session = Depends(get_db)):
    temp_file = None
    try:
        # Use a more robust temp file handling
        import tempfile
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            shutil.copyfileobj(file.file, tmp)
            temp_path = tmp.name
        
        print(f"DEBUG: Processing PDF {file.filename} from {temp_path}")
        current_rag = get_rag()
        
        if not os.getenv("PINECONE_API_KEY") or not os.getenv("PINECONE_INDEX_NAME"):
            raise ValueError("Missing Pinecone environment variables (API Key or Index Name)")

        current_rag.ingest_pdf(temp_path)
        
        if os.path.exists(temp_path):
            os.remove(temp_path)

        # Save to DB
        doc = Document(name=file.filename, source_type="pdf")
        db.add(doc)
        db.commit()

        return {"status": "success", "message": f"Ingested {file.filename}"}
    except Exception as e:
        print(f"CRITICAL ERROR during PDF ingestion: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Engine Error: {str(e)}")

@app.post("/ingest/url")
async def ingest_url(data: URLIngest, db: Session = Depends(get_db)):
    try:
        current_rag = get_rag()
        current_rag.ingest_url(data.url)

        # Save to DB
        doc = Document(name=data.url, source_type="url")
        db.add(doc)
        db.commit()

        return {"status": "success", "message": f"Ingested {data.url}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query")
async def query_handler(data: QueryRequest, db: Session = Depends(get_db)):
    start_time = time.time()
    try:
        current_rag = get_rag()
        # 1. Retrieve chunks
        relevant_docs = current_rag.search(data.query)
        if not relevant_docs:
            context_text = "No relevant information was found in the provided document for this query."
        else:
            context_text = "\n\n".join([f"Source: {d.metadata.get('source')}\nContent: {d.page_content}" for d in relevant_docs])
        
        # 2. Run CrewAI
        crew = PolyMindCrew(context=context_text)
        result = crew.run(data.query)
        
        end_time = time.time()
        duration = end_time - start_time
        
        # 3. Store in history
        history = QueryHistory(
            query=data.query,
            response=str(result),
            response_time=duration,
            source_type="mixed"
        )
        db.add(history)
        db.commit()
        
        return {
            "answer": str(result),
            "response_time": duration
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/history")
async def get_history(db: Session = Depends(get_db)):
    history = db.query(QueryHistory).order_by(QueryHistory.timestamp.desc()).limit(50).all()
    return history

@app.get("/metrics")
async def get_metrics(db: Session = Depends(get_db)):
    try:
        total_queries = db.query(QueryHistory).count()
        total_docs = db.query(Document).count()
        
        avg_time = 0
        if total_queries > 0:
            times = db.query(QueryHistory.response_time).all()
            avg_time = sum([t[0] for t in times]) / total_queries
        
        return {
            "total_queries": total_queries,
            "avg_response_time": round(avg_time, 2),
            "docs_ingested": total_docs,
            "system_health": "Optimal",
            "active_agents": 2
        }
    except Exception as e:
        return {"error": str(e)}
@app.get("/documents")
async def list_documents(db: Session = Depends(get_db)):
    return db.query(Document).order_by(Document.timestamp.desc()).all()

@app.delete("/documents/{doc_id}")
async def delete_document(doc_id: int, db: Session = Depends(get_db)):
    doc = db.query(Document).filter(Document.id == doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # 1. Delete from Pinecone
    current_rag = get_rag()
    success = current_rag.delete_source(doc.name)
    
    # 2. Delete from Postgres
    if success:
        db.delete(doc)
        db.commit()
        return {"status": "success", "message": f"Deleted {doc.name}"}
    else:
        raise HTTPException(status_code=500, detail="Failed to delete from vector store")

@app.delete("/documents")
async def clear_all_documents(db: Session = Depends(get_db)):
    # 1. Clear Pinecone
    current_rag = get_rag()
    success = current_rag.clear_all()
    
    # 2. Clear Postgres
    if success:
        db.query(Document).delete()
        db.commit()
        return {"status": "success", "message": "All documents cleared"}
    else:
        raise HTTPException(status_code=500, detail="Failed to clear vector store")
