/**
 * Text selection functionality for the RAG chatbot
 * Allows users to select text on the page and send it to the chatbot for contextual queries
 */

class TextSelectionManager {
  constructor() {
    this.selectedText = '';
    this.onTextSelectedCallback = null;

    this.init();
  }

  init() {
    // Add event listeners for text selection
    document.addEventListener('mouseup', this.handleSelection.bind(this));
    document.addEventListener('touchend', this.handleSelection.bind(this));
  }

  handleSelection() {
    // Get the selected text
    const selection = window.getSelection();
    const text = selection.toString().trim();

    if (text) {
      this.selectedText = text;

      // Trigger the callback if provided
      if (this.onTextSelectedCallback) {
        this.onTextSelectedCallback(text);
      }

      // Store in sessionStorage for persistence
      sessionStorage.setItem('chatbot-selected-text', text);
    } else {
      this.selectedText = '';
      sessionStorage.removeItem('chatbot-selected-text');
    }
  }

  getSelectedText() {
    return this.selectedText || sessionStorage.getItem('chatbot-selected-text') || '';
  }

  clearSelection() {
    this.selectedText = '';
    sessionStorage.removeItem('chatbot-selected-text');
    window.getSelection().removeAllRanges();
  }

  setOnTextSelected(callback) {
    this.onTextSelectedCallback = callback;
  }

  // Add visual feedback for selected text
  addVisualFeedback() {
    // Could add CSS classes or visual indicators here
    const selection = window.getSelection();
    if (selection.rangeCount > 0) {
      const range = selection.getRangeAt(0);
      const rect = range.getBoundingClientRect();

      // This could be used to add a special UI element near the selection
      console.log('Text selection at:', rect);
    }
  }
}

// Initialize the text selection manager when the DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  window.textSelectionManager = new TextSelectionManager();
});

// Export for use in other modules if needed
export default TextSelectionManager;