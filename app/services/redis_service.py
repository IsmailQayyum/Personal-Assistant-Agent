from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI
from langchain_redis import RedisChatMessageHistory
from app.services.llm_sevice import get_llm
from app.schemas.chat_schema import ChatRequest, ChatResponse
from app.services.prompt_service import get_system_prompt
REDIS_URL = "redis://localhost:6379"

def get_redis_response(chat_request:ChatRequest):

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", get_system_prompt()),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{input}"),
        ]
    )

    chain = prompt | get_llm()

    chain_with_history = RunnableWithMessageHistory(
        chain, get_redis_history, input_messages_key="input", history_messages_key="history"
    )
  
    response1 = chain_with_history.invoke(
        {"input": chat_request.message},
        config={"configurable": {"session_id": chat_request.session_id}},
    )
    return ChatResponse(response=response1.content)

def get_redis_history(session_id: str) -> BaseChatMessageHistory:
    return RedisChatMessageHistory(session_id, redis_url=REDIS_URL)
