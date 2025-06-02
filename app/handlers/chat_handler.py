from app.schemas.chat_schema import ChatRequest, ChatResponse, ChatMessages
from ..services import llm_sevice, prompt_service
from ..services.redis_service import get_redis_history, get_redis_response
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage

llm = llm_sevice.get_llm()


async def initialize_chat():
    messages = prompt_service.build_chat_messages()
    return messages

async def handle_chat_message(request: ChatRequest, messages: ChatMessages) -> ChatResponse:
    message_history = messages.message_history
    message_history.append(HumanMessage(content=request.message))
    response = llm.invoke(message_history)
    message_history.append(AIMessage(content=response.content))
    return ChatResponse(response=str(response.content))

