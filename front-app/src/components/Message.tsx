
import React from 'react';
import { ChatMessage } from '../types/chat';
import { FaUser, FaRobot } from 'react-icons/fa';
import ReactMarkdown from 'react-markdown';

const Message: React.FC<{ message: ChatMessage }> = ({ message }) => {
  const isUser = message.role === 'user';

  const LoadingIndicator = () => (
    <div className="flex items-center space-x-2">
        <span className="font-bold">LexiQuipu está pensando</span>
        <div className="w-2 h-2 bg-blue-400 rounded-full animate-pulse [animation-delay:-0.3s]"></div>
        <div className="w-2 h-2 bg-blue-400 rounded-full animate-pulse [animation-delay:-0.15s]"></div>
        <div className="w-2 h-2 bg-blue-400 rounded-full animate-pulse"></div>
    </div>
  );

  return (
    <div className={`flex items-start gap-4 my-6 ${isUser ? 'justify-end' : ''}`}>
      {!isUser && (
        <div className="w-10 h-10 rounded-full bg-gray-700 flex items-center justify-center flex-shrink-0 text-white/90">
          <FaRobot size={20} />
        </div>
      )}

      <div className={`p-4 rounded-2xl max-w-2xl ${isUser ? 'bg-blue-600 rounded-br-none text-white/85' : 'bg-[#1e1f20] rounded-bl-none text-white/85'}`}>
        {/* {message.isLoading ? <LoadingIndicator /> : <p className="whitespace-pre-wrap">{message.content}</p>} */}
        <article className="prose prose-invert prose-p:my-0 prose-headings:my-2">
            <ReactMarkdown>{message.content}</ReactMarkdown>
        </article>
        {/* Documentos fuente */}
      </div>

       {isUser && (
        <div className="w-10 h-10 rounded-full bg-gray-700 flex items-center justify-center flex-shrink-0">
          <FaUser size={20} />
        </div>
      )}
    </div>
  );
};

export default Message;