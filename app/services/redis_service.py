from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI
from langchain_redis import RedisChatMessageHistory
from app.services.llm_sevice import get_llm
from app.schemas.chat_schema import ChatRequest, ChatResponse
from app.services.prompt_service import get_system_prompt
from app.services.agent_service import agent
REDIS_URL = "redis://localhost:6379"


def get_redis_response(chat_request:ChatRequest):
    try:
        history = get_redis_history(chat_request.session_id)
        history.add_user_message(chat_request.message)
        agent_response = agent.process_message(chat_request.message)
        history.add_ai_message(agent_response)
        return ChatResponse(response=agent_response)
        
    except Exception as e:
        print(f"Error in Redis service: {str(e)}")
        try:
            response = agent.process_message(chat_request.message)
            return ChatResponse(response=response)
        except Exception:
            return ChatResponse(
                response="I'm sorry, I encountered an error processing your request."
            )

def get_redis_history(session_id: str) -> BaseChatMessageHistory:
    return RedisChatMessageHistory(session_id, redis_url=REDIS_URL)
