import React from 'react';
import { Button } from '@chakra-ui/react';


function SubmitFormButton({text, functionality}) {
    return (
        <Button
        onClick={async () => {
            try {
                const user = await functionality(); // functionality is the function to call directly
                // do something with the user and navigate to next page
            } catch (error) {
                // show error to user
            }
        }}
            colorScheme="teal"
            variant="solid"
            mt = {3}>{text}</Button>
    )
}

export default SubmitFormButton;