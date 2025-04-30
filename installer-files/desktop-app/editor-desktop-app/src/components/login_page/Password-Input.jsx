import React from 'react';
import { InputLeftElement, InputGroup, Input, InputRightElement, Button } from '@chakra-ui/react';
import { LockIcon } from '@chakra-ui/icons';

function PasswordInput({value, onChange, error}) {
    const [show, setShow] = React.useState(false)
    const handleClick = () => setShow(!show)
    return (
        <InputGroup
            w = "70vw"
            mt = {2}>
            <InputLeftElement pointerEvents='none'>
            <LockIcon color = 'gray.300' />
            </InputLeftElement>
            <Input
            pr='4.5rem'
            type = {show ? 'text' : 'password'}
            placeholder = 'Password'
            value = {value}
            onChange={onChange}
            variant='filled' 
            bg='gray.200'
            _focus={{ bg: 'gray.50' }}
            borderRadius="20px"
            borderColor={error ? 'red.500' : 'transparent'}  // Only change border color if there's an error
            borderWidth={error ? '3px' : '0px'}              // Optional: make border visible only if error
            />
            <InputRightElement  width='4.5rem'>
            <Button h='1.75rem' size ='sm' onClick={handleClick}>
                    {show ? 'Hide' : 'Show'}
            </Button></InputRightElement>
        </InputGroup>
    )
}
export default PasswordInput;