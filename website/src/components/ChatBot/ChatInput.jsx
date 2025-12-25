import React, { useState, useEffect } from 'react';

const ChatInput = ({ onSendMessage, isLoading }) => {
  const [inputValue, setInputValue] = useState('');
  const [selectedText, setSelectedText] = useState('');

  // Listen for selected text from the TextSelectionHandler
  useEffect(() => {
    const handleTextSelection = (event) => {
      const text = event.detail.selectedText;
      if (text && text !== selectedText) {
        setSelectedText(text);
      }
    };

    document.addEventListener('textSelected', handleTextSelection);

    return () => {
      document.removeEventListener('textSelected', handleTextSelection);
    };
  }, [selectedText]);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (inputValue.trim() && !isLoading) {
      onSendMessage(inputValue.trim(), selectedText);
      setInputValue('');
      // Clear the selected text after sending
      setSelectedText('');
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  const handleClearSelection = () => {
    setSelectedText('');
  };

  return (
    <form className="chat-input-form" onSubmit={handleSubmit}>
      <div className="chat-input-container">
        {selectedText && (
          <div className="selected-text-preview">
            <small>Context: "{selectedText.substring(0, 60)}{selectedText.length > 60 ? '...' : ''}"</small>
            <button type="button" className="clear-selection-btn" onClick={handleClearSelection}>
              ×
            </button>
          </div>
        )}
        <textarea
          className="chat-input"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder={selectedText
            ? "Ask a question about the selected text..."
            : "Ask a question about the textbook content..."}
          disabled={isLoading}
          rows="1"
        />
        <button
          type="submit"
          className="chat-send-button"
          disabled={isLoading || !inputValue.trim()}
        >
          {isLoading ? 'Sending...' : 'Send'}
        </button>
      </div>
    </form>
  );
};

export default ChatInput;