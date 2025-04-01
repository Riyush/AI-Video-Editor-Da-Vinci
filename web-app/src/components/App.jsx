import { useState } from 'react'
import reactLogo from '../assets/react.svg'
import viteLogo from '/vite.svg'
import '../css/App.css'

import {storage} from '../firebase/initialize_firebase_API.js';
import { ref, getDownloadURL } from "firebase/storage";

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

function App() {

  return (
    <>
      <h1>Download Button</h1>
      <div className="download-button">
        <button onClick={() => 
            {
              downloadInstaller()
              console.log("Click!");
            }
            }>
          Download
        </button>
        <p>
          Download the tool
        </p>
      </div>
      
    </>
  )
}

export default App
