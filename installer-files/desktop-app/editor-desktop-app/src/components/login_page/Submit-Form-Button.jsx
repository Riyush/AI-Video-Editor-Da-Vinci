import React from 'react';
import { useContext } from 'react';
import { Button } from '@chakra-ui/react';
import {doc, getDoc} from 'firebase/firestore';
import { db } from '../../utils/firebase/initialize_firebase_API';
import redirectToStripeCheckout from '../../utils/payment/stripe_redirect';
import { GlobalContext } from '../../page_hub/GlobalContext';
import { calculateRemainingTrialDays } from '../../utils/firebase/retrieve_user_details';

function SubmitFormButton({text, functionality, setError, setErrorMessage, navigate}) {

    const { setStripeSessionId, setUserId } = useContext(GlobalContext);
    
    return (
        <Button
        onClick={async () => {
            try {
                const user = await functionality(); // functionality is the function to call directly
                //Set Global State variable of user ID
                setUserId(user.uid);
                // Get user's document information
                const userRef = doc(db, 'users', user.uid);
                // getDoc must work because in this try block, we successfully return a user, 
                // meaning there is a database entry identified by consistent uid
                const docSnap = await getDoc(userRef);
                const userData = docSnap.data(); // 👈 this is a plain JS object

                // now we have the User details so we can calculate remaining trial days
                const remainingDays = calculateRemainingTrialDays(userData.createdAt);

                // If the user has not paid and their free trial is done as indicated by 0 remaining days
                // Then we navigate them to a page indicating that trial inspiration with a button for stripe checkout
                if (!userData.hasEnteredPaymentInformation && remainingDays === 0){
                    navigate("free-trial-expired");
                }
                else {
                    // I don't think I need to pass user information because global state records User ID
                    navigate("user-dashboard");
                }

                


            } catch (error) {
                // show error to user
                // Update the UI: show message, red borders, etc.
                setError(true);          // toggle red borders, etc.
                setErrorMessage(error.message); // Use Firebase Error Message
            }
        }}
            colorScheme="teal"
            variant="solid"
            mt = {3}>{text}</Button>
    )
}

export default SubmitFormButton;