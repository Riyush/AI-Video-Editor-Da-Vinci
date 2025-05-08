import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Navbar from '../components/Navbar.jsx'; // New component
import Home from '../pages/Home.jsx'; // New page
import DownloadPage from '../pages/DownloadPage.jsx'




function App() {
 return (
   <Router>
       <Navbar />
       <Routes>
         <Route path="/" element={<Home />} />


         <Route path="/register" element ={<DownloadPage />}/>
        
         {/* Add more routes later */}
       </Routes>
   </Router>


 );
}


export default App;