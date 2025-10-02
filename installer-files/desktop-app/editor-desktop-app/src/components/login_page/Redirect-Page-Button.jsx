import React from 'react';
import { Button } from '@chakra-ui/react';
import { GlobalContext } from '../../page_hub/GlobalContext';
import { useContext } from 'react';
import redirectToStripeCheckout from '../../utils/payment/stripe_redirect';
import { retrieveUserDetails } from '../../utils/firebase/retrieve_user_details';

function RedirectPageButton( {DisplayText, navigate, page}) {
    const { stripeSessionId, setStripeSessionId } = useContext(GlobalContext);
    const {userId, setUserId} = useContext(GlobalContext);

    const handleClick = async () => {
        // Custom behavior only when displayText indicates that we need to expire the checkout session
        if (DisplayText === "Cancel Checkout and Return to Login") {
          try {
            const res = await fetch('http://127.0.0.1:8000/api/billing/expire-checkout-session/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ session_id: stripeSessionId })
              });
            console.log("Checkout session expired.");
          } catch (error) {
            console.error("Failed to expire checkout session:", error);
          }
        }
        if (DisplayText === "Purchase $14/month subscription") {
          // prepare to create a checkout session by getting user Data and email.
          const userData = await retrieveUserDetails(userId);

          //This function directs the user to the stripe checkout in browser
          const session_id = await redirectToStripeCheckout(userData.email);
                    
          // Set global Stripe Session ID variable to access from the waiting page
          setStripeSessionId(session_id);
        }
    
        // In all cases, navigate
        navigate(page);
      };
    return (
        <Button
        onClick={() => { handleClick()}}
        colorScheme="orange"
        >{DisplayText}</Button>
    )
}

export default RedirectPageButton;