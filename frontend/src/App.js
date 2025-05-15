import React from 'react';
import ChatBot from './ChatBot';
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Mental Health FAQ Chatbot</h1>
      </header>
      <main>
        <ChatBot />
      </main>
      <footer>
        <p className="disclaimer">
          This chatbot provides information only and is not a substitute for professional medical advice, 
          diagnosis, or treatment. If you're in crisis, please contact a mental health professional, 
          call a crisis hotline, or go to your nearest emergency room.
        </p>
      </footer>
    </div>
  );
}

export default App;
