import React from 'react';

const Message = ({ message }) => {
  const isUser = message.role === 'user';

  return (
    <div className={`message ${isUser ? 'user-message' : 'bot-message'}`}>
      <div className="message-content">
        {message.content}
      </div>
      {message.sources && message.sources.length > 0 && (
        <div className="message-sources">
          <small>Sources: {message.sources.slice(0, 2).join(', ')}</small>
        </div>
      )}
      {message.selectedText && (
        <div className="message-context">
          <small>Context: "{message.selectedText}"</small>
        </div>
      )}
      <div className="message-timestamp">
        {new Date(message.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
      </div>
    </div>
  );
};

export default Message;