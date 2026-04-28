from fastapi import APIRouter
from pydantic import BaseModel
from ..services.llm_service import llm_service

router = APIRouter()

class ChatRequest(BaseModel):
    message: str

@router.post("/chat")
async def chat(request: ChatRequest):
    response = await llm_service.get_response(request.message)
    return {"status": "success", "response": response}
