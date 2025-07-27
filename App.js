// frontend/src/App.js
import React from 'react';
import './App.css';
import AgentChat from './components/AgentChat';
import EventOverview from './components/EventOverview';
import BudgetTracker from './components/BudgetTracker';
import TaskList from './components/TaskList';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        Planiva AI Event Planner
      </header>
      <main className="App-main">
        <section className="chat-section">
          <AgentChat />
        </section>
        <section className="dashboard-section">
          <EventOverview />
          <BudgetTracker />
          <TaskList />
        </section>
      </main>
    </div>
  );
}

export default App;