import { signInWithEmailAndPassword, signInWithRedirect, signInWithPopup } from "firebase/auth";
import { auth, provider } from "./initialize_firebase_API";

// Login via normal account
export async function login(email, password) {
  try {
    const userCredential = await signInWithEmailAndPassword(auth, email, password);
    console.log("User logged in:", userCredential.user);
    return userCredential.user;
  } catch (error) {
    console.error("Login failed:", error.message);
    throw error;
  }
}

//Login via Google
// This function handles login and new user creation
// auth is a variable derived from: getAuth(app), app comes from initializeApp(config)
// provider is created using GoogleAuthProvider() from Firebase
export async function handleGoogleLogin() {
  try {
    await signInWithRedirect(auth, provider);
    // due to page redirect, no code after the signInWithRedirect call runs
  } catch (error) {
    console.error("Google sign-in error:", error.message);
    throw error;
  }
}