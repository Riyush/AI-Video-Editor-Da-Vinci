import { useState, useEffect } from "react";

import Login from '../pages/LoginPage.jsx';
import Home from '../pages/HomePage.jsx';

import { listen } from '@tauri-apps/api/event';

// This app.jsx file acts as a central hub containing all pages that the user
// can navigate to. Pages are simply react components found in pages folder.
// On each page are buttons allowing the user navigate to different pages
// This file keeps track of each page and renders the appropriate one for the user
function App() {
  
  const [activePage, setActivePage] = useState('home'); // Track the current page

  useEffect(() => {
    // Start listening for global events sent from Rust
    const unlisten = listen('prompt-user-to-login', () => {
      console.log("Received prompt-user-to-login event");
      setActivePage('login');
    });

    // Clean up the listener when the component unmounts
    return () => {
      unlisten.then((fn) => fn());
    };
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
