    import React from 'react';
    import { useState } from "react";
    import {Box, Text, Button, VStack} from '@chakra-ui/react';
    import { login } from '../utils/firebase/login_function';

    //components
    import EmailInput from '../components/login_page/Email-Input';
    import PasswordInput from '../components/login_page/Password-Input';
    import SubmitFormButton from '../components/login_page/Submit-Form-Button';
    import GoogleLoginButton from '../components/login_page/Google-Login-Button';
    import RedirectPageButton from '../components/login_page/Redirect-Page-Button';

    function LoginPage({navigate}) {
        const [email, setEmail] = useState('');
        const [password, setPassword] = useState('');

        const handleEmailChange = (e) => setEmail(e.target.value);
        const handlePasswordChange = (e) => setPassword(e.target.value);

        return (
            <Box
            minH="100vh" // full height of screen
            bgGradient="radial(black, gray.700)"
            >   <VStack
                pt = {10}>
                <Text
                pt={4}
                pb= {2}
                textAlign={"center"}
                bgGradient='linear(to-b, white, cyan.200)'
                bgClip='text'
                fontSize='5xl'
                fontWeight='extrabold'> Login to GameTime</Text>
                
                <EmailInput 
                value={email} 
                onChange={handleEmailChange}
                />
                <PasswordInput 
                value={password} 
                onChange={handlePasswordChange}/>

                <SubmitFormButton text="Log In" functionality={() => login(email, password)}/>
                <GoogleLoginButton/>

                <Text
                pt= {16}
                color="orange.400"
                fontWeight={"bold"}
                fontSize='3xl'
                bgGradient='linear(to-b, orange, white)'
                bgClip='text'
                > New Here?</Text>
                <RedirectPageButton 
                DisplayText = "Create New Account"
                navigate = {navigate}
                page="signup"
                />
                </VStack>
            </Box>
        )
    }
    export default LoginPage;