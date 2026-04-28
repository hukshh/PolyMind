from fastapi import APIRouter, UploadFile, File, HTTPException
from ..services.pdf_service import pdf_service
from ..utils.logger import logger

router = APIRouter()

@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    logger.info(f"Incoming upload request: {file.filename}")
    
    if not file.filename.lower().endswith(".pdf"):
        logger.warning(f"Rejected non-PDF file: {file.filename}")
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    try:
        filename = await pdf_service.process_pdf(file)
        logger.info(f"File uploaded and processed successfully: {filename}")
        return {"filename": filename}
    except Exception as e:
        logger.error(f"Error during PDF upload: {str(e)}")
        raise HTTPException(status_code=500, detail=f"File upload failed: {str(e)}")
