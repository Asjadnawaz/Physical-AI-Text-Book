import React, { useState, useEffect } from 'react';
import ChatWindow from './ChatWindow';
import ChatInput from './ChatInput';
import './ChatBot.css';

const ChatBot = ({ pageUrl }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  // Initialize chat session when component mounts
  useEffect(() => {
    const initializeSession = async () => {
      try {
        const response = await fetch('/api/v1/chat/start', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            page_url: pageUrl,
            user_context: {}
          })
        });

        const data = await response.json();
        localStorage.setItem('chatSessionId', data.session_id);
      } catch (error) {
        console.error('Error initializing chat session:', error);
      }
    };

    initializeSession();
  }, [pageUrl]);

  const sendMessage = async (content, selectedText = '') => {
    const sessionId = localStorage.getItem('chatSessionId');
    if (!sessionId) {
      console.error('No chat session found');
      return;
    }

    // Add user message to UI immediately
    const userMessage = {
      id: Date.now().toString(),
      role: 'user',
      content: content,
      timestamp: new Date().toISOString(),
      selectedText: selectedText
    };

    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);

    try {
      const response = await fetch(`/api/v1/chat/${sessionId}/message`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          content: content,
          selected_text: selectedText
        })
      });

      const data = await response.json();

      const botMessage = {
        id: Date.now().toString() + '-bot',
        role: 'assistant',
        content: data.response,
        timestamp: new Date().toISOString(),
        sources: data.sources
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      console.error('Error sending message:', error);

      // Add error message
      const errorMessage = {
        id: Date.now().toString() + '-error',
        role: 'assistant',
        content: 'Sorry, I encountered an error processing your message. Please try again.',
        timestamp: new Date().toISOString(),
        sources: []
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const toggleChat = () => {
    setIsOpen(!isOpen);
  };

  return (
    <div className="chatbot-container">
      {isOpen ? (
        <div className="chatbot-window">
          <div className="chatbot-header">
            <h3>Textbook Assistant</h3>
            <button className="chatbot-close" onClick={toggleChat}>
              ×
            </button>
          </div>
          <ChatWindow messages={messages} />
          <ChatInput
            onSendMessage={sendMessage}
            isLoading={isLoading}
          />
        </div>
      ) : (
        <button className="chatbot-toggle" onClick={toggleChat}>
          💬 Ask Textbook
        </button>
      )}
    </div>
  );
};

export default ChatBot;