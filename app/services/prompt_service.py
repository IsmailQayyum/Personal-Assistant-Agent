from langchain_core.messages import SystemMessage 
from ..schemas.chat_schema import ChatMessages

SYSTEM_PROMT = '''
You are a very helpful personal assistant. 
Greet user in the beggining 
You talk to your user, and give him appropriate reply.
End the chat if you feel like user has ended the chat. 
You can load a document using the "load_document" tool if the user provides a file path. 
Then, you can use the "ask_about_document" tool to answer questions based on that document.'''


def build_chat_messages() -> ChatMessages:
    message_history=[]
    message_history.append(SystemMessage(content=SYSTEM_PROMT))
    messages= ChatMessages(message_history=message_history)
    return messages
    