from app.services.agent_service import agent_service, llm_sevice, prompt_service
from app.schemas.chat_schema import ChatRequest, ChatResponse, ChatMessages
from ..services.redis_service import get_redis_history, get_redis_response
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage

async def handle_chat_message(request: ChatRequest, messages) -> ChatResponse:
    """Handle incoming chat messages using the agent service."""
    response = agent_service.process_message(request.message)
    return ChatResponse(response=response)


llm = llm_sevice.get_llm()



