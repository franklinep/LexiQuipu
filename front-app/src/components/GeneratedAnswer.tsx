import React from 'react';

interface Props {
  answer: string;
}

const GeneratedAnswer: React.FC<Props> = ({ answer }) => {
  if (!answer) return null;

  return (
    <div className="bg-blue-50 border-l-4 border-blue-500 text-blue-800 p-6 rounded-lg shadow-md mb-8">
      <h2 className="font-bold text-xl mb-2">Respuesta Generada por IA</h2>
      <p className="whitespace-pre-wrap leading-relaxed">{answer}</p>
    </div>
  );
};

export default GeneratedAnswer;