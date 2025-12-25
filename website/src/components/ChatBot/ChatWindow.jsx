import React from 'react';
import Message from './Message';

const ChatWindow = ({ messages }) => {
  const messagesEndRef = React.useRef(null);

  React.useEffect(() => {
    // Scroll to bottom when messages change
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  return (
    <div className="chat-window">
      {messages.length === 0 ? (
        <div className="chat-welcome">
          <p>Hello! I'm your textbook assistant. Ask me anything about the content on this page.</p>
          <p>I can help explain concepts, find relevant sections, and answer questions based on the textbook material.</p>
        </div>
      ) : (
        messages.map((message) => (
          <Message key={message.id} message={message} />
        ))
      )}
      <div ref={messagesEndRef} />
    </div>
  );
};

export default ChatWindow;