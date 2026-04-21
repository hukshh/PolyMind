import os
import time
from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
import shutil

from database import init_db, get_db
from models import QueryHistory
from rag import RAGPipeline
from agents import PolyMindCrew

app = FastAPI(title="PolyMind API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

rag = RAGPipeline()

@app.on_event("startup")
def startup():
    init_db()

class URLIngest(BaseModel):
    url: str

class QueryRequest(BaseModel):
    query: str

@app.post("/ingest/pdf")
async def ingest_pdf(file: UploadFile = File(...)):
    try:
        temp_path = f"temp_{file.filename}"
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        rag.ingest_pdf(temp_path)
        os.remove(temp_path)
        return {"status": "success", "message": f"Ingested {file.filename}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ingest/url")
async def ingest_url(data: URLIngest):
    try:
        rag.ingest_url(data.url)
        return {"status": "success", "message": f"Ingested {data.url}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query")
async def query_handler(data: QueryRequest, db: Session = Depends(get_db)):
    start_time = time.time()
    try:
        # 1. Retrieve chunks
        relevant_docs = rag.search(data.query)
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
    total_queries = db.query(QueryHistory).count()
    # Simple average calculation
    avg_time = 0
    if total_queries > 0:
        times = db.query(QueryHistory.response_time).all()
        avg_time = sum([t[0] for t in times]) / total_queries
    
    return {
        "total_queries": total_queries,
        "avg_response_time": avg_time,
        "docs_ingested": "See Pinecone Index" # Placeholder
    }
