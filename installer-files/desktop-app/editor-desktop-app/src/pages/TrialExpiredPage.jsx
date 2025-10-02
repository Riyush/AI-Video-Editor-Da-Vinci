import React from "react";
import { Box, Flex, Text } from "@chakra-ui/react";
import RedirectPageButton from "../components/login_page/Redirect-Page-Button";

function TrialExpiredPage({navigate}) {

    return(
    <Box
    minH='100vh'
    bgGradient="radial(black, gray.900)">
        <Text
        pt={14}
            pb= {2}
            textAlign={"center"}
            bgGradient='linear(to-b, white, orange.400)'
            bgClip='text'
            fontSize='5xl'
            fontWeight="bold"> Your Free Trial Has Expired
            </Text>
        <Text
            textAlign={"center"}
            bgGradient='linear(to-b, white, cyan.400)'
            bgClip='text'
            fontSize='4xl'
            fontWeight='semibold'
            >
            But We'd Hate To See You Go..
            </Text>
        <Flex
        justify="center"
        mt={10}>
            <RedirectPageButton
            DisplayText="Purchase $14/month subscription"
            navigate={navigate}
            page="checkout-waiting"></RedirectPageButton>
        </Flex>
        

        <Text
        pt={10}
        pb={6}
        textAlign={"center"}
        bgGradient='linear(to-b, white, cyan.200)'
        bgClip='text'
        fontSize='4xl'
        fontWeight='extrabold'
        >Or..</Text>

        <Flex
        justify="center">
            <RedirectPageButton
        DisplayText="Return to Login"
        navigate={navigate}
        page="login"></RedirectPageButton>
        </Flex>
        
    </Box>
    )
}

export default TrialExpiredPage;