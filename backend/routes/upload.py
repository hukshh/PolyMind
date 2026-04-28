from fastapi import APIRouter, UploadFile, File, HTTPException
from services.pdf_service import pdf_service

router = APIRouter()

@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    filename = await pdf_service.process_pdf(file)
    return {"status": "success", "filename": filename}
