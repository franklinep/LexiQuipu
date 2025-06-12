import React from 'react';
import { SearchResult } from '../api/search';

const ResultItem: React.FC<{ result: SearchResult }> = ({ result }) => (
  <li className="bg-white p-4 rounded-lg shadow border border-gray-200 mb-4">
    <div className="mb-2">
      <span className="font-bold text-sm text-gray-800">
        Casación N°: {result.metadata.n_casacion || 'N/A'}
      </span>
      <span className="mx-2 text-gray-400">|</span>
      <span className="text-sm text-gray-600">
        Lugar: {result.metadata.lugar || 'N/A'}
      </span>
    </div>
    <p className="text-gray-700 leading-relaxed">
      {result.text}
    </p>
    <p className="text-sm text-blue-500 mt-3 font-medium">
      Relevancia (Distancia): {result.distance.toFixed(4)}
    </p>
  </li>
);

export default ResultItem;