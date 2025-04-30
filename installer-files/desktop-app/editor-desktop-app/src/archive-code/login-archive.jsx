import { getRedirectResult, onAuthStateChanged } from 'firebase/auth';
import { auth } from "../utils/firebase/initialize_firebase_API";

// react hook to check if a user has logged in via Google.
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