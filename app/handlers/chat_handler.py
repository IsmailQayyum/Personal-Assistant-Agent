from app.schemas.chat_schema import ChatRequest, ChatResponse, ChatMessages
from ..services.redis_service import get_redis_history, get_redis_response
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage
from app.services.agent_service import agent


async def handle_chat_message(request: ChatRequest, messages) -> ChatResponse:
    """Handle incoming chat messages using the agent service."""
    response = agent.process_message(request.message)
    return ChatResponse(response=response)


