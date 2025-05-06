import React from 'react';
import { useContext } from 'react';
import { Button } from '@chakra-ui/react';
import {doc, getDoc} from 'firebase/firestore';
import { db } from '../../utils/firebase/initialize_firebase_API';
import redirectToStripeCheckout from '../../utils/payment/stripe_redirect';
import { GlobalContext } from '../../page_hub/GlobalContext';

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

                //if the user hasn't setup payment information, send them to payment page
                if (!userData.hasEnteredPaymentInformation){
                    // While user checks out, display a waiting page that directs the user to complete checkout
                    //navigate("payment-waiting-page");

                    //This function directs the user to the stripe checkout in browser
                    const session_id = await redirectToStripeCheckout(userData.email);
                    
                    // Set global Stripe Session ID variable to access from the waiting page
                    setStripeSessionId(session_id);

                    //need to navigate to a waiting page which handles future logic
                    navigate("checkout-waiting");
                    
                }
                else {
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