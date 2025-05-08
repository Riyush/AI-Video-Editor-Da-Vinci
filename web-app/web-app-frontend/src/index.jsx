import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import './css/index.css';
import App from './page-hub/App.jsx';
import { ChakraProvider } from '@chakra-ui/react';

// This renders the App component to the DOM as the root Element??
createRoot(document.getElementById('root')).render(
  <StrictMode>
    <ChakraProvider>
    <App />
    </ChakraProvider>
  </StrictMode>,
)