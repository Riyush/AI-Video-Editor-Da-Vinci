import React from 'react';
import { Button } from '@chakra-ui/react';


function SubmitFormButton({text, functionality, setError, setErrorMessage}) {
    return (
        <Button
        onClick={async () => {
            try {
                const user = await functionality(); // functionality is the function to call directly
                // If its a new user:

            } catch (error) {
                // show error to user
                // Update the UI: show message, red borders, etc.
                setError(true);          // toggle red borders, etc.
                setErrorMessage(error.message); // Use Firebase Error Message
            }
        }}
            colorScheme="teal"
            variant="solid"
            mt = {3}>{text}</Button>
    )
}

export default SubmitFormButton;