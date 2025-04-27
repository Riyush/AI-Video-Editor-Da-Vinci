import React from 'react';
import {InputGroup, InputLeftElement, Input} from '@chakra-ui/react';
import {EmailIcon} from '@chakra-ui/icons';

function EmailInput({value, onChange}){
    return (
        <InputGroup
            w = "70vw"
            >
            <InputLeftElement pointerEvents='none'>
            <EmailIcon color='gray.300'/> 
            </InputLeftElement>
            <Input 
                placeholder='Email Address'
                value={value}
                onChange={onChange}
                variant='filled' 
                bg='gray.200'
                _focus={{ bg: 'gray.50' }}
                borderRadius="20px"
                />
        </InputGroup>
    )
}
export default EmailInput;