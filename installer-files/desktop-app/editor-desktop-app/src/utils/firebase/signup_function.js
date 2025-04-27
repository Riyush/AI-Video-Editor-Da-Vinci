import {auth} from './initialize_firebase_API';
import { createUserWithEmailAndPassword } from "firebase/auth";

export async function signup(email, password) {
    try {
      const userCredential = await createUserWithEmailAndPassword(auth, email, password);
      console.log("User created:", userCredential.user);
      return userCredential.user;
    } catch (error) {
      console.error("Signup failed:", error.message);
      throw error;
    }
  }
  