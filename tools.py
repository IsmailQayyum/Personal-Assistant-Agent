import os
import io
import fitz  
import base64
from typing import List, Dict, Tuple
from PIL import Image
from langchain_core.tools import tool
from langchain_openai import AzureChatOpenAI
from dotenv import load_dotenv
import PyPDF2
from langchain_community.vectorstores import FAISS
from langchain_openai import AzureOpenAIEmbeddings
from langchain_core.documents import Document

load_dotenv()

global ec
ec = False
doc_text = ""

image_descriptions = []
vectorstore = None

def initialize_embeddings():
    """Initialize and return Azure OpenAI embeddings."""
    ak = os.getenv('AZURE_OPENAI_API_KEY')
    av = os.getenv('API_VERSION')
    ep = os.getenv('ENDPOINT_URL')
    
    return AzureOpenAIEmbeddings(
        api_key=ak,
        api_version=av,
        azure_endpoint=ep,
        azure_deployment="text-embedding-3-small"  
    )

def extract_images_from_pdf(pdf_path: str) -> List[Tuple[Image.Image, int]]:
    """Extract images from PDF and return them with their page numbers."""
    images = []
    try:
        pdf_document = fitz.open(pdf_path)
        
        for page_num, page in enumerate(pdf_document):
            image_list = page.get_images(full=True)
            
            for img_index, img in enumerate(image_list):
                xref = img[0]
                base_image = pdf_document.extract_image(xref)
                image_bytes = base_image["image"]
                
                image = Image.open(io.BytesIO(image_bytes))
                images.append((image, page_num + 1))
                
        return images
    except Exception as e:
        print(f"Error extracting images: {e}")
        return []

def get_image_description(image: Image.Image) -> str:
    """Get description of an image using Azure OpenAI Vision model."""
    try:
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        ak = os.getenv('AZURE_OPENAI_API_KEY')
        av = os.getenv('API_VERSION')
        ep = os.getenv('ENDPOINT_URL')
        dn = os.getenv('DEPLOYMENT_NAME')
        
        vision_model = AzureChatOpenAI(
            api_key=ak,
            api_version=av,
            azure_endpoint=ep,
            azure_deployment=dn,  
        )
        
        message = {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Describe this image in detail. Focus on what's visually present."
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{img_str}"
                    }
                }
            ]
        }
        
        response = vision_model.invoke([message])
        return response.content
        
    except Exception as e:
        print(f"Error getting image description: {e}")
        return "Error analyzing image"

def process_pdf_images(pdf_path: str) -> Dict:
    """Process all images in a PDF, get descriptions and store them in vectorstore."""
    global image_descriptions, vectorstore
    
    images_with_pages = extract_images_from_pdf(pdf_path)
    
    if not images_with_pages:
        return {"status": "No images found in the PDF"}
    
    documents = []
    for idx, (image, page_num) in enumerate(images_with_pages):
        description = get_image_description(image)
        
        doc = Document(
            page_content=description,
            metadata={
                "source": pdf_path,
                "page": page_num,
                "image_index": idx
            }
        )
        documents.append(doc)
        
        image_descriptions.append({
            "page": page_num,
            "image_index": idx,
            "description": description
        })
    
    embeddings = initialize_embeddings()
    
    if not vectorstore:
        vectorstore = FAISS.from_documents(documents, embeddings)
    else:
        vectorstore.add_documents(documents)
    
    return {
        "status": "success",
        "images_processed": len(images_with_pages),
        "descriptions": image_descriptions
    }

def search_image_descriptions(query: str, k: int = 3) -> List[Dict]:
    """Search for relevant image descriptions based on the query."""
    global vectorstore
    
    if not vectorstore:
        return [{"error": "No images have been processed yet"}]
    
    results = vectorstore.similarity_search(query, k=k)
    
    response = []
    for doc in results:
        response.append({
            "description": doc.page_content,
            "page": doc.metadata["page"],
            "image_index": doc.metadata["image_index"],
            "source": doc.metadata["source"]
        })
    
    return response

@tool 
def end_chat():
    '''ends chat with the user.''' 
    print('[Tool]Ending Chat ... ')
    global ec 
    ec = True
    return ec

@tool
def load_document(path: str) -> str:
    '''Loads a document from the given path and processes text and images.'''
    global doc_text, image_descriptions, vectorstore
    try:
        ext = os.path.splitext(path)[1].lower()
        
        if ext == '.txt':
            with open(path, 'r', encoding='utf-8') as f:
                doc_text = f.read()
            return f"Text document '{path}' loaded successfully."
            
        elif ext == '.pdf':
            with open(path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                doc_text = ''
                for page in reader.pages:
                    doc_text += page.extract_text() or ''
            
            image_descriptions = []
            image_result = process_pdf_images(path)
            
            if image_result["status"] == "No images found in the PDF":
                return f"Document '{path}' loaded successfully."
            else:
                return f"Document '{path}' loaded successfully. Found and processed {image_result['images_processed']} images."
        else:
            return "Unsupported file format. Only .txt and .pdf files are supported."
            
        if not doc_text.strip():
            return "The document was loaded, but the text content appears to be empty or unreadable."
            
    except Exception as e:
        return f"Error loading document: {e}"
    
@tool
def ask_about_document(question: str) -> str:
    '''Answers questions about the loaded document's text content.'''
    global doc_text
    if not doc_text:
        return "No document loaded. Please load a document first using 'load_document'."
    
    relevant_sentences = [line for line in doc_text.split('. ') if any(word.lower() in line.lower() for word in question.split())]
    context = '. '.join(relevant_sentences[:5])  
    
    if not context:
        context = "No relevant information found in the document text."
    
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

@tool
def ask_about_images(question: str) -> str:
    '''Answers questions about images in the loaded document.'''
    global image_descriptions
    
    if not image_descriptions:
        return "No images have been processed. Please load a PDF document with images first."
    
    relevant_images = search_image_descriptions(question)
    
    if not relevant_images or "error" in relevant_images[0]:
        return "No relevant images found that can answer your question."
    
    context = "Information from document images:\n\n"
    for idx, img in enumerate(relevant_images):
        context += f"Image {idx+1} (Page {img['page']}):\n{img['description']}\n\n"
    
    ak = os.getenv('AZURE_OPENAI_API_KEY')
    av = os.getenv('API_VERSION')
    ep = os.getenv('ENDPOINT_URL')
    dn = os.getenv('DEPLOYMENT_NAME')
    llm = AzureChatOpenAI(api_key=ak, api_version=av, azure_endpoint=ep, azure_deployment=dn)
    
    prompt = (
        f"You are a helpful assistant analyzing images from a document. Based on the following image descriptions, answer the question.\n\n"
        f"Context:\n{context}\n\nQuestion: {question}\nAnswer:"
    )
    return llm.invoke(prompt).content

def get_ec():
    ret