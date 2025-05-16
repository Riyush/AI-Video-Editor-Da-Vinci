import React from "react";
import { Card, CardBody, CardFooter, CardHeader, Image, VStack, Text, Box } from "@chakra-ui/react";

function PresetCard({ imageLink, title, description, cardLabel, navigate, page }) {
  return (
    <Box 
    position="relative" 
    cursor="pointer" 
    onClick={() => {navigate(page)}}
    transition="all 0.2s ease-in-out"
    _hover={{
    transform: 'scale(1.03)',
    boxShadow: 'lg',
  }}
  >
    <Card 
      maxW="sm" // small max width for consistent sizing
      borderWidth="1px"
      borderRadius="lg"
      overflow="hidden"
      boxShadow="md"
      w="28vw"
    >
      {/* Diagonal label if cardLabel exists */}
        {cardLabel && (
          <Box
            position="absolute"
            top="10px"
            right="-30px"
            bg="green.400"
            color="white"
            px={2}
            py={1 }
            transform="rotate(45deg)"
            fontSize="xs"
            fontWeight="bold"
            zIndex="1"
            width="100px"
            textAlign="center"
            boxShadow="md"
          >
            {cardLabel}
          </Box>
        )}
        
        <Image 
          src={imageLink} 
          alt={title} 
          objectFit="cover"
          height="160px" // fix image height
          width="100%"
        />
      <CardBody p={0} >
        
        <VStack 
        spacing={2} p = {4} align="center"
        bgGradient="radial(blue.50, cyan.200)"
        >
          <Text fontWeight="bold" fontSize="lg">
            {title}
          </Text>
          <Text fontSize="sm" color="gray.600">
            {description}
          </Text>
        </VStack>
      </CardBody>
    </Card>
    </Box>
  );
}

export default PresetCard;