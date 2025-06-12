import { useState } from 'react';
import { searchJurisprudencia, SearchResult } from './api/search';
import SearchBar from './components/searchBar';
import ResultsList from './components/resultList';

function App() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<SearchResult[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSearch = async () => {
    setLoading(true);
    setError('');
    try {
      const data = await searchJurisprudencia(query, 5);
      setResults(data);
    } catch (err) {
      setError('Error al buscar. Verifica que la API esté activa.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 p-4">
      <div className="max-w-xl mx-auto">
        <h1 className="text-2xl font-bold mb-4 text-center text-blue-700">
          Búsqueda de Jurisprudencia
        </h1>

        <SearchBar
          query={query}
          onQueryChange={setQuery}
          onSearch={handleSearch}
          loading={loading}
        />

        {error && <p className="text-red-500 text-center mb-4">{error}</p>}

        <ResultsList results={results} />
      </div>
    </div>
  );
}

export default App;
