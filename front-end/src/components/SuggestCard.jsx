import { Flex, Image, Box, Text, Button, Icon } from "@chakra-ui/react";

export default function SuggestCard( props ) {
    return(
        <Flex direction="column">
            {/* <Flex className="suggest-card-header"></Flex> */}
            <Image src={props.candidateImage} alt={props.candidateName} borderRadius="full" height="auto" width="auto"/>
            <Text marginTop= "3px"align="center"fontWeight="600"> {props.candidateName}</Text>
        </Flex>
    )
}