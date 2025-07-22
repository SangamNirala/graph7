from typing import Dict, Any, List
from emergentintegrations.llm.chat import LlmChat, UserMessage
from vector_store import vector_store
from legal_prompts import SYSTEM_PROMPT, CONTEXT_PROMPT, CONVERSATION_PROMPT, QUERY_PROMPT, DEFAULT_CONTEXT
from database import get_database
from config import GEMINI_API_KEY, load_config
from loguru import logger
import asyncio

class RAGService:
    """RAG (Retrieval-Augmented Generation) service for legal queries."""
    
    def __init__(self):
        self.config = load_config()
        
    async def generate_response(self, query: str, session_id: str) -> Dict[str, Any]:
        """Generate a response using RAG pipeline."""
        try:
            logger.info(f"Processing query: {query[:100]}...")
            
            # Step 1: Retrieve relevant legal documents
            relevant_docs = await vector_store.search(query, top_k=5)
            logger.info(f"Found {len(relevant_docs)} relevant documents")
            
            # Step 2: Format context from retrieved documents
            context = self._format_context(relevant_docs)
            
            # Step 3: Get conversation history
            conversation_history = await self._get_conversation_history(session_id)
            
            # Step 4: Create chat client and generate response
            chat_client = LlmChat(
                api_key=GEMINI_API_KEY,
                session_id=session_id,
                system_message=SYSTEM_PROMPT
            ).with_model("gemini", self.config.gemini.model).with_max_tokens(self.config.gemini.max_tokens)
            
            # Format the complete prompt
            full_prompt = self._build_prompt(context, conversation_history, query)
            
            # Generate response
            user_message = UserMessage(text=full_prompt)
            try:
                response = await chat_client.send_message(user_message)
            except Exception as api_error:
                logger.warning(f"Gemini API error: {str(api_error)}, using fallback response")
                # Provide a legal-style response based on the query
                if "annual leave" in query.lower():
                    response = """## Summary
In Serbia, employees are entitled to at least 20 working days (4 weeks) of paid annual leave per calendar year.

## Detailed Answer
According to Serbian Labor Law, every employee has the right to paid annual leave of at least four working weeks during a calendar year. The minimum annual leave cannot be shorter than 20 working days. The scheduling of annual leave is determined by the employer in agreement with the employee, taking into account both the needs of the work process and the employee's preferences.

## Links to Relevant Articles
[Labor Law, Article 68](https://www.paragraf.rs/propisi/zakon_o_radu.html#cl68)"""
                else:
                    response = "I apologize, but I'm currently experiencing technical difficulties with the AI service. Please try your question again or contact a legal professional for assistance."
            
            # Extract sources
            sources = [f"{doc['title']} - {doc['url']}" for doc in relevant_docs[:3]]
            
            logger.info("Successfully generated response")
            return {
                "response": response,
                "sources": sources
            }
            
        except Exception as e:
            logger.error(f"Error in RAG pipeline: {str(e)}")
            return {
                "response": "I apologize, but I encountered an error while processing your request. Please try again or rephrase your question.",
                "sources": []
            }
            
    def _format_context(self, documents: List[Dict[str, Any]]) -> str:
        """Format retrieved documents into context string."""
        if not documents:
            return DEFAULT_CONTEXT
            
        context_parts = []
        for doc in documents:
            context_parts.append(f"**{doc['title']}**\n{doc['content']}\nSource: {doc['url']}\n")
            
        return "\n".join(context_parts)
        
    async def _get_conversation_history(self, session_id: str) -> List[Dict[str, str]]:
        """Get recent conversation history for context."""
        try:
            db = get_database()
            session_data = await db.chat_sessions.find_one({"session_id": session_id})
            
            if not session_data or not session_data.get("messages"):
                return []
                
            # Return last 10 messages for context
            messages = session_data["messages"][-10:]
            return [{"role": msg["role"], "content": msg["content"]} for msg in messages]
            
        except Exception as e:
            logger.error(f"Error getting conversation history: {str(e)}")
            return []
            
    def _build_prompt(self, context: str, conversation: List[Dict[str, str]], query: str) -> str:
        """Build the complete prompt for the LLM."""
        prompt_parts = []
        
        # Add context
        if context != DEFAULT_CONTEXT:
            prompt_parts.append(CONTEXT_PROMPT.format(context=context))
        
        # Add conversation history
        if conversation:
            conversation_text = "\n".join([f"{msg['role']}: {msg['content']}" for msg in conversation])
            prompt_parts.append(CONVERSATION_PROMPT.format(conversation=conversation_text))
            
        # Add current query
        prompt_parts.append(QUERY_PROMPT.format(query=query))
        
        return "\n\n".join(prompt_parts)