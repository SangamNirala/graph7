import React, { useEffect, useState } from 'react';
import { MessageSquare, Lightbulb, AlertTriangle, Trash2 } from 'lucide-react';
import { apiService } from '../services/api';

interface SidebarProps {
  sessionId?: string;
  onClearChat: () => void;
  onSuggestionClick: (suggestion: string) => void;
}

export const Sidebar: React.FC<SidebarProps> = ({ 
  sessionId, 
  onClearChat, 
  onSuggestionClick 
}) => {
  const [suggestions, setSuggestions] = useState<string[]>([]);

  useEffect(() => {
    const loadSuggestions = async () => {
      try {
        const data = await apiService.getQuerySuggestions();
        setSuggestions(data.suggestions);
      } catch (error) {
        console.error('Failed to load suggestions:', error);
      }
    };

    loadSuggestions();
  }, []);

  const handleClearChat = async () => {
    if (sessionId) {
      try {
        await apiService.clearChatHistory(sessionId);
        onClearChat();
      } catch (error) {
        console.error('Failed to clear chat:', error);
      }
    }
  };

  return (
    <div className="w-80 bg-white border-r border-gray-200 h-full flex flex-col">
      {/* Header */}
      <div className="p-4 border-b border-gray-200">
        <div className="flex items-center gap-2 mb-2">
          <MessageSquare className="text-primary-500" size={20} />
          <h1 className="text-lg font-semibold text-gray-800">LegaBot</h1>
        </div>
        <p className="text-sm text-gray-600">
          Your Serbian Legal Assistant
        </p>
      </div>

      {/* Clear Chat Button */}
      {sessionId && (
        <div className="p-4 border-b border-gray-200">
          <button
            onClick={handleClearChat}
            className="w-full btn-secondary flex items-center gap-2 justify-center"
          >
            <Trash2 size={16} />
            Clear Chat
          </button>
        </div>
      )}

      {/* Query Suggestions */}
      <div className="flex-1 p-4">
        <div className="mb-6">
          <div className="flex items-center gap-2 mb-3">
            <Lightbulb className="text-yellow-500" size={16} />
            <h3 className="font-medium text-gray-800">Query Suggestions</h3>
          </div>
          <div className="space-y-2 max-h-64 overflow-y-auto">
            {suggestions.map((suggestion, index) => (
              <button
                key={index}
                onClick={() => onSuggestionClick(suggestion)}
                className="w-full text-left p-2 text-sm text-gray-600 hover:bg-gray-50 rounded border border-gray-200 hover:border-primary-200 transition-colors"
              >
                {suggestion}
              </button>
            ))}
          </div>
        </div>

        {/* Warning */}
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-3">
          <div className="flex items-start gap-2">
            <AlertTriangle className="text-yellow-600 flex-shrink-0 mt-0.5" size={16} />
            <div>
              <h4 className="font-medium text-yellow-800 text-sm">Important Notice</h4>
              <p className="text-xs text-yellow-700 mt-1">
                Please note that LegaBot may make mistakes. For critical legal information, 
                always verify with a qualified legal professional. LegaBot is here to assist, 
                not replace professional legal advice.
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Footer */}
      <div className="p-4 border-t border-gray-200">
        <p className="text-xs text-gray-500">
          Built with ❤️ for legal assistance
        </p>
      </div>
    </div>
  );
};