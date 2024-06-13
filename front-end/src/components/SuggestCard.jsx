import { Flex, Image, Box, Text, Button, Icon } from "@chakra-ui/react";

export default function SuggestCard( props ) {
    return(
        <Flex direction="column">
            {/* <Flex className="suggest-card-header"></Flex> */}
            <Flex overflow="hidden" borderRadius="full" height="auto" width="auto">
              <Image _hover={{
        transform: 'scale(1.3)',
        transitionDuration: '600ms',
        WebkitTransform: 'scale(1.3)'
      }} src={props.candidateImage} alt={props.candidateName} borderRadius="full" height="auto" width="auto"/>
            </Flex>
            <Text marginTop= "3px"align="center"fontWeight="600"> {props.candidateName}</Text>
        </Flex>
    )
}