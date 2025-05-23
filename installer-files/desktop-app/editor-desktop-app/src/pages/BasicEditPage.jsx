import React, {useState, useEffect} from "react";
import { Box, Button, HStack, Text, VStack, Image } from "@chakra-ui/react";

import { invoke } from '@tauri-apps/api/core';

import FolderPicker from "../components/dashboard/FolderPicker";
import RedirectPageButton from "../components/login_page/Redirect-Page-Button";

function BasicEditPage({navigate}) {
    // All state variables to be sent to the script

    // whether or not the clips are already added to the timeline
    const [addedToTimeline, setAddedToTimeline] = useState(null);
    // if clips are not added, the path to those clips is here
    const [clipFolderPath, setClipFolderPath] = useState(null);
    //desired video pacing, this determines how much silence is removed, padding silence for pacing, etc
    const [pacingChoice, setPacingChoice] = useState(null);
    //use cuts and transitions vs none, cuts and transitions will be enhanced with sound effects
    const [useCutsAndTransitions, setUseCutsAndTransitions] = useState(null);
    //enhance audio in Resolve editor or not
    const [audioEnhancement, setAudioEnhancement] = useState(null);
    // Add Captions
    const [addCaptions, setAddCaptions] = useState(null);
    // AutoColor Option
    const [autoColor, setAutoColor] = useState(null);
    // useEffect that simply prints all state variables to be sent to script
    useEffect(() => {
        console.log("already added to timeline", addedToTimeline);
        console.log("Folder Path:", clipFolderPath);
        console.log("Pacing Choice:", pacingChoice);
        console.log("Use Cuts and Transitions:", useCutsAndTransitions);
        console.log("Audio Enhancement:", audioEnhancement);
        console.log("Add Captions:", addCaptions);
        console.log("AutoColor:", autoColor);
    }, [addedToTimeline, clipFolderPath, pacingChoice, useCutsAndTransitions, addCaptions, audioEnhancement, autoColor]);
    return (
        <Box
        minH="100vh" // full height of screen
        bgGradient="radial(black, gray.700)"
        position="relative"
        >
            {/* Top-right Back Button */}
        <Button
            position="absolute"
            top="4"
            right="4"
            colorScheme="teal"
            onClick={() => navigate("user-dashboard")}
        >
            Back
        </Button>
            <Text
            pt={4}
                pb= {2}
                textAlign={"center"}
                bgGradient='linear(to-b, white, cyan.200)'
                bgClip='text'
                fontSize='5xl'
                fontWeight='extrabold'> Tell us how you like it</Text>
            <VStack alignItems="left" mt={5} ml={5}>
                <HStack>
                    <Text
                    bgGradient='linear(to-b, white, cyan.200)'
                    bgClip='text'
                    fontSize='2xl'
                    fontWeight='extrabold'>Have you added clips to Timeline?</Text>
                    <Button
                    ml={7}
                    w="80px"
                    h="50px"
                    colorScheme={addedToTimeline === true ? 'green' : 'orange'}
                    variant={addedToTimeline === true ? 'solid' : 'outline'}
                    onClick={() =>{
                        setAddedToTimeline(true)
                    }}>Yes</Button>
                    <Button
                    ml={6}
                    w="80px"
                    h="50px"
                    colorScheme={addedToTimeline === false ? 'green' : 'orange'}
                    variant={addedToTimeline === false ? 'solid' : 'outline'}
                    onClick={() => {
                        setAddedToTimeline(false)
                    }}>No</Button>
                </HStack>
                {addedToTimeline === false && (
                <HStack align="start">
                    <Text
                    bgGradient='linear(to-b, white, cyan.200)'
                    bgClip='text'
                    fontSize='2xl'
                    fontWeight='extrabold'
                    mr={6}>
                        Select folder and label clip order
                    </Text>
                    <FolderPicker setClipFolderPath={setClipFolderPath} />
                    <RedirectPageButton
                    DisplayText="See Example"
                    navigate={navigate}
                    page="example-clip-folder"></RedirectPageButton>
                    
                </HStack>
                )}
            <HStack>
                <Text
                bgGradient='linear(to-b, white, cyan.200)'
                bgClip='text'
                fontSize='2xl'
                fontWeight='extrabold'> Video Pacing</Text>
                <Button
                    ml={6}
                    w="80px"
                    h="50px"
                    colorScheme={pacingChoice === 'calm' ? 'green' : 'orange'}
                    variant={pacingChoice === 'calm' ? 'solid' : 'outline'}
                    onClick={() => {
                        setPacingChoice('calm');
                    }}>Calm</Button>
                <Button
                    ml={6}
                    w="80px"
                    h="50px"
                    colorScheme={pacingChoice === 'normal' ? 'green' : 'orange'}
                    variant={pacingChoice === 'normal' ? 'solid' : 'outline'}
                    onClick={() => {
                        setPacingChoice('normal');
                    }}>Normal</Button>
                <Button
                    ml={6}
                    w="80px"
                    h="50px"
                    colorScheme={pacingChoice === 'Fast' ? 'green' : 'orange'}
                    variant={pacingChoice === 'Fast' ? 'solid' : 'outline'}
                    onClick={() => {
                        setPacingChoice('Fast')
                    }}>Fast</Button>
            </HStack>
            <HStack>
                <Text
                bgGradient='linear(to-b, white, cyan.200)'
                bgClip='text'
                fontSize='2xl'
                fontWeight='extrabold'
                >Use Zoom Cuts and Transitions?</Text>
                <Button
                    ml={7}
                    w="80px"
                    h="50px"
                    colorScheme={useCutsAndTransitions === true ? 'green' : 'orange'}
                    variant={useCutsAndTransitions === true ? 'solid' : 'outline'}
                    onClick={() =>{
                        setUseCutsAndTransitions(true)
                    }}>Yes</Button>
                    <Button
                    ml={6}
                    w="80px"
                    h="50px"
                    colorScheme={useCutsAndTransitions === false ? 'green' : 'orange'}
                    variant={useCutsAndTransitions === false ? 'solid' : 'outline'}
                    onClick={() => {
                        setUseCutsAndTransitions(false)
                    }}>No</Button>
            </HStack>
            <HStack>
                <Text
                bgGradient='linear(to-b, white, cyan.200)'
                bgClip='text'
                fontSize='2xl'
                fontWeight='extrabold'
                >Enhance Audio?</Text>
                <Button
                    ml={7}
                    w="80px"
                    h="50px"
                    colorScheme={audioEnhancement === true ? 'green' : 'orange'}
                    variant={audioEnhancement === true ? 'solid' : 'outline'}
                    onClick={() =>{
                        setAudioEnhancement(true)
                    }}>Yes</Button>
                    <Button
                    ml={6}
                    w="80px"
                    h="50px"
                    colorScheme={audioEnhancement === false ? 'green' : 'orange'}
                    variant={audioEnhancement === false ? 'solid' : 'outline'}
                    onClick={() => {
                        setAudioEnhancement(false)
                    }}>No</Button>
            </HStack>
            
            <HStack>
                <Text
                bgGradient='linear(to-b, white, cyan.200)'
                bgClip='text'
                fontSize='2xl'
                fontWeight='extrabold'
                >Add Captions?</Text>
                <Button
                    ml={7}
                    w="80px"
                    h="50px"
                    colorScheme={addCaptions === true ? 'green' : 'orange'}
                    variant={addCaptions === true ? 'solid' : 'outline'}
                    onClick={() =>{
                        setAddCaptions(true)
                    }}>Yes</Button>
                    <Button
                    ml={6}
                    w="80px"
                    h="50px"
                    colorScheme={addCaptions === false ? 'green' : 'orange'}
                    variant={addCaptions === false ? 'solid' : 'outline'}
                    onClick={() => {
                        setAddCaptions(false)
                    }}>No</Button>
            </HStack>
            <HStack>
                <Text
                bgGradient='linear(to-b, white, cyan.200)'
                bgClip='text'
                fontSize='2xl'
                fontWeight='extrabold'
                >Improve Brightness?</Text>
                <Button
                    ml={7}
                    w="80px"
                    h="50px"
                    colorScheme={autoColor === true ? 'green' : 'orange'}
                    variant={autoColor === true ? 'solid' : 'outline'}
                    onClick={() =>{
                        setAutoColor(true)
                    }}>Yes</Button>
                    <Button
                    ml={6}
                    w="80px"
                    h="50px"
                    colorScheme={autoColor === false ? 'green' : 'orange'}
                    variant={autoColor === false ? 'solid' : 'outline'}
                    onClick={() => {
                        setAutoColor(false)
                    }}>No</Button>
            </HStack>

            <Button
            // submit button that sends user prefferences to rust backend to send to script
            mt = {6}
            mb = {10}
            ml='40vw'
            w="150px"
            colorScheme="teal"
            onClick={()=>{
                const configurations = {
                    added_to_timeline: addedToTimeline,
                    clip_folder_path: clipFolderPath,
                    pacing_choice: pacingChoice,
                    use_cuts_and_transitions: useCutsAndTransitions,
                    audio_enhancement: audioEnhancement,
                    add_captions: addCaptions,
                    auto_color: autoColor,
                };
                invoke("Edit_Basic_Video", {configurations: configurations});
            }}>EDIT!!</Button>
            </VStack>
        </Box>
    )
}

export default BasicEditPage;