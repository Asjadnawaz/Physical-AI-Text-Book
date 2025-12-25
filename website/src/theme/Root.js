import React from 'react';
import ChatBot from '../components/ChatBot/ChatBot';

// Root component that wraps the entire Docusaurus application
function Root({ children }) {
  return (
    <>
      {children}
      <ChatBot pageUrl={typeof window !== 'undefined' ? window.location.href : ''} />
    </>
  );
}

export default Root;