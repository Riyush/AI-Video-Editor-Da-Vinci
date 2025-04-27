import { signInWithEmailAndPassword, signInWithPopup } from "firebase/auth";
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
export async function handleGoogleLogin() {
  try {
    const result = await signInWithPopup(auth, provider);
    console.log("User signed in:", result.user);
    return result.user;
  } catch (error) {
    console.error("Google sign-in error:", error.message);
    throw error;
  }
}