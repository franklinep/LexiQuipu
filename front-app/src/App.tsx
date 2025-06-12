// src/App.tsx

import { useState } from 'react';
import { searchJurisprudencia, SearchResult } from './api/search';
import SearchBar from './components/searchBar';
import ResultsList from './components/resultList';
import GeneratedAnswer from './components/GeneratedAnswer'; 

function App() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<SearchResult[]>([]);
  const [generatedAnswer, setGeneratedAnswer] = useState(''); // Estado para la respuesta de IA
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSearch = async () => {
    if (!query.trim()) return;
    
    setLoading(true);
    setError('');
    setGeneratedAnswer('');
    setResults([]);

    try {
      const data = await searchJurisprudencia(query, 5);
      setGeneratedAnswer(data.generated_answer); 
      setResults(data.source_documents);      
    } catch (err) {
      setError('Error al buscar. Verifica que la API esté activa.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4">
      <div className="max-w-4xl mx-auto">
        <header className="text-center mb-10">
            <h1 className="text-4xl font-extrabold text-gray-800 tracking-tight">Buscador de Jurisprudencia</h1>
            <p className="text-lg text-gray-600 mt-2">Potenciado por Inteligencia Artificial</p>
        </header>

        <main>
          <SearchBar
            query={query}
            onQueryChange={setQuery}
            onSearch={handleSearch}
            loading={loading}
          />

          {error && <p className="text-red-500 text-center my-4">{error}</p>}
          
          {loading && <p className="text-center text-gray-500 my-4">Buscando y generando respuesta...</p>}

          <GeneratedAnswer answer={generatedAnswer} />
          
          {results.length > 0 && (
            <div>
              <h2 className="text-2xl font-bold mb-4 text-gray-700">Documentos Fuente</h2>
              <ResultsList results={results} />
            </div>
          )}
        </main>
      </div>
    </div>
  );
}

export default App;