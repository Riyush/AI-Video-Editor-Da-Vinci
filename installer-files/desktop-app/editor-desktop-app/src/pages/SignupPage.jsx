import React from 'react';
import { useState } from "react";
import {Box, Text, Button, VStack} from '@chakra-ui/react';

// Import Components
import EmailInput from '../components/login_page/Email-Input';
import PasswordInput from '../components/login_page/Password-Input';
import SubmitFormButton from '../components/login_page/Submit-Form-Button';
import RedirectPageButton from '../components/login_page/Redirect-Page-Button';
import GoogleButton from '../components/login_page/Google-Button';
import ErrorText from '../components/login_page/Error-Text';

import { signup } from '../utils/firebase/signup_function';

// NOTE, I commented out the Google button, To add it:
// /*<GoogleButton text="Sign Up With Google" navigate={navigate}/>*/

function SignUpPage( {navigate}) {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    
    const handleEmailChange = (e) => setEmail(e.target.value);
    const handlePasswordChange = (e) => setPassword(e.target.value);

    // error state variables
    const [error, setError] = useState(false);
    const [errorMessage, setErrorMessage] = useState('');
    return (
        <Box
        minH='100vh'
        bgGradient="radial(black, gray.900)">
        <VStack>
            <Text
            pt={14}
            pb= {2}
            textAlign={"center"}
            bgGradient='linear(to-b, white, orange.400)'
            bgClip='text'
            fontSize='5xl'
            fontWeight='extrabold'> Create New Account</Text>

            <EmailInput 
                value={email} 
                onChange={handleEmailChange}
                error={error}
            />
            <PasswordInput 
                value={password} 
                onChange={handlePasswordChange}
                error={error}
            />
            <SubmitFormButton  text = "Create New Account" functionality={() => signup(email, password)} setError={setError} setErrorMessage={setErrorMessage} navigate={navigate}/>
            <ErrorText error={error} errorMessage={errorMessage}></ErrorText>
            <Text
                pt= {10}
                color="orange.400"
                fontWeight={"bold"}
                fontSize='3xl'
                bgGradient='linear(to-b, orange, white)'
                bgClip='text'
                > Returning User?</Text>
            <RedirectPageButton 
                DisplayText="Back to Log In"
                navigate={navigate}
                page="login"/>

        </VStack>
        </Box>
    )
}

export default SignUpPage;