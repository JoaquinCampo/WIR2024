import "../styles/RedditPost.css";
import { Flex, Image, Box, Text, Button, Icon } from "@chakra-ui/react";
import { faArrowUp, faArrowDown, faCircleUp, faCircleDown } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import ArrowUpwardIcon from '@mui/icons-material/ArrowUpward';
import ArrowDownwardIcon from '@mui/icons-material/ArrowDownward';
import { PiArrowFatDownThin } from "react-icons/pi";
import { PiArrowFatDownLight, PiArrowFatUpThin } from "react-icons/pi";
import { PiArrowFatUpLight } from "react-icons/pi";




export default function RedditPost (props) {


    return(
        <Flex direction="column" border='0' bg ='white' borderRadius={20} paddingY="5px" _hover={{bg: "#f2f4f5",transform: 'scale(1.1)', transitionDuration: '200ms', WebkitTransform: 'scale(1.1)'}}  cursor='pointer' margin="5px">
            <Flex className="header" paddingX={15} paddingY={2} align="center"> 
                <Image src="https://styles.redditmedia.com/t5_2qmvj/styles/communityIcon_ns64hvix3gu91.jpg?width=48&amp;height=48&amp;frame=1&amp;auto=webp&amp;crop=48:48,smart&amp;s=793f79f497f5b3029548de700f8965df10ecd3bf" srcSet="" boxSize="30px" alt="Icono de r/uruguay" borderRadius={20} />
                <Flex paddingLeft={15}> <Text>{props.subreddit} </Text></Flex>
                <Box mx={2} bg="#5c6c74" w="4px" h="4px" borderRadius="full" />
                <Flex> <Text>{props.date} </Text> </Flex>
            </Flex>

            <Flex paddingX="10%"><Text className="reddit-post-title" > {props.title}</Text></Flex>

            <Flex paddingX="10%" direction="column"> <Text>{props.content} </Text></Flex>
            
            <Flex className="reddit-upvote-container" marginX="10%" bg="#e5ebee" border="0" borderRadius={10} height="30px" width="fit-content">  
                <Box className="reddit-upvote-background" _hover={{bg:"#dbe4e9"}} borderRadius="full" height="30px" width="30px">
                    <PiArrowFatUpLight className="reddit-upvote-arrow"/>
                </Box>
                <Text> {props.upvotes} </Text>
                <Box className="reddit-upvote-background" _hover={{bg:"#dbe4e9"}} borderRadius="full" height="30px" width="30px">
                    <PiArrowFatDownLight className="reddit-downvote-arrow"/>
                </Box>
            </Flex>
            {/* <Button margin="3px" bg="#e5ebee" border="0" borderRadius={10} height="30px" width="30%"></Button>
            <Button margin="3px"  bg="#e5ebee" border="0" borderRadius={10} height="30px" width="30%"></Button> */}


        </Flex>
    )
}