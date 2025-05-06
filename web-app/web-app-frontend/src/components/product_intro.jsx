// src/components/ProductIntro.jsx

import { Box, SimpleGrid, Text, UnorderedList, ListItem, Image } from '@chakra-ui/react'
import editorsIcon from '../assets/editors-icon.png'

const ProductIntro = () => {
  return (
    <Box px={8} py={12}>
      <SimpleGrid columns={[1, null, 2]} spacing={10} alignItems="center">
        
        {/* Left Column: Text Description */}
        <Box>
          <Text fontSize="6xl" fontWeight="bold" mb={5}>
            Create YouTube Ready Gaming Videos in Minutes
          </Text>
          <Text fontWeight="semibold" fontSize="2xl" mb={5}>
            Our tool watches your raw footage <br /> and creates a high quality final video by:
          </Text>
          <UnorderedList fontWeight="medium" spacing={2} fontSize="md">
            <ListItem>Placing clips in timeline</ListItem>
            <ListItem>Trimming off fluff</ListItem>
            <ListItem>Take Your Video to the Next Level by adding:</ListItem>
            <ListItem> Well-Timed Transitions </ListItem>
            <ListItem>Eye-Catching Animations</ListItem>
            <ListItem>Hilarious Sound Effects</ListItem>
            <ListItem>Engaging Zoom Cuts</ListItem>
          </UnorderedList>
        </Box>

        {/* Right Column: Video + Image */}
        <Box textAlign="center">
          <Text fontSize="2xl" fontWeight="semibold" color="rgb(255, 102, 0)" 
          _hover={{ color: 'rgb(52, 165, 235)' }}>
            Demonstration
          </Text>
          
          {/* Embed a YouTube or local video */}
          <Box mb={6}>
            <iframe
              width="100%"
              height="315"
              src="https://www.youtube.com/embed/YOUR_VIDEO_ID"
              title="Product demo"
              frameBorder="0"
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
              allowFullScreen
              style={{ borderRadius: '12px' }}
            />
          </Box>

          {/* Compatibility image */}
          <Image 
            src={editorsIcon} 
            alt="Compatible with Da Vinci Resolve on Mac"
            maxW="250px"
            p="10px"
            mx="auto"
            mr="40px"
            borderRadius={50}
            boxShadow="lg"
          />
        </Box>

      </SimpleGrid>
    </Box>
  )
}

export default ProductIntro
