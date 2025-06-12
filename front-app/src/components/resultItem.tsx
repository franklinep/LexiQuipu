import React from 'react';
import { SearchResult } from '../api/search';

const ResultItem: React.FC<{ result: SearchResult }> = ({ result }) => (
  <li className="bg-white p-3 rounded shadow">
    <p className="font-semibold">{result.text}</p>
    <p className="text-sm text-gray-600">Distancia: {result.distance.toFixed(2)}</p>
  </li>
);

export default ResultItem;
