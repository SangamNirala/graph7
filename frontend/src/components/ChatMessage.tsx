import React from 'react';
import { ChatMessage as ChatMessageType } from '../types';
import { User, Bot } from 'lucide-react';

interface ChatMessageProps {
  message: ChatMessageType;
  sources?: string[];
}

export const ChatMessage: React.FC<ChatMessageProps> = ({ message, sources }) => {
  const isUser = message.role === 'user';

  return (
    <div className={`chat-message ${isUser ? 'text-right' : 'text-left'}`}>
      <div className={`flex items-start gap-3 ${isUser ? 'flex-row-reverse' : ''}`}>
        <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${
          isUser ? 'bg-primary-500 text-white' : 'bg-gray-200 text-gray-600'
        }`}>
          {isUser ? <User size={16} /> : <Bot size={16} />}
        </div>
        
        <div className={`chat-bubble ${isUser ? 'user' : 'assistant'}`}>
          <div className="prose prose-sm max-w-none">
            {message.content.split('\n').map((line, index) => (
              <p key={index} className={index === 0 ? 'mt-0' : ''}>
                {line}
              </p>
            ))}
          </div>
          
          {!isUser && sources && sources.length > 0 && (
            <div className="mt-4 pt-3 border-t border-gray-100">
              <p className="text-xs text-gray-500 font-medium mb-2">Sources:</p>
              <div className="space-y-1">
                {sources.map((source, index) => (
                  <div key={index} className="text-xs text-gray-600">
                    <a 
                      href={source.split(' - ')[1]} 
                      target="_blank" 
                      rel="noopener noreferrer"
                      className="text-primary-500 hover:text-primary-600 underline"
                    >
                      {source.split(' - ')[0]}
                    </a>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};