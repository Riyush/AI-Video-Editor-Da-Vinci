import React, { useEffect, useContext, useState} from "react";
import { GlobalContext } from "../page_hub/GlobalContext";
import {SettingsIcon} from '@chakra-ui/icons';
import { FiSettings, FiClock, FiCheckCircle } from 'react-icons/fi';
import { Text, Box, HStack, VStack, Icon, IconButton } from "@chakra-ui/react";

import {retrieveUserDetails, calculateRemainingTrialDays} from "../utils/firebase/retrieve_user_details";

function UserDashboardPage({navigate}) {
    //retrieve the logged in user ID
    const {userId } = useContext(GlobalContext);
    // state variable for user's account details from firestore
    const [userData, setUserData] = useState(null);

    //useEffect hook to call asynchronous retrieveUserDetails functions and store in userData
    useEffect(() => {
    async function fetchData() {
      const data = await retrieveUserDetails(userId);
      setUserData(data);
    }

    if (userId) {
      fetchData();
    }
    }, [userId]);

    // Don't render until we have userData
    if (!userData) {
    return null; 
    }
    
    // now we have the User details so we can calculate remaining trial days
    const remainingDays = calculateRemainingTrialDays(userData.createdAt);
    
    return (
    <Box 
    minH="100vh" // full height of screen
    bgGradient="radial(black, gray.700)">
        <Box
        display="flex"
        justifyContent="center"
        py={4}>
        <HStack
        justify="space-between"
        width="90%"
        align="center">
            {/* Conditionally render thtis VStack based on the user's payment plan */}
            {userData?.hasEnteredPaymentInformation ? (
                <VStack>
                    <FiCheckCircle/>
                    <Text> Basic Content Plan {remainingDays}</Text>
                </VStack>
            ) : (
                <VStack>
                <FiClock/>
                <Text> {remainingDays} Days Remaining</Text>
                </VStack>
            )}
            
        <Text
        textAlign={"center"}
        bgGradient='linear(to-b, white, cyan.200)'
        bgClip='text'
        fontSize='4xl'
        fontWeight='extrabold'
        > Select a Preset <br />Editing Style</Text>
        <SettingsIcon></SettingsIcon>
        </HStack>
        </Box>
    </Box>
    )
}

export default UserDashboardPage;