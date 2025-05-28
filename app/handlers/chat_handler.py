from app.schemas.chat_schema import ChatRequest , ChatResponse
from ..services import llm_sevice

async def handle_chat_message(request: ChatRequest) -> ChatResponse:
    
    llm = await llm_sevice.get_llm()
    response = llm.invoke(request.message)
    return ChatResponse(response=str(response.content))
    


