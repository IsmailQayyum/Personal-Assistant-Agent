# PA-Agent

**PA-Agent** is a secure, agentic AI chatbot built using FastAPI, LangChain, and OAuth2.0. It follows clean architecture principles, modular design, and integrates production-ready DevOps practices.

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

## Branch Structure
PA-Agent/
│── main/                 # Stable, production-ready branch
│── develop/              # Integration branch for new features
│── feature/              # Feature branches for development
│   ├── authentication/   # OAuth2.0, JWT, and user management
│   ├── chat-memory/      # Multi-turn conversation and memory integration
│   ├── file-processing/  # Document uploads, search, embeddings
│   ├── frontend-ui/      # User interface updates and chat interface
│   ├── langchain-tools/  # Web search, calculator, code executor
│── fix/                  # Bug fixes
│   ├── auth-token-bug/   # Example bug fix
│   ├── memory-issue/     # Fix conversation memory errors
│── hotfix/               # Urgent bug fixes
│   ├── jwt-security/     # Critical security patch
│── release/              # Versioned releases
│   ├── v1.0.0/           # First stable release
│── docs/                 # Documentation
│   ├── api-reference/    # API and endpoints
│   ├── setup-guide/      # Installation and deployment guide

