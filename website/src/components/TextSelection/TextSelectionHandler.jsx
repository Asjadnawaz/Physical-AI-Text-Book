import React, { useEffect } from 'react';

const TextSelectionHandler = ({ onTextSelected }) => {
  useEffect(() => {
    const handleSelection = () => {
      const selected = window.getSelection().toString().trim();
      if (selected) {
        // Dispatch a custom event that can be listened to by the ChatInput component
        const event = new CustomEvent('textSelected', {
          detail: { selectedText: selected }
        });
        document.dispatchEvent(event);

        // Call the prop callback if provided
        if (onTextSelected) {
          onTextSelected(selected);
        }
      }
    };

    document.addEventListener('mouseup', handleSelection);
    document.addEventListener('touchend', handleSelection);

    return () => {
      document.removeEventListener('mouseup', handleSelection);
      document.removeEventListener('touchend', handleSelection);
    };
  }, [onTextSelected]);

  return null; // This component doesn't render anything visible
};

export default TextSelectionHandler;