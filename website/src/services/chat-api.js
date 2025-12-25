/**
 * API service for chatbot functionality
 */

class ChatApiService {
  constructor() {
    this.baseUrl = process.env.CHATBOT_API_URL || '/api/v1';
  }

  async startSession(pageUrl = '', userContext = {}) {
    try {
      const response = await fetch(`${this.baseUrl}/chat/start`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          page_url: pageUrl,
          user_context: userContext
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error starting chat session:', error);
      throw error;
    }
  }

  async sendMessage(sessionId, content, selectedText = '') {
    try {
      const response = await fetch(`${this.baseUrl}/chat/${sessionId}/message`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          content: content,
          selected_text: selectedText
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error sending message:', error);
      throw error;
    }
  }

  async getChatHistory(sessionId) {
    try {
      const response = await fetch(`${this.baseUrl}/chat/${sessionId}/history`);

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error getting chat history:', error);
      throw error;
    }
  }

  async performSearch(query, maxResults = 5) {
    try {
      const response = await fetch(`${this.baseUrl}/search`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: query,
          max_results: maxResults
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error performing search:', error);
      throw error;
    }
  }
}

const chatApiService = new ChatApiService();
export default chatApiService;