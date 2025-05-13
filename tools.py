from langchain_core.tools import tool 
from langchain_openai import AzureChatOpenAI
import os
import PyPDF2

global ec 
ec = False 
doc_text = ""

@tool 
def end_chat():
    '''ends chat with the user.''' 
    print('[Tool]Ending Chat ... ')
    global ec 
    ec = True
    return ec

@tool
def load_document(path: str) -> str:
    '''Loads a document from the given path and stores it for Q&A.'''
    global doc_text
    try:
        ext = os.path.splitext(path)[1].lower()
        
        if ext == '.txt':
            with open(path, 'r', encoding='utf-8') as f:
                doc_text = f.read()
        elif ext == '.pdf':
            with open(path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                doc_text = ''
                for page in reader.pages:
                    doc_text += page.extract_text() or ''
        else:
            return "Unsupported file format. Only .txt and .pdf files are supported."

        if not doc_text.strip():
            return "The document was loaded, but it appears to be empty or unreadable."

        print(f"[Tool] Document '{path}' loaded successfully.")
        return f"Document '{path}' loaded successfully."
    
    except Exception as e:
        return f"Error loading document: {e}"
    
@tool
def ask_about_document(question: str) -> str:
    '''Answers questions about the loaded document.'''
    global doc_text
    if not doc_text:
        return "No document loaded. Please load a document first using 'load_document'."

    relevant_sentences = [line for line in doc_text.split('. ') if any(word.lower() in line.lower() for word in question.split())]

    context = '. '.join(relevant_sentences[:5])  

    if not context:
        context = "No relevant information found in the document."

    ak = os.getenv('AZURE_OPENAI_API_KEY')
    av = os.getenv('API_VERSION')
    ep = os.getenv('ENDPOINT_URL')
    dn = os.getenv('DEPLOYMENT_NAME')

    llm = AzureChatOpenAI(api_key=ak, api_version=av, azure_endpoint=ep, azure_deployment=dn)
    
    prompt = (
        f"You are a helpful assistant. Based on the following context, answer the question.\n\n"
        f"Context:\n{context}\n\nQuestion: {question}\nAnswer:"
    )

    return llm.invoke(prompt).content

def get_ec():
    return ec