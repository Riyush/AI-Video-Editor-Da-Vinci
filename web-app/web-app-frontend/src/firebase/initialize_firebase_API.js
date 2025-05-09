// This file sets up firebase API for use across the project

// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
import { getStorage, ref, uploadBytes } from "firebase/storage";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyBIO3eacRFSrFmkzdXanmzKjiSEXoqO82E",
  authDomain: "ai-video-editor-8b9db.firebaseapp.com",
  projectId: "ai-video-editor-8b9db",
  storageBucket: "ai-video-editor-8b9db.firebasestorage.app",
  messagingSenderId: "25800069178",
  appId: "1:25800069178:web:b959dc3caa818691862503",
  measurementId: "G-NXPBME3PBH"
};

// Initialize Firebase app and storage modules
const app = initializeApp(firebaseConfig);
const storage = getStorage(app);

//const analytics = getAnalytics(app);

export { app, storage };