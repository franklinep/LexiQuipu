import React from 'react';
import { ChatMessage, SourceDocument } from '../types/chat';
import { FaUser, FaRobot } from 'react-icons/fa';
import ReactMarkdown from 'react-markdown';
import { motion } from 'framer-motion';

// --- Componente para la burbuja de usuario ---
const UserMessage: React.FC<{ message: ChatMessage }> = ({ message }) => (
    <div className="flex items-start gap-4 justify-end">
        <div className="bg-[#2a2a2d] rounded-2xl p-3 max-w-xl">
            <p className="text-white/90 whitespace-pre-wrap">{message.content}</p>
        </div>
        <div className="w-10 h-10 rounded-full bg-gray-700 flex items-center justify-center flex-shrink-0">
            <FaUser size={20} />
        </div>
    </div>
);


// --- Componente para el mensaje del Asistente (LexiQuipu) ---
const AssistantMessage: React.FC<{ message: ChatMessage }> = ({ message }) => {
    // Determina el texto del encabezado de la burbuja de fuentes
    const hasSources = message.sources && message.sources.length > 0;
    const sourcesHeader = hasSources ? `LexiQuipu encontró ${message.sources!.length} documentos:` : "LexiQuipu está buscando...";

    return (
        <div className="flex items-start gap-4">
            <div className="w-10 h-10 rounded-full bg-gray-700 flex items-center justify-center flex-shrink-0 text-white/90">
                <FaRobot size={20} />
            </div>
            
            <div className="flex flex-col w-full max-w-3xl">
                {/* --- Burbuja de Pensamiento/Fuentes (Siempre visible durante la respuesta) --- */}
                {/* {message.isLoading && ( */}
                    <div className="bg-[#1e1f20] rounded-2xl p-4 mb-3">
                        <h4 className="text-sm font-semibold text-gray-300 mb-2">{sourcesHeader}</h4>
                        {hasSources && (
                             <div className="border-t border-gray-600 pt-3">
                                <ul className="space-y-1 max-h-32 overflow-y-auto">
                                    {message.sources!.map((source: SourceDocument) => (
                                        <li key={source.id} className="text-xs text-gray-400 truncate" title={source.metadata.file_name || 'Documento sin nombre'}>

                                            {source.metadata.file_name || 'Documento sin nombre'}
                                        </li>
                                    ))}
                                </ul>
                            </div>
                        )}
                    </div>
                {/* // )} */}
                
                {/* --- Contenido de la Respuesta (sin burbuja, aparece debajo) --- */}
                <div className="text-white/90">
                    <article className="prose prose-invert prose-p:my-2 prose-headings:my-3">
                        <ReactMarkdown>{message.content}</ReactMarkdown>
                    </article>
                </div>
            </div>
        </div>
    );
};


// --- Componente Principal que decide cuál mostrar ---
const Message: React.FC<{ message: ChatMessage }> = ({ message }) => {
    return (
        <motion.div
            className="my-6 w-full"
            initial={{ opacity: 0, y: 15 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3 }}
        >
            {message.role === 'user' ? <UserMessage message={message} /> : <AssistantMessage message={message} />}
        </motion.div>
    );
};

export default Message;