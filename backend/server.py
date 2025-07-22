from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import asyncio
from typing import List
import uuid
from datetime import datetime
from loguru import logger

from models import QueryRequest, QueryResponse, ChatSession, ChatMessage, HealthResponse
from database import connect_to_mongo, close_mongo_connection, get_database
from vector_store import vector_store
from legal_data import SAMPLE_LEGAL_DOCUMENTS
from rag_service import RAGService
from config import load_config


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting LegaBot backend...")
    await connect_to_mongo()
    
    # Initialize vector store with legal documents
    await vector_store.add_documents(SAMPLE_LEGAL_DOCUMENTS)
    logger.info("Vector store initialized with legal documents")
    
    yield
    
    # Shutdown
    logger.info("Shutting down LegaBot backend...")
    await close_mongo_connection()

app = FastAPI(
    title="LegaBot API", 
    description="Legal Assistant RAG API",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize RAG service
rag_service = RAGService()

@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        message="LegaBot API is running successfully"
    )

@app.post("/api/chat", response_model=QueryResponse)
async def chat_with_bot(request: QueryRequest):
    """Main chat endpoint for legal queries."""
    try:
        # Generate or use provided session ID
        session_id = request.session_id or str(uuid.uuid4())
        
        # Get response from RAG service
        response = await rag_service.generate_response(
            query=request.message,
            session_id=session_id
        )
        
        # Save conversation to database
        await save_chat_message(session_id, "user", request.message)
        await save_chat_message(session_id, "assistant", response["response"])
        
        return QueryResponse(
            response=response["response"],
            session_id=session_id,
            sources=response["sources"]
        )
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/api/chat/{session_id}", response_model=ChatSession)
async def get_chat_history(session_id: str):
    """Get chat history for a session."""
    try:
        db = get_database()
        session_data = await db.chat_sessions.find_one({"session_id": session_id})
        
        if not session_data:
            return ChatSession(session_id=session_id)
            
        return ChatSession(**session_data)
        
    except Exception as e:
        logger.error(f"Error getting chat history: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve chat history")

@app.delete("/api/chat/{session_id}")
async def clear_chat_history(session_id: str):
    """Clear chat history for a session."""
    try:
        db = get_database()
        result = await db.chat_sessions.delete_one({"session_id": session_id})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Session not found")
            
        return {"message": "Chat history cleared successfully"}
        
    except Exception as e:
        logger.error(f"Error clearing chat history: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to clear chat history")

@app.get("/api/suggestions")
async def get_query_suggestions():
    """Get sample query suggestions."""
    from legal_prompts import QUERY_SUGGESTIONS
    return {"suggestions": QUERY_SUGGESTIONS}

async def save_chat_message(session_id: str, role: str, content: str):
    """Save a chat message to the database."""
    try:
        db = get_database()
        message = ChatMessage(role=role, content=content)
        
        # Update or create session
        await db.chat_sessions.update_one(
            {"session_id": session_id},
            {
                "$push": {"messages": message.model_dump()},
                "$set": {"updated_at": datetime.utcnow()},
                "$setOnInsert": {"created_at": datetime.utcnow()}
            },
            upsert=True
        )
    except Exception as e:
        logger.error(f"Error saving chat message: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)