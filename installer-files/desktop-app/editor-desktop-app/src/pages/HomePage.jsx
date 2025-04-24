import React from 'react';
import { Box, SimpleGrid, Text, Image, Button, Flex } from '@chakra-ui/react';
import launchDemoImage from '../assets/GameTime_Launch_Demo.png';

function Home() {
  return (
    <Box 
    minH="100vh" // full height of screen
    bgGradient="radial(black, gray.700)">
      <Text 
      textAlign={"center"}
      bgGradient='linear(to-b, white, cyan.200)'
      bgClip='text'
      fontSize='4xl'
      fontWeight='extrabold'
      >Launch GameTime on <br /> DaVinci Resolve</Text>
      <Text
      textAlign={"center"}
      textColor={"gray.400"}
      pt="10px"
      >From Top Menu:</Text>
      <Text
      textAlign={"center"}
      textColor={"white"}
      >Workspace &gt; Scripts &gt; GameTime</Text>
      <Flex
      justify="center" align="center">
      <Image
      src={launchDemoImage}
      alt="Demo Image"
      objectFit="contain"

      boxSize="330px" // or use width/height
      maxW="400px"
      />
      </Flex>
      
    </Box>
  );
}

export default Home;