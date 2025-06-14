import React, { useEffect, useRef } from 'react';
import { ChatMessage as ChatMessageType } from '../types/chat';
import Message from './Message';

interface Props {
  messages: ChatMessageType[];
}

const MessageList: React.FC<Props> = ({ messages }) => {
    const endOfMessagesRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        endOfMessagesRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [messages]);

    return (
        <div className="flex-1 overflow-y-auto p-6">
            <div className="max-w-3xl mx-auto">
                {messages.map((msg) => (
                    <Message key={msg.id} message={msg} />
                ))}

                <div ref={endOfMessagesRef} />
            </div>
        </div>
    );
};

export default MessageList;