
import React, { useState } from 'react';
import { FiSend } from 'react-icons/fi';

interface Props {
  onSubmit: (query: string) => void;
  isLoading: boolean;
}

const PromptInput: React.FC<Props> = ({ onSubmit, isLoading }) => {
  const [query, setQuery] = useState('');

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (!query.trim() || isLoading) return;
    onSubmit(query);
    setQuery('');
  };

  return (
    <form onSubmit={handleSubmit} className="w-full max-w-3xl mx-auto px-4 py-1">
      <div className="relative">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Haz una pregunta a LexiQuipu..."
          className="w-full bg-[#1e1f20] border border-gray-600 rounded-full py-3 pl-6 pr-14 text-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all duration-300 text-white/80"
          disabled={isLoading}
        />
        <button
          type="submit"
          disabled={isLoading || !query.trim()}
          className="absolute right-3 top-1/2 -translate-y-1/2 p-2 rounded-full bg-blue-600 text-white hover:bg-blue-500 disabled:bg-gray-500 disabled:cursor-not-allowed transition-colors"
        >
          <FiSend size={20} />
        </button>
      </div>
    </form>
  );
};

export default PromptInput;