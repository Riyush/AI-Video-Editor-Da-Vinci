import { Box, Heading, Text, Button, VStack, HStack } from '@chakra-ui/react';
import { Link } from 'react-router-dom';
import ProductIntro from '../components/product_intro.jsx';

function Home() {
  return (
    <ProductIntro></ProductIntro>

/*
    <Box p={8} textAlign="center" bg="gray.100" minH="100vh">
      <VStack spacing={6}>
        <Heading as="h1" size="2xl" color="teal.600">
          Welcome to AI Video Editor
        </Heading>
        <Text fontSize="xl" color="gray.700">
          Edit videos with the power of AI—fast, simple, brilliant.
        </Text>
        <Button as={Link} to="/register" colorScheme="teal" size="lg" px={8}>
          Free Download
        </Button>
      </VStack>
    </Box>
*/
  );
}

export default Home;