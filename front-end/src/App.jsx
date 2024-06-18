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

  const [redditMin, setRedditMin] = useState({});
  const [redditNeutral, setRedditNeutral] = useState({});
  const [redditMax, setRedditMax] = useState({});
  const [redditMinDate, setRedditMinDate] = useState("");
  const [redditNeutralDate, setRedditNeutralDate] = useState("");
  const [redditMaxDate, setRedditMaxDate] = useState("");
  
  const [comment, setComment] = useState("");
  const [responseNOW, setResponseNOW] = useState([]);

  const [data, setData] = useState([]);
  const [error, setError] = useState(false);
  
  let candidatePost = {};
  let formattedDate;

  async function sendRequest() {
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    // let url= 'http://127.0.0.1:8000/politician' + searchValue;
    // fetch(url)
    // .then(response => {
    //   if (!response.ok) {
    //     throw new Error('Network response was not ok');
    //   }
    //   return response.json();
    // })
    // .then(data => {

    //   // let today = new Date()
    //   // formattedDate = data.date[6] + data.date[7] + '/' + data.date[4] + data.date[5] + '/' + data.date[0] + data.date[1] + data.date[2] + data.date[3];
    //   setWaiting(false);
    // })
    // .catch(error => {
    //   setError(error);
    //   setWaiting(false);
    // });
    setOnSubmit(true);
    setWaiting(false);
  }

  const handleInputChange = (event) => {
    setSearchValue(event.target.value);
    setError(event.target.value.length === 0)
  };

  const handlePresetInput = async (name) => {
    setRealTimeRequest(false);
    setSearchValue(name);
    setWaiting(true);

    // const auxComment = (await fetch(`http://127.0.0.1:8000/comment/${searchValue}`));
    // setComment(await auxComment.json);

    sendRequest();
  }

  const handleFormInput = async () => {
    setRealTimeRequest(true);
    
    setProgress(0);
    setprogressTarget(0);

    setWaiting(true);   
    try {
      const response = await fetch(`http://127.0.0.1:8000/politician_NOW/${searchValue}`);
      // const auxComment = await fetch(`http://127.0.0.1:8000/comment/${searchValue}`);
      // setComment(await auxComment.text());
      
      const data = await response.json();
      console.log(data)
      const newEstadisticas = data.stats.map(stat => stat.Reputation * 100);
      setResponseNOW(newEstadisticas);

      setData(data)
      setRedditMin(data["min"])
      setRedditNeutral(data["neutral"])
      setRedditMax(data["max"])
      setprogressTarget(data["average_reputation"])

    } catch (error) {
      console.error("Error fetching data: ", error);
    }

    sendRequest();
  }

  function reset() {      
    window.scrollTo({
      top: 0,
    behavior: "smooth",
    });
    setProgress(0)
    setprogressTarget(0)
    setWaiting(false);
    setOnSubmit(false);
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
      const increment = progressTarget / 20;
      const interval = setInterval(() => {
        setProgress((prev) => {
          setNextValue(prev + increment);
          if (nextValue >= progressTarget) {
            clearInterval(interval);
            return progressTarget;
          }
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
  }, [realTimeRequest])

  // useEffect(() => {
  //   let url = 'http://127.0.0.1:8000/politician/' + searchValue;

  //   fetch(url)
  //     .then(response => response.json())
  //     .then(data => {

  //     }).catch(error => {
  //       setError(error);
  //       setWaiting(false);
  //     });
  // }, [])


  useEffect(() => {
    let url = 'http://127.0.0.1:8000/politician/' + searchValue;

    fetch(url)
      .then(response => response.json())
      .then(data => {
        setRedditMin(data["min"])
        setRedditNeutral(data["neutral"])
        setRedditMax(data["max"])
        setprogressTarget(data["average_reputation"])

      })
      .catch(error => {
        console.error('Error:', error);
      });
  }, [searchValue]);



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
                <Text id='progress-indicator' _hover={{cursor:"default"}} align="center" fontSize="2rem" fontWeight={600} marginTop="5%">{Math.trunc(progressTarget* 100)}%</Text>
              </Flex>
                {/* <Text id="progress-comment" fontSize="1.5em" position="absolute" bottom="0" width="70%" bg="none" fontWeight={500} align="center" _hover={{cursor:"default"}}></Text> */}
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

                <Grid className="idea-container-content" marginTop="0%" padding="5%" templateColumns="repeat(4, minmax(20%, 1fr))" gap={10} left="15%">
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
                
                <Grid className="idea-container-content" marginTop="0%" padding="5%" templateColumns="repeat(4, minmax(20%, 1fr))" gap={10} left="15%">
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
              <Stat name={searchValue} type={realTimeRequest} response={responseNOW}>
              </Stat>
              <Flex direction="row" width="100%" height="100%" justifyContent="space-around" align="center">
                {!realTimeRequest && <StatComparison name={searchValue} candidateOne={searchValue === 'Donald Trump' ? 'Joe Biden' : 'Donald Trump'}/>}
                {!realTimeRequest && <StatComparison name={searchValue} candidateOne={searchValue === 'Donald Trump' ? 'Kamala Harris' : 'Ted Cruz'}/>}
              </Flex>
            </Flex>

            <Flex position="relative" justify="center" height="40%"  width="100%">
              <Flex direction="column" position="absolute" top="50%" left="5%" transform="translateY(-50%)">
                {/* <Button bg="none" color="#f2e3d6" _hover={{bg:"#45bdce"}}>Best</Button>
                <Button bg="none" color="#f2e3d6" _hover={{bg:"#45bdce"}}>Neutral</Button>
                <Button bg="none" color="#f2e3d6" _hover={{bg:"#45bdce"}}>Worst</Button> */}
              </Flex>
              <Grid
  className="reddit-posts"
  width="75%"
  templateColumns="repeat(auto-fit, minmax(32%, 1fr))"
  gap={4}
  borderRadius={20}
  margin="5%"
  color="black"
  transition="opacity 0.35s ease-in-out"
>
  <Flex className="reddit-post-wrapper" bg="#" borderRadius={12} width="100%">
    <GridItem width="100%">
      <Text color="red" fontWeight={750} letterSpacing="3px" align="center">Worst</Text>
      <RedditPost
        title={redditMin["title"]}
        subreddit={"r/politics"}
        content={redditMin["comment"]}
        upvotes={redditMin["thumbsup"]}
        _hover={{}}
      />
    </GridItem>
    <GridItem width="100%">
      <Text color="white" fontWeight={750} letterSpacing="3px" align="center">Neutral</Text>
      <RedditPost
        title={redditNeutral["title"]}
        subreddit={"r/politics"}
        content={redditNeutral["comment"]}
        upvotes={redditNeutral["thumbsup"]}
        _hover={{}}
      />
    </GridItem>
    <GridItem width="100%">
      <Text color="#0ae448" fontWeight={750} letterSpacing="3px" align="center">Best</Text>
      <RedditPost
        title={redditMax["title"]}
        subreddit={"r/politics"}
        content={redditMax["comment"]}
        upvotes={redditMax["thumbsup"]}
        _hover={{}}
      />
    </GridItem>
  </Flex>
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
                <Text marginTop="5%" maxWidth="40%" textAlign="center" fontWeight="100"> Obtén el estatus de tu candidato favorito en los últimos minutos. </Text>
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
                {/* <Slider id='slider' defaultValue={0} min={0} max={1000} colorScheme='teal' onChange={(v) => setSliderValue(v)} onMouseEnter={() => setShowTooltip(true)} onMouseLeave={() => setShowTooltip(false)} width="50%" marginTop="3%" marginLeft="25%">
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
                </Slider> */}
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