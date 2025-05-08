import { StrictMode } from 'react';
import ReactDOM from "react-dom/client";
import App from "./page_hub/App.jsx";
import { ChakraProvider } from '@chakra-ui/react';
import { GlobalProvider } from './page_hub/GlobalContext.jsx';

ReactDOM.createRoot(document.getElementById("root")).render(
  <StrictMode>
    <ChakraProvider>
    <GlobalProvider>
    <App />
    </GlobalProvider>
    </ChakraProvider>
  </StrictMode>,
);
