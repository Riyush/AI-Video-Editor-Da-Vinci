import React, { useEffect, useContext, useState} from "react";
import { GlobalContext } from "../page_hub/GlobalContext";
import {SettingsIcon} from '@chakra-ui/icons';
import { FiSettings, FiClock, FiCheckCircle } from 'react-icons/fi';
import { GiMaterialsScience } from "react-icons/gi";
import { Text, Box, HStack, VStack, Icon, IconButton } from "@chakra-ui/react";

import DashboardPresetGrid from "../components/dashboard/Dashboard-Preset-Grid";
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
        align="center"
        mx="auto">
            {/* Left Side */}
            {/* Left Side */}
        <Box minW="100px" maxW="120px">
            {userData?.hasEnteredPaymentInformation ? (
            <VStack spacing={1} textAlign="center" mt={6}>
                <GiMaterialsScience color="white" size="50px" />
                <Text
                color="white"
                fontWeight="semibold"
                bgGradient="linear(to-b, white, cyan.200)"
                bgClip="text"
                >
                Basic Content Plan
                </Text>
            </VStack>
            ) : (
            <VStack spacing={1} textAlign="center">
                <FiClock color="white" size="24px" />
                <Text
                color="white"
                fontWeight="semibold"
                bgGradient="linear(to-b, white, cyan.200)"
                bgClip="text"
                >
                {remainingDays} Days Remaining in Your Trial
                </Text>
            </VStack>
            )}
        </Box>

        {/* Center */}
        <Box flex="1" textAlign="center">
            <Text
            bgGradient="linear(to-b, white, cyan.200)"
            bgClip="text"
            fontSize="4xl"
            fontWeight="extrabold"
            >
            Select a Preset <br /> Editing Style
            </Text>
        </Box>

        {/* Right Side */}
        <Box minW="100px" textAlign="right">
            <IconButton
            icon={<SettingsIcon boxSize={10} />}
            onClick={() => navigate('user-settings')} //Need to implement this in future.
            aria-label="Settings"
            color="white"
            variant="ghost"
            mb={8}
            w={20}
            h={20}
            _hover={{ bg: 'gray.700' }}
            />
        </Box>
        </HStack>

        
        </Box>
        <DashboardPresetGrid navigate={navigate}/>
    </Box>
    )
}

export default UserDashboardPage;