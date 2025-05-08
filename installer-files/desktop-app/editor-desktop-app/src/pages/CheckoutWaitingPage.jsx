import React from "react";
import { Box, Text, Flex } from "@chakra-ui/react";
import RedirectPageButton from "../components/login_page/Redirect-Page-Button";
import {useEffect, useContext } from "react";
import pollPaymentStatus from "../utils/payment/poll_payment_status";
import { updateDoc, doc } from "firebase/firestore";
import { db } from "../utils/firebase/initialize_firebase_API";
import { GlobalContext } from "../page_hub/GlobalContext";

function CheckoutWaitingPage({navigate}) {
    const { stripeSessionId, userId } = useContext(GlobalContext);
    useEffect(() => {
    
        if (stripeSessionId && userId) {
          (async () => {
            try {
              const customerIDSuccessfulTransaction = await pollPaymentStatus(stripeSessionId);
    
              if (customerIDSuccessfulTransaction) {
                const userRef = doc(db, 'users', userId);
    
                await updateDoc(userRef, {
                  hasEnteredPaymentInformation: true,
                  stripe_CustomerID: customerIDSuccessfulTransaction
                });
    
                navigate('user-dashboard'); // ✅ you may want to consider 'user-dashboard' here instead?
              } else {
                navigate('login'); // session has expired without user clicking button, default back to login
              }
            } catch (err) {
              console.log("ERROR IN POLLING:", err);
              navigate('login'); // weird case
            }
          })(); // 👈 THIS final `()` invokes the async function!
        }
      }, [stripeSessionId, userId]);

    return(
    <Box
        pt={40}
        minH="100vh" // full height of screen
        bgGradient="radial(black, gray.700)">
            <Text
            pt={4}
            pb= {2}
            textAlign={"center"}
            bgGradient='linear(to-b, white, cyan.200)'
            bgClip='text'
            fontSize='5xl'
            fontWeight='extrabold'
            >Complete Checkout In Browser </Text>
            <Text
            textAlign={"center"}
            textColor={"orange.500"}
            fontSize='4xl'
            fontWeight='bold'
            >
                And Let's get to Editing!
            </Text>
            <Text
            pt={4}
            pb={6}
            textAlign={"center"}
            bgGradient='linear(to-b, white, cyan.200)'
            bgClip='text'
            fontSize='2xl'
            fontWeight='extrabold'
            > Or..</Text>
            <Flex justify="center">
            <RedirectPageButton DisplayText="Cancel Checkout and Return to Login" navigate={navigate} page="login"></RedirectPageButton>
            </Flex>
        </Box>
    )
}

export default CheckoutWaitingPage;