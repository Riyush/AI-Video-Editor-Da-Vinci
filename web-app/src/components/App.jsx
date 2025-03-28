import { useState } from 'react'
import reactLogo from '../assets/react.svg'
import viteLogo from '/vite.svg'
import '../css/App.css'

// function to download from firebase
const handleDownload = async () => {
  try {
    // ✅ Reference to your `.pkg` file in Firebase Storage
    const fileRef = ref(storage, "installers/my_downloader.pkg");

    // ✅ Get the direct URL for downloading
    const downloadURL = await getDownloadURL(fileRef);
    
    // ✅ Redirect the browser to the download URL
    // This code actually goes to the url and downloads the file
    window.location.href = downloadURL;
    console.log("Completed Download")
  } catch (error) {
    console.error("Error downloading file:", error);
  }
};

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <h1>Download Button</h1>
      <div className="download-button">
        <button onClick={() => 
            {
              handleDownload();
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
