from pydantic import BaseModel
from langchain_core.messages import SystemMessage, AIMessage, HumanMessage
class ChatRequest(BaseModel):
    message: str 

class ChatResponse(BaseModel):
    response: str 

class ChatMessages(BaseModel):
    message_history: list[SystemMessage | HumanMessage | AIMessage] 

