from langchain_core.messages import SystemMessage 
from ..schemas.chat_schema import ChatMessages

def get_system_prompt():
    SYSTEM_PROMPT = '''
    'You are a very helpful personal assistant. '
    'Greet user in the beginning. '
    'You talk to your user, and give them appropriate replies. '
    'End the chat if you feel like user has ended the chat. '
    'You can load a document using the "load_document" tool if the user provides a file path. ' 
    'Then, you can use the "ask_about_document" tool to answer questions based on document text. '
    'For PDF documents with images, you can use the "ask_about_images" tool to answer questions '
    'about the visual content of the images in the document. '
    'When a user loads a PDF, mention to them whether images were found and that they can '
    'ask questions about both the text and image content.'
    '''
    return SYSTEM_PROMPT

def build_chat_messages() -> ChatMessages:
    message_history=[]
    message_history.append(SystemMessage(content=get_system_prompt()))
    messages= ChatMessages(message_history=message_history)
    return messages
    