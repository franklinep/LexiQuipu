export interface SourceDocument {
    id: string;
    text: string;
    metadata: Record<string, any>;
    distance: number;
  }
  
  export type MessageRole = 'user' | 'assistant';
  
  export interface ChatMessage {
    id: string;
    role: MessageRole;
    content: string;
    isLoading?: boolean;
    sources?: SourceDocument[];
  }