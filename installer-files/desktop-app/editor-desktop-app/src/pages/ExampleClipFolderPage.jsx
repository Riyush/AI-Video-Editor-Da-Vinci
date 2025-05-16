import React from "react";
import { Text, Box, Image, VStack } from "@chakra-ui/react";
import RedirectPageButton from "../components/login_page/Redirect-Page-Button";
import ClipFolderStructureExample from '../assets/example-clip-folder-format.png';

function ExampleClipFolderPage({navigate}) {

    return (
        <Box
        minH="100vh" // full height of screen
        bgGradient="radial(black, gray.700)"
        >
            <VStack
            pt={14}>
            <Image
            src={ClipFolderStructureExample} />
            <Text
            p={5}
            bgGradient='linear(to-b, white, cyan.200)'
            bgClip='text'
            fontSize='2xl'
            fontWeight='extrabold'>Notice, each clip in "example clip folder" starts with a number to indicate the order in which the clip will appear on the Da Vinci Resolve Timeline</Text>
            <RedirectPageButton 
            DisplayText="Back to Edit Page"
            navigate={navigate}
            page="basic-edit-page"></RedirectPageButton>
            </VStack>
        </Box>
        
    )
}

export default ExampleClipFolderPage;