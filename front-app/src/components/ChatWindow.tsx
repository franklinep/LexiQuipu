import React, { useState } from 'react';
import { ChatMessage } from '../types/chat';
import MessageList from './MessageList';
import PromptInput from './PromptInput';
import { streamChat } from '../api/chat'; 

const ChatWindow: React.FC = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  

  const handleSendMessage = (query: string) => {

    const historyToSend = messages.filter(msg => !msg.isLoading);

    const userMessage: ChatMessage = {
      id: `user-${Date.now()}`,
      role: 'user',
      content: query,
    };
    
    const assistantLoadingMessage: ChatMessage = {
      id: `assistant-${Date.now()}`,
      role: 'assistant',
      content: '', 
      isLoading: true,
    };

    setMessages((prevMessages) => [...prevMessages, userMessage, assistantLoadingMessage]);
    setIsLoading(true);

    streamChat(
      query,
      historyToSend,
      (sources) => {
        setMessages(prev => prev.map(msg => 
            msg.id === assistantLoadingMessage.id 
            ? { ...msg, sources: sources } 
            : msg
        ));
      },
      (token) => {
        setMessages(prev =>
          prev.map(msg =>
            msg.id === assistantLoadingMessage.id
              ? { ...msg, content: msg.content + token }
              : msg
          )
        );
      },
      () => {
        setMessages(prev =>
            prev.map(msg =>
              msg.id === assistantLoadingMessage.id
                ? { ...msg, isLoading: false }
                : msg
            )
          );
        setIsLoading(false);
      },
      (error) => {
        setMessages(prev =>
            prev.map(msg =>
              msg.id === assistantLoadingMessage.id
                ? { ...msg, content: `**Error:** ${error.message}`, isLoading: false }
                : msg
            )
          );
        setIsLoading(false);
      }
    );
  };

  return (
    <div className="flex flex-col h-screen bg-[#131314]">
        <header className="text-center p-3 border-b border-gray-700/50">
            <h1 className="text-2xl font-bold text-white/90">LexiQuipu</h1>
            <p className="text-sm text-gray-400/60">Tu Asistente Legal de Jurisprudencia Peruana</p>
        </header>
        <MessageList messages={messages} />
        <PromptInput onSubmit={handleSendMessage} isLoading={isLoading} />
    </div>
  );
};

export default ChatWindow;