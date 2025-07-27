// frontend/src/components/TaskList.js
import React from 'react';
import { useEvent } from '../context/EventContext';

function TaskList() {
  const { currentEvent } = useEvent();

  return (
    <div className="dashboard-panel task-list">
      <h2>Action Items</h2>
      {currentEvent && currentEvent.action_items && currentEvent.action_items.length > 0 ? (
        <ul>
          {currentEvent.action_items.map((item, index) => (
            <li key={index} className="task-item">
              <input type="checkbox" id={`task-${index}`} />
              <label htmlFor={`task-${index}`}>{item}</label>
            </li>
          ))}
        </ul>
      ) : (
        <p className="placeholder-text">Your generated tasks and action items will appear here.</p>
      )}
    </div>
  );
}

export default TaskList;