// frontend/src/context/EventContext.js
import React, { createContext, useState, useContext } from 'react';

const EventContext = createContext();

export const EventProvider = ({ children }) => {
  const [currentEvent, setCurrentEvent] = useState(null);
  const [messages, setMessages] = useState([
    {
      sender: 'agent',
      text: 'Hello! How can I help you plan your event today? Try something like, "I want to plan a wedding for 100 people in New York."'
    }
  ]);
  const [isLoading, setIsLoading] = useState(false);

  const addMessage = (sender, text) => {
    setMessages((prevMessages) => [...prevMessages, { sender, text, timestamp: new Date() }]);
  };

  const updateCurrentEvent = (eventPlan) => {
    setCurrentEvent(eventPlan);
  };

  return (
    <EventContext.Provider value={{
      currentEvent,
      messages,
      addMessage,
      isLoading,
      setIsLoading,
      updateCurrentEvent
    }}>
      {children}
    </EventContext.Provider>
  );
};

export const useEvent = () => useContext(EventContext);