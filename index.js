// frontend/src/index.js
import React from 'react';
import ReactDOM from 'react-dom/client';
import './App.css'; // Global styles
import App from './App';
// import reportWebVitals from './reportWebVitals'; // <-- DELETE THIS LINE
import { EventProvider } from './context/EventContext'; // Import the provider

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <EventProvider> {/* Wrap App with the EventProvider */}
      <App />
    </EventProvider>
  </React.StrictMode>
);

// reportWebVitals(); // <-- AND DELETE THIS LINE