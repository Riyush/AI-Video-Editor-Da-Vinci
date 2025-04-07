import { Flex, Button, Heading, Spacer, VStack,Text } from '@chakra-ui/react';
import { Link } from 'react-router-dom';

function Navbar() {
  return (
    <Flex
      as="nav"
      justify="space-between"
      align="center"
      p={4}
      bgGradient="linear(to-r, gray.800, teal.900)"
      color="white"
      boxShadow="md"
      pb={2}
    >
      <Heading mr = {6} size="md">AI Editor</Heading>
      <Flex gap={6}>
        <Link to="/">Home</Link>
        <Link to="/features">Features</Link>
        <Link to="/pricing">Pricing</Link>
      </Flex>
      <Spacer /> {/* Pushes buttons to the right */}
      <Flex gap={4}>
        <VStack spacing ={.5}>
        <Button as={Link} to="/register" colorScheme="teal" variant="solid">
          Free Download
        </Button>
        <Text fontWeight='bold' fontSize='xs' textColor='orange' textShadow = '1px 1px #ff0000'>14 day Free Trial</Text>
        </VStack >
        <Button as={Link} to="/login" colorScheme="teal" variant="outline">
          Customer Login
        </Button>
      </Flex>
    </Flex>
  );
}

export default Navbar;