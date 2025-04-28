import { useState, useEffect } from "react";

//Import All Page Components
import Home from '../pages/HomePage.jsx';
import LoginPage from '../pages/LoginPage.jsx';
import SignUpPage from "../pages/SignupPage.jsx";

import { listen } from '@tauri-apps/api/event';
import { getRedirectResult, onAuthStateChanged } from 'firebase/auth';
import { auth } from "../utils/firebase/initialize_firebase_API";

// This app.jsx file acts as a central hub containing all pages that the user
// can navigate to. Pages are simply react components found in pages folder.
// On each page are buttons allowing the user navigate to different pages
// This file keeps track of each page and renders the appropriate one for the user
function App() {
  
  const [activePage, setActivePage] = useState('home'); // Track the current page

  
  useEffect(() => {
    // function to check redirect result
    async function checkLoginResult() {
      try {
        const result = await getRedirectResult(auth);
        console.log('Redirect result:', result);
  
        if (result) {
          console.log('User signed in successfully (from redirect):', result.user);
          // will redirect to new page in the future, figure this out once google login works
          setActivePage('login');
        } else {
          console.log('No user redirect result found.');
        }
      } catch (error) {
        console.error('Error checking redirect result:', error);
      }
    }
  
    // Call checkLoginResult once
    checkLoginResult();
  
    // Then ALSO listen for auth state changes
    const unsubscribe = onAuthStateChanged(auth, (user) => {
      console.log('onAuthStateChanged user:', user);
  
      if (user) {
        console.log('User is signed in via onAuthStateChanged:', user);
        setActivePage('login');
      } else {
        console.log('User is signed out.');
      }
    });
  
    // Clean up listener when component unmounts
    return () => unsubscribe();
  
  }, []);

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
        return <SignUpPage navigate={setActivePage}/>
      default:
        return <Home />; // fallbackp page
    }
  };  // Each case is a different page to navigate to

  return (
    <div>
      {renderPage()}
    </div>
  )
}

export default App;
