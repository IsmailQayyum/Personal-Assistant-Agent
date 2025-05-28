from fastapi import APIRouter
from ..schemas.chat_schema import ChatRequest , ChatResponse
from ..handlers import chat_handler
router = APIRouter(
    prefix='/chat',
    tags= ['chat']
)

@router.post('/' , response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest ):
    return await chat_handler.handle_chat_message(request)
    

