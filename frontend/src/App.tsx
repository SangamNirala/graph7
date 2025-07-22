import React, { useState, useEffect, useRef } from 'react';
import { ChatMessage as ChatMessageComponent } from './components/ChatMessage';
import { ChatInput } from './components/ChatInput';
import { Sidebar } from './components/Sidebar';
import { LoadingSpinner } from './components/LoadingSpinner';
import { ChatMessage, QueryResponse } from './types';
import { apiService } from './services/api';
import { AlertCircle } from 'lucide-react';

function App() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId, setSessionId] = useState<string>('');
  const [error, setError] = useState<string>('');
  const [isBackendReady, setIsBackendReady] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const [messageSources, setMessageSources] = useState<{ [key: number]: string[] }>({});

  // Scroll to bottom of messages
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Check backend health on component mount
  useEffect(() => {
    const checkBackend = async () => {
      try {
        await apiService.healthCheck();
        setIsBackendReady(true);
        
        // Add welcome message
        setMessages([{
          role: 'assistant',
          content: `Hello! I am a legal assistant, and my task is to help you understand procedures and answer questions related to the following Serbian regulations:
- Labor Law
- Personal Income Tax Law
- Personal Data Protection Law
- Consumer Protection Law
- Family Law

My role is to facilitate your understanding of legal procedures and provide you with useful and accurate information.

How can I assist you?`
        }]);
        
      } catch (error) {
        console.error('Backend not ready:', error);
        setError('Unable to connect to the backend. Please make sure the server is running.');
      }
    };

    checkBackend();
  }, []);

  const handleSendMessage = async (messageText: string) => {
    if (!messageText.trim() || isLoading) return;

    setError('');
    setIsLoading(true);

    // Add user message
    const userMessage: ChatMessage = {
      role: 'user',
      content: messageText
    };
    setMessages(prev => [...prev, userMessage]);

    try {
      const response: QueryResponse = await apiService.chatWithBot({
        message: messageText,
        session_id: sessionId || undefined
      });

      // Add assistant response
      const assistantMessage: ChatMessage = {
        role: 'assistant',
        content: response.response
      };
      
      setMessages(prev => [...prev, assistantMessage]);
      
      // Store sources for this message
      if (response.sources && response.sources.length > 0) {
        setMessageSources(prev => ({
          ...prev,
          [messages.length + 1]: response.sources
        }));
      }
      
      // Set session ID if not already set
      if (!sessionId && response.session_id) {
        setSessionId(response.session_id);
      }

    } catch (error: any) {
      console.error('Error sending message:', error);
      const errorMessage = error.response?.data?.detail || 'Sorry, I encountered an error while processing your request. Please try again.';
      setError(errorMessage);
      
      // Add error message to chat
      const errorChatMessage: ChatMessage = {
        role: 'assistant',
        content: 'Sorry, I encountered an error while processing your request. Please try again.'
      };
      setMessages(prev => [...prev, errorChatMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleClearChat = () => {
    setMessages([{
      role: 'assistant',
      content: `Hello! I am a legal assistant, and my task is to help you understand procedures and answer questions related to the following Serbian regulations:
- Labor Law
- Personal Income Tax Law
- Personal Data Protection Law
- Consumer Protection Law
- Family Law

My role is to facilitate your understanding of legal procedures and provide you with useful and accurate information.

How can I assist you?`
    }]);
    setSessionId('');
    setMessageSources({});
    setError('');
  };

  const handleSuggestionClick = (suggestion: string) => {
    handleSendMessage(suggestion);
  };

  if (!isBackendReady && !error) {
    return (
      <div className="h-screen flex items-center justify-center">
        <LoadingSpinner />
      </div>
    );
  }

  return (
    <div className="h-screen flex bg-gray-50">
      {/* Sidebar */}
      <Sidebar
        sessionId={sessionId}
        onClearChat={handleClearChat}
        onSuggestionClick={handleSuggestionClick}
      />

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col">
        {/* Error Banner */}
        {error && (
          <div className="bg-red-50 border-l-4 border-red-400 p-4">
            <div className="flex items-center">
              <AlertCircle className="text-red-400 mr-2" size={16} />
              <p className="text-red-700 text-sm">{error}</p>
            </div>
          </div>
        )}

        {/* Messages Area */}
        <div className="flex-1 overflow-y-auto">
          {messages.length === 0 ? (
            <div className="h-full flex items-center justify-center">
              <div className="text-center">
                <h2 className="text-xl font-semibold text-gray-800 mb-2">
                  Welcome to LegaBot
                </h2>
                <p className="text-gray-600">
                  Your Serbian Legal Assistant is ready to help!
                </p>
              </div>
            </div>
          ) : (
            <div className="py-4">
              {messages.map((message, index) => (
                <ChatMessageComponent
                  key={index}
                  message={message}
                  sources={messageSources[index]}
                />
              ))}
              {isLoading && (
                <div className="chat-message">
                  <div className="flex items-start gap-3">
                    <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gray-200 text-gray-600 flex items-center justify-center">
                      <div className="w-3 h-3 bg-gray-400 rounded-full animate-pulse"></div>
                    </div>
                    <div className="chat-bubble assistant">
                      <div className="flex items-center gap-2">
                        <div className="flex space-x-1">
                          <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                          <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                          <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                        </div>
                        <span className="text-gray-500 text-sm">Thinking...</span>
                      </div>
                    </div>
                  </div>
                </div>
              )}
              <div ref={messagesEndRef} />
            </div>
          )}
        </div>

        {/* Input Area */}
        <ChatInput
          onSendMessage={handleSendMessage}
          isLoading={isLoading}
          disabled={!isBackendReady}
        />
      </div>
    </div>
  );
}

export default App;