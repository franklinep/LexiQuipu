import React from 'react';
import { SearchResult } from '../api/search';
import ResultItem from './resultItem';

const ResultsList: React.FC<{ results: SearchResult[] }> = ({ results }) => (
  <ul className="space-y-2">
    {results.map((res) => (
      <ResultItem key={res.id} result={res} />
    ))}
  </ul>
);

export default ResultsList;
