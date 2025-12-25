/**
 * Service for managing chat session data in browser storage
 */

class SessionStorageService {
  constructor() {
    this.storage = typeof window !== 'undefined' ? window.localStorage : null;
    this.sessionKey = 'chatbot-session';
    this.historyKey = 'chatbot-history-';
  }

  // Store session ID
  setSessionId(sessionId) {
    if (this.storage) {
      this.storage.setItem(this.sessionKey, sessionId);
    }
  }

  // Get session ID
  getSessionId() {
    if (this.storage) {
      return this.storage.getItem(this.sessionKey);
    }
    return null;
  }

  // Clear session ID
  clearSessionId() {
    if (this.storage) {
      this.storage.removeItem(this.sessionKey);
    }
  }

  // Store chat history for a session
  setChatHistory(sessionId, messages) {
    if (this.storage && sessionId) {
      const key = this.historyKey + sessionId;
      this.storage.setItem(key, JSON.stringify(messages));
    }
  }

  // Get chat history for a session
  getChatHistory(sessionId) {
    if (this.storage && sessionId) {
      const key = this.historyKey + sessionId;
      const history = this.storage.getItem(key);
      return history ? JSON.parse(history) : [];
    }
    return [];
  }

  // Clear chat history for a session
  clearChatHistory(sessionId) {
    if (this.storage && sessionId) {
      const key = this.historyKey + sessionId;
      this.storage.removeItem(key);
    }
  }

  // Clear all chat data
  clearAllChatData() {
    if (this.storage) {
      // Remove session ID
      this.storage.removeItem(this.sessionKey);

      // Remove all history entries
      const keysToRemove = [];
      for (let i = 0; i < this.storage.length; i++) {
        const key = this.storage.key(i);
        if (key && key.startsWith(this.historyKey)) {
          keysToRemove.push(key);
        }
      }

      keysToRemove.forEach(key => this.storage.removeItem(key));
    }
  }

  // Get all available session IDs
  getAvailableSessions() {
    if (this.storage) {
      const sessions = [];
      for (let i = 0; i < this.storage.length; i++) {
        const key = this.storage.key(i);
        if (key && key.startsWith(this.historyKey)) {
          const sessionId = key.replace(this.historyKey, '');
          sessions.push(sessionId);
        }
      }
      return sessions;
    }
    return [];
  }
}

const sessionStorageService = new SessionStorageService();
export default sessionStorageService;