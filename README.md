# PA-Agent

**PA-Agent** is a secure, agentic AI chatbot built using FastAPI, LangChain, and OAuth2.0. It follows clean architecture principles, modular design, and integrates production-ready DevOps practices.

## Quick Start

### Backend Setup

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Set up environment variables (create `.env` file):

   ```
   AZURE_OPENAI_API_KEY=your_key_here
   API_VERSION=your_version
   ENDPOINT_URL=your_endpoint
   DEPLOYMENT_NAME=your_deployment
   ```

3. Start the backend:

   ```bash
   # Option 1: Use the structured app (recommended)
   uvicorn app.main:app --reload --port 8000

   # Option 2: Use the simple API
   uvicorn api:app --reload --port 8000
   ```

### Flutter App Setup

1. Navigate to the Flutter app directory:

   ```bash
   cd personal_assistant_mobile
   ```

2. Get Flutter dependencies:

   ```bash
   flutter pub get
   ```

3. Run the Flutter app:

   ```bash
   # For web
   flutter run -d chrome

   # For desktop/mobile
   flutter run
   ```

The app will connect to the backend at `http://localhost:8000` for document uploads and chat functionality.

## Project Overview

This Agent serves as a personal AI assistant capable of:

- Answering queries using an LLM (e.g., OpenAI)
- Handling multi-turn conversations with memory and context
- Searching over user-uploaded documents (PDF, DOCX)
- Utilizing LangChain tools (e.g., web search, calculator, Python REPL)
- Managing per-user embeddings and personalized knowledge
- Maintaining secure access through OAuth2.0 with JWT authentication

## Core Features

### FastAPI Backend

- Modular routing (`/auth`, `/chat`, `/user`, `/docs`)
- Dependency injection using `Depends`
- Schema validation using Pydantic
- OAuth2.0 with JWT-based auth flow
- Async handlers and background tasks
- File upload endpoints and secure file processing
- Rate limiting per user

### LangChain Agent Integration

- Agent with memory (e.g., ConversationBufferMemory)
- Integrated LangChain tools (search, calculator, code executor)
- Custom RAG-based document query using uploaded files
- Streaming support via SSE or WebSocket

### Frontend UI (Basic)

- User authentication (login/signup)
- Chat interface with conversation history
- File upload component
- Tool usage visual feedback

## Optional Enhancements

- WebSocket-based live chat interface

## PA-Agent Branching Structure

## Main Branches

- `main` - Stable, production-ready branch.

## Feature Branches (Per Collaborator)

Each collaborator works on their respective feature branches:

- `feature/authentication` - OAuth2.0, JWT, and user management.
- `feature/chat-memory` - Multi-turn conversation and memory integration.
- `feature/file-processing` - Document uploads, search, embeddings.
- `feature/frontend-ui` - User interface updates and chat interface.
- `feature/langchain-tools` - Web search, calculator, code executor.

## Workflow Example

1. Create feature branches from `main` and work on new features.
2. Submit pull requests (PRs) to merge changes back into `main`.
