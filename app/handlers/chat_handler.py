from ..services.agent_service import agent_service
from ..schemas.chat_schema import ChatRequest, ChatResponse

async def handle_chat_message(request: ChatRequest, messages) -> ChatResponse:
    """Handle incoming chat messages using the agent service."""
    response = agent_service.process_message(request.message)
    return ChatResponse(response=response)