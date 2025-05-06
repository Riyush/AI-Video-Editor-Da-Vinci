import React from 'react';
import { Button } from '@chakra-ui/react';
import { GlobalContext } from '../../page_hub/GlobalContext';
import { useContext } from 'react';

function RedirectPageButton( {DisplayText, navigate, page}) {
    const { stripeSessionId } = useContext(GlobalContext);

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