from fastapi import APIRouter, Depends, Header
from ..schemas.chat_schema import ChatRequest, ChatResponse, ChatMessages
from ..handlers import chat_handler
from langchain_core.messages import SystemMessage, AIMessage, HumanMessage
from ..services.prompt_service import build_chat_messages 
from ..services.redis_service import get_redis_response
router = APIRouter(
    prefix='/chat',
    tags= ['chat']
)

@router.post('/'  )
async def chat_endpoint(request: ChatRequest,messages:ChatMessages = Depends(build_chat_messages)):
    response = await chat_handler.handle_chat_message(request=request,messages=messages)
    return {'response': response.response,
            'message_history': messages.message_history}
    #return {'response': messages.message_history[-1].content}
    
@router.post('/redis')
async def chat_with_history( request: ChatRequest):
    response =  get_redis_response(chat_request=request)
    return {'redis-response': response.response}

