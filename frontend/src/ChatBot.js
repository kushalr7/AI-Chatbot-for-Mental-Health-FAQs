import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import './ChatBot.css';

const ChatBot = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  // Scroll to bottom of messages
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Add initial bot message when component mounts
  useEffect(() => {
    setMessages([
      {
        sender: 'bot',
        text: 'Hi there! I can help answer questions about mental health. What would you like to know?',
        disclaimer: ''
      }
    ]);
  }, []);

  const handleInputChange = (e) => {
    setInput(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!input.trim()) return;
    
    // Add user message to chat
    const userMessage = {
      sender: 'user',
      text: input.trim()
    };
    
    setMessages(prev => [...prev, userMessage]);
    setInput(''); // Clear input field
    setIsLoading(true);
    
    try {
      // Send request to backend
      const response = await axios.post('http://localhost:5000/ask', {
        query: userMessage.text
      });
      
      // Add bot response to chat
      setMessages(prev => [
        ...prev,
        {
          sender: 'bot',
          text: response.data.response,
          disclaimer: response.data.disclaimer
        }
      ]);
    } catch (error) {
      console.error('Error fetching response:', error);
      setMessages(prev => [
        ...prev,
        {
          sender: 'bot',
          text: 'Sorry, I encountered an error processing your question. Please try again.',
          disclaimer: ''
        }
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="chatbot-container">
      <div className="messages-container">
        {messages.map((message, index) => (
          <div key={index} className={`message ${message.sender}`}>
            <div className="message-text">{message.text}</div>
            {message.disclaimer && (
              <div className="message-disclaimer">{message.disclaimer}</div>
            )}
          </div>
        ))}
        {isLoading && (
          <div className="loading-indicator">
            <div className="dot"></div>
            <div className="dot"></div>
            <div className="dot"></div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>
      
      <form className="input-form" onSubmit={handleSubmit}>
        <input
          type="text"
          value={input}
          onChange={handleInputChange}
          placeholder="Type your question here..."
          disabled={isLoading}
        />
        <button type="submit" disabled={isLoading}>
          {isLoading ? '...' : 'Send'}
        </button>
      </form>
    </div>
  );
};

export default ChatBot;
