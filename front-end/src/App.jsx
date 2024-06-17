import "./styles/App.css";
import React, { useState, useEffect } from "react";
import { zoomies } from 'ldrs';

import { Flex, Text, Divider, Grid, GridItem, Img, Button, Heading, Input } from "@chakra-ui/react";
import {
  FormControl,
  FormLabel,
  FormErrorMessage,
  FormHelperText,
} from '@chakra-ui/react'

import {
  Slider,
  SliderTrack,
  SliderFilledTrack,
  SliderThumb,
  Tooltip as ChakraTooltip,
} from '@chakra-ui/react'

import { CloseIcon, SearchIcon } from '@chakra-ui/icons';

import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title,  Tooltip as ChartTooltip, Legend } from 'chart.js';

import Stat from './components/Stat';
import StatComparison from './components/StatComparison';
import RedditPost from "./components/RedditPost";
import SuggestCard from "./components/SuggestCard";

import candidates from "./politicians.json"
import redditPosts from "./redditPosts.json"
import results from "./results.json"

import backgroundImageBlue from './istockphoto-1432473911-170667a.webp';
import backgroundImageGreen from './abstract-gradient-neon-lights_23-2149279161.jpg';

zoomies.register()
ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, ChartTooltip, Legend);

function App() {
  const logo = "./logoWir.png";
  const [searchValue, setSearchValue] = useState("");
  const [onSubmit, setOnSubmit] = useState(false);
  const [waiting, setWaiting] = useState(false);
  const [progress, setProgress] = useState(0);
  const [progressTarget, setprogressTarget] = useState(0);
  const [nextValue, setNextValue] = useState(0);
  
  const [realTimeRequest, setRealTimeRequest] = useState(false);

  const [sliderValue, setSliderValue] = useState(0);
  const [showTooltip, setShowTooltip] = useState(false);

  const [data, setData] = useState([]);
  const [error, setError] = useState(false);
  
  let candidatePost = {};
  let formattedDate;


  const handleInputChange = (event) => {
    setRealTimeRequest(true);
    setSearchValue(event.target.value);
    setError(event.target.value.length === 0)
  };

  const handlePresetInput = (name) => {
    setRealTimeRequest(false);
    setSearchValue(name);

    setProgress(0);
    setprogressTarget(0);

    setWaiting(true);
    sendRequest(name);
  }

  const handleFormInput = () => {
    setRealTimeRequest(true);
    
    setProgress(0);
    setprogressTarget(0);

    setWaiting(true);   

    sendRequest(searchValue);
  }

  // const formSubmit = (event) => {
  //   event.preventDefault();
  //   if (searchValue.trim() !== "") {
  //     sendRequest(searchValue);
  //   } else {
  //     setError(true);
  //   }
  // };

  useEffect(() => {
    if (progressTarget > 0) {
      var elm = document.querySelector('#progress-indicator');

      const increment = progressTarget / 20;
      const interval = setInterval(() => {
        setProgress((prev) => {
          setNextValue(prev + increment);
          if (nextValue >= progressTarget) {
            clearInterval(interval);
            return progressTarget;
          }
          if(elm !== null)
            elm.innerHTML = Math.round(progressTarget * 100) + '%';
          return nextValue;
        });
      }, 10);
      return () => clearInterval(interval);
    }
  }, [progressTarget, nextValue]);

  useEffect(() => {
    if(!waiting){
      window.scrollTo({
        top: 85,
        behavior: "smooth",
      });
    }
  }, [progressTarget])

  // useEffect(() => {

  // }, []);
    
  async function sendRequest(name) {
  // Simulate long-running function
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    let url= 'http://127.0.0.1:8000/politician'
    fetch(url)
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    })
    .then(data => {
      setData(data);
      setprogressTarget(data[name]);
      formattedDate = data.date[6] + data.date[7] + '/' + data.date[4] + data.date[5] + '/' + data.date[0] + data.date[1] + data.date[2] + data.date[3];
      setWaiting(false);
    })
    .catch(error => {
      setError(error);
      setWaiting(false);
    });
    // switch (name) {
    //   case "Donald Trump": setprogressTarget(0.5); break;
    //   case "Joe Biden": setprogressTarget(0.85); break;
    //   case "Nancy Pelosi": setprogressTarget(0.2); break;
    //   default: setprogressTarget(parseInt(name));
    // }
    setOnSubmit(true);
    setWaiting(false);
  }

  function reset() {      
    window.scrollTo({
      top: 0,
    behavior: "smooth",
    });

    setWaiting(false);
    setOnSubmit(!onSubmit);
    }

    const maxItems = 3;
    redditPosts = redditPosts.slice(0, maxItems);
    const greenBackground = '../abstract-gradient-neon-lights_23-2149279161.jpg'

  return (
    <Flex className="App" display="inline" position="relative" color="white" overflow="hidden" height="fit-content" width="100vh">
        <Flex className="top-bg" bgImage={onSubmit && realTimeRequest ? backgroundImageGreen : backgroundImageBlue} bgSize="cover" position="relative" direction="column" minHeight="100vh" height="fit-content" alignItems="center">
          <Flex className="header" position="relative" direction="column" alignItems="center" justifyContent="space-around" width="100%" marginTop="10vh">
            <Flex direction="column" align="center" className={onSubmit && !waiting ? "moved" : ""} width="100%">
              <Heading className="main-Title" _hover={{cursor:"default"}}> Reputation Analyzer</Heading>
              <Img id="scroll-point" src={logo} className="logo" alt="logoWir" paddingTop="2%" />
            </Flex> 

            {onSubmit && !waiting &&
            <Flex className="progress-wrapper" direction="row" position="relative" transition="opacity 0.2s ease-in-out" height="30vh" width="100%">
              <Flex direction="column" width="100%" align="center">
                <Flex direction="row" position="relative" width="60%" justifyContent="center" align="center">
                  <progress id="progress-comment" className="progressBar" value={progress} max={1}></progress>
                  <CloseIcon color="#a7222c" onClick={reset} position="relative"
                   right="-10px"  _hover={{color:"red", transform: 'scale(1.3)', transitionDuration: '100ms', WebkitTransform: 'scale(1.3)'}}/>      
                </Flex>
                <Text id='progress-indicator' _hover={{cursor:"default"}} position="relative" left="25%">0%</Text>
              </Flex>
                <Text id="progress-comment" fontSize="2em" position="absolute" bottom="0" bg="none" _hover={{cursor:"default"}}>as</Text>
            </Flex>}

            {waiting &&
            <Flex margin="15%">
              <l-zoomies position="absolute" size="150" stroke="2" bg-opacity="0" speed="0.7" color="cyan"></l-zoomies>
            </Flex>}
          </Flex> 

          <Flex className="idea-container" marginBottom={1} transition="opacity 0.35s ease-in-out" direction="column" width="80%" marginTop="7vh" display={!onSubmit && !waiting? "" : "none"}>
            <Flex direction="row" alignItems="start" marginTop="2%" justifyContent="center">
              <Flex direction="column" width="30%" marginRight="5%">
                <Divider borderColor="gray.300" ></Divider>
                <Text className="party-name-text" margin="5%" align="center"> Republican Party </Text>

                <Grid className="idea-container-content" marginTop="0%" padding="5%" templateColumns="repeat(auto-fit, minmax(20%, 1fr))" gap={10} left="15%">
                  {candidates.filter(candidate => candidate.party === 'Republican Party').map((candidate, index) => (
                    <GridItem key={index} _hover={{ cursor: "grab" }} onClick={() => handlePresetInput(candidate.name)}>
                      <SuggestCard  candidateName={candidate.name} candidateImage={candidate.image} />
                    </GridItem>
                  ))}
                </Grid>
              </Flex>
              <Flex  zindex="1" direction="column" width="30%" marginLeft="5%">
                <Divider borderColor="gray.300" ></Divider>
                <Text className="party-name-text" margin="5%" align="center" _hover={{cursor:'default'}}> Democratic Party</Text>
                
                <Grid className="idea-container-content" marginTop="0%" padding="5%" templateColumns="repeat(auto-fit, minmax(20%, 1fr))" gap={10} left="15%">
                  {candidates.filter(candidate => candidate.party === 'Democratic Party').map((candidate, index) => (
                    <GridItem key={index} _hover={{ cursor: "grab" }} onClick={() => handlePresetInput(candidate.name)}>
                      <SuggestCard candidateName={candidate.name} candidateImage={candidate.image} />
                    </GridItem>
                  ))}
                </Grid>
              </Flex>
            </Flex>
          </Flex>
        </Flex>
        <Flex className={`lower-bg ${!onSubmit && !waiting ? "lower-no-submit" : waiting ? "" : "lower-submit"}`} bg={!onSubmit ? undefined : realTimeRequest ? "#002a29" : "#051b33"} direction="column" alignItems="center" width="100%">
          {onSubmit && !waiting && (     // SEGUNDA PANTALLA  ** REDDIT POSTS STATS **
            <>
            <Flex direction="column" align="center" marginTop="5%" width="100%">
              <Stat name={searchValue}>
              </Stat>
              <Flex direction="row" width="100%" height="100%" justifyContent="space-around" align="center">
                <StatComparison name={searchValue}/>
                <StatComparison name={searchValue}/>
              </Flex>
            </Flex>

            <Flex position="relative" justify="center" height="40%"  width="100%">
              <Flex direction="column" position="absolute" top="50%" left="5%" transform="translateY(-50%)">
                <Button bg="none" color="#f2e3d6" _hover={{bg:"#45bdce"}}>Best</Button>
                <Button bg="none" color="#f2e3d6" _hover={{bg:"#45bdce"}}>Neutral</Button>
                <Button bg="none" color="#f2e3d6" _hover={{bg:"#45bdce"}}>Worst</Button>
              </Flex>
              <Grid className="reddit-posts" width="75%" templateColumns="repeat(auto-fit, minmax(32%, 1fr))" gap={4} borderRadius={20} margin="5%" color="black" transition="opacity 0.35s ease-in-out" >
                {redditPosts.map((post, index) => (
                  // <Flex className="reddit-post-wrapper" bg="#ff9a00" borderRadius={12}>
                  <GridItem key={index}>
                    <Flex direction="column" justifyContent="center">
                    {index===0 && <Text color="red" fontWeight={750} letterSpacing="3px" align="center"> Worst </Text>}
                    {index===1 && <Text color="white" fontWeight={750} letterSpacing="3px" align="center"> Neutral </Text>}
                    {index===2 && <Text color="#0ae448" fontWeight={750} letterSpacing="3px" align="center"> Best </Text>}
                      <RedditPost title={post.title} subreddit={post.subreddit} date={post.date} content={post.content} upvotes={post.upvotes} _hover={{}} />
                    </Flex>
                  </GridItem>
                  // </Flex>
                ))}  
                  {/* <GridItem key={57}>
                    <RedditPost name={data.name} title={data.title} subreddit={data.subreddit} date={formattedDate} content={data.text === 'No text available.' ? data.text : ''} upvotes={data.thumbsup} _hover={{}} />
                    </GridItem> */}
              </Grid>
            </Flex>
            </>
          )
          }
          {!onSubmit && !waiting && (               // REAL TIME ANALYZER
            <>
            <Flex className="header" position="relative" direction="column" alignItems="center" justifyContent="center" width="100%" marginTop="10vh" height="fit-content">
              <Flex direction="column" align="center" className={onSubmit && !waiting ? "moved" : ""} width="100%">
                <Heading className="main-Title" _hover={{cursor:"default"}}> Real Time Analyzer</Heading>
                <Text marginTop="5%" maxWidth="40%" textAlign="center" fontWeight="100"> Define un tiempo de búsqueda y obtén el estatus de tu candidato favorito en los últimos minutos. </Text>
              </Flex> 
            </Flex> 

            <Flex className="lower-body" align="center" direction="column" position="relative"justifyContent="center" height="60%" width="100%">
              <form onSubmit={handleFormInput}>
                <FormControl isRequired isInvalid={error}>
                  <Input placeholder="Ingrese su búsqueda"  width="60vh" fontSize="1rem" color="white"  onChange={handleInputChange}></Input>
                  {error ? <FormErrorMessage> Por favor ingrese un político </FormErrorMessage> : ""}
                  <Button type="submit" bg="none" color="white" position="absolute">
                    <SearchIcon/>
                  </Button>
                </FormControl>
                <Slider id='slider' defaultValue={0} min={0} max={1000} colorScheme='teal' onChange={(v) => setSliderValue(v)} onMouseEnter={() => setShowTooltip(true)} onMouseLeave={() => setShowTooltip(false)} width="50%" marginTop="3%" marginLeft="25%">
                  <SliderTrack>
                    <SliderFilledTrack />
                  </SliderTrack>
                  <ChakraTooltip
                    hasArrow
                    bg='teal.500'
                    color='white'
                    placement='top'
                    isOpen={showTooltip}
                    label={`${sliderValue} posts`}
                  >
                    <SliderThumb />
                  </ChakraTooltip>
                </Slider>
              <Text align="center" fontSize="0.7rem" fontWeight="100" marginTop="5%"> Tiempo promedio análisis por cada 10 posts - 3 segundos</Text>
              </form>
            </Flex>
            </>
          )}
        </Flex>
    </Flex> 
  );
}

export default App;