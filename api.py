from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel 
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
import tools
import chat
import os
import shutil

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

class ChatMessage(BaseModel):
    role: str 
    content: str 

class ChatRequest(BaseModel):
    messages: list[ChatMessage]

class ChatResponse(BaseModel):
    message: str 
    conversation_ended: bool 

@app.get('/')
async def greet():
    return {'Hello': 'Go to /chat to chat with agent'}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        # Create uploads directory if it doesn't exist
        os.makedirs("uploads", exist_ok=True)
        
        # Save the file
        file_path = os.path.join("uploads", file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        return {"message": "File uploaded successfully", "filename": file.filename}
    except Exception as e:
        return {"error": str(e)}

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    langchain_messages = []    

    for msg in request.messages:
        if msg.role == "user":
            langchain_messages.append(HumanMessage(content=msg.content))
        elif msg.role == "assistant":
            langchain_messages.append(AIMessage(content=msg.content))
        elif msg.role == "system":
            langchain_messages.append(SystemMessage(content=msg.content))
    print(request)
    tools.ec = False 

    try: 
        response = chat.agent.invoke({'messages': langchain_messages})
    except Exception as e:
        return ChatResponse(
            message=f'An error occurred: {str(e)}',
            conversation_ended=True
        )
    assistant_message = response['messages'][-1].content 
    conversation_ended = tools.ec 
    return ChatResponse(
        message = assistant_message,
        conversation_ended = conversation_ended
    )
