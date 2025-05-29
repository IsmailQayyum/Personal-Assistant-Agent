from langchain_core.tools import tool
from .document_service import DocumentService

document_service = DocumentService()

@tool
def end_chat():
    '''Ends chat with the user.'''
    print('[Tool] Ending Chat ...')
    return "Chat ended."

@tool
def load_document(path: str) -> str:
    '''Loads a document from the given path and processes text and images.'''
    return document_service.load_document(path)

@tool
def ask_about_document(question: str) -> str:
    '''Answers questions about the loaded document's text content.'''
    return document_service.ask_about_document(question)

@tool
def ask_about_images(question: str) -> str:
    '''Answers questions about images in the loaded document.'''
    return document_service.ask_about_images(question)