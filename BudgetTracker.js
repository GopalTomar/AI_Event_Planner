// frontend/src/components/BudgetTracker.js
import React from 'react';
import { useEvent } from '../context/EventContext';

function BudgetTracker() {
  const { currentEvent } = useEvent();

  // For demonstration, let's assume expenses are 25% of the budget.
  // In a real app, this would come from the backend.
  const currentExpenses = currentEvent ? currentEvent.budget * 0.25 : 0;
  const budget = currentEvent ? currentEvent.budget : 0;
  const remainingBudget = budget - currentExpenses;
  const progressPercent = budget > 0 ? (currentExpenses / budget) * 100 : 0;

  // Helper to format numbers as Indian currency
  const formatAsINR = (num) => {
    return num.toLocaleString('en-IN');
  };

  return (
    <div className="dashboard-panel budget-tracker">
      <h2>Budget Tracker</h2>
      {currentEvent ? (
        <>
          <div className="budget-info">
            {/* Switched from $ to ₹ and used en-IN formatting */}
            <p><span>Planned Budget:</span> <strong>₹{formatAsINR(budget)}</strong></p>
            <p><span>Expenses:</span> <strong>₹{formatAsINR(currentExpenses)}</strong></p>
            <p><span>Remaining:</span> <strong>₹{formatAsINR(remainingBudget)}</strong></p>
          </div>
          <div className="budget-progress-bar">
            <div className="budget-progress-fill" style={{ width: `${progressPercent}%` }}></div>
          </div>
        </>
      ) : (
        <p className="placeholder-text">Your budget summary will be shown here.</p>
      )}
    </div>
  );
}

export default BudgetTracker;