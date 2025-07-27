// frontend/src/components/EventOverview.js
import React from 'react';
import { useEvent } from '../context/EventContext';

function EventOverview() {
  const { currentEvent } = useEvent();

  if (!currentEvent) {
    return (
      <div className="dashboard-panel event-overview">
        <h2>Event Overview</h2>
        <p className="placeholder-text">Your event details will appear here once you chat with the AI assistant.</p>
      </div>
    );
  }

  // Helper to format numbers as Indian currency
  const formatAsINR = (num) => {
    return num.toLocaleString('en-IN');
  };

  return (
    <div className="dashboard-panel event-overview">
      <h2>{currentEvent.event_name || 'Event Overview'}</h2>
      <ul>
        <li><strong>Event Type:</strong> {currentEvent.event_type}</li>
        <li><strong>Date:</strong> {currentEvent.event_date}</li>
        <li><strong>Guests:</strong> {currentEvent.number_of_guests}</li>
        {/* Switched from $ to ₹ and used en-IN formatting */}
        <li><strong>Budget:</strong> ₹{currentEvent.budget ? formatAsINR(currentEvent.budget) : 'N/A'}</li>
      </ul>
    </div>
  );
}

export default EventOverview;