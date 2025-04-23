import { useState, useEffect } from "react";
import { invoke } from "@tauri-apps/api/core";

import Login from '../pages/LoginPage.jsx';
import Home from '../pages/HomePage.jsx';

import { once } from '@tauri-apps/api/event';

// This app.jsx file acts as a central hub containing all pages that the user
// can navigate to. Pages are simply react components found in pages folder.
// On each page are buttons allowing the user navigate to different pages
// This file keeps track of each page and renders the appropriate one for the user
function App() {
  
  const [activePage, setActivePage] = useState('home'); // Track the current page

  useEffect(() => {
    // Listen for the global "show-login" event once
    once('prompt-user-to-login', () => {
      setActivePage('login');
    });
  }, []);
  // This function decides what to render based on current page state
  const renderPage = () => {
    switch (activePage) {
      case 'home':
        return <Home navigate={setActivePage} />;
      case 'login':
        return <Login navigate={setActivePage}/>; 
      default:
        return <Home navigate={setActivePage} />; // fallback
    }
  };  // Each case is a different page to navigate to

  return (
    <div>
      {renderPage()}
    </div>
  )
}

export default App;
