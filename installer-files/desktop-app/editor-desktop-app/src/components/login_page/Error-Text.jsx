import React from "react";
import { Text } from "@chakra-ui/react";

function ErrorText({error, errorMessage}) {
    if (!error) return null; // If there's no error, render nothing

    const formattedMessage = errorMessage.replace('Firebase: ', '');

    return (
        <Text color="red.500" mt={2}>
            {formattedMessage}
        </Text>
    )
}

export default ErrorText;