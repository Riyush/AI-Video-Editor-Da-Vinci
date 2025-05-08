import {auth, db} from './initialize_firebase_API';
import { createUserWithEmailAndPassword } from "firebase/auth";
import { doc, setDoc, collection, getDocs } from "firebase/firestore";
export async function signup(email, password) {
    try {
      const userCredential = await createUserWithEmailAndPassword(auth, email, password);
      const user = userCredential.user;
      listAllUsers();
      await addUserToDatabase(user); // add to Firestore
      console.log("User added to database:", userCredential.user);
      
      return user;
    } catch (error) {
      console.error("Signup failed:", error.message);
      throw error;
    }
  }
  
  async function addUserToDatabase(user) {
    const userRef = doc(db, "users", user.uid);

    const docData = {
      userID: user.uid,
      email: user.email,
      hasEnteredPaymentInformation: false,
      stripe_CustomerID: null,
      createdAt: new Date(),
    };
    console.log(docData);

    await setDoc(userRef, docData);
  }

  async function listAllUsers() {
    const querySnapshot = await getDocs(collection(db, "users"));
    querySnapshot.forEach((doc) => {
      console.log(`${doc.id} =>`, doc.data());
    });
  }