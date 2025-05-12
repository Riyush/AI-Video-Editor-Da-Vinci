import { useState, useEffect } from "react";

//Import All Page Components
import Home from '../pages/HomePage.jsx';
import LoginPage from '../pages/LoginPage.jsx';
import SignUpPage from "../pages/SignupPage.jsx";
import UserDashboardPage from "../pages/UserDashboardPage.jsx";
import CheckoutWaitingPage from "../pages/CheckoutWaitingPage.jsx";
import TrialExpiredPage from "../pages/TrialExpiredPage.jsx";

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
        return <Home />;
      case 'login':
        return <LoginPage navigate={setActivePage}/>; 
      case 'signup':
        return <SignUpPage navigate={setActivePage}/>;
      case 'checkout-waiting':
        return <CheckoutWaitingPage navigate={setActivePage} />;
      case 'user-dashboard':
        return <UserDashboardPage navigate={setActivePage}/>;
      case 'free-trial-expired':
        return <TrialExpiredPage navigate={setActivePage}/>;
      
      
      default:
        return <Home />; // fallback page
    }
  };  // Each case is a different page to navigate to

  return (
    <div>
      {renderPage()}
    </div>
  )
}

export default App;
