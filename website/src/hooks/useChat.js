import { useState, useEffect } from 'react';
import chatApiService from '../services/chat-api';
import sessionStorageService from '../services/session-storage';

const useChat = (pageUrl) => {
  const [sessionId, setSessionId] = useState(null);
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  // Initialize chat session
  useEffect(() => {
    const initializeSession = async () => {
      try {
        // Try to get existing session from storage
        const storedSessionId = sessionStorageService.getSessionId();

        if (storedSessionId) {
          setSessionId(storedSessionId);
          // Load existing messages
          const history = sessionStorageService.getChatHistory(storedSessionId);
          setMessages(history);
        } else {
          // Create new session
          const sessionData = await chatApiService.startSession(pageUrl);
          setSessionId(sessionData.session_id);
          sessionStorageService.setSessionId(sessionData.session_id);
        }
      } catch (err) {
        setError(err.message);
        console.error('Error initializing chat:', err);
      }
    };

    initializeSession();
  }, [pageUrl]);

  // Save messages to storage whenever they change
  useEffect(() => {
    if (sessionId) {
      sessionStorageService.setChatHistory(sessionId, messages);
    }
  }, [messages, sessionId]);

  const sendMessage = async (content, selectedText = '') => {
    if (!sessionId || !content.trim()) return;

    setIsLoading(true);
    setError(null);

    try {
      // Add user message to UI immediately
      const userMessage = {
        id: Date.now().toString(),
        role: 'user',
        content: content,
        timestamp: new Date().toISOString(),
        selectedText: selectedText
      };

      setMessages(prev => [...prev, userMessage]);

      // Send message to API
      const response = await chatApiService.sendMessage(sessionId, content, selectedText);

      // Add bot response to UI
      const botMessage = {
        id: Date.now().toString() + '-bot',
        role: 'assistant',
        content: response.response,
        timestamp: new Date().toISOString(),
        sources: response.sources
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (err) {
      setError(err.message);
      console.error('Error sending message:', err);

      // Add error message to UI
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

  const clearChat = () => {
    setMessages([]);
    if (sessionId) {
      sessionStorageService.clearChatHistory(sessionId);
    }
  };

  const getHistory = async () => {
    if (!sessionId) return [];

    try {
      const historyData = await chatApiService.getChatHistory(sessionId);
      return historyData.messages || [];
    } catch (err) {
      console.error('Error getting chat history:', err);
      return [];
    }
  };

  return {
    sessionId,
    messages,
    isLoading,
    error,
    sendMessage,
    clearChat,
    getHistory
  };
};

export default useChat;