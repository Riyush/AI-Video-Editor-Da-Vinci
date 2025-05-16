import { useState } from "react";
import { Button, Text, VStack } from "@chakra-ui/react";
import { open } from '@tauri-apps/plugin-dialog';
import { readDir, BaseDirectory } from '@tauri-apps/plugin-fs'; 
// I can do some sanity checks on the files within the clip folder that the user selects

function FolderPicker({setClipFolderPath}) {
    return(
        <Button
        mr={4}
        colorScheme="teal"
        maxW="200px"
        onClick={async () =>{
            // Open a dialog
            const directory = await open({
            multiple: false,
            directory: true,
            });
            setClipFolderPath(directory);
            console.log(directory); 
        }}>
            Select Clip Folder
        </Button>
    )
}

export default FolderPicker;