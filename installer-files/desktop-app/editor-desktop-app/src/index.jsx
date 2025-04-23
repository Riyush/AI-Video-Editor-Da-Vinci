import { StrictMode } from 'react';
import ReactDOM from "react-dom/client";
import App from "./page_hub/App.jsx";
import { ChakraProvider } from '@chakra-ui/react';

ReactDOM.createRoot(document.getElementById("root")).render(
  <StrictMode>
    <ChakraProvider>
    <App />
    </ChakraProvider>
  </StrictMode>,
);
