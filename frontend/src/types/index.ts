export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  timestamp?: string;
}

export interface ChatSession {
  session_id: string;
  messages: ChatMessage[];
  created_at?: string;
  updated_at?: string;
}

export interface QueryRequest {
  message: string;
  session_id?: string;
}

export interface QueryResponse {
  response: string;
  session_id: string;
  sources: string[];
}

export interface HealthResponse {
  status: string;
  message: string;
  timestamp: string;
}