from fastapi import APIRouter, HTTPException
from ..models.request_models import ChatRequest
from ..models.response_models import ChatResponse
from ..services.rag_service import rag_service
from ..utils.logger import logger

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    logger.info(f"Incoming chat request: {request.message}")
    
    if not request.message.strip():
        logger.warning("Empty message received")
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    
    try:
        response_text = await rag_service.generate_response(request.message)
        logger.info("Chat response generated successfully")
        return ChatResponse(response=response_text)
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error during chat processing")
