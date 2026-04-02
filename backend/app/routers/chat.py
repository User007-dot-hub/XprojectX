from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from app.services.chat_service import generate_chat_response

router = APIRouter(prefix="/api/chat", tags=["chat"])

class ChatMessage(BaseModel):
    role: str
    content: str
    
class ChatRequest(BaseModel):
    messages: List[ChatMessage]

class ChatResponse(BaseModel):
    response: str

@router.post("", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    if not request.messages:
        raise HTTPException(status_code=400, detail="Messages list cannot be empty.")
    
    msg_dicts = [{"role": msg.role, "content": msg.content} for msg in request.messages]
    
    response_text = await generate_chat_response(msg_dicts)
    return ChatResponse(response=response_text)
