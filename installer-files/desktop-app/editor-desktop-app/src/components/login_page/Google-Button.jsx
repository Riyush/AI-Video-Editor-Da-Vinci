import React from 'react';
import { Button, Image } from '@chakra-ui/react';
import { handleGoogleLogin } from '../../utils/firebase/login_function';
import GoogleIcon from '../../assets/google.png';

function GoogleButton({text, navigate}) {
    return (
        <Button
        mt={6}
        borderRadius='10px'
        _hover={{ bg: "yellow.100" }}
        leftIcon={<Image src={GoogleIcon} boxSize="1.5rem" />}
            onClick={async () => {
                try{
                    navigate('login')
                    handleGoogleLogin();
                    // do something with the user and navigate to next page
                }
                catch (error){
                    //show error to user
                }
            }}>
                {text}
            </Button>
    )
}

export default GoogleButton;