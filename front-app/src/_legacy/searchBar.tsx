import React from 'react';

interface Props {
  query: string;
  onQueryChange: (value: string) => void;
  onSearch: () => void;
  loading: boolean;
}

const SearchBar: React.FC<Props> = ({ query, onQueryChange, onSearch, loading }) => (
  <div className="flex gap-2 mb-4">
    <input
      type="text"
      className="flex-1 p-2 border rounded"
      placeholder="Escribe tu consulta..."
      value={query}
      onChange={(e) => onQueryChange(e.target.value)}
    />
    <button
      onClick={onSearch}
      className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
      disabled={loading}
    >
      {loading ? 'Buscando...' : 'Buscar'}
    </button>
  </div>
);

export default SearchBar;
