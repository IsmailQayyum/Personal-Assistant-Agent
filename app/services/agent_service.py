from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langgraph.prebuilt import create_react_agent
from .document_service import DocumentService
from .document_tools import end_chat, load_document, ask_about_document, ask_about_images
from .llm_sevice import get_llm
from .prompt_service import SYSTEM_PROMT

class AgentService:
    def __init__(self):
        self.llm = get_llm()
        self.document_service = DocumentService()
        self.agent = self._initialize_agent()
        self.messages = self._initialize_messages()

    def _initialize_agent(self):
        """Initialize the ReAct agent with tools."""
        agent_tools = [end_chat, load_document, ask_about_document, ask_about_images]
        return create_react_agent(self.llm, agent_tools)

    def _initialize_messages(self):
        """Initialize the system message."""
        return [SystemMessage(content=SYSTEM_PROMT)]

    def process_message(self, user_message: str):
        """Process a user message and return the agent's response."""
        self.messages.append(HumanMessage(content=user_message))
        response = self.agent.invoke({'messages': self.messages})
        assistant_message = response['messages'][-1].content
        self.messages.append(AIMessage(content=assistant_message))
        return assistant_message

# Create a singleton instance
agent_service = AgentService()