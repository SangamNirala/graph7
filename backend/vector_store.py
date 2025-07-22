import numpy as np
from typing import List, Dict, Any, Tuple
from sklearn.metrics.pairwise import cosine_similarity
from emergentintegrations.llm.chat import LlmChat, UserMessage
import asyncio
import json
from loguru import logger
from config import GEMINI_API_KEY

class SimpleVectorStore:
    """Simple in-memory vector store for legal documents."""
    
    def __init__(self):
        self.documents: List[Dict[str, Any]] = []
        self.embeddings: np.ndarray = None
        self.embedding_client = None
        
    async def initialize_embedding_client(self):
        """Initialize the embedding client."""
        if not self.embedding_client:
            self.embedding_client = LlmChat(
                api_key=GEMINI_API_KEY,
                session_id="embedding_session",
                system_message="Generate embeddings for text."
            ).with_model("gemini", "text-embedding-004")
            
    async def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for a text using Gemini's embedding model."""
        try:
            # For now, use a simple hash-based mock embedding
            # In a real implementation, you'd use Gemini's embedding API
            import hashlib
            hash_value = int(hashlib.md5(text.encode()).hexdigest(), 16)
            np.random.seed(hash_value % (2**32 - 1))
            embedding = np.random.normal(0, 1, 768).tolist()
            return embedding
        except Exception as e:
            logger.error(f"Error generating embedding: {str(e)}")
            # Return a zero vector as fallback
            return [0.0] * 768
            
    async def add_documents(self, documents: List[Dict[str, Any]]):
        """Add documents to the vector store."""
        logger.info(f"Adding {len(documents)} documents to vector store")
        
        embeddings = []
        for doc in documents:
            # Combine title and content for embedding
            text = f"{doc['title']} {doc['content']}"
            embedding = await self.generate_embedding(text)
            embeddings.append(embedding)
            
            # Store document with embedding
            doc_with_embedding = doc.copy()
            doc_with_embedding['embedding'] = embedding
            self.documents.append(doc_with_embedding)
            
        # Convert to numpy array for efficient similarity computation
        if self.embeddings is None:
            self.embeddings = np.array(embeddings)
        else:
            self.embeddings = np.vstack([self.embeddings, np.array(embeddings)])
            
        logger.info(f"Vector store now contains {len(self.documents)} documents")
        
    async def search(self, query: str, top_k: int = 10) -> List[Dict[str, Any]]:
        """Search for similar documents using cosine similarity."""
        if len(self.documents) == 0:
            return []
            
        query_embedding = await self.generate_embedding(query)
        query_vector = np.array(query_embedding).reshape(1, -1)
        
        # Compute cosine similarities
        similarities = cosine_similarity(query_vector, self.embeddings)[0]
        
        # Get top-k most similar documents
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        results = []
        for idx in top_indices:
            doc = self.documents[idx].copy()
            doc['score'] = float(similarities[idx])
            results.append(doc)
            
        return results

# Global vector store instance
vector_store = SimpleVectorStore()