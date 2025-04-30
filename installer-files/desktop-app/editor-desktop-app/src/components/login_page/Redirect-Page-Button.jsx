import React from 'react';
import { Button } from '@chakra-ui/react';

function RedirectPageButton( {DisplayText, navigate, page}) {
    return (
        <Button
        onClick={() => { navigate(page)}}
        colorScheme="orange"
        >{DisplayText}</Button>
    )
}

export default RedirectPageButton;