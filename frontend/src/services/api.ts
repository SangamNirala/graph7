import axios from 'axios';
import { QueryRequest, QueryResponse, ChatSession, HealthResponse } from '../types';

const API_BASE_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const apiService = {
  // Health check
  async healthCheck(): Promise<HealthResponse> {
    const response = await api.get<HealthResponse>('/api/health');
    return response.data;
  },

  // Chat with the bot
  async chatWithBot(request: QueryRequest): Promise<QueryResponse> {
    const response = await api.post<QueryResponse>('/api/chat', request);
    return response.data;
  },

  // Get chat history
  async getChatHistory(sessionId: string): Promise<ChatSession> {
    const response = await api.get<ChatSession>(`/api/chat/${sessionId}`);
    return response.data;
  },

  // Clear chat history
  async clearChatHistory(sessionId: string): Promise<void> {
    await api.delete(`/api/chat/${sessionId}`);
  },

  // Get query suggestions
  async getQuerySuggestions(): Promise<{ suggestions: string[] }> {
    const response = await api.get('/api/suggestions');
    return response.data;
  },
};