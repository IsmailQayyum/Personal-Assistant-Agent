from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
from app.routers import chat_router
from app.services.document_service import DocumentService


app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize document service
document_service = DocumentService()

# Get the absolute path to the project root directory
BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
static_dir = os.path.join(BASE_DIR, "static")
uploads_dir = os.path.join(BASE_DIR, "uploads")

# print(f"Base directory: {BASE_DIR}")
# print(f"Static directory: {static_dir}")
# print(f"Static directory exists: {os.path.exists(static_dir)}")

# Create static and uploads directories if they don't exist
os.makedirs(static_dir, exist_ok=True)
os.makedirs(uploads_dir, exist_ok=True)

# Mount static files with absolute path
app.mount("/static", StaticFiles(directory=static_dir), name="static")

app.include_router(chat_router.router)

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
    
    # Process the document automatically
    try:
        result = document_service.load_document(save_path)
        return {"success": True, "filename": file.filename, "message": result}
    except Exception as e:
        return JSONResponse(status_code=500, content={"success": False, "error": f"Failed to process document: {str(e)}"})

@app.get('/')
async def root():
    return FileResponse(os.path.join(static_dir, "index.html"))