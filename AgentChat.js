// frontend/src/components/AgentChat.js
import React, { useState, useEffect, useRef } from 'react';
import { useEvent } from '../context/EventContext';

function AgentChat() {
  const [input, setInput] = useState('');
  const { messages, addMessage, setIsLoading, isLoading, updateCurrentEvent } = useEvent();
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async () => {
    if (input.trim() === '' || isLoading) return;

    addMessage('user', input);
    setIsLoading(true);
    setInput('');

    try {
      const backendUrl = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8000';
      const response = await fetch(`${backendUrl}/api/agent/plan_event`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: input }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to get a plan from the AI agent.');
      }

      const data = await response.json();
      // A more conversational response from the agent
      addMessage('agent', `I have created a new event plan for you based on your request. You can see the details on the dashboard.`);
      updateCurrentEvent(data);
    } catch (error) {
      console.error("Error communicating with AI agent:", error);
      addMessage('agent', `I'm sorry, I encountered an error: ${error.message}`);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="agent-chat">
      <h2>AI Assistant</h2>
      <div className="messages">
        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.sender}`}>
            {msg.text}
          </div>
        ))}
        {isLoading && <div className="typing-indicator">Agent is typing...</div>}
        <div ref={messagesEndRef} />
      </div>
      <div className="input-area">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
          placeholder="Chat with your AI planner..."
          disabled={isLoading}
        />
        <button onClick={handleSendMessage} disabled={isLoading}>
          Send
        </button>
      </div>
    </div>
  );
}

export default AgentChat;