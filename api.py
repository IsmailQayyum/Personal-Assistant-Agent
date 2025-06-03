from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel 
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
import tools
import chat
import os

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create uploads directory
uploads_dir = "uploads"
os.makedirs(uploads_dir, exist_ok=True)

class ChatRequest(BaseModel):
    message: str 
    session_id: str

class ChatResponse(BaseModel):
    response: str 

@app.get('/')
async def greet():
    return {'Hello': 'Go to /chat to chat with agent'}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # Only allow .txt and .pdf
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in [".txt", ".pdf"]:
        return JSONResponse(status_code=400, content={"success": False, "error": "Only .txt and .pdf files are supported."})
    
    # Save the file
    save_path = os.path.join(uploads_dir, file.filename)
    with open(save_path, "wb") as f:
        content = await file.read()
        f.write(content)
    
    # Process the document automatically using tools.py
    try:
        result = tools.load_document(save_path)
        return {"success": True, "filename": file.filename, "message": result}
    except Exception as e:
        return JSONResponse(status_code=500, content={"success": False, "error": f"Failed to process document: {str(e)}"})

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    # Use the message directly with the agent
    tools.ec = False 
    
    try: 
        # Create a simple message list with the user's message
        langchain_messages = [HumanMessage(content=request.message)]
        response = chat.agent.invoke({'messages': langchain_messages})
    except Exception as e:
        return ChatResponse(response=f'An error occurred: {str(e)}')
    
    assistant_message = response['messages'][-1].content 
    return ChatResponse(response=assistant_message)
