import { db } from "./initialize_firebase_API";
import { doc, getDoc } from "firebase/firestore";

async function retrieveUserDetails(userID){
    const userRef = doc(db, 'users', userID);
    const docSnap = await getDoc(userRef);
    const userData = docSnap.data(); // 👈 this is a plain JS object
    return userData;
}

function calculateRemainingTrialDays(createdAt, trialLengthDays = 14){
    if (!createdAt || typeof createdAt.toDate !== 'function') {
    return null; // or 0, or "loading"
    }
    // Firebase Timestamp to JS Date
    const createdDate = createdAt.toDate(); 

    // Today's date
    const now = new Date();

    // Difference in milliseconds
    const diffMs = now - createdDate;

    // Convert to days
    const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));

    // Remaining trial days
    const remainingDays = Math.max(0, trialLengthDays - diffDays);

    console.log(remainingDays);

    return remainingDays
}
export {retrieveUserDetails, calculateRemainingTrialDays};