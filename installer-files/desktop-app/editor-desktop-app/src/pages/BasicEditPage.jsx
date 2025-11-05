import React, {useState, useEffect} from "react";
import { Box, Button, HStack, Text, VStack, Image } from "@chakra-ui/react";

import { invoke } from '@tauri-apps/api/core';
import { listen } from '@tauri-apps/api/event';

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
    const [silenceRemoval, setSilenceRemoval] = useState(null);
    // Add Captions
    const [addCaptions, setAddCaptions] = useState(null);

    // AutoColor Option
    const [addSoundEffects, setAddSoundEffects] = useState(null);

    //special variable for the number of audio tracks so that user can select which audio tracks to transcribe
    const [audioTracksCount, setAudioTracksCount] = useState(null);

    //array of int where each int represents a track to be transcribed, requires some processing
    const [tracksToTranscribe, setTracksToTranscribe] = useState([]);
    //special intermediate data structure for the tracks the user selects.
    const [selectedTracks, setSelectedTracks] = useState(null);
    // useEffect that simply prints all state variables to be sent to script
    useEffect(() => {
        //console.log("already added to timeline", addedToTimeline);
        //console.log("Folder Path:", clipFolderPath);
        //console.log("Pacing Choice:", pacingChoice);
        //console.log("Use Cuts and Transitions:", useCutsAndTransitions);
        //console.log("Silence Removal:", silenceRemoval);
        //console.log("Add Captions:", addCaptions);
        //console.log("addSoundEffects:", addSoundEffects);
        console.log("audioTracksCount:", audioTracksCount);
    }, [addedToTimeline, clipFolderPath, pacingChoice, useCutsAndTransitions, addCaptions, silenceRemoval, addSoundEffects, audioTracksCount]);

    useEffect(() => {
    const unlistenPromise = listen('audio-tracks-count', (event) => {
      console.log('Received audio tracks:', event.payload);
      if ('Audio_Track_Count' in event.payload) {
        setAudioTracksCount(Number(event.payload.Audio_Track_Count));
      }
    });

    return () => {
      unlistenPromise.then((unlisten) => unlisten()); // cleanup listener
    };
    }, []);

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
                >Remove Silences?</Text>
                <Button
                    ml={7}
                    w="80px"
                    h="50px"
                    colorScheme={silenceRemoval === true ? 'green' : 'orange'}
                    variant={silenceRemoval === true ? 'solid' : 'outline'}
                    onClick={() =>{
                        setSilenceRemoval(true)
                    }}>Yes</Button>
                    <Button
                    ml={6}
                    w="80px"
                    h="50px"
                    colorScheme={silenceRemoval === false ? 'green' : 'orange'}
                    variant={silenceRemoval === false ? 'solid' : 'outline'}
                    onClick={() => {
                        setSilenceRemoval(false)
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
                    w="110px"
                    h="50px"
                    colorScheme={addCaptions === "All Dialogue" ? 'green' : 'orange'}
                    variant={addCaptions === "All Dialogue" ? 'solid' : 'outline'}
                    onClick={() =>{
                        setAddCaptions("All Dialogue")
                        // Get Number of Audio Tracks from the Script
                        invoke("Get_Number_Of_Audio_Tracks");
                    }}>All Dialogue</Button>
                    <Button
                    ml={6}
                    w="120px"
                    h="50px"
                    colorScheme={addCaptions === "Key Moments" ? 'green' : 'orange'}
                    variant={addCaptions === "Key Moments" ? 'solid' : 'outline'}
                    onClick={() => {
                        setAddCaptions("Key Moments")
                        // Get Number of Audio Tracks from the Script
                        invoke("Get_Number_Of_Audio_Tracks");
                    }}>Key Moments</Button>
                    <Button
                    ml={6}
                    w="80px"
                    h="50px"
                    colorScheme={addCaptions === "None" ? 'green' : 'orange'}
                    variant={addCaptions === "None" ? 'solid' : 'outline'}
                    onClick={() => {
                        setAddCaptions("None")
                    }}>None</Button>
            </HStack>
            
            {((addCaptions === "Key Moments" || addCaptions === "All Dialogue") && addedToTimeline === true) && (
                // HStack block for users to select the timeline tracks they want to transcribe
                <VStack>
                    <Text
                    bgGradient='linear(to-b, white, cyan.200)'
                    bgClip='text'
                    fontSize='2xl'
                    fontWeight='extrabold'
                    >Select an Audio Track to add captions to </Text>
                    <HStack>
                        {Array.from({ length: audioTracksCount }, (_, i) => {
                        const trackNumber = i + 1;
                        return (
                        <Button
                            key={i}
                            colorScheme="cyan"
                            variant={selectedTracks === trackNumber ? "solid" : "outline"}
                            onClick={() => setSelectedTracks(trackNumber)}    // Only select one track
                        >
                            {`A${trackNumber}`}
                        </Button>
                        );
                    })}
                    </HStack>
                </VStack>
            )}
            
            <HStack>
                <Text
                bgGradient='linear(to-b, white, cyan.200)'
                bgClip='text'
                fontSize='2xl'
                fontWeight='extrabold'
                >Add Sound Effects?</Text>
                <Button
                    ml={7}
                    w="110px"
                    h="50px"
                    colorScheme={addSoundEffects === "Frequently" ? 'green' : 'orange'}
                    variant={addSoundEffects === "Frequently" ? 'solid' : 'outline'}
                    onClick={() =>{
                        setAddSoundEffects("Frequently")
                    }}>Frequently</Button>
                    <Button
                    ml={6}
                    w="120px"
                    h="50px"
                    colorScheme={addSoundEffects === "Key Moments" ? 'green' : 'orange'}
                    variant={addSoundEffects === "Key Moments" ? 'solid' : 'outline'}
                    onClick={() => {
                        setAddSoundEffects("Key Moments")
                    }}>Key Moments</Button>
                    <Button
                    ml={6}
                    w="80px"
                    h="50px"
                    colorScheme={addSoundEffects === "None" ? 'green' : 'orange'}
                    variant={addSoundEffects === "None" ? 'solid' : 'outline'}
                    onClick={() => {
                        setAddSoundEffects("None")
                    }}>None</Button>
            </HStack>

            <Button
            // submit button that sends user prefferences to rust backend to send to script
            mt = {6}
            mb = {10}
            ml='40vw'
            w="150px"
            colorScheme="teal"
            onClick={()=>{
                // Logic to finalize audio track to transcribe
                //Use a new local variable as to avoid asynchronous timing issues
                let newTracksToTranscribe = [];

                if (addCaptions === "None"){ //case where we transcribe no tracks
                    newTracksToTranscribe = [];
                }
                else if (addedToTimeline === false) {   // case where we always transcribe track 1
                    newTracksToTranscribe = [1];
                }
                else {  // case where we transcribe the selected track, can only be 1 track at this point 
                    newTracksToTranscribe = [selectedTracks];
                }

                const configurations = {
                    added_to_timeline: addedToTimeline,
                    clip_folder_path: clipFolderPath,
                    pacing_choice: pacingChoice,
                    use_cuts_and_transitions: useCutsAndTransitions,
                    silence_removal: silenceRemoval,
                    add_captions: addCaptions,
                    tracks_to_transcribe: newTracksToTranscribe,
                    add_sound_effects: addSoundEffects,
                };
                //resync the global state variable with the local variable.
                setTracksToTranscribe(newTracksToTranscribe);

                invoke("Edit_Basic_Video", {configurations: configurations});
            }}>EDIT!!</Button>
            </VStack>
        </Box>
    )
}

export default BasicEditPage;