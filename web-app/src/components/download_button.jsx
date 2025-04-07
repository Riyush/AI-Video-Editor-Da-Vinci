import {storage} from '../firebase/initialize_firebase_API.js';
import { ref, getDownloadURL } from "firebase/storage";
import { Box, SimpleGrid, Text, UnorderedList, ListItem, Image, HStack, Button } from '@chakra-ui/react';
import resolveLogo from "../assets/resolve-logo.png";

// function to download from firebase
function downloadInstaller() {
    // ✅ Reference to your `.pkg` file in Firebase Storage
    const storageRef = ref(storage, "final_installer.pkg");

    // ✅ Get the direct URL for download and download to user machine
    getDownloadURL(storageRef)
    .then(url => {
      const link = document.createElement("a");
      link.href = url;
      link.download = "final_installer.pkg"; // Suggests filename
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    })
    .catch(error => console.error("Download failed:", error));

}

function DownloadButton() {

  return (
    <Button borderColor="purple.600" backgroundColor="white" mt ={5} size="lg" onClick={downloadInstaller}>
      <HStack>
        <Image src={resolveLogo} boxSize="35px"/> 
        <Text>Download tool for DaVinci Resolve on Mac</Text>
      </HStack>
      
    </Button>
  )
}

export default DownloadButton;
