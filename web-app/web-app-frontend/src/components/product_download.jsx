import { Box, SimpleGrid, Text, UnorderedList, ListItem, Image, HStack } from '@chakra-ui/react'
import checkIcon from '../assets/check-icon.png';
import DownloadButton from '../components/download_button.jsx';

const ProductDownload = () => {
  return (
    <Box px={8} py={12} mt={20}>
      <SimpleGrid columns={[1, null, 2]} spacing={10} alignItems="center">
        
        {/* Left Column: Text Description */}
        <Box ml={10}>
            <Text fontSize="5xl" fontWeight="bold" mb={5}>
                Download AI Gaming Editor Extension
            </Text>
            <UnorderedList fontWeight="light" spacing={3} fontSize="lg" styleType="none" ml = {0}>
                <ListItem>
                <HStack spacing={3}>
                    <Image src={checkIcon} boxSize="35px" />
                    <Text>Available on Mac</Text>
                </HStack>
                </ListItem>
                <ListItem>
                <HStack spacing={3}>
                    <Image src ={checkIcon} boxSize="35px"/>
                    <Text>Da Vinci Resolve 19 </Text>
                </HStack>
                </ListItem>
                <ListItem>
                <HStack spacing={3}>
                    <Image src = {checkIcon} boxSize="35px"/>
                    <Text>14 Day Free Trial</Text>
                </HStack>
                </ListItem>
          </UnorderedList>

        <DownloadButton></DownloadButton>
        </Box>

        {/* Right Column: Video + Image */}
        <Box textAlign="center">
          
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

        </Box>

      </SimpleGrid>
    </Box>
  )
}

export default ProductDownload
